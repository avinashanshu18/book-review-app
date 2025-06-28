from fastapi import FastAPI
from app.api import book_reviews  # combined router module
from app.db.database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize the FastAPI app
app = FastAPI(
    title="Book Review API",
    version="1.0.0",
    description="A simple API to manage books and their reviews."
)

# Register routers
app.include_router(book_reviews.router)
