
from .base import BaseScraper
from interfaces import IWebScraper
from loguru import logger

class WebScraper(BaseScraper, IWebScraper):
    def __init__(self):
        super().__init__()
        logger.info("WebScraper initialized")

    def scrape_aljazeera(self):
        logger.info("Scraping Al Jazeera")
        return self.get_news_headlines([{
            'link': 'https://www.aljazeera.com/tag/sudan-war/',
            'selector': '.article-card__title',
            'source': 'Al Jazeera'
        }])

    def scrape_bbc(self):
        logger.info("Scraping BBC")
        return self.get_news_headlines([{  
            'link': 'https://www.bbc.com/news/topics/cq23pdgvgm8t',
            'selector': '[data-testid="card-headline"]',
            'source': 'BBC'
        }])

    def run_all(self):
        """Collects everything and returns a single list for the AI engine."""
        logger.info("Starting scraping...")
        
        # The Botasaurus already manages threads, so we call it directly
        aj_data = self.scrape_aljazeera()
        bbc_data = self.scrape_bbc()

        if aj_data and bbc_data:
            logger.info("Scraping completed successfully")
        else:
            logger.error("Scraping failed")
        
        # Sum the lists (Python)
        return aj_data + bbc_data