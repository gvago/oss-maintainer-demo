import json

from bookmarks.urls import normalize_url


def export_json(urls: list[str]) -> str:
    """Export unique normalized URLs in first-seen order."""
    return json.dumps(list(dict.fromkeys(normalize_url(url) for url in urls)), indent=2)


def export_readable(urls: list[str]) -> str:
    """Render a compact readable bookmark list."""
    from tabulate import tabulate

    return tabulate([[url.lower()] for url in dict.fromkeys(urls)], headers=["url"])
