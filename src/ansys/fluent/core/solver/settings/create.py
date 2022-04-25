#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .capture_simulation_report_data import capture_simulation_report_data
from .write_data import write_data


class create(Command):
    """Add new Design Point.

    Parameters
    ----------
        write_data : bool
            'write_data' child.
        capture_simulation_report_data : bool
            'capture_simulation_report_data' child.
    """

    fluent_name = "create"

    argument_names = ["write_data", "capture_simulation_report_data"]

    write_data: write_data = write_data
    """
    write_data argument of create
    """
    capture_simulation_report_data: capture_simulation_report_data = (
        capture_simulation_report_data
    )
    """
    capture_simulation_report_data argument of create
    """
