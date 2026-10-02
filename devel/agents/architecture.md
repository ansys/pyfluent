# Architecture map

Follow `AGENTS.md`. Source paths below are relative to `src/ansys/fluent/core`; test targets and execution requirements live in `devel/agents/testing.md`.

## Project orchestration

Read the diagrams for relationships, then use the owner table for exact edit locations. Arrows show conceptual control/data flow, not class inheritance or every import; dashed arrows show supporting inputs. Fluent itself is an external process, not Python code in this repository.

### Runtime paths

```mermaid
flowchart TB
	user["User scripts / examples / integrations"] --> public["Public exports: ansys.fluent.core"]
	public --> launch["execution/launcher: launch or connect"]
	platforms["Standalone / containers / PIM / Slurm"] --> launch
	resources["execution/docker + scheduler: containers / machine allocation"] -.-> launch
	launch --> connection["connectivity: FluentConnection / channel / cleanup"]
	launch --> sessions["execution/session: BaseSession / active context"]
	connection --> factories["Version-aware gRPC and high-level service factories"]
	factories --> sessions
	sessions --> meshing["meshing/session: Meshing / PureMeshing"]
	sessions --> solver["solver/session: Solver and variants"]
	meshing --> workflows["Pre-set meshing workflows + shared workflow wrappers"]
	meshing --> model["Datamodel / TUI wrappers + datamodel cache"]
	workflows --> model
	solver --> settings["solver/flobject: settings objects / built-ins"]
	solver --> model
	sessions --> fields["fields: field data / solver reductions and solution variables"]
	sessions --> streaming["Events / monitors / transcript / data streaming"]
	settings --> services["services: abstractions and high-level wrappers"]
	model --> services
	fields --> services
	streaming --> services
	services --> grpc["_grpc_services: backend implementations / protocol versions"]
	proto["External ansys-api-fluent: generated protobuf / gRPC schemas"] -.-> grpc
	grpc --> channel["gRPC channel managed by FluentConnection"]
	channel --> fluent["External Fluent server"]
	user --> http["REST client + independent HttpSolver"]
	http --> restsettings["services/rest_settings + shared flobject settings runtime"]
	restsettings --> transport["rest: client / HTTP transport"]
	transport --> web["External Fluent web server: 27.1+"]
	user --> offline["FileSession + file_reader: case/data-backed APIs"]
	files["Case / data assets"] --> offline
	transfer["connectivity: file/data transfer strategies"] -.-> sessions
	transfer -.-> files
```

- Settings, datamodel and TUI are distinct surfaces; they share session/service infrastructure but have different wrappers and schemas. Fields use runtime APIs, not generated settings wrappers.
- Expression/naming helpers support variable access; RP/Scheme helpers use services. Parametric studies orchestrate sessions; system coupling integrates solver operations with external coupled workflows.
- UI integrates session web/Jupyter presentation. Configuration, diagnostics, utilities, shared types and example downloads support the runtime across layers; search reads the generated API index rather than being a transport.

### Generation and repository tooling

Paths in this diagram are repository-relative. Detailed commands and prerequisites remain in `devel/agents/workflows.md` rather than being duplicated here.

```mermaid
flowchart LR
	driver["codegen/allapigen.py: live generation driver"] --> live["Meshing + solver-icing sessions: static info / workflow tasks"]
	live --> generators["src/ansys/fluent/core/codegen: schema generators"]
	generators --> output["generated: versioned settings / datamodel / TUI / task stubs + shared built-ins / API index"]
	output -.-> runtime["Runtime wrappers / built-in settings / search"]
	output -.-> docs["doc: API RST generators + Sphinx sources / gallery"]
	examples["examples: end-to-end user workflows"] --> runtime
	examples --> docs
	tests["tests: unit / live Fluent / version-mode / external integration"] --> runtime
	tests --> generators
	packaging["pyproject.toml + requirements: dependencies / extras / build and tool config"] -.-> runtime
	packaging -.-> tests
	ci[".github/workflows + .ci + Makefile: build / generate / test / docs / release lanes"] --> driver
	ci --> tests
	ci --> docs
	ci --> packaging
	guidance["AGENTS.md + devel/agents: routing / validation / operating rules"] -.-> work["Agent / contributor work"]
	notes["devel: engineering notes / investigations"] -.-> work
	work --> runtime
	work --> generators
	work --> tests
```

## Source owners and entry points

| Feature / public surface | Source owner |
| --- | --- |
| Public exports, legacy aliases; configuration/environment defaults | `__init__.py`; `module_config.py` |
| `launch_fluent()`, `connect_to_fluent()`; standalone/container/PIM/Slurm | `execution/launcher/launcher.py`; `execution/launcher/standalone_launcher.py`, `execution/launcher/container_launcher.py`, `execution/launcher/pim_launcher.py`, `execution/launcher/slurm_launcher.py` |
| Base session, `using()`, file-backed `FileSession` | `execution/session/session.py`; `execution/session/file.py` |
| gRPC connection lifetime, health checks, cleanup; file/data transfer | `connectivity/fluent_connection.py`; `connectivity/file_transfer_service.py`, `connectivity/data_transfer.py` |
| `Meshing`, `PureMeshing`; pre-set workflows and solver transitions | `meshing/session`; `meshing/meshing_workflow.py`, `meshing/meshing_workflow_old.py`; shared `workflow.py`, `workflow_old.py` |
| `Solver`, `SolverAero`, `SolverIcing`, `SolverLite`, `PrePost`; solve-mode APIs | `solver/session`; settings runtime in `solver/flobject.py` |
| `solver.settings`; built-in settings exports from `ansys.fluent.core.solver` | `solver/flobject.py`, `solver/settings_builtin_bases.py`, `solver/settings_builtin_data.py`; `services/settings.py` |
| Meshing datamodel roots; `session.tui` | `services/object_model.py`, `_data_model_cache.py`; `services/text_interface.py` |
| `session.fields.field_data`, `.new_batch()`; solver fields: `.reduction`, `.solution_variable_data`, `.solution_variable_info` | `fields/field_data/live_field_data.py`; `fields/reduction/reduction.py`; `fields/solution_variables/solution_variables.py` |
| Service abstractions/wrappers; events, monitors, transcripts and datamodel/field streaming | `services`; `services/streaming_services`; gRPC implementations in `_grpc_services` |
| Case/data readers and file-backed fields | `file_reader`; `execution/session/file.py` |
| `search(...)`, logging, journaling, exceptions | `diagnostics`; search implementation `diagnostics/search.py`, API index generator `codegen/api_tree.py` |
| Parametric studies; coupled simulation | `local_parametric_study.py`; `system_coupling.py` |
| Batch service calls; separately, queued/remote execution | `services/batch_ops.py`; `execution/scheduler`, `execution/docker`, launchers above |
| Expression construction/evaluation, RP variables, Scheme, file S-expressions | `expressions`; `rpvars.py`; `services/scheme_interpreter.py`; `file_reader/lispy.py` |
| `rest.connect_to_webserver()`, `FluentRestClient`, `HttpSolver` | `rest/client.py`, `rest/transport.py`, `services/rest_settings.py`, `solver/session/http_solver.py` |
| Web/Jupyter UI; utilities/setup; example downloads/assets | `ui`; `utils`; `examples` |
| Generated settings/datamodel/TUI/built-ins/search index; generation implementation | `generated`; `codegen/settingsgen.py`, `codegen/datamodelgen.py`, `codegen/tuigen.py`, `codegen/builtin_settingsgen.py`, `codegen/api_tree.py` (repository-root `codegen/allapigen.py` is the live-Fluent driver) |
| Shared types/launcher arguments; descriptor naming for expressions/fields/solution variables | `_types.py`; `_variable_strategies` |
| Legacy standalone datamodel-server helper, not a normal session entry point | `_stand_alone_datamodel_client/_datamodel_client.py`; verify its old imports/dependencies before use |

### Runtime contracts

- `FluentMode` in `execution/launcher/launch_options.py` accepts `meshing`, `pure_meshing`, `solver` (default), `solver_icing`, `solver_aero`, `pre_post`. The first five route to their corresponding sessions; `pre_post` currently maps to `Solver`. Do not infer launch support from the existence of a session class.
- `BaseSession` and `using()` live in execution; mode-specific sessions live in meshing/solver. `FileSession` is file-backed, not a live solver subclass; `HttpSolver` is independent of `BaseSession` and gRPC infrastructure.
- Solver settings objects use `solver/flobject.py` over a settings service. `get_root()` builds classes from static info when `config.use_runtime_python_classes` is enabled or the generated settings file is missing; otherwise it loads version-specific generated classes.
- Generated output uses version directories under `generated`, plus shared `generated/solver` and `generated/api_tree` data. Versions present in a local checkout depend on generation/install state; do not assume every supported version is generated locally.
- Legacy names registered in `__init__.py` are compatibility aliases, not current source locations. Start from the implementation path and check exports separately.

## Architectural rules

- The runtime package and session layer are the primary user-facing entry points.
- Generated code is authoritative for many schema-driven APIs; do not hand-edit it lightly.
- Field-data, reduction, settings, and datamodel access are higher-value feature areas than TUI-only command wrappers.
- For any version-specific path, prefer the generated or compatibility-aware implementation and confirm with the closest tests.
- If a feature is unclear, ask the user before assuming the route or test target.
- Fix runtime navigation/behavior in its owning wrapper or service; change generation logic for schema-output defects rather than hand-editing generated output.

Session, workflow, service and schema behavior varies by Fluent version, mode, packaging and environment. Check the closest compatibility-aware implementation and test rather than assuming one path.

File-backed APIs need no live server themselves; reader tests may need assets/downloads or Fluent. Search consumes generated API-index data and semantic search needs NLTK data. `HttpSolver` targets Fluent 27.1+; REST settings can use runtime classes without generated files. UI needs `ui` / `ui-jupyter` extras; Python-console tests are not UI-rendering coverage.
