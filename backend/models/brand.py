from fastapi import Form
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class BrandBase(BaseModel):
    name: str
    description: Optional[str]
    logo_url: Optional[str]
    is_deleted: Optional[int] = 0


class BrandCreate(BrandBase):

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def as_form(cls,
                name: str = Form(..., min_length=1,
                                 max_length=100, description="品牌名称"),
                description: str = Form(None, max_length=2000),

                logo_url: Optional[str] = Form(None),
                is_deleted: Optional[int] = Form(None)

                ):
        return cls(
            name=name,
            description=description,
            logo_url=logo_url,
            is_deleted=is_deleted
        )

# update 需要传入delete


class BrandUpdate(BrandBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def as_form(cls,
                id: int = Form(...),
                name: str = Form(..., min_length=1,
                                 max_length=100, description="品牌名称"),
                description: str = Form(None, max_length=2000),
                logo_url: Optional[str] = Form(None),
                is_deleted: Optional[int] = Form(None)
                ):
        return cls(
            id=id,
            name=name,
            description=description,
            logo_url=logo_url,
            is_deleted=is_deleted
        )


class BrandResponse(BrandBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)
