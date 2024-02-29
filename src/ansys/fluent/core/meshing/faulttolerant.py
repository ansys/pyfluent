"""Fault-tolerant workflow module."""

from ansys.fluent.core.launcher.launcher import launch_fluent
from ansys.fluent.core.launcher.launcher_utils import FluentMode

from .meshing_workflow import EnhancedMeshingWorkflow


def fault_tolerant_workflow(**launch_args) -> EnhancedMeshingWorkflow:
    """Meshing workflow wrapper, initialized as fault-tolerant.

    Parameters
    ----------
    launch_args
        Additional arguments forwarded to the launch_fluent function.

    Returns
    -------
    EnhancedMeshingWorkflow
        Meshing workflow wrapper.
    """
    # TODO share launch code with watertight
    if "dynamic_interface" in launch_args:
        del launch_args["dynamic_interface"]
    if "session" in launch_args:
        session = launch_args["session"]
    else:
        args = dict(mode=FluentMode.PURE_MESHING_MODE)
        args.update(launch_args)
        session = launch_fluent(**args)
    meshing_workflow = session.fault_tolerant()
    return meshing_workflow
