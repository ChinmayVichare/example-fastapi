
from random import randrange
from typing import Optional,List
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import outerjoin
from sqlalchemy.sql.functions import func
from .. import models,schemas,oauth2
from ..database import get_db


router = APIRouter(prefix="/posts",tags=['posts'])

@router.get("/" ,response_model=List[schemas.PostOut])
def get_posts(db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]=""):
    print(limit)
    # posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts =db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    # cursor.execute("""select * from posts""")
    # posts=cursor.fetchall()
    return posts



@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.postResponse)
def createpost(new_Post:schemas.PostCreate,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #//// Using ORM
    # new_Post1=models.Post(title=new_Post.title,content=new_Post.content,published=new_Post.published)
    #//// write like above or you can unpack using **new_post1.dict()
    print(current_user.email)
    new_Post1=models.Post(owner_id=current_user.id,**new_Post.dict())
    db.add(new_Post1)
    db.commit()
    db.refresh(new_Post1)

    #//// Using normal postgres databse
    # cursor.execute("""insert into posts(title,content,published) values(%s,%s,%s) returning *""",(new_Post.title,new_Post.content,new_Post.published))
    # new_Post1=cursor.fetchone()
    # conn.commit()
    #//// 

    #.///using local data
    # Post_dict=new_Post.dict()
    # Post_dict['id']=randrange(0,1000)
    # my_posts.append(Post_dict)
    # return{"data":Post_dict}
    #/////
    return new_Post1


@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int,response:Response,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
     #//// Using ORM
    # post=db.query(models.Post).filter(models.Post.id==id).first()

    post =db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(
        models.Post.id).filter(models.Post.id==id).first()
    #//// Using normal postgres databse
    # cursor.execute("""select * from posts where id= %s""",(str(id),))
    # post=cursor.fetchone()
    #////

     #.///using local data
    # post=find_post(int(id))
    #////
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} not  found")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return{"message":f"post with {id} not  found"}

    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #//// Using ORM
    deleted_post_query=db.query(models.Post).filter(models.Post.id==id)

    deleted_post=deleted_post_query.first()
    if  deleted_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} does not exits")

    if  deleted_post.owner_id !=current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN,detail="not authorized to perform requested action")

    deleted_post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    #//// Using normal postgres databse
    # cursor.execute("""delete from posts where id=%s returning *""",(str(id),))
    # deleted_post=cursor.fetchone()
    # conn.commit()
     #////

    #.///using local data
    # index =find_index_post(id)
    #////

    #/same for local and normal postgres dtabase
    # if deleted_post ==None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} does not exits")
    # # my_posts.pop(index)
    # return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model=schemas.postResponse)
def update_post(id:int,updated_post:schemas.PostCreate,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #//// Using ORM
    updated_post_query=db.query(models.Post).filter(models.Post.id==id)

    updated_post1=updated_post_query.first()

    if updated_post1 ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} does not exits")

    if updated_post1.owner_id !=current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN,detail="not authorized to perform requested action")   

    updated_post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return updated_post_query.first()
    #//// Using normal postgres databse
    # cursor.execute("""update posts set title =%s, content=%s,published=%s where id=%s returning *""",(updated_post.title,updated_post.content,updated_post.published,str(id),))
    # updated_post1=cursor.fetchone()
    # conn.commit()

    #.///using local data
    # index =find_index_post(id)
     #////

     #/same for local and normal postgres dtabase
    # if updated_post1 ==None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} does not exits")
    
    # post_dict=updated_post.dict()
    # post_dict['id']=id
    # my_posts[index]=post_dict
    # return{"data":updated_post1}