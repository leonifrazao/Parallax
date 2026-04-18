import re
from typing import List
from rapidfuzz import fuzz

from parallax.models import Headline


class HeadlineDeduplicator:

    @staticmethod
    def deduplicate(headlines: List[Headline], threshold: int = 84) -> List[Headline]:
        result: List[Headline] = []

        for candidate in headlines:
            candidate_text = HeadlineDeduplicator._build_text(candidate)

            found_duplicate = False

            for i, existing in enumerate(result):
                existing_text = HeadlineDeduplicator._build_text(existing)

                similarity = fuzz.token_set_ratio(candidate_text, existing_text)

                if similarity >= threshold:
                    found_duplicate = True

                    if HeadlineDeduplicator._score(candidate) > HeadlineDeduplicator._score(existing):
                        result[i] = candidate

                    break

            if not found_duplicate:
                result.append(candidate)

        return result

    @staticmethod
    def _build_text(headline: Headline) -> str:
        text = f"{headline.text or ''} {headline.description or ''}"
        return HeadlineDeduplicator._normalize(text)

    @staticmethod
    def _normalize(text: str) -> str:
        text = (text or "").lower().strip()
        text = text.replace("’", "'")
        text = re.sub(r"[^\w\s']", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text

    @staticmethod
    def _score(headline: Headline) -> int:
        return len(headline.text or "") + len(headline.description or "")