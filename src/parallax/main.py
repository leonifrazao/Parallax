from dependency_injector.wiring import Provide, inject
from parallax.container import Container
from parallax.interfaces import IWebScraper, INarrativeAnalysis
import asyncio


@inject
async def async_main(
    scraper: IWebScraper = Provide[Container.web_scraper], 
    engine: INarrativeAnalysis = Provide[Container.narrative_analysis]
):
    news = scraper.run_all()
    for batch in news:
        result = await engine.analyze_narratives(batch)
        print(result)
        


def main():
    asyncio.run(async_main())


container = Container()
container.wire(modules=[__name__])

if __name__ == "__main__":
    main()

# from analysis.engine import analyze_narratives
# import json

# with open('output/scrape_aljazeera.json', 'r') as f:
#     headlines = json.load(f)

# # Limiting to 5 for testing
# results = analyze_narratives(headlines[:5], "Al Jazeera")
# print(results)