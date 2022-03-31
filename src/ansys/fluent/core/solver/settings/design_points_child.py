#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .capture_simulation_report_data_1 import capture_simulation_report_data
from .input_parameters import input_parameters
from .output_parameters import output_parameters
from .write_data_1 import write_data


class design_points_child(Group):
    """'child_object_type' of design_points."""

    fluent_name = "child-object-type"

    child_names = [
        "input_parameters",
        "output_parameters",
        "write_data",
        "capture_simulation_report_data",
    ]

    input_parameters: input_parameters = input_parameters
    """
    input_parameters child of design_points_child
    """
    output_parameters: output_parameters = output_parameters
    """
    output_parameters child of design_points_child
    """
    write_data: write_data = write_data
    """
    write_data child of design_points_child
    """
    capture_simulation_report_data: capture_simulation_report_data = (
        capture_simulation_report_data
    )
    """
    capture_simulation_report_data child of design_points_child
    """
