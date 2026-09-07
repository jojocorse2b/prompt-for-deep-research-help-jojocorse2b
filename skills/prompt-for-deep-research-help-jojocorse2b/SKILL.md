---
name: prompt-for-deep-research-help-jojocorse2b
description: Generate safe, context-aware Deep Research prompts for complex technical, product, business, scientific, legal, or market questions.
---

# Deep Research Prompt Builder

This skill generates the prompt. The user then pastes it into ChatGPT,
Gemini, Perplexity, or another research tool. Do not pretend that generating a
prompt is the same as performing the research.

## Workflow

1. Restate the decision or question in one sentence.
2. Read only relevant project context. Prefer the bundled snapshot helper:
   `python scripts/context_snapshot.py . --json`. Exclude secrets, generated
   files, dependencies, caches, and unrelated large files.
3. Select a mode: `quick` for orientation, `standard` for a decision, or
   `deep` for high-stakes or contested questions.
4. Select one focused template: technical, product, market, scientific,
   legal, or general. Do not mix unrelated research missions.
5. Generate a prompt with exactly these sections: Objective, Context,
   Investigate, Source Requirements, Output Format, and Constraints.
6. Require current dates, primary sources where available, source URLs,
   counter-evidence, contradiction reporting, confidence labels, and an
   explicit distinction between fact and inference.
7. Run `python scripts/secret_scan.py` on the prompt and context snapshot.
   Redact anything suspicious before it reaches the clipboard.
8. Save the final prompt to a local history file using
   `python scripts/build_prompt.py ... --history-dir .research-prompts`.
9. Copy the prompt using the helper's safe clipboard fallback. If no clipboard
   is available, print it and tell the user to copy it manually.

## Context rules

- Never include API keys, tokens, passwords, private URLs, private source code,
  personal data, or full secret-bearing environment files.
- Prefer concrete versions, dependencies, architecture decisions, scale,
  constraints, team size, budget, timeline, and previously rejected options.
- Mark unknown context as `[unknown]`; never invent it.
- If the repository is empty or unrelated, say so and generate a bounded prompt
  instead of pretending to know the project.

## Modes

- **quick**: 3–5 research angles, 3–5 strong sources, concise recommendation.
- **standard**: 5–8 angles, source comparison, risks, trade-offs, and decision
  matrix.
- **deep**: multi-round research, counter-evidence, claim-level citations,
  contradiction log, confidence assessment, and limitations appendix.

## Prompt quality requirements

The generated prompt must:

- use imperative language and one clear research mission;
- request official documentation, standards, papers, filings, or maintainers
  before secondary summaries when applicable;
- ask the research tool to record publication dates and access dates;
- require direct evidence for numerical and causal claims;
- ask it to show disagreements instead of averaging them away;
- specify the desired deliverable and the decision it should support;
- contain no fabricated project details or citations.

## Refinement

When the user asks to narrow, broaden, or add an angle, load the most recent
prompt from history and modify it. Preserve the existing context and mission;
do not regenerate unrelated sections. Save a new timestamped revision.

## Helpers

```bash
python scripts/context_snapshot.py /path/to/project --json
python scripts/secret_scan.py /path/to/project
python scripts/build_prompt.py "research question" \
  --context /path/to/project/context.json \
  --mode standard --template technical \
  --history-dir /path/to/project/.research-prompts --copy
```

Read [prompt-format.md](../../references/prompt-format.md) when a custom
template or output contract is needed.
