#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .viscous_heating import viscous_heating
from .low_pressure_slip import low_pressure_slip
from .curvature_correction import curvature_correction
from .corner_flow_correction import corner_flow_correction
from .production_kato_launder import production_kato_launder
from .production_limiter import production_limiter
class options(Group):
    """
    'options' child.
    """

    fluent_name = "options"

    child_names = \
        ['viscous_heating', 'low_pressure_slip', 'curvature_correction',
         'corner_flow_correction', 'production_kato_launder',
         'production_limiter']

    viscous_heating: viscous_heating = viscous_heating
    """
    viscous_heating child of options
    """
    low_pressure_slip: low_pressure_slip = low_pressure_slip
    """
    low_pressure_slip child of options
    """
    curvature_correction: curvature_correction = curvature_correction
    """
    curvature_correction child of options
    """
    corner_flow_correction: corner_flow_correction = corner_flow_correction
    """
    corner_flow_correction child of options
    """
    production_kato_launder: production_kato_launder = production_kato_launder
    """
    production_kato_launder child of options
    """
    production_limiter: production_limiter = production_limiter
    """
    production_limiter child of options
    """
