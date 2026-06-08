from scraper.base import BaseScraper
from models.movie import Movie

class WikipediaAwardsScraper(BaseScraper):
    async def fetch_movies(self, year: int) -> List[Movie]:
        self.logger.warning("Wikipedia awards scraping not yet implemented.")
        return []