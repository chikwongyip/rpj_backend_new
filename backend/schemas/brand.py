from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
Base = declarative_base()


class Brands(Base):
    __tablename__ = 'brands'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    description = Column(String)
    logo_url = Column(String(255))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_deleted = Column(Integer)
