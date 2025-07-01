from fastapi import APIRouter
from db.db import get_db
from models.brand import BrandInfo as BrandModel
from schemas.brand import Brands as BrandSchemas
from models.common import BaseResponse
from typing import Optional

router = APIRouter(prefix='/admin/brand', tags=['品牌管理'])


@router.get('/info')
# 传入的id 可填可不填，如果填则返回所有品牌
async def get_brands(id: Optional[int] = None):

    with get_db() as session:
        if id:
            res = session.query(BrandSchemas).filter_by(
                id=id).first()
        else:
            res = session.query(BrandSchemas).all()
    if res:
        res = BrandSchemas.model_validate(res)
        # print(db_company.id)
        return BaseResponse.success(data=res)
    else:
        return BaseResponse.error(code=1, message="数据不存在")
