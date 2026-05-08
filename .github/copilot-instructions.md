# Copilot Instructions For PyFluent

Use this file for task-time guidance when editing this repository.

## First Reads

1. AGENTS.md
2. README.rst
3. CONTRIBUTING.md
4. pyproject.toml

## Change Scope

- Keep patches small and focused.
- Preserve existing public APIs unless the task explicitly changes behavior.
- Avoid drive-by refactors in unrelated modules.

## Generated Code

- Generated artifacts live in src/ansys/fluent/core/generated.
- Prefer editing code generation sources and regenerating when needed.
- If generated files are updated, include a note about regeneration steps.

## Testing Guidance

- Run focused tests first, then broaden only as needed.
- Some tests require Fluent, container images, or license server access.
- If required infrastructure is missing, report what was not run and why.

Useful commands:

- pip install -e .[tests]
- python -m pytest tests/test_flobject.py
- pre-commit run --all-files --show-diff-on-failure

## Docs And User-Facing Changes

- If user-facing behavior changes, update docs under doc/source.
- Keep terminology aligned with existing Fluent and PyFluent docs.

## Safety Rules

- Do not add secrets, tokens, or credentials.
- Do not edit CI or release workflows unless task requires it.
- Prefer explicit, reversible edits over broad rewrites.

## Additional AI Context

- docs/ai/repo-map.md
- docs/ai/codegen-rules.md
- docs/ai/test-playbook.md
- docs/ai/domain-glossary.md
- docs/ai/change-checklist.md
