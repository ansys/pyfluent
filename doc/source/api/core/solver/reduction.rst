.. _ref_reduction:

Reduction
=========

You can use reduction functions on Fluent data from one
or across multiple remote Fluent sessions.

Accessing reduction functions
-----------------------------

In order to access reduction functions, import it and launch the fluent solver.
Then, make boundary conditions data, etc. available (for example, by reading case files):

.. code-block:: python

  >>> from ansys.fluent.core.solver.function import reduction
  >>> import ansys.fluent.core as pyfluent
  >>> from ansys.fluent.core.examples import download_file
  >>> solver = pyfluent.launch_fluent(mode="solver")
  >>> case_path = download_file("Static_Mixer_main.cas.h5", "pyfluent/static_mixer")
  >>> solver.file.read(file_type="case", file_name=mixing_elbow_case_path)


Simple usage
------------

You can use the reduction functions from pyfluent simply by initializing the solution
and accessing the select functions with the required parameters.

For example, in the below case, we do hybrid initialization of the solution and perform
an area-average of absolute pressure over the velocity inlets.

.. code-block:: python

  >>> solver.solution.initialization.hybrid_initialize()
  >>> reduction.area_average(
  >>>   expr="AbsolutePressure",
  >>>   locations=solver.setup.boundary_conditions.velocity_inlet,
  >>> )

Similarly one can use the other functions available currently with pyfluent.

Usage of context
----------------

You can also use the context argument available with all the reduction functions
to mention the context instead of listing down the entire path of the locations,
and the path to the location is identified automatically.

For example, to calculate area of a location one has to do:

.. code-block:: python

  >>> solver.solution.initialization.hybrid_initialize()
  >>> assert reduction.area(
  >>>   locations=[solver.setup.boundary_conditions.velocity_inlet["inlet1"]],
  >>> )

Instead, one can use the context argument:

.. code-block:: python

  >>> reduction.area(locations=["inlet1"], ctxt=solver)


Current Capabilities
--------------------
At present, pyfluent allows the usage of the following reduction functions:

Area
~~~~
Compute the total area of the specified locations.

.. code-block:: python

  >>> reduction.area(locations)

Area Average
~~~~~~~~~~~~
Compute the area averaged value of the specified expression over the specified locations.

.. code-block:: python

  >>> reduction.area_average(expression, locations)

Area Integrated Average
~~~~~~~~~~~~~~~~~~~~~~~
Compute the area integrated averaged of the specified expression over the specified locations.

.. code-block:: python

  >>> reduction.area_integrated_average(expression, locations)

Volume
~~~~~~
Compute the total volume of the specified locations.

.. code-block:: python

  >>> reduction.volume(locations)

Volume Average
~~~~~~~~~~~~~~
Compute the volume averaged value of the specified expression over the specified locations.

.. code-block:: python

  >>> reduction.volume_average(expression, locations)

Volume Integrated Average
~~~~~~~~~~~~~~~~~~~~~~~~~
Compute the volume integrated averaged of the specified expression over the specified locations.

.. code-block:: python

  >>> reduction.volume_integrated_average(expression, locations)

Centroid
~~~~~~~~
Compute the geometric centroid of the specified location(s) as a vector.

.. code-block:: python

  >>> reduction.centroid(locations)

Count
~~~~~
Compute the total number of cells included in the specified locations.

.. code-block:: python

  >>> reduction.count(locations)

Minimum
~~~~~~~
Compute the minimum of the specified expression over the specified locations.

.. code-block:: python

  >>> reduction.minimum(expression, locations)

Maximum
~~~~~~~
Compute the maximum of the specified expression over the specified locations.

.. code-block:: python

  >>> reduction.maximum(expression, locations)

Mass Average
~~~~~~~~~~~~
Compute the mass-weighted average value of the specified expression over the specified locations.

.. code-block:: python

  >>> reduction.mass_average(expression, locations)

Mass Integrated Average
~~~~~~~~~~~~~~~~~~~~~~~
Compute the total mass-weighted value of the specified expression overthe specified locations.

.. code-block:: python

  >>> reduction.mass_integrated_average(expression, locations)

Mass Flow
~~~~~~~~~
Compute the total mass flow rate of the specified locations.

.. code-block:: python

  >>> reduction.mass_flow(locations)

Mass Flow Average
~~~~~~~~~~~~~~~~~
Compute the mass-flow-weighted average value of the specified expression over the specified locations.

.. code-block:: python

  >>> reduction.mass_flow_average(expression, locations)

Mass Flow Integrated Average
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Compute the total mass-flow-weighted value of the specified expression over the specified locations.

.. code-block:: python

  >>> reduction.mass_flow_integrated_average(expression, locations)


Example Use Cases
-----------------
You can either calculate the area of one inlet or the combine area of all
the velocity inlets with the below examples:

.. code-block:: python

  >>> area_inlet_1 = reduction.area(
  >>>   locations=[solver.setup.boundary_conditions.velocity_inlet["inlet1"]],
  >>> )

  >>> area_inlet = reduction.area(
  >>>   locations=[solver.setup.boundary_conditions.velocity_inlet],
  >>> )

You can calculate the area average of "Absolute Pressure" over the entire set of velocity
inlets as shown:

.. code-block:: python

  >>> reduction.area_average(
  >>>   expr="AbsolutePressure",
  >>>   locations=solver.setup.boundary_conditions.velocity_inlet,
  >>> )

You can calculate the area integrated average of "Absolute Pressure" over the velocity inlet 1
as shown:

.. code-block:: python

  >>> reduction.area_integrated_average(
  >>>   expr="AbsolutePressure",
  >>>   locations=[solver1.setup.boundary_conditions.velocity_inlet["inlet1"]],
  >>> )


You can calculate the geometric centroid of the velocity inlet 2 as shown:

.. code-block:: python

  >>> reduction.centroid(
  >>>   locations=[solver.setup.boundary_conditions.velocity_inlet["inlet2"]]
  >>> )


