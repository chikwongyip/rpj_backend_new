from pydantic import BaseModel, HttpUrl, Field, ConfigDict
from typing import Optional, Annotated
from datetime import datetime
from fastapi import File, Form, UploadFile


class CompanyInfo(BaseModel):
    id: Annotated[int, Form(...)]
    name: Annotated[str, Form()]
    description:  Annotated[str, Form()]
    logo_url: Annotated[UploadFile, File()]
    icp_number: Annotated[str, Form()]
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
    model_config = ConfigDict(from_attributes=True)
