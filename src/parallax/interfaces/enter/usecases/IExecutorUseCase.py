from abc import abstractmethod
from parallax.interfaces.enter import IWebScraper, INarrativeAnalysis

@abstractmethod
class IExecutorUseCase:
    @abstractmethod
    def execute(
        scraper: IWebScraper, 
        engine: INarrativeAnalysis 
    ):
        pass