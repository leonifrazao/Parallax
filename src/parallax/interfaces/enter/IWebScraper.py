from abc import ABC, abstractmethod
from typing import Iterable, List
from parallax.models.enter import Headline

class IWebScraper(ABC):

    @abstractmethod
    def run_all(self, query: str, sources: list[str] | None = None) -> List[Headline]:
        pass