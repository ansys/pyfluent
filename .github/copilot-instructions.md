# GitHub Copilot instructions for PyFluent

This file is intentionally minimal. The canonical project guidance lives in @AGENTS.md at the repository root. Use that file as the single source of truth for setup, repo map, commands, and default operating rules.

## Required behavior

- Read @AGENTS.md first for project orientation.
- Follow the repo rules in @AGENTS.md before expanding to deeper docs.
- Keep this file short; do not duplicate the root guidance.

## Repo-specific override

- Treat `src/ansys/fluent/core` as the main runtime package.
- Treat generated modules as schema-driven or generation-managed code unless a task explicitly requires otherwise.

## Documentation hierarchy

- @AGENTS.md — canonical startup and repo guidance
- @devel/agents/architecture.md — subsystem and architecture map
- @devel/agents/testing.md — validation strategy
- @devel/agents/workflows.md — contribution workflow

This file should stay brief and point to the canonical guidance rather than repeating it.
