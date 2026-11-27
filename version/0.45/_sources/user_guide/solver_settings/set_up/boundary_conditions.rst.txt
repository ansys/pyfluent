Boundary conditions and cell zone conditions
============================================
The examples in this section show how you use :ref:`ref_root` objects to set up
boundary conditions and cell zone conditions.

Boundary conditions
~~~~~~~~~~~~~~~~~~~

.. code:: python

    >>> from ansys.fluent.core import Solver, examples
    >>> from ansys.fluent.core.solver import VelocityInlet
    >>> file_name = examples.download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    >>> solver_session = Solver.from_install()
    >>> solver_session.settings.file.read_case(file_name=file_name)
    >>> cold_inlet = VelocityInlet(settings_source=solver_session, name="cold-inlet")
    >>> cold_inlet.momentum.velocity.set_state(0.4)
    >>> inlet_turbulence = cold_inlet.turbulence
    >>> turbulence_specification = inlet_turbulence.turbulence_specification
    >>> turbulence_specification.allowed_values()
    ['K and Omega', 'Intensity and Length Scale', 'Intensity and Viscosity Ratio', 'Intensity and Hydraulic Diameter']
    >>> turbulence_specification.set_state("Intensity and Hydraulic Diameter")
    >>> turbulent_intensity = inlet_turbulence.turbulent_intensity
    >>> turbulent_intensity.min(), turbulent_intensity.max()
    (0, 1)
    >>> turbulent_intensity.set_state(0.5)
    >>> inlet_turbulence.hydraulic_diameter.set_state("4 [in]")
    >>> cold_inlet.thermal.temperature.set_state(293.15)


Cell zone conditions
~~~~~~~~~~~~~~~~~~~~

.. code:: python

    >>> from ansys.fluent.core.solver import FluidCellZone
    >>> elbow_fluid = FluidCellZone(settings_source=solver_session, name="elbow-fluid")
    >>> elbow_fluid.laminar.set_state(True)
