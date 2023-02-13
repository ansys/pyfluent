from ansys.fluent.core.launcher.launcher import launch_fluent
from ansys.fluent.core.session_solver import Solver


def setup_for_fluent(*args, **kwargs):
    """Returns global PyConsole objects."""
    session = launch_fluent(*args, **kwargs)
    globals = {}
    if kwargs.get("mode", "solver") == "meshing":
        globals["meshing"] = session
        globals["PartManagement"] = session.PartManagement
        globals["PMFileManagement"] = session.PMFileManagement
        globals["solver"] = Solver(fluent_connection=session.fluent_connection)
    else:
        globals["solver"] = session
        globals["solverworkflow"] = session.solverworkflow

    globals["preferences"] = session.preferences
    globals["workflow"] = session.workflow

    return globals
