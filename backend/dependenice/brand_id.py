# coding:utf-8
from fastapi import Depends
from db.db import get_db
from sqlalchemy.orm import Session
from schemas.brand import Brands
from models.common import BaseResponse
from models.product import ProductModel, ProductBase


async def check_brand_ids(product_input: ProductModel, db: Session = Depends(get_db)):
    brand_ids = (
        [product_input.data.brand_id] if isinstance(product_input.data, ProductBase)
        else [i.brand_id for i in product_input.data]
    )
    brands = db.query(Brands).filter(
        Brands.id.in_(set(brand_ids))).all()
    found_ids = {brand.id for brand in brands}
    missing_ids = set(brand_ids) - found_ids
    if missing_ids:
        return BaseResponse.error(code=1, message=f"Brand id {missing_ids} Not Found")
    return product_input
