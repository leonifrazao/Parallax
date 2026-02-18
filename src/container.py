from dependency_injector import containers, providers
from scrapers.web import WebScraper

class Container(containers.DeclarativeContainer):
    
    web_scraper = providers.Factory(WebScraper)