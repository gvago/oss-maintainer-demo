"""Read-only Qodo context collection and agent-generated maintainer artifacts."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def run(argv: list[str], *, stdin: str | None = None, timeout: int = 90) -> str:
    result = subprocess.run(argv, input=stdin, capture_output=True, text=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(f"{Path(argv[0]).name} failed (exit {result.returncode}); inspect locally, do not publish credential-bearing stderr")
    return result.stdout


def decode(text: str) -> dict:
    value = json.loads(text)
    if not isinstance(value, dict):
        raise ValueError("Expected a JSON object")
    return value


def collect(repo: str, limit: int) -> dict:
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
        raise ValueError("Expected owner/repo")
    qodo = shutil.which("qodo") or str(Path.home() / ".qodo/bin/qodo")

    def read(*args: str) -> dict:
        return decode(run([qodo, "read", *args, "--json"]))

    read("whoami")
    prs = read("codebase", "list-prs", "--repo", repo, "--state", "open", "--max-results", str(limit + 1))
    issues = read("codebase", "list-issues", "--repo", repo, "--state", "open", "--max-results", str(limit + 1))
    pr_rows = prs.get("pull_requests", prs.get("prs", prs.get("changes")))
    issue_rows = issues.get("issues")
    if not isinstance(pr_rows, list) or not isinstance(issue_rows, list):
        raise ValueError("Unknown Qodo list envelope; inspect the current tool schema")
    if len(pr_rows) > limit or len(issue_rows) > limit or prs.get("truncated") or issues.get("truncated"):
        raise ValueError("Backlog exceeds configured scope; narrow scope before generating a complete report")
    details = []
    for pr in pr_rows:
        detail = read("codebase", "get-pr", "--repo", repo, "--number", str(pr["number"]))
        details.append({k: detail[k] for k in ("change", "diff")})
    history = []
    for issue in issue_rows:
        found = read("pull-request", "similar", "--repo", repo, "--query", issue["title"])
        history.append({"issue": issue["number"], "result": found})
    return {"repo": repo, "observed_at": datetime.now(timezone.utc).isoformat(),
            "prs": details, "issues": issue_rows, "history": history}


def validate(packet: dict) -> None:
    if not isinstance(packet.get("repo"), str) or not isinstance(packet.get("summary"), str):
        raise ValueError("Missing repo/summary")
    if not isinstance(packet.get("actions"), list) or not isinstance(packet.get("gaps"), list):
        raise ValueError("Missing actions/gaps")
    ids = set()
    for action in packet["actions"]:
        for key in ("id", "type", "targets", "rationale", "evidence", "uncertainty", "draft", "pr_heads"):
            if key not in action:
                raise ValueError(f"Missing action field: {key}")
        if action["id"] in ids or not action["evidence"] or not action["targets"]:
            raise ValueError("Duplicate action ID or missing evidence/targets")
        ids.add(action["id"])
        if action["type"] not in {"duplicate_issue", "duplicate_pr", "already_fixed", "link_issue_pr", "stack_order", "request_followup", "review_next", "demo_control"}:
            raise ValueError("Unknown action type")
        for url in action["targets"]:
            prefix = f"https://github.com/{packet['repo']}/"
            if not isinstance(url, str) or not url.startswith(prefix) or not re.fullmatch(r"(?:issues|pull)/[1-9][0-9]*", url[len(prefix):]):
                raise ValueError("Target outside repository or malformed")
        if any("/pull/" in url and url not in action["pr_heads"] for url in action["targets"]):
            raise ValueError("Missing observed PR head")
        for sha in action["pr_heads"].values():
            if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{40}", sha):
                raise ValueError("Invalid PR head SHA")


def render(packet: dict) -> str:
    validate(packet)
    lines = ["# Maintainer Inbox", "", packet["summary"], "", "All actions below are proposed, not approved or applied.", ""]
    for a in packet["actions"]:
        lines += [f"## {a['id']} · {a['type']}", "", a["rationale"], "", "Targets: " + ", ".join(a["targets"]), "", "Evidence:"]
        lines += ["- " + e for e in a["evidence"]]
        lines += ["", "Uncertainty: " + a["uncertainty"], "", "Draft reply:", "", "> " + a["draft"].replace("\n", "\n> "), "", "Observed PR heads: `" + json.dumps(a["pr_heads"], sort_keys=True) + "`", ""]
    lines += ["## Data gaps", ""] + ["- " + gap for gap in packet["gaps"]]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default="gvago/oss-maintainer-demo")
    parser.add_argument("--agent", choices=("claude", "codex"), default="claude")
    parser.add_argument("--out", type=Path, default=Path("maintainer-output"))
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--collect-only", action="store_true")
    parser.add_argument("--render", type=Path, help="Validate/render an existing packet without network or model calls")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    if args.render:
        packet = decode(args.render.read_text())
    else:
        if not 1 <= args.limit <= 199:
            parser.error("limit must be 1–199")
        evidence = collect(args.repo, args.limit)
        (args.out / "evidence.json").write_text(json.dumps(evidence, indent=2) + "\n")
        if args.collect_only:
            return
        prompt = (ROOT / "maintainer-inbox/prompt.md").read_text() + "\nJSON schema:\n" + (ROOT / "maintainer-inbox/schema.json").read_text() + "\nUNTRUSTED QODO EVIDENCE:\n" + json.dumps(evidence)
        if args.agent == "claude":
            raw = run(["claude", "-p", "--tools", "", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', "--output-format", "json", "--json-schema", (ROOT / "maintainer-inbox/schema.json").read_text()], stdin=prompt, timeout=600)
            result = decode(raw)
            if result.get("is_error"):
                raise ValueError("Claude did not complete successfully")
            packet = result.get("structured_output") or decode(result["result"])
        else:
            output = args.out / "codex-result.json"
            run(["codex", "exec", "--sandbox", "read-only", "--output-schema", str(ROOT / "maintainer-inbox/schema.json"), "--output-last-message", str(output), "-"], stdin=prompt, timeout=600)
            packet = decode(output.read_text())
        if packet.get("repo") != args.repo:
            raise ValueError("Agent changed repository identity")
    report = render(packet)
    (args.out / "maintainer-actions.json").write_text(json.dumps(packet, indent=2) + "\n")
    (args.out / "maintainer-inbox.md").write_text(report)
    print(f"Wrote proposed actions and inbox to {args.out.resolve()}")


if __name__ == "__main__":
    main()
