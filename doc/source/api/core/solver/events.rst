.. _ref_events:

EventsManager
=============

An instance of ``EventsManager`` exists as an active ``events_manager`` property in each
solution-mode session object. It allows to register client callback with server side events.
Whenever event occurs, the registered callback is triggered with session id and event info 
passed as arguments to callback. It is useful in solution monitoring and updating graphics 
during run time.

Supported events are:
``CalculationsEndedEvent, CalculationsStartedEvent, CaseReadEvent, DataReadEvent, 
InitializedEvent, IterationEndedEvent, ProgressEvent, TimestepEndedEvent``

Following code will trigger callback at end of every iteration.

.. code-block:: python

    def callback_executed_at_end_of_iteration(session_id, event_info):
        print("Iteration ended index", event_info.index)

    cb_itr_id = session.events_manager.register_callback('IterationEndedEvent', callback_executed_at_end_of_iteration)        

.. currentmodule:: ansys.fluent.core.solver.events_manager

.. autosummary::
   :toctree: _autosummary
   
.. automethod:: ansys.fluent.core.solver.events_manager.EventsManager.register_callback
.. automethod:: ansys.fluent.core.solver.events_manager.EventsManager.unregister_callback   


 