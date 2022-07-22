.. _ref_user_guide_launch:

Launching Fluent locally
========================
You can use the :func:`launch_fluent() <ansys.fluent.core.launcher.launcher.launch_fluent>`
method to start Fluent from Python in gRPC mode. The following code starts Fluent in the
background and sends commands to this service.

.. code:: python

    import ansys.fluent.core as pyfluent
    solver_session = pyfluent.launch_fluent()

Launcher options
----------------
The following examples show different ways that you can launch Fluent locally.
For more information, see the description for the :func:`launch_fluent() <ansys.fluent.core.launcher.launcher.launch_fluent>`
method.

Solver mode
~~~~~~~~~~~
This example shows how you can start Fluent in solution mode:

.. code:: python

   solver_session_a = pyfluent.launch_fluent()

   solver_session_b = pyfluent.launch_fluent(meshing_mode=False)

Meshing mode
~~~~~~~~~~~~
This example shows how you can start Fluent in meshing mode:

.. code:: python

   meshing_session = pyfluent.launch_fluent(meshing_mode=True)

Precision
~~~~~~~~~
This example shows how you can select double precision in solution mode:

.. code:: python

   solver_session = pyfluent.launch_fluent(precision='double')

Dimension
~~~~~~~~~
This example shows how you can select double precision and 2D in solution mode:

.. code:: python

   solver_session = pyfluent.launch_fluent(precision='double', version='2d')

Number of processors
~~~~~~~~~~~~~~~~~~~~
This example shows how you can also select the number of processors:

.. code:: python

   solver_session = pyfluent.launch_fluent(precision='double', version='2d', processor_count=2)

