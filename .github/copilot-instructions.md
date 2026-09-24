# GitHub Copilot instructions for PyFluent

This file is intentionally minimal. The canonical project guidance lives in @AGENTS.md at the repository root. Use that file as the single source of truth for setup, repo map, commands, and default operating rules.

## Required behavior

- Read @AGENTS.md first for project orientation.
- Start with one targeted search and the smallest relevant reads.
- Prefer the closest existing test coverage over new assumptions.
- Keep fixes narrow and root-cause focused.
- Do not hand-edit generated API files without a clear, justified reason.

## Repo-specific overrides

- Treat `src/ansys/fluent/core` as the main runtime package.
- Treat `codegen` and generated modules as schema-driven or generation-managed code unless explicitly required otherwise.
- Use the smallest relevant pytest target; do not default to a broad suite for a small fix.
- For deeper architecture or workflow guidance, follow the links in @AGENTS.md to the docs under `devel/agents`.

## Documentation hierarchy

- @AGENTS.md — canonical startup and repo guidance
- @devel/agents/architecture.md — subsystem and architecture map
- @devel/agents/testing.md — validation strategy
- @devel/agents/workflows.md — contribution workflow

This file should stay short and point to the canonical guidance rather than re-describing it.
