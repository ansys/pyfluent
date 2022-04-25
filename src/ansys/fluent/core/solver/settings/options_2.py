#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .relaxation_factor_2 import relaxation_factor
from .relaxation_options import relaxation_options
from .select_variables import select_variables


class options(Group):
    """'options' child."""

    fluent_name = "options"

    child_names = [
        "relaxation_factor",
        "select_variables",
        "relaxation_options",
    ]

    relaxation_factor: relaxation_factor = relaxation_factor
    """
    relaxation_factor child of options
    """
    select_variables: select_variables = select_variables
    """
    select_variables child of options
    """
    relaxation_options: relaxation_options = relaxation_options
    """
    relaxation_options child of options
    """
