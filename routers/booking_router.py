from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models.booking_model import Booking, BookingCreate, BookingUpdate
from services import booking_service

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


@router.post("/", response_model=Booking, status_code=status.HTTP_201_CREATED)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    """
    Create a new booking
    - Validates room availability
    - Checks for date conflicts
    - Validates guest capacity
    """
    return booking_service.create_booking(db, booking)


@router.get("/", response_model=List[Booking])
def get_all_bookings(
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        user_id: Optional[int] = None,
        db: Session = Depends(get_db)
):
    """
    Retrieve all bookings with optional filters
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    - **status**: Filter by booking status (pending, confirmed, cancelled)
    - **user_id**: Filter by user ID
    """
    return booking_service.get_all_bookings(db, skip, limit, status, user_id)


@router.get("/upcoming", response_model=List[Booking])
def get_upcoming_bookings(
        user_id: Optional[int] = None,
        db: Session = Depends(get_db)
):
    """
    Get upcoming bookings (check-in date in the future)
    - **user_id**: Optional filter by user ID
    """
    return booking_service.get_upcoming_bookings(db, user_id)


@router.get("/active", response_model=List[Booking])
def get_active_bookings(db: Session = Depends(get_db)):
    """
    Get currently active bookings (guests currently checked in)
    """
    return booking_service.get_active_bookings(db)


@router.get("/user/{user_id}", response_model=List[Booking])
def get_user_bookings(user_id: int, db: Session = Depends(get_db)):
    """
    Get all bookings for a specific user
    """
    return booking_service.get_user_bookings(db, user_id)


@router.get("/room/{room_id}", response_model=List[Booking])
def get_room_bookings(room_id: int, db: Session = Depends(get_db)):
    """
    Get all bookings for a specific room
    """
    return booking_service.get_room_bookings(db, room_id)


@router.get("/{booking_id}", response_model=Booking)
def get_booking_by_id(booking_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific booking by ID
    """
    booking = booking_service.get_booking_by_id(db, booking_id)

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with id {booking_id} not found"
        )

    return booking


@router.put("/{booking_id}", response_model=Booking)
def update_booking(
        booking_id: int,
        booking_update: BookingUpdate,
        db: Session = Depends(get_db)
):
    """
    Update booking details
    - Validates new dates for conflicts
    - Checks guest capacity if changed
    """
    booking = booking_service.update_booking(db, booking_id, booking_update)

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with id {booking_id} not found"
        )

    return booking


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    """
    Permanently delete a booking by ID
    """
    success = booking_service.delete_booking(db, booking_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with id {booking_id} not found"
        )

    return None


@router.patch("/{booking_id}/cancel", response_model=Booking)
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    """
    Cancel a booking (soft delete - changes status to 'cancelled')
    """
    booking = booking_service.cancel_booking(db, booking_id)

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with id {booking_id} not found"
        )

    return booking


@router.patch("/{booking_id}/confirm", response_model=Booking)
def confirm_booking(booking_id: int, db: Session = Depends(get_db)):
    """
    Confirm a pending booking
    """
    booking = booking_service.confirm_booking(db, booking_id)

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with id {booking_id} not found"
        )

    return booking
