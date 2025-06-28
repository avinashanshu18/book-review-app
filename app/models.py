from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float, Boolean, func
from app.db.database import Base


# class Book(Base):
#     __tablename__ = "books"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(255), nullable=False)
#     author = Column(String(255), nullable=False)
#     description = Column(Text, nullable=True)
#     genre = Column(String(100), nullable=True)
#     published_year = Column(Integer, nullable=True)
#     isbn = Column(String(13), unique=True, nullable=True)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# class Review(Base):
#     __tablename__ = "reviews"

#     id = Column(Integer, primary_key=True)
#     book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"))
#     reviewer_name = Column(String(100), nullable=True)
#     rating = Column(Float, nullable=False)
#     comment = Column(Text, nullable=True)
#     is_verified = Column(Boolean, default=False)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     updated_at = Column(DateTime(timezone=True), onupdate=func.now())



from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float, Boolean, func
from app.db.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    genre = Column(String(100), nullable=True)
    published_year = Column(Integer, nullable=True)
    isbn = Column(String(13), unique=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), index=True)  # ✅ Indexed for performance
    reviewer_name = Column(String(100), nullable=True)
    rating = Column(Float, nullable=False)
    comment = Column(Text, nullable=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
