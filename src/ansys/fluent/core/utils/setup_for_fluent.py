from ansys.fluent.core.launcher.launcher import launch_fluent
from ansys.fluent.core.session_solver import Solver


def setup_for_fluent(*args, **kwargs):
    """Returns global PyConsole objects."""

    session = launch_fluent(*args, **kwargs)
    globals = {}
    if "mode" in kwargs.keys() and kwargs["mode"] == "meshing":
        globals["meshing"] = session.meshing
        globals["PartManagement"] = session.PartManagement
        globals["PMFileManagement"] = session.PMFileManagement
        globals["solver"] = Solver(fluent_connection=session.fluent_connection)
    elif "mode" in kwargs.keys() and kwargs["mode"] == "solver":
        globals["solver"] = session
        globals["solverworkflow"] = session.solverworkflow

    globals["preferences"] = session.preferences
    globals["workflow"] = session.workflow

    return globals
