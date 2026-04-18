from pydantic import BaseModel

class ScrapeRequest(BaseModel):
    query: str
    sources: list[str] = []