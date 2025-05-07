from dataclasses import dataclass
from typing import Optional

from fastapi import APIRouter

from backend.apps.api_server.app_dependencies import AppDependencies


@dataclass
class Article:
    feed_url: str
    url: str
    title: Optional[str]
    content: str
    published_at: str


@dataclass
class ArticleListResponse:
    articles: list[Article]


def router(deps: AppDependencies) -> APIRouter:
    api = APIRouter()

    @api.get("/articles")
    def list_articles() -> ArticleListResponse:
        article_records = deps.articles_repository.find_all()
        article_list = [
            Article(
                feed_url=record.feed_url,
                url=record.url,
                title=record.title,
                content=record.content,
                published_at=record.published_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
            )
            for record in article_records
        ]
        return ArticleListResponse(articles=article_list)

    return api
