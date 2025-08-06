from sqlalchemy.orm import declarative_base
from schemas.base import BaseMixin
from sqlalchemy import String, Column, Integer

Base = declarative_base()


class ProductImages(Base, BaseMixin):
    __tablename__ = 'product_images'
    product_id = Column(Integer)
    url = Column(String(255))
    sort_order = Column(Integer)
    is_thumbnail = Column(Integer)
