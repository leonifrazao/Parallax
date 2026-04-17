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
        headlines_list = []

        logger.info(f"Scraping {data['source']}")
        try:
            response = request.get(data['link'])
            soup = soupify(response)
            
            # Gets only the text
            elements = soup.select(data['selector'])
            for el in elements:
                titulo = el.get_text(strip=True)
                
                # Creates the object without URL
                headline = Headline(text=titulo, source=data['source'])
                headlines_list.append(headline)
            
            if headlines_list:
                logger.info(f"Scraped {len(headlines_list)} headlines from {data['source']}")
            else:
                logger.warning(f"No headlines found in {data['source']}")
            return headlines_list
        except Exception as e:
            logger.error(f"Error fetching headlines from {data['link']}: {str(e)}")
            return None
