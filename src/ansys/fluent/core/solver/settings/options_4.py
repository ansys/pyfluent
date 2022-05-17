#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .nodes import nodes
from .edges import edges
from .faces import faces
from .partitions import partitions
from .overset_2 import overset
from .gap import gap
class options(Group):
    """
    'options' child.
    """

    fluent_name = "options"

    child_names = \
        ['nodes', 'edges', 'faces', 'partitions', 'overset', 'gap']

    nodes: nodes = nodes
    """
    nodes child of options
    """
    edges: edges = edges
    """
    edges child of options
    """
    faces: faces = faces
    """
    faces child of options
    """
    partitions: partitions = partitions
    """
    partitions child of options
    """
    overset: overset = overset
    """
    overset child of options
    """
    gap: gap = gap
    """
    gap child of options
    """
