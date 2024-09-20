from sqlalchemy.orm import Session
from models import SessionLocal, Items, Base
from fastapi import Depends, HTTPException, APIRouter
from model.ItemModel import ItemCreate, ItemUpdate

router = APIRouter(prefix="/api/items", tags=["Items"])


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None, h: Union[int, None] = None):
#     return {"item_id": item_id, "q": q, "h": h}


# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}


@router.post("/")
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Items(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/")
def get_items(db: Session = Depends(get_db)):
    item = db.query(Items).all()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.get("/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Items).filter(Items.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{item_id}")
def update_item(item_id: int, itemUpdate: ItemUpdate, db: Session = Depends(get_db)):
    item = db.query(Items).filter(Items.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in itemUpdate.dict().items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item
