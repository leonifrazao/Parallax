from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class IAnalysisMetrics(ABC):
    @abstractmethod
    def calculate_metrics(self, data: Optional[Dict, List] = None):
        pass
