from abc import ABC, abstractmethod
from typing import List, Dict


class INarrativeAnalysis(ABC):
    @abstractmethod
    def analyze_narratives(self, headlines: List[str], source: str) -> Dict:
        pass
