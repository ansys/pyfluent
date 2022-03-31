#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .choice import choice
from .columns import columns
from .ecad_name import ecad_name
from .pwr_names import pwr_names
from .ref_frame import ref_frame
from .rows import rows


class pcb_zone_info(Group):
    """'pcb_zone_info' child."""

    fluent_name = "pcb-zone-info"

    child_names = [
        "ecad_name",
        "choice",
        "rows",
        "columns",
        "ref_frame",
        "pwr_names",
    ]

    ecad_name: ecad_name = ecad_name
    """
    ecad_name child of pcb_zone_info
    """
    choice: choice = choice
    """
    choice child of pcb_zone_info
    """
    rows: rows = rows
    """
    rows child of pcb_zone_info
    """
    columns: columns = columns
    """
    columns child of pcb_zone_info
    """
    ref_frame: ref_frame = ref_frame
    """
    ref_frame child of pcb_zone_info
    """
    pwr_names: pwr_names = pwr_names
    """
    pwr_names child of pcb_zone_info
    """
