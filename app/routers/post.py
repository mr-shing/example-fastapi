from typing import List, Optional

from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user),
              limit: int = 20, offset: int = 0, search: Optional[str] = ""):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).offset(offset).limit(limit).all()
    results = (db.query(models.Post, func.count(models.Votes.post_id).label('votes'))
               .join(models.Votes,
                     models.Votes.post_id == models.Post.id,
                     isouter=True
                     )
               .filter(models.Post.title.contains(search))
               .group_by(models.Post.id).offset(offset).limit(limit).all())

    return results


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post, func.count(models.Votes.post_id).label('votes')).join(
        models.Votes, models.Votes.post_id == models.Post.id,
        isouter=True).filter(models.Post.id == id).group_by(models.Post.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post Not Found')
    return post


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING * """,(post.title,
    # post.content,post.published)) connect.commit() new_post = cursor.fetchone()
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post_request: schemas.UpdatePost, db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id = %s RETURNING * """,(post.title,
    # post.content,post.published,str(id))) updated_post = cursor.fetchone() if updated_post == None: raise
    # HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Post Not Found') connt.commit()
    update_query = db.query(models.Post).filter(models.Post.id == id)
    post = update_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post Not Found')
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized to perform request action')
    update_query.update(post_request.model_dump(), synchronize_session=False)
    db.commit()
    return update_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute("DELETE FROM posts WHERE id=%s RETURNING* ",(str(id),))
    # deleted_post = cursor.fetchone()
    # connect.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post Not Found')
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized to perform request action')
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
