from abc import ABC, abstractmethod
from parallax.models.enter.web import RenderRequest

class IRenderUseCase(ABC):
    @abstractmethod
    async def execute(self, request: RenderRequest) -> dict:
        pass