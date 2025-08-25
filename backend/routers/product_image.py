from fastapi import APIRouter, Depends
from db.db import get_db
from models.common import BaseResponse
from sqlalchemy.orm import Session
from models.product_image import ProductImageModel, ProductImageID, ProductImageBase
from schemas.product_image import ProductImages
import datetime
router = APIRouter(prefix='/admin/product_image', tags=['产品图片管理'])


@router.post('/add')
async def add_images(items: ProductImageModel, db: Session = Depends(get_db)):
    images = [ProductImages(product_id=i.product_id, url=str(i.url),
                            sort_order=i.sort_order, is_thumbnail=i.is_thumbnail) for i in items.data]

    db.add_all(images)
    db.commit()
    return BaseResponse.success(data={"result": "新增成功"})


@router.post('/delete')
async def delete_images(items: ProductImageID, db: Session = Depends(get_db)):
    res = db.query(ProductImages).filter(ProductImages.id.in_(
        items.ids)).delete(synchronize_session=False)
    db.commit()
    return BaseResponse.success(data=res)


@router.post('/update')
async def update_images(items: ProductImageModel, db: Session = Depends(get_db)):
    # print(items)
    ids = (
        [items.data.id] if isinstance(items.data, ProductImageBase)
        else [image.id for image in items.data]
    )
    db_item = db.query(ProductImages).filter(
        ProductImages.id.in_(set(ids))).all()
    found_ids = {i.id for i in db_item}
    missing_ids = set(ids) - found_ids
    if missing_ids:
        return BaseResponse.error(code=1, message=f"Image id {missing_ids} Not found")
    for item in items:
        item.updated_at = datetime.datetime.now()
        db_item.update(item.model_dump())
    db.commit()
    return BaseResponse.success(data={"result": "更新成功"})


@router.get('/info')
async def get_images(product_id: int = None, db: Session = Depends(get_db)):
    if product_id:
        db_item = db.query(ProductImages).filter_by(
            product_id=product_id).all()
    else:
        db_item = db.query(ProductImages).all()
    if db_item:
        modelRes = [ProductImageBase.model_validate(i) for i in db_item]
        return BaseResponse.success(data=modelRes)
    else:
        return BaseResponse.error(code=1, message="找不到数据")
