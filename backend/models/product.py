from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Union, List
from datetime import datetime

# 产品基础类


class ProductBase(BaseModel):
    brand_id: int
    name: str = Field(..., min_length=5, max_length=200)
    specification: Optional[str] = None
    description: Optional[str] = None
    is_deleted: Optional[int] = 0

# 产品返回基础类


class ProductBaseResponse(ProductBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

# 产品list 返回类


class ProductBaseListResponse(BaseModel):
    data: Union[ProductBaseResponse, List[ProductBaseResponse]]


class ProductAdd(BaseModel):
    data: Union[ProductBase, List[ProductBase]]
    # model_config = ConfigDict(from_attributes=True)


class ProductUpate(ProductBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ProductUpdateList(BaseModel):
    data: Union[ProductUpate, List[ProductUpate]]
