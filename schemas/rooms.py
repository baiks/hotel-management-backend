from sqlalchemy import (
    Column, Integer, String, Boolean, Float, Text,
    Enum, ForeignKey, DateTime, func, UniqueConstraint, Index
)
from sqlalchemy.orm import relationship
from database import Base
import enum

from schemas.bookings import Bookings
from schemas.users import Users


class RoomType(enum.Enum):
    single = "Single"
    double = "Double"
    twin = "Twin"
    suite = "Suite"
    deluxe = "Deluxe"
    family = "Family"


class Rooms(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    room_number = Column(String(10), nullable=False)
    floor = Column(Integer, nullable=True)
    type = Column(Enum(RoomType), nullable=False)
    description = Column(Text, nullable=True)

    price_per_night = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False, default="USD")
    capacity = Column(Integer, nullable=False, default=2)
    is_available = Column(Boolean, nullable=False, default=True)
    is_under_maintenance = Column(Boolean, nullable=False, default=False)
    has_offer = Column(Boolean, default=False)
    discount_percent = Column(Float, default=0.0)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # ✅ Corrected: relationship to Bookings (class name, not table name)
    bookings = relationship("Bookings", back_populates="room", cascade="all, delete")

    # ✅ Reference to user who created the room
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_by_user = relationship("Users", back_populates="rooms_created")

    __table_args__ = (
        UniqueConstraint("room_number", name="uq_room_room_number"),
        Index("ix_room_type_availability", "type", "is_available"),
    )
