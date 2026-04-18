from fastapi import FastAPI
from parallax.services.scraper_service.container import ScraperContainer
from parallax.services.scraper_service.app.controllers.scraper_controller import ScraperController

container = ScraperContainer()

app = FastAPI(title="scraper-service", version="0.1.0")

scraper_controller = ScraperController(
    scraper_service=container.scraper_service()
)

app.include_router(scraper_controller.router)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "scraper-service",
        "version": "0.1.0"
    }