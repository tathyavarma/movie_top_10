import asyncio
import json
import logging
from abc import ABC, abstractmethod
from typing import List, Optional
import aiohttp
from models.movie import Movie

class BaseScraper(ABC):
    def __init__(self, session: aiohttp.ClientSession, config: dict):
        self.session = session
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self._semaphore = asyncio.Semaphore(
            self.config["CONCURRENT_REQUESTS"]
        )
    @abstractmethod
    async def fetch_movies(self, year: int) -> List[Movie]:
        ...
    async def _get(self, url: str, **kwargs) -> Optional[str]:
        for attempt in range(self.config["RETRY_ATTEMPTS"]):
            try:
                async with self._semaphore:
                    await asyncio.sleep(
                        self.config["RATE_LIMIT_DELAY"]
                    )
                    async with self.session.get(
                        url,
                        headers=self.config["DEFAULT_HEADERS"],
                        timeout=self.config["REQUEST_TIMEOUT"],
                        **kwargs
                    ) as response:
                        if response.status == 429:
                            self.logger.warning(
                                "Rate limited, retrying..."
                            )
                            await asyncio.sleep(5)
                            continue
                        response.raise_for_status()
                        return await response.text()
            except Exception as e:
                self.logger.warning(
                    f"Attempt {attempt + 1} failed for {url}: {e}"
                )
                if attempt == self.config["RETRY_ATTEMPTS"] - 1:
                    self.logger.error(
                        f"All retries exhausted for {url}"
                    )
                    return None
                await asyncio.sleep(
                    self.config["RETRY_BACKOFF"] * (2 ** attempt)
                )
        return None
    async def _get_json(
        self,
        url: str,
        **kwargs
    ) -> Optional[dict]:

        text = await self._get(url, **kwargs)
        if not text:
            return None
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON parse error: {e}")
            return None