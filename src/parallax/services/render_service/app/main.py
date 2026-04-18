from fastapi import FastAPI
from parallax.services.render_service.app.controllers.render_controller import RenderController
from parallax.services.render_service.container import RenderContainer

app = FastAPI(title="render-service", version="0.1.0")

render_container = RenderContainer()
render_controller = RenderController(render_service=render_container.render_service())
app.include_router(render_controller.router)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "render-service",
        "version": "0.1.0",
    }