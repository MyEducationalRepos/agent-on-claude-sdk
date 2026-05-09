"""Formatter that converts a raw research result into the research-summary Skill shape."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ResearchSummary:
    """Structured output matching the research-summary Skill contract."""

    question: str
    key_findings: list[str]
    local_paths: list[str] = field(default_factory=list)
    external_links: list[str] = field(default_factory=list)
    evidence_gaps: list[str] = field(default_factory=list)
    next_step: str = ""

    def to_markdown(self) -> str:
        """Render the summary as a Markdown string following the Skill contract."""
        lines: list[str] = []

        lines.append("## 1. Question")
        lines.append("")
        lines.append(self.question.strip())
        lines.append("")

        lines.append("## 2. Key Findings")
        lines.append("")
        for finding in self.key_findings:
            lines.append(f"- {finding.strip()}")
        lines.append("")

        lines.append("## 3. Related Links")
        lines.append("")
        lines.append("**Local Paths**")
        lines.append("")
        if self.local_paths:
            for p in self.local_paths:
                lines.append(f"- {p.strip()}")
        else:
            lines.append("- *(none)*")
        lines.append("")
        lines.append("**External Links**")
        lines.append("")
        if self.external_links:
            for link in self.external_links:
                lines.append(f"- {link.strip()}")
        else:
            lines.append("- *(none)*")
        lines.append("")

        lines.append("## 4. Evidence Gaps")
        lines.append("")
        if self.evidence_gaps:
            for gap in self.evidence_gaps:
                lines.append(f"- {gap.strip()}")
        else:
            lines.append("- *(none identified)*")
        lines.append("")

        lines.append("## 5. Next Step")
        lines.append("")
        lines.append(self.next_step.strip() if self.next_step else "*(not specified)*")
        lines.append("")

        return "\n".join(lines)
