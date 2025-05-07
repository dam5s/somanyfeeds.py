from pathlib import Path

from backend.pkgs.feeds_processing.downloads import Download


def content_from_feed_resource(file_name: str) -> str:
    file_path = Path(__file__).parent / "resources" / file_name

    with open(file_path) as f:
        return f.read()


def download_from_feed_resource(file_name: str) -> Download:
    return Download(
        url=f"file://{file_name}",
        content=content_from_feed_resource(file_name),
    )
