from src.db.models.user_table import Users
from src.repositories.users import UserRepository
from src.schemas.user_model import UserCreate
from src.services.exceptions import UserNotFoundError
from src.authorization.security import hash_password


class UserService:

    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def get_users(self) -> list[Users]:
        return await self.repo.get_users()

    async def get_user_by_id(self, user_id:int) -> Users:
        result = await self.repo.get_user_by_id(user_id)
        if result is None:
            raise UserNotFoundError()
        return result

    async def get_user(self, username: str) -> Users:
        result = await self.repo.get_user(username)
        if result is None:
            raise UserNotFoundError()
        return result

    async def create_user(self, user: UserCreate) -> Users:
        username = user.username
        password_hash = hash_password(user.password)
        return await self.repo.create_user(username, password_hash)