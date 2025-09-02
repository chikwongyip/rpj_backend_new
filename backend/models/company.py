from pydantic import BaseModel
from typing import Optional
from fastapi import Form


class CompanyInfo(BaseModel):

    id: int
    name: str
    description: Optional[str]
    icp_number: Optional[str]

    @classmethod
    def as_form(cls,
                id: int = Form(...),
                name: str = Form(..., min_length=1,
                                 max_length=100, description="公司名称"),
                description: str = Form(None, max_length=2000),
                icp_number: Optional[str] = Form(None)
                ):
        return cls(
            id=id,
            name=name,
            description=description,
            icp_number=icp_number
        )
    # id: int = Field(..., description="主键")
    # name: str = Field(..., min_length=1, max_length=100, description="公司名称")
    # description: Optional[str] = Field(None, max_length=2000, description="描述")
    # icp_number: Optional[str] = Field(..., max_length=100, description="icp")

    # id: Annotated[int, Form(...)]
    # name: Annotated[str, Form()]
    # description:  Annotated[str, Form()]
    # logo_url: Annotated[UploadFile, File()]
    # icp_number: Annotated[str, Form()]
    # created_at: Optional[datetime] = Field(default_factory=datetime.now)
    # updated_at: Optional[datetime] = Field(default_factory=datetime.now)
    # model_config = ConfigDict(from_attributes=True)
