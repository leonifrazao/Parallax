from datetime import datetime
from uuid import uuid4
from pydantic import BaseModel, Field, ConfigDict


class Headline(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    text: str
    source: str
    url: str | None = None
    description: str | None = None
    author: str | None = None
    published_at: datetime | None = None
    scraped_at: datetime = Field(default_factory=datetime.now)
    id: str = Field(default_factory=lambda: str(uuid4()))