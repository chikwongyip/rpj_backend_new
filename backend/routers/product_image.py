from fastapi import APIRouter, Depends
from db.db import get_db
from models.common import BaseResponse
from sqlalchemy.orm import Session
from models.product_image import ProductImageModel
from schemas.product_image import ProductImages
import datetime
router = APIRouter(prefix='/admin/product_image', tags=['产品图片管理'])


@router.post('/add')
async def add_images(items: list[ProductImageModel], db: Session = Depends(get_db)):
    images = [ProductImages(product_id=i.product_id, url=i.url,
                            sort_order=i.sort_order, is_thumbnail=i.is_thumbnail) for i in items]

    db.add_all(images)
    db.commit()
    return BaseResponse.success(data={"result": "新增成功"})


@router.post('/delete')
async def delete_images(items: list[id:int], db: Session = Depends(get_db)):
    res = db.query(ProductImages).filter(ProductImages.id.in_(
        items)).delete(synchronize_session=False)
    db.commit()
    return BaseResponse.success(data=res)


@router.post('/update')
async def update_image(item: ProductImageModel, db: Session = Depends(get_db)):
    db_item = db.query(ProductImages).filter_by(id=item.id).first()
    if not db_item:
        return BaseResponse.error(code=1, message="图片id不存在")
    db.delete()
    db.commit()
    return BaseResponse.success(data={"result": "更新成功"})
