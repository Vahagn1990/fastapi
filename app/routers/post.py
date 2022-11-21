from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get("/", response_model =List[schemas.PostOut]) # Import List from Typing to convert many responses into list

def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 2, skip: int = 0, search: Optional[str] = ""):
    
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() # order_by(models.Post.id).first()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts

@router.get("/{id}", response_model=schemas.PostOut)
def get_post_by_id(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    #one_post = db.query(models.Post).filter(models.Post.id == id).first()

    one_post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if one_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: ({id}) wasn't found")
    return one_post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # new_post = models.Post(title = post.title, content=post.content, published=post.published)

    new_post = models.Post(owner_id=current_user.id, **post.dict()) # Not to writ all necessary fileds into (models.Post()) we using the /**post.dict()/
    
    db.add(new_post)
    db.commit() 
    db.refresh(new_post) # to get new info into (new_post)
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    del_post_query = db.query(models.Post).filter(models.Post.id == id)
    del_post = del_post_query.first()

    if del_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Such id: {id} not present")

    if del_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You don't have access to this post")

    del_post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):  
    
    upt_post_query = db.query(models.Post).filter(models.Post.id == id)
    upt_post = upt_post_query.first()
    if upt_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Such id: {id} not present")

    if upt_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You don't have access to this post")

    upt_post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return upt_post_query.first() # get a first post