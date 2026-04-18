from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Annotated
from datetime import datetime

Stance = Annotated[
    str,
    Field(
        pattern=r"^(neutral|pro_[a-z0-9_]+|anti_[a-z0-9_]+)$",
        description="Must be exactly 'neutral', or a single label like 'pro_iran' or 'anti_israel'"
    )
]


class NarrativeLLM(BaseModel):
    id: str
    headline: str
    stance: Stance

    emotional_tone: Literal[
        "alarmist",
        "factual",
        "sympathetic",
        "triumphalist",
        "defeatist",
    ]
    
    emotional_intensity: float = Field(
        ge=0,
        le=10,
        description="A score from 0 to 10"
    )
    key_entities: List[str]
    narrative_summary: str
    motives: List[str]
    published_at: Optional[datetime] = None


class NarrativeListResponse(BaseModel):
    headlines: List[NarrativeLLM]