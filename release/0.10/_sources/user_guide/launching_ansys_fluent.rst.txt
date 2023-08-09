.. _ref_user_guide_launch:

Launching Ansys Fluent Locally
==============================
Fluent can be started from Python in gRPC mode using
:func:`launch_fluent() <ansys.fluent.core.launcher.launcher.launch_fluent>`.
This starts Fluent in the background and sends commands to that service.

.. code:: python

    import ansys.fluent.core as pyfluent
    solver_session = pyfluent.launch_fluent()

Launcher Options
----------------

Solver Mode
~~~~~~~~~~~
The following examples demonstrate how you can start Fluent in solution mode:

.. code:: python

   solver_session_a = pyfluent.launch_fluent()

   solver_session_b = pyfluent.launch_fluent(meshing_mode=False)

Meshing Mode
~~~~~~~~~~~~
The following example demonstrates how you can start Fluent in meshing mode:

.. code:: python

   meshing_session = pyfluent.launch_fluent(meshing_mode=True)

Precision
~~~~~~~~~
The following example demonstrates how you can select double precision in solution mode:

.. code:: python

   solver_session = pyfluent.launch_fluent(precision='double')

Dimension
~~~~~~~~~
The following example demonstrates how you can select double precision and 2D in solution mode:

.. code:: python

   solver_session = pyfluent.launch_fluent(precision='double', version='2d')

Number of Processors
~~~~~~~~~~~~~~~~~~~~
The following example demonstrates how you can select the number of processors:

.. code:: python

   solver_session = pyfluent.launch_fluent(precision='double', version='2d', processor_count=2)

API Reference
-------------
For more details on controlling how Ansys Fluent launches locally, see the
function description for :func:`launch_fluent() <ansys.fluent.core.launcher.launcher.launch_fluent>`.