from scraper.base import BaseScraper

class RottenTomatoesScraper(BaseScraper):
    async def fetch_movies(self, year: int) -> List[Movie]:
        self.logger.warning("Rotten Tomatoes scraping is not yet implemented. Falling back.")
        return []