from model.LoginRequest import LoginRequest
from model.Token import Token
from models import Users
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from model.UserModel import UserCreate
from database import get_db
from passlib.context import CryptContext
from utils.auth import (
    authenticate_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    hash_password,
    verify_token
)
from datetime import timedelta

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/")
def get_users(db: Session = Depends(get_db), token: str = Depends(verify_token)):
    print('Token: ', token)
    users = db.query(Users).all()
    if users is None:
        raise HTTPException(status_code=200, detail=[])
    return users


@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_data = user.dict()
    user_data["password"] = hash_password(user.password)
    db_user = Users(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login", response_model=Token)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(data.email, data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": data.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
