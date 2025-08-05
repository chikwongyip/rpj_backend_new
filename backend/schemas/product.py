from sqlalchemy.orm import declarative_base
from schemas.base import BaseMixin
from sqlalchemy import String, Column, Integer
Base = declarative_base()


class Products(Base, BaseMixin):
    __tablename__ = 'products'
    brand_id = Column(Integer)
    name = Column(String(200))
    specification = Column(String(100))
    description = Column(String)
