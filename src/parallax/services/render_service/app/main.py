from fastapi import FastAPI
from parallax.services.render_service.app.controllers.render_controller import RenderController

app = FastAPI(title="render-service", version="0.1.0")

render_controller = RenderController()
app.include_router(render_controller.router)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "render-service",
        "version": "0.1.0",
    }