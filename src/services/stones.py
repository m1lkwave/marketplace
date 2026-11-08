from src.db.models.stone_table import Stone
from src.repositories.stones import StoneRepository
from src.schemas.stone_model import StoneCreate
from src.services.exceptions import StoneNotFoundError


class StoneService:

    def __init__(self, repo: StoneRepository):
        self.repository = repo

    async def get_stones(self) -> list[Stone]:
        return await self.repository.get_stones()      

    async def get_stone(self, stonename: str) -> Stone:
        result = await self.repository.get_stone_from_name(stonename)
        if result is None:
            raise StoneNotFoundError()
        return result 

    async def create_stone(self, stone: StoneCreate) -> Stone:
        return await self.repository.create_stone(stone)