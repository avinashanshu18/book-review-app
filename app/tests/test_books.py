from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# ========== Test: Create Book ==========
def test_create_book():
    payload = {"title": "Test Book", "author": "Test Author"}
    res = client.post("/books/", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == payload["title"]
    assert data["author"] == payload["author"]
    assert "id" in data

# ========== Test: Create Book (Missing Field) ==========
def test_create_book_missing_title():
    payload = {"author": "No Title Author"}
    res = client.post("/books/", json=payload)
    assert res.status_code == 422  # Unprocessable Entity (validation error)

# ========== Test: Get Book by ID ==========
def test_get_book():
    # Create first
    create_res = client.post("/books/", json={"title": "Fetch Me", "author": "Fetcher"})
    book_id = create_res.json()["id"]

    # Fetch
    res = client.get(f"/books/{book_id}")
    assert res.status_code == 200
    assert res.json()["title"] == "Fetch Me"

# ========== Test: List Books ==========
def test_list_books():
    res = client.get("/books/")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data["books"], list)
    assert "total" in data

# ========== Test: Get Non-Existent Book ==========
def test_get_nonexistent_book():
    res = client.get("/books/999999")  # assuming this ID doesn't exist
    assert res.status_code == 404
    assert res.json()["detail"] == "Book not found"

# ========== (Optional) Teardown / Cleanup ==========
# You can add fixtures with setup/teardown using pytest later to reset the DB
