from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union


class IAnalysisMetrics(ABC):
    @abstractmethod
    def calculate_metrics(self, data: Union[Dict, List, None] = None):
        pass
