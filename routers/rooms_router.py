from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models.rooms_model import Room, RoomBase, RoomUpdate
from services import room_service
from utils.auth import get_current_user

router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)


@router.post("/", response_model=Room, status_code=status.HTTP_201_CREATED)
def create_room(room: RoomBase, db: Session = Depends(get_db), current_user_data: dict = Depends(get_current_user)):
    """
    Create a new room in the hotel
    """
    return room_service.create_room(db, room, current_user_data)


@router.get("/", response_model=List[Room])
def get_all_rooms(
        skip: int = 0,
        limit: int = 100,
        is_available: Optional[bool] = None,
        room_type: Optional[str] = None,
        db: Session = Depends(get_db)
):
    """
    Retrieve all rooms with optional filters
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    - **is_available**: Filter by availability status
    - **room_type**: Filter by room type
    """
    return room_service.get_all_rooms(db, skip, limit, is_available, room_type)


@router.get("/available", response_model=List[Room])
def get_available_rooms(db: Session = Depends(get_db)):
    """
    Retrieve only available rooms (not under maintenance and available for booking)
    """
    return room_service.get_available_rooms(db)


@router.get("/{room_id}", response_model=Room)
def get_room_by_id(room_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific room by ID
    """
    room = room_service.get_room_by_id(db, room_id)

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with id {room_id} not found"
        )

    return room


@router.put("/{room_id}", response_model=Room)
def update_room(room_id: int, room_update: RoomUpdate, db: Session = Depends(get_db)):
    """
    Update room details
    """
    room = room_service.update_room(db, room_id, room_update)

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with id {room_id} not found"
        )

    return room


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(room_id: int, db: Session = Depends(get_db)):
    """
    Delete a room by ID
    """
    success = room_service.delete_room(db, room_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with id {room_id} not found"
        )

    return None


@router.patch("/{room_id}/availability", response_model=Room)
def update_room_availability(
        room_id: int,
        is_available: bool,
        db: Session = Depends(get_db)
):
    """
    Update room availability status
    """
    room = room_service.update_room_availability(db, room_id, is_available)

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with id {room_id} not found"
        )

    return room


@router.patch("/{room_id}/maintenance", response_model=Room)
def set_room_maintenance(
        room_id: int,
        under_maintenance: bool,
        db: Session = Depends(get_db)
):
    """
    Set room maintenance status
    When set to maintenance, room automatically becomes unavailable
    """
    room = room_service.set_room_maintenance(db, room_id, under_maintenance)

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with id {room_id} not found"
        )

    return room
