Launching Ansys Fluent Locally
===============================
Fluent can be started from python in gRPC mode using
:func:`launch_fluent() <ansys.fluent.core.launcher.launcher.launch_fluent>`.
This starts Fluent in the background and sends commands to that service.

.. code:: python

    import ansys.fluent.core as pyfluent
    solver_session = pyfluent.launch_fluent()

Fluent is now active and you can send commands to it as a genuine a
Python class.


Launcher Options
-----------------
Examples:


Solver Mode
~~~~~~~~~~~~

.. code:: python

   solver_session = pyfluent.launch_fluent()

Meshing Mode
~~~~~~~~~~~~~
.. code:: python

   meshing_session = pyfluent.launch_fluent(meshing_mode=True)

Precision
~~~~~~~~~~

.. code:: python

   solver_session = pyfluent.launch_fluent(precision="double")

Dimension
~~~~~~~~~~

.. code:: python

   solver_session = pyfluent.launch_fluent(precision="double", version="2d")

Number of Processors
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   solver_session = pyfluent.launch_fluent(precision="double", version="2d", processor_count=2)

API Reference
--------------
For more details for controlling how Ansys Fluent launches locally, see the
function description of :func:`launch_fluent() <ansys.fluent.core.launcher.launcher.launch_fluent>`.