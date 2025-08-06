from fastapi import APIRouter, Depends
from db.db import get_db
from models.common import BaseResponse
from sqlalchemy.orm import Session
from models.product import ProductModel
from schemas.product import Products
import datetime
router = APIRouter(prefix='/admin/product', tags=['产品管理'])


@router.get('/list')
async def get_product_list(id: int = None, db: Session = Depends(get_db)):
    if id:
        db_item = db.query(Products).filter_by(id=id).first()
    else:
        db_item = db.query(Products).all()
    if db_item:
        res = [ProductModel.model_validate(i) for i in db_item]
        return BaseResponse.success(data=res)
    return BaseResponse.error(code=1, message="没有找到产品")


@router.post('/add')
async def add_product(product: ProductModel, db: Session = Depends(get_db)):
    product = Products(
        brand_id=product.brand_id,
        name=product.name,
        specification=product.specification,
        description=product.description
    )
    db.add(product)
    db.commit()
    return BaseResponse.success(data={"result": "新增成功"})


@router.delete('/delete/{id}')
async def del_product(id: int, db: Session = Depends(get_db)):
    db_item = db.query(Products).filter_by(id=id).first()
    if not db_item:
        return BaseResponse.error(code=1, message="找不到该产品")
    db.delete(db_item)
    db.commit()
    return BaseResponse.success(data={'result': '删除成功'})


@router.post('/update')
async def update_product(product: ProductModel, db: Session = Depends(get_db)):
    db_item = db.query(Products).filter_by(id=product.id).first()
    if not db_item:
        return BaseResponse.error(code=1, message="找不到该产品")
    db_item.name = product.name
    db_item.brand_id = product.brand_id
    db_item.specification = product.specification
    db_item.description = product.description
    db_item.updated_at = datetime.datetime.now()
    db.commit()
    return BaseResponse.success(data={"result": "更新成功"})
