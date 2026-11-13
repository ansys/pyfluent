# Contributor workflow

Follow the root rules in `AGENTS.md`; this guide adds command and maintenance details.

## Default flow

1. Find the owner and nearest test with targeted searches/reads; ask if uncertain.
2. Diagnose and fix the root cause within that feature, following existing patterns and runtime/generated boundaries.
3. Validate the behavior cheaply, check changed imports/exports before heavier tests, and summarize changes with evidence. Preserve user changes and instruction intent as required by the root rules.

## Ownership and commands

- Packaging, extras, Python support, pytest options, and tool configuration live in `pyproject.toml`; build dependencies are in `requirements/requirements_build.txt`.
- API generation logic lives in `src/ansys/fluent/core/codegen`. `codegen/allapigen.py` launches live meshing and solver-icing sessions to gather static info, then generates versioned APIs, workflow task stubs, and search index data into `config.codegen_outdir`.
- Generated output is not an ordinary runtime edit target. For a schema-output defect, update the responsible generator and validate its output contract with `tests/test_codegen.py` and the nearest downstream API test. Full regeneration needs suitable Fluent/server resources.
- Setup: editable install from `AGENTS.md`; extras/test requirements from `devel/agents/testing.md`.
- Style: `pre-commit run --files <changed-files>` for a focused check; `pre-commit run --all-files` remains the canonical full check. Hook configuration is in `.pre-commit-config.yaml`; some hooks explicitly scan whole trees even with a file selection.
- CI entry points are in `.github/workflows`; helper scripts and the type-check baseline live in `.ci`. `Makefile` defines versioned `unittest-dev-*`, `unittest-all-*` (nightly), and `unittest-solvermode-*` lanes, plus `api-codegen`, `test-import`, and documentation targets.
- Treat make targets as CI/platform workflows, not portable local defaults: `make install` runs `git clean -fd`, versioned test targets clear example data with `sudo rm`, and API/docs targets assume Bash/Linux tools and may remove generated output. Inspect the target and confirm destructive cleanup before running it.
- Documentation sources are in `doc/source`; API RST generators are in `doc`, examples in `examples/00-fluent`, and changelog fragments in `doc/changelog.d` (Towncrier configuration in `pyproject.toml`). With doc dependencies installed, `make -C doc html` builds Sphinx; `BUILD_ALL_DOCS` controls API RST regeneration. Full builds can import generated APIs and execute gallery examples, so they are not a cheap default for guidance-only edits.

## Keeping maps accurate

- After user approval under the root maintenance rule, update moved source owners, public/legacy import routing, and test paths together. Verify paths/node IDs, not inferred names.
- Keep one home per fact: root rules, architecture source owners, testing targets/requirements, workflow commands. Load only relevant sections; keep `.github/copilot-instructions.md` a pointer.
- Classify cost from bodies/transitive fixtures and actual skip rules, not filenames or markers.
- For guidance-only changes, check referenced paths (allow explicitly generated-on-demand outputs), command definitions, retained rules, and `git diff --check`; runtime integration tests are unnecessary unless the change also affects executable behavior.

Review the relevant compatibility/schema/build/CI definitions when work touches Fluent versions, generation, packaging/releases, or platform-specific execution; escalate unresolved constraints rather than guessing.
