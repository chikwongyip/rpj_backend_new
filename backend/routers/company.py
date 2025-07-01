from fastapi import APIRouter
from db.db import get_db
from schemas.company import CompanyInfo as CompanyInfoSchema
from models.common import BaseResponse
from models.company import CompanyInfo as CompanyInfoModel
router = APIRouter(prefix='/admin/company', tags=['企业管理'])


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
    # print(company.id)
    with get_db() as session:
        result = session.query(CompanyInfoSchema).filter_by(
            id=company.id
        ).one_or_none()

        if not result:
            return BaseResponse.error(code=1, message="comany id 不存在")

        result.name = company.name
        result.description = company.description
        result.logo_url = str(company.logo_url)
        result.icp_number = company.icp_number

        session.commit()
        return BaseResponse.success(data={"result": "更新成功"})
