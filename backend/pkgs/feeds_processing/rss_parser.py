from backend.pkgs.feeds_processing.downloads import Download
from backend.pkgs.feeds_processing.feed_parser import FeedParser, ParseFeedFailure, ParseError, Feed


class RssParser(FeedParser):
    def try_parse(self, download: Download) -> Feed | ParseFeedFailure:
        return ParseFeedFailure(errors=[ParseError(message="Not implemented")])
