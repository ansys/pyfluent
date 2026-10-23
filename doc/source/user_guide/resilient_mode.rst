.. _ref_resilient_guide:

==============
Resilient mode
==============

Resilient mode makes a solver workflow *survivable*. Enable it with a single
launch flag (``resilient_mode=True``) and keep writing ordinary PyFluent code --
the settings tree is transparently wrapped so a long, automated setup-and-solve
run can recover from mistakes and from solver failures without you restarting from
scratch:

* **auto-recovery** from non-catastrophic Fluent errors,
* **two-tier checkpoints** with a unified **undo / redo** stack,
* an opt-in **warm session pool** with health monitoring, and
* automatic **failover and state replay** when the active session dies.

It lives in :mod:`ansys.fluent.core.resilient` and depends on neither
``fastmcp`` nor the AI layer -- the same behavior benefits a human or an
autonomous agent. Everything is driven through the typed settings tree, so it
behaves identically over gRPC and REST.

.. note::

   Resilient mode never changes *what* Fluent does. It wraps your settings and
   command calls with classification, checkpointing, and recovery. If a value is
   accepted by Fluent, it is applied unchanged.


Getting started
---------------

Resilient mode is **transparent**: you write ordinary PyFluent code and turn it on
with a single launch flag. Pass ``resilient_mode=True`` and keep using the session
exactly as you normally would -- the settings tree is wrapped so every write and
command gains resilience automatically.

.. code:: python

  >>> import ansys.fluent.core as pyfluent
  >>> solver = pyfluent.launch_fluent(mode="solver", resilient_mode=True)
  >>>
  >>> # ...ordinary PyFluent code from here on...
  >>> solver.settings.file.read_case(file_name="mixing_elbow.cas.h5")
  >>> solver.settings.setup.models.energy.enabled = True
  >>> inlet = solver.settings.setup.boundary_conditions.velocity_inlet["cold-inlet"]
  >>> inlet.momentum.velocity_magnitude.value = 0.4
  >>> inlet.turbulence.turbulent_intensity = 0.05   # auto-recovered if out of range
  >>>
  >>> solver.settings.solution.initialization.hybrid_initialize()
  >>> solver.checkpoint("pre-iterate")               # explicit checkpoint
  >>> solver.settings.solution.run_calculation.iterate(iter_count=100)
  >>> solver.undo()                                  # roll back to pre-iterate

``Solver.from_install`` accepts the same flag:

.. code:: python

  >>> from ansys.fluent.core import Solver
  >>> solver = Solver.from_install(resilient_mode=True)

There is **no new per-call API to learn.** The only addition is a handful of
convenience methods attached to the session for checkpoint / undo / redo:

================================  ==========================================================
Session member                    Purpose
================================  ==========================================================
``solver.checkpoint(name, ...)``  Take an explicit checkpoint (file by default).
``solver.undo()`` / ``redo()``    Walk the unified undo / redo stack.
``solver.rewind_to(name)``        Undo repeatedly back to a named checkpoint.
``solver.resilient_checkpoints``  The :class:`CheckpointManager` (undo / redo stacks).
================================  ==========================================================

Enabling a warm pool (for failover) is done through ``resilient_config``:

.. code:: python

  >>> from ansys.fluent.core.resilient import ResilientConfig, PoolConfig
  >>> solver = pyfluent.launch_fluent(
  ...     mode="solver",
  ...     resilient_mode=True,
  ...     resilient_config=ResilientConfig(pool=PoolConfig(size=3)),
  ... )

.. note::

   Resilient mode never changes *what* Fluent does. It wraps your settings and
   command calls with classification, checkpointing, and recovery. If a value is
   accepted by Fluent, it is applied unchanged.

Enabling on an existing session
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you already have a session (for example from ``connect_to_fluent``), enable
resilient mode in place:

.. code:: python

  >>> from ansys.fluent.core.resilient import enable_resilient_mode
  >>> enable_resilient_mode(solver)   # same session, now resilient

Advanced: the explicit facade
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For programmatic control (e.g. inspecting the :class:`StepOutcome` of each write,
or driving the runtime without a live tree in tests), an explicit
:class:`~ansys.fluent.core.resilient.ResilientSolver` facade is also available. It
exposes ``set(path, value)`` / ``command(path, **args)`` that take string paths
and return outcomes. Most users should prefer transparent ``resilient_mode=True``.

.. code:: python

  >>> from ansys.fluent.core.resilient import ResilientSolver
  >>> with ResilientSolver(session, pool_size=1) as rsolver:
  ...     out = rsolver.set("setup.models.energy.enabled", True)
  ...     print(out.ok, out.fixes_applied)


Feature 1 -- automatic recovery from non-catastrophic errors
------------------------------------------------------------

When a settings write fails, the runtime classifies the error and, if it is
*recoverable*, repairs and retries it automatically using **live** object
introspection (``is_active`` / ``is_read_only`` / ``allowed_values`` / ``min`` /
``max``). The repair happens inside the normal ``obj.x = v`` call -- you do not
catch anything. (The explicit facade additionally returns a :class:`StepOutcome`
recording what happened.)

**How errors are classified.** Fluent flattens most errors to
``RuntimeError(<text>)``, so the classifier combines typed exceptions, the shared
fatal-error state, and text heuristics:

====================  ===========  ==================================================
Category              Severity     Automatic action
====================  ===========  ==================================================
``inactive_target``   recoverable  Discover the governing model by live introspection, enable it, then retry.
``out_of_range``      recoverable  Clamp to the live ``[min, max]`` and retry.
``wrong_value``       recoverable  Snap to the nearest live ``allowed_values`` entry.
``wrong_type``        recoverable  Coerce a numeric string to ``int`` / ``float``.
``read_only``         hard         Not fixable; raises ``UnrecoverableStepError``.
``benign_interrupt``  benign       A clean solver stop (``RuntimeError("()")``) -- treated as success.
``fatal``             catastrophic Triggers **failover** (see Feature 4).
``unknown``           hard         Raises ``UnrecoverableStepError``.
====================  ===========  ==================================================

**Where each error is detected (and how it is caught).** The three value errors
you might expect -- out of range, not an allowed value, wrong type -- are not all
raised in the same place, and resilient mode hooks every layer so recovery is
transparent regardless:

=========================  ================================================  ================================================
Error                      Where it is raised                                How resilient mode catches it
=========================  ================================================  ================================================
Out of range               Fluent server (``RuntimeError`` via ``set_var``)  At the settings-service layer (``set_var``).
Not an allowed value       Fluent server (``set_var``), or client-side       At the settings-service layer; client-side
                           ``DisallowedValuesError``                         ``DisallowedValuesError`` is caught by the
                                                                             guarded ``__setattr__`` wrapper.
Wrong data type            Client-side ``TypeError`` in ``Textual.set_state``  By the guarded ``__setattr__`` wrapper, before
                           / type checks (``flobject.py``) -- *before* any     the value reaches the server.
                           value reaches the server
Inactive target            Client-side ``InactiveObjectError`` in            By the guarded ``__getattribute__`` wrapper,
                           ``Group.__getattribute__`` while *navigating*      which runs model-activation discovery.
                           into an inactive branch
=========================  ================================================  ================================================

This is why resilient mode wraps **three** points, not one: the settings-service
layer (``set_var`` / ``execute_cmd``) for server-reported errors, and -- for the
errors Fluent raises *client-side before the value is ever sent* -- a guarded,
reference-counted pair of wrappers around the settings tree's ``__getattribute__``
and ``__setattr__``. All of these wrappers are a complete no-op for non-resilient
sessions.

.. note::

   Fluent is permissive about some "type" cases: a numeric string on a real-valued
   field is accepted natively (treated as a value or expression), so no coercion is
   needed. The ``wrong_type`` repair only applies when Fluent actually raises a
   ``TypeError``, and only performs a *safe* coercion (numeric string to a number).
   A genuinely unconvertible assignment (for example an integer given to a
   string-valued enumeration) has no safe fix, so the original ``TypeError`` is
   re-raised unchanged -- resilient mode never masks a real mistake.

**Example (verified on Fluent 27.1.0).** Turbulent intensity must be a fraction
in ``[0, 1]``. Setting ``5.0`` makes Fluent raise ``Value is not in range``. The
runtime reads the live bounds (``min=0``, ``max=1``), clamps to ``1``, and
retries:

.. code:: python

  >>> out = rsolver.set(
  ...     'setup.boundary_conditions.velocity_inlet["cold-inlet"].turbulence'
  ...     '.turbulent_intensity',
  ...     5.0,
  ... )
  >>> out.ok
  True
  >>> out.fixes_applied
  ['clamp']
  >>> out.attempts
  2
  >>> out.old_value, out.new_value
  (0.05, 1)

In transparent mode the same thing happens through ordinary PyFluent code --
``cold_inlet.turbulence.turbulent_intensity = 5.0`` simply succeeds with the value
clamped to ``1``.

**Example -- disallowed value snapped (verified on Fluent 27.1.0).** A near-miss of
an allowed enumeration value is snapped to the nearest valid entry:

.. code:: python

  >>> # 'Intensity and Hydraulic Diamete' (typo) -> nearest allowed value
  >>> cold_inlet.turbulence.turbulence_specification = "Intensity and Hydraulic Diamete"
  >>> cold_inlet.turbulence.turbulence_specification()
  'Intensity and Hydraulic Diameter'

**Inactive targets: automatic model activation (live discovery).** Many settings
are *inactive* until a governing model is enabled -- for example a thermal boundary
condition is inactive while the energy model is off, and Fluent raises
``InactiveObjectError`` the moment you navigate into it
(``cold_inlet.thermal.temperature.value = 293.15``). Resilient mode handles this
transparently by **live introspection rather than guesswork**: it tentatively
enables each candidate governing model that is currently off, re-checks whether
the target has become active, and keeps only the model that actually activates it
(reverting the rest). So in resilient mode the write above simply succeeds -- the
energy model is discovered and enabled automatically, then the value is applied.

.. code:: python

  >>> # energy model is off; resilient mode enables it automatically
  >>> cold_inlet.thermal.temperature.value = 293.15
  >>> solver.settings.setup.models.energy.enabled()
  True

This discovery happens both when navigating into an inactive branch (a guarded
wrapper around the settings tree's attribute access, active only for resilient
sessions) and when a write reaches the service layer. If **no** model activates
the target (for example it requires a zone-type assignment instead), the original
``InactiveObjectError`` is re-raised unchanged -- the runtime never enables models
blindly.

**Bounded retries.** Recovery is capped (``max_resolver_attempts``, default
``3``). If no safe fix can be derived, the runtime raises
``UnrecoverableStepError`` with the original Fluent error chained as the cause --
it never silently swallows a failure.


Feature 2 -- two-tier checkpoints and undo / redo
-------------------------------------------------

Reversible settings changes and irreversible commands require different
checkpoint strategies, so the runtime keeps **two tiers** under a single
undo / redo stack:

* **Settings tier** -- an in-memory snapshot of one or more settings subtrees via
  ``get_state`` (cheap, no disk). Restored with ``set_state``. Use this for
  reversible parameter changes.
* **File tier** -- a case/data file written with
  ``settings.file.write_case_data`` and reloaded with ``read_case_data``. This is
  the only way to undo *irreversible* operations such as ``iterate`` or
  ``read_case``, which cannot be reversed by ``set_state``.

Take a checkpoint explicitly:

.. code:: python

  >>> rsolver.checkpoint("before-bcs", kind=CheckpointKind.SETTINGS,
  ...                    paths=["setup.boundary_conditions"])   # lightweight
  >>> rsolver.checkpoint("pre-iterate", kind=CheckpointKind.FILE)  # case + data

If you omit ``kind``, a **file** checkpoint is taken (the safest, broadest
option).

**Automatic checkpoints before irreversible commands.** ``command`` recognizes
irreversible leaves (``iterate``, ``calculate``, ``dual_time_iterate``,
``read_case``, ``read_case_data``, ``read_data``, ``read``) and takes a file
checkpoint *before* running them, so they remain undoable even if you did not ask
for a checkpoint.

**Undo / redo semantics.** ``undo`` pops the newest checkpoint and restores it.
To keep every undo redoable, the runtime first captures the *current* state (same
tier) onto the redo stack, then restores the popped entry:

* a **settings** undo snapshots the present with ``get_state`` and writes back the
  past with ``set_state``;
* a **file** undo writes the present with ``write_case_data`` and then reloads the
  past with ``read_case_data``.

.. code:: python

  >>> rsolver.set("setup.models.energy.enabled", True)
  >>> rsolver.undo()   # settings restore -> energy back to its previous value
  >>> rsolver.redo()   # re-applies the change

Taking any *new* checkpoint clears the redo stack (a new branch of history).
``rewind_to("name")`` undoes repeatedly until the named checkpoint has been
restored.

.. note::

   Undo is a **state + data** rollback, not a wall-clock rewind. Reloading a case
   restores the mesh, settings, and solution data, but transient artifacts such
   as residual history or monitor plots are not reconstructed.

**Disk usage.** File checkpoints are written to the directory configured by
:class:`FileCheckpointConfig` (default ``resilient_checkpoints/``) and pruned with
a ring buffer (``keep_last``, default ``5``). Set ``data=False`` to checkpoint the
case only (smaller, faster) when solution data does not need to be preserved.
Checkpoint labels that contain path-like characters (dots, colons) are sanitized
before they become file names, so they are safe on Windows.

**Fail-fast pre-flight checks.** A case/data write or read is a *synchronous*
Fluent command: if the server-side file operation fails in a way that never
returns a response (an illegal file name, a missing or unwritable directory, an
over-long path, or -- on restore -- a missing / empty / unreadable artifact), the
client can block indefinitely. To avoid that, the file-checkpoint tier validates
the target **locally, before** issuing the command, and raises an immediate,
actionable ``CheckpointError`` instead. This turns a latent stall into a clear
error you can act on.

.. note::

   The pre-flight checks guard the file-checkpoint operations the runtime issues
   itself. They do not impose any client-side timeout on Fluent commands in
   general. A broader "a command was accepted but never returned" detector would
   build on the Fluent **transcript stream** (observing that an in-flight command
   has produced no new transcript output), which is a possible future addition --
   the runtime deliberately does not time out Fluent operations on your behalf
   today.


Feature 3 -- the warm session pool
----------------------------------

A single catastrophic solver error normally forces you to cold-launch a fresh
Fluent session and replay your whole setup. The warm pool avoids that by keeping
additional sessions ready.

* ``pool_size=1`` (the **default**) keeps a single session and consumes no extra
  licenses or resources. Failover is disabled -- there is nothing to fail over to.
* ``pool_size=N`` (``N > 1``) launches ``N - 1`` **warm standby** sessions
  eagerly, so a failover is near-instant. Each standby consumes a license and
  host resources (RAM and cores), so choose ``N`` deliberately.

.. code:: python

  >>> rsolver = ResilientSolver(session, pool_size=3)  # 1 active + 2 standbys

**Health monitoring.** Every session is watched by a
:class:`SessionHealthMonitor` that combines two signals:

* a push-based subscription to the ``FATAL_ERROR`` solver event (the exact event
  that flips Fluent's shared error state) -- near-instant, zero steady-state cost;
* a slow poll backstop (default every ``2`` seconds) that also catches a hard
  crash whose event never arrived.

Fatal state is *sticky* and the detector is thread-safe. The event callback only
flips a flag -- it performs no RPCs.

Standby launch keyword arguments are taken from the pool configuration. When you
use :meth:`ResilientSolver.launch`, the arguments you pass are reused for the
standbys:

.. code:: python

  >>> rsolver = ResilientSolver.launch(pool_size=3, mode="solver",
  ...                                  precision="double", processor_count=2)


Feature 4 -- failover and checkpoint replay
-------------------------------------------

When the active session enters a fatal state, a ``set`` or ``command`` on it
raises a *catastrophic* error. The runtime then:

#. promotes the healthiest **warm standby** to active;
#. **replays the last good checkpoint** onto it; and
#. retries the failed operation once on the new active session.

The returned :class:`StepOutcome` has ``failed_over=True`` so you can tell a
failover happened.

**Why replay from a checkpoint, not from the dead session?** Once Fluent is
fatal, every RPC to it is refused -- you cannot read its state. Recovery therefore
relies solely on the last checkpoint:

* with ``replay_from="auto"`` (default), the newest **file** checkpoint is
  reloaded as the base (mesh + settings + data) and the newest **settings**
  snapshot is layered on top for any changes made after that file was written;
* ``replay_from="file"`` reloads only the newest file checkpoint;
* ``replay_from="settings"`` restores only the newest settings snapshot.

This is why the runtime auto-checkpoints before irreversible commands and why you
should take a checkpoint before risky steps -- anything changed after the last
checkpoint cannot be recovered on the standby.

.. code:: python

  >>> with ResilientSolver(session, pool_size=3) as rsolver:
  ...     rsolver.command("file.read_case", file_name="elbow.cas.h5")
  ...     rsolver.checkpoint("configured")          # replay base
  ...     out = rsolver.set("setup.models.energy.enabled", True)
  ...     out.failed_over   # True if the active died and a standby took over

If the pool has no healthy standby (for example ``pool_size=1``), or if replaying
the checkpoint onto the standby fails, the runtime raises ``FailoverError`` rather
than silently continuing on a broken session. The dead session is retired off the
critical path, and the pool refills a replacement standby in the background.


Configuration
-------------

:class:`ResilientConfig` groups every option:

.. code:: python

  >>> from ansys.fluent.core.resilient import (
  ...     ResilientConfig, PoolConfig, FileCheckpointConfig,
  ... )
  >>> config = ResilientConfig(
  ...     pool=PoolConfig(size=3, health_interval=2.0, replay_from="auto"),
  ...     file_checkpoint=FileCheckpointConfig(
  ...         directory="my_checkpoints", keep_last=10, data=True,
  ...     ),
  ...     max_resolver_attempts=3,
  ...     auto_file_checkpoint_before_irreversible=True,
  ... )
  >>> rsolver = ResilientSolver(session, config=config)


Error handling
--------------

Resilient-runtime errors all derive from
:class:`~ansys.fluent.core.resilient.ResilientError` and always chain the
underlying Fluent error as the cause (``raise ... from err``):

================================  ==================================================
Exception                         Raised when
================================  ==================================================
``UnrecoverableStepError``        A step failed and no safe automatic fix applied (session still usable).
``FailoverError``                 No healthy standby, or replay onto the standby failed.
``CheckpointError``               A checkpoint could not be captured, restored, or found.
``PathResolutionError``           A settings path could not be resolved on the live tree.
================================  ==================================================


End-to-end example
------------------

A complete, runnable mixing-elbow example -- read the case, configure boundary
conditions (with a deliberately out-of-range value that is auto-recovered),
checkpoint, iterate, and undo -- is available at
:ref:`ref_mixing_elbow_resilient`.
