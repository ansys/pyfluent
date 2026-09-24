# Architecture map for AI agents

This document is intentionally small but repo-specific. It gives agents the fastest path to the right feature area and the most relevant validation target.

## 1. Product shape

PyFluent exposes a Pythonic API on top of Ansys Fluent. The major layers are:

1. Fluent launch and session management
2. Meshing and solver sessions
3. Settings and datamodel surfaces
4. Generated API layer
5. Field data, reduction, and solution-variable workflows
6. File transfer, file sessions, and reader workflows
7. Search, workflows, scheduling, remote execution, and API utilities

## 2. Core package map

- `src/ansys/fluent/core/__init__.py` — top-level package exports and public entry points
- `src/ansys/fluent/core/launcher` — launch orchestration and mode selection
- `src/ansys/fluent/core/session` — concrete session classes: solver, meshing, file, pre/post
- `src/ansys/fluent/core/meshing` — meshing workflows and workflow wrappers
- `src/ansys/fluent/core/solver` — solver API surface and generated settings entry points
- `src/ansys/fluent/core/fields` — field data, reduction, solution variables
- `src/ansys/fluent/core/services` — service interfaces and backend wrappers
- `src/ansys/fluent/core/file_transfer_service.py` — file transfer service
- `src/ansys/fluent/core/file_reader` — case/data file readers
- `src/ansys/fluent/core/search.py` — search API across object hierarchy
- `src/ansys/fluent/core/workflow.py`, `workflow_old.py` — workflow wrappers and compatibility paths
- `src/ansys/fluent/core/local_parametric_study.py` — parametric study support
- `src/ansys/fluent/core/scheduler` — scheduler integration
- `src/ansys/fluent/core/rest` and `src/ansys/fluent/core/ui` — REST / UI helpers
- `src/ansys/fluent/core/utils` — general utilities and setup helpers
- `src/ansys/fluent/core/generated` — generated API layer; treat as generation-managed unless a task explicitly requires otherwise
- `codegen` — generation scripts and schema-driven workflows

## 3. Feature-to-entry-point map

Use this as the first-stop lookup before reading code.

- Launch and session lifecycle
  - package: `src/ansys/fluent/core/launcher`, `src/ansys/fluent/core/session`
  - entry: `pyfluent.launch_fluent()`
  - tests: `tests/test_launcher.py`, `tests/test_launcher_remote.py`, `tests/test_fluent_session.py`, `tests/test_session.py`, `tests/test_pre_post_session.py`

- Meshing
  - package: `src/ansys/fluent/core/meshing`, `src/ansys/fluent/core/session/meshing.py`
  - entry: `pyfluent.launch_fluent(mode="meshing")`, `Meshing`, `PureMeshing`
  - tests: `tests/test_meshing_workflow.py`, `tests/test_new_meshing_workflow.py`, `tests/test_meshing_utilities.py`, `tests/test_pure_mesh_vs_mesh_workflow.py`, `tests/test_server_meshing_workflow.py`

- Solver and solver variants
  - package: `src/ansys/fluent/core/solver`, `src/ansys/fluent/core/session/solver.py`
  - entry: `pyfluent.launch_fluent(mode="solver")`, `Solver`, `SolverAero`, `SolverIcing`, `PrePost`
  - tests: `tests/test_solution_variables.py`, `tests/test_solvermode`, `tests/test_tui_api.py`, `tests/test_public_api.py`, `tests/test_settings_api.py`

- Fields and reduction
  - package: `src/ansys/fluent/core/fields`
  - entry: `ansys.fluent.core.fields.FieldData`, `FieldDataBatch`, `Reduction`, `SolutionVariableData`, `SolutionVariableInfo`
  - tests: `tests/test_field_data.py`, `tests/test_reduction.py`, `tests/test_solution_variables.py`, `tests/test_physical_quantities.py`

- Settings and datamodel
  - package: `src/ansys/fluent/core/services/object_model.py`, generated settings under `src/ansys/fluent/core/generated`
  - entry: runtime session settings object tree and datamodel interfaces
  - tests: `tests/test_settings_api.py`, `tests/test_settings_reader.py`, `tests/test_datamodel_api.py`, `tests/test_datamodel_service.py`, `tests/test_builtin_settings.py`

- File transfer and file sessions
  - package: `src/ansys/fluent/core/file_transfer_service.py`, `src/ansys/fluent/core/session/file.py`, `src/ansys/fluent/core/file_reader`
  - entry: `FileSession`, file-transfer strategies and case/data readers
  - tests: `tests/test_file_session.py`, `tests/test_file_transfer_service.py`, `tests/test_datareader.py`, `tests/test_casereader.py`

- Search and API lookup
  - package: `src/ansys/fluent/core/search.py`
  - entry: `search(...)`
  - tests: `tests/test_search.py`

- Workflow and parametric study
  - package: `src/ansys/fluent/core/workflow.py`, `src/ansys/fluent/core/local_parametric_study.py`
  - entry: workflow objects and parametric study helpers
  - tests: `tests/test_batch_ops.py`, `tests/test_scheduler.py`, `tests/test_slurm_future.py`, `tests/test_systemcoupling.py`, `tests/test_parametric` if present in the repo

- Streaming, event, and service plumbing
  - package: `src/ansys/fluent/core/services/streaming_services`, `src/ansys/fluent/core/services`
  - entry: streaming services, events, monitor and transcript integrations
  - tests: `tests/test_events_manager.py`, `tests/test_streaming_services.py`

- Batch operations and remote execution
  - package: `src/ansys/fluent/core/services/batch_ops.py`, `src/ansys/fluent/core/scheduler`, `src/ansys/fluent/core/docker`
  - entry: batch operations and remote/scheduler launch flows
  - tests: `tests/test_batch_ops.py`, `tests/test_scheduler.py`, `tests/test_slurm_future.py`, `tests/test_launcher_remote.py`

- Expressions, variables, and utility APIs
  - package: `src/ansys/fluent/core/expressions`, `src/ansys/fluent/core/rpvars.py`, `src/ansys/fluent/core/utils`
  - entry: expression helpers, RP vars, utility wrappers
  - tests: `tests/test_rp_vars.py`, `tests/test_lispy.py`, `tests/test_pyconsole.py`, `tests/test_type_stub.py`

- REST and UI helpers
  - package: `src/ansys/fluent/core/rest`, `src/ansys/fluent/core/ui`
  - entry: REST client and UI integrations
  - tests: `tests/test_rest.py`, `tests/test_pyconsole.py`, relevant UI or web tests if present

## 4. High-value architectural rules

- The runtime package and session layer are the primary user-facing entry points.
- Generated code is authoritative for many schema-driven APIs; do not hand-edit it lightly.
- Field-data, reduction, settings, and datamodel access are higher-value feature areas than TUI-only command wrappers.
- For any version-specific path, prefer the generated or compatibility-aware implementation and confirm with the closest tests.
- If a feature is unclear, ask the user before assuming the route or test target.

## 5. Validation strategy

Prefer the closest relevant test target before escalating:

1. import / syntax check
2. nearest feature test file
3. nearest subsystem suite
4. broader integration or Fluent-session tests only when required

Examples:

- reduction bug: start at `src/ansys/fluent/core/fields/reduction.py` and `tests/test_reduction.py`
- file transfer bug: start at `src/ansys/fluent/core/file_transfer_service.py` and `tests/test_file_transfer_service.py`
- launch/session issue: start at `src/ansys/fluent/core/launcher` and `tests/test_launcher.py`
- settings/datamodel bug: start at the generated settings surface and `tests/test_settings_api.py` / `tests/test_datamodel_api.py`
- search bug: start at `src/ansys/fluent/core/search.py` and `tests/test_search.py`

This map is intentionally compact but broad enough to route an agent quickly across the main PyFluent subsystems without scanning the whole repo.
