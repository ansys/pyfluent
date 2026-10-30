.. _user_guide_variables:

===============================
Working with physical variables
===============================

PyFluent integrates with the PyAnsys-units library, which provides a shared catalog of variable objects based on physical quantities like temperature, pressure, and velocity. These variable objects, or VariableDescriptors, can be used throughout PyFluent to reference fields and quantities in a clear, consistent, and reliable way.

Instead of relying on raw strings like ``"temperature"`` or ``"SV_T"``, which may vary between Fluent interfaces or be hard to interpret, you can use named descriptors from the catalog. This improves code readability, reduces the chance of errors, and makes it easier to work across different APIs.

The same catalog is designed to work not just with PyFluent, but also with other PyAnsys libraries, offering a unified and expressive way to interact with physical quantities across products.

Overview
--------

The key benefits of using the ``VariableCatalog`` include:

- Code that is portable across Ansys products and more resistant to typos
- Simplified refactoring when field names change in Fluent or across versions
- Integrated dimensional consistency (via ``ansys-units``)
- Autocompletion and discoverability of supported quantities

Accessing field data
---------------------

Here’s how to use ``VariableCatalog`` to read and reduce field data using unit-aware quantity references:

.. code-block:: python

    from ansys.fluent.core import launch_fluent, examples
    from ansys.units.variable_descriptor import VariableCatalog

    solver_session = launch_fluent()
    case_path = examples.download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    solver_session.file.read(file_type="case", file_name=case_path)

    solver_session.settings.solution.initialization.hybrid_initialize()

    temperature = VariableCatalog.TEMPERATURE
    locations = ["hot-inlet"]

    # Access scalar field data
    temp_data = solver_session.fields.field_data.get_scalar_field_data(
        field_name=temperature, surfaces=locations
    )
    print(temp_data[locations[0]][0])  # value at hot-inlet

    # Compute minimum of a physical quantity
    temp_min = solver_session.fields.reduction.minimum(expression=temperature, locations=locations)
    print(temp_min)

    # Access solution variable data
    sol_data = solver_session.fields.solution_variable_data.get_data(
        variable_name=temperature, zone_names=locations
    )
    print(sol_data[locations[0]][0])

Using variables with report definitions
---------------------------------------

You can also use physical quantities in report definitions to improve clarity and maintainability:

.. code-block:: python

    surface_report = solver_session.settings.solution.report_definitions.surface["avg_temp"]
    surface_report.report_type = "surface-areaavg"
    surface_report.field = temperature  # Note: using VariableCatalog, not a string
    surface_report.surface_names = locations

    result = solver_session.solution.report_definitions.compute(report_defs=["avg_temp"])
    print(result[0]["avg_temp"][0])

Notes
-----

- All quantities used via ``VariableCatalog`` map to their correct Fluent field identifiers internally.
- These objects can be validated against their expected dimensional types.
- ``VariableCatalog`` is part of ``ansys-units``, which is automatically installed with PyFluent.
