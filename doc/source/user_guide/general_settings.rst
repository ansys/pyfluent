Applying General Settings
=========================

Text User Interface (TUI) API
-----------------------------
The following example demonstrates how you can use some general
settings using the TUI API:

Checking Mesh
~~~~~~~~~~~~~

.. code:: python

	import ansys.fluent.core as pyfluent
	session = pyfluent.launch_fluent(precision="double", processor_count=2)
	session.solver.tui.file.read_case(case_file_name='file.cas.h5')
	session.solver.tui.mesh.check()
	
Reporting Mesh Quality
~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

	session.solver.tui.mesh.quality()
	
Defining Units
~~~~~~~~~~~~~~

.. code:: python

	session.solver.tui.define.units("length", "in")