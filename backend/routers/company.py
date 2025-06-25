from fastapi import APIRouter
from db.db import get_db
from schemas.company import CompanyInfo
from models.common import BaseResponse
from models.company import CompanyInfo as CompanyInfoSchema
router = APIRouter(prefix='/company', tags=['企业管理'])


@router.get('/info')
async def get_company_info(id: int):
    with get_db() as session:
        db_company = session.query(CompanyInfo).filter_by(
            id=id).first()
    if db_company:
        return BaseResponse.success(data=db_company)
    else:
        return BaseResponse.error(code=1, message="数据不存在")


@router.post('/edit')
async def edit_company_info(company: CompanyInfoSchema):
    with get_db as session:
        db_compay = session.query(CompanyInfo).filter_by(
            id=company.id
        ).first()
