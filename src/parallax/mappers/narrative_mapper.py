from typing import List, Dict, Optional
from dataclasses import fields
from parallax.models import Narrative


class NarrativeMapper:

    @staticmethod
    def _filter_fields(data: Dict) -> Dict:
        valid_fields = {f.name for f in fields(Narrative)}
        return {k: v for k, v in data.items() if k in valid_fields}

    @staticmethod
    def from_dict(data: Dict, **kwargs) -> Narrative:
        merged = {**data, **kwargs}
        filtered = NarrativeMapper._filter_fields(merged)
        return Narrative(**filtered)

    @staticmethod
    def from_response(data: Dict) -> List[Narrative]:
        if isinstance(data, dict) and "headlines" in data:
            items = data["headlines"]
        elif isinstance(data, list):
            items = data
        else:
            return []

        return [NarrativeMapper.from_dict(item) for item in items]