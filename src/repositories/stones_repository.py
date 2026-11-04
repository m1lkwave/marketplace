from abc import ABC, abstractmethod
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.stone_model import StoneGet, StoneCreate
from src.db.models.stone_table import Stone

class StoneRepository(ABC):

    @abstractmethod
    def get_stone_from_name(self, stonename: StoneGet):
        pass

    @abstractmethod
    def get_stone_from_name_id(self, stonename: StoneGet, id: StoneGet | None = None):
        pass

    @abstractmethod
    def get_stones(self):
        pass 

    @abstractmethod
    def create_stone(self, stonename: StoneCreate, price: StoneCreate):
        pass

class SqlAlchemyStoneRepository(StoneRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_stones(self):
        result = await self.session.execute(select(Stone))
        return result.scalars().all()

    async def get_stone_from_name(self, stonename: StoneGet):
        result = await self.session.execute(select(Stone).where(Stone.stone_name == stonename))
        return result.scalar_one_or_none()

    async def get_stone_from_name_id(self, stonename: StoneGet, id: StoneGet|None = None):
        result = await self.session.execute(select(Stone).where(Stone.stone_name == stonename, Stone.id == id))
        return result.scalar_one_or_none()

    async def create_stone(self, stonename: StoneCreate):
        new_stone = Stone(**stonename.model_dump())
        self.session.add(new_stone)
        await self.session.commit()
        await self.session.refresh(new_stone)
        return new_stone