import json
from pathlib import Path
from models.movie import Movie
from typing import List
class JSONExporter:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
    def export(self, year: int, movies: List[Movie]):
        data = []
        for m in movies:
            data.append({
                "title": m.title,
                "year": m.year,
                "final_score": m.final_score,
                "ratings": {
                    "imdb": m.imdb_rating,
                    "tmdb": m.tmdb_rating,
                    "rotten_critics": m.rotten_critics,
                    "rotten_audience": m.rotten_audience,
                    "metacritic": m.metacritic,
                },
                "awards": {"wins": m.award_wins, "nominations": m.award_nominations},
                "metrics": {
                    "popularity": m.popularity_score,
                    "critic_consensus": m.critic_consensus,
                    "audience_consensus": m.audience_consensus,
                    "cultural_impact": m.cultural_impact_score,
                },
                "genres": m.genres,
                "director": m.director,
                "plot": m.plot,
                "sources": m.source_urls,
            })
        with open(self.output_dir / f"movies_{year}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logging.info(f"JSON dataset saved.")