from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import schemas, database, models, oauth2

router = APIRouter(
    prefix="/vote",
    tags=['Votes']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote_schema: schemas.Vote, db: Session = Depends(database.get_db),
         current_user: models.User = Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote_schema.post_id,
                                               models.Votes.user_id == current_user.id)

    post = db.query(models.Post).filter(models.Post.id == vote_schema.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {vote_schema.post_id} Not Found")

    found_vote = vote_query.first()
    if vote_schema.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.id} has already voted on post with id of {vote_schema.post_id}"
            )
        new_vote = models.Votes(post_id=vote_schema.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": 'successfully added vote'}

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Vote does not exits')
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully delete vote"}
