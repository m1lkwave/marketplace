import datetime
from typing import Annotated, TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from src.db.models.stone_table import Stone

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

class StoneImage(Base):
    __tablename__ = "stone_images"

    id: Mapped[int] = mapped_column(primary_key=True)
    stone_id: Mapped[int] = mapped_column(ForeignKey("stones.id"), nullable=False)
    stone: Mapped["Stone"] = relationship(back_populates="images")
    object_key: Mapped[str] = mapped_column(
    unique=True,
    nullable=False,
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
