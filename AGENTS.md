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
# optional extras
pip install -e ".[reader,search,ui,ui-jupyter]"
```

## Primary objectives

1. Good answers with minimal token consumption.
2. Accurate answers using the correct repo map and architecture.

## Commands

```bash
python -m pytest tests
pre-commit run --all-files
```

## Repo map

- `src/ansys/fluent/core` — runtime package
- `src/ansys/fluent/core/generated` — generated API code
- `codegen` — generation workflow
- `tests` — behavior and regression tests
- `doc` / `examples` / `devel` — docs, examples, engineering notes

## Agent rules

1. Start with one targeted search and the smallest relevant reads.
2. Prefer existing tests and project conventions over guessing.
3. Keep patches narrow and fix one root cause.
4. Do not hand-edit generated API files unless required.
5. Validate with the smallest relevant test target.
6. Prefer cheap validation first: import checks, syntax checks, and nearby non-Fluent tests.
7. Avoid large integration or active-Fluent-session tests unless the change truly requires them.
8. If imports, package boundaries, or public APIs are affected, check import paths before escalating.
9. If the subsystem, feature mapping, or test target is unclear, ask the user instead of guessing.

## Deeper guidance

- `devel/agents/architecture.md` — subsystem map
- `devel/agents/testing.md` — validation strategy
- `devel/agents/workflows.md` — contribution workflow
- `.github/copilot-instructions.md` — short repo-specific pointer

Use these only when the task touches Fluent lifecycle, meshing/solver APIs, settings/datamodel generation, packaging, or CI behavior.
