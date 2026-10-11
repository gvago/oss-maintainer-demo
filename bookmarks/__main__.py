import argparse

from bookmarks.exports import export_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize and deduplicate bookmarks as JSON")
    parser.add_argument("urls", nargs="+")
    args = parser.parse_args()
    try:
        print(export_json(args.urls))
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
