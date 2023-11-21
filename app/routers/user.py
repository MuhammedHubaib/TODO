from fastapi import FastAPI,HTTPException,status,Depends,APIRouter,Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,schema,utilites

router = APIRouter(prefix='/user',
                   tags=['Users'])


@router.post("/",status_code=status.HTTP_201_CREATED,response_model= schema.UserOut)
def CreateUser(user: schema.CreateUser,db: Session= Depends(get_db)):
    
    hashed_password = utilites.hash(user.password)
    user.password = user.password = hashed_password
    
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
    
@router.get("/{id}",response_model=schema.UserOut)
def GetById(id: int,db: Session= Depends(get_db)):
    
    user= db.query(models.Users).filter(models.Users.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The user with ID {id} is not found")
    
    return user
         
@router.get("/",response_model=list[schema.UserOut])
def GetAllUsers(db: Session= Depends(get_db)):
    
    users= db.query(models.Users).all()
    return users


    