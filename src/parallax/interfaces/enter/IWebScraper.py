from abc import ABC, abstractmethod
from botasaurus.request import Request
from typing import Iterable, List
from parallax.models import Headline

class IWebScraper(ABC):

    @abstractmethod
    def run_all(self, query: str) -> List[Headline]:
        pass