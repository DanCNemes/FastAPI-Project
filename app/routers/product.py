from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import get_db
from .. import orm_models, schema_models, oauth2
from typing import List, Optional

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("/", response_model=List[schema_models.ProductOut])
def get_products(db: Session = Depends(get_db), token_data: schema_models.TokenData = Depends(oauth2.verify_access_token), limit: int = 10,
                 offset: int = 0, search: Optional[str] = ""):

    results = db.query(orm_models.Product, func.count(orm_models.Vote.product_id).label("votes")).join(
             orm_models.Vote, orm_models.Product.product_id == orm_models.Vote.product_id, isouter=True).group_by(
             orm_models.Product.product_id).filter(
             orm_models.Product.product_name.contains(
             search)).limit(
             limit).offset(offset).all()
    
    return results

@router.get("/{id}", response_model=schema_models.ProductOut)
def get_product(id: int, db: Session = Depends(get_db), token_data: schema_models.TokenData = Depends(oauth2.verify_access_token)):
    try:
        product = db.query(orm_models.Product, func.count(orm_models.Vote.product_id).label("votes")).join(
                           orm_models.Vote, orm_models.Product.product_id == orm_models.Vote.product_id,  isouter=True).group_by(
                           orm_models.Product.product_id).filter(
                           orm_models.Product.product_id == id).first()
        if not product:
            raise Exception()
    except(Exception):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post {id} not found")
        
    return product

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema_models.ProductResponse)
def create_product(product: schema_models.ProductCreate, db: Session = Depends(get_db), token_data: schema_models.TokenData = Depends(oauth2.verify_access_token)):
    product_dict = product.dict()
    #Unpack the product dictionary
    new_product = orm_models.Product(user_id=token_data.user_id, **product_dict)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.put("/{id}", response_model=schema_models.ProductResponse)
def update_post(product: schema_models.ProductUpdate, id: int, db: Session = Depends(get_db), token_data: schema_models.TokenData = Depends(oauth2.verify_access_token)):
    product_query = db.query(orm_models.Product).filter(orm_models.Product.product_id == id)
    curr_product = product_query.first()
    if not curr_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product {id} not found")
    if curr_product.user_id != int(token_data.user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Cannot delete product created by another user")
    product_query.update(product.dict(), synchronize_session=False)
    db.commit()
    return curr_product

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db), token_data: schema_models.TokenData = Depends(oauth2.verify_access_token)):
    is_product = db.query(orm_models.Product).filter(orm_models.Product.product_id == id).first()
    if not is_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product {id} not found")
    if is_product.user_id != token_data.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Cannot delete product created by another user")
    db.query(orm_models.Product).filter(orm_models.Product.product_id == id).delete()
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)