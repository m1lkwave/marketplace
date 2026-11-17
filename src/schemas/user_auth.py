from pydantic import BaseModel, Field

class UserLogin(BaseModel):
    username: str = Field(min_length=2, max_length=100)
    password: str = Field(min_length=8, max_length=20)