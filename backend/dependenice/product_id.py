# coding:utf-8
from fastapi import Depends
from db.db import get_db
from sqlalchemy.orm import Session
from schemas.product import Products
from models.common import BaseResponse
from models.product_image import ProductImageModel, ProductImageBase
from models.product_attachments import ProductAttachmentsModel, ProductAttachmentsBase


async def check_image_product_ids(image_input: ProductImageModel, db: Session = Depends(get_db)):
    product_ids = (
        [image_input.data.product_id] if isinstance(image_input.data, ProductImageBase)
        else [image.product_id for image in image_input.data]
    )
    products = db.query(Products).filter(
        Products.id.in_(set(product_ids))).all()
    found_ids = {product.id for product in products}
    missing_ids = set(product_ids) - found_ids
    if missing_ids:
        return BaseResponse.error(code=1, message=f"Product id {missing_ids} Not Found")
    return image_input


async def check_attachment_product_ids(attachment_input: ProductAttachmentsModel, db: Session = Depends(get_db)):
    product_ids = (
        [attachment_input.data.product_id if isinstance(attachment_input.data, ProductAttachmentsBase)
         else [i.product_id for i in attachment_input.data]]
    )
    products = db.query(Products).filter(
        Products.id.in_(set(product_ids))).all()
    found_ids = {product.id for product in products}
    missing_ids = set(product_ids) - found_ids
    if missing_ids:
        return BaseResponse.error(code=1, message=f"Product id{missing_ids} Not Found")

    return attachment_input
