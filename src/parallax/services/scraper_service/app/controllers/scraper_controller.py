from fastapi import APIRouter
from loguru import logger
from parallax.interfaces.enter import IScraperUseCase
from parallax.models.enter.web import ScrapeRequest


class ScraperController:
    def __init__(self, scraper_service: IScraperUseCase):
        self.router = APIRouter()
        self.scraper_service = scraper_service
        self.router.add_api_route("/scrape", self.scrape, methods=["POST"])

    async def scrape(self, request: ScrapeRequest):
        logger.info("Scraping headlines for query={} sources={}", request.query, request.sources)
        return await self.scraper_service.execute(request.query, request.sources)