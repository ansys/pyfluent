#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .duplicate import duplicate
from .export_design_table import export_design_table
from .import_design_table import import_design_table
from .initialize import initialize
from .parametric_studies_child import parametric_studies_child
from .set_as_current import set_as_current
from .use_base_data import use_base_data


class parametric_studies(NamedObject[parametric_studies_child]):
    """'parametric_studies' child."""

    fluent_name = "parametric-studies"

    command_names = [
        "initialize",
        "duplicate",
        "set_as_current",
        "use_base_data",
        "export_design_table",
        "import_design_table",
    ]

    initialize: initialize = initialize
    """
    initialize command of parametric_studies
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of parametric_studies
    """
    set_as_current: set_as_current = set_as_current
    """
    set_as_current command of parametric_studies
    """
    use_base_data: use_base_data = use_base_data
    """
    use_base_data command of parametric_studies
    """
    export_design_table: export_design_table = export_design_table
    """
    export_design_table command of parametric_studies
    """
    import_design_table: import_design_table = import_design_table
    """
    import_design_table command of parametric_studies
    """
    child_object_type: parametric_studies_child = parametric_studies_child
    """
    child_object_type of parametric_studies.
    """
