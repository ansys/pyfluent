# Test Playbook For AI Tools

Use this playbook to choose the smallest meaningful test set first.

## Environment Notes

- Some tests require a local Fluent installation, container image access, or a license server.
- If infrastructure is unavailable, run what is possible and report what was skipped.

## Install

- pip install -e .[tests]

## Fast, Focused Validation

- Single-file sanity:
  - python -m pytest tests/test_flobject.py
- Small targeted run for changed area:
  - python -m pytest tests/test_<area>.py

## Pytest Defaults In This Repo

- testpaths is tests
- addopts includes:
  - --ignore=tests/fluent
  - --ignore=tests/journals
  - -v
  - --durations=0
  - --show-capture=all

## Marker Guidance

Common markers in pyproject.toml:

- settings_only
- nightly
- codegen_required
- standalone
- fluent_version(version)

## Broader Validation

- Optional style check:
  - pre-commit run --all-files --show-diff-on-failure
- Optional expanded tests (when infra exists):
  - python -m pytest -m "not codegen_required"

## Reporting Format

When finishing a change, include:

- Tests run and their outcome.
- Tests not run and why (for example, missing Fluent/license/container access).
