from fastapi import FastAPI
from parallax.services.pipeline_service.container import PipelineContainer
from parallax.services.pipeline_service.app.controllers.pipeline_controller import PipelineController

container = PipelineContainer()

app = FastAPI(title="pipeline-service", version="0.1.0")

pipeline_controller = PipelineController(
    executor_service=container.executor_service()
)

app.include_router(pipeline_controller.router)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "pipeline-service",
        "version": "0.1.0"
    }