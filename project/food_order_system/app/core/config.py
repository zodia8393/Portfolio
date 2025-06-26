from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "smart_lunch_mate"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    MYSQL_SERVER: str
    MYSQL_PORT: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DB: str

    UNSPLASH_ACCESS_KEY: Optional[str] = None
    PERPLEXITY_API_KEY: str
    VUE_APP_ADMIN_USERNAME: str
    VUE_APP_ADMIN_PASSWORD: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ADMIN_SECRET_KEY : str = '1q2w3e4r1!'

    # 새로운 관리자 기능을 위한 설정
    ADMIN_SECRET_KEY: str  # 관리자 인증을 위한 비밀키

    class Config:
        env_file = "C:/Users/BioBrain/Desktop/WS/WORK/Project/food_order_system/.env"
        extra = "allow"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.DATABASE_URL = f"mysql+aiomysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_SERVER}:{self.MYSQL_PORT}/{self.MYSQL_DB}"

settings = Settings()
