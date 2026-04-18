from abc import ABC, abstractmethod
from typing import Iterable
from parallax.models.enter import Headline


class IScraper(ABC):
    @abstractmethod
    def scrape(self, query: str) -> Iterable[Headline]:
        pass