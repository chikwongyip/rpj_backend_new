from sqlalchemy.orm import declarative_base
from schemas.base import BaseMixin
from sqlalchemy import String, Column, Integer

Base = declarative_base()


class ProductAttachments(Base, BaseMixin):
    __tablename__ = 'product_images'
    product_id = Column(Integer)
    url = Column(String(255))
    original_name = Column(String(255))
    file_type = Column(String(20))
    size = Column(Integer)
