from fastapi import APIRouter, Depends
from db.db import get_db
from schemas.company import CompanyInfo as CompanyInfoSchema
from models.common import BaseResponse
from models.company import CompanyInfo as CompanyInfoModel
from sqlalchemy.orm import Session
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
async def edit_company_info(company: CompanyInfoModel, db: Session = Depends(get_db)):

    db_item = db.query(CompanyInfoSchema).filter_by(
        id=company.id).one_or_none()
    if not db_item:
        return BaseResponse.error(code=1, message="company id 不存在")

    db_item.name = company.name
    db_item.description = company.description
    db_item.logo_url = str(company.logo_url)
    db_item.icp_number = str(company.icp_number)
    db_item.commit()
    return BaseResponse.success(data={"result": "更新成功"})
