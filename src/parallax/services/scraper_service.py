from parallax.interfaces.enter import IWebScraper, IScraperUseCase
from parallax.models import Headline
from typing import List

class ScraperService(IScraperUseCase):
    def __init__(self, scraper: IWebScraper):
        self.scraper = scraper

    def execute(self, query: str) -> List[Headline]:
        return self.scraper.run_all(query)