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

Use this as the first-stop lookup before reading code. Each section follows the same repo-aligned template:

- module path
- public entry point
- feature intent
- tests to run
- generated/version-specific notes

### 3.1 Launch and session lifecycle

- module path: `src/ansys/fluent/core/launcher`, `src/ansys/fluent/core/session`, `src/ansys/fluent/core/__init__.py`
- public entry point: `pyfluent.launch_fluent()`, session classes such as `Solver`, `Meshing`, `PureMeshing`, `FileSession`, and `PrePost`
- feature intent: create Fluent sessions, switch runtime modes, and manage lifecycle, health checks, and command routing
- tests to run: `tests/test_launcher.py`, `tests/test_launcher_remote.py`, `tests/test_fluent_session.py`, `tests/test_session.py`, `tests/test_pre_post_session.py`
- generated/version-specific notes: session behavior is runtime-sensitive and often depends on Fluent version and launch mode; prefer the session and launcher entry points before reading the generated tree

### 3.2 Meshing workflows

- module path: `src/ansys/fluent/core/meshing`, `src/ansys/fluent/core/session/meshing.py`
- public entry point: `pyfluent.launch_fluent(mode="meshing")`, `Meshing`, `PureMeshing`
- feature intent: meshing mode workflows, meshing-specific operations, and transitions between mesh and solver workflows
- tests to run: `tests/test_meshing_workflow.py`, `tests/test_new_meshing_workflow.py`, `tests/test_meshing_utilities.py`, `tests/test_pure_mesh_vs_mesh_workflow.py`, `tests/test_server_meshing_workflow.py`
- generated/version-specific notes: workflow implementation may vary by Fluent packaging and mesh mode compatibility; validate against the nearest meshing tests before assuming a single path

### 3.3 Solver and solver variants

- module path: `src/ansys/fluent/core/solver`, `src/ansys/fluent/core/session/solver.py`, `src/ansys/fluent/core/generated`
- public entry point: `pyfluent.launch_fluent(mode="solver")`, `Solver`, `SolverAero`, `SolverIcing`, `PrePost`
- feature intent: solve-mode sessions, solver-specific APIs, and generated object-model surfaces
- tests to run: `tests/test_solution_variables.py`, `tests/test_solvermode`, `tests/test_tui_api.py`, `tests/test_public_api.py`, `tests/test_settings_api.py`
- generated/version-specific notes: many solver and settings entry points are generation-managed; treat the generated layer as authoritative unless the task explicitly requires a runtime wrapper change

### 3.4 Field data, reduction, and solution variables

- module path: `src/ansys/fluent/core/fields`, `src/ansys/fluent/core/services`
- public entry point: `ansys.fluent.core.fields.FieldData`, `FieldDataBatch`, `Reduction`, `SolutionVariableData`, `SolutionVariableInfo`
- feature intent: access live field data, compute reductions, and inspect solution-variable metadata and values
- tests to run: `tests/test_field_data.py`, `tests/test_reduction.py`, `tests/test_solution_variables.py`, `tests/test_physical_quantities.py`
- generated/version-specific notes: field and solution-variable paths are usually part of the runtime API surface rather than generated model wrappers, but they can still depend on service behavior and Fluent schema versioning

### 3.5 Settings and datamodel

- module path: `src/ansys/fluent/core/generated`, `src/ansys/fluent/core/services/object_model.py`, session settings surfaces
- public entry point: runtime session settings object tree and datamodel interfaces
- feature intent: expose Fluent settings and object-model navigation in a Pythonic, structured form
- tests to run: `tests/test_settings_api.py`, `tests/test_settings_reader.py`, `tests/test_datamodel_api.py`, `tests/test_datamodel_service.py`, `tests/test_builtin_settings.py`
- generated/version-specific notes: this is a core generation-managed area; if the behavior is schema-driven, inspect the generated code before editing runtime wrappers

### 3.6 File transfer and file sessions

- module path: `src/ansys/fluent/core/file_transfer_service.py`, `src/ansys/fluent/core/session/file.py`, `src/ansys/fluent/core/file_reader`
- public entry point: `FileSession`, file-transfer strategies, and case/data readers
- feature intent: read and transfer Fluent case/data files and operate against file-backed session workflows
- tests to run: `tests/test_file_session.py`, `tests/test_file_transfer_service.py`, `tests/test_datareader.py`, `tests/test_casereader.py`
- generated/version-specific notes: file behavior is often environment-sensitive and may depend on Fluent runtime setup; treat reader/service tests as the primary validation target before broader integration tests

### 3.7 Search and API lookup

- module path: `src/ansys/fluent/core/search.py`
- public entry point: `search(...)`
- feature intent: discover Fluent objects and APIs by name or object path across the exposed model surface
- tests to run: `tests/test_search.py`
- generated/version-specific notes: search is usually layer-aware and object-model dependent, so it should be validated against the nearest public lookup tests when schema or object names change

### 3.8 Workflow and parametric study

- module path: `src/ansys/fluent/core/workflow.py`, `src/ansys/fluent/core/workflow_old.py`, `src/ansys/fluent/core/local_parametric_study.py`
- public entry point: workflow objects and parametric-study helpers
- feature intent: hold automation workflows, batch operations, and parametric study orchestration over Fluent sessions
- tests to run: `tests/test_batch_ops.py`, `tests/test_scheduler.py`, `tests/test_slurm_future.py`, `tests/test_systemcoupling.py`, `tests/test_parametric` if present in the repo
- generated/version-specific notes: these workflows often mix runtime orchestration and generated API behavior; prefer the specific workflow test cluster rather than broad session tests

### 3.9 Streaming, events, and service plumbing

- module path: `src/ansys/fluent/core/services`, `src/ansys/fluent/core/services/streaming_services`
- public entry point: streaming services, event managers, monitor hooks, and transcript integrations
- feature intent: provide asynchronous service and event plumbing for Fluent runtime interactions
- tests to run: `tests/test_events_manager.py`, `tests/test_streaming_services.py`
- generated/version-specific notes: event and streaming behavior is usually service-layer specific and should be validated near the service/monitor path rather than broad session tests

### 3.10 Batch operations and remote execution

- module path: `src/ansys/fluent/core/services/batch_ops.py`, `src/ansys/fluent/core/scheduler`, `src/ansys/fluent/core/docker`
- public entry point: batch operation helpers and remote scheduler launch flows
- feature intent: orchestrate remote or queued Fluent execution patterns for larger automation work
- tests to run: `tests/test_batch_ops.py`, `tests/test_scheduler.py`, `tests/test_slurm_future.py`, `tests/test_launcher_remote.py`
- generated/version-specific notes: remote execution can change significantly by environment and Fluent packaging; start with the scheduler and batch tests before any broad integration path

### 3.11 Expressions, variables, and utility APIs

- module path: `src/ansys/fluent/core/expressions`, `src/ansys/fluent/core/rpvars.py`, `src/ansys/fluent/core/utils`
- public entry point: expression helpers, RP variables, and general utility wrappers
- feature intent: provide expression evaluation, variable access, and generic helper logic around Fluent operations
- tests to run: `tests/test_rp_vars.py`, `tests/test_lispy.py`, `tests/test_pyconsole.py`, `tests/test_type_stub.py`
- generated/version-specific notes: this area is often runtime helper-driven rather than schema-driven, but some behavior may still reflect Fluent version-specific naming or object semantics

### 3.12 REST and UI helpers

- module path: `src/ansys/fluent/core/rest`, `src/ansys/fluent/core/ui`
- public entry point: REST client interfaces and UI integration helpers
- feature intent: support REST and UI-oriented interactions around Fluent sessions and tooling
- tests to run: `tests/test_rest.py`, `tests/test_pyconsole.py`, and any UI/web tests present in the repository
- generated/version-specific notes: REST/UI integrations are usually not generation-managed; they are more likely to be compatibility wrappers and environment-dependent adapters

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
