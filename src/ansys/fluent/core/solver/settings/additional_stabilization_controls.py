#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .blended_compressive_scheme import blended_compressive_scheme
from .pseudo_transient_stabilization import pseudo_transient_stabilization


class additional_stabilization_controls(Group):
    """'additional_stabilization_controls' child."""

    fluent_name = "additional-stabilization-controls"

    child_names = [
        "blended_compressive_scheme",
        "pseudo_transient_stabilization",
    ]

    blended_compressive_scheme: blended_compressive_scheme = (
        blended_compressive_scheme
    )
    """
    blended_compressive_scheme child of additional_stabilization_controls
    """
    pseudo_transient_stabilization: pseudo_transient_stabilization = (
        pseudo_transient_stabilization
    )
    """
    pseudo_transient_stabilization child of additional_stabilization_controls
    """
