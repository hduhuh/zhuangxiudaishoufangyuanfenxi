import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / (name + ".py"))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


verify = module("verify_delivery")
checks = module("checks")
SHA = "a" * 40
REPO = "owner/repo"
BRANCH = "codex/test"


def snapshot():
    return {
        "default_branch": "main", "remote_sha": SHA,
        "pr": {"number": 1, "state": "open", "draft": True, "mergeable": True,
               "head": {"ref": BRANCH, "sha": SHA, "repo": {"full_name": REPO}},
               "base": {"ref": "main", "repo": {"full_name": REPO}}},
        "checks": [{"id": 1, "name": "ziwo-delivery-gate", "status": "completed",
                    "conclusion": "success", "head_sha": SHA, "app": {"id": 1}}],
        "statuses": [],
        "task_record": {"issue": "issue", "target_version": "V1", "validation": ["test"],
                        "rollback": "close PR", "required_docs": ["safe.md"], "repo": REPO, "branch": BRANCH},
        "changed_files": ["safe.md"],
        "local": {"head": SHA, "branch": BRANCH, "dirty": False, "unmerged": False,
                  "origin": "https://github.com/owner/repo.git", "upstream": "origin/" + BRANCH},
    }


class DeliveryTests(unittest.TestCase):
    def assess(self, data):
        return verify.assess(data, REPO, BRANCH, SHA, 1, ["ziwo-delivery-gate"])

    def test_complete_evidence_passes(self):
        self.assertEqual(self.assess(snapshot())["status"], "DELIVERY_VERIFIED")

    def test_empty_ci_fails(self):
        s = snapshot(); s["checks"] = []
        self.assertIn("CI_NOT_CONFIGURED:ziwo-delivery-gate", self.assess(s)["errors"])

    def test_old_sha_does_not_pass(self):
        s = snapshot(); s["checks"][0]["head_sha"] = "b" * 40
        self.assertIn("CI_WRONG_SHA:ziwo-delivery-gate", self.assess(s)["errors"])

    def test_remote_must_match(self):
        s = snapshot(); s["remote_sha"] = "b" * 40
        self.assertIn("REMOTE_SHA_MISMATCH", self.assess(s)["errors"])

    def test_pr_head_must_match(self):
        s = snapshot(); s["pr"]["head"]["sha"] = "b" * 40
        self.assertIn("PR_HEAD_MISMATCH", self.assess(s)["errors"])

    def test_draft_required(self):
        for state, draft in [("closed", True), ("open", False)]:
            s = snapshot(); s["pr"].update(state=state, draft=draft)
            self.assertIn("OPEN_DRAFT_PR_REQUIRED", self.assess(s)["errors"])

    def test_fork_is_not_target_branch(self):
        s = snapshot(); s["pr"]["head"]["repo"]["full_name"] = "other/repo"
        self.assertIn("PR_HEAD_REPOSITORY_MISMATCH", self.assess(s)["errors"])

    def test_unapproved_pr_base_rejected(self):
        s = snapshot(); s["pr"]["base"]["ref"] = "other"
        self.assertIn("PR_BASE_BRANCH_MISMATCH", self.assess(s)["errors"])
        r = verify.assess(s, REPO, BRANCH, SHA, 1, ["ziwo-delivery-gate"], expected_base="other")
        self.assertNotIn("PR_BASE_BRANCH_MISMATCH", r["errors"])

    def test_main_master_and_nonstandard_default_rejected(self):
        for branch, default in [("main", "main"), ("master", "main"), ("stable", "stable")]:
            s = snapshot(); s["default_branch"] = default
            r = verify.assess(s, REPO, branch, SHA, 1, ["ziwo-delivery-gate"])
            self.assertIn("PROTECTED_BRANCH", r["errors"])

    def test_dirty_and_no_upstream_fail(self):
        s = snapshot(); s["local"].update(dirty=True, upstream=None, unmerged=True)
        r = self.assess(s)
        for error in ["UNCOMMITTED_WORK", "UPSTREAM_NOT_CONFIGURED", "UNRESOLVED_LOCAL_CONFLICTS"]:
            self.assertIn(error, r["errors"])

    def test_wrong_origin_fails(self):
        s = snapshot(); s["local"]["origin"] = "https://github.com/other/repo"
        self.assertIn("ORIGIN_MISMATCH", self.assess(s)["errors"])

    def test_pending_failed_skipped_cancelled_never_pass(self):
        for conclusion in ["failure", "skipped", "cancelled", None, "neutral"]:
            s = snapshot(); s["checks"][0]["conclusion"] = conclusion
            self.assertIn("CI_NOT_PASSED:ziwo-delivery-gate", self.assess(s)["errors"])
        s = snapshot(); s["checks"][0]["status"] = "in_progress"
        self.assertNotEqual(self.assess(s)["status"], "DELIVERY_VERIFIED")

    def test_latest_rerun_overrides_old_green(self):
        s = snapshot()
        c = copy.deepcopy(s["checks"][0]); c.update(id=2, conclusion="failure")
        s["checks"].append(c)
        self.assertNotEqual(self.assess(s)["status"], "DELIVERY_VERIFIED")

    def test_failure_from_second_app_not_hidden(self):
        s = snapshot(); c = copy.deepcopy(s["checks"][0])
        c.update(id=2, conclusion="failure", app={"id": 2}); s["checks"].append(c)
        self.assertNotEqual(self.assess(s)["status"], "DELIVERY_VERIFIED")

    def test_status_context_failure_also_blocks(self):
        s = snapshot(); s["statuses"] = [{"context": "product", "state": "failure"}]
        self.assertIn("STATUS_NOT_PASSED:product", self.assess(s)["errors"])

    def test_missing_task_and_unupdated_docs_generate_backlog(self):
        s = snapshot(); s["changed_files"] = []
        report = self.assess(s)
        self.assertIn("DOCUMENTATION_NOT_UPDATED:safe.md", report["errors"])
        self.assertTrue(report["sync_backlog"])
        s.pop("task_record")
        self.assertIn("TASK_RECORD_MISSING", self.assess(s)["errors"])

    def test_new_status_overrides_old_failure(self):
        s = snapshot()
        s["statuses"] = [{"context": "product", "state": "success"}, {"context": "product", "state": "failure"}]
        self.assertEqual(self.assess(s)["status"], "DELIVERY_VERIFIED")

    def test_missing_or_unknown_mergeability_blocks(self):
        for value, error in [(False, "PR_CONFLICT"), (None, "PR_MERGEABILITY_PENDING")]:
            s = snapshot(); s["pr"]["mergeable"] = value
            self.assertIn(error, self.assess(s)["errors"])

    def test_web_only_source_explicit(self):
        s = snapshot(); s.pop("local")
        self.assertEqual(self.assess(s)["local"], "LOCAL_NOT_APPLICABLE")
        self.assertEqual(self.assess(s)["native_tool_attribution"], "REQUIRES_SEPARATE_SESSION_EVIDENCE")


class TaskScopeTests(unittest.TestCase):
    def task(self):
        return {
            "task_id": "T", "project": "P", "repo": REPO, "issue": "https://github.com/owner/repo/issues/1",
            "target_version": "V1", "branch": BRANCH, "primary_executor": "Codex", "scope": "rules",
            "allowed_paths": ["rules/**"], "validation": [{"command": "unit", "result": "PASS"}],
            "risk": "none known", "rollback": "close PR", "production_changes": False, "merge_authorized": False,
            "required_docs": ["rules/progress.md"],
        }

    def test_complete_task(self):
        self.assertEqual(checks.task_errors(self.task(), REPO, BRANCH), [])

    def test_no_issue_or_version_fails(self):
        for name in ["issue", "target_version", "validation", "rollback"]:
            task = self.task(); task.pop(name)
            self.assertIn("MISSING_TASK_FIELD:" + name, checks.task_errors(task))

    def test_wrong_repo_or_branch_fails(self):
        self.assertIn("TASK_REPOSITORY_MISMATCH", checks.task_errors(self.task(), "wrong/repo"))
        self.assertIn("TASK_BRANCH_MISMATCH", checks.task_errors(self.task(), branch="other"))

    def test_unknown_tool_fails(self):
        task = self.task(); task["primary_executor"] = "unknown"
        self.assertIn("INVALID_EXECUTOR", checks.task_errors(task))

    def test_production_or_merge_flag_fails(self):
        for key in ["production_changes", "merge_authorized"]:
            task = self.task(); task[key] = True
            self.assertIn("PRODUCTION_OR_MERGE_NOT_ALLOWED", checks.task_errors(task))

    def test_outside_scope(self):
        self.assertIn("OUTSIDE_TASK_SCOPE:app.js", checks.path_errors(["app.js"], ["rules/**"]))

    def test_secrets_and_private_paths(self):
        for path in [".env", ".env.production", "a/key.pem", "private-evidence/photo.jpg", "a/secret.key"]:
            self.assertIn("SENSITIVE_PATH:" + path, checks.path_errors([path], ["*"]))

    def test_traversal_rejected(self):
        self.assertIn("UNSAFE_PATH:../outside", checks.path_errors(["../outside"], ["*"]))

    def test_example_env_allowed_only_in_scope(self):
        self.assertEqual(checks.path_errors([".env.example"], [".env.example"]), [])



if __name__ == "__main__":
    unittest.main()
