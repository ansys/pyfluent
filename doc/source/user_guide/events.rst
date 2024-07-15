.. _ref_events_guide:

EventsManager
=============

Each solver session object has an ``events`` child of type ``EventsManager``. You can call
the ``events.register_callback()`` method in order to receive notifications of various events
occurring in Fluent. (The EventsManager calls each callback whenever a Fluent
event occurs, passing the relevant solver session object and event information as arguments to the
callback). The EventsManager is useful for solution monitoring and dynamic update of graphics.

Supported events are enumerated by the PyFluent ``Event`` class.

The following code triggers a callback at the end of every iteration.

.. code-block:: python

    >>> from ansys.fluent.core import Event
    >>>
    >>> def on_iteration_ended(session, event_info):
    >>>     print("Iteration ended. Index = ", event_info.index)
    >>>
    >>> callback_id = solver.events.register_callback(Event.ITERATION_ENDED, on_iteration_ended)
