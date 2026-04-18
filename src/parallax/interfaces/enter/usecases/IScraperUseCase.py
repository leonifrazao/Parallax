from abc import ABC, abstractmethod
from typing import List
from parallax.models.enter import Headline

class IScraperUseCase(ABC):
    @abstractmethod
    def execute(self, query: str) -> List[Headline]:
        pass