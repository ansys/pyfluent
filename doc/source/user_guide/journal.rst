.. _ref_journal_guide:

Journaling
==========

Journaling allows you to record and play back Python journals seamlessly 
across the entire ecosystem of PyFluent, Fluent, and the Fluent Web UI
without making any adjustments. Here's how you can record a Python journal:

.. code-block:: python

  >>> solver.journal.start(file_name="pyfluent-journal.py")
  <Python code>
  >>> solver.journal.stop()


The software creates or overwrites the file specified by
``file_name``, and reflects scripted and interactive actions
via Python code written to the file until the ``stop()`` method is called.

The following rules specify what is written to the journal:

#. **PyFluent actions**.
  * Many PyFluent actions are journaled: all interactions with solver settings, meshing and solver workflows, preferences and Python TUI commands.
  * Any other Python code that you execute is omitted from the journal.

#. **Commands versus Queries**. 
  * Commands are journaled but queries are omitted.
  * A command is any action that causes a change or side effect, e.g., reading a case file, modifying a boundary condition setting.
  * A query is a request to get data, e.g., computing an area average of pressure, getting a boundary condition setting.

#. **Non-GUI actions in Fluent**.
  * Python calls in Fluent itself, such as those made in the Fluent Python console, are treated equivalently as if they originated in PyFluent.
  * Commands received from external clients, such as the Fluent Web UI, are treated equivalently as if they originated in PyFluent.  
  * Commands invoked directly via the Fluent TUI are journaled.
  * Calls made in the Scheme programming language are not journaled.

#. **Fluent GUI actions**.
  * Commands actioned through Fluent guided workflow GUIs are journaled. This includes meshing workflows actions in the meshing mode GUI.
  * Commands actioned through the preferences panel in either meshing or solution mode are journaled.
  * Other commands actioned through the solution mode GUI are not journaled. To journal based on solution mode GUI actions, use the Fluent Web UI.
  
#. **Python output**
  * All journaled Python code uses method calls to PyFluent objects.
  * Any TUI call (direct or via Python) that has a settings object equivalent is journaled as a method call on the equivalent settings object.
  * Any such TUI call that does not have a settings object equivalent is journaled as a call to a Python TUI command object.
  * Meshing workflow calls are journaled according to the classic meshing workflow Python interface. 