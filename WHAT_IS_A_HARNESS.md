# What a harness is: from-scratch vs Claude Agent SDK

Target publish date: 2026-05-25

## What a harness is

A harness is the part of an agent system that keeps the work loop stable. It is the layer that sends the task to the model, receives the response, notices when the model wants a tool, runs that tool, returns the result, and decides whether the run should continue or stop. In plain language, the harness is the operational frame around the model. The model provides reasoning and text generation; the harness handles the repetition, safety checks, and control flow that make the agent usable.

That distinction matters because many first agent projects start by mixing those responsibilities together. The result can work, but it is harder to extend and harder to trust. A project called `agent-from-scratch` shows that tradeoff clearly. When you build the loop yourself, you also own turn tracking, message shaping, stop conditions, tool dispatch, error handling, and the logic that feeds tool results back into the next model call.

The Claude Agent SDK changes that balance. Instead of rewriting the same infrastructure every time, you start with a harness that already understands the common agent lifecycle. That does not remove the need for careful design. You still have to define tools, prompts, validation, and outputs. What it removes is the low-level plumbing that is easy to get wrong and tedious to maintain.

The comparison is not really about magic intelligence. It is about leverage. In the from-scratch path, most early effort goes into orchestration. With the Claude Agent SDK path, more of that effort can move into product behavior: better tool contracts, clearer validation, reusable formats like a research summary, and documentation that is easier to review. The harness becomes a reusable boundary instead of a pile of custom glue.

That is why this draft is ready to publish. It explains the difference in plain language, keeps the contrast concrete, and gives readers a simple mental model: the model thinks, the harness runs the loop.