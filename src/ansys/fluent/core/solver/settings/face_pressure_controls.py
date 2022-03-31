#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .face_pressure_options import face_pressure_options


class face_pressure_controls(Group):
    """'face_pressure_controls' child."""

    fluent_name = "face-pressure-controls"

    child_names = ["face_pressure_options"]

    face_pressure_options: face_pressure_options = face_pressure_options
    """
    face_pressure_options child of face_pressure_controls
    """
