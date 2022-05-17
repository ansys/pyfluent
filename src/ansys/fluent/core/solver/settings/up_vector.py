#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .xyz import xyz
class up_vector(Command):
    """
    Set the camera up-vector.
    
    Parameters
    ----------
        xyz : typing.List[real]
            'xyz' child.
    
    """

    fluent_name = "up-vector"

    argument_names = \
        ['xyz']

    xyz: xyz = xyz
    """
    xyz argument of up_vector
    """
