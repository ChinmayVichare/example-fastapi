from os import access
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from app import models
from .. import schemas,utils,oauth2
from ..database import get_db

router = APIRouter(tags=['Authentication'])


@router.post('/login',response_model=schemas.Token)
def login(user_crenditals:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    #when use OAuth2PasswordRequestForm it will store anything ithing into username varaible example username=email
    user=db.query(models.User).filter(models.User.email==user_crenditals.username).first()

    if not user:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN,detail="invalid crendtials")
    
    if not utils.verify(user_crenditals.password,user.password):
        raise HTTPException(status_code=HTTP_403_FORBIDDEN,detail="invalid crendtials")
    
    #create Token
    access_token= oauth2.create_access_token(data={"user_id":user.id})
    #return Token
    return{"access_token":access_token,"token_type":"bearer"}
