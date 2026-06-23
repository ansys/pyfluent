"""Shared utilities for PyFluent RST doc generators."""

# Bridge content strings appended to section index RST files to provide
# a brief human-readable description below the toctree.

# Bridge content for the meshing workflow section.
meshing_workflow_bridge_content = """
The meshing workflow provides task-based guided workflows for surface and volume meshing."""

# Bridge content for the legacy section.
legacy_bridge_content = """
Legacy APIs provide backward-compatible access to earlier interface versions."""

# Bridge content for the solver workflows section.
solver_workflows_bridge_content = """
Solver workflows provide task-based guided workflows for setting up and running solver simulations."""


def get_display_name(node_name: str, display_name_overrides: dict | None = None) -> str:
    """Return display name for a node with fallback formatting.

    If an overrides dict is provided and the node name is found in it, the
    override is returned. Otherwise, underscores are replaced with spaces and
    only the first character is capitalized.

    Parameters
    ----------
    node_name : str
        Raw node or file name.
    display_name_overrides : dict, optional
        Mapping of node names to their display name overrides.

    Returns
    -------
    str
        Formatted display name.
    """
    if display_name_overrides and node_name in display_name_overrides:
        return display_name_overrides[node_name]
    fallback = node_name.replace("_", " ")
    if not fallback:
        return fallback
    return fallback[0].upper() + fallback[1:]
