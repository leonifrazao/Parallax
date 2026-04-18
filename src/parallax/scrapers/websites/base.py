
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