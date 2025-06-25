# coding:utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.config import mysql_config
from contextlib import contextmanager
from urllib.parse import quote_plus
# print(mysql_config.get('username'))
# engine_url = "mysql+mysqlconnector://" + \
#     mysql_config.get('username') + ":" + \
#     mysql_config.get("password")+"@"+mysql_config.get("url") + \
#     ":3306/"+mysql_config.get("schema")

# engine_url = """
# mysql+mysqlconnector://{0}:{1}@{2}:3306/{3}
# """.format(mysql_config.get('username'), mysql_config.get("password"), mysql_config.get("url"), mysql_config.get("schema"))
# print(engine_url)
safe_password = quote_plus(mysql_config.get('password'))
engine_url = f"mysql+mysqlconnector://{mysql_config.get('username')}:{safe_password}@localhost:3306/rpj"
print(engine_url)
engine = create_engine(engine_url)
SessionFactory = sessionmaker(bind=engine)


@contextmanager
def get_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()
