from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()
fake_items_db = [{"item_name": "Foo"}, {
    "item_name": "Bar"}, {"item_name": "Baz"}]


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/")
async def read_root():
    return {"hello": "world"}


@app.get("/item/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):

    return {"item_id": item_id, "q": q}


@app.put("/item/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


# 查询参数 默认skip 0 limit 10
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip:skip+limit]
