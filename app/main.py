from fastapi import FastAPI
from . import models
from .database import engine
from .routers import user,task,auth
from fastapi.middleware.cors import CORSMiddleware

origins=["*"]


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def start():
    return {"message": "TO_DO"}

app.include_router(user.router)
app.include_router(task.router)
app.include_router(auth.router)