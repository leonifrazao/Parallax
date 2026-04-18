from dependency_injector import containers, providers
from parallax.services.render_service.app.services.render_service import RenderService


class RenderContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    render_service = providers.Factory(RenderService)
    