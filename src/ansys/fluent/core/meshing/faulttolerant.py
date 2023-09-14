"""Fault-tolerant workflow module."""

from ansys.fluent.core.launcher.launcher import FluentMode, launch_fluent

from .meshing_workflow import MeshingWorkflow


def fault_tolerant_workflow(**launch_args) -> MeshingWorkflow:
    """A meshing workflow wrapper, initialized as fault-tolerant.

    Parameters
    ----------
    launch_args
        Additional arguments forwarded to the launch_fluent function.

    Returns
    -------
    MeshingWorkflow
        A meshing workflow wrapper
    """
    # TODO share launch code with watertight
    dynamic_interface = True
    if "dynamic_interface" in launch_args:
        dynamic_interface = launch_args["dynamic_interface"]
        del launch_args["dynamic_interface"]
    if "session" in launch_args:
        session = launch_args["session"]
    else:
        args = dict(mode=FluentMode.PURE_MESHING_MODE)
        args.update(launch_args)
        session = launch_fluent(**args)
    meshing_workflow = session.workflow
    meshing_workflow.fault_tolerant(dynamic_interface=dynamic_interface)
    return meshing_workflow
