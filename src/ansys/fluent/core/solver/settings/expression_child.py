#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .average_over import average_over
from .define import define
from .expr_value import expr_value
from .list_valid_report_names import list_valid_report_names
from .old_props import old_props


class expression_child(Group):
    """'child_object_type' of expression."""

    fluent_name = "child-object-type"

    child_names = [
        "list_valid_report_names",
        "define",
        "expr_value",
        "average_over",
        "old_props",
    ]

    list_valid_report_names: list_valid_report_names = list_valid_report_names
    """
    list_valid_report_names child of expression_child
    """
    define: define = define
    """
    define child of expression_child
    """
    expr_value: expr_value = expr_value
    """
    expr_value child of expression_child
    """
    average_over: average_over = average_over
    """
    average_over child of expression_child
    """
    old_props: old_props = old_props
    """
    old_props child of expression_child
    """
