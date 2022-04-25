#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .display import display
from .mesh_child_1 import mesh_child


class mesh(NamedObject[mesh_child]):
    """'mesh' child."""

    fluent_name = "mesh"

    command_names = ["display"]

    display: display = display
    """
    display command of mesh
    """
    child_object_type: mesh_child = mesh_child
    """
    child_object_type of mesh.
    """
