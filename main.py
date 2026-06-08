import asyncio
import sys
import logging
import aiohttp
import config
from scraper.imdb import IMDBScraper
from scraper.tmdb import TMDBScraper
from scraper.omdb import OMDbScraper
from scraper.rotten_tomatoes import RottenTomatoesScraper
from scraper.metacritic import MetacriticScraper
from scraper.wikipedia import WikipediaAwardsScraper
from ranking_engine import RankingEngine
from exporters.txt_exporter import TXTExporter
from exporters.csv_exporter import CSVExporter
from exporters.json_exporter import JSONExporter
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
async def collect_movies(year, session):
    movies = []
    omdb = None
    jobs = []
    if "imdb" in config.ACTIVE_SOURCES:
        jobs.append(IMDBScraper(session, config.__dict__).fetch_movies(year))
    if "tmdb" in config.ACTIVE_SOURCES:
        jobs.append(TMDBScraper(session, config.__dict__).fetch_movies(year))
    if "rotten_tomatoes" in config.ACTIVE_SOURCES:
        jobs.append(
            RottenTomatoesScraper(
                session,
                config.__dict__
            ).fetch_movies(year)
        )
    if "metacritic" in config.ACTIVE_SOURCES:
        jobs.append(
            MetacriticScraper(
                session,
                config.__dict__
            ).fetch_movies(year)
        )
    if "wikipedia" in config.ACTIVE_SOURCES:
        jobs.append(
            WikipediaAwardsScraper(
                session,
                config.__dict__
            ).fetch_movies(year)
        )
    if "omdb" in config.ACTIVE_SOURCES:
        omdb = OMDbScraper(session, config.__dict__)
    results = await asyncio.gather(*jobs, return_exceptions=True)
    for result in results:
        if isinstance(result, Exception):
            logger.error(result)
            continue
        movies.extend(result)
    return movies, omdb
async def main():
    config.CACHE_DIR.mkdir(exist_ok=True)
    config.DATASET_DIR.mkdir(exist_ok=True)
    try:
        year = int(
            sys.argv[1]
            if len(sys.argv) > 1
            else input("Year: ")
        )
    except ValueError:
        print("Invalid year")
        return
    logger.info(f"Fetching movie data for {year}")
    connector = aiohttp.TCPConnector(
        limit=config.CONCURRENT_REQUESTS
    )
    async with aiohttp.ClientSession(
        connector=connector
    ) as session:
        movies, omdb = await collect_movies(year, session)
        logger.info(f"Collected {len(movies)} records")
        engine = RankingEngine()
        movies = engine.merge_movies(movies)
        if omdb:
            logger.info("Fetching missing OMDb details")
            for movie in movies:
                if movie.director and movie.plot:
                    continue
                try:
                    details = await omdb.enrich(
                        movie.title,
                        movie.year
                    )
                    if details:
                        engine._merge_into(movie, details)
                except Exception as e:
                    logger.warning(
                        f"OMDb lookup failed for {movie.title}: {e}"
                    )
        ranked = engine.compute_scores(movies)
        TXTExporter(config.DATASET_DIR).export(year, ranked)
        CSVExporter(config.DATASET_DIR).export(year, ranked)
        JSONExporter(config.DATASET_DIR).export(year, ranked)
        print("\nTop Movies\n")
        for idx, movie in enumerate(ranked[:10], start=1):
            print(
                f"{idx}. {movie.title} "
                f"({movie.final_score:.2f})"
            )
        logger.info("Finished")
        
if __name__ == "__main__":
    asyncio.run(main())