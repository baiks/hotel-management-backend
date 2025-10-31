from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class Items(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    price = Column(Integer, index=True)
    is_offer = Column(Boolean, index=True)
