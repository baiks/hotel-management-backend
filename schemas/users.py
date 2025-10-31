from sqlalchemy import Column, Integer, String, Boolean, Enum as SqlEnum
from database import Base
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    NORMAL = "NORMAL"
    MANAGER = "MANAGER"


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), index=True)
    last_name = Column(String(255), index=True)
    email = Column(String(255), index=True, unique=True)
    password = Column(String(255), index=True)
    role = Column(SqlEnum(UserRole), index=True, nullable=False, default=UserRole.NORMAL)
