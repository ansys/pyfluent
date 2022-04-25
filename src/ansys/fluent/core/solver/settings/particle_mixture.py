#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .mixture_child import mixture_child


class particle_mixture(NamedObject[mixture_child]):
    """'particle_mixture' child."""

    fluent_name = "particle-mixture"

    child_object_type: mixture_child = mixture_child
    """
    child_object_type of particle_mixture.
    """
