.. _ref_user_guide_events_manager:

Use events manager
==================

The following code triggers a callback at the end of every iteration.

.. code-block:: python

    def callback_executed_at_end_of_iteration(session_id, event_info):
        print("Iteration ended index", event_info.index)

    cb_itr_id = session.events_manager.register_callback('IterationEndedEvent', callback_executed_at_end_of_iteration)
