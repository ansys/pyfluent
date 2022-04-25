#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .edges_1 import edges
from .faces_1 import faces
from .material_color import material_color
from .nodes_1 import nodes


class manual(Group):
    """'manual' child."""

    fluent_name = "manual"

    child_names = ["faces", "edges", "nodes", "material_color"]

    faces: faces = faces
    """
    faces child of manual
    """
    edges: edges = edges
    """
    edges child of manual
    """
    nodes: nodes = nodes
    """
    nodes child of manual
    """
    material_color: material_color = material_color
    """
    material_color child of manual
    """
