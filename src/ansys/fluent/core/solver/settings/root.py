#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .current_parametric_study import current_parametric_study
from .file import file
from .parametric_studies import parametric_studies
from .results import results
from .setup import setup
from .solution import solution


class root(Group):
    """'root' object."""

    fluent_name = ""

    child_names = [
        "file",
        "setup",
        "solution",
        "results",
        "parametric_studies",
        "current_parametric_study",
    ]

    file: file = file
    """
    file child of root
    """
    setup: setup = setup
    """
    setup child of root
    """
    solution: solution = solution
    """
    solution child of root
    """
    results: results = results
    """
    results child of root
    """
    parametric_studies: parametric_studies = parametric_studies
    """
    parametric_studies child of root
    """
    current_parametric_study: current_parametric_study = (
        current_parametric_study
    )
    """
    current_parametric_study child of root
    """
