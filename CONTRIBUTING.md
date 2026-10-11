# Contributing

Small, focused contributions are welcome. Contributors remain responsible for understanding,
checking and explaining their changes, whether written manually or with an assistant.

## Contribution contract

- **CONTRIB-01 — Regression checks.** A PR adding or changing runtime behavior in
  `bookmarks/` must add or update an executable test in `tests/` exercising that behavior.
  A passing old suite alone is insufficient. Documentation-only changes are exempt.
- **CONTRIB-02 — Standard library only.** Runtime modules in `bookmarks/` must use only
  Python's standard library and this repository's modules. Do not add third-party imports
  or runtime dependencies; propose a policy change separately if a dependency is needed.
- **CONTRIB-03 — Shared URL identity.** Every export and CLI format must normalize URLs
  through `bookmarks.urls.normalize_url`, directly or through an existing exporter.
  Do not implement a separate normalization or deduplication identity in a format handler.
- **CONTRIB-04 — Preserve query semantics.** Normalization must preserve the query string
  exactly: names, values, repetitions and ordering. A query can identify a different resource.
  Never silently strip all query parameters or tracking-looking names in the shared helper.

## Sending a PR

Explain the problem and link an issue if one exists; lack of an issue is not a blocker.
Keep unrelated changes separate. Name callers affected by shared-helper changes.
Run `python3 -m unittest discover -s tests -v` and report the command's actual outcome.
Do not claim checks you did not run.

A maintainer may request changes for contribution-contract violations. A request for
changes is not automatic PR closure. Review and merge remain separate decisions.
