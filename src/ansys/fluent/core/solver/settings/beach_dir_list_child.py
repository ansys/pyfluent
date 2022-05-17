#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .ni import ni
from .nj import nj
from .nk import nk
from .xe import xe
from .len import len
class beach_dir_list_child(Group):
    """
    'child_object_type' of beach_dir_list
    """

    fluent_name = "child-object-type"

    child_names = \
        ['ni', 'nj', 'nk', 'xe', 'len']

    ni: ni = ni
    """
    ni child of beach_dir_list_child
    """
    nj: nj = nj
    """
    nj child of beach_dir_list_child
    """
    nk: nk = nk
    """
    nk child of beach_dir_list_child
    """
    xe: xe = xe
    """
    xe child of beach_dir_list_child
    """
    len: len = len
    """
    len child of beach_dir_list_child
    """
