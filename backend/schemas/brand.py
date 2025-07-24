from sqlalchemy.orm import declarative_base
from schemas.base import BaseMixin
from sqlalchemy import String, Column, Integer, DateTime
from datetime import datetime
Base = declarative_base()


class Brands(Base, BaseMixin):
    __tablename__ = "brands"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String)
    url = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
