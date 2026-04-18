from typing import Iterable
from datetime import datetime
from newsapi import NewsApiClient
from loguru import logger

from parallax.interfaces.enter import IScraper
from parallax.models.enter import Headline
from parallax.scrapers.websites.base import BaseScraper


class NewsAPIScraper(BaseScraper, IScraper):

    def __init__(self, api_key: str):
        super().__init__()
        if not api_key:
            raise ValueError("api_key não pode ser vazio")
        self.api_key = api_key

    @property
    def client(self) -> NewsApiClient:
        return NewsApiClient(api_key=self.api_key)

    def _parse(self, response: dict) -> Iterable[Headline]:
        for article in response.get("articles", []):
            title = article.get("title")
            url = article.get("url")
            description = article.get("description")
            source = article.get("source", {}).get("name", "Unknown")

            if not title or not url or title == "[Removed]":
                continue
            if not description:
                continue

            published_raw = article.get("publishedAt")
            published_at = (
                datetime.fromisoformat(published_raw.replace("Z", "+00:00"))
                if published_raw else None
            )

            yield Headline(
                text=title,
                source=source,
                url=url,
                description=description,
                author=article.get("author"),
                published_at=published_at,
            )

    def scrape(self, query: str) -> Iterable[Headline]:
        logger.info(f"Scraping NewsAPI for: {query}")
        return self.get_headlines(
            fetcher=lambda: self.client.get_everything(
                q=query,
                language="en",
                sort_by="publishedAt",
                page_size=20,
            ),
            parser=self._parse,
        )

    def fetch_article_content(self, url: str) -> str:
        return self.get_page_content({
            "url": url,
            "root_selector": "article",
        })