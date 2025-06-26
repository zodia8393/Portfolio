from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime, Float, Date, func, select
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    selections = relationship("Selection", back_populates="user")

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    address = Column(String(255))
    category = Column(String(100))
    parking = Column(String(50))
    main_menu = Column(String(255))
    revisit_intention = Column(String(50))
    room = Column(String(50))
    transport = Column(String(50))

    reviews = relationship("Review", back_populates="restaurant")

class Option(Base):
    __tablename__ = "options"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    category = Column(String(100), index=True)

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    rating = Column(Float)
    username = Column(String(255))
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    created_at = Column(DateTime, server_default=func.now())

    restaurant = relationship("Restaurant", back_populates="reviews")

class Selection(Base):
    __tablename__ = "user_selections"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    selected_at = Column(DateTime)

    user = relationship("User", back_populates="selections")
    restaurant = relationship("Restaurant")

class AdminLog(Base):
    __tablename__ = "admin_logs"

    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(255))
    target = Column(String(255))
    timestamp = Column(DateTime)

    admin = relationship("User")

class RestaurantEdit(Base):
    __tablename__ = "restaurant_edits"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    admin_id = Column(Integer, ForeignKey("users.id"))
    field_name = Column(String(100))
    old_value = Column(String(255))
    new_value = Column(String(255))
    edit_timestamp = Column(DateTime)

    restaurant = relationship("Restaurant")
    admin = relationship("User")

class OptionEdit(Base):
    __tablename__ = "option_edits"

    id = Column(Integer, primary_key=True, index=True)
    option_id = Column(Integer, ForeignKey("options.id"))
    admin_id = Column(Integer, ForeignKey("users.id"))
    field_name = Column(String(100))
    old_value = Column(String(255))
    new_value = Column(String(255))
    edit_timestamp = Column(DateTime)

    option = relationship("Option")
    admin = relationship("User")

class RestaurantSelection(Base):
    __tablename__ = "restaurant_selections"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_name = Column(String(255), index=True)
    selected_options = Column(Text)  # JSON 형태로 저장
    selected_at = Column(DateTime)
    exclude_until = Column(DateTime)  # 제외 기간 종료일
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def is_excluded(self):
        return datetime.now() <= self.exclude_until if self.exclude_until else False

class AdminSettings(Base):
    __tablename__ = "admin_settings"

    id = Column(Integer, primary_key=True, index=True)
    setting_name = Column(String(255), unique=True, index=True)
    setting_value = Column(String(255))
    description = Column(String(500))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    @classmethod
    async def get_exclusion_days(cls, db: AsyncSession):
        query = select(cls).where(cls.setting_name == 'exclusion_days')
        result = await db.execute(query)
        setting = result.scalar_one_or_none()
        return int(setting.setting_value) if setting else 7  # 기본값 7일

    @classmethod
    async def set_exclusion_days(cls, db: AsyncSession, days: int):
        query = select(cls).where(cls.setting_name == 'exclusion_days')
        result = await db.execute(query)
        setting = result.scalar_one_or_none()
        
        if setting:
            setting.setting_value = str(days)
        else:
            setting = cls(
                setting_name='exclusion_days',
                setting_value=str(days),
                description='식당 추천 제외 기간 (일)'
            )
            db.add(setting)
        
        await db.commit()
        await db.refresh(setting)
        return setting

class SelectedRestaurantLog(Base):
    __tablename__ = "selected_restaurant_logs"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_name = Column(String(255), index=True)
    selected_options = Column(Text)  # JSON 형태로 저장
    selected_date = Column(Date, index=True)
    exclude_until = Column(Date, index=True)
    created_at = Column(DateTime, server_default=func.now())

    @classmethod
    async def add_selection(cls, db, restaurant_name, options, exclusion_days):
        selected_date = datetime.now().date()
        exclude_until = selected_date + timedelta(days=exclusion_days)
        
        log = cls(
            restaurant_name=restaurant_name,
            selected_options=options,
            selected_date=selected_date,
            exclude_until=exclude_until
        )
        db.add(log)
        await db.commit()
        return log

    @classmethod
    async def get_excluded_restaurants(cls, db):
        current_date = datetime.now().date()
        query = select(cls.restaurant_name).where(cls.exclude_until >= current_date)
        result = await db.execute(query)
        return [row[0] for row in result]
