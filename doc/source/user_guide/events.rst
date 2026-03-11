.. _ref_events_guide:

.. vale Google.Spacing = NO

Observing events
================

Each session object has an ``events`` child of type :obj:`~ansys.fluent.core.streaming_services.events_streaming.EventsManager`. You can call
the ``events.register_callback()`` method in order to receive notifications of various events
occurring in Fluent. (The :obj:`~ansys.fluent.core.streaming_services.events_streaming.EventsManager` object calls each callback whenever a Fluent
event occurs, passing the relevant session object and event information as arguments to the
callback). The :obj:`~ansys.fluent.core.streaming_services.events_streaming.EventsManager` object is useful for solution monitoring and dynamic update
of graphics.

Supported events are enumerated by the PyFluent :obj:`~ansys.fluent.core.streaming_services.events_streaming.SolverEvent` and :obj:`~ansys.fluent.core.streaming_services.events_streaming.MeshingEvent` classes.

The following code triggers a callback at the end of every iteration.

.. code-block:: python

  >>> from ansys.fluent.core import SolverEvent, IterationEndedEventInfo
  >>>
  >>> def on_iteration_ended(session, event_info: IterationEndedEventInfo):
  >>>     print("Iteration ended. Index = ", event_info.index)
  >>>
  >>> callback_id = solver_session.events.register_callback(SolverEvent.ITERATION_ENDED, on_iteration_ended)

The general signature of the callback function is ``cb(session, event_info, <additional arguments>)``, where ``session`` is the session instance
and ``event_info`` instance holds information about the event. The event information classes for each event are documented in the
API reference of the :obj:`~ansys.fluent.core.streaming_services.events_streaming` module. See the callback function
``on_case_loaded_with_args()`` in the below examples for an example of how to pass additional arguments to the callback
function.


Examples
--------

This script demonstrates how to use the Fluent event callback mechanism in PyFluent
to trigger a custom Python function when a specific solver event occurs. In this example,
a callback is registered to the CASE_LOADED event. When a case file is read into the solver,
the registered function is automatically called, allowing users to perform custom actions
(like logging, validation, or automated workflows) immediately after the case is loaded.

.. code-block:: python

  >>> import ansys.fluent.core as pyfluent
  >>> from ansys.fluent.core import SolverEvent, examples
  >>> case_file_name = examples.download_file(
  >>>     "mixing_elbow.cas.h5", "pyfluent/mixing_elbow"
  >>> )
  >>> def on_case_loaded(session, event_info):
  >>>     on_case_loaded.loaded = True

  >>> on_case_loaded.loaded = False

  >>> solver_session = pyfluent.launch_fluent()
  >>> solver_session.events.register_callback(SolverEvent.CASE_LOADED, on_case_loaded)

  >>> on_case_loaded.loaded
  False

  >>> solver_session.settings.file.read_case(file_name=case_file_name)

  >>> on_case_loaded.loaded
  True


The next example demonstrates how to register multiple event callbacks with additional arguments
in PyFluent's event handling system.
It builds on the basic usage of event callbacks by showcasing how to pass both positional and
keyword arguments to the callback functions. The script registers three different callbacks to the CASE_LOADED event:

1. A simple callback that sets a flag when the case is loaded.

2. A callback that accepts optional arguments (x, y) before the standard parameters.

3. A callback that expects x and y after the standard parameters.

When a case file is read into Fluent, all three callbacks are triggered in order,
and their internal state is updated accordingly. This pattern is useful for building flexible,
reusable handlers that can react differently based on runtime configuration or contextual data.

.. code-block:: python

  >>> import ansys.fluent.core as pyfluent
  >>> from ansys.fluent.core import SolverEvent, examples
  >>> case_file_name = examples.download_file(
  >>>     "mixing_elbow.cas.h5", "pyfluent/mixing_elbow"
  >>> )
  >>> def on_case_loaded(session, event_info):
  >>>     on_case_loaded.loaded = True

  >>> on_case_loaded.loaded = False

  >>> def on_case_loaded_with_args_optional_first(x, y, session, event_info):
  >>>     on_case_loaded_with_args_optional_first.state = dict(x=x, y=y)

  >>> on_case_loaded_with_args_optional_first.state = None

  >>> def on_case_loaded_with_args(session, event_info, x, y):
  >>>     on_case_loaded_with_args.state = dict(x=x, y=y)

  >>> on_case_loaded_with_args.state = None

  >>> solver_session = pyfluent.launch_fluent()

  >>> solver_session.events.register_callback(SolverEvent.CASE_LOADED, on_case_loaded)
  >>> solver_session.events.register_callback(SolverEvent.CASE_LOADED, on_case_loaded_with_args_optional_first, 12, y=42)
  >>> solver_session.events.register_callback(SolverEvent.CASE_LOADED, on_case_loaded_with_args, 12, y=42)

  >>> on_case_loaded.loaded
  False

  >>> solver_session.settings.file.read_case(file_name=case_file_name)

  >>> on_case_loaded.loaded
  True
  >>> on_case_loaded_with_args_optional_first.state
  {'x': 12, 'y': 42}
  >>> on_case_loaded_with_args.state
  {'x': 12, 'y': 42}
