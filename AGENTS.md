# PyFluent Agent Instructions

This file gives coding agents high-signal context for making safe, reviewable changes.

## Project Snapshot

- Package: ansys-fluent-core
- Python: >=3.10,<3.15
- Build backend: flit
- Main source root: src/ansys/fluent/core
- Main test root: tests

## Canonical References

Read these before making non-trivial changes:

- README.rst
- CONTRIBUTING.md
- pyproject.toml
- Makefile
- .pre-commit-config.yaml
- .github/workflows/ci.yml

## Repository Map

- src/ansys/fluent/core: runtime package code
- src/ansys/fluent/core/generated: generated API artifacts
- codegen: generation entry points and scripts
- tests: pytest suite
- doc/source: end-user and API docs
- examples: usage examples
- docker: supported Fluent container definitions

See docs/ai/repo-map.md for more detail.

## Editing Rules

- Keep changes targeted and minimal.
- Do not reformat unrelated files.
- Treat src/ansys/fluent/core/generated as generated output.
- If behavior changes, add or update focused tests under tests.
- If public behavior or docs are impacted, update docs under doc/source.

## Codegen Rules

- Prefer editing codegen sources over hand-editing generated outputs.
- Use python codegen/allapigen.py (or -v) when regeneration is required.
- Document regeneration in PR notes when generated files are changed.

See docs/ai/codegen-rules.md.

## Local Validation

Typical sequence for most changes:

1. Install editable package and test extras.
2. Run targeted pytest file(s).
3. Run pre-commit checks.

Common commands:

- pip install -e .[tests]
- python -m pytest tests/test_flobject.py
- pre-commit run --all-files --show-diff-on-failure

Use docs/ai/test-playbook.md for test selection and environment constraints.

## PR Readiness Checklist

Before opening or updating a PR:

- Ensure changed code paths have tests.
- Ensure formatting/lint checks pass locally where feasible.
- Note Fluent/version/license dependencies for tests that cannot run locally.
- Update docs/changelog artifacts when required by repo policy.

Use docs/ai/change-checklist.md for the full checklist.
