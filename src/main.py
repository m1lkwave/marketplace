import uvicorn
from fastapi import FastAPI

from src.routers.user_api import user_router
from src.routers.stone_api import stone_router

app = FastAPI()

app.include_router(user_router)
app.include_router(stone_router)

if __name__ == "__main__":
    uvicorn(app="main:app")