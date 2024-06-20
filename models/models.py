from models.basemodel import Base
from sqlalchemy import Column,String,Integer,DateTime,Text,func,ForeignKey,Double,Boolean
from sqlalchemy.orm import relationship
from factory import bcrypt
from enum import Enum as pyenum

class RoleEnum(pyenum):
  user = 1
  admin = 2


class User(Base):
    
    __tablename__ = 'user_table'
    
    name = Column(String(50),nullable=False)
    email = Column(String(60),nullable=False,unique=True)
    password = Column(Text,nullable=False)
    role_id = Column(Integer,default=RoleEnum.user.value,nullable=False)
    
    activities = relationship('Activity',uselist=True, back_populates='user')
    skills = relationship('Skills',back_populates='user')
    
    def __init__(self,name,email,password) -> None:
        self.name = name
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.email = email

class Activity(Base):
    
    __tablename__ = 'user_activity_table'
    
    user_id = Column(Integer,ForeignKey('user_table.id'),nullable=False)
    login_at = Column(DateTime(timezone=True),default=func.now())
    logout_at = Column(DateTime(timezone=True))
    session_id = Column(String(50),nullable=False)
    
    def __init__(self,user):
        self.user = user
    
    user = relationship('User', back_populates='activities')
    

class Skills(Base):
  
  __tablename__ = 'user_skill_table'
  
  skill_name = Column(String(50),nullable=False)
  user_id = Column(Integer,ForeignKey('user_table.id'),nullable=False)
  
  user = relationship('User',back_populates='skills')
  
  