from pydantic import BaseModel, Field, ConfigDict, HttpUrl
from typing import Optional, List
from datetime import datetime


class ProductImageBase(BaseModel):
    id: Optional[int] = None
    product_id: int
    url: HttpUrl
    sort_order: int = 99
    is_thumbnail: int = 0
    is_deleted: Optional[int] = 0


class ProductImageModel(ProductImageBase):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


class ProductImageID(BaseModel):
    ids: List[int]
