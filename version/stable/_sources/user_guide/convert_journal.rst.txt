.. _ref_convert_journal:

Converting TUI Journals to Python
=================================

The ``topy`` and ``journal_file_names`` arguments in the :func:`launch_fluent() <ansys.fluent.core.launch_fluent>` function is utilized to convert TUI journals into Python journals. 
This process supports the conversion of multiple TUI journals by passing a list of TUI journal files.

.. code-block:: python

  >>> # Write the converted Python commands from journal.jou to journal.py
  >>> solver = pyfluent.launch_fluent(journal_file_names="journal.jou", topy=True)
  >>> solver.exit()
  >>>
  >>> # Write the converted Python commands from journal.jou to journal_1.py
  >>> solver = pyfluent.launch_fluent(journal_file_names="journal.jou", topy="journal_1.py")
  >>> solver.exit()
  >>>
  >>> # Write the converted Python commands from journal_1.jou and then from journal_2.jou to a single file journal_1_journal_2.py
  >>> solver = pyfluent.launch_fluent(journal_file_names=["journal_1.jou", "journal_2.jou"], topy=True)
  >>> solver.exit()
  >>>
  >>> # Write the converted Python commands from journal_1.jou and then from journal_2.jou to journal_1_2.py
  >>> solver = pyfluent.launch_fluent(journal_file_names=["journal_1.jou", "journal_2.jou"], topy="journal_1_2.py")
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
