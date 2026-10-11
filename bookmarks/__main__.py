import argparse
import sys

from bookmarks.exports import export_csv, export_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize and deduplicate bookmarks as JSON")
    parser.add_argument("urls", nargs="+")
    parser.add_argument("--format", choices=("json", "csv"), default="json")
    args = parser.parse_args()
    try:
        exporter = export_csv if args.format == "csv" else export_json
        output = exporter(args.urls)
        if args.format == "csv":
            sys.stdout.reconfigure(encoding="utf-8", newline="")
        print(output, end="" if output.endswith("\n") else "\n")
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
