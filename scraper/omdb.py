import re
from typing import List, Optional
from models.movie import Movie
from scraper.base import BaseScraper
class OMDbScraper(BaseScraper):
    BASE_URL = "http://www.omdbapi.com/"

    def __init__(self, session, config):
        super().__init__(session, config)
        self.api_key = config["OMDB_API_KEY"]

    async def fetch_movies(self, year: int) -> List[Movie]:
        return []

    async def enrich(
        self,
        title: str,
        year: int
    ) -> Optional[Movie]:

        params = {
            "apikey": self.api_key,
            "t": title,
            "y": year,
            "plot": "full",
        }

        data = await self._get_json(
            self.BASE_URL,
            params=params
        )

        if (
            not data
            or data.get("Response") == "False"
        ):
            return None

        runtime = self._parse_runtime(
            data.get("Runtime")
        )

        genres = (
            data.get("Genre", "").split(", ")
            if data.get("Genre")
            else []
        )

        writers = (
            data.get("Writer", "").split(", ")
            if data.get("Writer")
            else []
        )

        actors = (
            data.get("Actors", "").split(", ")
            if data.get("Actors")
            else []
        )

        awards = data.get("Awards", "")

        wins = self._extract_number(
            awards,
            r"(\d+)\s+win"
        )

        nominations = self._extract_number(
            awards,
            r"(\d+)\s+nomination"
        )

        imdb_rating = (
            float(data["imdbRating"]) * 10
            if data.get("imdbRating") != "N/A"
            else None
        )

        imdb_votes = (
            int(data["imdbVotes"].replace(",", ""))
            if data.get("imdbVotes") != "N/A"
            else None
        )

        metascore = (
            float(data["Metascore"])
            if data.get("Metascore") != "N/A"
            else None
        )

        return Movie(
            title=data["Title"],
            year=year,
            runtime=runtime,
            genres=genres,
            director=data.get("Director"),
            writers=writers,
            main_cast=actors,
            country=data.get("Country"),
            language=data.get("Language"),
            plot=data.get("Plot"),
            poster_url=(
                data.get("Poster")
                if data.get("Poster") != "N/A"
                else None
            ),
            imdb_rating=imdb_rating,
            imdb_votes=imdb_votes,
            metacritic=metascore,
            award_wins=wins,
            award_nominations=nominations,
            source_urls=[
                (
                    "https://www.imdb.com/title/"
                    f"{data['imdbID']}/"
                )
            ],
        )

    @staticmethod
    def _parse_runtime(
        runtime: Optional[str]
    ) -> Optional[int]:

        if not runtime or runtime == "N/A":
            return None

        match = re.search(r"(\d+)", runtime)

        return int(match.group(1)) if match else None

    @staticmethod
    def _extract_number(
        text: str,
        pattern: str
    ) -> int:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        return int(match.group(1)) if match else 0