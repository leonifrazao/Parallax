import httpx
from parallax.models.enter import Headline
from loguru import logger


class ScraperClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    async def execute(self, query: str, sources: list[str] | None = None) -> list[Headline]:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.base_url}/scrape",
                json={"query": query, "sources": sources},
            )
            response.raise_for_status()
            data = response.json()
            return [Headline.model_validate(item) for item in data]