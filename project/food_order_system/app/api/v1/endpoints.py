import json
import re
import random
import httpx
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_, select, not_
from sqlalchemy.sql import operators
from app.core.core import authenticate_user, create_access_token, get_current_user, get_password_hash
from app.db.db import get_db, get_db_recommendation
from app.models.models import User, Restaurant, Option, Review, Selection, AdminSettings, SelectedRestaurantLog
from app.schemas.schemas import UserCreate, UserLogin, Token, RestaurantCreate, OptionCreate, ReviewCreate, UserSelectionCreate, ExclusionDaysInput
from app.core.config import settings
from app.schemas.schemas import (
    UserCreate, UserLogin, Token, RestaurantCreate, 
    OptionCreate, ReviewCreate, UserSelectionCreate, 
    ExclusionDaysInput
)

router = APIRouter()

# 사용자 관련 엔드포인트
@router.post("/users", response_model=Token)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = User(
        email="admin@biobrain.com",
        hashed_password=get_password_hash("1q2w3e4r1!"),
        is_admin=True
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    db_user = await authenticate_user(user.email, user.password, db)
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/auth/refresh-token")
async def refresh_token(current_user: User = Depends(get_current_user)):
    access_token = create_access_token(data={"sub": current_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/auth/login", response_model=Token)
async def login_auth(user: UserLogin, db: AsyncSession = Depends(get_db)):
    db_user = await authenticate_user(user.email, user.password, db)
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# 레스토랑 관련 엔드포인트
@router.post("/restaurants", response_model=RestaurantCreate)
async def create_restaurant(restaurant: RestaurantCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db_restaurant = Restaurant(**restaurant.dict())
    db.add(db_restaurant)
    await db.commit()
    await db.refresh(db_restaurant)
    return db_restaurant

@router.get("/restaurants")
async def get_restaurants_public(db: AsyncSession = Depends(get_db)):
    query = select(Restaurant)
    result = await db.execute(query)
    restaurants = result.scalars().all()
    return restaurants

# 옵션 관련 엔드포인트
@router.post("/options", response_model=OptionCreate)
async def create_option(option: OptionCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db_option = Option(**option.dict())
    db.add(db_option)
    await db.commit()
    await db.refresh(db_option)
    return db_option

@router.get("/options")
async def get_options(category: str = None, db: AsyncSession = Depends(get_db)):
    try:
        query = select(Option)
        if category:
            query = query.where(Option.category == category)
        result = await db.execute(query)
        options = result.scalars().all()
        
        unique_options = {f"{opt.category}_{opt.name}": {
            "id": opt.id,
            "name": opt.name,
            "category": opt.category
        } for opt in options}
        
        options_list = list(unique_options.values())
        random.shuffle(options_list)
        
        return options_list
    except Exception as e:
        print(f"Error in get_options: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# 리뷰 관련 엔드포인트
@router.post("/reviews", response_model=ReviewCreate)
async def create_review(review: ReviewCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_review = Review(**review.dict(), user_id=current_user.id)
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    return db_review

# 사용자 선택 관련 엔드포인트
@router.post("/user-selections", response_model=UserSelectionCreate)
async def create_user_selection(selection: UserSelectionCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_selection = Selection(**selection.dict(), user_id=current_user.id)
    db.add(db_selection)
    await db.commit()
    await db.refresh(db_selection)
    return db_selection

# 추천 관련 엔드포인트
@router.post("/recommendations")
async def get_recommendations(selected_options: dict, db: AsyncSession = Depends(get_db)):
    try:
        print("\n=== Recommendation Request ===")
        print("Received selected options:", selected_options)
        
        excluded_restaurants = await SelectedRestaurantLog.get_excluded_restaurants(db)
        excluded_restaurants.extend(selected_options.get('excludedRestaurants', []))
        
        options = process_selected_options(selected_options)
        
        if not options:
            return JSONResponse(status_code=400, content={"error": "선택된 옵션이 없습니다."})

        # 분류가 선택된 경우, 다른 조건은 무시
        category_option = next((opt for opt in options if opt['category'] == '분류'), None)
        if category_option and category_option['name'] != '무관':
            options = [category_option]

        query = build_restaurant_query(options, excluded_restaurants)
        available_restaurants = await execute_query(db, query)

        # 결과가 없으면 조건을 점진적으로 완화
        if not available_restaurants:
            for i in range(len(options) - 1, -1, -1):
                query = build_restaurant_query(options[:i], excluded_restaurants)
                available_restaurants = await execute_query(db, query)
                if available_restaurants:
                    break

        # 여전히 결과가 없으면 모든 식당 중에서 선택
        if not available_restaurants:
            query = select(Restaurant)
            if excluded_restaurants:
                query = query.where(not_(Restaurant.name.in_(excluded_restaurants)))
            available_restaurants = await execute_query(db, query)

        if not available_restaurants:
            return JSONResponse(
                status_code=404,
                content={"error": "조건에 맞는 식당이 없습니다.", "message": "다른 조건을 선택해주세요."}
            )

        best_match = random.choice(available_restaurants)
        print(f"Selected restaurant: {best_match.name}")

        if best_match.name not in excluded_restaurants:
            excluded_restaurants.append(best_match.name)

        conditions = [f"{opt['category']}: {'상관없음' if opt['name'] == '무관' else opt['name']}" for opt in options]
        ai_recommendation = await get_ai_recommendation(conditions, excluded_restaurants)

        return {
            "db_recommendation": restaurant_to_dict(best_match),
            "ai_recommendation": ai_recommendation,
            "matched_info": {
                "total_conditions": len(options),
                "matched_conditions": len([opt for opt in options if opt['name'] != '무관']),
                "matched_details": [f"{opt['category']}: {'상관없음' if opt['name'] == '무관' else opt['name']}" for opt in options],
                "excluded_count": len(excluded_restaurants),
                "total_available": len(available_restaurants)
            },
            "excluded_restaurants": excluded_restaurants
        }

    except Exception as e:
        print(f"Error in recommendations: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "추천을 처리하는 중 오류가 발생했습니다.", "detail": str(e)}
        )

# 관리자 기능
@router.get("/admin/restaurants")
async def get_restaurants(db: AsyncSession = Depends(get_db)):
    query = select(Restaurant)
    result = await db.execute(query)
    restaurants = result.scalars().all()
    return restaurants

@router.post("/admin/restaurants")
async def add_restaurant_admin(restaurant: RestaurantCreate, db: AsyncSession = Depends(get_db)):
    db_restaurant = Restaurant(**restaurant.dict())
    db.add(db_restaurant)
    await db.commit()
    await db.refresh(db_restaurant)
    return db_restaurant

@router.delete("/admin/restaurants/{restaurant_id}")
async def delete_restaurant_admin(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Restaurant).where(Restaurant.id == restaurant_id)
    result = await db.execute(query)
    restaurant = result.scalar_one_or_none()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    await db.delete(restaurant)
    await db.commit()
    return {"ok": True}

@router.get("/admin/options")
async def get_all_options_admin(db: AsyncSession = Depends(get_db)):
    query = select(Option)
    result = await db.execute(query)
    options = result.scalars().all()
    return options

@router.post("/admin/options")
async def add_option_admin(option: OptionCreate, db: AsyncSession = Depends(get_db)):
    db_option = Option(**option.dict())
    db.add(db_option)
    await db.commit()
    await db.refresh(db_option)
    return db_option

@router.delete("/admin/options/{option_id}")
async def delete_option_admin(option_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Option).where(Option.id == option_id)
    result = await db.execute(query)
    option = result.scalar_one_or_none()
    if not option:
        raise HTTPException(status_code=404, detail="Option not found")
    await db.delete(option)
    await db.commit()
    return {"ok": True}

@router.get("/admin/reviews")
async def get_reviews_admin(db: AsyncSession = Depends(get_db)):
    query = select(Review)
    result = await db.execute(query)
    reviews = result.scalars().all()
    return reviews

@router.post("/admin/reviews")
async def add_review_admin(review: ReviewCreate, db: AsyncSession = Depends(get_db)):
    db_review = Review(**review.dict())
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    return db_review

@router.delete("/admin/reviews/{review_id}")
async def delete_review_admin(review_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Review).where(Review.id == review_id)
    result = await db.execute(query)
    review = result.scalar_one_or_none()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    await db.delete(review)
    await db.commit()
    return {"ok": True}

@router.get("/admin/settings/exclusion-days")
async def get_exclusion_days(db: AsyncSession = Depends(get_db)):
    days = await AdminSettings.get_exclusion_days(db)
    return {"days": days}

@router.post("/admin/settings/exclusion-days")
async def set_exclusion_days(input_data: ExclusionDaysInput = Body(...), db: AsyncSession = Depends(get_db)):
    days = input_data.days
    if days < 1 or days > 30:
        raise HTTPException(status_code=400, detail="제외 기간은 1일에서 30일 사이여야 합니다.")
    
    setting = await AdminSettings.set_exclusion_days(db, days)
    return {"message": "설정이 저장되었습니다.", "days": int(setting.setting_value)}

@router.post("/selected-restaurants")
async def save_selected_restaurant(restaurant: dict, db: AsyncSession = Depends(get_db)):
    exclusion_days = await AdminSettings.get_exclusion_days(db)
    log = await SelectedRestaurantLog.add_selection(
        db, 
        restaurant["name"], 
        json.dumps(restaurant["options"]), 
        exclusion_days
    )
    return {"message": "선택된 식당이 저장되었습니다.", "exclude_until": log.exclude_until}

# 헬퍼 함수들
def process_selected_options(selected_options):
    if isinstance(selected_options.get('selectedOptions'), list):
        options = selected_options.get('selectedOptions', [])
    else:
        options = selected_options.get('selectedOptions', {}).get('selectedOptions', [])

    unique_options = {}
    for opt in reversed(options):
        category = opt.get('category')
        if category not in unique_options:
            unique_options[category] = opt
    
    return list(unique_options.values())

def build_restaurant_query(options, excluded_restaurants):
    query = select(Restaurant)
    non_mutual_options = [opt for opt in options if opt.get('name') != '무관']
    
    for option in non_mutual_options:
        category = option.get('category')
        name = option.get('name')
        
        if category == '분류':
            query = query.where(Restaurant.category == name)
        elif category == '도보/차량':
            if name in ['차', '차량']:
                query = query.where(Restaurant.transport.in_(['차', '차량']))
            else:
                query = query.where(Restaurant.transport == name)
        elif category == '주차장':
            query = query.where(Restaurant.parking == name)
        elif category == '룸':
            query = query.where(Restaurant.room == name)

    if excluded_restaurants:
        query = query.where(not_(Restaurant.name.in_(excluded_restaurants)))
    
    return query

async def execute_query(db, query):
    result = await db.execute(query)
    return result.scalars().all()

def restaurant_to_dict(restaurant):
    return {
        "name": restaurant.name,
        "address": restaurant.address,
        "category": restaurant.category,
        "parking": restaurant.parking,
        "main_menu": restaurant.main_menu,
        "room": restaurant.room,
        "transport": restaurant.transport
    }

async def get_ai_recommendation(conditions, excluded_restaurants):
    prompt = f"""
대전시기준으로 다음 조건에 맞는 실제 존재하는 식당을 하나만 추천해주세요.
정보가 제공되지 않은곳은 제외합니다.
조건:
{chr(10).join(f"- {condition}" for condition in conditions)}

다음 식당들은 반드시 제외해주세요: '{", ".join(excluded_restaurants)}'

아래 JSON 형식으로만 응답하고 추가 설명은 하지 마세요. 
{{
    "name": "식당이름",
    "address": "대전시 상세주소",
    "category": "분류",
    "parking": "주차 가능/불가",
    "main_menu": "대표 메뉴",
    "room": "룸 있음/없음",
    "transport": "도보/차량"
}}
"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.PERPLEXITY_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.1-sonar-huge-128k-online",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 300
                }
            )
        
        if response.status_code == 200:
            ai_content = response.json()['choices'][0]['message']['content'].strip()
            print(f"AI Raw Response: {ai_content}")
            json_match = re.search(r'\{[^}]+\}', ai_content)
            if json_match:
                return json.loads(json_match.group(0))
            else:
                raise ValueError("JSON 형식을 찾을 수 없습니다.")
        else:
            print(f"AI API Error Response: {response.text}")
            return create_default_ai_recommendation("AI 추천 실패")
    except Exception as e:
        print(f"AI Recommendation Error: {str(e)}")
        return create_default_ai_recommendation("AI 추천 오류")

def create_default_ai_recommendation(name):
    return {
        "name": name,
        "address": "대전시",
        "category": "정보 없음",
        "parking": "정보 없음",
        "main_menu": "정보 없음",
        "room": "정보 없음",
        "transport": "정보 없음"
    }

@router.post("/selected-restaurant")
async def save_selected_restaurant(restaurant: dict, db: AsyncSession = Depends(get_db)):
    exclusion_days = await AdminSettings.get_exclusion_days(db)
    selected_date = datetime.now().date()
    exclude_until = selected_date + timedelta(days=exclusion_days)
    
    new_selection = SelectedRestaurantLog(
        restaurant_name=restaurant["name"],
        selected_options=json.dumps(restaurant["options"]),
        selected_date=selected_date,
        exclude_until=exclude_until,
        category=restaurant["category"],
        address=restaurant["address"],
        parking=restaurant["parking"],
        main_menu=restaurant["main_menu"],
        room=restaurant["room"],
        transport=restaurant["transport"]
    )
    db.add(new_selection)
    await db.commit()
    await db.refresh(new_selection)
    return {"message": "선택된 식당이 저장되었습니다.", "exclude_until": exclude_until}

@router.get("/selected-restaurants")
async def get_selected_restaurants(db: AsyncSession = Depends(get_db)):
    query = select(SelectedRestaurantLog).order_by(SelectedRestaurantLog.selected_date.desc())
    result = await db.execute(query)
    selected_restaurants = result.scalars().all()
    return [restaurant_to_dict(restaurant) for restaurant in selected_restaurants]

@router.post("/reviews")
async def add_review(review: ReviewCreate, db: AsyncSession = Depends(get_db)):
    print("Received review:", review)  # 디버깅용 로그
    new_review = Review(**review.dict())
    db.add(new_review)
    try:
        await db.commit()
        await db.refresh(new_review)
        print("Review added successfully")  # 디버깅용 로그
        return {"message": "리뷰가 추가되었습니다.", "review_id": new_review.id}
    except Exception as e:
        print("Error adding review:", str(e))  # 디버깅용 로그
        await db.rollback()
        raise HTTPException(status_code=500, detail="리뷰 추가 중 오류가 발생했습니다.")



@router.get("/reviews/{restaurant_id}")
async def get_reviews(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Review).where(Review.restaurant_id == restaurant_id)
    result = await db.execute(query)
    reviews = result.scalars().all()
    return [{"id": review.id, "content": review.content, "rating": review.rating, "username": review.username, "created_at": review.created_at} for review in reviews]