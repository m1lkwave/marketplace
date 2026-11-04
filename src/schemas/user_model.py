from pydantic import BaseModel, Field, ConfigDict

class UserCreate(BaseModel):
    username: str = Field(min_length=2, max_length=50)
    password: str = Field(min_length=8, max_length=100)


class UserGet(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)
    