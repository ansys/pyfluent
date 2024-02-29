"""Fault-tolerant workflow module."""

from .meshing_workflow import EnhancedMeshingWorkflow


def fault_tolerant_workflow(**launch_args) -> EnhancedMeshingWorkflow:
    """Meshing workflow wrapper, initialized as fault-tolerant.

    Parameters
    ----------
    launch_args
        Additional arguments forwarded to the launch_fluent function.

    Returns
    -------
    FaultTolerantMeshingWorkflow
        Fault-tolerant meshing workflow wrapper.
    """
    fault_tolerant = EnhancedMeshingWorkflow.pyfluent_launch_code(
        is_ftm=True, **launch_args
    )
    return fault_tolerant
