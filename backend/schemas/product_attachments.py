from sqlalchemy.orm import declarative_base
from schemas.base import BaseMixin
from sqlalchemy import String, Column, Integer, DateTime

Base = declarative_base()


class ProductAttachments(Base, BaseMixin):
    __tablename__ = 'product_attachments'
    product_id = Column(Integer)
    url = Column(String(255))
    original_name = Column(String(255))
    file_type = Column(String(20))
    size = Column(Integer)
    key = Column(String)
    file_id = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
