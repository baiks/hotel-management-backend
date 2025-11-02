from sqlalchemy import Column, Integer, String, Boolean, Enum as SqlEnum, DateTime, ForeignKey, func
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
    created_on = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_on = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
