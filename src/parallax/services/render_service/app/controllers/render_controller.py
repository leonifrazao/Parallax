from fastapi import APIRouter, HTTPException
from parallax.models.enter.web import RenderRequest
from datetime import datetime
from parallax.interfaces.enter.usecases import IRenderUseCase
from loguru import logger
import time


class RenderController:
    def __init__(self, render_service: IRenderUseCase):
        self.router = APIRouter()
        self.render_service = render_service
        self.router.add_api_route("/render/save", self.render_and_save, methods=["POST"])
    
    def _timestamp(self) -> str:
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    async def render_and_save(self, request: RenderRequest):
        try:
            render_start = time.time()
            logger.info("Render request received | filename={} items={}", request.filename, len(request.items))
            result = await self.render_service.execute(request)
            logger.info("Render request completed | result={}", result)
            logger.info("Render total took {}ms", int((time.time() - render_start) * 1000))
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Render failed: {str(e)}")

        