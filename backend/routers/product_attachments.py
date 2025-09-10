from datetime import datetime
import mimetypes
from fastapi import APIRouter, Depends, UploadFile, Form
from typing import Annotated, List
from db.db import get_db
from models.common import BaseResponse
from sqlalchemy.orm import Session
from models.product_attachments import ProductAttachmentsID, ProductAttachmentsBase, ProductAttachmentUpdate, ProductAttachmentBaseResponse
from schemas.product_attachments import ProductAttachments
from app_config.oss_config import endpoint, region, bucket_name
from uitls.oss import AliyunOSS
from uitls.handle_filename import generate_filename
from dependenice.product_id_check import check_product_id
router = APIRouter(prefix='/admin/product_attachments', tags=['产品附件管理'])
ALLOWED_MIME_TYPES = {
    "application/vnd.ms-powerpoint",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/pdf"
}

# 允许的扩展名
ALLOWED_EXTENSIONS = {".ppt", ".pptx",
                      ".doc", ".docx", ".xls", ".xlsx", ".pdf"}


def validate_file(file: UploadFile) -> bool:
    # 检查扩展名
    extension = f".{file.filename.split('.')[-1].lower()}"
    if extension not in ALLOWED_EXTENSIONS:
        return False

    # 检查 MIME 类型
    content_type = file.content_type
    if content_type not in ALLOWED_MIME_TYPES:
        # 如果 MIME 类型不可靠，尝试根据扩展名推断
        guessed_type, _ = mimetypes.guess_type(file.filename)
        if guessed_type not in ALLOWED_MIME_TYPES:
            return False

    return True


@router.post('/add')
async def add_attachements(files: List[UploadFile], product_id: Annotated[int, Depends(check_product_id)],  db: Session = Depends(get_db)):
    oss_client = AliyunOSS(
        endpoint=endpoint, region=region, bucket_name=bucket_name)
    if files:

        attachments = []
        for file in files:
            data = await file.read()
            full_name = generate_filename(prefix=router.prefix,
                                          filename=file.filename)
            # print(full_name)
            res = await oss_client.upload_file(
                name=full_name, data=data)
            attachment = ProductAttachments(product_id=product_id,
                                            url=str(res.get('url')) if res.get(
                                                'url') else '',
                                            original_name=file.filename,
                                            file_type=file.content_type,
                                            size=file.size if file.size else 0,
                                            created_at=datetime.now(),
                                            updated_at=datetime.now(),
                                            key=res.get('key') if res.get(
                                                'key') else '',
                                            file_id=res.get('etag') if res.get('etag') else '')
            attachments.append(attachment)

        db.add_all(attachments)
        db.commit()
        return BaseResponse.success(data={"result": "新增成功"})
    else:
        return BaseResponse.error(code=1, message="没有上传附件")


@router.post('/delete')
async def delete_attachements(items: ProductAttachmentsID, db: Session = Depends(get_db)):
    res = db.query(ProductAttachments).filter(ProductAttachments.id.in_(
        items.ids)).delete(synchronize_session=False)
    db.commit()
    return BaseResponse.success(data=res)


@router.post('/update')
async def update_attachment(items: ProductAttachmentUpdate = Depends(ProductAttachmentUpdate.as_form), db: Session = Depends(get_db)):
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
        for i in db_item:
            print(i)
        modelRes = [ProductAttachmentBaseResponse.model_validate(
            i) for i in db_item]
        return BaseResponse.success(data=modelRes)
    else:
        return BaseResponse.error(code=1, message="找不到数据")
