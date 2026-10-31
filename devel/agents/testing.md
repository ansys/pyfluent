# Testing strategy

Follow `AGENTS.md`: validate imports/syntax, then the nearest behavior-scoped node/file, then subsystem/integration tests only as needed. Prefer real behavior over mock-only assertions; validate downstream contracts for generated/schema changes and add a focused public-API regression test. Never replace relevant validation with unrelated cheap tests.

## Commands

`python -m pytest tests` is the broad default, not the starting point for a narrow fix:

```bash
python -m pytest tests/test_rest.py
python -m pytest tests/test_search.py::test_match_whole_word
python -m pytest tests/test_settings_api.py -k relevant_behavior --fluent-version=26.1
python -m pytest tests/test_solvermode/test_models.py --solvermode --fluent-version=26.1
```

Use the actual target Fluent version. `python -m pytest --collect-only <target>` checks imports/node IDs without ordinary fixture execution; it does not prove tests will run rather than skip.

## Requirements and skips

The source of truth is `pyproject.toml` (`tool.pytest.ini_options`) and `tests/conftest.py`:

- Discovery starts in `tests`; generated-on-demand `tests/fluent` and `tests/journals` are ignored. `--write-fluent-journals` regenerates output and clears the collected run; not routine validation.
- `nightly` tests skip without `--nightly`. This flag enables nightly tests in addition to ordinary tests.
- `tests/test_solvermode` runs only with `--solvermode`; that flag also skips tests outside that directory. `tests/test_meshingmode` has no corresponding mode flag.
- `fluent_version(spec)` checks `--fluent-version` if supplied. `latest` means the current release in ordinary runs and release-or-newer in nightly/solvermode runs; `dev` means the current development version. Omitting the version option does not automatically filter unsupported tests.
- `standalone` means incompatible with container execution, not mock-only or server-free. `settings_only` means settings without mesh/solve work, not no Fluent session.
- `rest_server` identifies live web-server tests. Read `rest_server_connection` and `solver_session_grpc_rest` fixtures for launch, endpoint, and authentication requirements; the marker alone does not start or skip a server.
- Inspect fixture dependencies in `tests/conftest.py` before classifying a test as offline. `tests/fluent_fixtures.py` supplies helpers for generated Fluent journals, not the ordinary pytest fixture registry.
- The autouse fixture changes the working directory to `tmp_path`, sets test configuration, and copies local certificates when present.
- Install the package and `tests` extra for pytest; readers need `reader` (`h5py`), semantic search needs `search` (`nltk`), and UI needs `ui` / `ui-jupyter`. Case-data downloads, generated APIs, licenses, Docker, and live Fluent are separate requirements; test extras alone do not provide them.

## Feature-to-test map

Repository-relative candidates, not guarantees that whole files are cheap/server-free. Source owners are in `devel/agents/architecture.md`.

- Launch and session lifecycle: `tests/test_launcher.py`, `tests/test_launcher_remote.py`, `tests/test_fluent_session.py`, `tests/test_session.py`, `tests/test_pre_post_session.py` (mixed unit/live coverage).
- Connections/security/errors: `tests/test_grpc_security_options.py`, `tests/test_error_handling.py`; config: `tests/test_config.py`.
- Meshing workflows: `tests/test_meshing_workflow.py`, `tests/test_new_meshing_workflow.py`, `tests/test_meshing_utilities.py`, `tests/test_pure_mesh_vs_mesh_workflow.py`, `tests/test_server_meshing_workflow.py` (live/version-sensitive).
- Meshing launch/end-to-end: `tests/test_meshingmode/test_meshing_launch.py`, `tests/test_cad_to_post_wtm.py`, `tests/test_cad_to_post_ftm.py` (live).
- Solver and solver-mode behavior: `tests/test_solution_variables.py`, `tests/test_solvermode`, `tests/test_tui_api.py`, `tests/test_public_api.py`; variants: `tests/test_aero_session.py`, `tests/test_icing_session.py`, `tests/test_pre_post_session.py` (live; solvermode requires its flag).
- Fields and reduction: `tests/test_field_data.py`, `tests/test_reduction.py`, `tests/test_solution_variables.py`, `tests/test_physical_quantities.py` (live paths; select mock checks where present).
- Settings and datamodel API: `tests/test_settings_api.py`, `tests/test_settings_reader.py`, `tests/test_datamodel_api.py`, `tests/test_datamodel_service.py`, `tests/test_builtin_settings.py`, `tests/test_mapped_api.py`, `tests/test_creatable.py`, `tests/test_preferences.py` (mostly live/model-dependent).
- Settings runtime/cache/generation: `tests/test_flobject.py`, `tests/test_data_model_cache.py`, `tests/test_codegen.py`, `tests/test_type_stub.py` (mixed mock/live/generated contracts).
- File and transfer behavior: `tests/test_file_session.py`, `tests/test_file_transfer_service.py`, `tests/test_datareader.py`, `tests/test_casereader.py` (mixed live, file assets/downloads, reader extras).
- Search and API browsing: `tests/test_search.py` (mocked lookup, generated index, NLTK/downloads, and live-session selections).
- API and object surfaces: `tests/test_flobject.py`, `tests/test_rp_vars.py`, `tests/test_public_api.py` (mixed; do not assume object-model tests are offline).
- Batch/remote/scheduler: `tests/test_batch_ops.py`, `tests/test_launcher_remote.py`, `tests/test_slurm_future.py`; machine allocation: `tests/test_scheduler.py` (no Fluent).
- Events/streaming/monitors: `tests/test_events_manager.py`, `tests/test_streaming_services.py`, `tests/test_solver_monitors.py` (live).
- Parametric/coupling: `tests/parametric/test_local_parametric_setup.py` (reader/data download), `tests/parametric/test_local_parametric_run.py`, `tests/parametric/test_parametric_workflow.py`, `tests/test_systemcoupling.py`; optiSLang: `tests/integration/test_optislang/test_optislang_integration.py` (external integration).
- Expressions: `tests/expressions` (parser/builder unit tests and live smoke/integration tests); Scheme/RP/console: `tests/test_scheme_eval.py`, `tests/test_rp_vars.py`, `tests/test_pyconsole.py`; file S-expressions: `tests/test_lispy.py` (no Fluent).
- REST: `tests/test_rest.py` (mocked client/transport); parity: `tests/test_settings_grpc_rest.py` (live gRPC/web-server fixtures). No dedicated Panel/Jupyter rendering test file is currently mapped.
- Utilities/compatibility/docs: `tests/test_utils.py`, `tests/test_fluent_version.py`, `tests/test_fluent_version_marker.py`, `tests/test_deprecate.py`, `tests/test_logging.py`, `tests/test_fix_doc.py`, `tests/test_topy.py`, `tests/test_fluent_fixes.py` (check individual fixtures).

### Cheap starting targets

No Fluent server: `tests/test_config.py`, `tests/test_fluent_version.py`, `tests/test_fluent_version_marker.py`, `tests/test_lispy.py`, `tests/test_scheduler.py`, `tests/test_rest.py`. Package/pytest dependencies still apply.

Mixed-file unit nodes: `tests/test_search.py::test_match_whole_word`, `tests/test_data_model_cache.py::test_data_model_cache`. Inspect bodies/transitive fixtures before expanding.
