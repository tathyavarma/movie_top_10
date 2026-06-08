import pandas as pd
from pathlib import Path
from models.movie import Movie
from typing import List
class CSVExporter:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
    def export(self, year: int, movies: List[Movie]):
        df = pd.DataFrame([{
            "Title": m.title,
            "Year": m.year,
            "Final Score": m.final_score,
            "IMDb Rating": m.imdb_rating,
            "TMDb Rating": m.tmdb_rating,
            "Rotten Critics": m.rotten_critics,
            "Metacritic": m.metacritic,
            "Awards Wins": m.award_wins,
            "Awards Noms": m.award_nominations,
            "Popularity": m.popularity_score,
            "Critic Consensus": m.critic_consensus,
            "Audience Consensus": m.audience_consensus,
            "Genres": ", ".join(m.genres),
            "Director": m.director,
            "Plot": m.plot,
        } for m in movies])
        df.to_csv(self.output_dir / f"movies_{year}.csv", index=False)
        logging.info(f"CSV dataset saved.")