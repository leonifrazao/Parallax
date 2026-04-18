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

    def _normalize(self, text: str) -> str:
        return (text or "").lower()

    def _text_of(self, h: Headline) -> str:
        return self._normalize(f"{h.text} {h.description or ''}")

    def _filter_by_query(self, query: str, headlines: list[Headline]) -> list[Headline]:
        term = self._normalize(query).strip()

        if not term:
            return headlines

        filtered = [
            h for h in headlines
            if term in self._text_of(h)
        ]

        logger.info("Query filter applied | query={} before={} after={}", query, len(headlines), len(filtered))
        return filtered

    def scrape(self, query: str, sources: list[str] | None = None) -> Iterable[Headline]:
        logger.info("Scraping NewsAPI for: {} | sources={}", query, sources)

        params = {
            "q": query,
            "language": "en",
            "sort_by": "relevancy",
            "page_size": 20,
        }

        if sources:
            params["sources"] = ",".join(sources)

        headlines = list(self.get_headlines(
            fetcher=lambda: self.client.get_everything(**params),
            parser=self._parse,
        ))

        filtered = self._filter_by_query(query, headlines)

        logger.info("Filtered headlines {} -> {}", len(headlines), len(filtered))
        return filtered

    def fetch_article_content(self, url: str) -> str:
        return self.get_page_content({
            "url": url,
            "root_selector": "article",
        })