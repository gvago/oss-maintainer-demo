# Bookmark Kit

A tiny, dependency-free Python toolkit for normalizing and exporting bookmarks.
Python 3.11+. MIT licensed. This is a working OSS project used as a maintainer-demo sandbox;
its seeded issues and PRs are examples, not outside community contributions.

```sh
python3 -m bookmarks 'HTTPS://Example.com/articles?lang=en#intro'
python3 -m unittest discover -s tests -v
```

## Where behavior lives

- `bookmarks/urls.py`: shared HTTP(S) identity, validation and normalization.
- `bookmarks/exports.py`: JSON export, stable first-seen deduplication.
- `bookmarks/__main__.py`: command-line interface, delegates to the exporter.
- `tests/test_bookmarks.py`: runnable regression checks, no test dependencies.

Scheme and host are case-insensitive. Path, query and fragment are preserved.
URLs without a path use `/`. Credentials, non-HTTP(S) schemes, whitespace and
invalid ports are rejected. The toolkit does not fetch URLs or promise that a host exists.

See [CONTRIBUTING.md](CONTRIBUTING.md) before sending a PR.

## Quickstart example

Pass multiple URLs to export them as a stable first-seen JSON list:

```sh
python3 -m bookmarks https://example.com/docs https://example.com/news
```
