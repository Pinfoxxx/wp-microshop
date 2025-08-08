from sqlalchemy import Column, ForeignKey, Integer, Table, UniqueConstraint

from .base import Base


order_product_association_table = Table(
    "order_product_association",
    Base.metadata,
    Column("id", Integer, primary_key=True),  # This id is need for simple add columns
    Column(
        "order_id", ForeignKey("orders.id"), nullable=False
    ),  # Primary key can be for a two columns, because we want to add one product
    Column(
        "product_id", ForeignKey("products.id"), nullable=False
    ),  # only one time, but the quantity can be any. One id = one product in order
    UniqueConstraint("order_id", "product_id", name="index_unique_order_product"),
)
