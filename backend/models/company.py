from pydantic import BaseModel, HttpUrl, Field, ConfigDict, field_validator
from typing import Optional
from datetime import datetime


class CompanyInfo(BaseModel):
    id: int
    name: str = Field(..., min_length=2, max_length=20)
    description: Optional[str] = None
    logo_url: Optional[HttpUrl] = None
    icp_number: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    # 自定义校验：确保名称有效
    model_config = ConfigDict(from_attributes=True)

    @field_validator("created_at", mode="before")
    def parse_datetime(cls, value):
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value
