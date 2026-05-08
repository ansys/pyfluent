# Change Checklist For AI Tools

Use this checklist before opening or updating a PR.

## Scope And Safety

- Change is limited to requested scope.
- No unrelated refactors were introduced.
- No secrets, tokens, or credentials were added.

## Correctness

- Behavior changes are covered by focused tests.
- Existing tests for affected areas still pass.
- Version-specific logic is handled where applicable.

## Generated Code

- Generated files were not hand-edited unless explicitly required.
- If generated files changed, regeneration command is documented.

## Style And Quality

- pre-commit checks were run when feasible.
- New code follows existing style and naming patterns.
- Public APIs were not changed unintentionally.

## Documentation

- User-facing behavior changes are documented under doc/source.
- Terminology is consistent with Fluent/PyFluent docs.

## Final Report

- Include tests run and outcomes.
- List tests not run and why.
- Mention infrastructure blockers (license server, Fluent install, container access).
