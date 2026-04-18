from dataclasses import dataclass, field
from typing import List

@dataclass
class Narrative:
    id: str
    headline: str
    stance: str
    emotional_tone: str
    emotional_intensity: float
    key_entities: List[str]
    narrative_summary: str
    motives: str
    url: str
    source: str