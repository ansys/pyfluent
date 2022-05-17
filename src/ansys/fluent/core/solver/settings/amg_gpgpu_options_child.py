#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .enable_gpu import enable_gpu
from .term_criterion import term_criterion
from .solver_1 import solver
from .max_num_cycle import max_num_cycle
from .coarsen_by_size import coarsen_by_size
from .pre_sweep import pre_sweep
from .post_sweep import post_sweep
from .smoother import smoother
class amg_gpgpu_options_child(Group):
    """
    'child_object_type' of amg_gpgpu_options
    """

    fluent_name = "child-object-type"

    child_names = \
        ['enable_gpu', 'term_criterion', 'solver', 'max_num_cycle',
         'coarsen_by_size', 'pre_sweep', 'post_sweep', 'smoother']

    enable_gpu: enable_gpu = enable_gpu
    """
    enable_gpu child of amg_gpgpu_options_child
    """
    term_criterion: term_criterion = term_criterion
    """
    term_criterion child of amg_gpgpu_options_child
    """
    solver: solver = solver
    """
    solver child of amg_gpgpu_options_child
    """
    max_num_cycle: max_num_cycle = max_num_cycle
    """
    max_num_cycle child of amg_gpgpu_options_child
    """
    coarsen_by_size: coarsen_by_size = coarsen_by_size
    """
    coarsen_by_size child of amg_gpgpu_options_child
    """
    pre_sweep: pre_sweep = pre_sweep
    """
    pre_sweep child of amg_gpgpu_options_child
    """
    post_sweep: post_sweep = post_sweep
    """
    post_sweep child of amg_gpgpu_options_child
    """
    smoother: smoother = smoother
    """
    smoother child of amg_gpgpu_options_child
    """
