from parallax.interfaces.enter.usecases import IExecutorUseCase
from parallax.models.enter import Narrative
from parallax.helpers import ModelToFile, HeadlineDeduplicator
from loguru import logger
import time


class ExecutorService(IExecutorUseCase):
    def __init__(self, scraper, analyzer, renderer):
        self.scraper = scraper
        self.analyzer = analyzer
        self.renderer = renderer

    async def execute(
        self,
        query: str,
        limit: int = 10,
        tojson: bool = False,
    ) -> list[Narrative]:
        pipeline_start = time.time()

        news = await self.scraper.execute(query)
        if not news:
            raise ValueError("No news found")

        logger.info("Pipeline fetched headlines | count={}", len(news))

        deduped = HeadlineDeduplicator.deduplicate(news)
        logger.info(
            "Pipeline deduplicated headlines | before={} after={}",
            len(news),
            len(deduped),
        )

        selected = deduped[:limit]
        logger.info("Pipeline selected headlines | limit={} selected={}", limit, len(selected))

        result = await self.analyzer.execute(selected)
        if not result:
            raise ValueError("No narratives found")

        if tojson:
            ModelToFile.to_json(result)
        
        await self.renderer.execute(
            title=f"Narrative Analysis - {query}",
            filename=f"{query.replace(' ', '_')}.html",
            items=result,
        )

        logger.info("Pipeline total took {}ms", int((time.time() - pipeline_start) * 1000))
        return result