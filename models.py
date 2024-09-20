from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import urllib.parse

# Load environment variables from .env file
load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = urllib.parse.quote(os.getenv("DB_PASSWORD"))
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Replace with your MySQL database URL
# DATABASE_URL = "mysql+pymysql://root:Baiks@123@localhost/fastapi"

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print("Database Connection: ", DATABASE_URL)

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Items(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    price = Column(Integer, index=True)
    is_offer = Column(Boolean, index=True)


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), index=True)
    last_name = Column(String(255), index=True)
    username = Column(String(255), index=True)
    password = Column(String(255), index=True)


Base.metadata.create_all(bind=engine)
