from parallax.interfaces.enter import IWebScraper, IScraperUseCase
from parallax.models.enter import Headline
from loguru import logger
import time


class ScraperService(IScraperUseCase):
    def __init__(self, scraper: IWebScraper):
        self.scraper = scraper

    async def execute(self, query: str, sources: list[str] | None = None) -> list[Headline]:
        start = time.time()
        result = self.scraper.run_all(query, sources or [])
        logger.info("Scraping took {}ms", int((time.time() - start) * 1000))
        return result