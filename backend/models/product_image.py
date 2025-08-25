from pydantic import BaseModel, Field, ConfigDict, HttpUrl
from typing import Optional, List, Union
from datetime import datetime


class ProductImageBase(BaseModel):
    id: Optional[int] = None
    product_id: int
    url: str
    sort_order: int = 99
    is_thumbnail: int = 0
    is_deleted: Optional[int] = 0
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
    model_config = ConfigDict(from_attributes=True)


class ProductImageModel(BaseModel):
    data: Union[ProductImageBase, List[ProductImageBase]]
    # model_config = ConfigDict(from_attributes=True)


class ProductImageID(BaseModel):
    ids: List[int]
