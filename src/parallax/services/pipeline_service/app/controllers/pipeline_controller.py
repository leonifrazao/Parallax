from fastapi import APIRouter, HTTPException
from parallax.models.enter import Narrative
from parallax.models.enter.web import PipelineRequest
from parallax.interfaces.enter.usecases import IExecutorUseCase
import httpx
from loguru import logger


class PipelineController:
    def __init__(self, executor_service: IExecutorUseCase):
        self.router = APIRouter()
        self.executor_service = executor_service

        self.router.add_api_route(
            "/pipeline",
            self.run_pipeline,
            methods=["POST"],
            response_model=list[Narrative],
        )

    async def run_pipeline(self, request: PipelineRequest):
        logger.info("Pipeline request received | query={} limit={} tojson={}", request.query, request.limit, request.tojson)
        try:
            result = await self.executor_service.execute(
                query=request.query,
                limit=request.limit,
                tojson=request.tojson,
                sources=request.sources,
            )
            logger.info(
                "Pipeline request completed | narratives={} ids={}",
                len(result),
                [n.id for n in result],
            )
            return result
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=502, detail=f"Upstream service error: {e.response.text}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Pipeline failed: {str(e)}")