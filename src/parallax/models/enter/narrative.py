from pydantic import BaseModel, ConfigDict


class Narrative(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    headline: str
    stance: str
    emotional_tone: str
    emotional_intensity: float
    key_entities: list[str]
    narrative_summary: str
    motives: list[str]
    url: str
    source: str