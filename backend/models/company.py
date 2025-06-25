from pydantic import BaseModel, HttpUrl, Field
from typing import Optional


class CompanyInfo(BaseModel):
    id: int
    name: str = Field(..., min_length=2, max_length=20)
    description: Optional[str] = None
    logo_url: Optional[HttpUrl] = None
    icp_number: Optional[str] = None
    # 自定义校验：确保名称有效
