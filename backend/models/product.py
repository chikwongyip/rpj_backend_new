from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Union, List
from datetime import datetime


class ProductBase(BaseModel):
    id: Optional[int] = None
    brand_id: int
    name: str = Field(..., min_length=5, max_length=200)
    specification: Optional[str] = None
    description: Optional[str] = None
    is_deleted: Optional[int] = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


class ProductModel(BaseModel):
    data: Union[ProductBase, List[ProductBase]]


# class ProductUpdate(BaseModel):
#     id: int
#     name: str = Field(..., min_length=2, max_length=20)
#     description: Optional[str] = None
#     logo_url: Optional[HttpUrl] = None
#     is_deleted: Optional[int] = 0
#     updated_at: Optional[datetime] = datetime.utcnow()
#     model_config = ConfigDict(from_attributes=True)
