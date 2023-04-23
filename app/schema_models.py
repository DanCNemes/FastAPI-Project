from pydantic import BaseModel, EmailStr, conint
from datetime import datetime


class UserLogin(BaseModel):
    password: str
    email: EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserCreateResponse(BaseModel):
    user_id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class UserGetResponse(BaseModel):
    email: EmailStr
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: int
    exp: int


class Product(BaseModel):
    product_name: str
    product_price: float
    is_sale: bool = False
    product_inventory: int = 0
    class Config:
        orm_mode = True

class ProductCreate(Product):
    pass

class ProductUpdate(Product):
    pass

class ProductResponse(BaseModel):
    product_id: int
    product_name: str
    product_price: float
    user: UserCreateResponse
    class Config:
        orm_mode = True

class ProductOut(BaseModel):
    Product: Product
    votes: int
    class Config:
        orm_mode = True

class Vote(BaseModel):
    product_id: int
    dir: conint(ge=0, le=1)