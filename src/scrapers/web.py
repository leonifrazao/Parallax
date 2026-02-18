
from .base import BaseScraper
from interfaces import IWebScraper

class WebScraper(BaseScraper, IWebScraper):
    def __init__(self):
        super().__init__()

    def scrape_aljazeera(self):
        return self.get_news_headlines([{
            'link': 'https://www.aljazeera.com/tag/sudan-war/',
            'selector': '.article-card__title',
            'source': 'Al Jazeera'
        }])

    def scrape_bbc(self):
        return self.get_news_headlines([{  
            'link': 'https://www.bbc.com/news/topics/cq23pdgvgm8t',
            'selector': '[data-testid="card-headline"]',
            'source': 'BBC'
        }])

    def run_all(self):
        """Collects everything and returns a single list for the AI engine."""
        print("[OBSERVER] Starting scraping...")
        
        # The Botasaurus already manages threads, so we call it directly
        aj_data = self.scrape_aljazeera()
        bbc_data = self.scrape_bbc()
        
        # Sum the lists (Python)
        return aj_data + bbc_data