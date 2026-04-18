import fastapi
from parallax.interfaces.enter import IScraperUseCase
from parallax.models.enter import ScrapeRequest, Headline
from fastapi import HTTPException
from loguru import logger

class ScraperController:
    def __init__(self, scraper_service: IScraperUseCase):
        self.router = fastapi.APIRouter()
        self.scraper_service = scraper_service
        self.router.add_api_route("/scrape", self.scrape, methods=["POST"], response_model=list[Headline])
    
    def scrape(self, request: ScrapeRequest):
        logger.info("Scraping headlines for query: {}", request.query)
        return self.scraper_service.execute(request.query)