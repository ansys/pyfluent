#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .mean_and_std_deviation import mean_and_std_deviation
from .pb_disc_components import pb_disc_components
class pb_disc(Group):
    """
    'pb_disc' child.
    """

    fluent_name = "pb-disc"

    child_names = \
        ['mean_and_std_deviation', 'pb_disc_components']

    mean_and_std_deviation: mean_and_std_deviation = mean_and_std_deviation
    """
    mean_and_std_deviation child of pb_disc
    """
    pb_disc_components: pb_disc_components = pb_disc_components
    """
    pb_disc_components child of pb_disc
    """
