# Testing strategy

Use the smallest relevant test target that checks the changed behavior.

## Canonical command

```bash
python -m pytest tests
```

## Rules

1. Start from the nearest test file or selection for the changed behavior.
2. Prefer real behavior validation over mock-only assertions.
3. If the change touches generated or schema-driven code, validate the downstream contract as well.
4. Do not default to a full suite for a narrow fix.
5. Prefer cheap validation first: import checks, syntax checks, and the closest non-Fluent tests.
6. Avoid large integration suites or tests requiring an active Fluent session unless the change genuinely requires them.
7. If the change affects imports, package boundaries, or public APIs, validate import paths and package exposure before escalating.
8. If a public API regression is fixed, add or update a focused test.
9. If the correct test target is unclear, ask the user instead of guessing or running broad suites.
10. Keep the first objective in mind: good answers with minimal token usage; use the cheapest validation that still checks the behavior.

## Repo context

The `tests` tree covers:

- runtime API behavior
- Fluent launch and session lifecycle
- settings/datamodel access
- field data and solution-variable workflows
- meshing and solver-mode behavior
- file transfer and session persistence
- regression and compatibility checks

## Feature-to-test map

Use this as a quick routing guide before choosing a test target:

- Launch and session lifecycle: `test_launcher.py`, `test_launcher_remote.py`, `test_fluent_session.py`, `test_session.py`
- Settings and datamodel API: `test_settings_api.py`, `test_settings_reader.py`, `test_datamodel_api.py`, `test_datamodel_service.py`
- Field data and solution variables: `test_field_data.py`, `test_solution_variables.py`, `test_physical_quantities.py`
- Meshing workflows: `test_meshing_workflow.py`, `test_new_meshing_workflow.py`, `test_meshing_utilities.py`, `test_pure_mesh_vs_mesh_workflow.py`, `test_server_meshing_workflow.py`
- File and transfer behavior: `test_file_session.py`, `test_file_transfer_service.py`, `test_datareader.py`, `test_casereader.py`
- API and object surfaces: `test_flobject.py`, `test_tui_api.py`, `test_rp_vars.py`, `test_public_api.py`

This is not exhaustive, but it gives a stable map from feature area to the most likely test cluster.

Use this structure to choose the closest validation path, not a broad one.
