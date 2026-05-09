#!/usr/bin/env bash
# Guard: fail if secret patterns or gitignored clutter are staged/tracked.
# Exits 0 on clean; 1 on any finding.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

FAIL=0

# ── secret pattern scan (tracked + untracked non-ignored files) ───────────────
# Excludes: tests/ (fake fixture keys), scripts/ (grep args), .github/ (CI placeholders)
echo "[check] scanning for secret patterns..."
SECRET_HITS="$(git grep -rn -e 'sk-ant-' -e 'tvly-' \
    -- ':!tests/' ':!scripts/' ':!.github/' ':!*.md' 2>/dev/null || true)"

if [[ -n "${SECRET_HITS}" ]]; then
    echo "FAIL: secret patterns found in tracked files:"
    echo "${SECRET_HITS}"
    FAIL=1
else
    echo "  OK: no secret patterns in tracked files"
fi

# Also scan untracked (non-ignored) files, excluding tests/, scripts/, .github/
UNTRACKED_SECRETS="$(git ls-files --others --exclude-standard \
    | grep -v -e '^tests/' -e '^scripts/' -e '^\.github/' \
    | xargs grep -ln -e 'sk-ant-' -e 'tvly-' 2>/dev/null || true)"

if [[ -n "${UNTRACKED_SECRETS}" ]]; then
    echo "FAIL: secret patterns found in untracked files:"
    echo "${UNTRACKED_SECRETS}"
    FAIL=1
else
    echo "  OK: no secret patterns in untracked files"
fi

# ── .env file guard ───────────────────────────────────────────────────────────
echo "[check] verifying .env is ignored..."
if git ls-files --error-unmatch .env &>/dev/null; then
    echo "FAIL: .env is tracked by git"
    FAIL=1
else
    echo "  OK: .env is not tracked"
fi

# ── gitignored clutter guard (warn only, not fail) ───────────────────────────
echo "[check] checking for ignored clutter in worktree..."
CLUTTER="$(git ls-files --ignored --exclude-standard --others \
    | grep -E '^\.(pytest_cache|venv)|^__pycache__|^runs/' || true)"

if [[ -n "${CLUTTER}" ]]; then
    echo "  WARN: ignored paths present in worktree (not tracked, safe to ignore):"
    echo "${CLUTTER}" | head -10
else
    echo "  OK: no unexpected clutter"
fi

# ── result ────────────────────────────────────────────────────────────────────
if [[ "${FAIL}" -eq 1 ]]; then
    echo ""
    echo "RESULT: FAIL"
    exit 1
fi

echo ""
echo "RESULT: PASS"
