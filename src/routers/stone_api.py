from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.connection import get_async_session
from src.repositories.stones import SqlAlchemyStoneRepository, StoneRepository
from src.schemas.stone_model import StoneCreate, StoneGet
from src.services.stones import StoneService

stone_router = APIRouter(
    prefix="/api/v1/stone",
    tags=["Stone"]
)

async def get_stone_repository(session: AsyncSession = Depends(get_async_session)) -> StoneRepository:
    return SqlAlchemyStoneRepository(session)

async def get_stone_service(repo: StoneRepository = Depends(get_stone_repository)) -> StoneService:
    return StoneService(repo)

@stone_router.get("/all", response_model=list[StoneGet])
async def get_stones(service: StoneService=Depends(get_stone_service)):
    return await service.get_stones()

@stone_router.get("/{stonename}", response_model=StoneGet)
async def get_stone(stonename: str, service: StoneService=Depends(get_stone_service)):
    return await service.get_stone(stonename)
    

@stone_router.post("/new", response_model=StoneCreate, status_code=201)
async def create_stone(stone: StoneCreate, service: StoneService=Depends(get_stone_service)):
    return await service.create_stone(stone)