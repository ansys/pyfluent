#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .dbns_cases import dbns_cases
from .pbns_cases import pbns_cases
class flux_type(Group):
    """
    'flux_type' child.
    """

    fluent_name = "flux-type"

    child_names = \
        ['dbns_cases', 'pbns_cases']

    dbns_cases: dbns_cases = dbns_cases
    """
    dbns_cases child of flux_type
    """
    pbns_cases: pbns_cases = pbns_cases
    """
    pbns_cases child of flux_type
    """
