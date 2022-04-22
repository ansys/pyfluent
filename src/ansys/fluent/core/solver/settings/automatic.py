#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .id import id
from .normal import normal
from .option import option
from .partition import partition
from .type_2 import type


class automatic(Group):
    """'automatic' child."""

    fluent_name = "automatic"

    child_names = ["option", "type", "id", "normal", "partition"]

    option: option = option
    """
    option child of automatic
    """
    type: type = type
    """
    type child of automatic
    """
    id: id = id
    """
    id child of automatic
    """
    normal: normal = normal
    """
    normal child of automatic
    """
    partition: partition = partition
    """
    partition child of automatic
    """
