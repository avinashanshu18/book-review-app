# import redis
# import json
# from typing import Optional, List
# from app.schemas import BookOut

# # Initialize Redis connection
# r = redis.Redis(host="localhost", port=6379, decode_responses=True)

# # Default TTL (in seconds) for book list cache
# CACHE_TTL_SECONDS = 3600


# def get_cached_books() -> Optional[List[BookOut]]:
#     try:
#         cached = r.get("books")
#         if cached:
#             books_data = json.loads(cached)
#             return [BookOut(**book) for book in books_data]
#         return None
#     except redis.RedisError as e:
#         # Optionally log the error
#         print(f"[Redis] Error fetching cached books: {e}")
#         return None


# def set_cached_books(books: List[BookOut], ttl: int = CACHE_TTL_SECONDS) -> None:
#     try:
#         books_serialized = [book.dict() for book in books]
#         r.set("books", json.dumps(books_serialized), ex=ttl)
#     except redis.RedisError as e:
#         # Optionally log the error
#         print(f"[Redis] Error setting cached books: {e}")



import redis
import json
import logging
from typing import Optional, List
from app.schemas import BookOut

logger = logging.getLogger(__name__)

# Initialize Redis connection
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

BOOKS_CACHE_KEY = "books"
CACHE_TTL_SECONDS = 3600

def get_cached_books() -> Optional[List[BookOut]]:
    try:
        cached = r.get(BOOKS_CACHE_KEY)
        if cached:
            books_data = json.loads(cached)
            return [BookOut(**book) for book in books_data]
    except redis.RedisError as e:
        logger.warning("[Redis] Error fetching cached books: %s", e)
    return None

def set_cached_books(books: List[BookOut], ttl: int = CACHE_TTL_SECONDS) -> None:
    try:
        books_serialized = [book.dict() for book in books]
        r.set(BOOKS_CACHE_KEY, json.dumps(books_serialized), ex=ttl)
    except redis.RedisError as e:
        logger.warning("[Redis] Error setting cached books: %s", e)
