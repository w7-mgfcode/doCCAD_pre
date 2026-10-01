#!/usr/bin/env python3
"""GitHub Approval Verifier (AD-9, ADR-005, E3).

Implements the two-step governance merge gate for production documentation publication:
1. Local claim verification:
   - Document claims approval_status: approved.
   - approval_record is present and contains {pr, approved_by, approved_at, approved_hash}.
   - The body sha256 matches approved_hash (detects post-approval edits; mismatch sends artifact back to in-review).
2. GitHub REST API gate verification:
   - PR `pr` is merged into main.
   - PR has an approving review by an authorized CODEOWNER whose login equals approved_by.
   - Review's submitted_at timestamp is valid.
   - PR changed files list includes the target document.

Distinguishes between:
- Verification negatives (hash mismatch, unmerged PR, missing CODEOWNER approval, file not in PR) -> excludes page.
- API / permission errors (network down, bad token, 401/403, rate limits) -> fails the job.

The verifier supports dependency injection via GitHubApiClient for deterministic,
zero-network unit testing with mock responses.
"""

from __future__ import annotations

import fnmatch
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = ROOT.parent
CODEOWNERS_FILE = REPO_ROOT / ".github" / "CODEOWNERS"

FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)


class ApprovalVerificationError(Exception):
    """Base exception for approval verification failures."""


class ApiPermissionError(ApprovalVerificationError):
    """An API error, auth/permission failure, HTTP 401/403/429, or network failure (must fail the publish job)."""


class VerificationNegative(ApprovalVerificationError):
    """A negative verification result (unmerged PR, hash mismatch, missing review, file not in PR). Excludes page."""


def compute_body_hash(content: str) -> str:
    """Return 'sha256:<hex>' of the markdown body after YAML frontmatter."""
    m = FRONTMATTER_RE.match(content)
    body = content[m.end():] if m else content
    return "sha256:" + hashlib.sha256(body.encode("utf-8")).hexdigest()


def compute_file_body_hash(path: Path) -> str:
    """Compute body sha256 for a document file on disk."""
    return compute_body_hash(path.read_text(encoding="utf-8"))


def parse_codeowners(codeowners_file: Optional[Path] = None) -> List[Tuple[str, List[str]]]:
    """Parse a CODEOWNERS file into a list of (pattern, [owner_usernames])."""
    path = codeowners_file or CODEOWNERS_FILE
    if not path.is_file():
        return []
    rules: List[Tuple[str, List[str]]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) >= 2:
            pattern = parts[0].lstrip("/")
            owners = [p.lstrip("@") for p in parts[1:] if p.startswith("@")]
            rules.append((pattern, owners))
    return rules


def is_authorized_codeowner(
    repo_rel_path: str,
    username: str,
    codeowners_file: Optional[Path] = None
) -> bool:
    """Check if `username` is an authorized CODEOWNER for `repo_rel_path`."""
    rules = parse_codeowners(codeowners_file)
    rel = repo_rel_path.lstrip("/")
    matched_owners: List[str] = []
    # CODEOWNERS rules are evaluated top to bottom; later rules override earlier ones
    for pattern, owners in rules:
        pat = pattern.rstrip("/")
        if fnmatch.fnmatch(rel, pattern) or fnmatch.fnmatch(rel, f"{pat}/*") or fnmatch.fnmatch(rel, f"{pat}/**"):
            matched_owners = owners
    return username in matched_owners


class GitHubApiClient:
    """Interface for GitHub REST API queries."""

    def get(self, endpoint: str) -> Any:
        raise NotImplementedError


class RealGitHubApiClient(GitHubApiClient):
    """Real GitHub REST API client using urllib and GITHUB_TOKEN."""

    def __init__(self, token: Optional[str] = None):
        self.token = token or os.environ.get("GITHUB_TOKEN", "")

    def get(self, endpoint: str) -> Any:
        url = f"https://api.github.com/{endpoint.lstrip('/')}"
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "DOCCAD-ApprovalGate/1.0",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=15) as res:
                return json.loads(res.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):
                raise ApiPermissionError(f"GitHub API authentication/permission error ({e.code}): {e.reason}")
            if e.code == 404:
                raise VerificationNegative(f"GitHub API resource not found ({endpoint}): {e.reason}")
            raise ApiPermissionError(f"GitHub API HTTP {e.code} error: {e.reason}")
        except urllib.error.URLError as e:
            raise ApiPermissionError(f"GitHub API connection error: {e.reason}")
        except Exception as e:
            if isinstance(e, ApprovalVerificationError):
                raise
            raise ApiPermissionError(f"GitHub API query failed: {e}")


class MockGitHubApiClient(GitHubApiClient):
    """Deterministic mock client for offline tests."""

    def __init__(self, responses: Optional[Dict[str, Any]] = None, errors: Optional[Dict[str, Exception]] = None):
        self.responses = responses or {}
        self.errors = errors or {}

    def get(self, endpoint: str) -> Any:
        ep = endpoint.lstrip("/")
        if ep in self.errors:
            raise self.errors[ep]
        for key, err in self.errors.items():
            if fnmatch.fnmatch(ep, key):
                raise err

        if ep in self.responses:
            return self.responses[ep]
        for key, resp in self.responses.items():
            if fnmatch.fnmatch(ep, key):
                return resp
        raise KeyError(f"Mock endpoint not found: {ep}")


class ApprovalVerifier:
    """Verifies production eligibility of an approved generated view (E3)."""

    def __init__(
        self,
        client: Optional[GitHubApiClient] = None,
        repo: Optional[str] = None,
        codeowners_file: Optional[Path] = None,
    ):
        self.client = client
        self.repo = repo or os.environ.get("GITHUB_REPOSITORY", "w7-mgfcode/doCCAD_pre")
        self.codeowners_file = codeowners_file or CODEOWNERS_FILE

    def verify(
        self,
        doc_path: Path,
        frontmatter: Dict[str, Any],
        require_api_gate: bool = True
    ) -> Tuple[bool, str]:
        """Perform full validation of the approval claim and GitHub API gate.

        Raises:
          VerificationNegative: if claim fails verification (hash mismatch, unmerged PR, etc.)
          ApiPermissionError: if API/network/permission fails
        Returns (is_valid, reason).
        """
        gen = frontmatter.get("generation")
        if not isinstance(gen, dict):
            raise VerificationNegative("Missing generation block")

        status = gen.get("approval_status")
        if status != "approved":
            raise VerificationNegative(f"approval_status is '{status}', not 'approved'")

        rec = gen.get("approval_record")
        if not isinstance(rec, dict):
            raise VerificationNegative("Missing approval_record block for approved status")

        pr = rec.get("pr")
        approved_by = rec.get("approved_by")
        approved_at = rec.get("approved_at")
        approved_hash = rec.get("approved_hash")

        if not pr or not approved_by or not approved_at or not approved_hash:
            raise VerificationNegative(f"Incomplete approval_record: {rec}")

        # 1. Verify content body hash integrity (detects tamper / drift after approval)
        actual_hash = compute_file_body_hash(doc_path)
        if actual_hash != approved_hash:
            raise VerificationNegative(
                f"Hash mismatch: body modified after approval; "
                f"recorded {approved_hash}, actual {actual_hash}. "
                f"Artifact must return to in-review."
            )

        if not require_api_gate:
            return True, "Local approval claim and body hash verified"

        # 2. GitHub REST API Gate
        client = self.client
        if client is None:
            token = os.environ.get("GITHUB_TOKEN")
            if not token:
                raise ApiPermissionError("GITHUB_TOKEN not set; cannot verify PR approval against GitHub API")
            client = RealGitHubApiClient(token=token)

        # Compute repo-relative path of target document
        try:
            repo_rel = doc_path.resolve().relative_to(REPO_ROOT).as_posix()
        except ValueError:
            repo_rel = doc_path.as_posix()

        # Check CODEOWNER authorization of approved_by
        if not is_authorized_codeowner(repo_rel, approved_by, self.codeowners_file):
            raise VerificationNegative(f"Reviewer '{approved_by}' is not an authorized CODEOWNER for '{repo_rel}'")

        # Query 1: PR state & merged status
        pr_data = client.get(f"repos/{self.repo}/pulls/{pr}")
        if not isinstance(pr_data, dict):
            raise ApiPermissionError(f"PR #{pr} query returned unexpected response format")
        if not pr_data.get("merged", False):
            raise VerificationNegative(f"PR #{pr} is not merged (state: {pr_data.get('state')})")

        # Query 2: PR reviews
        reviews = client.get(f"repos/{self.repo}/pulls/{pr}/reviews")
        if not isinstance(reviews, list):
            raise ApiPermissionError(f"PR #{pr} reviews query returned unexpected response format")

        valid_review_found = False
        for r in reviews:
            reviewer_login = (r.get("user") or {}).get("login")
            state = r.get("state")
            submitted_at = r.get("submitted_at")
            if reviewer_login == approved_by and state == "APPROVED":
                if submitted_at:
                    valid_review_found = True
                    break

        if not valid_review_found:
            raise VerificationNegative(f"PR #{pr} has no APPROVED review submitted by CODEOWNER '{approved_by}'")

        # Query 3: PR changed files
        files_data = client.get(f"repos/{self.repo}/pulls/{pr}/files")
        if not isinstance(files_data, list):
            raise ApiPermissionError(f"PR #{pr} files query returned unexpected response format")

        pr_filenames = {f.get("filename") for f in files_data if isinstance(f, dict)}
        if repo_rel not in pr_filenames:
            raise VerificationNegative(f"PR #{pr} did not modify '{repo_rel}'")

        return True, f"Verified: PR #{pr} merged with CODEOWNER approval from {approved_by}"
