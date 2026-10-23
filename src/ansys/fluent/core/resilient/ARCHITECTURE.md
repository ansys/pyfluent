# Resilient Mode — Architecture & User Guide

`ansys.fluent.core.resilient`

A native, transport-agnostic runtime that makes an automated Fluent
setup-and-solve workflow **survivable**: it recovers from recoverable solver
errors automatically, lets you checkpoint / undo / redo across two tiers, and
(optionally) fails over to a warm standby session and replays the last
checkpoint when the active solver dies.

It depends on **neither `fastmcp` nor the AI layer** — the same surface is used
by a human or by an autonomous agent. Everything is driven through the typed
settings tree (`get_state` / `set_state` / command invocation), so it behaves
identically over gRPC and REST.

---

## Table of contents

1. [Why resilient mode](#1-why-resilient-mode)
2. [Quick start](#2-quick-start)
3. [The four features](#3-the-four-features)
4. [Architecture](#4-architecture)
5. [How it works — end to end](#5-how-it-works--end-to-end)
6. [Configuration reference](#6-configuration-reference)
7. [Error handling](#7-error-handling)
8. [Testing](#8-testing)
9. [Design decisions & limitations](#9-design-decisions--limitations)

---

## 1. Why resilient mode

A long, scripted Fluent run is fragile. A single bad boundary-condition value, a
setting applied before its model is enabled, or a solver crash mid-solve forces
you to start over. Resilient mode wraps your settings and command calls with:

- **auto-recovery** from non-catastrophic Fluent errors,
- **two-tier checkpoints** with a unified **undo / redo** stack,
- an opt-in **warm session pool** with health monitoring, and
- automatic **failover and state replay** when the active session dies.

> **It never changes *what* Fluent does.** If a value is accepted by Fluent, it
> is applied unchanged. Resilient mode only adds classification, checkpointing,
> and recovery *around* your calls.

---

## 2. Quick start

Resilient mode is **transparent**. Launch with `resilient_mode=True` and write
ordinary PyFluent code — the settings tree is wrapped so every write and command
gains resilience automatically. There is no new per-call API.

```python
import ansys.fluent.core as pyfluent

solver = pyfluent.launch_fluent(mode="solver", resilient_mode=True)

# ...ordinary PyFluent code from here on...
solver.settings.file.read_case(file_name="mixing_elbow.cas.h5")
solver.settings.setup.models.energy.enabled = True

inlet = solver.settings.setup.boundary_conditions.velocity_inlet["cold-inlet"]
inlet.momentum.velocity_magnitude.value = 0.4
inlet.turbulence.turbulent_intensity = 0.05   # auto-recovered if out of range

solver.settings.solution.initialization.hybrid_initialize()
solver.checkpoint("pre-iterate")               # explicit checkpoint
solver.settings.solution.run_calculation.iterate(iter_count=100)
solver.undo()                                  # reloads the pre-iterate case + data
```

`Solver.from_install(resilient_mode=True)` works the same way. To enable on an
already-connected session, call `enable_resilient_mode(solver)`.

The session gains four convenience members (and nothing else changes):

| Session member | Purpose |
| --- | --- |
| `solver.checkpoint(name, kind=..., paths=...)` | Take an explicit checkpoint (file by default). |
| `solver.undo()` / `redo()` | Walk the unified undo / redo stack. |
| `solver.rewind_to(name)` | Undo repeatedly back to a named checkpoint. |
| `solver.resilient_checkpoints` | The `CheckpointManager` (undo / redo stacks). |

A warm pool (for failover) is enabled via `resilient_config`:

```python
from ansys.fluent.core.resilient import ResilientConfig, PoolConfig
solver = pyfluent.launch_fluent(
    mode="solver", resilient_mode=True,
    resilient_config=ResilientConfig(pool=PoolConfig(size=3)),
)
```

### Advanced: the explicit facade

For programmatic control (inspecting each write's `StepOutcome`, or driving the
runtime without a live tree in tests) an explicit `ResilientSolver` facade is also
available. It takes **string paths** and returns outcomes. Most users should
prefer transparent `resilient_mode=True`.

```python
from ansys.fluent.core.resilient import ResilientSolver, CheckpointKind

with ResilientSolver(session, pool_size=1) as rsolver:
    rsolver.command("file.read_case", file_name="mixing_elbow.cas.h5")
    out = rsolver.set("setup.models.energy.enabled", True)
    assert out.ok
    rsolver.checkpoint("pre-iterate", kind=CheckpointKind.FILE)
    rsolver.command("solution.run_calculation.iterate", iter_count=100)
    rsolver.undo()
```

The `with` block guarantees an orderly shutdown (health monitors and any warm
standbys) on exit; teardown never happens from a finalizer.

---

## 3. The four features

### 3.1 Automatic recovery from non-catastrophic errors

When a settings write fails, the runtime **classifies** the error and, if it is
*recoverable*, **repairs and retries** it using **live** object introspection
(`is_active` / `is_read_only` / `allowed_values` / `min` / `max`). You get back a
`StepOutcome` recording what happened (`attempts`, `fixes_applied`, `old_value`,
`new_value`).

| Category | Severity | Automatic action |
| --- | --- | --- |
| `inactive_target` | recoverable | Discover the governing model by live introspection, enable it, then retry. |
| `out_of_range` | recoverable | Clamp to the live `[min, max]` and retry. |
| `wrong_value` | recoverable | Snap to the nearest live `allowed_values` entry. |
| `wrong_type` | recoverable | Coerce a numeric string to `int` / `float`. |
| `read_only` | hard | Not fixable → `UnrecoverableStepError`. |
| `benign_interrupt` | benign | Clean solver stop (`RuntimeError("()")`) → treated as success. |
| `fatal` | catastrophic | Triggers failover (see 3.4). |
| `unknown` | hard | → `UnrecoverableStepError`. |

```python
out = rsolver.set('....turbulence.turbulent_intensity', 5.0)
# out.ok == True, out.fixes_applied == ['clamp'], out.attempts == 2
# out.old_value == 0.05, out.new_value == 1
```

**Inactive targets — automatic model activation by live discovery.** Many
settings are inactive until a governing model is on (e.g. a thermal BC needs the
energy model). Fluent raises `InactiveObjectError` **client-side**, inside
`Group.__getattribute__`, the moment you navigate into an inactive branch — before
any write reaches the service layer. Resilient mode handles this via `patch.py`: a
guarded, ref-counted wrapper around `Group.__getattribute__` (a no-op unless a
resilient session is active) catches that specific error, calls
`resolver.activate_object(obj)`, and retries. `activate_object` **discovers** the
right model empirically: it tentatively enables each candidate model flag that is
off, re-checks `obj.is_active()`, keeps the one that activates it, and reverts the
rest. If nothing activates the target (e.g. it needs a zone-type assignment), the
original error is re-raised unchanged — models are never enabled blindly.

**Bounded.** Recovery is capped (`max_resolver_attempts`, default `3`). If no
safe fix can be derived, `UnrecoverableStepError` is raised with the original
Fluent error chained as the cause — failures are never silently swallowed.

### 3.2 Two-tier checkpoints and undo / redo

Reversible settings changes and irreversible commands need different strategies,
so there are **two tiers** under a **single** undo / redo stack:

- **Settings tier** — an in-memory snapshot of one or more settings subtrees via
  `get_state` (cheap, no disk). Restored with `set_state`.
- **File tier** — a case/data file written with `settings.file.write_case_data`
  and reloaded with `read_case_data`. The **only** way to undo irreversible
  operations such as `iterate` or `read_case`.

```python
rsolver.checkpoint("before-bcs", kind=CheckpointKind.SETTINGS,
                   paths=["setup.boundary_conditions"])   # lightweight
rsolver.checkpoint("pre-iterate", kind=CheckpointKind.FILE)  # case + data
```

If you omit `kind`, a **file** checkpoint is taken (the safest, broadest option).

**Automatic checkpoints before irreversible commands.** `command` recognizes
irreversible leaves (`iterate`, `calculate`, `dual_time_iterate`, `read_case`,
`read_case_data`, `read_data`, `read`) and takes a file checkpoint *before*
running them.

**Undo / redo semantics.** `undo` pops the newest checkpoint and restores it. To
keep every undo redoable, the runtime first captures the *current* state (same
tier) onto the redo stack, then restores the popped entry:

- a **settings** undo snapshots the present with `get_state` and writes back the
  past with `set_state`;
- a **file** undo writes the present with `write_case_data`, then reloads the
  past with `read_case_data`.

Taking any *new* checkpoint clears the redo stack (a new branch of history).
`rewind_to("name")` undoes repeatedly until the named checkpoint is restored.

> Undo is a **state + data** rollback, not a wall-clock rewind. Reloading a case
> restores mesh, settings, and solution data, but transient artifacts such as
> residual history or monitor plots are not reconstructed.

### 3.3 The warm session pool

- `pool_size=1` (**default**) — a single session, no extra licenses/resources.
  Failover is disabled (nothing to fail over to).
- `pool_size=N` (`N > 1`) — `N - 1` **warm standby** sessions launched eagerly,
  so failover is near-instant. Each standby consumes a license and host
  resources (RAM and cores), so choose `N` deliberately.

```python
rsolver = ResilientSolver(session, pool_size=3)  # 1 active + 2 standbys
```

**Health monitoring** combines two signals per session:

- a push-based subscription to the `FATAL_ERROR` solver event (the exact event
  that flips Fluent's shared error state) — near-instant, zero steady-state cost;
- a slow poll backstop (default every `2` s) that also catches a hard crash whose
  event never arrived.

Fatal state is *sticky* and the detector is thread-safe (one `RLock`). The event
callback only flips a flag — it performs no RPCs.

### 3.4 Failover and checkpoint replay

When the active session enters a fatal state, a `set` or `command` raises a
*catastrophic* error. The runtime then:

1. promotes the healthiest **warm standby** to active;
2. **replays the last good checkpoint** onto it; and
3. retries the failed operation once on the new active session.

The returned `StepOutcome` has `failed_over=True`.

**Why replay from a checkpoint, not from the dead session?** Once Fluent is
fatal, every RPC to it is refused — you cannot read its state. Recovery relies
solely on the last checkpoint:

- `replay_from="auto"` (default) — reload the newest **file** checkpoint as the
  base (mesh + settings + data), then layer the newest **settings** snapshot on
  top;
- `replay_from="file"` — reload only the newest file checkpoint;
- `replay_from="settings"` — restore only the newest settings snapshot.

This is why the runtime auto-checkpoints before irreversible commands: anything
changed after the last checkpoint cannot be recovered on the standby. If no
healthy standby is available (e.g. `pool_size=1`) or replay fails, `FailoverError`
is raised rather than silently continuing on a broken session.

---

## 4. Architecture

### 4.1 Module map

```
ansys/fluent/core/resilient/
├── __init__.py       Public exports.
├── types.py          Enums + dataclasses (Classification, Fix, StepOutcome, UndoEntry).
├── _compat.py        The ONLY module touching core internals (path resolve + scheme-path
│                     resolve, _error_state, health).
├── exceptions.py     ResilientError hierarchy (all chained `from err`).
├── errors.py         ErrorClassifier: exception -> {category, severity}.
├── snapshot.py       Settings-tier capture/restore + safe_set_state (child-by-child recursion).
├── resolver.py       RecoverableErrorResolver: propose + apply a fix, bounded retry.
├── apply.py          SafeApplier: one set/command with classification + recovery.
├── filecheck.py      File-tier checkpoints + fail-fast pre-flight validation.
├── checkpoint.py     CheckpointManager: two-tier unified undo/redo stack.
├── health.py         SessionHealthMonitor: FATAL_ERROR subscription + poll backstop.
├── pool.py           WarmSessionPool: N sessions, health, failover + replay.
│
│   # transparent resilient mode (the primary user path):
├── interceptor.py    ResilientSettingsService: wraps the settings service; intercepts
│                     set_var / execute_cmd, delegates everything else transparently.
├── controller.py     ResilientController: owns resilient state; the apply envelope
│                     (classify -> recover -> checkpoint / failover) over string paths.
├── patch.py          Guarded, ref-counted Group.__getattribute__ wrapper: catches the
│                     client-side InactiveObjectError raised while navigating into an
│                     inactive branch, discovers + enables the governing model, retries.
├── attach.py         enable_resilient_mode(session): swaps in the wrapped service and
│                     attaches checkpoint/undo/redo onto the session.
│
└── solver.py         ResilientSolver facade (explicit/advanced path; wraps the pool).
```

**Two entry paths, one engine.** The lower-level modules (`errors`, `resolver`,
`snapshot`, `filecheck`, `checkpoint`, `health`, `pool`) are shared. They are
driven either transparently via `attach` + `interceptor` + `controller`
(`resilient_mode=True`), or explicitly via the `ResilientSolver` facade. Both
reach the live tree only through `_compat`.

### 4.1.1 How transparent interception works

Every write and command on the settings tree funnels through two methods on the
settings service object (`services/settings.py :: BaseSettings`):

- `set_var(path, value)` — every `obj.x = v` and `obj.set_state(v)`;
- `execute_cmd(path, command, **kwds)` — every `command(...)`.

`enable_resilient_mode` replaces `solver._settings_service` with a
`ResilientSettingsService` that wraps the real one and routes exactly those two
methods through the `ResilientController`; all other methods (`get_var`,
`get_attrs`, `is_wildcard`, ...) are delegated unchanged via `__getattr__`. The
cached settings root is dropped so it rebuilds against the wrapped service. The
user's PyFluent code is therefore **completely unchanged**.

> **Path formats.** At the service layer the path is a Fluent **scheme path**
> (slash-separated, hyphenated, e.g.
> `setup/boundary-conditions/velocity-inlet/cold-inlet/turbulence/turbulent-intensity`).
> For recovery the controller must introspect the live object (`min` / `max` /
> `allowed_values`), so `_compat.resolve_any` resolves a scheme path
> segment-by-segment against the live tree using each object's `fluent_name`
> metadata (handling named-object keys with hyphens such as `cold-inlet`).

### 4.2 Layering

```
                 ┌─────────────────────────────┐
   user / agent  │        ResilientSolver       │  facade: set / command / checkpoint / undo
                 └──────────────┬──────────────┘
          ┌─────────────────────┼───────────────────────┐
          ▼                     ▼                        ▼
   ┌─────────────┐      ┌──────────────┐        ┌──────────────────┐
   │ SafeApplier │      │ Checkpoint   │        │ WarmSessionPool  │
   │  (apply.py) │      │  Manager     │        │   (pool.py)      │
   └──────┬──────┘      └──────┬───────┘        └────────┬─────────┘
          │                    │                         │
  ┌───────┴────────┐    ┌──────┴───────┐        ┌────────┴─────────┐
  ▼                ▼    ▼              ▼         ▼                  ▼
ErrorClassifier  Resolver  snapshot  filecheck  SessionHealthMonitor
 (errors.py)  (resolver.py)(settings) (file I/O)    (health.py)
          │                    │                         │
          └──────────── _compat.py (the one coupling point) ──────────────┐
                                                                           ▼
                                               core PyFluent (settings tree, events,
                                                _fluent_connection._error_state)
```

**Key rule:** only `_compat.py` reaches into core internals. Everything else
talks to it or to the public settings protocol, which is why the runtime is
transport-agnostic and easy to unit-test with a mock tree.

### 4.3 Core signals the runtime wires to

| Need | Core symbol | Location |
| --- | --- | --- |
| Launch sessions | `pyfluent.launch_fluent` | `execution/launcher/launcher.py` |
| Apply / read state | `get_state` / `set_state` / `__call__` | `solver/flobject.py` |
| Live introspection | `is_active` / `is_read_only` / `allowed_values` / `min` / `max` | `solver/flobject.py` |
| Typed errors | `InactiveObjectError`, `ReadOnlyActionError` | `solver/flobject.py` |
| Fatal state | `ErrorState` (`.name == "fatal"`) | `connectivity/fluent_connection.py` |
| Fatal event | `SolverEvent.FATAL_ERROR` via `events.register_callback` | `services/streaming_services/events_streaming.py` |
| File checkpoints | `settings.file.write_case_data` / `read_case_data` | `solver/settings_builtin_data.py` |

---

## 5. How it works — end to end

### 5.1 A `set` call

```
rsolver.set(path, value)
  └─ SafeApplier.set(path, value)
       1. resolve(path) -> live object            (_compat.resolve)
       2. refuse if is_active() is False          (avoid solver crash)
       3. old = obj.get_state()                   (captured for rollback)
       4. obj.set_state(value)
            ├─ success -> StepOutcome(ok=True, old, new)
            └─ raises  -> classify(err, session)   (ErrorClassifier)
                 ├─ benign       -> StepOutcome(ok=True, "interrupted")
                 ├─ catastrophic -> re-raise ──────────────► failover (5.3)
                 ├─ recoverable  -> resolver.resolve_and_retry(...)
                 │                    propose Fix (clamp / snap / activate / coerce)
                 │                    apply pre-mutations, retry, re-classify
                 │                    (bounded by max_resolver_attempts)
                 └─ hard         -> raise UnrecoverableStepError from err
```

### 5.2 A `command` call

```
rsolver.command(path, **args)
  1. if is_irreversible(path) and auto_file_checkpoint:
        checkpoints.checkpoint_file("auto:<path>")   (best-effort; never blocks)
  2. SafeApplier.command(path, **args)
        resolve_parent(path) -> (parent, leaf); parent.leaf(**args)
          ├─ success               -> StepOutcome(ok=True, result)
          ├─ RuntimeError("()")    -> StepOutcome(ok=True, "interrupted")  (clean stop)
          ├─ catastrophic          -> re-raise ──────► failover (5.3)
          └─ other                 -> raise UnrecoverableStepError from err
```

### 5.3 Failover (triggered by a catastrophic error)

```
ResilientSolver._maybe_failover_and_retry(err, retry, path)
  classify(err) is catastrophic?  yes ▼            no -> re-raise
  WarmSessionPool.failover(checkpoint_mgr):
    1. standby = acquire_standby()         (healthiest; else FailoverError)
    2. replay(checkpoint_mgr, standby):    (NEVER reads the dead session)
         auto: read_case_data(newest FILE) then set_state(newest SETTINGS)
    3. promote standby to active; checkpoint_mgr.rebind(standby)
    4. retire dead session off the critical path; refill a standby in background
  applier.rebind(standby); retry() once; outcome.failed_over = True
```

### 5.4 Checkpoint / undo (two tiers, one stack)

```
checkpoint_settings(name, paths)  -> UndoEntry(SETTINGS, states={path: get_state()})
checkpoint_file(name)             -> preflight_write(path); write_case_data(path)
                                     -> UndoEntry(FILE, case_data_path=path)

undo():
  entry = undo_stack.pop()
  redo_entry = capture_current(entry.kind)      # snapshot present onto redo stack
  apply(entry):                                 # restore the past
      SETTINGS -> set_state(entry.states)
      FILE     -> preflight_read(path); read_case_data(path)
  redo_stack.push(redo_entry)
```

### 5.5 Fail-fast file pre-flight (hang avoidance)

A case/data write or read is a **synchronous** Fluent command. If the server-side
file op fails in a way that never returns a response (illegal file name, missing
/ unwritable directory, over-long path, or on restore a missing / empty /
unreadable artifact), the client could block indefinitely. So the file tier
validates the target **locally, before** issuing the command:

```python
preflight_write(path)   # before write_case_data -> CheckpointError if bad
preflight_read(path)    # before read_case_data  -> CheckpointError if bad
```

This turns a latent stall into an immediate, actionable `CheckpointError`. It
does **not** impose a client-side timeout on Fluent commands.

> **Future direction:** a general "command accepted but never returned" detector
> would build on the Fluent **transcript stream** (observing that an in-flight
> command has produced no new transcript output). The runtime deliberately does
> **not** time out Fluent operations today.

---

## 6. Configuration reference

```python
from ansys.fluent.core.resilient import (
    ResilientConfig, PoolConfig, FileCheckpointConfig,
)

config = ResilientConfig(
    pool=PoolConfig(
        size=3,                 # 1 active + 2 warm standbys
        launch_kwargs={},       # forwarded to launch_fluent for standbys
        health_interval=2.0,    # poll backstop interval (seconds)
        replay_from="auto",     # "auto" | "file" | "settings"
    ),
    file_checkpoint=FileCheckpointConfig(
        directory="resilient_checkpoints",
        keep_last=5,            # ring buffer depth
        data=True,              # write_case_data vs write_case (case-only)
        name_template="resilient_{name}_{ts}",
    ),
    max_resolver_attempts=3,
    auto_file_checkpoint_before_irreversible=True,
)

rsolver = ResilientSolver(session, config=config)
```

Convenience launcher (standby kwargs reused automatically):

```python
rsolver = ResilientSolver.launch(
    pool_size=3, mode="solver", precision="double", processor_count=2,
)
```

---

## 7. Error handling

All runtime errors derive from `ResilientError` and chain the underlying Fluent
error as the cause (`raise ... from err`):

| Exception | Raised when |
| --- | --- |
| `UnrecoverableStepError` | A step failed and no safe automatic fix applied (session still usable). |
| `FailoverError` | No healthy standby, or replay onto the standby failed. |
| `CheckpointError` | A checkpoint could not be captured, restored, or found (incl. pre-flight rejections). |
| `PathResolutionError` | A settings path could not be resolved on the live tree. |

---

## 8. Testing

### 8.1 Unit tests (no Fluent — fast)

The whole runtime is unit-tested against a **mock settings tree** that implements
exactly the surface the runtime relies on (`get_state` / `set_state` /
`is_active` / `is_read_only` / `allowed_values` / `min` / `max`, named-object
indexing, a `file` command group, and an events stub). No live Fluent is needed.

```bash
# Run the whole package
python -m pytest tests/resilient -v

# By marker (works from anywhere in the suite)
python -m pytest -m resilient

# A single file / test
python -m pytest tests/resilient/test_apply.py
python -m pytest tests/resilient/test_apply.py::test_out_of_range_auto_clamped -v

# With coverage of the new package
python -m pytest tests/resilient --cov=ansys.fluent.core.resilient --cov-report=term-missing
```

What the suites prove:

| Requirement | Test file |
| --- | --- |
| Error classification (benign / fatal / recoverable / hard) | `test_errors.py` |
| Path resolve + settings snapshot/restore + `safe_set_state` recursion | `test_snapshot.py` |
| Auto-recover (clamp / snap), inactive refusal, catastrophic propagation | `test_apply.py` |
| Two-tier checkpoints, undo/redo, rewind, pruning, filename sanitize | `test_checkpoint.py` |
| Fail-fast file pre-flight (write + read) | `test_filecheck_preflight.py` |
| Health monitor (event + poll backstop, sticky fatal) | `test_health.py` |
| Warm pool + failover + replay (never reads dead session) | `test_pool.py` |
| End-to-end facade (set → recover → checkpoint → iterate → undo → failover) | `test_solver_facade.py` |

Example of a focused unit test (how the mock models a Fluent rejection):

```python
def test_out_of_range_auto_clamped():
    def reject(value):
        if value > 1.0:
            raise RuntimeError("value is above maximum 1.0")

    leaf = FakeLeaf(0.0, minimum=0.0, maximum=1.0, set_raises=reject)
    session = _session(setup=FakeGroup(ti=leaf))
    out = SafeApplier(session).set("setup.ti", 5.0)
    assert out.ok and "clamp" in out.fixes_applied
    assert leaf.get_state() == 1.0     # clamped to the live max
```

### 8.2 Live integration (real Fluent)

Run the gallery example end-to-end against an installed Fluent:

```bash
python examples/00-fluent/mixing_elbow_resilient.py
```

It reads the mixing-elbow case, sets a deliberately out-of-range turbulent
intensity (auto-clamped), checkpoints before `iterate`, iterates, and `undo`s.
Validated on **Fluent 27.1.0**, where `turbulent_intensity = 5.0` is rejected
with `Value is not in range`, then clamped to the live `max = 1` and retried
(`fixes_applied == ['clamp']`, `attempts == 2`).

### 8.3 Manually demonstrating failover (optional)

Catastrophic failover is hard to trigger on demand (there is no supported way to
crash Fluent), so it is proven in unit tests with a simulated fatal. To watch it
live, flip the fatal flag yourself with `pool_size >= 2`:

```python
rsolver.session._fluent_connection._error_state.set("fatal", "manual test")
out = rsolver.set("setup.models.energy.enabled", True)  # promotes a standby
assert out.failed_over
```

---

## 9. Design decisions & limitations

- **No dependency on `fastmcp` or the AI layer.** The runtime reimplements the
  proven snapshot/validate/recover patterns cleanly in core so it is usable by
  anyone, agentic or not.
- **One coupling point.** Only `_compat.py` touches core internals
  (`_fluent_connection._error_state`); it degrades gracefully (returns `None` /
  best-effort) so mock sessions and REST transports still work.
- **No RPCs from finalizers.** All teardown is explicit via `__exit__` /
  `shutdown()` / `stop()`. Event callbacks only flip flags.
- **Undo is state + data, not wall-clock.** Monitors / residual history are not
  reconstructed by a case reload.
- **Resource cost.** `N` warm sessions = `N` licenses + `N` × RAM/cores; the
  default `pool_size=1` disables failover and costs nothing extra.
- **Replay fidelity.** A standby replays from the last checkpoint only (the dead
  session's RPCs are refused), so anything changed after the last checkpoint is
  lost — hence auto-checkpointing before irreversible commands.
- **No client-side timeout.** Fail-fast pre-flight guards the file operations the
  runtime issues, but the runtime does not impose timeouts on Fluent commands; a
  transcript-based stall detector is a possible future addition.

---

## See also

- User guide (Sphinx): `doc/source/user_guide/resilient_mode.rst`
- Runnable example: `examples/00-fluent/mixing_elbow_resilient.py`
- Tests: `tests/resilient/`
