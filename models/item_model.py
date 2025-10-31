# from typing import Union
from pydantic import BaseModel


class ItemCreate(BaseModel):
    name: str
    price: float
    is_offer: bool


class ItemUpdate(BaseModel):
    name: str
    price: float
