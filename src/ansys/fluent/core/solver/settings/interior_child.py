#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .phase_8 import phase
from .is_not_a_rans_les_interface import is_not_a_rans_les_interface
class interior_child(Group):
    """
    'child_object_type' of interior
    """

    fluent_name = "child-object-type"

    child_names = \
        ['phase', 'is_not_a_rans_les_interface']

    phase: phase = phase
    """
    phase child of interior_child
    """
    is_not_a_rans_les_interface: is_not_a_rans_les_interface = is_not_a_rans_les_interface
    """
    is_not_a_rans_les_interface child of interior_child
    """
