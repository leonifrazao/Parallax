from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class Headline:
    text: str
    source: str
    url: Optional[str] = None
    scraped_at: datetime = field(default_factory=datetime.now)

@dataclass
class Analysis:
    stance: str
    emotional_tone: str
    emotional_intensity: float
    narrative_summary: str
    motives: str
    key_entities: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
