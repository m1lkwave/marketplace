from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.stone_model import StoneGet, StoneCreate
from src.db.connection import get_async_session
from src.repositories.stones_repository import StoneRepository, SqlAlchemyStoneRepository

stone_router = APIRouter(
    prefix="/api/v1/stone",
    tags=["Stone"]
)

async def get_stone_repository(session: AsyncSession = Depends(get_async_session)) -> StoneRepository:
    return SqlAlchemyStoneRepository(session)

@stone_router.get("/all", response_model=list[StoneGet])
async def get_stones(repo: StoneRepository=Depends(get_stone_repository)):
    return await repo.get_stones()

@stone_router.get("/{stonename}", response_model=StoneGet)
async def get_stone(stonename: str, id: int | None = None, repo: StoneRepository=Depends(get_stone_repository)):
    if id is not None:
        stone = await repo.get_stone_from_name_id(stonename, id)

        if stone is None:
            raise HTTPException(
                status_code=404,
                detail="Stone not found"
            )
        return stone

    else:
        stone = await repo.get_stone_from_name(stonename)
        
        if stone is None:
            raise HTTPException(
                status_code=404,
                detail="Stone not found"
            )

        return stone
    

@stone_router.post("/new", response_model=StoneCreate, status_code=201)
async def create_stone(stone: StoneCreate, repo: StoneRepository=Depends(get_stone_repository)):
    return await repo.create_stone(stone)