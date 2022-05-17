#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .option import option
from .inside import inside
from .outside import outside
class options(Group):
    """
    'options' child.
    """

    fluent_name = "options"

    child_names = \
        ['option', 'inside', 'outside']

    option: option = option
    """
    option child of options
    """
    inside: inside = inside
    """
    inside child of options
    """
    outside: outside = outside
    """
    outside child of options
    """
