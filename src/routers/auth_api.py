from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.users import SqlAlchemyUsersRepository, UserRepository
from src.schemas.user_auth import UserLogin
from src.db.connection import get_async_session
from src.services.auth import AuthService

auth_router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

async def get_user_repository(session: AsyncSession = Depends(get_async_session)) -> UserRepository:
    return SqlAlchemyUsersRepository(session)

async def get_auth_service(repo: SqlAlchemyUsersRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(repo)

@auth_router.post("/login")
async def login(user: UserLogin, service: AuthService = Depends(get_auth_service)):
    token = await service.login(user.username, user.password)
    return {
    "access_token": token,
    "token_type": "bearer",
    }