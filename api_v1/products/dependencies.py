# ====== Dependency for views.py / get product by id ====== #

from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.products import crud
from core.models import db_helper, Product


async def product_by_id(
    product_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Product:
    # Checking avaliable product
    product = await crud.get_product(session=session, product_id=product_id)
    if product is not None:
        return product

    # Giving exception 404 if product not found
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product {product_id} not found!",
    )
