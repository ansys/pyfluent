#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .courant_number_reduction import courant_number_reduction
from .correction_reduction import correction_reduction
from .correction_smoothing import correction_smoothing
from .species_correction_reduction import species_correction_reduction
class relaxation_factor(Group):
    """
    'relaxation_factor' child.
    """

    fluent_name = "relaxation-factor"

    child_names = \
        ['courant_number_reduction', 'correction_reduction',
         'correction_smoothing', 'species_correction_reduction']

    courant_number_reduction: courant_number_reduction = courant_number_reduction
    """
    courant_number_reduction child of relaxation_factor
    """
    correction_reduction: correction_reduction = correction_reduction
    """
    correction_reduction child of relaxation_factor
    """
    correction_smoothing: correction_smoothing = correction_smoothing
    """
    correction_smoothing child of relaxation_factor
    """
    species_correction_reduction: species_correction_reduction = species_correction_reduction
    """
    species_correction_reduction child of relaxation_factor
    """
