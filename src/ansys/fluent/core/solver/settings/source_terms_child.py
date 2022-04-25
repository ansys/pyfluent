#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .child_object_type_child import child_object_type_child


class source_terms_child(ListObject[child_object_type_child]):
    """'child_object_type' of source_terms."""

    fluent_name = "child-object-type"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of source_terms_child.
    """
