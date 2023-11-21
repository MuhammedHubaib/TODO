from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base
from datetime import datetime



class List(Base):
    __tablename__ = "tasks"
    
    id= Column(Integer,primary_key=True,nullable=False,index=True,unique=True,autoincrement=True)
    task = Column(String,nullable=False)
    ToBeDone = Column(TIMESTAMP, server_default=text('now()'), nullable=False)
    current_id = Column(Integer,ForeignKey('User.id',ondelete='CASCADE'),nullable=False)
    created_at= Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
     

class Users(Base):
    __tablename__ = "User"
    
    id= Column(Integer,primary_key=True,nullable=False,index=True,unique=True,autoincrement=True)
    email= Column(String,nullable=False,unique=True)
    password= Column(String,nullable=False)
    created_at= Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))