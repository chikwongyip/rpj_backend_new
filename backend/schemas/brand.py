from sqlalchemy.orm import declarative_base
from schemas.base import BaseMixin
from sqlalchemy import String, Column
Base = declarative_base()


class brands(Base, BaseMixin):
    __tablename__ = "brands"
    name = Column(String(100))
    description = Column(String)
    url = Column(String(255))
