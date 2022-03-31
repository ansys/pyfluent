#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .enable import enable
from .options_2 import options


class high_order_term_relaxation(Group):
    """'high_order_term_relaxation' child."""

    fluent_name = "high-order-term-relaxation"

    child_names = ["enable", "options"]

    enable: enable = enable
    """
    enable child of high_order_term_relaxation
    """
    options: options = options
    """
    options child of high_order_term_relaxation
    """
