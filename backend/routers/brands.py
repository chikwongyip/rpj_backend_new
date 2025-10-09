# coding:utf-8
from datetime import datetime
from fastapi import APIRouter, Depends, UploadFile
from db.db import get_db
from schemas.product import Products
from models.brand import BrandCreate, BrandUpdate, BrandResponse
from schemas.brand import Brands
from models.common import BaseResponse
from typing import Optional
from sqlalchemy.orm import Session
from uitls.oss import AliyunOSS
from app_config.oss_config import endpoint, region, bucket_name
from uitls.handle_filename import generate_filename
router = APIRouter(prefix='/admin/brand', tags=['品牌管理'])


@router.get('/info')
# 传入的id 可填可不填，如果填则返回所有品牌
async def get_brands(id: Optional[int] = None, db: Session = Depends(get_db)):
    if id:
        db_item = db.query(Brands).filter_by(id=id).first()
    else:
        db_item = db.query(Brands).all()
    if db_item:
        modelRes = [BrandResponse.model_validate(i) for i in db_item]
        return BaseResponse.success(data=modelRes)
    else:
        return BaseResponse.error(code=1, message="没有查到数据")


@router.post('/add')
async def add_brand(logo: Optional[UploadFile], brand: BrandCreate = Depends(BrandCreate.as_form), db: Session = Depends(get_db)):
    if logo:
        raw = await logo.read()
        # 获取当前路由位置作为文件路径
        full_name = generate_filename(
            prefix=router.prefix, filename=logo.filename, name=None)
        # print(full_name)
        oss_client = AliyunOSS(
            endpoint=endpoint, region=region, bucket_name=bucket_name)
        res = await oss_client.upload_file(
            name=full_name, data=raw)
    brand = Brands(
        name=brand.name,
        description=brand.description,
        logo_url=res.get('url') if res.get('url') else '',
        created_at=datetime.now(),
        updated_at=datetime.now(),
        is_deleted=brand.is_deleted,
        key=res.get('key') if res.get('key') else '',
        file_id=res.get('etag') if res.get('etag') else ''

    )
    db.add(brand)
    db.commit()
    return BaseResponse.success(data={"添加成功!"})


@router.delete('/delete/{id}')
async def delete_brand(id: int, db: Session = Depends(get_db)):
    # check_res = await check_brand_id(id)
    check_res = db.query(Products).filter_by(brand_id=id).first()
    if not check_res:
        db_item = db.query(Brands).filter_by(id=id).first()

        if not db_item:
            return BaseResponse.error(code=1, message="品牌不存在")

        res = db.delete(db_item)
        db.commit()
        return BaseResponse.success(data=res)
    else:
        return BaseResponse.error(code=1, message="已存在产品关联该品牌")

# table 需要加一个image_id key


@router.post('/update')
async def update_brand(logo: Optional[UploadFile], brand: BrandUpdate = Depends(BrandUpdate.as_form), db: Session = Depends(get_db)):
    db_item = db.query(Brands).filter_by(id=brand.id).first()
    if not db_item:
        return BaseResponse.error(code=1, message="品牌不存在")

    if logo:
        allowed_types = ["image/jpeg", "image/png", "image/gif"]
        if logo.content_type not in allowed_types:
            return BaseResponse.error(code=1, message="上传文件内容不允许")
        raw = await logo.read()
        if raw:
            oss_client = AliyunOSS(
                endpoint=endpoint, region=region, bucket_name=bucket_name)
            full_name = generate_filename(
                prefix=router.prefix, filename=logo.filename, name=None)
            res = await oss_client.upload_file(
                name=full_name, data=raw)
            db_item.logo_url = res.get('url') if res.get('url') else ''
            db_item.key = res.get('key') if res.get('key') else ''
            db_item.file_id = res.get('file_id') if res.get('file_id') else ''
        else:
            return BaseResponse.error(code=1, message='图片上传失败')
    db_item.description = brand.description
    db_item.is_deleted = brand.is_deleted
    db_item.name = brand.name
    db_item.updated_at = datetime.now()
    db.commit()
    return BaseResponse.success(data={"result": "更新成功"})
