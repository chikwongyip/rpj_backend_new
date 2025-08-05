from pydantic import BaseModel, HttpUrl, Field, ConfigDict
from typing import Optional
from datetime import datetime


class BrandBase(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=2, max_length=20)
    description: Optional[str] = None
    logo_url: Optional[HttpUrl] = None
    is_deleted: Optional[int] = 0


class BrandCreate(BrandBase):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


class BrandUpdate(BaseModel):
    id: int
    name: str = Field(..., min_length=2, max_length=20)
    description: Optional[str] = None
    logo_url: Optional[HttpUrl] = None
    is_deleted: Optional[int] = 0
    updated_at: Optional[datetime] = datetime.utcnow()
    model_config = ConfigDict(from_attributes=True)
