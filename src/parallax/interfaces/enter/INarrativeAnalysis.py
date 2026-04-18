from abc import ABC, abstractmethod
from typing import List, Dict
from parallax.models.enter import Narrative, Headline


class INarrativeAnalysis(ABC):
    @abstractmethod
    def analyze_narratives(self, headlines: List[Headline]) -> List[Narrative]:
        pass
