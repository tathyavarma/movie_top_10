
import logging
from pathlib import Path
from models.movie import Movie
from typing import List
class TXTExporter:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
    def export(self, year: int, movies: List[Movie]):
        top10 = movies[:10]
        filepath = self.output_dir / f"Top10_{year}.txt"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# Top 10 Movies of {year}\n\n")
            for i, m in enumerate(top10, 1):
                f.write(f"{i}. {m.title} ({m.year})\n")
                f.write(f"   Final Score: {m.final_score:.1f}\n")
                f.write(f"   IMDb: {m.imdb_rating/10:.1f}/10 | TMDb: {m.tmdb_rating/10:.1f}/10 | Meta: {m.metacritic}\n")
                f.write(f"   Critics Consensus: {m.critic_consensus:.1f} | Audience: {m.audience_consensus:.1f}\n")
                f.write(f"   Awards: {m.award_wins} wins, {m.award_nominations} noms\n")
                if m.plot:
                    f.write(f"   Plot: {m.plot[:200]}...\n")
                f.write("-" * 80 + "\n\n")
        logging.info(f"TXT report saved to {filepath}")