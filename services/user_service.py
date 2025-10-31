from sqlalchemy.orm import Session
from schemas.users import Users
from utils.auth import hash_password, authenticate_user
from models.user_model import UserCreate, UserUpdate


def get_all_users(db: Session):
    return db.query(Users).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(Users).filter(Users.id == user_id).first()


def create_user(db: Session, user: UserCreate):
    user_data = user.dict()
    user_data["password"] = hash_password(user.password)
    db_user = Users(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None

    update_data = {k: v for k, v in user_update.dict().items() if v not in [None, ""]}
    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user_service(db: Session, email: str, password: str):
    return authenticate_user(email, password, db)
