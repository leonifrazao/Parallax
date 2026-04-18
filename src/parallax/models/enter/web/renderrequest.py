from pydantic import BaseModel
from parallax.models.enter import Narrative


class RenderRequest(BaseModel):
    title: str
    filename: str
    items: list[Narrative]
