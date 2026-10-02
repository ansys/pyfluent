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
- `src/ansys/fluent/core/execution` — launchers, base-session context, file sessions, containers, schedulers
- `src/ansys/fluent/core/connectivity` — Fluent connections and file/data transfer
- `src/ansys/fluent/core/meshing` — meshing sessions and pre-set meshing workflows
- `src/ansys/fluent/core/solver` — solver sessions and solver APIs, including settings objects
- `src/ansys/fluent/core/fields` / `services` — field APIs and backend transports
- `src/ansys/fluent/core/diagnostics` — search, logging, journaling, exceptions
- `src/ansys/fluent/core/generated` — generated API code
- `codegen` — generation workflow
- `tests` — behavior and regression tests
- `doc` / `examples` / `devel` — docs, examples, engineering notes

## Agent rules

1. Start with one targeted search and the smallest relevant reads.
2. Prefer existing tests and project conventions over guessing.
3. Diagnose the root cause and fix it in the owning abstraction; avoid symptom patches or workarounds. Keep changes narrow and unrelated behavior untouched.
4. Do not hand-edit generated API files unless required.
5. Validate with the smallest relevant test target.
6. Prefer cheap validation first: import checks, syntax checks, and nearby non-Fluent tests.
7. Avoid large integration or active-Fluent-session tests unless the change truly requires them.
8. If imports, package boundaries, or public APIs are affected, check import paths before escalating.
9. If the subsystem, feature mapping, or test target is unclear, ask the user instead of guessing.
10. Use current implementation paths, not legacy import aliases, to locate owners; check public compatibility aliases in `src/ansys/fluent/core/__init__.py` when imports change.
11. Follow standard software design principles: separation of concerns, cohesive responsibilities, explicit contracts, and minimal coupling. Prefer existing patterns, simple solutions, and justified abstractions over duplication or speculative complexity.
12. Preserve user changes and existing instruction intent; confirm before removing instructions. When new concepts, anomalies, or stale guidance suggest an improvement, explain the evidence and proposed update, ask the user, and modify `AGENTS.md` or the relevant guide only after approval. Keep updates concise and verified; remove duplication, not unique facts, constraints, or safety rules.

## Deeper guidance

- `devel/agents/architecture.md` — source owners, feature entry points, runtime relationships
- `devel/agents/testing.md` — test map, cheap targets, dependencies and skip rules
- `devel/agents/workflows.md` — contribution, generation, CI/docs commands and maintenance
- `.github/copilot-instructions.md` — short repo-specific pointer

Load only the relevant section when routing or validation is unclear, or the task touches lifecycle, meshing/solver APIs, generation, packaging, or CI. Do not preload all guides or duplicate their maps here.
