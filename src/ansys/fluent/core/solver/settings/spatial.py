#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .first_to_second_order_blending import first_to_second_order_blending
from .first_to_second_order_blending_list import first_to_second_order_blending_list
from .scheme import scheme
from .flow_skew_diffusion_exclude import flow_skew_diffusion_exclude
from .scalars_skew_diffusion_exclude import scalars_skew_diffusion_exclude
from .rhie_chow_flux_specify import rhie_chow_flux_specify
from .rhie_chow_method import rhie_chow_method
class spatial(Group):
    """
    'spatial' child.
    """

    fluent_name = "spatial"

    child_names = \
        ['first_to_second_order_blending',
         'first_to_second_order_blending_list', 'scheme',
         'flow_skew_diffusion_exclude', 'scalars_skew_diffusion_exclude',
         'rhie_chow_flux_specify', 'rhie_chow_method']

    first_to_second_order_blending: first_to_second_order_blending = first_to_second_order_blending
    """
    first_to_second_order_blending child of spatial
    """
    first_to_second_order_blending_list: first_to_second_order_blending_list = first_to_second_order_blending_list
    """
    first_to_second_order_blending_list child of spatial
    """
    scheme: scheme = scheme
    """
    scheme child of spatial
    """
    flow_skew_diffusion_exclude: flow_skew_diffusion_exclude = flow_skew_diffusion_exclude
    """
    flow_skew_diffusion_exclude child of spatial
    """
    scalars_skew_diffusion_exclude: scalars_skew_diffusion_exclude = scalars_skew_diffusion_exclude
    """
    scalars_skew_diffusion_exclude child of spatial
    """
    rhie_chow_flux_specify: rhie_chow_flux_specify = rhie_chow_flux_specify
    """
    rhie_chow_flux_specify child of spatial
    """
    rhie_chow_method: rhie_chow_method = rhie_chow_method
    """
    rhie_chow_method child of spatial
    """
