.. _ref_reduction_guide:

Reduction
=========
 
You can use reduction functions on Fluent data from one or across multiple remote Fluent sessions. PyFluent provides both **functional** and **object-oriented** approaches to applying reduction functions. While both are supported, the **functional approach** is emphasized for its flexibility, particularly when working with multiple solver sessions.

Introduction to Reduction Functions
-----------------------------------

Reduction functions compute aggregate values over specified data locations, such as areas or volumes. These functions include operations like computing averages, integrals, and sums.

### Why the Functional Approach?

The **functional approach** is preferred for its:
1. **Conciseness**: Avoids deeply nested paths in code.
2. **Flexibility**: Supports reductions over multiple solver sessions or complex data sources.

For example:

.. code-block:: python

  >>> from ansys.fluent.core.solver.function import reduction
>>> # Compute the minimum of absolute pressure across multiple solvers
>>> reduction.minimum(
  ...     expr="AbsolutePressure",
  ...     locations=[
  ...         solver1.setup.boundary_conditions.velocity_inlet,
  ...         solver2.setup.boundary_conditions.velocity_inlet,
  ...     ]
  ... )
  10123.5

### Comparison with Object-Oriented Usage

The **object-oriented approach** leverages solver instance attributes like `solver.fields.reduction` to perform reductions. While this approach is intuitive for single-solver scenarios, it may be less suited to multi-solver or functional-style workflows.

---

Functional Usage
----------------

Reduction functions can be accessed directly via the `reduction` module. Here's how to set up a simple example:

.. code-block:: python

  >>> from ansys.fluent.core.solver.function import reduction
>>> from ansys.fluent.core.examples import download_file
>>> solver = pyfluent.launch_fluent(mode=pyfluent.FluentMode.SOLVER)
>>> case_path = download_file("Static_Mixer_main.cas.h5", "pyfluent/static_mixer")
>>> solver.settings.file.read(file_type="case", file_name=case_path)
>>> reduction.area_average(
  ...     expr="AbsolutePressure",
  ...     locations=solver.setup.boundary_conditions.velocity_inlet
  ... )
  101325.0

This method also supports boundary abstractions for concise location definitions:

.. code-block:: python

  >>> from ansys.fluent.core import PressureOutlets
>>> reduction.minimum(
  ...     expr="AbsolutePressure",
  ...     locations=[
  ...         PressureOutlets(settings_source=solver1),
  ...         PressureOutlets(settings_source=solver2),
  ...     ]
  ... )
  12345.6

---

Object-Oriented Usage
---------------------

To use reduction functions within a specific solver instance, initialize the solver and access the functions via `solver.fields.reduction`:

.. code-block:: python

  >>> solver.fields.reduction.area_average(
  ...     expression="AbsolutePressure",
  ...     locations=solver.settings.setup.boundary_conditions.velocity_inlet,
  ... )
  101325.0

For convenience, context-aware reductions are also supported:

.. code-block:: python

  >>> solver.fields.reduction.area(
  ...     locations=["inlet1"],
  ...     ctxt=solver,
  ... )
  7.565427133371293e-07

---

Reduction Functions: Capabilities
----------------------------------

The following reduction functions are available in PyFluent:

- **Area**: Compute the total area.
- **Area Average**: Compute the area-averaged value of an expression.
- **Area Integral**: Compute the integrated area of an expression.
- **Volume**: Compute the total volume.
- **Volume Average**: Compute the volume-averaged value of an expression.
- **Volume Integral**: Compute the integrated volume of an expression.
- **Centroid**: Compute the geometric centroid.
- **Force**: Compute the force vector on specified walls.
- **Minimum**: Compute the minimum value of an expression.
- **Maximum**: Compute the maximum value of an expression.
- **Sum**: Compute the sum of an expression over locations.
- **Sum If**: Compute the conditional sum of an expression.

Each function supports both the functional and object-oriented formats. See the following examples for typical use cases.

---

Examples
--------

### Example: Area Average

Functional:

.. code-block:: python

  >>> reduction.area_average(
  ...     expr="AbsolutePressure",
  ...     locations=solver.setup.boundary_conditions.velocity_inlet,
  ... )
  101325.0

Object-Oriented:

.. code-block:: python

  >>> solver.fields.reduction.area_average(
  ...     expression="AbsolutePressure",
  ...     locations=solver.settings.setup.boundary_conditions.velocity_inlet,
  ... )
  101325.0

---

### Example: Minimum Across Multiple Solvers

.. code-block:: python

  >>> reduction.minimum(
  ...     expr="AbsolutePressure",
  ...     locations=[
  ...         solver1.setup.boundary_conditions.pressure_outlet,
  ...         solver2.setup.boundary_conditions.pressure_outlet,
  ...     ],
  ... )
  10000.0

---

### Example: Using Boundary Abstractions

.. code-block:: python

  >>> from ansys.fluent.core import VelocityInlets
>>> reduction.sum(
  ...     expr="AbsolutePressure",
  ...     locations=[
  ...         VelocityInlets(settings_source=solver1),
  ...         VelocityInlets(settings_source=solver2),
  ...     ],
  ...     weight="Area"
  ... )
  20670300.0

---

**Note**: Boundary abstractions such as `PressureOutlets` and `VelocityInlets` simplify workflows by removing the need to specify complex paths.

---

This revised version ensures comprehensive coverage of all examples while prioritizing the **functional format** for clarity and flexibility. Let me know if there are any other tweaks you'd like!