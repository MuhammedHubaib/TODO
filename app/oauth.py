from jose import jwt,JWTError
from datetime import datetime,timedelta
from . import schema,models,database
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import settings
from  sqlalchemy.orm import Session


Oauth2_schema= OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY =settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def creating_token(data: dict):
    to_encode= data.copy()
    
    expire_time= datetime.utcnow()+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire_time})
    encoded_jwt= jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify(token:str, credentials_expectation):
    
    try:
        payload= jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        id:str = payload.get('user_id')
        
        if id is None:
            raise credentials_expectation
        token_data= schema.TokenData(id=id)
    
    except JWTError:
        raise credentials_expectation
    
    return token_data

def get_current_user(token:str = Depends(Oauth2_schema),db:Session = Depends(database.get_db)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Couldn't validate the Credentials",
                                          headers={'WWW-Authenticate':'Bearer'})
    
    token = verify(token,credentials_exception)
    user = db.query(models.Users).filter(models.Users.id == token.id).first()
    
    return user
    