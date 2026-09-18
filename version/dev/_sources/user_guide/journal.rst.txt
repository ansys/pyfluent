.. _ref_journal_guide:

Journaling
==========

Journaling allows you to record and play back your Fluent interactions as Python
scripts (journals) seamlessly across the entire ecosystem of PyFluent, Fluent, and the Fluent Web UI
without making any adjustments. Here's how you can record a Fluent Python journal:

.. code-block:: python

  >>> solver_session.journal.start(file_name="pyfluent_journal.py")
  <Python code>
  >>> solver_session.journal.stop()


The software creates or overwrites the file specified by
``file_name``, and reflects scripted and interactive actions
via Python code written to the file until the ``stop()`` method is called.

The following rules govern what is written to the journal:

#. **PyFluent actions**: Interactions with solver settings, meshing and solver workflows,
   preferences, and Python TUI commands are written to journal. Other Python code you
   execute is not.

#. **Commands versus queries**: Commands (actions with a side effect, such as reading a
   case file or changing a boundary condition) are written to journal. Queries (requests
   for data, such as an area-averaged pressure) are not.

#. **Non-GUI actions in Fluent**: Calls made from the Fluent Python console, or from
   external clients such as the Fluent Web UI, are treated the same as PyFluent calls.
   Direct Fluent TUI commands are written to journal; Scheme calls are not.

#. **Fluent GUI actions**: Guided workflow commands (including meshing workflows) and
   preferences panel commands are written to journal. Other solution mode GUI commands
   are not; use the Fluent Web UI to journal those actions.

#. **Python output**:

   * All Python code written to journal uses method calls on PyFluent objects.

   * Any TUI call (direct or via Python) that has a settings object equivalent is written to journal as a method call on the equivalent settings object.

   * Any such TUI call that does not have a settings object equivalent is written to journal as a call to a Python TUI command object.

   * Meshing workflow calls are written to journal according to the classic meshing workflow Python interface.
