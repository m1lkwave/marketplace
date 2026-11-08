from pydantic_settings import BaseSettings, SettingsConfigDict


class DbSettting(BaseSettings):
    db_host: str
    db_port: str
    db_name: str
    db_user: str
    db_password: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    model_config = SettingsConfigDict(
        env_file=".env",
    )

settings = DbSettting()

