import os
from pathlib import Path
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "your_tmdb_api_key_here")
OMDB_API_KEY = os.getenv("OMDB_API_KEY", "your_omdb_api_key_here")
BASE_DIR = Path(__file__).resolve().parent
CACHE_DIR = BASE_DIR / "cache"
DATASET_DIR = BASE_DIR / "datasets"
LOG_DIR = BASE_DIR / "logs"
REQUEST_TIMEOUT = 15
RETRY_ATTEMPTS = 3
RETRY_BACKOFF = 2
CONCURRENT_REQUESTS = 10
RATE_LIMIT_DELAY = 1.0

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}
ACTIVE_SOURCES = [
    "imdb",
    "tmdb",
    "omdb",
    "rotten_tomatoes",
    "metacritic",
    "wikipedia",
]
ALLOWED_TITLE_TYPES = {"movie", "film"}
RANKING_WEIGHTS = {
    "imdb_rating": 0.30,
    "rotten_critics": 0.25,
    "metacritic": 0.15,
    "tmdb_rating": 0.10,
    "awards": 0.10,
    "popularity": 0.05,
    "review_volume": 0.05,
}

FUZZY_MATCH_THRESHOLD = 85