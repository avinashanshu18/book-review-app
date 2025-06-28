from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# ====================== BOOK SCHEMAS ======================

class BookBase(BaseModel):
    title: str = Field(..., example="Clean Code")
    author: str = Field(..., example="Robert C. Martin")

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, example="Clean Architecture")
    author: Optional[str] = Field(None, example="Uncle Bob")

class BookOut(BookBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class BookList(BaseModel):
    total: int
    books: List[BookOut]

# ====================== REVIEW SCHEMAS ======================

class ReviewBase(BaseModel):
    content: str = Field(..., example="Great book on software practices.")
    rating: int = Field(..., ge=1, le=5, example=5)

class ReviewCreate(ReviewBase):
    book_id: int = Field(..., example=1)

class ReviewUpdate(BaseModel):
    content: Optional[str] = Field(None, example="Updated review text.")
    rating: Optional[int] = Field(None, ge=1, le=5)

class ReviewOut(ReviewBase):
    id: int
    book_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class ReviewList(BaseModel):
    total: int
    reviews: List[ReviewOut]

# ====================== NESTED SCHEMAS ======================

class BookWithReviews(BookOut):
    reviews: List[ReviewOut] = []

class ReviewWithBook(ReviewOut):
    book: BookOut
