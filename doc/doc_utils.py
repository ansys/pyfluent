"""Shared utilities for PyFluent RST doc generators."""

# Bridge content strings appended to section index RST files to provide
# a brief human-readable description below the toctree.

# Bridge content for the meshing section.
meshing_bridge_content = """
The meshing workflow provides task-based guided workflows for surface and volume meshing.

The generated meshing workflow API exposes Fluent's underlying workflow objects
through a verbose, path-dependent hierarchy. This is useful when direct access
to the complete Fluent object model is required, but navigating those paths can
make common workflows difficult to discover and use.

The :class:`~ansys.fluent.core.meshing.meshing_workflow.MeshingWorkflow` classes
wrap that generated API with simpler, documented usability classes. They provide
an object-oriented interface for common meshing operations while retaining access
to the generated workflow when more detailed control is needed. See
:ref:`ref_meshing_workflow_new` for the underlying generated API and task hierarchy.

The :ref:`meshing utilities <ref_meshing_datamodel_meshing_utilities>` provide
direct operations for querying and modifying mesh entities, zones, labels, and
quality-related data."""

# Bridge content for the legacy section.
legacy_bridge_content = """
Legacy APIs provide backward-compatible access to earlier interface versions."""

# Bridge content for the solver workflows section.
solver_workflows_bridge_content = """
Solver workflows provide task-based guided workflows for setting up and running solver simulations."""
