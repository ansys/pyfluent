# Architecture map for AI agents

This document is intentionally narrow and repo-specific. It gives agents the minimum map needed to navigate PyFluent without requiring a huge root-level instruction file.

## 1. Product shape

PyFluent exposes a Pythonic API on top of Ansys Fluent. The architecture is organized around the layers that matter most for correctness and maintainability:

1. Fluent launch and session management
2. Settings and datamodel surfaces
3. Generated API layer for Fluent objects and commands
4. Runtime helpers and integration code
5. Tests, docs, and examples

The TUI-oriented command access layer is present, but it is not the primary architectural focus for most agent work.

## 2. Key directories

- `src/ansys/fluent/core` — primary runtime code and package entry points
- `src/ansys/fluent/core/generated` — generated API code; usually not the place for hand-written changes
- `codegen` — generation scripts and schema-driven workflows
- `tests` — behavioral validation and regression coverage
- `doc` — Sphinx docs and generated API docs
- `examples` — usage examples
- `devel` — engineering and repo notes

## 3. High-level architectural boundaries

### Runtime and session layer

This is the core operational layer. It owns the Fluent session lifecycle, launch behavior, health checks, command routing, and the Python-facing abstractions that most users call.

Typical responsibilities include:

- launching Fluent from local or managed environments
- session lifecycle and health checks
- command dispatch and result handling
- service-level integration around Fluent operations
- settings/datamodel access wrappers

The main entry point is `pyfluent.launch_fluent()` in the launcher module. It returns a mode-specific session such as solver or meshing variants.

### Settings and datamodel layer

This layer is central to correctness in PyFluent. Much of the project surface is built around structured Fluent settings, datamodel access, and generated object mappings.

This is a high-value area for agent understanding because bugs here often affect API behavior rather than isolated UI concerns.

### Generated API layer

The generated API layer is tightly coupled to Fluent versioned schema and command definitions. It is often the authoritative contract for schema-driven behavior.

Important rule:

- generated files are often authoritative for schema-driven APIs
- hand edits are generally risky and should be justified by a generation or API contract decision

### Field and solution data layer

The field-data subsystem is a distinct feature area rather than a generic utility. It is exposed via `ansys.fluent.core.fields` and includes:

- `FieldData` / `FieldDataBatch` for live field access
- `Reduction` for reduction operations
- `SolutionVariableData` / `SolutionVariableInfo` for solution-variable metadata and data access

This layer is the primary entry point for field-level workflows and is usually validated with `test_field_data.py` and related solution-variable coverage.

### Test and documentation layer

The project maintains behavior-focused tests in `tests/` and documentation in `doc/` and `examples/`. These are the main validation and guidance surfaces for making safe changes.

## 4. Feature entry points and capability map

Use these as the first-stop map for feature work:

- Session launch: `pyfluent.launch_fluent()` in `src/ansys/fluent/core/launcher/launcher.py`
- Solver and meshing sessions: `FluentMode.SOLVER`, `FluentMode.MESHING`, `FluentMode.PURE_MESHING`, and the session objects returned from the launch call
- Field data: `ansys.fluent.core.fields.FieldData`, `FieldDataBatch`, `Reduction`, `SolutionVariableData`
- Settings/datamodel access: session-level settings and datamodel surfaces exposed from the runtime session objects
- File transfer and persistence: file-session and transfer service modules under `src/ansys/fluent/core`

This is the capability map agents should keep in memory before drilling into a specific module.

## 5. Feature-by-feature inventory

This is the practical subsystem map agents should keep in memory when working on PyFluent.

### 5.1 Session and lifecycle

Primary responsibility:

- launch Fluent sessions
- manage session lifecycle and health checks
- choose solver, meshing, or specialized session modes

Key entry points:

- `pyfluent.launch_fluent()` in `src/ansys/fluent/core/launcher/launcher.py`
- `ansys.fluent.core.session` exports concrete session classes such as `Solver`, `Meshing`, `PureMeshing`, `FileSession`, `PrePost`
- `ansys.fluent.core.__init__` re-exports the public entry points and exposes `Fluent` as the top-level session-oriented class

Likely validation targets:

- `tests/test_launcher.py`
- `tests/test_launcher_remote.py`
- `tests/test_fluent_session.py`
- `tests/test_session.py`
- `tests/test_pre_post_session.py`

Confidence:

- High. These are repo-backed, public session entry points.

### 5.2 Meshing workflows

Primary responsibility:

- meshing mode sessions
- workflow wrappers and meshing-specific operations
- transition between meshing and solver flows

Key entry points:

- `src/ansys/fluent/core/meshing/__init__.py`
- `src/ansys/fluent/core/session/meshing.py` and related session classes
- meshing workflow classes under the meshing package and related workflow modules

Likely validation targets:

- `tests/test_meshing_workflow.py`
- `tests/test_new_meshing_workflow.py`
- `tests/test_meshing_utilities.py`
- `tests/test_pure_mesh_vs_mesh_workflow.py`
- `tests/test_server_meshing_workflow.py`

Confidence:

- High for workflow entry points and the public meshing API surface.
- Some details are version-specific; when a workflow changes behavior by Fluent version, the generated or compatibility path should be checked before assuming a single implementation.

### 5.3 Solver and solver-mode sessions

Primary responsibility:

- solver sessions and specialized solver variants
- solver-mode integration and setup
- solver-specific APIs and add-ons such as aero and icing flows

Key entry points:

- `src/ansys/fluent/core/solver/__init__.py`
- `src/ansys/fluent/core/session/solver.py`
- specialized session modules for solver variants and pre/post flows
- generated settings surface under `src/ansys/fluent/core/generated`

Likely validation targets:

- `tests/test_solution_variables.py`
- `tests/test_solvermode/`
- `tests/test_tui_api.py`
- `tests/test_public_api.py`
- `tests/test_settings_api.py`

Confidence:

- High for the public solver entry points and generated settings surfaces.
- Some exact internal boundaries may be generated and version-bound; this should be treated as generation-managed code unless the repo explicitly says otherwise.

### 5.4 Fields, reductions, and solution variables

Primary responsibility:

- field-data access and reduction operations
- solution-variable metadata and data retrieval
- Fluent field and solution data workflows

Key entry points:

- `src/ansys/fluent/core/fields/__init__.py`
- `FieldData`, `FieldDataBatch`, `Reduction`, `SolutionVariableData`, and `SolutionVariableInfo`
- lower-level services in `src/ansys/fluent/core/services` and gRPC field-data service modules

Likely validation targets:

- `tests/test_field_data.py`
- `tests/test_solution_variables.py`
- `tests/test_physical_quantities.py`

Confidence:

- High. This is a well-defined feature cluster with clear public entry points and direct test coverage.

### 5.5 Settings and datamodel surfaces

Primary responsibility:

- Fluent settings access
- datamodel object navigation
- settings readers and schema-backed behaviors

Key entry points:

- session-level settings objects exposed from the runtime session
- generated settings modules under `src/ansys/fluent/core/generated`
- settings readers and model wrappers under the core runtime package

Likely validation targets:

- `tests/test_settings_api.py`
- `tests/test_settings_reader.py`
- `tests/test_datamodel_api.py`
- `tests/test_datamodel_service.py`
- `tests/test_builtin_settings.py`

Confidence:

- High for test coverage and public API surface.
- Very high generation dependence: if a bug is schema-driven, the generated layer should be treated as the source of truth before modifying runtime wrappers.

### 5.6 File transfer and file-session workflows

Primary responsibility:

- file session access
- file transfer service behavior
- case/data reader workflows
- file-backed Fluent workflows

Key entry points:

- `src/ansys/fluent/core/session/file.py`
- `src/ansys/fluent/core/file_transfer_service.py`
- `src/ansys/fluent/core/file_reader` and related reader modules

Likely validation targets:

- `tests/test_file_session.py`
- `tests/test_file_transfer_service.py`
- `tests/test_datareader.py`
- `tests/test_casereader.py`

Confidence:

- High for the public file-related API surface.
- Some lower-level file-transfer behavior may depend on environment and Fluent runtime setup, so these are not always the cheapest validation targets.

### 5.7 Public API and compatibility surface

Primary responsibility:

- package-level exports
- deprecations and compatibility shims
- high-level user-facing API stability

Key entry points:

- `src/ansys/fluent/core/__init__.py`
- compatibility and deprecation layers within the core package

Likely validation targets:

- `tests/test_public_api.py`
- `tests/test_deprecate.py`
- `tests/test_flobject.py`

Confidence:

- High for visible API/compatibility behaviors.

## 6. How to choose the right validation path

When a patch is in doubt, prefer this order:

1. import/syntax check
2. nearest unit-level or API-level test
3. nearest feature test cluster
4. broader Fluent-session or integration tests only if required by the feature

Examples:

- change in launch/session lifecycle → start with `test_launcher.py` or `test_fluent_session.py`
- change in meshing flow → use `test_meshing_workflow.py` and related meshing tests
- change in fields or solution variables → use `test_field_data.py` and `test_solution_variables.py`
- change in settings/datamodel behavior → use `test_settings_api.py` and `test_datamodel_api.py`
- change in file transfer or file reading → use the file-session and reader tests

## 7. Agent-specific heuristics

- If a change looks schema-driven, inspect the generated layer before editing runtime code.
- If a change affects public APIs, check tests and docs together.
- If a bug is in Fluent integration behavior, validate against the likely session/launcher and settings/datamodel path.
- If there is uncertainty about generated vs hand-authored code, search for generated markers before editing.
- When a mapping is unclear due to version-specific behavior, do not assume a single implementation; prefer the generated or compatibility-aware path and confirm with the nearest repo tests.

## 8. Cost-aware usage guidance

To reduce token use and improve answer quality:

- read the local runtime and settings/datamodel entrypoints first
- search for the feature name before broad file scanning
- avoid reading the full generated tree unless the behavior is explicitly generated
- prefer the specific test file closest to the changed behavior
- treat large Fluent-session tests as escalation points, not default validation paths

This document is a map, not a manual. It should orient the agent and keep the work focused, not replace targeted investigation.
