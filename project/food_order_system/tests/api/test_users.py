import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.main import app
from app.services.user_service import UserService

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient, db: AsyncSession):
    response = await client.post(
        f"{settings.API_V1_STR}/users/",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

@pytest.mark.asyncio
async def test_authenticate_user(client: AsyncClient, db: AsyncSession):
    # First, create a user
    user_in = {"email": "auth@example.com", "password": "authpassword"}
    user = await UserService.create_user(db, user_in)
    
    # Now, try to authenticate
    response = await client.post(
        f"{settings.API_V1_STR}/login/access-token",
        data={"username": user_in["email"], "password": user_in["password"]}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_read_users_me(client: AsyncClient, db: AsyncSession, normal_user_token_headers):
    response = await client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "normal@example.com"
    assert data["is_active"] is True
    assert data["is_superuser"] is False
