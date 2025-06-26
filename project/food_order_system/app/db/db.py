from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from sqlalchemy.sql import text
import pandas as pd
from app.models.models import Restaurant, Option, Base
from sqlalchemy.future import select

engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def get_db_recommendation(db: AsyncSession, selected_options: dict):
    try:
        # selectedOptions 배열에서 각 옵션의 정보 추출
        options_dict = {}
        for option in selected_options.get('selectedOptions', []):
            category = option.get('category')
            name = option.get('name')
            if category and name:
                options_dict[category] = name

        # 쿼리 생성
        query = select(Restaurant)

        # 각 조건 추가
        if '분류' in options_dict:
            query = query.where(Restaurant.category == options_dict['분류'])
        if '주차장' in options_dict:
            query = query.where(Restaurant.parking == options_dict['주차장'])
        if '룸' in options_dict:
            query = query.where(Restaurant.room == options_dict['룸'])
        if '도보/차량' in options_dict:
            query = query.where(Restaurant.transport == options_dict['도보/차량'])
        
        # 쿼리 실행
        result = await db.execute(query)
        restaurants = result.scalars().all()
        
        if not restaurants:
            return None
            
        import random
        return random.choice(restaurants)
        
    except Exception as e:
        print(f"Error in get_db_recommendation: {str(e)}")
        return None



async def init_db(db: AsyncSession):
    try:
        # 데이터가 이미 존재하는지 확인
        result = await db.execute(select(Restaurant).limit(1))
        if result.scalar_one_or_none() is not None:
            print("Database already initialized. Skipping initialization.")
            return

        # 레스토랑 데이터 초기화
        df = pd.read_excel('C:/Users/BioBrain/Desktop/WS/WORK/Project/food_order_system/대전_맛집_리스트.xlsx')
        for _, row in df.iterrows():
            restaurant = Restaurant(
                name=row['상호명'],
                address=row['주소'],
                category=row['분류'],
                parking=row['주차장'],
                main_menu=row['대표 메뉴'],
                revisit_intention=row['재방문 의사'],
                room=row['룸'],
                transport=row['도보/차']
            )
            db.add(restaurant)
        
        # 옵션 데이터 초기화
        options_data = [
            {"name": "한식", "category": "분류"},
            {"name": "중식", "category": "분류"},
            {"name": "분식", "category": "분류"},
            {"name": "일식", "category": "분류"},
            {"name": "양식", "category": "분류"},
            {"name": "멕시코", "category": "분류"},
            {"name": "브라질", "category": "분류"},
            {"name": "베트남", "category": "분류"},
            {"name": "기타", "category": "분류"},
            {"name": "무관", "category": "분류"},
            {"name": "주차 가능", "category": "주차장"},
            {"name": "주차 불가", "category": "주차장"},
            {"name": "무관", "category": "주차장"},
            {"name": "재방문 의사 있음", "category": "재방문의사"},
            {"name": "재방문 의사 없음", "category": "재방문의사"},
            {"name": "무관", "category": "재방문의사"},
            {"name": "룸 있음", "category": "룸"},
            {"name": "룸 없음", "category": "룸"},
            {"name": "무관", "category": "룸"},
            {"name": "도보", "category": "도보/차량"},
            {"name": "차량", "category": "도보/차량"},
            {"name": "무관", "category": "도보/차량"},
        ]
        
        for option_data in options_data:
            option = Option(**option_data)
            db.add(option)
        
        await db.commit()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")
        await db.rollback()
        raise

async def initialize_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as session:
        await init_db(session)
