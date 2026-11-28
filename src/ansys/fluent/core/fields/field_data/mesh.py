# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Public mesh models returned by :meth:`FieldData.get_mesh`."""

import dataclasses
from enum import Enum

__all__ = (
    "CellElementType",
    "Element",
    "Facet",
    "Mesh",
    "Node",
    "ZoneInfo",
    "ZoneType",
)


class ZoneType(Enum):
    """Enumeration of zone types that classify mesh zones in the Fluent solver."""

    CELL = 1
    FACE = 2


@dataclasses.dataclass
class ZoneInfo:
    """Metadata describing a mesh zone in the Fluent solver.

    Attributes
    ----------
    _id : int
        Integer zone ID assigned by the Fluent solver.
    name : str
        Name of the zone as defined in the Fluent case.
    zone_type : ZoneType
        Whether the zone is a cell zone or a face zone.
    """

    _id: int
    name: str
    zone_type: ZoneType


@dataclasses.dataclass
class Node:
    """A single mesh node with its spatial coordinates.

    Attributes
    ----------
    _id : int
        Integer node ID assigned by the Fluent solver.
    x : float
        X-coordinate of the node in the solver's length unit.
    y : float
        Y-coordinate of the node in the solver's length unit.
    z : float
        Z-coordinate of the node in the solver's length unit.
    """

    _id: int
    x: float
    y: float
    z: float


class CellElementType(Enum):
    """Enumeration of cell element topologies supported by the Fluent mesh.

    Each member corresponds to a standard finite-volume cell shape. The number of
    nodes and faces for each type is noted in the member comments.
    """

    # 3 nodes, 3 faces
    TRIANGLE = 1
    # 4 nodes, 4 faces
    TETRAHEDRON = 2
    # 4 nodes, 4 faces
    QUADRILATERAL = 3
    # 8 nodes, 6 faces
    HEXAHEDRON = 4
    # 5 nodes, 5 faces
    PYRAMID = 5
    # 6 nodes, 5 faces
    WEDGE = 6
    # Arbitrary number of nodes and faces
    POLYHEDRON = 7
    # 2 nodes, 1 face (only in 2D)
    GHOST = 8
    # 10 nodes, 4 faces
    QUADRATIC_TETRAHEDRON = 9
    # 20 nodes, 6 faces
    QUADRATIC_HEXAHEDRON = 10
    # 13 nodes, 5 faces
    QUADRATIC_PYRAMID = 11
    # 15 nodes, 5 faces
    QUADRATIC_WEDGE = 12


@dataclasses.dataclass
class Facet:
    """A face of a polyhedral mesh element, defined by its node indices.

    Used only for :attr:`CellElementType.POLYHEDRON` elements; standard
    element types store connectivity directly on :class:`Element` via
    ``node_indices``.

    Attributes
    ----------
    node_indices : list[int]
        Zero-based indices into the :attr:`Mesh.nodes` array for the nodes
        that form this facet.
    """

    node_indices: list[int]


@dataclasses.dataclass
class Element:
    """A single mesh cell containing topology and connectivity information.

    For standard element types (e.g. hexahedron, tetrahedron), connectivity is
    stored in ``node_indices``. For polyhedral elements, connectivity is stored
    as a list of :class:`Facet` objects in ``facets``.

    Attributes
    ----------
    _id : int
        Integer element ID assigned by the Fluent solver.
    element_type : CellElementType
        Shape of the element; see :class:`CellElementType`.
    node_indices : list[int]
        Zero-based indices into :attr:`Mesh.nodes` for standard elements.
        Empty for polyhedral elements.
    facets : list[Facet]
        Faces of the element for :attr:`CellElementType.POLYHEDRON` elements.
        Empty for standard elements.
    """

    _id: int
    element_type: CellElementType
    node_indices: list[int] = dataclasses.field(default_factory=list)
    facets: list[Facet] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class Mesh:
    """Computational mesh for a Fluent zone, containing nodes and elements.

    Returned by :meth:`LiveFieldData.get_mesh`. The ``nodes`` array provides
    spatial coordinates indexed from 0, and the ``elements`` array stores
    connectivity referencing those node indices.

    Attributes
    ----------
    nodes : list[Node]
        Ordered list of :class:`Node` objects; element connectivity uses
        zero-based indices into this list.
    elements : list[Element]
        List of :class:`Element` objects describing cell topology and
        connectivity.
    """

    nodes: list[Node]
    elements: list[Element]
