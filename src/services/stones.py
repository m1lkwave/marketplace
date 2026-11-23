import logging
from typing import BinaryIO
from uuid import uuid4


from src.db.models.stone_table import Stone
from src.repositories.stones import StoneRepository
from src.schemas.stone_model import StoneCreate
from src.services.exceptions import StoneNotFoundError
from src.storage.base import Storage
from src.db.transaction import TransactionManager

logger = logging.getLogger(__name__)

class StoneService:

    def __init__(self, repo: StoneRepository, storage: Storage, transaction: TransactionManager):
        self.repository = repo
        self.storage = storage
        self.transaction = transaction

    async def get_stones(self) -> list[Stone]:
        return await self.repository.get_stones()      

    async def get_stone(self, stonename: str) -> Stone:
        result = await self.repository.get_stone_from_name(stonename)
        if result is None:
            raise StoneNotFoundError()
        return result 

    async def create_stone(self, stone: StoneCreate) -> Stone:
        return await self.repository.create_stone(stone)

    async def upload_file(
            self,
            stone_id: int,
            file: BinaryIO,
            content_type: str,
    ) -> str:
        stone = await self.repository.get_stone_from_id(stone_id)
        
        if stone is None:
            raise StoneNotFoundError()
        try:
            key = f"stones/{stone_id}/{uuid4()}"
            
            await self.storage.upload(file=file,content_type=content_type, key=key)

            await self.repository.create_stone_image(
                stone_id=stone_id,
                object_key=key
            )

            await self.transaction.commit()
        except Exception:
            try:
                await self.transaction.rollback()
            except Exception:
                logger.exception(
                    "Failed to rollback transaction for stone_id=%s",
                    stone_id,
                )

            try:
                await self.storage.delete(key)
            except Exception:
                logger.exception(
                    "Failed to delete uploaded object: key=%s",
                    key,
                )

            raise

        return key
    
        
        
        