from dependency_injector import containers, providers

from parallax.analysis.engine import NarrativeAnalysis
from parallax.services.analysis_service.app.services import AnalysisService


class AnalysisContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    narrative_analysis = providers.Factory(NarrativeAnalysis)

    analysis_service = providers.Factory(
        AnalysisService,
        narrative_analysis=narrative_analysis,
    )