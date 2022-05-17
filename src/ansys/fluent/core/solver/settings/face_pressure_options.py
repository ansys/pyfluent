#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .pressure_corr_grad import pressure_corr_grad
from .face_pressure_calculation_method import face_pressure_calculation_method
from .exclude_transient_term_in_face_pressure_calc import exclude_transient_term_in_face_pressure_calc
class face_pressure_options(Group):
    """
    'face_pressure_options' child.
    """

    fluent_name = "face-pressure-options"

    child_names = \
        ['pressure_corr_grad', 'face_pressure_calculation_method',
         'exclude_transient_term_in_face_pressure_calc']

    pressure_corr_grad: pressure_corr_grad = pressure_corr_grad
    """
    pressure_corr_grad child of face_pressure_options
    """
    face_pressure_calculation_method: face_pressure_calculation_method = face_pressure_calculation_method
    """
    face_pressure_calculation_method child of face_pressure_options
    """
    exclude_transient_term_in_face_pressure_calc: exclude_transient_term_in_face_pressure_calc = exclude_transient_term_in_face_pressure_calc
    """
    exclude_transient_term_in_face_pressure_calc child of face_pressure_options
    """
