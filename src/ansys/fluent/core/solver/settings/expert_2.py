#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .numerics import numerics
from .numerics_dbns import numerics_dbns
from .reaction_source_term_relaxation_factor import (
    reaction_source_term_relaxation_factor,
)
from .reactions_1 import reactions


class expert(Group):
    """'expert' child."""

    fluent_name = "expert"

    child_names = [
        "reactions",
        "reaction_source_term_relaxation_factor",
        "numerics",
        "numerics_dbns",
    ]

    reactions: reactions = reactions
    """
    reactions child of expert
    """
    reaction_source_term_relaxation_factor: reaction_source_term_relaxation_factor = (
        reaction_source_term_relaxation_factor
    )
    """
    reaction_source_term_relaxation_factor child of expert
    """
    numerics: numerics = numerics
    """
    numerics child of expert
    """
    numerics_dbns: numerics_dbns = numerics_dbns
    """
    numerics_dbns child of expert
    """
