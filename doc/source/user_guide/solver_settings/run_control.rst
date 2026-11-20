.. _ref_run_control:

Interrupting and resuming a solver run
============================================================

Use ``solver_session.settings.solution.run_calculation.interrupt()`` to stop
a running calculation cleanly. Call ``iterate()`` again to continue from the
current solution, without reinitializing or reloading the case. These commands
are part of the :ref:`solver settings API <ref_solver_settings_guide>`.

Interrupt and resume outside a callback
------------------------------------------------------------

The following example assumes that ``solver_session`` has a loaded case.
It interrupts after ten iterations, checks how many iterations were completed,
and runs only the remaining iterations.

.. code-block:: python

   from ansys.fluent.core import SolverEvent

   solution = solver_session.settings.solution
   total_iterations = 30
   solution.initialization.hybrid_initialize()
   initial_iteration = solver_session.scheme.eval("(get-current-iteration)")
   interrupt_requested = []

   def on_iteration_ended(session, event_info):
       if event_info.index >= initial_iteration + 10 and not interrupt_requested:
           interrupt_requested.append(event_info.index)
           session.settings.solution.run_calculation.interrupt()

   callback_id = solver_session.events.register_callback(
       SolverEvent.ITERATION_ENDED, on_iteration_ended
   )
   try:
       solution.run_calculation.iterate(iter_count=total_iterations)
       completed_iterations = (
           solver_session.scheme.eval("(get-current-iteration)") - initial_iteration
       )
       assert interrupt_requested
       assert 10 <= completed_iterations < total_iterations
       solution.run_calculation.iterate(
           iter_count=total_iterations - completed_iterations
       )
   finally:
       solver_session.events.unregister_callback(callback_id)

Callback holds and self-unregistration
------------------------------------------------------------

``ITERATION_ENDED`` and ``TIMESTEP_ENDED`` callbacks execute on the event-stream
thread while Fluent holds the solver. Normally, PyFluent releases that hold
after the callback returns, including when the callback raises an exception.

A callback can unregister itself using
:meth:`~ansys.fluent.core.services.streaming_services.events_streaming.EventsManager.unregister_callback`.
This disables future invocations and explicitly releases that callback's
current hold before unregistration returns. Other callbacks or connected
clients retain their own holds.

An interrupted calculation can be restarted inside a callback after releasing
its hold. The following pattern requires that no other solution-event callback
or client holds the solver or needs this event-stream thread during the nested
calculation:

.. code-block:: python

   def on_iteration_ended(session, event_info):
       if event_info.index < initial_iteration + 10:
           return
       session.settings.solution.run_calculation.interrupt()
       session.events.unregister_callback(callback_id)
       completed_iterations = (
           session.scheme.eval("(get-current-iteration)") - initial_iteration
       )
       session.settings.solution.run_calculation.iterate(
           iter_count=total_iterations - completed_iterations
       )

Use the outside-callback workflow when other solution callbacks are registered.
Nested calls block event processing until they return. The original
``iterate()`` can return before the nested calculation finishes, so callers
that need its result must explicitly synchronize with callback completion.
Do not restart while the solver is still held: ``iterate()`` can be inactive.
This nested restart pattern has been verified with Fluent 2027 R1.
See :ref:`Observing events <ref_events_guide>` for callback registration and
monitoring.

Interrupt, pause, and reload
------------------------------------------------------------

An interrupt ends the current solve command while preserving the in-memory
solution. A new solve command continues from that solution. It does not suspend
and later resume the same command.

An event hold temporarily pauses the current command while a callback examines
or changes the model. Releasing the hold normally lets that command continue;
releasing it after ``interrupt()`` lets the command stop.

Saving case and data files provides a persistent checkpoint that can be
reloaded in a later session. Saving and reloading is not required to continue
an interrupted calculation in the same session.
