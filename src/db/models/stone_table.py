from decimal import Decimal
from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column
from src.db.base import Base

class Stone(Base):
    __tablename__ = "stones"

    id: Mapped[int] = mapped_column(primary_key=True)
    stone_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2), nullable=False)

