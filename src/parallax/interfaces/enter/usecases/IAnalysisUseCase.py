from abc import ABC, abstractmethod
from typing import List
from parallax.models import Narrative, Headline


class IAnalysisUseCase(ABC):
    @abstractmethod
    def execute(self, headlines: List[Headline]) -> List[Narrative]:
        pass