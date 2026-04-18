from parallax.interfaces.enter import IWebScraper, IScraperUseCase
from parallax.models.enter import Headline
from typing import List
import time
from loguru import logger

class ScraperService(IScraperUseCase):
    def __init__(self, scraper: IWebScraper):
        self.scraper = scraper

    def execute(self, query: str) -> List[Headline]:
        start_time = time.time()
        result = self.scraper.run_all(query)
        end_time = time.time()
        logger.info("Scraping took {}ms", int((end_time - start_time) * 1000))
        return result