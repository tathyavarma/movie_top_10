from typing import List
from models.movie import Movie
from scraper.base import BaseScraper

class TMDBScraper(BaseScraper):
    BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self, session, config):
        super().__init__(session, config)
        self.api_key = config["TMDB_API_KEY"]

    async def fetch_movies(self, year: int) -> List[Movie]:
        url = f"{self.BASE_URL}/discover/movie"

        params = {
            "api_key": self.api_key,
            "primary_release_year": year,
            "sort_by": "vote_average.desc",
            "vote_count.gte": 100,
            "page": 1,
        }

        data = await self._get_json(
            url,
            params=params
        )

        if not data or "results" not in data:
            self.logger.error(
                "TMDb API returned no results."
            )
            return []

        movies = []

        for item in data["results"]:

            if (
                item.get("media_type")
                and item["media_type"] != "movie"
            ):
                continue

            movies.append(
                Movie(
                    title=item["title"],
                    original_title=item.get(
                        "original_title"
                    ),
                    year=year,
                    genres=item.get("genre_ids", []),
                    plot=item.get("overview"),
                    poster_url=(
                        "https://image.tmdb.org/t/p/w500"
                        f"{item['poster_path']}"
                        if item.get("poster_path")
                        else None
                    ),
                    tmdb_rating=(
                        item["vote_average"] * 10
                    ),
                    source_urls=[
                        (
                            "https://www.themoviedb.org/movie/"
                            f"{item['id']}"
                        )
                    ],
                )
            )

        self.logger.info(
            f"TMDb: fetched {len(movies)} candidates for {year}"
        )

        return movies