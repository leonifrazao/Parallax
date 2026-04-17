from botasaurus.request import request, Request
from botasaurus.soupify import soupify
from parallax.database.models import Headline
from loguru import logger

class BaseScraper:
    def __init__(self):
        pass

    @staticmethod
    @request(output=None)
    def get_news_headlines(request: Request, data):

        logger.info(f"Getting news headlines from {data['source']}")
        try:
            response = request.get(data['link'])
            soup = soupify(response)
            
            # Gets only the text
            elements = soup.select(data['selector'])
            for el in elements:
                titulo = el.get_text(strip=True)
                
                # Creates the object without URL
                headline = Headline(text=titulo, source=data['source'])
                yield headline
                
        except Exception as e:
            logger.error(f"Error fetching headlines from {data['link']}: {str(e)}")
            return None
