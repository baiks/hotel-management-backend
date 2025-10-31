from pydantic import BaseModel, Field, EmailStr
from typing import Optional

from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    NORMAL = "NORMAL"
    MANAGER = "MANAGER"


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr = Field(..., example="john.doe@example.com")
    password: str = Field(..., min_length=6, example="strongpassword123")
    role: UserRole = Field(default=UserRole.NORMAL, example="NORMAL")


class LoginRequest(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
