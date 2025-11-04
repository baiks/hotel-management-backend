from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from utils.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, verify_token
from datetime import timedelta
from models.user_model import UserCreate, LoginRequest, Token, UserUpdate
from services.user_service import (
    get_all_users,
    get_user_by_id,
    create_user,
    update_user,
    authenticate_user_service
)

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/")
def read_users(db: Session = Depends(get_db), _: str = Depends(verify_token)):
    users = get_all_users(db)
    return users or []


@router.get("/{id}")
def read_user(id: int, db: Session = Depends(get_db), _: str = Depends(verify_token)):
    user = get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/")
def add_user(user: UserCreate, db: Session = Depends(get_db), _: str = Depends(verify_token)):
    return create_user(db, user)


@router.put("/{id}")
def modify_user(id: int, user: UserUpdate, db: Session = Depends(get_db), _: str = Depends(verify_token)):
    updated_user = update_user(db, id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.post("/login", response_model=Token)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user_service(db, data.email, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    print('Users:: ', user)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": data.email, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
