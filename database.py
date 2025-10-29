# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
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


# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
