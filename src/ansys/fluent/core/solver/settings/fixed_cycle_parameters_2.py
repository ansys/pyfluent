#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .pre_sweeps_2 import pre_sweeps
from .post_sweeps_2 import post_sweeps
class fixed_cycle_parameters(Group):
    """
    'fixed_cycle_parameters' child.
    """

    fluent_name = "fixed-cycle-parameters"

    child_names = \
        ['pre_sweeps', 'post_sweeps']

    pre_sweeps: pre_sweeps = pre_sweeps
    """
    pre_sweeps child of fixed_cycle_parameters
    """
    post_sweeps: post_sweeps = post_sweeps
    """
    post_sweeps child of fixed_cycle_parameters
    """
