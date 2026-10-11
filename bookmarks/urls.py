from urllib.parse import urlsplit, urlunsplit


def normalize_url(value: str, *, strip_fragment: bool = False) -> str:
    """Normalize HTTP(S) identity while preserving path, query and fragment."""
    if not isinstance(value, str) or not value or any(c.isspace() or ord(c) < 32 or ord(c) == 127 for c in value):
        raise ValueError("URL must be a nonempty string without whitespace or controls")
    try:
        parts = urlsplit(value)
        port = parts.port
        host = parts.hostname
    except ValueError as error:
        raise ValueError("Invalid URL") from error
    if parts.scheme not in {"http", "https"} or not host or parts.username is not None or parts.password is not None:
        raise ValueError("Expected an HTTP(S) URL without credentials")
    host = host.lower()
    authority = f"[{host}]" if ":" in host else host
    if port is not None and (parts.scheme, port) not in {("http", 80), ("https", 443)}:
        authority += f":{port}"
    fragment = parts.fragment if not strip_fragment else ""
    return urlunsplit((parts.scheme.lower(), authority, parts.path or "/", parts.query, fragment))
