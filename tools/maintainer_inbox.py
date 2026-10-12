"""Read-only Qodo context collection and agent-generated maintainer artifacts."""
import argparse
import json
from html import escape
from pathlib import Path
import re
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


def validate(packet: dict) -> None:
    if not isinstance(packet.get("repo"), str) or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", packet["repo"]) or not isinstance(packet.get("summary"), str):
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
    def literal(text: str) -> str:
        return "<p>" + escape(text).replace("\n", "<br>\n") + "</p>"

    lines = ["# Maintainer Inbox", "", literal(packet.get("coverage", "Coverage unavailable for this legacy packet.")), "", literal(packet["summary"]), "", "All actions below are proposed, not approved or applied.", ""]
    for a in packet["actions"]:
        lines += [f"<details><summary>{escape(a['id'])} · {escape(a['type'])}</summary>", "", literal(a["rationale"]), "", "Targets: " + ", ".join(a["targets"]), "", "Evidence:"]
        lines += [literal(e) for e in a["evidence"]]
        lines += ["", "Uncertainty:", literal(a["uncertainty"]), "", "Draft reply:", literal(a["draft"]), "", "Observed PR heads:", literal(json.dumps(a["pr_heads"], sort_keys=True)), "", "</details>", ""]
    lines += ["## Data gaps", ""] + [literal(gap) for gap in packet["gaps"]]
    return "\n".join(lines).rstrip() + "\n"


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
<style>body{background:#f5f6f9;color:#202936;font:16px/1.55 system-ui;margin:0}*{box-sizing:border-box}body{overflow-wrap:anywhere}main{min-width:0;max-width:1060px;margin:40px auto;padding:0 24px}h1{font-size:42px;letter-spacing:-1.5px;margin:4px 0}header{border-left:5px solid #6b46c1;padding-left:22px}.eyebrow{color:#6344a1;text-transform:uppercase;letter-spacing:2px;font-size:12px;font-weight:700}nav{display:flex;gap:8px;flex-wrap:wrap;margin:28px 0}button{font:inherit;border:1px solid #cbd0da;background:white;color:#283446;border-radius:7px;padding:8px 12px;cursor:pointer}button[aria-pressed=true]{background:#3f2a70;color:white}details{background:white;border:1px solid #d9dee7;border-radius:10px;margin:12px 0;overflow:hidden}summary{cursor:pointer;padding:18px}.badge{color:#4b3979;background:#f0eafa;border-radius:5px;padding:4px 8px;font-size:12px;text-transform:uppercase;margin-right:10px}.links{float:right;font-size:14px}a{color:#31559b}.body{padding:0 22px 22px;border-top:1px solid #e5e8ee}h3{font-size:14px;text-transform:uppercase;letter-spacing:1px;margin-top:24px}.uncertain{border-left:3px solid #c48931;padding-left:14px;color:#65502f}pre{overflow-wrap:anywhere;white-space:pre-wrap;font:inherit;background:#f7f8fb;border:1px solid #e5e8ee;padding:16px;border-radius:8px}small{display:block;margin-top:18px;overflow-wrap:anywhere;color:#647084}.notice{color:#647084}li{margin-bottom:8px}@media(max-width:650px){.links{float:none;display:block;margin-top:10px}h1{font-size:32px}main{padding:0 16px}}</style><main><header><div class="eyebrow">Maintainer decision packet</div><h1>Less backlog. Clear next steps.</h1><p>""" + escape(packet["repo"]) + "</p><p>" + escape(packet.get("coverage", "Coverage unavailable")) + "</p><p>" + escape(packet["summary"]) + '</p><p class="notice">Proposed only · No changes applied · Refresh evidence before acting</p></header><nav aria-label="Filter recommendations">' + filters + '</nav>' + "".join(cards) + '<details><summary>Data gaps &amp; limitations</summary><div class="body"><ul>' + gaps + "</ul></div></details></main>" + """<script>document.querySelectorAll('[data-filter]').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('[data-filter]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));document.querySelectorAll('[data-kind]').forEach(d=>d.hidden=b.dataset.filter!=='all'&&d.dataset.kind!==b.dataset.filter)}));document.querySelectorAll('.copy').forEach(b=>b.addEventListener('click',async()=>{try{await navigator.clipboard.writeText(b.parentElement.querySelector('pre').textContent);b.nextElementSibling.textContent='Copied'}catch(e){b.nextElementSibling.textContent='Select the reply above to copy'}}));</script></html>"""


def bind_evidence(packet: dict, evidence: dict) -> None:
    calls = evidence["calls"]
    for tool, key in [("litegit-list-prs", "pull_requests"), ("litegit-list-issues", "issues")]:
        discovered = [c["result"] for c in calls if c["tool"] == tool and c["arguments"] == {"repo": packet["repo"], "state": "open", "max_results": 200}]
        if not discovered or discovered[-1].get("truncated") or not isinstance(discovered[-1].get(key), list) or len(discovered[-1][key]) >= 200:
            raise ValueError("Missing or incomplete open backlog discovery")
    prs = next(c["result"]["pull_requests"] for c in reversed(calls) if c["tool"] == "litegit-list-prs" and c["arguments"] == {"repo": packet["repo"], "state": "open", "max_results": 200})
    issues = next(c["result"]["issues"] for c in reversed(calls) if c["tool"] == "litegit-list-issues" and c["arguments"] == {"repo": packet["repo"], "state": "open", "max_results": 200})
    validate(packet)
    heads = {f"https://github.com/{packet['repo']}/pull/{p['number']}": p.get("head_sha", p.get("head_commit")) for p in prs}
    open_issues = {f"https://github.com/{packet['repo']}/issues/{i['number']}" for i in issues}
    for action in packet["actions"]:
        if any("/issues/" in url and url not in open_issues for url in action["targets"]):
            raise ValueError("Recommendation targets an unobserved open issue")
        for url, sha in action["pr_heads"].items():
            if url not in heads or sha != heads[url]:
                raise ValueError("Recommendation head differs from observed PR")
    if not any(c["tool"] == "get-pr-review-findings" for c in calls):
        raise ValueError("No Qodo review context retrieved")
    if not any(c["tool"].startswith("pull-request-") for c in calls):
        raise ValueError("No Qodo history context retrieved")
    validate(packet)
    packet["coverage"] = f"{len(prs)} open PRs · {len(issues)} open issues · Observed {evidence['observed_at']}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default="gvago/oss-maintainer-demo")
    parser.add_argument("--out", type=Path, default=Path("maintainer-output"))
    parser.add_argument("--render", type=Path, help="Render a recorded packet without retrieval")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", args.repo):
        parser.error("Expected owner/repo")
    args.out.mkdir(parents=True, exist_ok=True)
    if args.render:
        packet = decode(args.render.read_text())
    else:
        evidence_path = (args.out / "evidence.json").resolve()
        if evidence_path.exists():
            raise ValueError("Use a fresh output directory for each run")
        mcp = {"mcpServers": {"qodo": {"command": "python3", "args": [str(ROOT / "tools/qodo_read_mcp.py"), "--repo", args.repo, "--evidence", str(evidence_path)]}}}
        prompt = (ROOT / "maintainer-inbox/prompt.md").read_text() + "\nRepository: " + args.repo
        raw = run(["claude", "-p", "--tools", "", "--strict-mcp-config", "--mcp-config", json.dumps(mcp), "--allowedTools", "mcp__qodo__*", "--permission-mode", "dontAsk", "--output-format", "json", "--json-schema", (ROOT / "maintainer-inbox/schema.json").read_text()], stdin=prompt, timeout=1200)
        result = decode(raw)
        if result.get("is_error") or result.get("permission_denials"):
            raise ValueError("Agent failed or was denied a tool; do not publish partial success")
        packet = result.get("structured_output") or decode(result["result"])
        if packet.get("repo") != args.repo:
            raise ValueError("Agent changed repository identity")
        evidence = decode(evidence_path.read_text())
        bind_evidence(packet, evidence)
    (args.out / "maintainer-actions.json").write_text(json.dumps(packet, indent=2) + "\n")
    (args.out / "maintainer-inbox.md").write_text(render(packet))
    (args.out / "maintainer-inbox.html").write_text(render_html(packet))
    print(f"Wrote proposed actions and inbox to {args.out.resolve()}")


if __name__ == "__main__":
    main()
