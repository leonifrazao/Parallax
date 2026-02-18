from abc import ABC, abstractmethod


class INarrativeAnalysis(ABC):
    @abstractmethod
    def analyze_narratives(self):
        pass
