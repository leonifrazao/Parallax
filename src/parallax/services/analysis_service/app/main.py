from fastapi import FastAPI
from parallax.services.analysis_service.container import AnalysisContainer
from parallax.services.analysis_service.app.controllers.analysis_controller import AnalysisController

container = AnalysisContainer()

app = FastAPI(title="analysis-service", version="0.1.0")

analysis_controller = AnalysisController(
    analysis_service=container.analysis_service()
)

app.include_router(analysis_controller.router)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "analysis-service",
        "version": "0.1.0"
    }