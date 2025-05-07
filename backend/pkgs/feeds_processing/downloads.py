from dataclasses import dataclass

import requests


@dataclass(frozen=True)
class Download:
    url: str
    content: str


@dataclass(frozen=True)
class DownloadFailure:
    exception: Exception


def download(url: str) -> Download | DownloadFailure:
    try:
        response = requests.get(url)
        return Download(url, content=response.content.decode("utf-8"))
    except Exception as e:
        return DownloadFailure(e)
