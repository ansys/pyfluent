# Contributor workflow

Keep work narrow, test-driven, and repo-aware.

## Default flow

1. Identify the owning subsystem.
2. Search for the relevant symbols and tests.
3. Read only the tightest relevant sections.
4. Fix one root cause.
5. Run the cheapest validation that checks the changed behavior.
6. Check import paths and package-level exposure before escalating to heavier tests.
7. Avoid large Fluent-session tests unless the patch genuinely requires them.
8. If there is uncertainty about the correct feature mapping or fix site, ask the user instead of guessing.
9. Keep the primary objectives in view: minimal token consumption and high accuracy through targeted repo knowledge.
10. Summarize what changed and the evidence.

## Repo conventions

- Keep patches within the owning feature area.
- Prefer existing project patterns over new abstractions.
- Respect the separation between runtime code and generated code.
- Do not broaden scope for a single bug fix.

## Escalate when the work touches

- Fluent version compatibility
- generation or schema workflows
- packaging or release behavior
- CI or platform-specific execution

Use the root AGENTS file as the startup brief, and the deeper docs only when the task actually needs that context.
