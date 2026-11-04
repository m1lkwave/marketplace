from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.user_model import UserGet, UserCreate
from src.db.connection import get_async_session
from src.repositories.users_repository import UserRepository, SqlAlchemyUsersRepository

user_router = APIRouter(
    prefix="/api/v1/user",
    tags=["User"]
)

async def get_user_repository(session: AsyncSession = Depends(get_async_session)) -> UserRepository:
    return SqlAlchemyUsersRepository(session)

@user_router.get("/", response_model=list[UserGet])
async def get_all_users(repo: UserRepository = Depends(get_user_repository)):
    return await repo.get_users()

@user_router.get("/{username}", response_model=UserGet)
async def get_user(
    username: str,
    repo: UserRepository = Depends(get_user_repository),
):
    user = await repo.get_user(username)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user

@user_router.post("/", response_model=UserGet, status_code=201)
async def create_user(user: UserCreate, repo: UserRepository=Depends(get_user_repository)):
    return await repo.create_user(user)