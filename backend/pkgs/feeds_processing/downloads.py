from dataclasses import dataclass
from urllib.request import urlopen


@dataclass(frozen=True)
class Download:
    url: str
    content: str


@dataclass(frozen=True)
class DownloadFailure:
    exception: Exception


def download(url: str) -> Download | DownloadFailure:
    try:
        output = urlopen(url).read()
        return Download(url, content=output.decode('utf-8'))
    except Exception as e:
        return DownloadFailure(e)
