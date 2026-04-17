from dependency_injector import containers, providers
from parallax.scrapers.web import WebScraper
from parallax.analysis.engine import NarrativeAnalysis

class Container(containers.DeclarativeContainer):
    
    wiring_config = containers.WiringConfiguration(modules=["parallax.main"])

    web_scraper = providers.Factory(WebScraper)
    narrative_analysis = providers.Factory(NarrativeAnalysis)