from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class Movie:
    title: str
    original_title: Optional[str] = None
    year: int = 0
    runtime: Optional[int] = None           # minutes
    genres: List[str] = field(default_factory=list)
    director: Optional[str] = None
    writers: List[str] = field(default_factory=list)
    main_cast: List[str] = field(default_factory=list)
    production_companies: List[str] = field(default_factory=list)
    country: Optional[str] = None
    language: Optional[str] = None
    budget: Optional[int] = None
    revenue: Optional[int] = None

    imdb_rating: Optional[float] = None
    imdb_votes: Optional[int] = None
    tmdb_rating: Optional[float] = None
    rotten_critics: Optional[float] = None
    rotten_audience: Optional[float] = None
    metacritic: Optional[float] = None
    num_reviews: Optional[int] = None     
    award_wins: int = 0
    award_nominations: int = 0
    plot: Optional[str] = None
    poster_url: Optional[str] = None
    trailer_url: Optional[str] = None
    source_urls: List[str] = field(default_factory=list)
    final_score: float = 0.0
    critic_consensus: float = 0.0
    audience_consensus: float = 0.0
    popularity_score: float = 0.0
    cultural_impact_score: float = 0.0