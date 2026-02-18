from dependency_injector.wiring import Provide, inject
from container import Container
from interfaces import IWebScraper

@inject
def main(scraper: IWebScraper = Provide[Container.web_scraper]):
    titles = scraper.run_all()
    print(titles)

if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])
    main()

# from analysis.engine import analyze_narratives
# import json

# with open('output/scrape_aljazeera.json', 'r') as f:
#     headlines = json.load(f)

# # Limiting to 5 for testing
# results = analyze_narratives(headlines[:5], "Al Jazeera")
# print(results)