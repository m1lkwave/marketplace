from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.stone_table import Stone
from src.schemas.stone_model import StoneCreate, StoneGet


class StoneRepository(ABC):

    @abstractmethod
    async def get_stone_from_name(self, stonename: str) -> Stone | None:
        pass

    @abstractmethod
    async def get_stones(self) -> list[Stone]:
        pass 

    @abstractmethod
    async def create_stone(self, stonename: StoneCreate) -> Stone:
        pass

class SqlAlchemyStoneRepository(StoneRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_stones(self) -> list[Stone]:
        result = await self.session.execute(select(Stone))
        return list(result.scalars().all())

    async def get_stone_from_name(self, stonename: StoneGet) -> Stone:
        result = await self.session.execute(select(Stone).where(Stone.stone_name == stonename))
        return result.scalar_one_or_none()

    async def create_stone(self, stone: StoneCreate) -> Stone:
        new_stone = Stone(**stone.model_dump())
        self.session.add(new_stone)
        await self.session.commit()
        await self.session.refresh(new_stone)
        return new_stone