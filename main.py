from fastapi import FastAPI, Path
from typing import Optional
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
# 可选参数


async def read_items_opt(item_id: str, q: Optional[str] = None):
    if q:
        return {"item_id": item_id, "q": q}
    else:
        return {"item_id": item_id}


# 导入Pydantic 的BaseModel作为request body

@app.post("/create_items/")
async def create_item(item: Item):
    return item

# 但现实中，快递柜的编号不可能为负数，也不可能超过 1000号柜。这时候就需要用 Path 对参数做验证和约束，比如：

# 编号必须大于 0（gt=0）
# 编号必须小于 1000（lt=1000）
# 给这个参数写个说明，方便别人看懂接口文档（description）


@app.get("/locker/{locker_id}")
def get_locker(
    locker_id: int = Path(  # 用 Path 包裹参数
        ...,                # ... 表示这个参数必须传（不能省略）
        title="快递柜编号",  # 在文档中显示参数名称
        description="请输入你的快递柜编号（1~999）",  # 参数说明
        gt=0,              # 必须大于0（防止用户输入0或负数）
        lt=1000            # 必须小于1000（防止用户输入超大的数字）
    )
):
    return {"你的快递在": locker_id, "内容": "一箱零食"}
