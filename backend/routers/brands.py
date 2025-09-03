import os
from datetime import datetime
from fastapi import APIRouter, Depends, UploadFile
from db.db import get_db
from models.brand import BrandCreate, BrandUpdate
from schemas.brand import Brands
from models.common import BaseResponse
from typing import Optional
from sqlalchemy.orm import Session
from uitls.oss import upload_oss_file
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


@router.post('/add')
async def add_brand(logo: Optional[UploadFile], brand: BrandCreate = Depends(BrandCreate.as_form), db: Session = Depends(get_db)):
    if logo:
        raw = logo.read()
        prefix = router.prefix.lstrip('/')
        file_ext = os.path.splitext(logo.filename)[1]
        res = await upload_oss_file(filepath=prefix, ext=file_ext, data=raw)
    brand = Brands(
        name=brand.name,
        description=brand.description,
        logo_url=res.get('url') if res.get('url') else '',
        created_at=datetime.now(),
        updated_at=datetime.now(),
        is_deleted=brand.is_deleted,
        key=res.get('key') if res.get('key') else '',
        file_id=res.get('file_id') if res.get('file_id') else ''

    )
    db.add(brand)
    db.commit()
    return BaseResponse.success(data={"添加成功!"})


@router.delete('/delete/{id}')
async def delete_brand(id: int, db: Session = Depends(get_db)):
    db_item = db.query(Brands).filter_by(id=id).first()

    if not db_item:
        return BaseResponse.error(code=1, message="品牌不存在")

    res = db.delete(db_item)
    db.commit()
    return BaseResponse.success(data=res)

# table 需要加一个image_id key


@router.post('/update')
async def update_brand(logo: Optional[UploadFile], brand: BrandUpdate, db: Session = Depends(get_db)):
    db_item = db.query(Brands).filter_by(id=brand.id).first()
    if not db_item:
        return BaseResponse.error(code=1, message="品牌不存在")

    if logo:
        raw = logo.read()
        prefix = router.prefix.lstrip('/')
        file_ext = os.path.splitext(logo.filename)[1]
        file_id = db_item.file_id if db_item.file_id != '' else None
        res = await upload_oss_file(filepath=prefix, ext=file_ext,
                                    data=raw, file_id=file_id)
        db_item.logo_url = res.get('url') if res.get('url') else ''
        db_item.key = res.get('key') if res.get('key') else ''
        db_item.file_id = res.get('file_id') if res.get('file_id') else ''

    db_item.description = brand.description
    db_item.is_deleted = brand.is_deleted
    db_item.name = brand.name
    db_item.updated_at = datetime.now()
    db.commit()
    return BaseResponse.success(data={"result": "更新成功"})
