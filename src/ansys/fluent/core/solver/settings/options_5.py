#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .oil_flow import oil_flow
from .reverse import reverse
from .node_values_1 import node_values
from .relative_1 import relative
class options(Group):
    """
    'options' child.
    """

    fluent_name = "options"

    child_names = \
        ['oil_flow', 'reverse', 'node_values', 'relative']

    oil_flow: oil_flow = oil_flow
    """
    oil_flow child of options
    """
    reverse: reverse = reverse
    """
    reverse child of options
    """
    node_values: node_values = node_values
    """
    node_values child of options
    """
    relative: relative = relative
    """
    relative child of options
    """
