#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .option import option
from .all import all
from .feature import feature
from .outline import outline
class edge_type(Group):
    """
    'edge_type' child.
    """

    fluent_name = "edge-type"

    child_names = \
        ['option', 'all', 'feature', 'outline']

    option: option = option
    """
    option child of edge_type
    """
    all: all = all
    """
    all child of edge_type
    """
    feature: feature = feature
    """
    feature child of edge_type
    """
    outline: outline = outline
    """
    outline child of edge_type
    """
