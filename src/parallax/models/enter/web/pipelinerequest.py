from pydantic import BaseModel


class PipelineRequest(BaseModel):
    query: str
    limit: int = 10
    tojson: bool = False