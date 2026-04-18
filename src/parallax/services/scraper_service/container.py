import os
from dependency_injector import containers, providers

from parallax.scrapers.web import WebScraper
from parallax.scrapers.websites.newsapi import NewsAPIScraper
from parallax.services.scraper_service.app.services import ScraperService


class ScraperContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    newsapi_scraper = providers.Factory(
        NewsAPIScraper,
        api_key=os.getenv("NEWSAPI_KEY"),
    )

    web_scraper = providers.Factory(
        WebScraper,
        scrappers=providers.List(newsapi_scraper),
    )

    scraper_service = providers.Factory(
        ScraperService,
        scraper=web_scraper,
    )