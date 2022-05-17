#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .create import create
from .duplicate_1 import duplicate
from .load_case_data import load_case_data
from .delete_design_points import delete_design_points
from .save_journals import save_journals
from .clear_generated_data import clear_generated_data
from .update_current import update_current
from .update_all import update_all
from .update_selected import update_selected
from .design_points_child import design_points_child

class design_points(NamedObject[design_points_child]):
    """
    'design_points' child.
    """

    fluent_name = "design-points"

    command_names = \
        ['create', 'duplicate', 'load_case_data', 'delete_design_points',
         'save_journals', 'clear_generated_data', 'update_current',
         'update_all', 'update_selected']

    create: create = create
    """
    create command of design_points
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of design_points
    """
    load_case_data: load_case_data = load_case_data
    """
    load_case_data command of design_points
    """
    delete_design_points: delete_design_points = delete_design_points
    """
    delete_design_points command of design_points
    """
    save_journals: save_journals = save_journals
    """
    save_journals command of design_points
    """
    clear_generated_data: clear_generated_data = clear_generated_data
    """
    clear_generated_data command of design_points
    """
    update_current: update_current = update_current
    """
    update_current command of design_points
    """
    update_all: update_all = update_all
    """
    update_all command of design_points
    """
    update_selected: update_selected = update_selected
    """
    update_selected command of design_points
    """
    child_object_type: design_points_child = design_points_child
    """
    child_object_type of design_points.
    """
