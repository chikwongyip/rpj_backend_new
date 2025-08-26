from pydantic import BaseModel, HttpUrl, Field, ConfigDict
from typing import Optional
from datetime import datetime
from fastapi import File


class CompanyInfo(BaseModel):
    id: int = Field(...)
    name: str = Field(..., min_length=2, max_length=20)
    description: Optional[str] = Field(
        None, title="Company Description", max_length=255)
    logo_url: Optional[bytes] = File()
    icp_number: Optional[str] = Field(None, max_length=100)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
    model_config = ConfigDict(from_attributes=True)

    # @field_validator("created_at", mode="before")
    # def parse_datetime(cls, value):
    #     if isinstance(value, str):
    #         return datetime.fromisoformat(value)
    #     return value
