"""This module contains the code generation logic for Fluent's Python API."""

from enum import Enum, auto


class StaticInfoType(Enum):
    """An enumeration over the different types of static info that can be fetched from
    Fluent."""

    TUI_SOLVER = auto()
    TUI_MESHING = auto()
    DATAMODEL_WORKFLOW = auto()
    DATAMODEL_MESHING = auto()
    DATAMODEL_PART_MANAGEMENT = auto()
    DATAMODEL_PM_FILE_MANAGEMENT = auto()
    DATAMODEL_FLICING = auto()
    DATAMODEL_PREFERENCES = auto()
    DATAMODEL_SOLVER_WORKFLOW = auto()
    DATAMODEL_MESHING_UTILITIES = auto()
    SETTINGS = auto()
