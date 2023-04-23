from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import orm_models, schema_models, oauth2
from ..utils import hash

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema_models.UserCreateResponse)
def create_user(user: schema_models.UserCreate, db: Session = Depends(get_db)):
    #hash the password - user.password
    user.password = hash(user.password)
    user_dict = user.dict()
    #Unpack the product dictionary
    new_user = orm_models.User(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schema_models.UserGetResponse)
def get_user(id: int, db: Session = Depends(get_db), token_data: int = Depends(oauth2.verify_access_token)):
    try:
        user = db.query(orm_models.User).filter(orm_models.User.user_id == id).one_or_none()
        if not user:
            raise Exception()
    except(Exception):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User {id} not found")
        
    return user
