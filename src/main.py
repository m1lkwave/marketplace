from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.routers.stone_api import stone_router
from src.routers.user_api import user_router
from src.routers.auth_api import auth_router
from src.services.exceptions import StoneNotFoundError, UserNotFoundError, InvalidCredentialsError
from src.authorization.jwt import security

app = FastAPI()

security.handle_errors(app)

app.include_router(user_router)
app.include_router(stone_router)
app.include_router(auth_router)

@app.exception_handler(StoneNotFoundError)
async def stone_not_found_handler(
    request: Request,
    exc: StoneNotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": "Stone Not Found"}
    )

@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(
    request: Request,
    exc: UserNotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": "UserNotFound"}
    )

@app.exception_handler(InvalidCredentialsError)
async def login_error_handler(
    request: Request,
    exc: UserNotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={"detail": "Incorrect username or password"},
        headers={"WWW-Authenticate": "Bearer"}
    )