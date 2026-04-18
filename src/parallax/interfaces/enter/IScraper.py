from abc import ABC, abstractmethod
from typing import Iterable
from parallax.models import Headline


class IScraper(ABC):
    @abstractmethod
    def scrape(self, query: str) -> Iterable[Headline]:
        pass