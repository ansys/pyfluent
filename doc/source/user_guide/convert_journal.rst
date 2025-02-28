.. _ref_convert_journal:

Converting TUI Journals to Python
=================================

The ``topy`` argument in the launch_fluent function is utilized to convert TUI journals into Python journals. 
This process supports the conversion of multiple TUI journals by passing a list of TUI journal files. 
The resulting Python journal files are created in the working directory, retaining the same names as their TUI counterparts.

.. code-block:: python

  >>> solver = pyfluent.launch_fluent(topy="my_journal.jou")
  >>> solver.exit()
  >>> solver = pyfluent.launch_fluent(topy=["my_journal1.jou", "my_journal2.jou"])
  >>> solver.exit()


Recording a Python Journal
==========================

Journaling enables seamless recording and playback of Fluent interactions as Python scripts across PyFluent, Fluent, and 
the Fluent Web UI without requiring adjustments. For additional details, refer to the `Journaling <https://fluent.docs.pyansys.com/version/stable/user_guide/journal.html#journaling>`_ section. 
Here’s how to record a Fluent Python journal:

.. code-block:: python

  >>> solver.journal.start(file_name="pyfluent_journal.py")
  <Python code>
  >>> solver.journal.stop()


The specified file is created or overwritten, capturing both scripted and interactive actions as Python code until the ``stop()`` method is invoked.

**Limitations**:

   * TUI calls with settings object equivalents are recorded as method calls on those objects.

   * TUI calls without settings object equivalents are recorded as calls to Python TUI command objects. For more information, see the `Using TUI commands <https://fluent.docs.pyansys.com/version/stable/user_guide/legacy/tui.html#using-tui-commands>`_ section.
