#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .first_to_second_order_blending_dbns import (
    first_to_second_order_blending_dbns,
)


class numerics_dbns(Group):
    """'numerics_dbns' child."""

    fluent_name = "numerics-dbns"

    child_names = ["first_to_second_order_blending_dbns"]

    first_to_second_order_blending_dbns: first_to_second_order_blending_dbns = (
        first_to_second_order_blending_dbns
    )
    """
    first_to_second_order_blending_dbns child of numerics_dbns
    """
