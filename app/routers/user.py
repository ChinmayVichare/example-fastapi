from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session, session
from .. import models,schemas,utils
from ..database import get_db

router = APIRouter(tags=['users'])

@router.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):

    #hash password
    hashed_password =utils.hash(user.password)
    user.password=hashed_password
    #///
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/users/{id}",response_model=schemas.UserResponse)
def get_user(id:int, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user with id {id} does not exists")

    return user