from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.connection import get_async_session
from src.repositories.stones import SqlAlchemyStoneRepository, StoneRepository
from src.schemas.stone_model import StoneCreate, StoneGet
from src.services.stones import StoneService
from src.dependencies.storage import get_storage
from src.storage.base import Storage
from src.db.transaction import TransactionManager
from src.dependencies.transaction import get_transaction_manager

stone_router = APIRouter(
    prefix="/api/v1/stone",
    tags=["Stone"]
)

async def get_stone_repository(session: AsyncSession = Depends(get_async_session)) -> StoneRepository:
    return SqlAlchemyStoneRepository(session)

async def get_stone_service(
        repo: StoneRepository = Depends(get_stone_repository),
        storage: Storage = Depends(get_storage),
        transaction: TransactionManager = Depends(get_transaction_manager)
    ) -> StoneService:
    return StoneService(repo, storage, transaction)

@stone_router.get("/all", response_model=list[StoneGet])
async def get_stones(service: StoneService=Depends(get_stone_service)):
    return await service.get_stones()

@stone_router.get("/{stonename}", response_model=StoneGet)
async def get_stone(stonename: str, service: StoneService=Depends(get_stone_service)):
    return await service.get_stone(stonename)
    

@stone_router.post("/new", response_model=StoneCreate, status_code=201)
async def create_stone(stone: StoneCreate, service: StoneService=Depends(get_stone_service)):
    return await service.create_stone(stone)

@stone_router.post("/{stone_id}/image")
async def give_image(
        stone_id: int,
        file: UploadFile,
        service: StoneService = Depends(get_stone_service),
):
    key = await service.upload_file(
        file=file.file,
        stone_id=stone_id,
        content_type=file.content_type or "application/octet-stream"
    )
    return {
    "stone_id": stone_id,
    "image_key": key,
    }