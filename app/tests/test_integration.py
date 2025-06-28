from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_books_cache_miss(monkeypatch):
    # Simulate cache miss by patching the cache getter to return None
    monkeypatch.setattr("app.utils.cache.get_cached_books", lambda: None)

    # Hit the /books endpoint, which should query the DB instead of Redis
    res = client.get("/books/")
    assert res.status_code == 200
    data = res.json()
    
    # Ensure we got a list even if empty
    assert "books" in data
    assert isinstance(data["books"], list)
