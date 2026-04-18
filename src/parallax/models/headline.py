from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
import uuid


@dataclass
class Headline:
    text: str
    source: str
    url: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None
    published_at: Optional[datetime] = None
    scraped_at: datetime = field(default_factory=datetime.now)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))