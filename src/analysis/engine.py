import json
import logging
from typing import List, Dict, Optional
from ollama import chat
from interfaces.INarrativeAnalysis import INarrativeAnalysis

logger = logging.getLogger(__name__)

class NarrativeAnalysis(INarrativeAnalysis):
    def __init__(self, headlines: List[str], source: str):
        self.headlines = headlines
        self.source = source

    def _build_prompt(self) -> str:
        return f"""
        You are a senior intelligence analyst, cynical and an expert in Realistic Geopolitics.
        Analyze these headlines from '{self.source}': {json.dumps(self.headlines)}

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

    def analyze_narratives(self) -> Optional[List[Dict]]:
        try:
            response = chat(
                model='llama3.1',
                messages=[{'role': 'user', 'content': self._build_prompt()}],
                format='json',
                stream=False
            )
            
            content = response.get('message', {}).get('content', '')
            return json.loads(content) if content else None
            
        except Exception as e:
            logger.error(f"Narrative analysis failed: {e}")
            return None
