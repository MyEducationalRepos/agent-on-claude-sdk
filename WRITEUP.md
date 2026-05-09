What the harness gave me for free that I wrote myself in agent-from-scratch was the boring but critical plumbing around the model loop. In the scratch project, I manually tracked turns, appended assistant messages, collected tool_use blocks, dispatched each tool, wrapped exceptions, and stitched tool_result payloads back into the next request. I also hand-coded startup checks for missing API keys, stop_reason branching, and guardrails to halt after max turns. The harness removed most of that ceremony. I can focus on task intent, tool contracts, and output quality while the SDK handles lifecycle details, message shaping, and safer defaults. It also made extension easier: adding a helper for related links and a reusable research-summary format feels incremental instead of invasive. Observability improved too, because hooks and conventions give me predictable traces and formatting without custom shell glue everywhere. The practical gain is not magic intelligence; it is leverage. I spend less time rebuilding infrastructure and more time validating behavior, refining prompts, and shipping learning artifacts that are easier to compare, review, and teach. That tradeoff is exactly why this repo exists. It also standardizes defaults, shortens onboarding for collaborators, and reduces regressions because conventions, hooks, and structure stay consistent across sessions.

---

## agent-from-scratch: manual loop

```mermaid
flowchart TD
    A([Start]) --> B[Check API key]
    B -->|missing| Z1([Crash])
    B -->|present| C[Send messages to Claude]
    C --> D{stop_reason?}
    D -->|end_turn| E([Done])
    D -->|max_tokens| Z2([Halt])
    D -->|tool_use| F[Collect tool_use blocks manually]
    F --> G[Dispatch each tool by name]
    G --> H{exception?}
    H -->|yes| I[Wrap error, stitch into message]
    H -->|no| I
    I --> J[Append tool_result payload]
    J --> K{max turns reached?}
    K -->|yes| Z3([Guard halt])
    K -->|no| C
```

## agent-on-claude-sdk: harness loop

```mermaid
flowchart TD
    A([Start]) --> B[Config.load — fail-fast]
    B --> C[Harness.run task]
    C --> D[SDK: send messages]
    D --> E{stop_reason?}
    E -->|end_turn| F[Persist run + trace]
    F --> G([Done])
    E -->|max_turns| H([Ceiling halt])
    E -->|tool_use| I[Registry.dispatch]
    I --> J[tool_result block]
    J --> D
```

## what moved where

```mermaid
quadrantChart
    title Effort before vs after the harness
    x-axis Low effort --> High effort
    y-axis Low value --> High value
    quadrant-1 Keep focus here
    quadrant-2 Now handled by SDK
    quadrant-3 Eliminated
    quadrant-4 Worth automating
    Task intent: [0.85, 0.90]
    Tool contracts: [0.75, 0.85]
    Prompt refinement: [0.80, 0.80]
    Behavior validation: [0.70, 0.75]
    Turn tracking: [0.30, 0.20]
    Message stitching: [0.40, 0.15]
    API key checks: [0.20, 0.10]
    Stop-reason branching: [0.35, 0.25]
```

