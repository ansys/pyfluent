"""Provides a module to get global PyConsole objects."""

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
        globals["solver"] = Solver(
            fluent_connection=session._fluent_connection,
            scheme_eval=session._fluent_connection._connection_interface.scheme_eval,
        )
    else:
        globals["solver"] = session

    globals["preferences"] = session.preferences
    globals["workflow"] = session.workflow

    return globals
