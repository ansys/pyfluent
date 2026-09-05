# Plan: Runtime Type-Checking Support in PyFluent (issue #4739)

Add opt-in runtime type-checking to PyFluent using **beartype**, behind a thin swappable
wrapper, activated by a new `pyfluent.config` option, and enabled in CI unit tests.

---

## Research verdict: why beartype, and is it feasible?

### Candidates evaluated
| Library | Per-call cost | Deps | Coerces? | Verdict |
|---|---|---|---|---|
| **beartype** | O(1), ~1 microsec (random one-way walk) | none, pure Python, MIT | No | **Recommended** |
| typeguard | O(n) — deep-walks entire containers every call | none, MIT | No | Rejected: fatal on PyFluent hot paths |
| pydantic `@validate_call` | O(n) + Rust core | pydantic + pydantic-core (compiled) | **Yes, by default** | Rejected: silently mutates API semantics |
| jaxtyping | array shape/dtype only | needs beartype/typeguard underneath | No | Complementary, not a replacement |
| hand-rolled isinstance guards | manual | none | No | Rejected: unmaintainable at PyFluent's API surface |

### Why beartype wins for PyFluent specifically
1. **O(1) checking is the decisive factor.** PyFluent routinely passes multi-million element
   payloads through `services/field_data.py`, `SettingsBase.get_state/set_state`,
   `Group.to_scheme_keys()` / `to_python_keys()`. typeguard type-checks *every* element of
   *every* nested container on *every* call (documented worst case: ~107 minutes for a
   1e9-element nested list). beartype samples one random element per nesting level, giving
   constant ~1 microsec regardless of payload size. Only beartype is viable on these paths.
2. **Zero transitive dependencies, pure Python, MIT.** PyFluent is redistributed inside Ansys
   installations; adding a compiled Rust wheel (pydantic-core) is a supply-chain and packaging
   cost. beartype adds one pure-Python wheel.
3. **No coercion.** pydantic's `@validate_call` coerces `"3"` -> `3`, `1` -> `True` etc. That
   would silently change PyFluent's public API behaviour and defeat the purpose (issue #1003
   wants *Pythonic error messages for wrong data types*, not silent conversion).
4. **Non-invasive activation.** `beartype.claw.beartype_package()` decorates every annotated
   callable/class at import time via an AST import hook — no source changes required, and it
   can be switched off entirely so shipped-default behaviour is unchanged.
5. **Granular opt-out** via `typing.no_type_check` or `beartype(conf=BeartypeConf(strategy=O0))`
   — required for flobject's gRPC proxy classes.
6. **Version support** matches `requires-python = ">=3.10,<3.15"`; full PEP 604/585/563/673
   support; pyright/mypy-clean so IDE completion is unaffected.

### Feasibility: YES. Blockers verified and each has a concrete fix.

1. **PR #4973's stated blocker is a one-line fix, not a blocker.**
   That PR (closed, unmerged) added a comment saying `beartype_this_package()` cannot be used
   because `ansys` / `ansys.fluent` are PEP 420 namespace packages, and fell back to manually
   decorating functions. The *symptom* is real but the *conclusion* was wrong:
   `beartype_this_package()` derives its target from `__name__.rpartition(".")[0]`, which from
   `src/ansys/fluent/core/__init__.py` resolves to `ansys.fluent` — the namespace package, which
   has no `__init__.py`. The fix is to name the package explicitly:
   `beartype_package("ansys.fluent.core")`. Confirmed: `src/ansys/__init__.py` and
   `src/ansys/fluent/__init__.py` do not exist; the 20 `__init__.py` files all live at
   `ansys/fluent/core/` and below. Claw's finder matches on module-name prefix, so a namespace
   parent is irrelevant. Also note the upstream link cited in that PR (beartype issue #286) is a
   TypeVar Q&A discussion, unrelated to namespace packages.
2. **Dynamically generated settings classes are a non-issue.**
   `get_cls()` / `_create_generated_class()` in `solver/flobject.py` build classes with `type()`
   at runtime from Fluent metadata. `beartype.claw` transforms *source ASTs at import*, so it
   never sees them, and they carry no `__annotations__`, so `@beartype` on them is a no-op.
   They are neither checked nor slowed — a coverage gap, not a failure mode.
3. **`Solver`'s conditional base class is a genuine trap.**
   `class Solver(BaseSession, settings_root.root if TYPE_CHECKING else object)` in
   `session/solver.py` means the runtime MRO differs from the static MRO. Any annotation naming
   `settings_root.root` / `preferences_root` / `main_menu` is unresolvable at runtime and will
   raise `BeartypeCallHintForwardRefException` at call time. Must be audited and either given a
   runtime-importable annotation or excluded.
4. **PEP 563 / forward-ref exposure is small and bounded** — not a rewrite:
   - 16 modules use `from __future__ import annotations`
   - 14 `if TYPE_CHECKING:` blocks
   - ~13 implicit-Optional params (`x: SomeType = None`)
   - `_types.py`: `PathType: TypeAlias = "os.PathLike[str] | str"` is a *quoted* alias, plus 4
     quoted TypedDict members
5. **Decorator stacking**: `utils/deprecate.py` `deprecate_arguments` / `deprecate_function` use
   `functools.wraps` but do **not** set `__signature__`. Stacked under beartype the wrapper's
   `*args/**kwargs` is what gets introspected. Fix: `wrapper.__signature__ = inspect.signature(func)`
   (PR #4973 already contained this fix plus two tests — reusable).
6. **`@overload`** at `launcher/launcher.py` (8) and `session/session.py` (4): beartype ignores
   overload stubs and checks the implementation signature only. Non-issue provided the
   implementation signature is a true union superset.
7. **flobject proxy classes** (`Base`, `SettingsBase`, `Group`, `WildcardPath`, `NamedObject`,
   `ListObject`, `Action`) define `__setattr__`/`__getattr__` that proxy to gRPC. Decorating them
   risks unintended network calls during introspection and attribute-write failures. Mark with
   `@typing.no_type_check` (exactly as PR #4973 did).

---

## Architecture

### Activation ordering constraint (important)
`src/ansys/fluent/core/__init__.py` eagerly imports the whole package at the top
(`from ansys.fluent.core.module_config import *` is the first statement). `beartype.claw` only
affects modules imported *after* the hook is installed. Therefore the hook must be installed as
the **very first executable statement** of `__init__.py`, before `module_config` is imported.
That means the activation switch must be read from `os.environ` directly by a dependency-free
module, and the `Config` descriptor mirrors it for introspection.

Consequence: `pyfluent.config.runtime_type_checking = True` set *after* import cannot
retroactively hook already-imported modules. Document this; make the setter emit a warning when
it disagrees with the installed state.

### New module: `src/ansys/fluent/core/_type_checking.py`
Sibling of `module_config.py`, **no** PyFluent imports (avoids circular import at hook time).
Public surface (the swappable wrapper mkundu1 asked for):
- `TypeCheckBackend` enum / registry: `{"beartype": _BeartypeBackend, "none": _NullBackend}`
- `runtime_type_check(obj)` — decorator; delegates to active backend, no-op when disabled
- `no_runtime_type_check(obj)` — opt-out; maps to `typing.no_type_check`
- `is_type_checking_enabled() -> bool`
- `install_import_hook() -> bool` — reads `PYFLUENT_RUNTIME_TYPE_CHECKING`, calls
  `beartype.claw.beartype_package("ansys.fluent.core", conf=...)`; returns False and warns
  (never raises) if `beartype` is not installed
- All `beartype` imports are local/lazy so the module is importable without beartype present.

### Config option: `src/ansys/fluent/core/module_config.py`
Follow the existing `_ConfigDescriptor` pattern with the `#:` doc comment (auto-documented):
```
#: Whether to enable runtime type-checking of the PyFluent API, defaults to False.
runtime_type_checking = _ConfigDescriptor["Config"](
    lambda instance: instance._env.get("PYFLUENT_RUNTIME_TYPE_CHECKING") == "1"
)
```
(no `deprecated_var` second arg — this is a new option with no legacy module-level variable).
**Recommended default: `False`** (opt-in). Turning it on by default would convert working
user code into hard `BeartypeCallHintParamViolation` errors — a breaking change for a library
whose API is duck-typed in places.

### Dependency
`pyproject.toml`: add `beartype>=0.19` to a new `[project.optional-dependencies] type-checking`
group **and** to the existing `tests` group. Not a hard runtime dependency, because the feature
is off by default. Add the beartype MIT license text under `LICENSES/` per repo convention.

---

## Phases

### Phase 1 — Abstraction layer + config (blocks everything else)
1. Create `src/ansys/fluent/core/_type_checking.py` as described.
2. Add `runtime_type_checking` descriptor to `module_config.py`.
3. Add `install_import_hook()` call as first statement in `core/__init__.py`.
4. `pyproject.toml`: add `beartype>=0.19` to `type-checking` + `tests` extras; add
   `LICENSES/beartype-MIT.txt`.
5. New `tests/test_runtime_type_checking.py`: hook installs/doesn't install per env var;
   `runtime_type_check` is a no-op when disabled; violation raises when enabled; graceful
   degradation when beartype is absent (simulate via `sys.modules` patch).

### Phase 2 — Annotation cleanup (parallelisable; 2a/2b/2c independent)
2a. **Implicit-Optional** (~13 sites): `solver/flobject.py:753`,
    `codegen/builtin_settingsgen.py:179` (fix the *emitted* string too),
    `search.py:303`, `meshing/meshing_workflow_new.py:268`,
    `rest/transport.py:51,134,198`, `legacy/local_parametric_study.py:333`,
    `utils/get_completer_info.py:44,46`, `services/object_model.py` (3).
2b. **Forward refs / PEP 563**: unquote `PathType` and the 4 quoted TypedDict members in
    `_types.py`; drop `from __future__ import annotations` where it only exists to enable
    self-references (16 modules — evaluate individually, keep where genuinely needed);
    audit the 14 `TYPE_CHECKING` blocks for names used in *runtime-evaluated* annotations,
    especially `session/solver.py` (`FluentConnection`, `settings_root`, `preferences_root`,
    `main_menu`) and `fields/field_data_interfaces.py` (`VariableDescriptor`).
2c. **Decorator/opt-out fixes**: set `wrapper.__signature__` in both decorators in
    `utils/deprecate.py` (+ the 2 tests from PR #4973 in `tests/test_deprecate.py`);
    add `@typing.no_type_check` to `Base`, `SettingsBase`, `Group`, `WildcardPath`,
    `NamedObject`, `ListObject`, `Action` and to `get_cls()` in `solver/flobject.py`.

### Phase 3 — Iterate to green (depends on Phase 1 + 2)
6. Run the full unit suite locally with the hook on; triage each violation as either
   (a) a genuine annotation bug -> fix the annotation, (b) a genuine caller bug -> fix the call,
   (c) an unsupportable dynamic construct -> `no_runtime_type_check`.
   Expect the bulk of the work here; keep a running list in the PR description.

### Phase 4 — CI (depends on Phase 3 being green)
7. Add `PYFLUENT_RUNTIME_TYPE_CHECKING: 1` to the **Unit Testing** job in
   `.github/workflows/ci.yml` (job `name: Unit Testing`, line ~503; step line ~571 runs
   `make unittest-dev-${MATRIX_VERSION}`). Set it at the *step* level, not the workflow-global
   `env:` block, so codegen/doc jobs are unaffected.
8. Keep it out of the nightly `unittest-all-*` targets initially to limit blast radius.

### Phase 5 — Docs + changelog
9. The `#:` comment on the descriptor auto-documents the config option; add a short prose
   section to the configuration docs covering: opt-in nature, the env var, the
   import-ordering caveat, and how to opt a function out.
10. `doc/changelog.d/<PR#>.added.md`.

---

## Relevant files
- `src/ansys/fluent/core/_type_checking.py` — **new**, backend abstraction + import hook
- `src/ansys/fluent/core/__init__.py` — install hook as first statement (line ~25, before
  `from ansys.fluent.core.module_config import *`)
- `src/ansys/fluent/core/module_config.py` — `_ConfigDescriptor` pattern, add
  `runtime_type_checking` next to the other bool options (~line 108)
- `src/ansys/fluent/core/_types.py` — unquote `PathType` (line ~44) and 4 TypedDict members
- `src/ansys/fluent/core/solver/flobject.py` — `@no_type_check` on proxy classes / `get_cls`
- `src/ansys/fluent/core/utils/deprecate.py` — `__signature__` in both wrappers
- `src/ansys/fluent/core/session/solver.py` — `TYPE_CHECKING` conditional base, line 99
- `pyproject.toml` — extras; `.github/workflows/ci.yml` — Unit Testing step env
- `tests/test_runtime_type_checking.py` (new), `tests/test_deprecate.py`, `tests/test_config.py`

## Verification
1. `python -c "import ansys.fluent.core"` — clean with hook off **and** with
   `PYFLUENT_RUNTIME_TYPE_CHECKING=1`.
2. `python -X importtime -c "import ansys.fluent.core"` — compare total import time hook-on vs
   hook-off; beartype front-loads cost at decoration time, so guard against a large regression.
3. `pytest tests/test_runtime_type_checking.py tests/test_config.py tests/test_deprecate.py`
4. `make unittest-dev-261` with and without `PYFLUENT_RUNTIME_TYPE_CHECKING=1` — both green.
5. Negative test: `pyfluent.launch_fluent(processor_count="two")` raises a beartype violation
   with hook on; unchanged (old) behaviour with hook off.
6. Micro-benchmark `SettingsBase.get_state()` and a `field_data` fetch on a large case,
   hook-on vs hook-off; assert overhead stays in the microsecond range.
7. Confirm pip install without the `type-checking` extra still imports and runs (beartype absent).

## Decisions
- beartype is the backend; wrapped behind `_type_checking.py` so it can be swapped (issue sub-task 1).
- Default **off**; opt-in via `pyfluent.config.runtime_type_checking` / `PYFLUENT_RUNTIME_TYPE_CHECKING=1` (sub-task 2).
- On in CI unit tests only (sub-task 3).
- `beartype_package("ansys.fluent.core")`, **not** `beartype_this_package()`.
- beartype is an optional extra, not a hard dependency.
- Generated settings/datamodel classes are explicitly **out of scope** for checking.
- Not adopting `pytest-beartype`: it would duplicate the hook we already own and bypass the config.

## Further considerations
1. Violation severity — raise vs warn. Recommend: raise (default `BeartypeConf`). A `"warn"`
   third mode via `BeartypeConf(violation_type=UserWarning)` is possible; confirm the parameter
   exists in the pinned beartype version before promising it.
2. Should annotation cleanup (Phase 2) ship as its own PR ahead of the feature? Recommend yes —
   it is behaviour-neutral, easy to review, and de-risks the feature PR.
3. Long-term: teach `codegen/settingsgen.py` to emit real annotations on generated command
   methods so the settings API becomes checkable. Large, separate effort — out of scope here.
