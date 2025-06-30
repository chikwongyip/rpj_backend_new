from fastapi import APIRouter
from db.db import get_db
from schemas.company import CompanyInfo as CompanyInfoSchema
from models.common import BaseResponse
from models.company import CompanyInfo as CompanyInfoModel
router = APIRouter(prefix='/company', tags=['企业管理'])


@router.get('/info')
async def get_company_info(id: int):
    with get_db() as session:
        db_company = session.query(CompanyInfoSchema).filter_by(
            id=id).first()
    if db_company:
        res = CompanyInfoModel.model_validate(db_company)
        # print(db_company.id)
        return BaseResponse.success(data=res)
    else:
        return BaseResponse.error(code=1, message="数据不存在")


@router.post('/edit')
async def edit_company_info(company: CompanyInfoModel):
    print(company.id)
    with get_db() as session:
        db_company = session.query(CompanyInfoSchema).filter_by(
            id=company.id
        ).one()
    if db_company:
        db_company.name = company.name
        db_company.description = company.description
        db_company.logo_url = company.logo_url
        db_company.icp_number = company.icp_number

        session.commit()
        return BaseResponse.success(data={"result": "更新成功"})
    else:
        return BaseResponse.error(code=1, message="comany id 不存在")
