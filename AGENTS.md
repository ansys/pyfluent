# AGENTS.md — PyFluent (ansys-fluent-core)

Pythonic API over Ansys Fluent. src-layout under src/ansys/fluent/core.
Python 3.10–3.14. Build backend: flit. Supported Fluent: 2024 R2 SP05,
2025 R1 SP04, 2025 R2 SP03, 2026 R1, and later.

## Entry points
- Launch/connect via `pyfluent.launch_fluent(...)` (and `connect_to_fluent`) in
  execution/launcher/launcher.py; returns a meshing or solver session.
- Example data via `ansys.fluent.core.examples.download_file(...)`.
- Read behavior from `pyfluent.config.<attr>`.
- Generated API is per Fluent version (generated/v261/, generated/v271/, …);
  don't hardcode a version path — resolve it from the live session.

## Never hand-edit
- src/ansys/fluent/core/generated/** — auto-generated (header "DO NOT EDIT"),
  gitignored, shipped in wheels. Regenerate ONLY if its code is wrong or being
  changed, via `python codegen/allapigen.py` (needs a licensed Fluent). Routine
  work does NOT require re-running codegen.
- Don't lint/format/auto-fix generated/ (already excluded from every tool), the
  codegen data inputs under src/ansys/fluent/core/codegen/data/, or
  devel/field_level_help/field_level_help.csv.
- A fresh clone has no generated/: `import ansys.fluent.core` works, but
  session.settings and session.tui need generated/ at runtime.

## Current vs legacy — use the current one
- Prefer the settings API (session.settings.*) for new code. The TUI API
  (session.tui.*) is superseded/legacy (docs under user_guide/legacy/) but still
  supported — use it only when no settings equivalent exists; don't mass-migrate.
- workflow.py is current; workflow_old.py is legacy (ClassicWorkflow).
- Use file_reader/ and _variable_strategies/; filereader/ and
  variable_strategies/ are empty back-compat shims.
- Keep the sys.modules back-compat aliases in __init__.py; don't route new
  imports through them.
- When deprecating, use the `@deprecated` decorator and raise/emit
  PyFluentDeprecationWarning (diagnostics/exceptions.py); don't just delete.

## Hazards (silent breakage)
- Preserve __init__.py import order: config before logging, logging before other
  modules (the `isort: off` blocks are intentional).
- pyfluent.config and PYFLUENT_* env vars are frozen at import — setting them
  mid-process has no effect; configure before import/launch.

## Tests
- Prefer mock / no-Fluent tests (pytest-mock, tests using mock servers) first,
  both when running and when writing tests; only reach for Fluent-backed tests
  for what those can't verify.
- Most tests need a running Fluent (local or container) + a license, and many
  download example files over the network (examples/downloads.py).
  rest_server-marked tests need a live Fluent web server. A plain sandbox can't
  run these — a failure there is usually a missing resource, not a code bug.
- Run: `python -m pytest -n 4 --fluent-version=25.1`
  (container mode: set PYFLUENT_LAUNCH_CONTAINER=1).
- Markers: settings_only, nightly, standalone, rest_server, fluent_version.
- Respect existing skips in tests/conftest.py (SKIP_UNKNOWN/INVESTIGATING/
  BLOCKED); don't re-enable known-broken tests. addopts ignores tests/fluent and
  tests/journals.

## Style & workflow
- pre-commit gates: black, isort, flake8, bandit, codespell, pylint, conventional
  commit messages, license headers. Run `make style` before committing.
- Changelog: add a towncrier fragment under doc/changelog.d; never edit
  doc/source/changelog.rst by hand.

## Docs
- When docs and code disagree, trust the code. Known stale spot: README.rst
  headlines the TUI as a core feature though it is now legacy.
