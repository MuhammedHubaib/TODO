from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime

class TaskIn(BaseModel):
    
    task: str
    ToBeDone: datetime

class Taskout(BaseModel):
    
    id: int
    task: str
    ToBeDone: datetime
    current_id: int
    created_at: datetime


class CreateUser(BaseModel):
    
    email: EmailStr
    password: str
    
class UserOut(BaseModel):
    
    id:int
    email: EmailStr
    
class TokenData(BaseModel):
    
    id: Optional[int] = None
    
    