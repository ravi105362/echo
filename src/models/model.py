from src.database import Base
from sqlalchemy import Column, Integer, String, JSON


class Endpoint(Base):
    __tablename__ = "endpoint"
    id = Column(Integer, primary_key=True, index=True)
    verb = Column(String)
    path = Column(String, unique=True)
    code = Column(String)
    headers = Column(JSON, nullable=True)
    body = Column(String, nullable=True)
