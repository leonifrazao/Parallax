from botasaurus.request import request, Request
from botasaurus.soupify import soupify
from database.models import Headline

class BaseScraper:
    def __init__(self):
        pass

    @staticmethod
    @request(output=None)
    def get_news_headlines(request: Request, data):
        headlines_list = []
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
                
            return headlines_list
        except Exception as e:
            print(f"Error fetching headlines from {data['link']}: {str(e)}")
            return None
