#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .data_sampling import data_sampling
from .sampling_interval import sampling_interval
from .statistics_shear_stress import statistics_shear_stress
from .statistics_heat_flux import statistics_heat_flux
from .wall_statistics import wall_statistics
from .force_statistics import force_statistics
from .time_statistics_dpm import time_statistics_dpm
from .species_list import species_list
from .statistics_mixture_fraction import statistics_mixture_fraction
from .statistics_reaction_progress import statistics_reaction_progress
from .save_cff_unsteady_statistics import save_cff_unsteady_statistics
from .setup_unsteady_statistics import setup_unsteady_statistics
class data_sampling(Group):
    """
    'data_sampling' child.
    """

    fluent_name = "data-sampling"

    child_names = \
        ['data_sampling', 'sampling_interval', 'statistics_shear_stress',
         'statistics_heat_flux', 'wall_statistics', 'force_statistics',
         'time_statistics_dpm', 'species_list', 'statistics_mixture_fraction',
         'statistics_reaction_progress', 'save_cff_unsteady_statistics']

    data_sampling: data_sampling = data_sampling
    """
    data_sampling child of data_sampling
    """
    sampling_interval: sampling_interval = sampling_interval
    """
    sampling_interval child of data_sampling
    """
    statistics_shear_stress: statistics_shear_stress = statistics_shear_stress
    """
    statistics_shear_stress child of data_sampling
    """
    statistics_heat_flux: statistics_heat_flux = statistics_heat_flux
    """
    statistics_heat_flux child of data_sampling
    """
    wall_statistics: wall_statistics = wall_statistics
    """
    wall_statistics child of data_sampling
    """
    force_statistics: force_statistics = force_statistics
    """
    force_statistics child of data_sampling
    """
    time_statistics_dpm: time_statistics_dpm = time_statistics_dpm
    """
    time_statistics_dpm child of data_sampling
    """
    species_list: species_list = species_list
    """
    species_list child of data_sampling
    """
    statistics_mixture_fraction: statistics_mixture_fraction = statistics_mixture_fraction
    """
    statistics_mixture_fraction child of data_sampling
    """
    statistics_reaction_progress: statistics_reaction_progress = statistics_reaction_progress
    """
    statistics_reaction_progress child of data_sampling
    """
    save_cff_unsteady_statistics: save_cff_unsteady_statistics = save_cff_unsteady_statistics
    """
    save_cff_unsteady_statistics child of data_sampling
    """
    command_names = \
        ['setup_unsteady_statistics']

    setup_unsteady_statistics: setup_unsteady_statistics = setup_unsteady_statistics
    """
    setup_unsteady_statistics command of data_sampling
    """
