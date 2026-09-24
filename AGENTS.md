# AGENTS.md

PyFluent is the Python interface for Ansys Fluent.

## Setup

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
pip install -e ".[tests]"
```

For optional feature sets, install the relevant extras explicitly as needed, for example:

```bash
pip install -e ".[reader,search,ui,ui-jupyter]"
```

## Primary objectives

1. Provide good answers with minimal token consumption.
2. Provide accurate answers by using the correct architectural map and repo-specific guidance.

## Commands

```bash
python -m pytest tests
```

```bash
pre-commit run --all-files
```

## Repo map

- `src/ansys/fluent/core` — runtime package
- `src/ansys/fluent/core/generated` — generated API code
- `codegen` — generation workflow
- `tests` — behavior and regression tests
- `doc` — docs
- `examples` — usage examples
- `devel` — repo engineering notes

## Agent rules

1. Start with one targeted search and the smallest relevant reads.
2. Prefer existing tests and project conventions over guessing.
3. Keep patches narrow and fix one root cause.
4. Do not hand-edit generated API files unless the workflow explicitly requires it.
5. Validate with the smallest relevant test target.
6. Prefer cheap validation first: import checks, syntax checks, and the closest non-Fluent tests.
7. Avoid large integration suites or tests that require an active Fluent session unless the change genuinely requires them.
8. If a change affects imports, package boundaries, or public APIs, check import paths and package-level exposure before escalating to heavier tests.
9. If unsure about the correct subsystem, feature mapping, or test target, ask the user instead of guessing or hallucinating.
10. Keep AGENTS.md lightweight; do not stuff all repo details here. Use the deeper docs for architecture and workflow details.

## Deeper guidance

- `devel/agents/architecture.md` — subsystem map
- `devel/agents/testing.md` — validation strategy
- `devel/agents/workflows.md` — contribution workflow
- `.github/copilot-instructions.md` — repo-specific Copilot overrides

Use the deeper docs only when the task touches Fluent lifecycle, meshing/solver APIs, settings/datamodel generation, packaging, or CI behavior.
