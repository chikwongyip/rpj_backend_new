# coding:utf-8
from fastapi import Depends, Form, HTTPException
from db.db import get_db
from sqlalchemy.orm import Session
from schemas.product import Products
from models.common import BaseResponse
# from models.product_image import ProductImageModel, ProductImageBase
# from models.product_attachments import ProductAttachmentsBase


async def check_product_id(product_id: int = Form(...), db: Session = Depends(get_db)):
    products = db.query(Products).filter_by(id=product_id).first()
    if not products:
        # return BaseResponse.error(code=1, message=f"Product ID {product_id} does not exist")
        raise HTTPException(
            status_code=400, detail=f"Product ID {product_id} does not exist")
    return product_id


async def check_brand_id(brand_id: int, db: Session = Depends(get_db)):
    products = db.query(Products).filter_by(brand_id=brand_id).first()
    if products:
        raise HTTPException(
            status_code=400, detail=f"已有产品维护了该品牌"
        )
    return brand_id

# async def check_attachment_product_ids(attachment_input: ProductAttachmentsBase, db: Session = Depends(get_db)):
    # product_ids = (ProductAttachmentsBase
    #                [attachment_input.data.product_id if isinstance(attachment_input.data, ProductAttachmentsBase)
    #                 else [i.product_id for i in attachment_input.data]]
    #                )
    # products = db.query(Products).filter(
    #     Products.id.in_(set(product_ids))).all()
    # found_ids = {product.id for product in products}
    # missing_ids = set(product_ids) - found_ids
    # if missing_ids:
    #     return BaseResponse.error(code=1, message=f"Product id{missing_ids} Not Found")

    # return attachment_input
