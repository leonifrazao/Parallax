from parallax.interfaces.enter import IAnalysisUseCase
import fastapi
from parallax.models.enter import Headline, Narrative
from fastapi import HTTPException
from loguru import logger

class AnalysisController:
    def __init__(self, analysis_service: IAnalysisUseCase):
        self.router = fastapi.APIRouter()
        self.analysis_service = analysis_service

        self.router.add_api_route("/analyze", self.analyze, methods=["POST"], response_model=list[Narrative])
    
    async def analyze(self, headlines: list[Headline]):
        logger.info("Analyzing headlines with ids: {}", [h.id for h in headlines])
        try:
            return await self.analysis_service.execute(headlines)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Analysis failed: {str(e)}"
            )