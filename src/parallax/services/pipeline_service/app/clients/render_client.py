import httpx
from parallax.models.enter import Narrative


class RenderClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    async def execute(
        self,
        title: str,
        filename: str,
        items: list[Narrative],
    ) -> dict:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/render/save",
                json={
                    "title": title,
                    "filename": filename,
                    "items": [item.model_dump(mode="json") for item in items],
                },
            )
            response.raise_for_status()
            return response.json()