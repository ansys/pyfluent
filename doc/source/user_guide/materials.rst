Define materials
==================
PyFluent allows you to use :ref:`ref_settings` to interact with materials settings.

Copy material from database
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Python code**

.. code:: python

    solver.setup.materials.fluid.make_a_copy(from_="water",to="water-2")
    solver.setup.cell_zone_conditions.fluid["elbow-fluid"].material = "water-2"

Create new material
~~~~~~~~~~~~~~~~~~~

**Python code**

.. code:: python

    mysolid = solver.setup.materials.solid.create("mysolid")
    mysolid.chemical_formula = "SiO2"
    mysolid.density.value = 2650
    mysolid.specific_heat.value = 1887
    mysolid.thermal_conductivity.value = 7.6

.. code:: python

    myfluid = solver.setup.materials.fluid.create("myfluid")
    myfluid.chemical_formula = "H2O"
    myfluid.density.value = 1000
    myfluid.specific_heat.value = 4186
    myfluid.thermal_conductivity.value = 0.6
    myfluid.viscosity.value = 1.03e-3