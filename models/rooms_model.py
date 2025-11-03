from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


# Match your RoomType enum from the model
class RoomType(str, Enum):
    single = "Single"
    double = "Double"
    twin = "Twin"
    suite = "Suite"
    deluxe = "Deluxe"
    family = "Family"


# ----- Base schema -----
class RoomBase(BaseModel):
    room_number: str = Field(..., example="101")
    floor: Optional[int] = Field(None, example=1)
    type: RoomType
    description: Optional[str] = None
    price_per_night: float = Field(..., gt=0)
    currency: str = Field(default="USD", example="USD")
    capacity: int = Field(default=2, ge=1)
    is_available: bool = True
    is_under_maintenance: bool = False
    has_offer: bool = False
    discount_percent: float = 0.0


# ----- Create schema -----
class RoomCreate(RoomBase):
    created_by: Optional[int] = None  # user ID creating the room


# ----- Update schema -----
class RoomUpdate(BaseModel):
    description: Optional[str] = None
    price_per_night: Optional[float] = None
    is_available: Optional[bool] = None
    is_under_maintenance: Optional[bool] = None
    has_offer: Optional[bool] = None
    discount_percent: Optional[float] = None


# ----- Read schema (response) -----
class Room(RoomBase):
    id: int
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
