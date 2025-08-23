from pydantic import BaseModel, Field, ConfigDict, HttpUrl
from typing import Optional, List
from datetime import datetime


class ProductAttachmentsBase(BaseModel):
    id: Optional[int] = None
    product_id: int
    url: str
    original_name: Optional[str] = None
    file_type: Optional[str] = None
    size: Optional[int] = 0


class ProductAttachmentsModel(ProductAttachmentsBase):
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
    model_config = ConfigDict(from_attributes=True)


class ProductAttachmentsID(BaseModel):
    ids: List[int]
