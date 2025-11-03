from sqlalchemy import (
    Column, Integer, String, DateTime, Float, ForeignKey, Boolean, Text,
    func, UniqueConstraint, CheckConstraint
)
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Bookings(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign keys
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Booking details
    check_in = Column(DateTime(timezone=True), nullable=False)
    check_out = Column(DateTime(timezone=True), nullable=False)
    guests = Column(Integer, nullable=False, default=1)
    total_price = Column(Float, nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    notes = Column(Text, nullable=True)

    # Audit
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # ✅ Relationships
    room = relationship("Rooms", back_populates="bookings")
    user = relationship("Users", foreign_keys=[user_id])
    created_by_user = relationship("Users", foreign_keys=[created_by])

    __table_args__ = (
        CheckConstraint("check_out > check_in", name="check_dates_valid"),
        UniqueConstraint("room_id", "check_in", "check_out", name="uq_room_booking_period"),
    )
