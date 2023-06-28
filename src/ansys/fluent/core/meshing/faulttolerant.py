from ansys.fluent.core.launcher.launcher import LaunchMode, launch_fluent

from .meshing_workflow import MeshingWorkflow


def fault_tolerant_workflow(**launch_args) -> MeshingWorkflow:
    # TODO share launch code with watertight
    dynamic_interface = True
    if "dynamic_interface" in launch_args:
        dynamic_interface = launch_args["dynamic_interface"]
        del launch_args["dynamic_interface"]
    args = dict(mode=LaunchMode.PURE_MESHING_MODE)
    args.update(launch_args)
    session = launch_fluent(**args)
    meshing_workflow = session.workflow
    meshing_workflow.fault_tolerant(dynamic_interface=dynamic_interface)
    return meshing_workflow
