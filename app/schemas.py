from os import access
from re import I
from typing import Optional
from psycopg2 import connect
from pydantic import BaseModel,EmailStr
from datetime import datetime
from pydantic.types import conint

from sqlalchemy.sql.sqltypes import String


class PostBase(BaseModel):
    title:str
    content:str
    published:bool=True
    # rating: Optional[int]=None

class PostCreate(PostBase):
    pass




class UserResponse(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config:
        orm_mode = True





class postResponse(PostBase):
    id:int
    created_at:datetime
    owner_id:str
    owner:UserResponse
    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: postResponse
    votes: int

    class Config:
        orm_mode = True

        
class UserCreate(BaseModel):
    email:EmailStr
    password:str


class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str]=None

class Vote(BaseModel):
    post_id:int
    dir:conint(le=1)