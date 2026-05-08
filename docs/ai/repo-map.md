# Repository Map For AI Tools

Use this map to quickly route edits to the right location.

## Top-Level Areas

- src/ansys/fluent/core
  - Main runtime package code.
  - Includes launch/session APIs, service clients, datamodel support, and utilities.
- src/ansys/fluent/core/generated
  - Generated API artifacts. Prefer regeneration over manual edits.
- codegen
  - Code generation scripts. Entry point: codegen/allapigen.py.
- tests
  - Pytest suite with markers and Fluent version dependent behaviors.
- doc/source
  - User docs and API documentation sources.
- examples
  - End-user examples.
- docker
  - Container support assets for Fluent images.
- .github/workflows
  - CI pipelines and quality gates.

## Frequently Touched Files

- pyproject.toml: dependencies, pytest defaults, markers.
- Makefile: local shortcuts for install/test/docs/codegen.
- .pre-commit-config.yaml: style/lint checks.

## Typical Task Routing

- Bug in runtime behavior: src + focused tests.
- API shape generated from Fluent metadata: codegen sources + regeneration.
- User-facing docs mismatch: doc/source updates.
- Tooling/lint issues: pyproject.toml and pre-commit configuration.
