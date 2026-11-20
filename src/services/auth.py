from src.repositories.users import UserRepository
from src.services.exceptions import InvalidCredentialsError
from src.authorization.security import verify_password
from src.authorization.jwt import security


class AuthService:

    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def login(self, username: str, password: str) -> str:
        user = await self.repo.get_user(username)

        if user is None:
            raise InvalidCredentialsError()

        is_valid = verify_password(password, user.password_hash)

        if not is_valid:
            raise InvalidCredentialsError()

        return security.create_access_token(uid=str(user.id))
