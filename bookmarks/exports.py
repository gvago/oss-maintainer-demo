import json

from bookmarks.urls import normalize_url


def export_json(urls: list[str]) -> str:
    """Export unique normalized URLs in first-seen order."""
    return json.dumps(list(dict.fromkeys(normalize_url(url) for url in urls)), indent=2)
