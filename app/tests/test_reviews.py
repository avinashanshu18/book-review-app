from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# === Helper to create a book first ===
def create_test_book(title="Sample", author="Tester"):
    res = client.post("/books/", json={"title": title, "author": author})
    assert res.status_code == 201
    return res.json()["id"]

# === Helper to create a review ===
def create_test_review(book_id, content="Great!", rating=5):
    res = client.post(f"/books/{book_id}/reviews", json={"content": content, "rating": rating, "book_id": book_id})
    assert res.status_code == 201
    return res.json()


# ========== Test: Create Review ==========
def test_create_review():
    book_id = create_test_book()
    review = create_test_review(book_id)
    assert review["content"] == "Great!"
    assert review["rating"] == 5
    assert review["book_id"] == book_id

# ========== Test: Create Review for Non-Existent Book ==========
def test_create_review_invalid_book():
    res = client.post("/books/999999/reviews", json={"content": "Invalid", "rating": 3, "book_id": 999999})
    assert res.status_code == 404
    assert res.json()["detail"] == "Book not found"

# ========== Test: List Reviews ==========
def test_list_reviews():
    book_id = create_test_book("ReviewBook", "RevAuthor")
    create_test_review(book_id, content="Review 1", rating=4)
    create_test_review(book_id, content="Review 2", rating=5)
    
    res = client.get(f"/books/{book_id}/reviews")
    assert res.status_code == 200
    data = res.json()
    assert "total" in data
    assert len(data["reviews"]) >= 2

# ========== Test: Update Review ==========
def test_update_review():
    book_id = create_test_book("UpdateBook", "AuthorX")
    review = create_test_review(book_id, "Initial", 3)

    update_payload = {"content": "Updated content", "rating": 4}
    res = client.put(f"/reviews/{review['id']}", json=update_payload)
    assert res.status_code == 200
    updated = res.json()
    assert updated["content"] == "Updated content"
    assert updated["rating"] == 4

# ========== Test: Delete Review ==========
def test_delete_review():
    book_id = create_test_book("DeleteBook", "AuthorY")
    review = create_test_review(book_id)

    res = client.delete(f"/reviews/{review['id']}")
    assert res.status_code == 204  # No content

    # Verify it’s gone
    res = client.put(f"/reviews/{review['id']}", json={"content": "try", "rating": 2})
    assert res.status_code == 404

# ========== Test: Update Non-existent Review ==========
def test_update_nonexistent_review():
    res = client.put("/reviews/999999", json={"content": "Nowhere", "rating": 2})
    assert res.status_code == 404
    assert res.json()["detail"] == "Review not found"
