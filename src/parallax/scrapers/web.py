
from parallax.models.enter import Headline
from typing import Iterable, List
from parallax.interfaces.enter import IWebScraper, IScraper
from loguru import logger

class WebScraper(IWebScraper):
    def __init__(self, scrappers: List[IScraper]):
        logger.info("WebScraper initialized")
        self.scrappers = scrappers

    def run_all(self, query: str, sources: list[str] | None = None) -> List[Headline]:
        """Collects everything and returns a single list for the AI engine."""
        logger.info("Starting scraping...")
        
        all_data = []
        
        for scraper in self.scrappers:
            data = scraper.scrape(query, sources)
            all_data.extend(data)

        if all_data:
            logger.info("Scraping completed successfully")
        else:
            logger.error("Scraping failed")
        
        # Sum the lists (Python)
        return all_data