#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .udf_cf_names import udf_cf_names


class setup_unsteady_statistics(Command):
    """'setup_unsteady_statistics' command.

    Parameters
    ----------
        udf_cf_names : typing.List[str]
            'udf_cf_names' child.
    """

    fluent_name = "setup-unsteady-statistics"

    argument_names = ["udf_cf_names"]

    udf_cf_names: udf_cf_names = udf_cf_names
    """
    udf_cf_names argument of setup_unsteady_statistics
    """
