import datetime
from decimal import Decimal
from typing import Annotated

from sqlalchemy import DateTime, Numeric, func, text
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base

created_at = Annotated[datetime.datetime, mapped_column(
    DateTime, 
    server_default=text("TIMEZONE('utc', now())"), 
    nullable=False,
    )]
updated_at = Annotated[datetime.datetime, mapped_column(
        DateTime,
        server_default=text("TIMEZONE('utc', now())"), 
        onupdate=func.timezone("utc", func.now()),
        nullable=False,
    )]

class Stone(Base):
    __tablename__ = "stones"

    id: Mapped[int] = mapped_column(primary_key=True)
    stone_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2), nullable=False)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at] 

