import datetime
from fastapi import APIRouter, Depends
from db.db import get_db
from models.common import BaseResponse
from sqlalchemy.orm import Session
from models.product import ProductBaseResponse, ProductAdd, ProductBase, ProductUpate, ProductUpdateList
from schemas.product import Products
from dependenice.brand_id import check_brand_ids
router = APIRouter(prefix='/admin/product', tags=['产品管理'])


@router.get('/list')
async def get_product_list(id: int = None, db: Session = Depends(get_db)):
    if id:
        db_item = db.query(Products).filter_by(id=id).first()
    else:
        db_item = db.query(Products).all()
    if db_item:
        res = [ProductBaseResponse.model_validate(i) for i in db_item]
        return BaseResponse.success(data=res)
    return BaseResponse.error(code=1, message="没有找到产品")


@router.post('/add')
async def add_product(product: ProductAdd = Depends(check_brand_ids), db: Session = Depends(get_db)):
    if product.code:
        return product
    if isinstance(product.data, ProductBase):
        products = [Products(
            brand_id=product.data.brand_id,
            name=product.data.name,
            specification=product.data.specification,
            description=product.data.description
        )]
    else:

        products = [Products(brand_id=i.brand_id, name=i.name,
                             specification=i.specification, description=i.description) for i in product.data]
    if not products:
        return BaseResponse.error(code=1, message="新增产品失败")
    db.add_all(products)
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
async def update_product(product: ProductUpdateList = Depends(check_brand_ids), db: Session = Depends(get_db)):
    if product.code:
        return product
    ids = (
        [product.data.id] if isinstance(product.data, ProductUpate)
        else [i.id for i in product.data]
    )
    db_item = db.query(Products).filter(
        Products.id.in_(set(ids))).all()
    if db_item:
        found_ids = {i.id for i in db_item}
        missing_ids = set(ids) - found_ids
    if missing_ids:
        return BaseResponse.error(code=1, message=f"Image id {missing_ids} Not found")
    for item in product:
        item.updated_at = datetime.datetime.now()
        db_item.update(item.model_dump())
    db.commit()
