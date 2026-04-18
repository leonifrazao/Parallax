from botasaurus.request import request, Request
from botasaurus.soupify import soupify
from loguru import logger
from typing import Callable, Iterable, Any
from parallax.models.enter import Headline


class BaseScraper:
    def __init__(self):
        pass

    @staticmethod
    def get_headlines(fetcher: Callable[[], Any], parser: Callable[[Any], Iterable[Headline]]) -> Iterable[Headline]:
        logger.info("Fetching headlines...")
        try:
            raw = fetcher()
            yield from parser(raw)
        except Exception as e:
            logger.error(f"Error fetching headlines: {e}")

    @staticmethod
    @request(output=None)
    def get_page_content(request: Request, data) -> str:
        logger.info(f"Getting page content from {data['url']}")
        try:
            response = request.get(data["url"])
            soup = soupify(response)
            root = soup.select_one(data["root_selector"])
            if not root:
                return ""
            return "\n".join(
                p.get_text(strip=True)
                for p in root.find_all("p")
                if len(p.get_text(strip=True)) > 40
            )
        except Exception as e:
            logger.error(f"Error fetching content: {e}")
            return ""