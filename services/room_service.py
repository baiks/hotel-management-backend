from sqlalchemy.orm import Session
from schemas.rooms import Rooms
from models.rooms_model import RoomCreate, RoomUpdate
from fastapi import HTTPException, status
from typing import List, Optional


def get_all_rooms(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        is_available: Optional[bool] = None,
        room_type: Optional[str] = None
) -> List[Rooms]:
    """Get all rooms with optional filters"""
    query = db.query(Rooms)

    if is_available is not None:
        query = query.filter(Rooms.is_available == is_available)

    if room_type:
        query = query.filter(Rooms.type == room_type)

    return query.offset(skip).limit(limit).all()


def get_room_by_id(db: Session, room_id: int) -> Optional[Rooms]:
    """Get a single room by ID"""
    return db.query(Rooms).filter(Rooms.id == room_id).first()


def get_room_by_number(db: Session, room_number: str) -> Optional[Rooms]:
    """Get a room by room number"""
    return db.query(Rooms).filter(Rooms.room_number == room_number).first()


def create_room(db: Session, room: RoomCreate) -> Rooms:
    """Create a new room"""
    # Check if room number already exists
    existing_room = get_room_by_number(db, room.room_number)
    if existing_room:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Room number {room.room_number} already exists"
        )

    room_data = room.dict()
    db_room = Rooms(**room_data)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


def update_room(db: Session, room_id: int, room_update: RoomUpdate) -> Optional[Rooms]:
    """Update an existing room"""
    db_room = get_room_by_id(db, room_id)
    if not db_room:
        return None

    # Update only provided fields
    update_data = {k: v for k, v in room_update.dict().items() if v not in [None, ""]}

    for key, value in update_data.items():
        setattr(db_room, key, value)

    db.commit()
    db.refresh(db_room)
    return db_room


def delete_room(db: Session, room_id: int) -> bool:
    """Delete a room by ID"""
    db_room = get_room_by_id(db, room_id)
    if not db_room:
        return False

    db.delete(db_room)
    db.commit()
    return True


def aget_available_rooms(db: Session) -> List[Rooms]:
    """Get only available rooms (not under maintenance)"""
    return db.query(Rooms).filter(
        Rooms.is_available == True,
        Rooms.is_under_maintenance == False
    ).all()


def update_room_availability(db: Session, room_id: int, is_available: bool) -> Optional[Rooms]:
    """Update room availability status"""
    db_room = get_room_by_id(db, room_id)
    if not db_room:
        return None

    db_room.is_available = is_available
    db.commit()
    db.refresh(db_room)
    return db_room


def set_room_maintenance(db: Session, room_id: int, under_maintenance: bool) -> Optional[Rooms]:
    """Set room maintenance status"""
    db_room = get_room_by_id(db, room_id)
    if not db_room:
        return None

    db_room.is_under_maintenance = under_maintenance
    if under_maintenance:
        db_room.is_available = False  # Make unavailable when under maintenance

    db.commit()
    db.refresh(db_room)
    return db_room
