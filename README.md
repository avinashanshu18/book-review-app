# 📚 Book Review API

A full-featured backend service for managing books and reviews, built with **FastAPI**, **SQLAlchemy**, **Alembic**, **SQLite**, and **Redis**.

---

## 🗂️ Project Structure

```
book-review-app/
├── alembic.ini                   # Alembic configuration
├── requirements.txt              # Project dependencies
├── README.md                     # This file
├── alembic/                      # Migration scripts
│   ├── env.py
│   └── versions/
├── app/
│   ├── api/
│   │   └── book_reviews.py       # Combined routes
│   ├── db/
│   │   ├── database.py           # SQLAlchemy DB engine
│   │   └── redis.py              # Redis utility functions
│   ├── main.py                   # FastAPI app entrypoint
│   ├── models.py                 # Book + Review SQLAlchemy models
│   ├── schemas.py                # Pydantic schemas
│   └── tests/                    # Unit + integration tests
│       ├── test_books.py
│       ├── test_reviews.py
│       └── test_integration.py
└── venv/                         # (Virtualenv folder, excluded from Git)
```

---

## 🚀 Features

✅ Add and list books  
✅ Add and list reviews  
✅ Redis caching for `/books` with fallback  
✅ Alembic DB migrations with review index  
✅ Swagger & ReDoc interactive docs  
✅ Pytest test coverage for key flows  

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/book-review-app.git
cd book-review-app
```

---

### 2. Create a Virtual Environment & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

### 3. Run Alembic Migrations

```bash
alembic upgrade head
```

If you later modify models:

```bash
alembic revision --autogenerate -m "your message here"
alembic upgrade head
```

---

### 4. Start Redis Server

#### On macOS:

```bash
brew install redis
brew services start redis
```

#### On Ubuntu/Linux:

```bash
sudo apt install redis-server
sudo systemctl start redis
```

---

### 5. Run the FastAPI App

```bash
uvicorn app.main:app --reload
```

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc Docs: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧪 Run Tests

```bash
pytest app/tests/
```

Includes:
- ✅ `test_books.py`: Book creation
- ✅ `test_reviews.py`: Review creation
- ✅ `test_integration.py`: Cache miss fallback

---

## 🔌 API Endpoints

| Method | Endpoint                   | Description                     |
|--------|----------------------------|---------------------------------|
| GET    | `/books`                   | List all books (cache-first)    |
| POST   | `/books`                   | Add a new book                  |
| GET    | `/books/{id}/reviews`      | Get reviews for a book          |
| POST   | `/books/{id}/reviews`      | Submit a review for a book      |

---

## 🧱 Models

```python
# app/models.py

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
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), index=True)
    reviewer_name = Column(String(100), nullable=True)
    rating = Column(Float, nullable=False)
    comment = Column(Text, nullable=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

---

## ⚙️ Redis Caching Logic

```python
# app/db/redis.py

def get_cached_books() -> Optional[List[BookOut]]:
    try:
        cached = r.get("books")
        if cached:
            books_data = json.loads(cached)
            return [BookOut(**book) for book in books_data]
    except redis.RedisError:
        print("⚠️ Redis unavailable — falling back to DB.")
    return None

def set_cached_books(books: List[BookOut], ttl: int = 3600) -> None:
    try:
        books_serialized = [book.dict() for book in books]
        r.set("books", json.dumps(books_serialized), ex=ttl)
    except redis.RedisError as e:
        print(f"[Redis] Error setting cached books: {e}")
```

---

## 🗃️ Alembic Migrations

**Alembic Config:** `alembic.ini`  
**Script Folder:** `alembic/`  
**Main command to run migrations:**

```bash
alembic upgrade head
```

Auto-generate after schema/model changes:

```bash
alembic revision --autogenerate -m "add index or column"
alembic upgrade head
```

---

## 🎯 Deliverables Checklist

| Requirement                     | Status        |
|--------------------------------|---------------|
| API with FastAPI               | ✅ Done        |
| Swagger/OpenAPI Docs           | ✅ Built-in    |
| Redis Caching                  | ✅ Implemented |
| Alembic + Migration Index      | ✅ Complete    |
| Unit + Integration Tests       | ✅ Complete    |
| README with all instructions   | ✅ This file   |

---

## 📩 Author

**Avinash Anshu**  
GitHub: [github.com/avinashanshu18](https://github.com/avinashanshu18)

<!-- pair touch -->
