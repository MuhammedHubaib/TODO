from fastapi import FastAPI,HTTPException,status,Depends,APIRouter,Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,schema,oauth


router = APIRouter(prefix='/task',
                   tags=['Task'])

@router.get("/",response_model=list[schema.Taskout])
def GetAll(db: Session= Depends(get_db),current_user:int = Depends(oauth.get_current_user)):
    
    AllTask= db.query(models.List).filter(models.List.current_id == current_user.id)
    task=AllTask.all()    
    
#print(current_user.id)
    return task

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.Taskout)
def CreateTask(task: schema.TaskIn,db: Session= Depends(get_db),current_user:int = Depends(oauth.get_current_user)):
    
    new_task= models.List(current_id= current_user.id,**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    return new_task

@router.get("/{id}",response_model=schema.Taskout)
def GetById(id:int, db: Session= Depends(get_db),current_user:int = Depends(oauth.get_current_user)):
    
    GetTask= db.query(models.List).filter(models.List.id == id)
    task = GetTask.first()
    
   # print(list[task])
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The task with ID {id} is not found")
    
    print(current_user.id)
    if task.current_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f'There no task with ID {id} found')
    
    return task
    
@router.put("/{id}",response_model=schema.Taskout)
def UpdateTask(id:int,updated_task:schema.TaskIn,db: Session= Depends(get_db),current_user:int = Depends(oauth.get_current_user)):
    
    task_query= db.query(models.List).filter(models.List.id == id)
    task= task_query.first()
    
    if not task:
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The task with id {id} is not found")
    
    if task.current_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f'There no task with ID {id} found')
    
    task_query.update(updated_task.dict(),synchronize_session=False)
    db.commit()
    
    return task_query.first()    
    
@router.delete("/{id}")
def DeleteTask(id: int,db: Session= Depends(get_db),current_user:int = Depends(oauth.get_current_user)):
    
    task_query= db.query(models.List).filter(models.List.id == id)
    task= task_query.first()
    
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The task with ID {id} is not found")
    
    if task.current_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f'There no task with ID {id} found')
    
    task_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)