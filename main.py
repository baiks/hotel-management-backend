from fastapi import FastAPI
from routers import usersRouter, itemsRouter

# https://fastapi.tiangolo.com/features/#validation
app = FastAPI(
    title="My FastAPI Application",  # Set the title of the Swagger UI
    description="This is a sample FastAPI application with multiple controllers.",  # Set the description
    version="1.0.0",  # Set the version
    docs_url="/api/docs",  # Optional: Change the URL for the Swagger documentation
    redoc_url="/api/redoc"  # Optional: Change the URL for Redoc documentation
)
app.include_router(usersRouter.router)
app.include_router(itemsRouter.router)


@app.get("api/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}
