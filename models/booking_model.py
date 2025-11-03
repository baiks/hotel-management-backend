from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ----- Base schema -----
class BookingBase(BaseModel):
    room_id: int
    user_id: Optional[int] = None
    check_in: datetime
    check_out: datetime
    guests: int = Field(default=1, ge=1)
    notes: Optional[str] = None


# ----- Create schema -----
class BookingCreate(BookingBase):
    total_price: float = Field(..., gt=0)
    status: str = Field(default="pending")
    created_by: Optional[int] = None


# ----- Update schema -----
class BookingUpdate(BaseModel):
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None
    guests: Optional[int] = None
    status: Optional[str] = None
    notes: Optional[str] = None


# ----- Read schema (response) -----
class Booking(BookingBase):
    id: int
    total_price: float
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None

    class Config:
        orm_mode = True
