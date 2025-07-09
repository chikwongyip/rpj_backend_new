from pydantic import BaseModel
from datetime import datetime


class BrandBase(BaseModel):
    name: str
    description: str | None = None
    logo_url: str | None = None


class BrandCreate(BrandBase):
    pass


class BrandUpdate(BrandBase):
    pass


class BrandInDB(BrandBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

    class Config:
        orm_mode = True
