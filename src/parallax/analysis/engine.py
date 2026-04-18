from parallax.models.enter.narrativeLLM import NarrativeListResponse
from typing import Iterable
import json
import os
from typing import List
from ollama import AsyncClient
from parallax.interfaces.enter import INarrativeAnalysis
from parallax.models.enter import Headline, Narrative
from loguru import logger


class NarrativeAnalysis(INarrativeAnalysis):

    def __init__(self, model: str = "llama3.1"):
        self.client = AsyncClient(host=os.getenv("OLLAMA_HOST", "http://localhost:11434"))
        self.model = model
        logger.info("NarrativeAnalysis initialized | model={} host={}", self.model, os.getenv("OLLAMA_HOST"))

    def _build_prompt(self, headlines: List[Headline]) -> str:
        payload = [
            {
                "id": h.id,
                "headline": h.text,
                "description": h.description or "",
                "source": h.source,
            }
            for h in headlines
        ]

        logger.info("Building prompt | headlines={}", len(payload))

        return f"""
You are a senior intelligence analyst specialized in geopolitical narrative analysis.

Analyze the following headlines:

{json.dumps(payload, ensure_ascii=False)}

SUPER IMPORTANT: EMOTIONAL INTENSITY: 0.0 - 1.0
"""

    async def analyze_narratives(self, headlines: Iterable[Headline]) -> List[Narrative]:
        logger.info("Starting narrative analysis...")

        try:
            iterable_list = list(headlines)
            logger.info("Received headlines | count={}", len(iterable_list))

            if not iterable_list:
                logger.warning("No headlines provided")
                return []

            logger.info("Calling Ollama | model={}", self.model)

            response = await self.client.chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": self._build_prompt(iterable_list),
                    }
                ],
                format=NarrativeListResponse.model_json_schema(),
                options={"temperature": 0},
                stream=False,
            )

            if not response:
                logger.error("Ollama returned no response")
                return []

            logger.info("Ollama response received")

            content = response.message.content or ""

            if not content:
                logger.error("Empty response content")
                return []

            parsed = NarrativeListResponse.model_validate_json(content)
            logger.info("Parsed LLM output | candidates={}", len(parsed.headlines))

            original_by_id = {headline.id: headline for headline in iterable_list}
            narratives: List[Narrative] = []

            for item in parsed.headlines:
                original = original_by_id.get(item.id)

                if not original:
                    logger.warning("Unknown id returned by LLM | id={}", item.id)
                    continue

                data = item.model_dump()
                data["url"] = original.url
                data["source"] = original.source

                narratives.append(Narrative.model_validate(data))

            logger.success("Analysis completed | final_narratives={}", len(narratives))

            return narratives

        except Exception:
            logger.exception("Narrative analysis crashed")
            raise