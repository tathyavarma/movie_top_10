from scraper.base import BaseScraper

class MetacriticScraper(BaseScraper):
    async def fetch_movies(self, year: int) -> List[Movie]:
        self.logger.warning("Metacritic scraping not yet implemented. Falling back.")
        return []