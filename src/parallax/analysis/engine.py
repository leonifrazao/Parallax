from typing import Iterable
import json
import logging
import os
from typing import List, Dict, Optional
from ollama import AsyncClient
from parallax.interfaces import INarrativeAnalysis
from parallax.database.models import Headline

logger = logging.getLogger(__name__)

class NarrativeAnalysis(INarrativeAnalysis):

    def __init__(self):
        self.client = AsyncClient(host=os.getenv("OLLAMA_HOST", "http://localhost:11434"))

    def _build_prompt(self, headlines: List[Headline]) -> str:

        source = headlines[0].source
        texts = [h.text for h in headlines]

        return f"""
        You are a senior intelligence analyst, cynical and an expert in Realistic Geopolitics.
        Analyze these headlines from '{source}': {json.dumps(texts)}

        CRITERIA:
        1. Look for hidden agendas and political beneficiaries.
        2. Identify attempts to legitimize or demonize.
        3. Avoid obvious motives (e.g., "inform the public").
        4. Be brief, direct, and cynical.

        RESPONSE FORMAT:
        Return ONLY a JSON list of objects:
        [
            {{
                "headline": "string",
                "stance": "pro_[country]" | "neutral" | "anti_[country]",
                "emotional_tone": "alarmist" | "factual" | "patriotic",
                "emotional_intensity": from -1 (sad) to 1 (happy),
                "key_entities": ["entity1", "entity2"],
                "narrative_summary": "short context",
                "motives": "political/ideological reasoning"
            }}
        ]
        """

    async def analyze_narratives(self, headlines: Iterable[Headline]) -> Optional[List[Dict]]:

        logger.info(f"Analyzing narratives from a new batch...")
        try:

            iterable_list = list(headlines)

            if not iterable_list:
                logger.error(f"No headlines provided")
                return ""

            response = await self.client.chat(
                model='llama3.1',
                messages=[{'role': 'user', 'content': self._build_prompt(iterable_list)}],
                format='json',
                stream=False
            )
            
            content = response.message.content or ""

            if content:
                logger.info(f"Narrative analysis completed successfully")
                return json.loads(content)
            else:
                logger.error(f"Narrative analysis failed")
                return None
            
        except Exception as e:
            logger.error(f"Narrative analysis failed: {e}")
            return None
