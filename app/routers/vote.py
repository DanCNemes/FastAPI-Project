from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import orm_models, schema_models, oauth2
from typing import List, Optional

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(vote: schema_models.Vote, db: Session = Depends(get_db), token_data: schema_models.TokenData = Depends(oauth2.verify_access_token)):
    vote_query = db.query(orm_models.Vote).filter(orm_models.Vote.user_id == token_data.user_id).filter(orm_models.Vote.product_id == vote.product_id)
    if vote.dir == 1:
        if vote_query.one_or_none():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Product {vote.product_id} is already liked")
        try:
            new_vote = orm_models.Vote(user_id=token_data.user_id, product_id=vote.product_id)
            db.add(new_vote)
            db.commit()
            db.refresh(new_vote)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid input")
        return new_vote
    if vote.dir == 0:
        if not vote_query.one_or_none():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Vote does not exist")
        vote_query.delete()
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)