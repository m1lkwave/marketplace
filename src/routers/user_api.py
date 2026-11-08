from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.connection import get_async_session
from src.repositories.users import SqlAlchemyUsersRepository, UserRepository
from src.schemas.user_model import UserCreate, UserGet
from src.services.users import UserService

user_router = APIRouter(
    prefix="/api/v1/user",
    tags=["User"]
)

async def get_user_repository(session: AsyncSession = Depends(get_async_session)) -> UserRepository:
    return SqlAlchemyUsersRepository(session)

async def get_user_service(repo: SqlAlchemyUsersRepository=Depends(get_user_repository)) -> UserService:
    return UserService(repo)

@user_router.get("/", response_model=list[UserGet])
async def get_all_users(service: UserService = Depends(get_user_service)):
    return await service.get_users()

@user_router.get("/{username}", response_model=UserGet)
async def get_user(
    username: str,
    service: UserService = Depends(get_user_service),
):
    return await service.get_user(username)

@user_router.post("/", response_model=UserGet, status_code=201)
async def create_user(user: UserCreate, service: UserService=Depends(get_user_service)):
    return await service.create_user(user)