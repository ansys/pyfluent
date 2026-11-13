.. _ref_resilient_guide:

.. vale Google.Spacing = NO

Resilient mode
==============

Resilient mode allows an automated setup-and-solve script to continue running
despite failures that would normally halt execution, all while letting you write
standard PyFluent code. Resilient mode works for solver sessions now:

* **Checkpoints and rollback**: specific commands such as ``iterate``,
  ``calculate`` and ``read_case`` are preceded by an automatic case and data
  checkpoint. If such a command fails, the session is restored to that
  checkpoint and the original error is raised.
* **Undo and redo** of settings writes from a journal.
* **Failover**: with a warm pool of standby sessions that are kept up to date
  with the active session, your script keeps running on a standby session when
  the active solver process dies.

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
standby with the same launch arguments as the active session.

Standbys are kept up to date with the active session. Every settings write,
command and object change that succeeds on the active session is applied to
each standby, in the same order, in the background, so your script does not
wait for the standbys. Undo, redo and rollback are applied as well. Calls that
fail are not applied, and neither are commands that only produce output, such
as ``write_case``, exports and printing. Solve commands such as ``iterate``
run on the standbys too, so each standby uses as much computing time as the
active session.

If the active session dies, the next settings call fails over: the standby
first applies the changes it has not applied yet, then takes over, and a
:class:`~ansys.fluent.core.resilient.ResilientFailoverWarning` is emitted. A
read is then repeated on the standby, so your script continues.

A write or command that was running when the session died is not repeated on
the standby, because it may be what made Fluent fail. Its original error is
raised with a note, and the standby has the state from before that call. Run
the call again to apply it on the standby.

A standby that cannot apply a change, for example because it rejects a value,
is out of sync, and a :class:`~ansys.fluent.core.resilient.ResilientWarning`
is emitted. An interrupted solve also puts the standbys out of sync, because
it stopped part way. The next checkpoint brings them back in sync. If a
standby that is out of sync must take over, it is rebuilt from the latest
checkpoint and the changes made since. A standby launched to replace one that
took over is brought up to date the same way.

To wait until every standby applied the changes made so far, call
``solver.resilient.wait_for_standbys()``. It returns whether every standby is
in sync.

Keep these points in mind:

* Take a checkpoint once your case is loaded. It is the starting point for
  bringing standbys back in sync.
* Failover reroutes ``solver.settings``. Use ``solver.resilient.active_session``
  to reach other services, such as field data, of the session now serving.
* Standbys are launched automatically for sessions that PyFluent launches on
  your machine, directly or in a container. For PIM or remote sessions, or
  sessions that use a file transfer service, pass ``PoolConfig.launch_kwargs``
  or ``PoolConfig.launcher``.
* Exiting ``solver`` exits all the sessions of the pool.

Fluent in a container
~~~~~~~~~~~~~~~~~~~~~

Resilient mode works the same way when Fluent runs in a container:

.. code-block:: python

    import ansys.fluent.core as pyfluent
    from ansys.fluent.core.resilient import PoolConfig, ResilientConfig

    solver = pyfluent.Solver.from_container(
        resilient_mode=True,
        resilient_config=ResilientConfig(pool=PoolConfig(size=2)),
    )

Each standby is another container, started with the same arguments, so it
mounts the same host folder: ``pyfluent.config.container_mount_source``, or the
current working directory by default. Fluent's working directory in each
container is that folder, mounted at ``pyfluent.config.container_mount_target``
(``/home/container/workdir`` by default).

By default, checkpoints are written to that working directory. They appear on
the host in the mounted folder, and every standby can read them. To write them
elsewhere, give ``CheckpointConfig.directory`` as a path inside the container
that every container can read, such as a folder inside the mounted folder:

.. code-block:: python

    from ansys.fluent.core.resilient import CheckpointConfig

    config = ResilientConfig(
        checkpoint=CheckpointConfig(directory="/home/container/workdir/checkpoints"),
        pool=PoolConfig(size=2),
    )

The folder must already exist. A host path does not work, because Fluent writes
the files from inside the container. Checkpoints in a container are not deleted
when more than ``CheckpointConfig.keep_last`` are written.

Files that your script reads, such as case files, must be in the mounted folder
so that the standbys can read them too.


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
