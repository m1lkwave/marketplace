from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.user_table import Users


class UserRepository(ABC):

    @abstractmethod
    async def get_users(self) -> list[Users]:
        pass

    @abstractmethod
    async def get_user(self, username: str) -> Users | None:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> Users | None:
        pass

    @abstractmethod
    async def create_user(self, username: str, password_hash: str) -> Users:
        pass


class SqlAlchemyUsersRepository(UserRepository):
    
    def __init__(self, session: AsyncSession):
        self.session = session    

    async def get_users(self) -> list[Users]:
        result = await self.session.execute(select(Users))
        return list(result.scalars().all())

    async def get_user(self, username: str) -> Users | None:
        result = await self.session.execute(select(Users).where(Users.username == username))
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: int) -> Users | None:
        result = await self.session.execute(select(Users).where(Users.id == user_id))
        return result.scalar_one_or_none()

    async def create_user(self, username: str, password_hash: str) -> Users:
        new_user = Users(username=username, password_hash=password_hash)
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user
