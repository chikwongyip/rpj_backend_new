from pydantic import BaseModel, ConfigDict
from fastapi import Depends, Form
from typing import Optional, List, Union
from dependenice.product_id import check_attachment_product_ids
from datetime import datetime


class ProductAttachmentsBase(BaseModel):
    id: Optional[int] = None
    product_id: int = Depends(check_attachment_product_ids)
    url: str
    original_name: Optional[str] = None
    file_type: Optional[str] = None
    size: Optional[int] = 0
    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def as_form(cls,
                id: int = Form(...),
                product_id: int = Form(default=Depends(
                    check_attachment_product_ids)),
                url: str = Form(None),
                file_type: str = Form(None),
                size: int = Form(None),
                original_name: str = Form(None)
                ):
        return cls(
            id=id,
            product_id=product_id,
            url=url,
            original_name=original_name,
            file_type=file_type,
            size=size
        )


class ProductAttachmentBaseResponse(ProductAttachmentsBase):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)


class ProductAttachmentsModel(BaseModel):
    data: Union[ProductAttachmentsBase, List[ProductAttachmentsBase]]


class ProductAttachmentsID(BaseModel):
    ids: List[int]


class ProductAttachmentResponse(BaseModel):
    data: Union[ProductAttachmentBaseResponse,
                List[ProductAttachmentBaseResponse]]


class ProductAttachmentUpdate(BaseModel):
    id: Optional[int] = None
    product_id: int = Depends(check_attachment_product_ids)
    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def as_form(cls, id: int = Form(...), product_id: int = Form(...)):
        return cls(id=id, product_id=product_id)
