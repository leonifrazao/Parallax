from parallax.interfaces.enter.usecases import IExecutorUseCase, IScraperUseCase, IAnalysisUseCase
from parallax.models import Narrative
from parallax.helpers import ModelToFile, HeadlineDeduplicator


class ExecutorService(IExecutorUseCase):
    def __init__(self, scraper: IScraperUseCase, analyzer: IAnalysisUseCase):
        self.scraper = scraper
        self.analyzer = analyzer

    async def execute(self, limit: int = 10, tojson: bool = False) -> list[Narrative]:
        all_narratives: list[Narrative] = []

        news = self.scraper.execute("israel hamas war")
        if not news:
            raise ValueError("No news found")

        deduped = HeadlineDeduplicator.deduplicate(news)

        result = await self.analyzer.execute(deduped[:limit])
        if not result:
            raise ValueError("No narratives found")
        
        all_narratives.extend(result)

        if tojson:
            ModelToFile.to_json(all_narratives)

        return all_narratives