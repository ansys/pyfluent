Launching Ansys Fluent Locally
==============================
Fluent can be started from python in gRPC mode using
:func:`launch_fluent() <ansys.fluent.core.launcher.launcher.launch_fluent>`.
This starts Fluent in the background and sends commands to that service.

.. code:: python

    import ansys.fluent.core as pyfluent
    solver_session = pyfluent.launch_fluent()

Fluent is now active and you can send commands to it as a Python class.

Launcher Options
----------------
Examples:

Solver Mode
~~~~~~~~~~~
The following example demonstrates how you can start Fluent using the default launcher options:

.. code:: python

   solver_session = pyfluent.launch_fluent()

Meshing Mode
~~~~~~~~~~~~
The following example demonstrates how you can start Fluent in the meshing mode:

.. code:: python

   meshing_session = pyfluent.launch_fluent(meshing_mode=True)

Precision
~~~~~~~~~
The following example demonstrates how you can select the double precision:

.. code:: python

   solver_session = pyfluent.launch_fluent(precision="double")

Dimension
~~~~~~~~~
The following example demonstrates how you can select the 2d dimension:

.. code:: python

   solver_session = pyfluent.launch_fluent(precision="double", version="2d")

Number of Processors
~~~~~~~~~~~~~~~~~~~~
The following example demonstrates how you can select the number of processors:

.. code:: python

   solver_session = pyfluent.launch_fluent(precision="double", version="2d", processor_count=2)

API Reference
-------------
For more details on controlling how Ansys Fluent launches locally, see the
function description for :func:`launch_fluent() <ansys.fluent.core.launcher.launcher.launch_fluent>`.