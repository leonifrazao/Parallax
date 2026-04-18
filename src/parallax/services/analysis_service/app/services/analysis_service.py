from parallax.interfaces.enter import IAnalysisUseCase, INarrativeAnalysis
from parallax.models.enter import Narrative, Headline
from typing import List
from loguru import logger
import asyncio
import time


class AnalysisService(IAnalysisUseCase):
    def __init__(self, narrative_analysis: INarrativeAnalysis):
        self.narrative_analysis = narrative_analysis

    def chunk(self, lst: List[Headline], size: int):
        for i in range(0, len(lst), size):
            yield lst[i:i + size]

    async def execute(self, headlines: List[Headline]) -> List[Narrative]:
        analysis_start = time.time()

        try:
            batches = list(self.chunk(headlines, 3))

            results = await asyncio.gather(
                *[self.narrative_analysis.analyze_narratives(batch) for batch in batches]
            )

            flattened = [
                narrative
                for batch_result in results
                for narrative in batch_result
            ]

            logger.info("Analysis took {}ms", int((time.time() - analysis_start) * 1000))
            return flattened

        except Exception:
            logger.exception("Analysis failed")
            raise