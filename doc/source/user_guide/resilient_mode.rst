.. _ref_resilient_guide:

.. vale Google.Spacing = NO

Resilient mode
==============

Resilient mode allows an automated setup-and-solve script to continue running
despite failures that would normally halt execution, all while letting you write
standard PyFluent code. Resilient mode works for solver sessions now:

* **Checkpoints and rollback**: irreversible commands such as ``iterate``,
  ``calculate`` and ``read_case`` are preceded by an automatic case and data
  checkpoint. If such a command fails, the session is restored to that
  checkpoint and the original error is raised.
* **Undo and redo** of settings writes from a journal.
* **Failover**: with a warm pool of standby sessions, your script keeps running
  on a standby session when the active solver process dies, resuming from the
  latest checkpoint.

Resilient mode does not alter your settings. A value that Fluent rejects raises
the original error unchanged, so your existing ``except`` clauses keep working.

Resilient mode is available for solver sessions that PyFluent launches over
gRPC. It does not apply to sessions you connect to, meshing sessions, or REST
(``HttpSolver``) sessions.


Enable resilient mode
---------------------

Every function that launches a solver session accepts ``resilient_mode`` and
``resilient_config``:

.. code-block:: python

    import ansys.fluent.core as pyfluent
    from ansys.fluent.core.resilient import PoolConfig, ResilientConfig

    solver = pyfluent.Solver.from_install(resilient_mode=True)

    # The same options apply to launch_fluent, Solver.from_container and
    # Solver.from_pim.
    solver = pyfluent.Solver.from_install(
        resilient_mode=True,
        resilient_config=ResilientConfig(pool=PoolConfig(size=2)),
    )

Once enabled, ``solver.resilient`` gives access to every resilient-mode
feature. :func:`~ansys.fluent.core.resilient.is_resilient` tells whether a session
is resilient, and ``solver.resilient.disable()`` turns resilient mode off.


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

    solver = pyfluent.Solver.from_install(
        resilient_mode=True,
        resilient_config=ResilientConfig(pool=PoolConfig(size=2)),
    )

``PoolConfig.size`` counts the active session, so ``size=2`` launches one
standby with the same launch arguments as the active session. If the active
session dies, the next settings call fails over: a standby session takes over,
rebuilt from the latest checkpoint and the settings calls that succeeded since,
and a :class:`~ansys.fluent.core.resilient.ResilientFailoverWarning` is emitted.
A read is then repeated on the standby, so your script continues.

A write or command that was running when the session died is not repeated on
the standby, because it may be what made Fluent fail. Its original error is
raised with a note, and the standby has the state from before that call. Run
the call again to apply it on the standby.

Keep these points in mind:

* Take a checkpoint once your case is loaded. Failover resumes from the latest
  checkpoint; without one, the standby starts from an empty session.
* Failover reroutes ``solver.settings``. Use ``solver.resilient.active_session``
  to reach other services, such as field data, of the session now serving.
* Standbys are launched automatically for local standalone sessions. For
  container, PIM or remote sessions, pass ``PoolConfig.launch_kwargs`` or
  ``PoolConfig.launcher``.
* Exiting ``solver`` exits all the sessions of the pool.


Event listeners and logging
---------------------------

Register a listener to react to what resilient mode does:

.. code-block:: python

    def show(event):
        print(f"[{event.kind.value}] {event.message}")

    solver.resilient.on_event(show)

Each event has one of the kinds listed in
:class:`~ansys.fluent.core.resilient.EventKind`: ``CHECKPOINT``, ``ROLLBACK``,
``UNDO``, ``REDO`` and ``FAILOVER``. The same information is logged on the
``ansys.resilient`` logger, and ``solver.resilient.journal.to_script()`` returns
the journal as plain data.

If resilient mode cannot do something it normally does, for example when an
automatic checkpoint fails, it emits a
:class:`~ansys.fluent.core.resilient.ResilientWarning`.


Configuration reference
-----------------------

.. list-table::
   :header-rows: 1

   * - Option
     - Default
     - Description
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
