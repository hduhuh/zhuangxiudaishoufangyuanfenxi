#!/usr/bin/env python3
"""Read-only Git/GitHub delivery audit. Empty or stale CI never passes."""
import argparse
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

TOOLS = {"Codex", "Muse", "Grok", "OpenClaw", "Cursor", "Rork", "WorkBuddy"}
PACKAGE = "control-center/github-sync-v1"


def run(args, cwd=None):
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=45)
    if p.returncode:
        # Do not echo arbitrary CLI stderr, which can include credentials.
        raise RuntimeError(f"{args[0]} read-only command failed (exit {p.returncode})")
    return p.stdout.strip()


def api(endpoint, paginate=False):
    args = ["gh", "api", endpoint]
    if paginate:
        args += ["--paginate", "--slurp"]
    return json.loads(run(args))


def latest_checks(checks):
    latest = {}
    for c in checks:
        key = (c.get("app", {}).get("id"), c["name"])
        if key not in latest or c["id"] > latest[key]["id"]:
            latest[key] = c
    return list(latest.values())


def assess(snapshot, repo, branch, sha, pr_number, required_checks, expected_base=None):
    errors = []
    if not re.fullmatch(r"[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+", repo):
        errors.append("INVALID_REPOSITORY")
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        errors.append("FULL_COMMIT_SHA_REQUIRED")
    if branch in {"main", "master", snapshot["default_branch"]}:
        errors.append("PROTECTED_BRANCH")
    if snapshot["remote_sha"] != sha:
        errors.append("REMOTE_SHA_MISMATCH")
    pr = snapshot["pr"]
    if pr.get("number") != pr_number:
        errors.append("PR_NUMBER_MISMATCH")
    if pr.get("state") != "open" or not pr.get("draft"):
        errors.append("OPEN_DRAFT_PR_REQUIRED")
    if pr.get("head", {}).get("ref") != branch or pr.get("head", {}).get("sha") != sha:
        errors.append("PR_HEAD_MISMATCH")
    if pr.get("head", {}).get("repo", {}).get("full_name") != repo:
        errors.append("PR_HEAD_REPOSITORY_MISMATCH")
    if pr.get("base", {}).get("repo", {}).get("full_name") != repo:
        errors.append("PR_BASE_REPOSITORY_MISMATCH")
    if pr.get("base", {}).get("ref") != (expected_base or snapshot["default_branch"]):
        errors.append("PR_BASE_BRANCH_MISMATCH")
    if pr.get("mergeable") is False:
        errors.append("PR_CONFLICT")
    elif pr.get("mergeable") is None:
        errors.append("PR_MERGEABILITY_PENDING")
    checks = latest_checks(snapshot["checks"])
    # A success from any source with the same name cannot hide another source's failure.
    for name in required_checks:
        matches = [c for c in checks if c["name"] == name]
        if not matches:
            errors.append("CI_NOT_CONFIGURED:" + name)
    for c in checks:
        if c.get("head_sha") != sha:
            errors.append("CI_WRONG_SHA:" + c["name"])
        if c.get("status") != "completed" or c.get("conclusion") != "success":
            errors.append("CI_NOT_PASSED:" + c["name"])
    statuses = {}
    for status in snapshot["statuses"]:  # REST statuses are newest first.
        statuses.setdefault(status["context"], status)
    for name, status in statuses.items():
        if status.get("state") != "success":
            errors.append("STATUS_NOT_PASSED:" + name)
    task = snapshot.get("task_record")
    if not task:
        errors.append("TASK_RECORD_MISSING")
    else:
        for field in ["issue", "target_version", "validation", "rollback", "required_docs"]:
            if not task.get(field):
                errors.append("TASK_FIELD_MISSING:" + field)
        if task.get("repo") != repo or task.get("branch") != branch:
            errors.append("TASK_IDENTITY_MISMATCH")
        for path in task.get("required_docs", []):
            if path not in snapshot.get("changed_files", []):
                errors.append("DOCUMENTATION_NOT_UPDATED:" + path)
    local = snapshot.get("local")
    if local:
        if local["head"] != sha or local["branch"] != branch:
            errors.append("LOCAL_HEAD_OR_BRANCH_MISMATCH")
        if local["dirty"]:
            errors.append("UNCOMMITTED_WORK")
        if local["unmerged"]:
            errors.append("UNRESOLVED_LOCAL_CONFLICTS")
        origin = local["origin"]
        accepted = {f"https://github.com/{repo}", f"https://github.com/{repo}.git",
                    f"git@github.com:{repo}.git", f"ssh://git@github.com/{repo}.git"}
        if origin not in accepted:
            errors.append("ORIGIN_MISMATCH")
        if not local["upstream"]:
            errors.append("UPSTREAM_NOT_CONFIGURED")
        if local["upstream"] != "origin/" + branch:
            errors.append("UPSTREAM_MISMATCH")
    return {
        "status": "DELIVERY_VERIFIED" if not errors else "INCOMPLETE",
        "errors": errors,
        "checks": [{"name": c["name"], "status": c.get("status"),
                    "conclusion": c.get("conclusion"), "sha": c.get("head_sha"),
                    "url": c.get("html_url")} for c in checks],
        "local": "CHECKED" if local else "LOCAL_NOT_APPLICABLE",
        "native_tool_attribution": "REQUIRES_SEPARATE_SESSION_EVIDENCE",
        "business_acceptance": "REQUIRES_TASK_TEST_EVIDENCE",
        "sync_backlog": [{"id": "DELIVERY-" + str(i + 1), "failure": e,
                          "status": "PENDING", "owner_role": "OpenClaw / designated executor"}
                         for i, e in enumerate(errors)],
    }


def collect(repo, branch, sha, number, local_repo=None, task_id=None):
    from urllib.parse import quote
    meta = api(f"repos/{repo}")
    ref = api(f"repos/{repo}/git/ref/heads/{quote(branch, safe='/')}")
    pr = api(f"repos/{repo}/pulls/{number}")
    pages = api(f"repos/{repo}/commits/{sha}/check-runs?per_page=100", True)
    statuses = api(f"repos/{repo}/commits/{sha}/statuses?per_page=100", True)
    snapshot = {
        "default_branch": meta["default_branch"], "remote_sha": ref["object"]["sha"],
        "pr": pr, "checks": [c for p in pages for c in p["check_runs"]],
        "statuses": [s for p in statuses for s in p],
    }
    if task_id:
        import base64
        try:
            item = api(f"repos/{repo}/contents/{PACKAGE}/tasks/{task_id}.json?ref={sha}")
            snapshot["task_record"] = json.loads(base64.b64decode(item["content"]))
        except RuntimeError:
            snapshot["task_record"] = None
        pages = api(f"repos/{repo}/pulls/{number}/files?per_page=100", True)
        snapshot["changed_files"] = [item["filename"] for page in pages for item in page]
    if local_repo:
        def git(*args):
            return run(["git", "--no-optional-locks", *args], cwd=local_repo)
        try:
            upstream = git("rev-parse", "--abbrev-ref", "@{upstream}")
        except RuntimeError:
            upstream = None
        snapshot["local"] = {
            "head": git("rev-parse", "HEAD"), "branch": git("branch", "--show-current"),
            "dirty": bool(git("status", "--porcelain=v1")),
            "unmerged": bool(git("ls-files", "-u")),
            "origin": git("remote", "get-url", "origin"), "upstream": upstream,
        }
    return snapshot


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ["repo", "branch", "commit", "tool", "task", "issue"]:
        p.add_argument("--" + name, required=True)
    p.add_argument("--pr", required=True, type=int)
    p.add_argument("--target-version", default="V1.0")
    p.add_argument("--base", help="Explicit task-approved PR base; defaults to repository default")
    p.add_argument("--check", action="append", required=True)
    p.add_argument("--local-repo", type=Path)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    if args.tool not in TOOLS:
        p.error("unregistered tool; update the existing tool map first")
    if not re.fullmatch(r"[0-9a-f]{40}", args.commit):
        p.error("a full lowercase Commit SHA is required")
    if not re.fullmatch(r"[\w.-]+/[\w.-]+", args.repo):
        p.error("invalid OWNER/REPO")
    if not re.fullmatch(r"[A-Za-z0-9_-]+", args.task):
        p.error("invalid task ID")
    try:
        snapshot = collect(args.repo, args.branch, args.commit, args.pr, args.local_repo, args.task)
        report = assess(snapshot, args.repo, args.branch, args.commit, args.pr, args.check, args.base)
        task = snapshot.get("task_record") or {}
        if task.get("primary_executor") != args.tool or task.get("issue") != args.issue:
            report["errors"].append("TASK_EXECUTOR_OR_ISSUE_MISMATCH")
            report["status"] = "INCOMPLETE"
        report["remote_sha"] = snapshot["remote_sha"]
        report["pr_url"] = snapshot["pr"]["html_url"]
    except (RuntimeError, KeyError, ValueError, OSError) as exc:
        report = {"status": "INCOMPLETE", "errors": [type(exc).__name__ + ":read audit unavailable"]}
    report.update(repo=args.repo, branch=args.branch, commit=args.commit, pr=args.pr,
                  tool=args.tool, task=args.task, issue=args.issue,
                  target_version=args.target_version,
                  checked_at=datetime.now(timezone.utc).isoformat())
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    print(text, end="")
    return 0 if report["status"] == "DELIVERY_VERIFIED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
