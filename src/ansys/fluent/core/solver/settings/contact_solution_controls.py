#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .amg import amg
from .methods import methods
from .miscellaneous import miscellaneous
from .models_2 import models
from .parameters import parameters
from .set_settings_to_default import set_settings_to_default
from .solution_stabilization import solution_stabilization
from .spatial import spatial
from .transient import transient
from .verbosity_1 import verbosity


class contact_solution_controls(Group):
    """'contact_solution_controls' child."""

    fluent_name = "contact-solution-controls"

    child_names = [
        "solution_stabilization",
        "verbosity",
        "parameters",
        "spatial",
        "transient",
        "amg",
        "models",
        "methods",
        "miscellaneous",
    ]

    solution_stabilization: solution_stabilization = solution_stabilization
    """
    solution_stabilization child of contact_solution_controls
    """
    verbosity: verbosity = verbosity
    """
    verbosity child of contact_solution_controls
    """
    parameters: parameters = parameters
    """
    parameters child of contact_solution_controls
    """
    spatial: spatial = spatial
    """
    spatial child of contact_solution_controls
    """
    transient: transient = transient
    """
    transient child of contact_solution_controls
    """
    amg: amg = amg
    """
    amg child of contact_solution_controls
    """
    models: models = models
    """
    models child of contact_solution_controls
    """
    methods: methods = methods
    """
    methods child of contact_solution_controls
    """
    miscellaneous: miscellaneous = miscellaneous
    """
    miscellaneous child of contact_solution_controls
    """
    command_names = ["set_settings_to_default"]

    set_settings_to_default: set_settings_to_default = set_settings_to_default
    """
    set_settings_to_default command of contact_solution_controls
    """
