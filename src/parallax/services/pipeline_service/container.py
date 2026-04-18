import os
from dependency_injector import containers, providers

from parallax.services.pipeline_service.app.clients.scraper_client import ScraperClient
from parallax.services.pipeline_service.app.clients.analysis_client import AnalysisClient
from parallax.services.pipeline_service.app.services.executor_service import ExecutorService


class PipelineContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    scraper_client = providers.Singleton(
        ScraperClient,
        base_url=os.getenv("SCRAPER_SERVICE_URL", "http://scraper-service:8000"),
    )

    analysis_client = providers.Singleton(
        AnalysisClient,
        base_url=os.getenv("ANALYSIS_SERVICE_URL", "http://analysis-service:8000"),
    )

    executor_service = providers.Factory(
        ExecutorService,
        scraper=scraper_client,
        analyzer=analysis_client,
    )