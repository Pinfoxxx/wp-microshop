from typing import TYPE_CHECKING

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING: # hack
    from .user import User

class Post(Base):
    __tablename__ = "posts"

    title: Mapped[str] = mapped_column(String(100))
    body: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
    )
    user: Mapped["User"] = relationship(back_populates='posts')