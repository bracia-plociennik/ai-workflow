#!/usr/bin/env python3
"""Exercise real branch identities, index blobs and detached CI boundaries."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[3]
ENV = {key: value for key, value in os.environ.items()
       if not key.startswith(("GITHUB_", "AI_WORKFLOW_", "GIT_"))}


class BranchPolicyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="branch-policy-")
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name) / "official"
        self.setup_repo(self.repo)

    def git(self, *args, repo=None):
        return subprocess.check_output(["git", "-C", str(repo or self.repo), *args], env=ENV).decode().strip()

    def setup_repo(self, repo):
        repo.mkdir(parents=True)
        self.git("init", "-q", "-b", "main", repo=repo)
        self.git("config", "user.name", "Synthetic Fixture", repo=repo)
        self.git("config", "user.email", "fixture@example.invalid", repo=repo)
        self.git("remote", "add", "origin", "https://github.com/bracia-plociennik/ai-workflow.git", repo=repo)
        for raw in (".systems/scripts/check-branch-policy", ".systems/scripts/check-workspace-publication",
                    ".systems/scripts/lib/workspace-publication.py"):
            target = repo / raw
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(SOURCE / raw, target)
        self.git("add", ".systems", repo=repo)
        self.git("commit", "-qm", "fixture source", repo=repo)

    def snapshot(self, repo=None):
        repo = repo or self.repo
        raw = "ai-workflow-workspace/repo/core/example.md"
        path = repo / raw
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# Synthetic runtime\n", encoding="utf-8")
        review = repo / "ai-workflow-workspace/repo/publication-review.json"
        review.write_text(json.dumps({"schema": 1, "privacy_review": "completed", "reviewed_at": "2026-10-08",
                                      "source_head": self.git("rev-parse", "HEAD", repo=repo),
                                      "quality_authority": "supporting-only",
                                      "files": {raw: hashlib.sha256(path.read_bytes()).hexdigest()}}))
        self.git("add", "ai-workflow-workspace", repo=repo)
        return path

    def check(self, ok, repo=None, diagnostic=None, **extra):
        repo = repo or self.repo
        result = subprocess.run([str(repo / ".systems/scripts/check-branch-policy")],
                                env={**ENV, **extra}, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0 if ok else 1, result.stdout + result.stderr)
        if diagnostic:
            self.assertIn(diagnostic, result.stdout + result.stderr)

    def dev(self):
        self.git("switch", "-qc", "dev")

    def test_main_and_overrides_reject(self):
        self.snapshot()
        for policy in ("auto", "dev", "public"):
            self.check(False, AI_WORKFLOW_BRANCH_POLICY=policy, GITHUB_REF_NAME="dev",
                       GITHUB_BASE_REF="dev", diagnostic="Branch policy violation")

    def test_dev_accepts_only_reviewed_index(self):
        self.dev()
        path = self.snapshot()
        self.check(True)
        self.check(True, AI_WORKFLOW_BRANCH_POLICY="dev")
        self.check(False, AI_WORKFLOW_BRANCH_POLICY="public")
        path.write_text("# Changed after review\n")
        self.check(True)  # Worktree modifications are not the staged publication.
        self.git("add", "ai-workflow-workspace")
        self.check(False, diagnostic="inventory/hash mismatch")

    def test_feature_and_unknown_branch_reject(self):
        self.git("switch", "-qc", "codex/example")
        self.snapshot()
        self.check(False, AI_WORKFLOW_BRANCH_POLICY="dev")
        self.git("commit", "-qm", "synthetic runtime")
        self.git("checkout", "-q", "--detach")
        self.check(False, AI_WORKFLOW_BRANCH_POLICY="dev", GITHUB_REF_NAME="dev")

    def ci_env(self):
        return {"GITHUB_ACTIONS": "true", "GITHUB_REPOSITORY": "bracia-plociennik/ai-workflow",
                "GITHUB_SHA": self.git("rev-parse", "HEAD"), "GITHUB_EVENT_NAME": "push",
                "GITHUB_REF": "refs/heads/dev", "GITHUB_REF_NAME": "dev"}

    def test_detached_actions_context(self):
        self.dev()
        self.snapshot()
        self.git("commit", "-qm", "synthetic runtime")
        self.git("checkout", "-q", "--detach")
        context = self.ci_env()
        self.check(True, **context)
        for update in ({"GITHUB_SHA": "0" * 40}, {"GITHUB_REPOSITORY": "other/repo"},
                       {"GITHUB_REF": "refs/tags/dev"}, {"GITHUB_EVENT_NAME": "pull_request_target"}):
            self.check(False, **{**context, **update})
        self.check(False, **{**context, "GITHUB_EVENT_NAME": "pull_request", "GITHUB_BASE_REF": "dev",
                            "GITHUB_REF": "refs/pull/12/merge", "GITHUB_REF_NAME": "12/merge"})
        self.check(False, **{**context, "GITHUB_EVENT_NAME": "pull_request", "GITHUB_BASE_REF": "main",
                             "GITHUB_REF": "refs/pull/12/merge"})

    def test_local_identity_and_pr_destination(self):
        self.dev()
        self.snapshot()
        self.check(False, GITHUB_BASE_REF="main", GITHUB_HEAD_REF="dev")
        self.check(False, AI_WORKFLOW_MODE="target")

    def linked_worker(self):
        self.dev()
        self.snapshot()
        self.git("commit", "-qm", "reviewed dev snapshot")
        worker = Path(self.tmp.name) / "worker"
        self.git("worktree", "add", "-qb", "codex/worker", str(worker), "dev")
        return worker

    def test_linked_dev_worker_inherits_only_unchanged_index(self):
        worker = self.linked_worker()
        self.check(True, repo=worker)
        product = worker / ".systems/product.txt"
        product.write_text("reviewed product\n")
        self.git("add", ".systems/product.txt", repo=worker)
        self.git("commit", "-qm", "product only", repo=worker)
        self.check(True, repo=worker)
        # Even a refreshed publication review cannot authorize worker runtime.
        path = worker / "ai-workflow-workspace/repo/core/new.md"
        path.write_text("new synthetic runtime\n")
        review = worker / "ai-workflow-workspace/repo/publication-review.json"
        inventory = json.loads(review.read_text())
        inventory["files"][str(path.relative_to(worker))] = hashlib.sha256(path.read_bytes()).hexdigest()
        review.write_text(json.dumps(inventory))
        self.git("add", "ai-workflow-workspace", repo=worker)
        self.check(False, repo=worker, diagnostic="inherited dev workspace must remain unchanged")

    def test_linked_worker_cannot_remove_entire_snapshot(self):
        worker = self.linked_worker()
        self.git("rm", "-qrf", "ai-workflow-workspace", repo=worker)
        self.check(False, repo=worker, diagnostic="inherited dev workspace must remain unchanged")

    def test_reverted_workspace_commit_still_rejects_worker_and_pr(self):
        worker = self.linked_worker()
        runtime = worker / "ai-workflow-workspace/repo/core/example.md"
        runtime.write_text("changed runtime\n")
        self.git("add", "ai-workflow-workspace", repo=worker)
        self.git("commit", "-qm", "runtime change", repo=worker)
        self.git("revert", "--no-edit", "HEAD", repo=worker)
        self.assertEqual(self.git("diff", "dev", "HEAD", "--", "ai-workflow-workspace", repo=worker), "")
        self.check(False, repo=worker, diagnostic="including commit history")
        self.git("merge", "--no-ff", "-qm", "synthetic PR", "codex/worker")
        self.git("checkout", "-q", "--detach")
        context = {**self.ci_env(), "GITHUB_EVENT_NAME": "pull_request",
                   "GITHUB_BASE_REF": "dev", "GITHUB_REF": "refs/pull/12/merge"}
        self.check(False, diagnostic="including commit history", **context)

    def test_primary_codex_snapshot_is_not_linked_inheritance(self):
        self.dev()
        self.snapshot()
        self.git("commit", "-qm", "snapshot")
        self.git("switch", "-qc", "codex/primary")
        self.check(False)

    def test_linked_worker_guards_and_stale_dev(self):
        worker = self.linked_worker()
        self.check(False, repo=worker, AI_WORKFLOW_BRANCH_POLICY="public")
        self.check(False, repo=worker, AI_WORKFLOW_MODE="target")
        self.check(False, repo=worker, GITHUB_BASE_REF="main")
        self.git("remote", "set-url", "origin", "https://github.com/other/repo.git")
        self.check(False, repo=worker)
        self.git("remote", "set-url", "origin", "https://github.com/bracia-plociennik/ai-workflow.git")
        self.git("commit", "--allow-empty", "-qm", "advanced dev")
        self.check(False, repo=worker)

    def test_linked_non_dev_ancestor_rejects_copied_snapshot(self):
        self.dev()
        self.snapshot()
        self.git("commit", "-qm", "snapshot")
        worker = Path(self.tmp.name) / "worker"
        self.git("worktree", "add", "-qb", "codex/worker", str(worker), "main")
        self.snapshot(worker)
        self.check(False, repo=worker)

    def test_verified_pr_dev_requires_unchanged_first_parent_workspace(self):
        worker = self.linked_worker()
        product = worker / ".systems/product.txt"
        product.write_text("product\n")
        self.git("add", ".systems/product.txt", repo=worker)
        self.git("commit", "-qm", "product", repo=worker)
        self.git("merge", "--no-ff", "-qm", "synthetic PR", "codex/worker")
        self.git("checkout", "-q", "--detach")
        context = {**self.ci_env(), "GITHUB_EVENT_NAME": "pull_request",
                   "GITHUB_BASE_REF": "dev", "GITHUB_REF": "refs/pull/12/merge"}
        self.check(True, **context)
        self.check(False, **{**context, "GITHUB_BASE_REF": "main"})
        self.git("rm", "-qf", "ai-workflow-workspace/repo/core/example.md")
        self.check(False, diagnostic="inherited dev workspace must remain unchanged", **context)
        self.git("rm", "-qrf", "ai-workflow-workspace")
        self.check(False, diagnostic="inherited dev workspace must remain unchanged", **context)

    def test_filtered_publication_excludes_runtime_history(self):
        worker = self.linked_worker()
        source = worker / ".systems/product.txt"
        source.write_text("completed product\n")
        self.git("add", ".systems/product.txt", repo=worker)
        self.git("commit", "-qm", "product", repo=worker)
        product_commit = self.git("rev-parse", "HEAD", repo=worker)
        dev_commit = self.git("rev-parse", "dev")
        self.git("switch", "-qc", "codex/release", "main")
        self.git("cherry-pick", product_commit)
        self.assertEqual(self.git("ls-files", "ai-workflow-workspace"), "")
        ancestry = subprocess.run(["git", "-C", str(self.repo), "merge-base", "--is-ancestor",
                                   dev_commit, "HEAD"], env=ENV)
        self.assertEqual(ancestry.returncode, 1)
        self.check(True)

    def test_nested_dev_rejects_even_official_override(self):
        parent = Path(self.tmp.name) / "target"
        parent.mkdir()
        self.git("init", "-q", repo=parent)
        nested = parent / "ai-workflow"
        self.setup_repo(nested)
        self.git("switch", "-qc", "dev", repo=nested)
        self.snapshot(nested)
        self.check(False, repo=nested, AI_WORKFLOW_MODE="official", AI_WORKFLOW_BRANCH_POLICY="dev")

    def test_legacy_stays_forbidden(self):
        self.dev()
        path = self.repo / "workspace/runtime.md"
        path.parent.mkdir()
        path.write_text("legacy\n")
        self.git("add", "workspace")
        self.check(False, diagnostic="legacy workspace files")

    def test_other_repository_rejects_dev_exception(self):
        self.dev()
        self.snapshot()
        self.git("remote", "set-url", "origin", "https://github.com/other/repo.git")
        self.check(False, AI_WORKFLOW_MODE="official", AI_WORKFLOW_BRANCH_POLICY="dev")

    def test_missing_review_and_secret_reject(self):
        self.dev()
        path = self.snapshot()
        self.git("rm", "-qf", "ai-workflow-workspace/repo/publication-review.json")
        self.check(False, diagnostic="missing workspace publication review")
        path.write_text("ghp_" + "a" * 36)
        self.git("add", "ai-workflow-workspace")
        self.check(False, diagnostic="credential pattern")

    def test_symlink_and_gitlink_reject(self):
        self.dev()
        path = self.snapshot()
        link = path.parent / "link.md"
        link.symlink_to("example.md")
        self.git("add", "ai-workflow-workspace")
        self.check(False, diagnostic="non-regular")
        self.git("rm", "-qf", str(link.relative_to(self.repo)))
        link.unlink(missing_ok=True)
        self.git("update-index", "--add", "--cacheinfo", "160000," + self.git("rev-parse", "HEAD")
                 + ",ai-workflow-workspace/nested")
        self.check(False, diagnostic="non-regular")

    def test_cache_and_env_reject(self):
        self.dev()
        path = self.snapshot()
        bad = path.parent / ".env"
        bad.write_text("SYNTHETIC=1\n")
        self.git("add", "ai-workflow-workspace")
        self.check(False, diagnostic="forbidden workspace publication path")

    def test_committed_inventory_and_no_workspace(self):
        self.check(True)
        self.dev()
        self.snapshot()
        self.git("commit", "-qm", "reviewed snapshot")
        result = subprocess.run([str(self.repo / ".systems/scripts/check-workspace-publication"), "--ref", "HEAD"],
                                env=ENV, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
