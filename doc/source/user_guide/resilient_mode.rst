.. _ref_resilient_guide:

Resilient mode
==============

Resilient mode makes an automated setup-and-solve script survive the errors
that would normally stop it. You keep writing ordinary PyFluent code. Resilient
mode works inside the settings API:

* **Recovery**: a rejected value (out of range, a near-miss of an allowed
  string, or the wrong type) is repaired and applied. You get a warning.
* **Model activation** (opt-in): writing a setting that is inactive because its
  governing model is off (for example a thermal boundary condition while the
  energy model is disabled) enables that model first.
* **Checkpoints and rollback**: irreversible commands such as ``iterate``,
  ``calculate`` and ``read_case`` are preceded by an automatic case and data
  checkpoint. If such a command fails, the session is restored to that
  checkpoint and the original error is raised.
* **Undo and redo** of settings writes from a journal.
* **Failover**: with a warm pool of standby sessions, a solver that dies is
  replaced by a standby. The standby is brought to the same state from the
  newest checkpoint and the journal, and the failed call is retried.

Resilient mode only works with solver sessions. It does not apply to meshing
sessions or to REST (``HttpSolver``) sessions.


Enable resilient mode
---------------------

Every entry point that creates a solver session accepts ``resilient_mode`` and
``resilient_config``:

.. code-block:: python

    import ansys.fluent.core as pyfluent
    from ansys.fluent.core.resilient import ResilientConfig

    solver = pyfluent.launch_fluent(mode="solver", resilient_mode=True)

    # The same options apply to connect_to_fluent and to Solver.from_install,
    # Solver.from_container, Solver.from_pim and Solver.from_connection.
    solver = pyfluent.Solver.from_install(
        resilient_mode=True,
        resilient_config=ResilientConfig(allow_model_activation=True),
    )

You can also enable it on a session you already have:

.. code-block:: python

    from ansys.fluent.core.resilient import enable_resilient_mode

    enable_resilient_mode(solver)

Once enabled, ``solver.resilient`` gives access to every resilient-mode
feature. :func:`~ansys.fluent.core.resilient.is_resilient` tells whether a session
is resilient, and ``solver.resilient.disable()`` turns resilient mode off.


Recovery
--------

When Fluent rejects a write, resilient mode classifies the error and, if it can
be repaired, applies a fix and retries:

.. list-table::
   :header-rows: 1

   * - Rejected write
     - Fix
   * - Value outside the allowed range
     - Clamp to the nearest bound.
   * - String that is not an allowed value
     - Snap to the closest allowed value (close matches only).
   * - Value of the wrong type, such as ``"0.5"`` for a real
     - Convert to the expected type.
   * - Setting that is inactive
     - Enable the governing model (only when ``allow_model_activation=True``).

``ResilientConfig.recovery`` selects how a repair is reported:

* ``RecoveryPolicy.WARN`` (default): apply the fix and emit a
  :class:`~ansys.fluent.core.resilient.ResilientRecoveryWarning`.
* ``RecoveryPolicy.SILENT``: apply the fix and log it on the
  ``ansys.resilient`` logger.
* ``RecoveryPolicy.STRICT``: do not repair; raise the original error.

When a value cannot be repaired, the original Fluent error is raised unchanged,
so existing ``except`` clauses keep working.

Model activation is off by default because enabling a model changes the
physics. With ``allow_model_activation=True``, only writes trigger activation.
Reading an inactive setting raises the usual error and never changes the
model:

.. code-block:: python

    solver.settings.setup.models.energy.enabled = False
    inlet = solver.settings.setup.boundary_conditions.velocity_inlet["cold-inlet"]
    inlet.thermal.temperature.value = 293.15  # enables the energy model, then writes

Activation tries governing-model settings in turn and keeps one only if it makes
the written setting active; otherwise the change is reverted and the original
error is raised. The built-in rule enables the energy model
(``setup.models.energy.enabled``). Add rules for your own cases with
``ResilientConfig.activation_candidates``; they are tried before the built-in
rule:

.. code-block:: python

    from ansys.fluent.core.resilient import ActivationCandidate, ResilientConfig

    config = ResilientConfig(
        allow_model_activation=True,
        activation_candidates=(
            ActivationCandidate("setup.models.viscous.model", "k-omega"),
        ),
    )


Checkpoints and rollback
------------------------

With ``auto_checkpoint=True`` (default), resilient mode writes a checkpoint
before each irreversible command once the session has a valid case. If the
command fails and ``auto_rollback=True`` (default), the session is restored to
that checkpoint and the original exception is raised with a note that says
so. ``solver.resilient.last_outcome.rolled_back`` is then ``True``. If the
checkpoint cannot be restored, the note says that instead and ``rolled_back``
is ``False``.

.. code-block:: python

    try:
        solver.settings.solution.run_calculation.calculate()
    except RuntimeError:
        # The session is back at the state before calculate().
        solver.settings.solution.run_calculation.transient_controls.time_step_size = 1e-3
        solver.settings.solution.run_calculation.calculate()

Named checkpoints can also be written and restored explicitly:

.. code-block:: python

    solver.resilient.checkpoint("initialized")
    solver.settings.solution.run_calculation.iterate(iter_count=100)
    solver.resilient.rollback("initialized")  # or rollback() for the newest one

Rolling back discards newer checkpoints. Checkpoints are written to a
``<run-id>`` folder in ``CheckpointConfig.directory``, or in
``resilient_checkpoints`` under the current working directory by default. Only
the newest ``CheckpointConfig.keep_last`` checkpoints are kept. Set
``include_data=False`` to write case files only.

When Fluent runs on a host or container that does not share the client's file
system, checkpoints are written to the Fluent working directory instead.


Undo and redo
-------------

Every settings write is journaled together with the previous value:

.. code-block:: python

    solver.settings.setup.models.viscous.model = "laminar"
    solver.resilient.undo()  # restores the previous viscous model
    solver.resilient.redo()  # applies "laminar" again

Undo applies to settings writes only. Commands such as ``iterate`` are reverted
by rolling back to a checkpoint. To capture the previous value, resilient mode
reads each setting before writing it, which costs one extra server round trip
per write. Writes to the whole settings tree are not read back and cannot be
undone.


Failover
--------

Failover needs at least one warm standby session:

.. code-block:: python

    from ansys.fluent.core.resilient import PoolConfig, ResilientConfig

    solver = pyfluent.launch_fluent(
        mode="solver",
        resilient_mode=True,
        resilient_config=ResilientConfig(pool=PoolConfig(size=2)),
    )

``PoolConfig.size`` counts the active session, so ``size=2`` launches one
standby with the same launch arguments as the active session. If the active
session dies during a settings write or command, resilient mode:

#. promotes a healthy standby,
#. restores the newest checkpoint on it and replays the journaled operations
   recorded since then,
#. retries the failed call, and
#. emits a :class:`~ansys.fluent.core.resilient.ResilientFailoverWarning`.

A replacement standby is launched in the background.

Keep these limits in mind:

* Failover reroutes ``solver.settings``. Other services of the dead session, such
  as field data, are not rerouted. Use ``solver.resilient.active_session`` to
  reach the session that is currently serving.
* Replay starts from the newest checkpoint. Without a checkpoint, the standby
  starts from launch state, so take a checkpoint once the case is loaded.
* The failed call is retried once, on the standby. If the call itself crashed
  the server, the retry fails too and its error is raised.
* Standbys are launched automatically only for local standalone sessions. For
  container, PIM or remote sessions, pass ``PoolConfig.launch_kwargs`` or
  ``PoolConfig.launcher``.
* Exiting ``solver`` exits all the sessions of the pool.


Events and logging
------------------

Register a listener to react to what resilient mode does:

.. code-block:: python

    def show(event):
        print(f"[{event.kind.value}] {event.message}")

    solver.resilient.on_event(show)

Events are of the kinds listed in
:class:`~ansys.fluent.core.resilient.EventKind`: ``RECOVERED``, ``ACTIVATED``,
``CHECKPOINT``, ``ROLLBACK``, ``UNDO``, ``REDO`` and ``FAILOVER``. The same
information is logged on the ``ansys.resilient`` logger, and
``solver.resilient.journal.to_script()`` returns the journal as plain data.

If resilient mode cannot do something it normally does, for example when an
automatic checkpoint fails or a failed repair cannot be fully reverted, it emits a
:class:`~ansys.fluent.core.resilient.ResilientWarning` whatever the recovery
policy.


Configuration reference
-----------------------

.. list-table::
   :header-rows: 1

   * - Option
     - Default
     - Description
   * - ``recovery``
     - ``RecoveryPolicy.WARN``
     - How repairs are reported, or ``STRICT`` to disable them.
   * - ``allow_model_activation``
     - ``False``
     - Enable a governing model when an inactive setting is written.
   * - ``activation_candidates``
     - ``()``
     - Additional governing-model settings to try before the built-in ones.
   * - ``max_resolver_attempts``
     - ``3``
     - Maximum repair attempts for a single write.
   * - ``auto_checkpoint``
     - ``True``
     - Checkpoint before irreversible commands.
   * - ``auto_rollback``
     - ``True``
     - Restore that checkpoint when the command fails.
   * - ``journal_max_ops``
     - ``10000``
     - Maximum number of journaled operations kept in memory.
   * - ``checkpoint``
     - ``CheckpointConfig()``
     - ``directory``, ``keep_last`` (``5``) and ``include_data`` (``True``).
   * - ``pool``
     - ``PoolConfig()``
     - ``size`` (``1``, no standby), ``launch_kwargs`` and ``launcher``.


Design
------

Resilient mode is split into a product-neutral engine and a small product
adapter:

* ``ansys.fluent.core.resilient.engine`` holds the classifier, resolver,
  journal, checkpoint store, warm pool and controller. It depends only on the
  Python standard library, so other Ansys clients can reuse it. PyCFX uses it
  through ``ansys-cfx-core[resilient]``.
* :class:`~ansys.fluent.core.resilient.FluentAdapter` implements the Fluent
  details: error types, health checks, checkpoint I/O, launching standbys and
  the list of irreversible commands.

The controller wraps the session's settings service. Every write, command and
named-object change made through ``solver.settings`` therefore goes through
resilient mode without any change to the settings classes.
