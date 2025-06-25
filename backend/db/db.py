# coding:utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.config import mysql_config
from contextlib import contextmanager
from urllib.parse import quote_plus

safe_password = quote_plus(mysql_config.get('password'))
engine_url = f"mysql+mysqlconnector://{mysql_config.get('username')}:{safe_password}@localhost:3306/rpj"

engine = create_engine(engine_url)
SessionFactory = sessionmaker(bind=engine)


@contextmanager
def get_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()
