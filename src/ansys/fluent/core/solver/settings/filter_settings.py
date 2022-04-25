#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .enabled_2 import enabled
from .field import field
from .filter_maximum import filter_maximum
from .filter_minimum import filter_minimum
from .options_7 import options


class filter_settings(Group):
    """'filter_settings' child."""

    fluent_name = "filter-settings"

    child_names = [
        "field",
        "options",
        "enabled",
        "filter_minimum",
        "filter_maximum",
    ]

    field: field = field
    """
    field child of filter_settings
    """
    options: options = options
    """
    options child of filter_settings
    """
    enabled: enabled = enabled
    """
    enabled child of filter_settings
    """
    filter_minimum: filter_minimum = filter_minimum
    """
    filter_minimum child of filter_settings
    """
    filter_maximum: filter_maximum = filter_maximum
    """
    filter_maximum child of filter_settings
    """
