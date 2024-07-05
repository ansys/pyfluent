.. _ref_events_guide:

EventsManager
=============

Each solver session object has an ``events`` child of type ``EventsManager``. You can call
the ``events.register_callback()`` method in order to receive notifications of various events
occurring in Fluent. (The EventsManager calls each callback whenever a Fluent
event occurs, passing the session ID and event information as arguments to the callback. This
interface is subject to change). The EventsManager is useful for solution monitoring and dynamic
update of graphics.

Supported events are:

- ``CalculationsEndedEvent``
- ``CalculationsStartedEvent``
- ``CaseReadEvent, DataReadEvent``
- ``InitializedEvent``
- ``IterationEndedEvent``
- ``ProgressEvent``
- ``TimestepEndedEvent``

The following code triggers a callback at the end of every iteration.

.. code-block:: python

    def callback_executed_at_end_of_iteration(session_id, event_info):
        print("Iteration ended index", event_info.index)

    cb_itr_id = session.events.register_callback('IterationEndedEvent', callback_executed_at_end_of_iteration)
