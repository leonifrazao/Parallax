from abc import ABC, abstractmethod
from typing import Iterable
from parallax.models.enter import Narrative


class ICliApp(ABC):
    @abstractmethod
    def render_narratives(self, narratives: Iterable[Narrative]) -> None:
        pass