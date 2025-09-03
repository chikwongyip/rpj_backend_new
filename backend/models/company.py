from pydantic import BaseModel, ConfigDict
from typing import Optional
from fastapi import Form
from datetime import datetime


class CompanyBase(BaseModel):
    id: int
    name: str
    description: Optional[str]
    logo_url: Optional[str]
    icp_number: Optional[str]


class CompanyUpdate(CompanyBase):

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def as_form(cls,
                id: int = Form(...),
                name: str = Form(..., min_length=1,
                                 max_length=100, description="公司名称"),
                description: str = Form(None, max_length=2000),
                icp_number: Optional[str] = Form(None),
                logo_url: Optional[str] = Form(None)
                ):
        return cls(
            id=id,
            name=name,
            description=description,
            icp_number=icp_number,
            logo_url=logo_url
        )


class CompanyResponse(CompanyBase):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)
