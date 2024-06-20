from sqlalchemy import Column,Integer,DateTime,func
from config import db

class Base(db.Model):
    
    __abstract__ = True
    
    id = Column(Integer, primary_key = True, autoincrement=True)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    updated_at = Column(DateTime(timezone=True),server_onupdate=func.now(),default=func.now())
    