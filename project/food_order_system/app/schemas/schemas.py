from pydantic import BaseModel
from datetime import datetime, date
from typing import List, Optional

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class RestaurantBase(BaseModel):
    name: str
    address: str
    category: str
    parking: str
    main_menu: str
    revisit_intention: str
    room: str
    transport: str

class RestaurantCreate(RestaurantBase):
    pass

class Restaurant(RestaurantBase):
    id: int

    class Config:
        orm_mode = True

class OptionBase(BaseModel):
    name: str
    category: str

class OptionCreate(OptionBase):
    pass

class Option(OptionBase):
    id: int

    class Config:
        orm_mode = True

class ReviewBase(BaseModel):
    content: str
    rating: int
    username: str  # 새로 추가된 필드

class ReviewCreate(ReviewBase):
    restaurant_id: int

class Review(ReviewBase):
    id: int
    restaurant_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserSelectionBase(BaseModel):
    restaurant_id: int

class UserSelectionCreate(UserSelectionBase):
    pass

class UserSelection(UserSelectionBase):
    id: int
    user_id: int
    selected_at: datetime

    class Config:
        orm_mode = True

class TokenRefresh(BaseModel):
    refresh_token: str

# 관리자 기능을 위한 스키마

class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    category: Optional[str] = None
    parking: Optional[str] = None
    main_menu: Optional[str] = None
    revisit_intention: Optional[str] = None
    room: Optional[str] = None
    transport: Optional[str] = None

class OptionUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None

class ReviewUpdate(BaseModel):
    content: Optional[str] = None
    rating: Optional[int] = None
    username: Optional[str] = None  # 새로 추가된 필드

class AdminRestaurantResponse(Restaurant):
    reviews: List[Review] = []

class AdminOptionResponse(Option):
    pass

class AdminReviewResponse(Review):
    restaurant: Restaurant

class AdminResponse(BaseModel):
    restaurants: List[AdminRestaurantResponse]
    options: List[AdminOptionResponse]
    reviews: List[AdminReviewResponse]

class ExclusionDaysInput(BaseModel):
    days: int

# 새로 추가된 스키마

class AdminSettingCreate(BaseModel):
    setting_name: str
    setting_value: str
    description: Optional[str] = None

class AdminSetting(AdminSettingCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class SelectedRestaurantLogCreate(BaseModel):
    restaurant_name: str
    selected_options: str
    selected_date: date
    exclude_until: date

class SelectedRestaurantLog(SelectedRestaurantLogCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
