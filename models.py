from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class Items(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    price = Column(Integer, index=True)
    is_offer = Column(Boolean, index=True)


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), index=True)
    last_name = Column(String(255), index=True)
    email = Column(String(255), index=True, unique=True)
    password = Column(String(255), index=True)
