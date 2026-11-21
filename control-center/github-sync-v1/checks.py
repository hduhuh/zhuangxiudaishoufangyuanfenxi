#!/usr/bin/env python3
"""Local/CI validation of task scope, source pins and protocol package."""
import argparse
import fnmatch
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path, PurePosixPath

PACKAGE = "control-center/github-sync-v1"
TOOLS = {"Codex", "Muse", "Grok", "OpenClaw", "Cursor", "Rork", "WorkBuddy"}
SECRET = re.compile(
    r"(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|"
    r"-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----|https?://[^\s/@:]+:[^\s/@]+@)"
)


def task_errors(task, repo=None, branch=None):
    errors = []
    for name in ["task_id", "project", "repo", "issue", "target_version",
                 "branch", "primary_executor", "scope", "allowed_paths",
                 "validation", "risk", "rollback", "required_docs"]:
        if not task.get(name):
            errors.append("MISSING_TASK_FIELD:" + name)
    if task.get("primary_executor") not in TOOLS:
        errors.append("INVALID_EXECUTOR")
    if task.get("branch") in {"main", "master"}:
        errors.append("PROTECTED_BRANCH")
    if repo and task.get("repo") != repo:
        errors.append("TASK_REPOSITORY_MISMATCH")
    if branch and task.get("branch") != branch:
        errors.append("TASK_BRANCH_MISMATCH")
    if task.get("production_changes") is not False or task.get("merge_authorized") is not False:
        errors.append("PRODUCTION_OR_MERGE_NOT_ALLOWED")
    if not isinstance(task.get("allowed_paths"), list):
        errors.append("INVALID_ALLOWED_PATHS")
    if not isinstance(task.get("required_docs"), list):
        errors.append("REQUIRED_DOCUMENTATION_NOT_DECLARED")
    elif task.get("required_docs"):
        for name in task["required_docs"]:
            if not isinstance(name, str) or ".." in PurePosixPath(name).parts or PurePosixPath(name).is_absolute():
                errors.append("INVALID_REQUIRED_DOCUMENTATION_PATH")
    return errors


def path_errors(paths, allowed):
    errors = []
    for name in paths:
        p = PurePosixPath(name)
        if p.is_absolute() or ".." in p.parts:
            errors.append("UNSAFE_PATH:" + name)
        if (p.name.startswith(".env") and p.name not in {".env.example", ".env.sample"}) or \
                p.suffix.lower() in {".pem", ".p12", ".key"} or \
                any(s in p.parts for s in [".git", "private-evidence", "node_modules"]):
            errors.append("SENSITIVE_PATH:" + name)
        if not any(fnmatch.fnmatchcase(name, pattern) for pattern in allowed):
            errors.append("OUTSIDE_TASK_SCOPE:" + name)
    return errors


def validate(root, event=None):
    errors = []
    package = root / PACKAGE
    manifest = json.loads((package / "BUNDLE.json").read_text())
    if manifest.get("authority_repo") != "hduhuh/ziwo-ai-os":
        errors.append("AUTHORITY_MISMATCH")
    mode = manifest.get("mode")
    if mode == "reference":
        if not re.fullmatch(r"[0-9a-f]{40}", manifest.get("authority_commit", "")):
            errors.append("UNPINNED_AUTHORITY")
    elif mode != "authority":
        errors.append("INVALID_BUNDLE_MODE")
    for relative, expected in manifest["files"].items():
        p = root / relative
        if PurePosixPath(relative).is_absolute() or ".." in PurePosixPath(relative).parts:
            errors.append("UNSAFE_BUNDLE_PATH")
            continue
        if not p.is_file() or p.is_symlink():
            errors.append("MISSING_OR_SYMLINK_FILE:" + relative)
            continue
        if hashlib.sha256(p.read_bytes()).hexdigest() != expected:
            errors.append("BUNDLE_HASH_MISMATCH:" + relative)
    agents = (root / "AGENTS.md").read_text()
    if agents.count("<!-- ZIWO_GITHUB_GOVERNANCE:BEGIN -->") != 1 or \
            agents.count("<!-- ZIWO_GITHUB_GOVERNANCE:END -->") != 1:
        errors.append("MISSING_OR_DUPLICATE_AGENTS_BLOCK")
    tasks = sorted((package / "tasks").glob("*.json"))
    if not tasks:
        errors.append("NO_TASK_RECORD")
    for p in tasks:
        errors.extend(f"{p.name}:{e}" for e in task_errors(json.loads(p.read_text())))
    if event and event.get("pull_request"):
        pr = event["pull_request"]
        head, base = pr["head"]["sha"], pr["base"]["sha"]
        repo, branch = pr["base"]["repo"]["full_name"], pr["head"]["ref"]
        if branch in {"main", "master", pr["base"]["repo"]["default_branch"]}:
            errors.append("PROTECTED_BRANCH")
        if not pr.get("draft"):
            errors.append("DRAFT_REQUIRED")
        result = subprocess.run(["git", "diff", "--name-only", "-z", f"{base}...{head}"],
                                cwd=root, capture_output=True, check=True)
        changed = [p for p in result.stdout.decode().split("\0") if p]
        changed_tasks = [p for p in changed if p.startswith(PACKAGE + "/tasks/") and p.endswith(".json")]
        if not changed_tasks:
            errors.append("CHANGED_TASK_RECORD_REQUIRED")
        owners = set()
        allowed = []
        for p in changed_tasks:
            if not (root / p).is_file():
                errors.append("TASK_RECORD_REMOVED:" + p)
                continue
            task = json.loads((root / p).read_text())
            errors.extend(task_errors(task, repo, branch))
            owners.add(task.get("primary_executor"))
            allowed.extend(task.get("allowed_paths", []))
        if len(owners) != 1:
            errors.append("ONE_PRIMARY_EXECUTOR_REQUIRED")
        errors.extend(path_errors(changed, allowed))
        for p in changed_tasks:
            if (root / p).is_file():
                for name in json.loads((root / p).read_text()).get("required_docs", []):
                    if name not in changed:
                        errors.append("DOCUMENTATION_NOT_UPDATED:" + name)
        for p in changed:
            f = root / p
            if f.is_file() and f.stat().st_size < 2_000_000:
                if SECRET.search(f.read_text(errors="replace")):
                    errors.append("CREDENTIAL_PATTERN:" + p)
    return errors


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=Path.cwd())
    p.add_argument("--event", type=Path)
    args = p.parse_args()
    event = json.loads(args.event.read_text()) if args.event else None
    try:
        errors = validate(args.root.resolve(), event)
    except (KeyError, ValueError, OSError, subprocess.CalledProcessError) as exc:
        errors = ["VALIDATION_UNAVAILABLE:" + type(exc).__name__]
    print(json.dumps({"status": "PASS" if not errors else "FAIL", "errors": errors}, ensure_ascii=False))
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
