from fastapi import APIRouter
from typing import Union

main = APIRouter(
    responses={404: {"description": "Not found"}},
)


@main.get("/")
def read_root():
    return {"Hello": "World"}


@main.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}