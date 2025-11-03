from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from schemas.bookings import Bookings
from models.booking_model import BookingCreate, BookingUpdate
from services.room_service import get_room_by_id
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import datetime


def get_all_bookings(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        user_id: Optional[int] = None
) -> List[Bookings]:
    """Get all bookings with optional filters"""
    query = db.query(Bookings)

    if status:
        query = query.filter(Bookings.status == status)

    if user_id:
        query = query.filter(Bookings.user_id == user_id)

    return query.offset(skip).limit(limit).all()


def get_booking_by_id(db: Session, booking_id: int) -> Optional[Bookings]:
    """Get a single booking by ID"""
    return db.query(Bookings).filter(Bookings.id == booking_id).first()


def check_room_availability(
        db: Session,
        room_id: int,
        check_in: datetime,
        check_out: datetime,
        exclude_booking_id: Optional[int] = None
) -> bool:
    """Check if a room is available for the given date range"""
    query = db.query(Bookings).filter(
        Bookings.room_id == room_id,
        Bookings.status.in_(["pending", "confirmed"]),  # Only check active bookings
        or_(
            # New booking starts during existing booking
            and_(Bookings.check_in <= check_in, Bookings.check_out > check_in),
            # New booking ends during existing booking
            and_(Bookings.check_in < check_out, Bookings.check_out >= check_out),
            # New booking completely contains existing booking
            and_(Bookings.check_in >= check_in, Bookings.check_out <= check_out)
        )
    )

    # Exclude current booking when updating
    if exclude_booking_id:
        query = query.filter(Bookings.id != exclude_booking_id)

    conflicting_bookings = query.first()
    return conflicting_bookings is None


def create_booking(db: Session, booking: BookingCreate) -> Bookings:
    """Create a new booking"""
    # Validate dates
    if booking.check_out <= booking.check_in:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Check-out date must be after check-in date"
        )

    # Check if room exists
    room = get_room_by_id(db, booking.room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with id {booking.room_id} not found"
        )

    # Check if room is available
    if not room.is_available or room.is_under_maintenance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Room is not available for booking"
        )

    # Check for booking conflicts
    if not check_room_availability(db, booking.room_id, booking.check_in, booking.check_out):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Room is already booked for the selected dates"
        )

    # Check guest capacity
    if booking.guests > room.capacity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Number of guests ({booking.guests}) exceeds room capacity ({room.capacity})"
        )

    # Create booking
    booking_data = booking.dict()
    db_booking = Bookings(**booking_data)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


def update_booking(db: Session, booking_id: int, booking_update: BookingUpdate) -> Optional[Bookings]:
    """Update an existing booking"""
    db_booking = get_booking_by_id(db, booking_id)
    if not db_booking:
        return None

    # Get update data
    update_data = {k: v for k, v in booking_update.dict().items() if v not in [None, ""]}

    # If dates are being updated, validate them
    check_in = update_data.get("check_in", db_booking.check_in)
    check_out = update_data.get("check_out", db_booking.check_out)

    if check_out <= check_in:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Check-out date must be after check-in date"
        )

    # Check for conflicts if dates are changing
    if "check_in" in update_data or "check_out" in update_data:
        if not check_room_availability(
                db,
                db_booking.room_id,
                check_in,
                check_out,
                exclude_booking_id=booking_id
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Room is already booked for the selected dates"
            )

    # Check guest capacity if being updated
    if "guests" in update_data:
        room = get_room_by_id(db, db_booking.room_id)
        if update_data["guests"] > room.capacity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Number of guests exceeds room capacity ({room.capacity})"
            )

    # Apply updates
    for key, value in update_data.items():
        setattr(db_booking, key, value)

    db.commit()
    db.refresh(db_booking)
    return db_booking


def delete_booking(db: Session, booking_id: int) -> bool:
    """Delete a booking by ID"""
    db_booking = get_booking_by_id(db, booking_id)
    if not db_booking:
        return False

    db.delete(db_booking)
    db.commit()
    return True


def cancel_booking(db: Session, booking_id: int) -> Optional[Bookings]:
    """Cancel a booking (soft delete by changing status)"""
    db_booking = get_booking_by_id(db, booking_id)
    if not db_booking:
        return None

    if db_booking.status == "cancelled":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking is already cancelled"
        )

    db_booking.status = "cancelled"
    db.commit()
    db.refresh(db_booking)
    return db_booking


def confirm_booking(db: Session, booking_id: int) -> Optional[Bookings]:
    """Confirm a pending booking"""
    db_booking = get_booking_by_id(db, booking_id)
    if not db_booking:
        return None

    if db_booking.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot confirm booking with status: {db_booking.status}"
        )

    db_booking.status = "confirmed"
    db.commit()
    db.refresh(db_booking)
    return db_booking


def get_user_bookings(db: Session, user_id: int) -> List[Bookings]:
    """Get all bookings for a specific user"""
    return db.query(Bookings).filter(Bookings.user_id == user_id).all()


def get_room_bookings(db: Session, room_id: int) -> List[Bookings]:
    """Get all bookings for a specific room"""
    return db.query(Bookings).filter(Bookings.room_id == room_id).all()


def get_upcoming_bookings(db: Session, user_id: Optional[int] = None) -> List[Bookings]:
    """Get upcoming bookings (check-in date in the future)"""
    query = db.query(Bookings).filter(
        Bookings.check_in > datetime.now(),
        Bookings.status.in_(["pending", "confirmed"])
    )

    if user_id:
        query = query.filter(Bookings.user_id == user_id)

    return query.order_by(Bookings.check_in).all()


def get_active_bookings(db: Session) -> List[Bookings]:
    """Get currently active bookings (guests are currently checked in)"""
    now = datetime.now()
    return db.query(Bookings).filter(
        Bookings.check_in <= now,
        Bookings.check_out > now,
        Bookings.status == "confirmed"
    ).all()