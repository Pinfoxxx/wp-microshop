from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .order_product_association import order_product_association_table

if TYPE_CHECKING:
    from .product import Product


class Order(Base):
    __tablename__ = "orders"

    promocode: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.now,  # WARNING!!! Don't user datetime.now like a callback (use without '()')
    )
    products: Mapped[list["Product"]] = relationship(
        secondary=order_product_association_table,
        back_populates="orders",
        # lazy="noload"     # This method is dangerous
    )
