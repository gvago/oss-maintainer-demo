"""Read-only Qodo context collection and agent-generated maintainer artifacts."""
import argparse
from datetime import datetime, timezone
import json
from html import escape
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

    run([qodo, "--version"])
    read("whoami")
    run([qodo, "tools", "--refresh", "--json"])
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
        if detail.get("qar_operation_result_truncated"):
            detail = read("codebase", "get-pr", "--repo", repo, "--number", str(pr["number"]), "--args", '{"include_diff":false}')
            detail["diff"] = {"unavailable": "Combined diff exceeds upstream byte limit; do not classify as duplicate or complete implementation."}
        if "change" not in detail or "diff" not in detail:
            raise ValueError(f"PR #{pr['number']} returned unsupported envelope keys {list(detail)}; code={detail.get('code', detail.get('error_code', 'unknown'))}")
        details.append({k: detail[k] for k in ("change", "diff")})
    history = []
    for issue in issue_rows:
        found = read("pull-request", "similar", "--repo", repo, "--query", issue["title"])
        history.append({"issue": issue["number"], "result": found})
    current = {}
    for path in ("bookmarks/urls.py", "bookmarks/exports.py", "bookmarks/__main__.py"):
        # ponytail: demo source paths; interactive skill selects relevant paths for other repos.
        if repo == "gvago/oss-maintainer-demo":
            source = read("codebase", "read-file", "--repo", repo, "--path", path, "--ref", "main", "--refresh")
            if not source.get("ok") or source.get("truncated") or source.get("content_truncated_upstream") or not source.get("content") or not re.fullmatch(r"[0-9a-f]{40}", source.get("sha", "")):
                raise ValueError("Incomplete current-main evidence")
            if current and source["sha"] != next(iter(current.values()))["sha"]:
                raise ValueError("Main changed during collection; retry")
            current[path] = source
    return {"repo": repo, "observed_at": datetime.now(timezone.utc).isoformat(),
            "prs": details, "issues": issue_rows, "history": history, "current_main": current}


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
        if not isinstance(action["pr_heads"], dict):
            raise ValueError("PR heads must be a mapping")
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
        lines += [f"<details><summary>{escape(a['id'])} · {escape(a['type'])}</summary>", "", a["rationale"], "", "Targets: " + ", ".join(a["targets"]), "", "Evidence:"]
        lines += ["- " + e for e in a["evidence"]]
        lines += ["", "Uncertainty: " + a["uncertainty"], "", "Draft reply:", "", "> " + a["draft"].replace("\n", "\n> "), "", "Observed PR heads: `" + json.dumps(a["pr_heads"], sort_keys=True) + "`", "", "</details>", ""]
    lines += ["## Data gaps", ""] + ["- " + gap for gap in packet["gaps"]]
    return "\n".join(lines) + "\n"


def render_html(packet: dict) -> str:
    validate(packet)
    cards = []
    for a in packet["actions"]:
        links = " · ".join(f'<a href="{escape(u, quote=True)}" target="_blank" rel="noopener">{escape(u.rsplit("/", 2)[-2] + " #" + u.rsplit("/", 1)[-1])}</a>' for u in a["targets"])
        evidence = "".join("<li>" + escape(e) + "</li>" for e in a["evidence"])
        cards.append(f'<details data-kind="{escape(a["type"])}"><summary><span class="badge">{escape(a["type"].replace("_", " "))}</span> <strong>{escape(a["id"])}</strong><span class="links">{links}</span></summary><div class="body"><p>{escape(a["rationale"])}</p><h3>Evidence</h3><ul>{evidence}</ul><p class="uncertain">{escape(a["uncertainty"])}</p><h3>Suggested reply</h3><pre>{escape(a["draft"])}</pre><button class="copy">Copy reply</button> <span class="status" role="status"></span><small>Observed heads: {escape(json.dumps(a["pr_heads"]))}</small></div></details>')
    kinds = sorted({a["type"] for a in packet["actions"]})
    filters = '<button data-filter="all" aria-pressed="true">All</button>' + "".join(f'<button data-filter="{escape(k)}" aria-pressed="false">{escape(k.replace("_", " "))}</button>' for k in kinds)
    gaps = "".join("<li>" + escape(g) + "</li>" for g in packet["gaps"])
    return """<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Maintainer inbox</title>
<style>body{background:#f5f6f9;color:#202936;font:16px/1.55 system-ui;margin:0}main{max-width:1060px;margin:40px auto;padding:0 24px}h1{font-size:42px;letter-spacing:-1.5px;margin:4px 0}header{border-left:5px solid #6b46c1;padding-left:22px}.eyebrow{color:#6344a1;text-transform:uppercase;letter-spacing:2px;font-size:12px;font-weight:700}nav{display:flex;gap:8px;flex-wrap:wrap;margin:28px 0}button{font:inherit;border:1px solid #cbd0da;background:white;color:#283446;border-radius:7px;padding:8px 12px;cursor:pointer}button[aria-pressed=true]{background:#3f2a70;color:white}details{background:white;border:1px solid #d9dee7;border-radius:10px;margin:12px 0;overflow:hidden}summary{cursor:pointer;padding:18px}.badge{color:#4b3979;background:#f0eafa;border-radius:5px;padding:4px 8px;font-size:12px;text-transform:uppercase;margin-right:10px}.links{float:right;font-size:14px}a{color:#31559b}.body{padding:0 22px 22px;border-top:1px solid #e5e8ee}h3{font-size:14px;text-transform:uppercase;letter-spacing:1px;margin-top:24px}.uncertain{border-left:3px solid #c48931;padding-left:14px;color:#65502f}pre{white-space:pre-wrap;font:inherit;background:#f7f8fb;border:1px solid #e5e8ee;padding:16px;border-radius:8px}small{display:block;margin-top:18px;overflow-wrap:anywhere;color:#647084}.notice{color:#647084}li{margin-bottom:8px}@media(max-width:650px){.links{float:none;display:block;margin-top:10px}h1{font-size:32px}main{padding:0 16px}}</style><main><header><div class="eyebrow">Maintainer decision packet</div><h1>Less backlog. Clear next steps.</h1><p>""" + escape(packet["repo"]) + "</p><p>" + escape(packet["summary"]) + '</p><p class="notice">Proposed only · No changes applied · Refresh evidence before acting</p></header><nav aria-label="Filter recommendations">' + filters + '</nav>' + "".join(cards) + '<details><summary>Data gaps &amp; limitations</summary><div class="body"><ul>' + gaps + "</ul></div></details></main>" + """<script>document.querySelectorAll('[data-filter]').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('[data-filter]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));document.querySelectorAll('[data-kind]').forEach(d=>d.hidden=b.dataset.filter!=='all'&&d.dataset.kind!==b.dataset.filter)}));document.querySelectorAll('.copy').forEach(b=>b.addEventListener('click',async()=>{try{await navigator.clipboard.writeText(b.parentElement.querySelector('pre').textContent);b.nextElementSibling.textContent='Copied'}catch(e){b.nextElementSibling.textContent='Select the reply above to copy'}}));</script></html>"""


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
    (args.out / "maintainer-inbox.html").write_text(render_html(packet))
    print(f"Wrote proposed actions and inbox to {args.out.resolve()}")


if __name__ == "__main__":
    main()
