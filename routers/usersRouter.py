from models import SessionLocal, Users
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from model.UserModel import UserCreate

router = APIRouter(prefix="/api/users", tags=["Users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(Users).all()
    if users is None:
        raise HTTPException(status_code=200, detail=[])
    return users


@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = Users(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/{id}")
def get_user(item_id: int, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == item_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
