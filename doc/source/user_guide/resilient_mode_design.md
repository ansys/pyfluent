# Resilient Mode — Design Details

`ansys.fluent.core.resilient`

This document explains how resilient mode works **under the hood**, aimed at the
two questions raised in review:

1. **Does PyFluent manage an undo / redo mechanism?** — Yes. §3 explains the
   operation journal and the automatic undo→recover→redo cycle.
2. **Does PyFluent encapsulate auto-resilience by handling multiple product /
   server sessions per client session?** — Yes (opt-in). §4 explains the warm
   session pool, health monitoring, and failover with checkpoint replay.

Everything is driven through the typed settings tree, so it behaves identically
over gRPC and REST, and it depends on **neither `fastmcp` nor any AI layer**.

---

## 1. The short answer

> *"Right now it seems to have undo, redo & checkpointing in some form in
> PyFluent, right?"*

Correct. Resilient mode adds three cooperating subsystems **inside PyFluent**,
transparently wrapping the existing settings API:

| Subsystem | What it does | Key module |
| --- | --- | --- |
| **Operation journal** | A per-client, in-memory undo/redo timeline of the operations performed, using `get_state` values as undo points. | `journal.py` |
| **Two-tier checkpointing** | In-memory settings snapshots + case/data file checkpoints, for rollback of reversible and irreversible operations. | `checkpoint.py`, `snapshot.py`, `filecheck.py` |
| **Warm session pool** | One client session fronting **N** product/server sessions; promotes a standby and replays state on a fatal error. | `pool.py`, `health.py` |

A user turns all of this on with a single flag and then writes **ordinary
PyFluent code**:

```python
import ansys.fluent.core as pyfluent

solver = pyfluent.launch_fluent(mode="solver", resilient_mode=True)
solver.settings.setup.models.energy.enabled = True          # normal code
solver.settings.solution.run_calculation.iterate(iter_count=100)
```

There is no new per-call API. Resilience happens inside the settings tree.

---

## 2. Where resilient mode plugs in (architecture overview)

Every write and command on the typed settings tree funnels through **two methods**
on the settings-service object (`services/settings.py :: BaseSettings`):

- `set_var(path, value)` — every `obj.x = v` and `obj.set_state(v)`
- `execute_cmd(path, command, **kwds)` — every command call

`enable_resilient_mode(session)` replaces that service with a thin
`ResilientSettingsService` proxy that routes exactly those two methods through a
`ResilientController`, and **delegates everything else unchanged**. The user's
code and the entire settings tree are untouched.

```
  user code:  solver.settings.setup.models.energy.enabled = True
                         │  (ordinary attribute assignment)
                         ▼
        Group.__setattr__ -> SettingsBase.set_state -> BaseSettings.set_var(path, value)
                         │
                         ▼
     ┌─────────────────────────────────────────────────────────────┐
     │  ResilientSettingsService  (interceptor.py)                   │
     │    set_var / execute_cmd  ───────────────┐                    │
     │    (everything else delegated to inner)  │                    │
     └──────────────────────────────────────────┼────────────────────┘
                                                 ▼
     ┌─────────────────────────────────────────────────────────────┐
     │  ResilientController  (controller.py)                         │
     │   • classify errors        (errors.py)                       │
     │   • auto-recover values     (resolver.py)                    │
     │   • record on the JOURNAL   (journal.py)      ◄── undo/redo   │
     │   • checkpoint / rollback   (checkpoint.py)   ◄── 2-tier      │
     │   • failover to a standby   (pool.py)         ◄── N sessions  │
     └─────────────────────────────────────────────────────────────┘
                                                 │
                          one coupling point (_compat.py)
                                                 ▼
               core PyFluent settings tree / events / connection
```

Only `_compat.py` touches any private core attribute (the fatal-error state);
it degrades gracefully so mock sessions and REST work too.

---

## 3. PyFluent-managed undo / redo

### 3.1 Model: journal of operations, not snapshots of state

The undo/redo mechanism is an **operation journal** (`journal.py`). It records
*what was done* (the operations), not copies of the whole Fluent state. This is
deliberate — it is lightweight (one value per step) and makes a setup
**replayable**.

Each successful operation becomes one journal entry:

```python
@dataclass
class SetOp:                      # a value write
    path: str
    old_value: object            # read via get_state BEFORE the write (the undo point)
    new_value: object            # the value finally applied
    fixes: list[str]             # any auto-recovery fixes applied (e.g. ["clamp"])

@dataclass
class CommandOp:                  # a command invocation
    path: str
    args: dict
    irreversible: bool           # iterate / read_case / ... ?
    checkpoint_name: str | None  # the file checkpoint protecting it, if any
```

The `Journal` is a single global timeline with an undo/redo **cursor**:

```python
class Journal:
    record(op)      # append; truncates any redone-then-diverged tail
    undo()  -> op   # cursor back; restores op.old_value on the live tree
    redo()  -> op   # cursor forward; re-applies op.new_value
    can_undo() / can_redo()
    live_operations      # ops currently applied (up to the cursor)
    replay_script()      # live ops as dicts -> a replayable setup journal
    on_event(listener)   # notified of "record" / "undo" / "redo"
```

Undo restores `old_value`; redo re-applies `new_value`. Because `old_value` is
captured with `get_state` *before* the write, PyFluent always knows the exact
value to roll a setting back to — no full-tree snapshot required.

### 3.2 The automatic undo → recover → redo cycle

The journal is driven automatically by the per-step envelope in
`ResilientController`. For **every `set`**:

```
old = get_state(path)              # 1. read the undo point (last-good value)
try:
    set_state(value)               # 2. attempt the write
    journal.record(SetOp(path, old, value))     # success -> record (silent)
except error:
    classify(error)
      ├─ benign (clean stop)  -> treat as success
      ├─ catastrophic (fatal) -> hand to the pool (failover, §4)
      └─ recoverable:
            set_state(old)         # 3. UNDO  -> restore the last-good value
            fix = resolver.propose(path, value, error)   # 4. compute a repair
            set_state(fix.new_value)                      # 5. REDO -> apply fixed
            journal.record(SetOp(path, old, fixed, fixes))
```

So a failed, recoverable step is **undone** (back to the last successful state)
and then **redone** with a repaired value — all automatically, bounded by
`max_resolver_attempts` (default 3). If no safe fix exists it raises
`UnrecoverableStepError` with the original error chained (never a silent pass).

The recoverable repairs the resolver can apply, using **live introspection**:

| Error category | Repair (redo value) | Introspection used |
| --- | --- | --- |
| out of range | clamp to `[min, max]` | `min()`, `max()` |
| disallowed value | snap to nearest allowed | `allowed_values()` |
| wrong type | safe numeric-string coercion | — |
| inactive target | enable the governing model, then retry | `is_active()` + model probing |

### 3.3 What a viewer sees

Listeners on `on_journal_event` receive `record` / `undo` / `redo`. In the demo
this surfaces as, for an out-of-range value:

```
undo          : turbulent-intensity: step failed -> restored the last successful state
redo          : turbulent-intensity: re-applied after recovery (clamp)
auto-recovery : turbulent_intensity: 5.0 rejected -> applied 1
```

### 3.4 Irreversible operations use the checkpoint tier

Settings `get_state`/`set_state` cannot reverse a solve. So irreversible commands
(`iterate`, `calculate`, `read_case`, `read_case_data`, ...) are protected by the
**file-checkpoint tier** instead: a case + data file is written automatically
*before* the command, and if the command fails non-catastrophically the runtime
**auto-rolls-back** by reloading that checkpoint. This is the same undo idea at a
coarser granularity (whole solver state) for operations that `set_state` can't
undo.

Two tiers, one mental model:

| Tier | Granularity | Undo mechanism | Used for |
| --- | --- | --- | --- |
| Journal / settings | per value | `get_state` value restore | reversible `set` operations |
| File checkpoint | whole case+data | `read_case_data` reload | irreversible commands |

Pre-flight checks validate the checkpoint target (writable dir, legal filename,
non-empty artifact) **before** issuing the write/read, so a bad path fails fast
in Python instead of stalling a synchronous Fluent command.

---

## 4. PyFluent managing multiple product/server sessions per client session

> *"PyFluent encapsulating auto-resilience by handling multiple product/server
> sessions per client session — is that the kind of thing we have here?"*

Yes — this is the `WarmSessionPool` (`pool.py`), an **opt-in** capability. One
client-side `ResilientSolver` / resilient session fronts **N** live Fluent
product/server sessions:

- **1 active** session serves all the user's calls.
- **N − 1 warm standby** sessions are launched eagerly and kept ready.

```python
from ansys.fluent.core.resilient import ResilientConfig, PoolConfig
solver = pyfluent.launch_fluent(
    mode="solver",
    resilient_mode=True,
    resilient_config=ResilientConfig(pool=PoolConfig(size=3)),  # 1 active + 2 standby
)
```

Default `size = 1` (no standbys, no extra cost). `size = N` costs **N licenses +
N × RAM/cores**, so warm standbys are strictly opt-in.

### 4.1 Health monitoring

Each session is watched by a `SessionHealthMonitor` combining two signals:

- **primary** — a push subscription to the `FATAL_ERROR` solver event (the exact
  code path that sets Fluent's shared `ErrorState`): near-instant, zero
  steady-state cost; the callback only flips a flag (no RPCs);
- **backstop** — a slow daemon poll of the error-state + a serving probe, to
  catch a hard crash whose event never arrived.

Fatal is **sticky** (write-once-true) and guarded by a single `RLock` (both the
event-callback thread and the poll thread touch it).

### 4.2 Failover + state replay

When the active session goes fatal, a `set`/`command` raises a *catastrophic*
error and the controller calls `pool.failover(...)`:

```
1. acquire_standby()        # pick the healthiest warm standby (else FailoverError)
2. replay last checkpoint   # reload newest FILE checkpoint (+ latest SETTINGS snapshot)
3. promote standby -> active, rebind the controller/journal/service to it
4. retire the dead session off the critical path (never read from it)
5. refill a replacement standby in the background
6. retry the failed operation once on the new active session
```

**Why replay from a checkpoint and not from the dead session?** Once Fluent is
fatal, every RPC to it is *refused* — its state can't be read. Recovery therefore
relies only on the last good checkpoint. This is exactly why the runtime
auto-checkpoints before irreversible commands: so a standby can be brought up to
the last protected state.

The returned `StepOutcome` has `failed_over=True`; from the user's perspective the
call simply succeeded on a healthy session.

### 4.3 Client-session encapsulation

The important design property: **the user holds one logical session.** The pool,
the active/standby sessions, the health monitors, and the failover are all
encapsulated behind the single `ResilientSolver` / resilient `Solver`. After a
failover `solver.session` (the active handle) changes underneath, but the user
keeps calling the same object with the same ordinary PyFluent code.

---

## 5. How the pieces fit per operation

A single `set` through resilient mode:

```
set_var(path, value)
  └─ controller.apply_set
       old = get_state(path)                    # journal undo point
       set_state(value)
          success ─────────────► journal.record(SetOp)                 [done]
          raises  ─► classify
               benign ─────────► treated as success
               catastrophic ──► pool.failover() + replay + retry       (§4)
               recoverable ──► set_state(old)            # UNDO
                               resolver.propose()        # repair
                               set_state(fixed)          # REDO
                               journal.record(SetOp+fix)                [done]
               hard ──────────► UnrecoverableStepError (chained)
```

A single irreversible `command` (e.g. `iterate`):

```
execute_cmd(path, "iterate", ...)
  └─ controller.apply_command
       checkpoint_file(before)                  # automatic file checkpoint
       execute_cmd(...)
          success ─────────────► journal.record(CommandOp)             [done]
          raises  ─► classify
               catastrophic ──► pool.failover() + replay + retry       (§4)
               non-catastrophic ─► reload the pre-command checkpoint    # AUTO-ROLLBACK
                                   return outcome(auto-rolled-back)     [done]
```

---

## 6. Module map

```
ansys/fluent/core/resilient/
├── __init__.py       Public exports.
├── types.py          Enums + dataclasses (Classification, Fix, StepOutcome, UndoEntry).
├── _compat.py        The ONLY module touching core internals (path resolve, error state).
├── exceptions.py     ResilientError hierarchy (all chained `from err`).
├── errors.py         ErrorClassifier: exception -> {category, severity}.
├── journal.py        Operation journal: SetOp / CommandOp + undo/redo timeline.   ◄ §3
├── snapshot.py       Settings-tier capture/restore (get_state/set_state).
├── resolver.py       RecoverableErrorResolver: propose + apply a fix (clamp/snap/activate).
├── filecheck.py      File-tier checkpoints + fail-fast pre-flight validation.
├── checkpoint.py     CheckpointManager: two-tier checkpoints.
├── health.py         SessionHealthMonitor: FATAL_ERROR subscription + poll backstop.  ◄ §4
├── pool.py           WarmSessionPool: N sessions, health, failover + replay.           ◄ §4
├── interceptor.py    ResilientSettingsService: wraps set_var / execute_cmd.
├── controller.py     ResilientController: the per-step envelope (recover/journal/checkpoint/failover).
├── patch.py          Guarded Group.__getattribute__/__setattr__ wrappers (client-side errors).
├── attach.py         enable_resilient_mode(session): wires it all onto a live Solver.
└── solver.py         ResilientSolver facade + ResilientConfig (explicit/advanced path).
```

---

## 7. Configuration

```python
from ansys.fluent.core.resilient import (
    ResilientConfig, PoolConfig, FileCheckpointConfig,
)

config = ResilientConfig(
    pool=PoolConfig(
        size=3,                 # 1 active + 2 warm standby sessions
        launch_kwargs={},       # forwarded to launch_fluent for standbys
        health_interval=2.0,    # poll backstop interval (s)
        replay_from="auto",     # "auto" | "file" | "settings"
    ),
    file_checkpoint=FileCheckpointConfig(
        directory="resilient_checkpoints", keep_last=5, data=True,
    ),
    max_resolver_attempts=3,
    auto_file_checkpoint_before_irreversible=True,
    auto_rollback_on_failed_command=True,
)

solver = pyfluent.launch_fluent(mode="solver", resilient_mode=True,
                                resilient_config=config)
```

---

## 8. Design principles & honest limitations

**Principles**
- **Transparent**: ordinary PyFluent code; one launch flag; no new per-call API.
- **Transport-agnostic**: everything rides `get_state` / `set_state` / command
  invocation, so gRPC and REST behave identically. The single core-coupling point
  (fatal `ErrorState`) is isolated and guarded in `_compat.py`.
- **No RPCs from finalizers**: all teardown is explicit (`__exit__` / `shutdown` /
  `stop`); health callbacks only flip flags.
- **Automatic classification**: only the authoritative `ErrorState` marks a
  session fatal — error *text* never escalates to a failover.

**Limitations (by design)**
- **Journal undo is value-level**, using `get_state`. It reverses *settings*, not
  solution data; irreversible solves are covered by the file-checkpoint tier
  instead.
- **Failover replays from the last checkpoint**, so anything changed after the
  last checkpoint on a crashed session is lost — hence auto-checkpointing before
  irreversible ops.
- **Warm standbys cost licenses + RAM/cores**; default `size=1` keeps resilient
  mode free until failover is explicitly requested.
- **Re-convergence after a rolled-back solve is the engineer's domain** — the
  runtime guarantees the *mechanics* of recovery (detect, keep alive, restore),
  not that a retry with the same settings will converge.

---

## 9. Where to look / try it

- User guide (Sphinx): `doc/source/user_guide/resilient_mode.rst`
- Runnable examples:
  - `examples/00-fluent/mixing_elbow_resilient.py` — transparent auto-recovery
  - `examples/00-fluent/modeling_solidification_workflow_resilient.py` — a real
    diverging solve recovered via checkpoint rollback
  - `examples/00-fluent/demo_resilient_mode.py` — a guided, colour-coded demo
    printing each capability and the matching action in Fluent
- Tests: `tests/resilient/` (unit tests run with no live Fluent via a mock
  settings tree; live checks are `@pytest.mark.standalone`).
