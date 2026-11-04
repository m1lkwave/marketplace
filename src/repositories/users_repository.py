from abc import ABC, abstractmethod
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.user_model import UserGet, UserCreate
from src.db.models.user_table import Users

class UserRepository(ABC):

    @abstractmethod
    async def get_users(self) -> list[Users]:
        pass

    @abstractmethod
    async def get_user(self, user: UserGet):
        pass

    @abstractmethod
    async def create_user(self, user: UserCreate)->Users:
        pass


class SqlAlchemyUsersRepository(UserRepository):
    
    def __init__(self, session: AsyncSession):
        self.session = session    

    async def get_users(self) -> list[Users]:
        result = await self.session.execute(select(Users))
        return result.scalars().all()

    async def get_user(self, username: UserGet) -> dict:
        result = await self.session.execute(select(Users).where(Users.username == username))
        return result.scalar_one_or_none()

    async def create_user(self, user):
        new_user = Users(**user.model_dump())
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user
