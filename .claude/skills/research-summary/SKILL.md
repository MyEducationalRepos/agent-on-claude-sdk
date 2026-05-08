---
name: research-summary
description: Produce a concise research summary with the standard project output format. Use when the user asks for a research summary, literature scan, source roundup, or related-links synthesis.
license: MIT
---

# Research Summary Skill

Use this Skill when the user needs a compact research synthesis from repository materials, web sources, papers, or related links.

## Output Format

Write the answer in this structure:

```markdown
## Research Summary

### Question
State the research question in one sentence.

### Key Findings
- Finding 1 with source or path.
- Finding 2 with source or path.
- Finding 3 with source or path.

### Related Links
- [Label](path-or-url): why it matters.

### Gaps
- What remains unknown or unverified.

### Next Step
One concrete follow-up action.
```

## Rules

- Keep findings brief and evidence-linked.
- Prefer repository-relative paths for local files.
- Separate confirmed facts from assumptions.
- If no reliable source is available, say so plainly.