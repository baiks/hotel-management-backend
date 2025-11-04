from fastapi import FastAPI
from routers import users_router, rooms_router, booking_router
from database import engine, Base

# uvicorn main:app --reload
# https://fastapi.tiangolo.com/features/#validation

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Hotel Management System",  # Set the title of the Swagger UI
    description="This is a Hotel Management System.",  # Set the description
    version="1.0.0",  # Set the version
    docs_url="/api/docs",  # Optional: Change the URL for the Swagger documentation
    redoc_url="/api/redoc"  # Optional: Change the URL for Redoc documentation
)
app.include_router(users_router.router)
app.include_router(rooms_router.router)
app.include_router(booking_router.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Hotel Management API!"}
