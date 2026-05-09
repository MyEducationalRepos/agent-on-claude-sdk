"""Helper that collects and formats related local paths and external links."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class RelatedLinks:
    """Container for local repo paths and external URLs."""

    local_paths: list[str] = field(default_factory=list)
    external_links: list[str] = field(default_factory=list)

    def to_markdown(self) -> str:
        """Render as Markdown with two sub-sections."""
        lines: list[str] = []

        lines.append("## Local Paths")
        lines.append("")
        if self.local_paths:
            for p in self.local_paths:
                lines.append(f"- {p.strip()}")
        else:
            lines.append("- *(none)*")
        lines.append("")

        lines.append("## External Links")
        lines.append("")
        if self.external_links:
            for link in self.external_links:
                lines.append(f"- {link.strip()}")
        else:
            lines.append("- No external link available yet")
        lines.append("")

        return "\n".join(lines)


def collect_local_paths(root: Path, patterns: list[str] | None = None) -> list[str]:
    """Return workspace-relative paths matching *patterns* under *root*.

    Args:
        root: Repo root directory to search from.
        patterns: Glob patterns to match (e.g. ``["**/*.md", "src/**/*.py"]``).
                  Defaults to a standard project set when omitted.

    Returns:
        Sorted list of POSIX-style relative path strings.
    """
    if patterns is None:
        patterns = [
            "CLAUDE.md",
            "WRITEUP.md",
            "README.md",
            "architecture.md",
            "skills/research-summary/SKILL.md",
            "src/**/*.py",
        ]

    found: set[str] = set()
    for pattern in patterns:
        for p in root.glob(pattern):
            if p.is_file():
                found.add(p.relative_to(root).as_posix())

    return sorted(found)
