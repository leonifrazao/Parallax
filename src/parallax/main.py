import asyncio
from dependency_injector.wiring import Provide, inject

from parallax.container import Container
from parallax.interfaces.enter import IExecutorUseCase
from parallax.interfaces.out import ICliApp


class ParallaxApp:
    def __init__(self, executor: IExecutorUseCase, ui: ICliApp):
        self.executor = executor
        self.ui = ui

    async def run(self):
        narratives = await self.executor.execute(limit=5, tojson=True)
        if not narratives:
            raise ValueError("No narratives found")
        self.ui.render_narratives(narratives)



@inject
def main(
    executor: IExecutorUseCase = Provide[Container.executor_service],
    ui: ICliApp = Provide[Container.cli_app],
):
    app = ParallaxApp(executor, ui)
    asyncio.run(app.run())


container = Container()
container.wire(modules=[__name__])

if __name__ == "__main__":
    main()