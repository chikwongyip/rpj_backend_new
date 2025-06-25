from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
Base = declarative_base()


class CompanyInfo(Base):
    __tablename__ = 'company_info'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    description = Column(String)
    logo_url = Column(String(255))
    icp_number = Column(String(50))
    created_at = Column(DateTime)
    update_at = Column(DateTime)
