.. _field_data_vs_solution_variable_data:

Choosing Between Field Data and Solution Variable Data APIs
===========================================================

Overview
--------

PyFluent provides two primary APIs for accessing field array data from Fluent:

- **Field Data API** (``field_data``):
  Surface-centric access to a wide range of CFD fields, mesh geometry, and pathlines.

- **Solution Variable Data API** (``solution_variable_data``):
  Zone-centric access to Fluent's core solution variable arrays (SVARs), with support for both reading and writing.

This guide summarizes the scope, strengths, and intended use cases for each API, and provides guidance on how to choose the appropriate interface for your workflow.

Field Data API (``field_data``)
-------------------------------

- **Scope**:
  - Accesses field data on surfaces (boundaries, face zones, etc.).
  - Supports scalar, vector, and pathlines data, as well as mesh geometry and connectivity.
  - Designed for post-processing, visualization, and mesh extraction.
- **Typical Use Cases**:
  - Extracting pressure, velocity, temperature, or other fields on boundaries or surfaces.
  - Accessing mesh geometry for visualization or export.
  - Streaming field data for real-time updates (in meshing mode).
- **Limitations**:
  - Read-only access.
  - Data is organized by surface, not by zone.
  - Not all solver variables are available; some fields are derived or post-processed.

Solution Variable Data API (``solution_variable_data``)
-------------------------------------------------------

- **Scope**:
  - Accesses Fluent's internal solution variable arrays (SVARs) on zones (cell or face zones).
  - Supports both reading and writing of SVAR data.
  - Provides detailed metadata about zones and variables.
- **Typical Use Cases**:
  - Direct extraction or modification of solver arrays for advanced workflows.
  - Custom initialization or manipulation of solution fields.
  - Accessing zone-specific data for scripting or automation.
- **Limitations**:
  - Data is organized by zone, not by surface.
  - Does not provide mesh geometry or general field/derived data.
  - Requires knowledge of Fluent's SVAR naming conventions.

How to Choose
-------------

Use the following table to help decide which API to use for your context:

+--------------------------+---------------------+-----------------------------+
| **Requirement**          | **field_data**      | **solution_variable_data**  |
+==========================+=====================+=============================+
| Data on a surface        | Yes                 | No                          |
+--------------------------+---------------------+-----------------------------+
| Data on a zone           | No                  | Yes                         |
+--------------------------+---------------------+-----------------------------+
| Mesh geometry/connectivity| Yes                | No                          |
+--------------------------+---------------------+-----------------------------+
| Pathlines                | Yes                 | No                          |
+--------------------------+---------------------+-----------------------------+
| Read/write access        | Read-only           | Read and write              |
+--------------------------+---------------------+-----------------------------+
| Derived/post-processed fields | Yes            | No (SVARs only)             |
+--------------------------+---------------------+-----------------------------+
| Direct solver arrays     | No                  | Yes                         |
+--------------------------+---------------------+-----------------------------+
| Available in meshing mode | Yes                 | No                         |
+--------------------------+---------------------+-----------------------------+

**General Guidance:**

- Use **field_data** for post-processing, visualization, and mesh-related queries on surfaces.
- Use **solution_variable_data** for direct access to solver variables on zones, especially when you need to modify data or work with SVARs.

Examples
--------

**Extracting pressure on a surface:**

.. code-block:: python

    from ansys.fluent.core import ScalarFieldDataRequest
    data = solver_session.fields.field_data.get_field_data(
        ScalarFieldDataRequest(field_name="pressure", surfaces=["inlet"])
    )

**Extracting and modifying temperature in a cell zone:**

.. code-block:: python

    sv_t = solver_session.fields.solution_variable_data.get_data(
        variable_name="SV_T", zone_names=["fluid"], domain_name="mixture"
    )
    temp_array = sv_t["fluid"]
    temp_array[:] = 600  # Set all temperatures to 600
    solver_session.fields.solution_variable_data.set_data(
        variable_name="SV_T", zone_names_to_data={"fluid": temp_array}, domain_name="mixture"
    )

Further Reading
---------------

- :ref:`ref_field_data_guide`
- :ref:`ref_solution_variable_data_guide`
