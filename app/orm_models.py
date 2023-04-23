from .database import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String, Float, Boolean, text, ForeignKey
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = "products"
    __schemaname__ = "public"

    product_id = Column(Integer, primary_key=True, nullable=False)
    product_name = Column(String, nullable=False)
    product_price = Column(Float, nullable=False)
    is_sale = Column(Boolean, server_default='True', nullable=False)
    product_inventory = Column(Integer, server_default='0', nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    user = relationship("User")


class User(Base):
    __tablename__ = "users"
    __schemaname__ = "public"
    
    user_id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Vote(Base):
    __tablename__ = "votes"
    __schemaname__ = "public"
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True, nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id", ondelete="CASCADE"), primary_key=True, nullable=False)