# coding:utf-8
from sqlalchemy import Column, Integer, DateTime, String
import datetime


class BaseMixin:
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False,
                        default=datetime.datetime.now)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.datetime.now)
