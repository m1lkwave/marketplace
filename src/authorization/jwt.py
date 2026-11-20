from authx import AuthX, AuthXConfig
from src.settings import settings

config = AuthXConfig()
config.JWT_SECRET_KEY = settings.jwt_secret_key
config.JWT_TOKEN_LOCATION = ["headers"]

security = AuthX(config=config)

