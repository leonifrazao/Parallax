from abc import ABC, abstractmethod
from botasaurus.request import Request

class IWebScraper(ABC):
    @abstractmethod
    def scrape_aljazeera(request: Request, data):
        pass
    
    @abstractmethod
    def scrape_bbc(request: Request, data):
        pass

    @abstractmethod
    def run_all(self):
        pass