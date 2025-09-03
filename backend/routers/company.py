import os
from datetime import datetime
from fastapi import APIRouter, Depends, UploadFile
from db.db import get_db
from schemas.company import CompanyInfo as CompanyInfoSchema
from models.common import BaseResponse
from models.company import CompanyInfo as CompanyInfoModel
from sqlalchemy.orm import Session
from typing import Optional
from app_config.oss_config import endpoint, region, bucket_name
from uitls.oss import AliyunOSS
router = APIRouter(prefix='/admin/company', tags=['企业管理'])


@router.get('/info')
async def get_company_info(id: int, db: Session = Depends(get_db)):
    db_item = db.query(CompanyInfoSchema).filter_by(id=id).first()
    if db_item:
        res = CompanyInfoModel.model_validate(db_item)
        return BaseResponse.success(data=res)
    else:
        return BaseResponse.error(code=1, message="数据不存在")


@router.post('/edit')
async def edit_company_info(logo: Optional[UploadFile], company: CompanyInfoModel = Depends(CompanyInfoModel.as_form),  db: Session = Depends(get_db)):
    # print(company.id)
    db_item = db.query(CompanyInfoSchema).filter_by(
        id=company.id).one_or_none()
    if not db_item:
        return BaseResponse.error(code=1, message="company id 不存在")
    if logo:

        allowed_types = ["image/jpeg", "image/png", "image/gif"]
        if logo.content_type not in allowed_types:
            return BaseResponse.error(code=1, message="上传文件内容不允许")
        raw = await logo.read()
        prefix = router.prefix.lstrip('/')
        file_ext = os.path.splitext(logo.filename)[1]
        filename = f"{prefix}/logo{file_ext}"
        # res = asyncio.run(upload_oss_file(file_name=filename, data=raw))
        oss_client = AliyunOSS(
            endpoint=endpoint, region=region, bucket_name=bucket_name)
        res = await oss_client.upload_file(
            filename, data=raw)

        db_item.logo_url = str(res.get('url'))
    db_item.name = company.name
    db_item.description = company.description
    db_item.icp_number = str(company.icp_number)
    db_item.updated_at = datetime.now()
    db.commit()
    return BaseResponse.success(data={"result": "更新成功"})
