import re
from typing import List
from bs4 import BeautifulSoup
from models.movie import Movie
from scraper.base import BaseScraper
class IMDBScraper(BaseScraper):
    BASE_URL = "https://www.imdb.com/search/title"
    async def fetch_movies(self, year: int) -> List[Movie]:
        params = {
            "release_date": f"{year},{year}",
            "title_type": "feature",
            "sort": "num_votes,desc",
            "count": 100,
        }
        query = "&".join(f"{k}={v}" for k, v in params.items())
        url = f"{self.BASE_URL}?{query}"

        html = await self._get(url)

        if not html:
            return []
        soup = BeautifulSoup(html, "lxml")
        movies = []
        for item in soup.select(".lister-item"):
            try:
                title_elem = item.select_one(
                    ".lister-item-header a"
                )
                if not title_elem:
                    continue
                title = title_elem.text.strip()
                year_elem = item.select_one(
                    ".lister-item-year"
                )
                year_text = (
                    year_elem.text if year_elem else ""
                )
                match = re.search(r"\d{4}", year_text)
                movie_year = (
                    int(match.group()) if match else year
                )
                rating_elem = item.select_one(
                    ".ratings-imdb-rating strong"
                )
                rating = (
                    float(rating_elem.text)
                    if rating_elem
                    else None
                )
                votes_elem = item.select_one(
                    ".sort-num_votes-visible span:nth-of-type(2)"
                )
                votes = (
                    int(votes_elem.text.replace(",", ""))
                    if votes_elem and votes_elem.text
                    else None
                )
                genre_elem = item.select_one(".genre")
                genres = (
                    [
                        genre.strip()
                        for genre in genre_elem.text.split(",")
                    ]
                    if genre_elem
                    else []
                )
                desc_elem = item.select_one(
                    ".text-muted + p.text-muted"
                )
                plot = (
                    desc_elem.text.strip()
                    if desc_elem
                    else None
                )
                movie = Movie(
                    title=title,
                    year=movie_year,
                    genres=genres,
                    plot=plot,
                    imdb_rating=(
                        rating * 10 if rating else None
                    ),
                    imdb_votes=votes,
                    source_urls=[
                        f"https://www.imdb.com{title_elem['href']}"
                    ],
                )
                movies.append(movie)

            except Exception as e:
                self.logger.debug(
                    f"IMDb parse error: {e}"
                )

        self.logger.info(
            f"IMDb: fetched {len(movies)} candidates for {year}"
        )
        return movies