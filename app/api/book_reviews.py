from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app import models, schemas

router = APIRouter(prefix="/books", tags=["Books & Reviews"])

# ========================= BOOK ROUTES =========================

@router.post("/", response_model=schemas.BookOut, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.get("/", response_model=schemas.BookList)
def list_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db)
):
    books = db.query(models.Book).offset(skip).limit(limit).all()
    total = db.query(models.Book).count()
    return {"total": total, "books": books}


@router.get("/{book_id}", response_model=schemas.BookWithReviews)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=schemas.BookOut)
def update_book(book_id: int, book_data: schemas.BookUpdate, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    for field, value in book_data.dict(exclude_unset=True).items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return


# ========================= REVIEW ROUTES =========================

@router.post("/{book_id}/reviews", response_model=schemas.ReviewOut, status_code=status.HTTP_201_CREATED)
def create_review(book_id: int, review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db_review = models.Review(**review.dict(), book_id=book_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


@router.get("/{book_id}/reviews", response_model=schemas.ReviewList)
def list_reviews(
    book_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db)
):
    if not db.query(models.Book).filter(models.Book.id == book_id).first():
        raise HTTPException(status_code=404, detail="Book not found")
    
    reviews = (
        db.query(models.Review)
        .filter(models.Review.book_id == book_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    total = db.query(models.Review).filter(models.Review.book_id == book_id).count()
    return {"total": total, "reviews": reviews}


@router.put("/reviews/{review_id}", response_model=schemas.ReviewOut)
def update_review(review_id: int, review_data: schemas.ReviewUpdate, db: Session = Depends(get_db)):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    for field, value in review_data.dict(exclude_unset=True).items():
        setattr(review, field, value)

    db.commit()
    db.refresh(review)
    return review


@router.delete("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(review)
    db.commit()
    return
