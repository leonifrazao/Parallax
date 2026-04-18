from dependency_injector import containers, providers
from parallax.scrapers.web import WebScraper
from parallax.analysis.engine import NarrativeAnalysis
from parallax.services import ExecutorService, AnalysisService, ScraperService
from parallax.ui.app import CliApp
from parallax.scrapers.websites.newsapi import NewsAPIScraper
import os

class Container(containers.DeclarativeContainer):   
    
    wiring_config = containers.WiringConfiguration(modules=["parallax.main"])

    web_scraper = providers.Factory(WebScraper, scrappers=[NewsAPIScraper(api_key=os.getenv("NEWSAPI_KEY"))])
    narrative_analysis = providers.Factory(NarrativeAnalysis)

    cli_app = providers.Factory(CliApp)

    analysis_service = providers.Factory(AnalysisService, narrative_analysis=narrative_analysis)

    scraper_service = providers.Factory(ScraperService, scraper=web_scraper)

    executor_service = providers.Factory(ExecutorService, scraper=scraper_service, analyzer=analysis_service)