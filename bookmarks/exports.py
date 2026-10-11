import json

from bookmarks.urls import normalize_url


def export_json(urls: list[str]) -> str:
    """Export unique normalized URLs in first-seen order."""
    return json.dumps(list(dict.fromkeys(normalize_url(url) for url in urls)), indent=2)


def export_csv(urls: list[str]) -> str:
    """Export normalized unique URLs as one CSV column."""
    import csv
    import io

    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(["url"])
    writer.writerows([url] for url in dict.fromkeys(normalize_url(url) for url in urls))
    return output.getvalue()
