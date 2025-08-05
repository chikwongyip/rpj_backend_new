from fastapi import APIRouter, Depends
from db.db import get_db
from models.brand import BrandCreate, BrandUpdate
from schemas.brand import Brands
from models.common import BaseResponse
from typing import Optional
from sqlalchemy.orm import Session
# from pydantic_sqlalchemy import sqlalchemy_to_pydantic
router = APIRouter(prefix='/admin/brand', tags=['品牌管理'])


@router.get('/info')
# 传入的id 可填可不填，如果填则返回所有品牌
async def get_brands(id: Optional[int] = None, db: Session = Depends(get_db)):
    if id:
        db_item = db.query(Brands).filter_by(id=id).first()
    else:
        db_item = db.query(Brands).all()
    if db_item:
        modelRes = [BrandCreate.model_validate(i) for i in db_item]
        return BaseResponse.success(data=modelRes)
    else:
        return BaseResponse.error(code=1, message="没有查到数据")
    # with get_db() as session:
    #     if id:
    #         res = session.query(Brands).filter_by(
    #             id=id).first()
    #     else:
    #         res = session.query(Brands).all()
    # if res:
    #     # print(res)
    #     modelRes = [BrandCreate.model_validate(i) for i in res]
    #     return BaseResponse.success(data=modelRes)
    # else:
    #     return BaseResponse.error(code=1, message="没有查到数据")


@router.post('/add')
async def add_brand(brand: BrandCreate, db: Session = Depends(get_db)):
    brand = Brands(
        name=brand.name,
        description=brand.description,
        logo_url=str(brand.logo_url),
        created_at=brand.created_at,
        updated_at=brand.updated_at,
        is_deleted=brand.is_deleted
    )
    db.add(brand)
    db.commit()

    # with get_db() as session:

    #     brand = Brands(
    #         name=brand.name,
    #         description=brand.description,
    #         logo_url=str(brand.logo_url),
    #         created_at=brand.created_at,
    #         updated_at=brand.updated_at,
    #         is_deleted=brand.is_deleted
    #     )
    #     # print(brand)
    #     session.add(brand)
    #     session.commit()
    return BaseResponse.success(data={"添加成功!"})


@router.delete('/delete/{id}')
async def delete_brand(id: int, db: Session = Depends(get_db)):
    db_item = db.query(Brands).filter_by(id=id).first()
    # print(db_item)
    if not db_item:
        return BaseResponse.error(code=1, message="品牌不存在")

    res = db.delete(db_item)
    db.commit()
    return BaseResponse.success(data=res)


@router.post('/update')
async def update_brand(brand: BrandUpdate, db: Session = Depends(get_db)):
    db_item = db.query(Brands).filter_by(id=brand.id).first()
    if not db_item:
        return BaseResponse.error(code=1, message="品牌不存在")
    db_item.description = brand.description
    db_item.is_deleted = brand.is_deleted
    db_item.name = brand.name
    db_item.logo_url = str(brand.logo_url)
    db.commit()
    return BaseResponse.success(data={"result": "更新成功"})
