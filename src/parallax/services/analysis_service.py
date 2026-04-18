
from parallax.interfaces.enter import IAnalysisUseCase, INarrativeAnalysis
from parallax.models import Narrative, Headline
from typing import List

class AnalysisService(IAnalysisUseCase):
    def __init__(self, narrative_analysis: INarrativeAnalysis):
        self.narrative_analysis = narrative_analysis

    def execute(self, headlines: List[Headline]) -> List[Narrative]:
        return self.narrative_analysis.analyze_narratives(headlines)