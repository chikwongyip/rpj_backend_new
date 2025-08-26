import datetime
from fastapi import APIRouter, Depends
from db.db import get_db
from models.common import BaseResponse
from sqlalchemy.orm import Session
from models.product_attachments import ProductAttachmentsModel, ProductAttachmentsID, ProductAttachmentsBase
from schemas.product_attachments import ProductAttachments
from dependenice.product_id import check_attachment_product_ids
router = APIRouter(prefix='/admin/product_attachments', tags=['产品附件管理'])


@router.post('/add')
async def add_attachements(items: ProductAttachmentsModel = Depends(check_attachment_product_ids), db: Session = Depends(get_db)):
    if items.code:
        return items
    attachments = [ProductAttachments(product_id=i.product_id, url=str(i.url),
                                      original_name=i.original_name, file_type=i.file_type, size=i.size) for i in items.data]

    db.add_all(attachments)
    db.commit()
    return BaseResponse.success(data={"result": "新增成功"})


@router.post('/delete')
async def delete_attachements(items: ProductAttachmentsID, db: Session = Depends(get_db)):
    res = db.query(ProductAttachments).filter(ProductAttachments.id.in_(
        items.ids)).delete(synchronize_session=False)
    db.commit()
    return BaseResponse.success(data=res)


@router.post('/update')
async def update_attachment(items: ProductAttachmentsModel = Depends(check_attachment_product_ids), db: Session = Depends(get_db)):
    if items.code:
        return items
    ids = (
        [items.data.id] if isinstance(items.data, ProductAttachmentsBase)
        else [image.id for image in items.data]
    )
    db_item = db.query(ProductAttachments).filter(
        ProductAttachments.id.in_(set(ids))).all()
    found_ids = {i.id for i in db_item}
    missing_ids = set(ids) - found_ids
    if missing_ids:
        return BaseResponse.error(code=1, message="图片id不存在")
    for item in items:
        item.updated_at = datetime.datetime.now()
        db_item.update(item.model_dump())
    db.commit()
    return BaseResponse.success(data={"result": "更新成功"})


@router.get('/info')
async def get_attachments(product_id: int = None, db: Session = Depends(get_db)):
    if product_id:
        db_item = db.query(ProductAttachments).filter_by(
            product_id=product_id).all()
    else:
        db_item = db.query(ProductAttachments).all()
    if db_item:
        modelRes = [ProductAttachmentsBase.model_validate(i) for i in db_item]
        return BaseResponse.success(data=modelRes)
    else:
        return BaseResponse.error(code=1, message="找不到数据")
