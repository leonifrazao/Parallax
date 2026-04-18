import httpx
from fastapi.encoders import jsonable_encoder
from parallax.models.enter import Headline, Narrative
from loguru import logger


class AnalysisClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    async def execute(self, headlines: list[Headline]) -> list[Narrative]:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/analyze",
                json=[jsonable_encoder(h) for h in headlines],
            )
            response.raise_for_status()
            data = response.json()
            return [Narrative.model_validate(item) for item in data]