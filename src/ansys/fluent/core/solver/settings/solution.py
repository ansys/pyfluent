#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .controls import controls
from .initialization import initialization
from .methods_1 import methods
from .report_definitions import report_definitions
from .run_calculation import run_calculation


class solution(Group):
    """'solution' child."""

    fluent_name = "solution"

    child_names = [
        "controls",
        "methods",
        "report_definitions",
        "initialization",
        "run_calculation",
    ]

    controls: controls = controls
    """
    controls child of solution
    """
    methods: methods = methods
    """
    methods child of solution
    """
    report_definitions: report_definitions = report_definitions
    """
    report_definitions child of solution
    """
    initialization: initialization = initialization
    """
    initialization child of solution
    """
    run_calculation: run_calculation = run_calculation
    """
    run_calculation child of solution
    """
