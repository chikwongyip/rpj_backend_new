import os
from pydantic import BaseModel, ConfigDict, Field
from fastapi import Depends, UploadFile, File, Form
from typing import Optional, List, Union, Annotated
from dependenice.product_id_check import check_product_id
from datetime import datetime


async def get_file_size(file: UploadFile) -> int:
    """获取准确的文件大小"""
    file.file.seek(0, os.SEEK_END)
    size = file.file.tell()
    file.file.seek(0)  # 重置文件指针
    return size


class ProductAttachmentsBase(BaseModel):
    product_id: int = Field(..., gt=0)
    # url: str
    # original_name: str
    # file_type: str
    # size: int
    model_config = ConfigDict(from_attributes=True)
    # @classmethod
    # def as_form(cls,
    #             # id: int = Form(...),
    #             product_id: int = Form(default=Depends(
    #                 check_product_id)),
    #             url: str = Form(None),
    #             file_type: str = Form(None),
    #             size: int = Form(None),
    #             original_name: str = Form(None)
    #             ):
    #     return cls(
    #         # id=id,
    #         product_id=product_id,
    #         url=url,
    #         original_name=original_name,
    #         file_type=file_type,
    #         size=size
    #     )


# class FileInfo(BaseModel):
#     original_name: str
#     file_type: str
#     size: int
#     items: List[FileInfo]


class ProductAttachmentCreate(ProductAttachmentsBase):
    @classmethod
    async def as_form(cls,
                      product_id: Annotated[int, Depends(check_product_id)]
                      ):

        return cls(
            product_id=product_id
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
    id: int
    product_id: int
    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def as_form(cls,
                id: int = Form(...),
                product_id: int = Annotated[int, Depends(check_product_id)]

                ):
        return cls(
            id=id,
            product_id=product_id
        )
