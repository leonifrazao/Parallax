from parallax.models.narrativeLLM import NarrativeListResponse
from typing import Iterable
import json
import logging
import os
from typing import List, Dict, Optional
from ollama import AsyncClient
from parallax.interfaces.enter import INarrativeAnalysis
from parallax.models import Headline, Narrative
from parallax.mappers import NarrativeMapper
from rapidfuzz import fuzz
import re

logger = logging.getLogger(__name__)

class NarrativeAnalysis(INarrativeAnalysis):

    def __init__(self, model: str = "llama3.1"):
        self.client = AsyncClient(host=os.getenv("OLLAMA_HOST", "http://localhost:11434"))
        self.model = model

    def _build_prompt(self, headlines: List[Headline]) -> str:

        source = headlines[0].source
        payload = [
            {
                "id": h.id,
                "headline": h.text,
                "description": h.description or "",
            }
            for h in headlines
        ]

        return f"""
You are a senior intelligence analyst specialized in geopolitical narrative analysis.

Analyze the following headlines from '{source}':

{json.dumps(payload, ensure_ascii=False)}

Your task:
For each distinct narrative, return exactly one structured analysis entry.

Core rules:
- You MUST preserve each "id" exactly as provided.
-Use a 0 to 10 scale, not 0 to 1
- Never invent, alter, reorder, or omit ids unless removing duplicates.
- Deduplicate aggressively.
- If two or more headlines describe the same event, same claim, same speech, same ceasefire, or the same narrative framing, keep ONLY the single best headline.
- Prefer the headline that is more specific, more informative, and better supported by its description.
- Preserve proper capitalization for countries, organizations, and people.
- Do not lowercase named entities.
- Prefer geopolitical actors (countries, organizations) over individual politicians when both are present.
- The output may contain fewer items than the input.

Stance rules:
- stance must be exactly one value only.
- Allowed format:
  - neutral
  - pro_<actor>
  - anti_<actor>
- Use lowercase only.
- Use underscores instead of spaces.
- Never output multiple stance values.
- Never use commas, parentheses, explanations, annotations, or placeholders.
- Never output values like:
  - pro_<actor>
  - anti_<actor>
  - anti_us, anti_israel
  - pro_iran (government)
- If multiple actors are involved, choose only the single dominant actor.
- Prefer stable geopolitical actors, states, organizations, or major political actors explicitly central to the narrative.

Narrative rules:
- Focus on framing, political beneficiaries, legitimization, delegitimization, and strategic messaging.
- Identify the implied narrative, not just the surface topic.
- Be analytical, concise, and realistic.
- Do not write vague or generic summaries.

Motives rules:
- motives must reflect likely strategic communication intent.
- Avoid generic motives such as:
  - informing_the_public
  - neutrality_maintenance
  - reporting_events
  - raising_awareness
  - strategic_messaging
- Motives should describe specific narrative purpose, such as:
  - legitimization_of_hezbollah
  - delegitimization_of_israel
  - framing_ceasefire_as_temporary
  - boosting_resistance_morale
  - portraying_us_as_destabilizing_actor
- Return short, specific, analytical motive labels using underscores.

Entity rules:
- key_entities must include ALL major actors explicitly central to the narrative.
- Include countries, leaders, and organizations when relevant.
- Prefer 2 to 5 entities.
- Do not omit obvious actors present in the headline.

- emotional_tone must reflect how the article is framed, not the outcome of the conflict.
- Use:
  - alarmist → fear, urgency, threat framing
  - triumphalist → victory, strength, success framing
  - defeatist → loss, collapse, exhaustion framing
  - sympathetic → human impact, suffering
  - factual → neutral, descriptive tone

Style rules:
- Preserve the original capitalization of headlines.
- Keep narrative_summary concise, analytical, and directly tied to the framing.
- Do not output filler, hedging, or generic media-language.



"""

    async def analyze_narratives(self, headlines: Iterable[Headline]) -> Optional[List[Narrative]]:

        logger.info(f"Analyzing narratives from a new batch...")
        try:

            iterable_list = list(headlines)

            if not iterable_list:
                logger.error(f"No headlines provided")
                return None

            response = await self.client.chat(
                model=self.model,
                messages=[
                    {
                        'role': 'user', 
                        'content': self._build_prompt(iterable_list)
                    }
                ],

                format=NarrativeListResponse.model_json_schema(),
                options={'temperature':0},
                stream=False
            )

            if not response:
                logger.error("Narrative analysis failed: no response")
                return None

            content = response.message.content or ""

            if not content:
                logger.error("Narrative analysis failed: empty response content")
                return None
            
            parsed = NarrativeListResponse.model_validate_json(content)

            original_by_id = {
                headline.id: headline
                for headline in iterable_list
            }

            narratives = []

            for item in parsed.headlines:
                original = original_by_id.get(item.id)

                if not original:
                    logger.warning(f"Unknown id returned by LLM: {item.id}")
                    continue

                narratives.append(
                    NarrativeMapper.from_dict(
                        item.model_dump(),
                        url=original.url,
                        source=original.source,
                        published_at=original.published_at
                    )
                )

            logger.info(f"Narrative analysis completed successfully")
            return narratives
            
        except Exception as e:
            logger.error(f"Narrative analysis failed: {e}")
            return None
