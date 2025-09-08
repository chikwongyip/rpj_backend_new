import os
from datetime import datetime
from fastapi import APIRouter, Depends, UploadFile
from db.db import get_db
from schemas.company import CompanyInfo as CompanyInfoSchema
from models.common import BaseResponse
from models.company import CompanyUpdate, CompanyResponse
from sqlalchemy.orm import Session
from typing import Optional
from app_config.oss_config import endpoint, region, bucket_name
from uitls.oss import AliyunOSS
from uitls.handle_filename import generate_filename
router = APIRouter(prefix='/admin/company', tags=['企业管理'])


@router.get('/info')
async def get_company_info(id: int, db: Session = Depends(get_db)):
    db_item = db.query(CompanyInfoSchema).filter_by(id=id).first()
    if db_item:
        res = CompanyResponse.model_validate(db_item)
        return BaseResponse.success(data=res)
    else:
        return BaseResponse.error(code=1, message="数据不存在")


@router.post('/edit')
async def edit_company_info(logo: Optional[UploadFile], company: CompanyUpdate = Depends(CompanyUpdate.as_form),  db: Session = Depends(get_db)):
    # 先根据id 查询 company 表是否存在
    db_item = db.query(CompanyInfoSchema).filter_by(
        id=company.id).one_or_none()
    if not db_item:
        return BaseResponse.error(code=1, message="company id 不存在")
    # 如果用户有上传图片则运行阿里云上传图片
    if logo:
        # 检查图片类型是否 图片类型
        allowed_types = ["image/jpeg", "image/png", "image/gif"]
        if logo.content_type not in allowed_types:
            return BaseResponse.error(code=1, message="上传文件内容不允许")
        raw = await logo.read()
        # 获取当前路由位置作为文件路径
        # prefix = router.prefix.lstrip('/')
        # file_ext = os.path.splitext(logo.filename)[1]
        oss_client = AliyunOSS(
            endpoint=endpoint, region=region, bucket_name=bucket_name)

        # name = 'logo'
        full_name = generate_filename(prefix=router.prefix,
                                      filename=logo.filename, name='logo')
        # print(full_name)
        res = await oss_client.upload_file(
            name=full_name, data=raw)

        db_item.logo_url = str(res.get('url')) if res.get('url') else ''
        db_item.key = str(
            res.get('key')) if res.get('key') else ''
        db_item.file_id = str(res.get('etag')) if res.get('etag') else ''

    db_item.name = company.name
    db_item.description = company.description
    db_item.icp_number = str(company.icp_number)
    db_item.updated_at = datetime.now()
    db.commit()
    return BaseResponse.success(data={"result": "更新成功"})
