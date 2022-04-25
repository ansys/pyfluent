#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .bounded import bounded
from .compute_from_view_plane import compute_from_view_plane
from .edges_2 import edges
from .methods_2 import methods
from .p0_1 import p0
from .p1 import p1
from .p2 import p2
from .point_normal import point_normal
from .point_vector import point_vector
from .sample_point import sample_point
from .surface_aligned_normal import surface_aligned_normal
from .x import x
from .y import y
from .z import z


class plane_surface_child(Group):
    """'child_object_type' of plane_surface."""

    fluent_name = "child-object-type"

    child_names = [
        "methods",
        "x",
        "y",
        "z",
        "point_vector",
        "point_normal",
        "compute_from_view_plane",
        "surface_aligned_normal",
        "p0",
        "p1",
        "p2",
        "bounded",
        "sample_point",
        "edges",
    ]

    methods: methods = methods
    """
    methods child of plane_surface_child
    """
    x: x = x
    """
    x child of plane_surface_child
    """
    y: y = y
    """
    y child of plane_surface_child
    """
    z: z = z
    """
    z child of plane_surface_child
    """
    point_vector: point_vector = point_vector
    """
    point_vector child of plane_surface_child
    """
    point_normal: point_normal = point_normal
    """
    point_normal child of plane_surface_child
    """
    compute_from_view_plane: compute_from_view_plane = compute_from_view_plane
    """
    compute_from_view_plane child of plane_surface_child
    """
    surface_aligned_normal: surface_aligned_normal = surface_aligned_normal
    """
    surface_aligned_normal child of plane_surface_child
    """
    p0: p0 = p0
    """
    p0 child of plane_surface_child
    """
    p1: p1 = p1
    """
    p1 child of plane_surface_child
    """
    p2: p2 = p2
    """
    p2 child of plane_surface_child
    """
    bounded: bounded = bounded
    """
    bounded child of plane_surface_child
    """
    sample_point: sample_point = sample_point
    """
    sample_point child of plane_surface_child
    """
    edges: edges = edges
    """
    edges child of plane_surface_child
    """
