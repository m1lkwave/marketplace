from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

class StoneGet(BaseModel):
    id: int | None = None
    stone_name: str

    model_config = ConfigDict(from_attributes=True)

class StoneCreate(BaseModel):
    stone_name: str
    price: Decimal = Field(gt=0, decimal_places=2)