from typing import Annotated

from fastapi import APIRouter, Path

router = APIRouter(prefix="/items", tags=["Items"])


@router.get("/")
def list_items():
    return [
        "item1",
        "item2",
        "item3",
    ]


# It's important to use right order of endpoints, because if this endpoint was after "/items/{item_id}/", It will be processing by first endpoint and giving error 422, because dict != int
@router.get("/latest/")
def get_latest_item():
    return {"item": {"id": "0", "name": "latest"}}


# Endpoint with type annotation
@router.get("/{item_id}/")
def get_item_by_id(item_id: Annotated[int, Path(ge=1, lt=1000000)]):
    return {"item": {"id": item_id}}
