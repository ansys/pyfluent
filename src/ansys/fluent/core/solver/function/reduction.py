# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
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

"""Module providing reductions functions that can be applied to Fluent data from one or
across multiple remote Fluent sessions.

The following parameters are relevant for the reduction functions. The
expr parameter is not relevant to all reductions functions.

Parameters
----------
expression : Any
    Expression that can be either a string or an
    instance of a specific settings API named_expressions
    object. The expression can be a field variable or a
    a valid Fluent expression. A specified named expression
    can be handled for multiple solvers as long as the
    expression's definition is valid in each solver (it
    does not need to be created in each solver)
locations : Any
    A list of location strings, or an API object that can be
    resolved to a list of location strings
    (for example, setup.boundary_conditions,
    or results.surfaces.plane_surface),
    or a list of such objects. If location strings are
    included in the list, then only string must be included
ctxt : Any, optional
    An optional API object (for example, the root solver session
    object but any solver API object will suffice) to set
    the context of the call's execution. If the location
    objects are strings, then such a context is required

Returns
-------
float or List[float]
    The result of the reduction

Examples
--------

>>> from ansys.fluent.core.solver.function import reduction
>>> # Compute the area average of absolute pressure across all boundary
>>> # condition surfaces of the given solver
>>> reduction.area_average(
...     expr = "AbsolutePressure",
...     locations = solver.setup.boundary_conditions.velocity_inlet
... )
10623.0

>>> from ansys.fluent.core.solver.function import reduction
>>> # Compute the minimum of the square of velocity magnitude
>>> # for all pressure outlets across two solvers
>>> named_exprs = solver1.setup.named_expressions
>>> vsquared = named_exprs["vsquared"] = {}
>>> vsquared.definition = "VelocityMagnitude ** 2"
>>> reduction.minimum(
...     expr = vsquared,
...     locations = solver1.setup.boundary_conditions.pressure_outlet
...     + solver2.setup.boundary_conditions.pressure_outlet
...     )
19.28151
"""
from collections.abc import Iterable
from enum import Enum

import numpy as np
from numpy import array

from ansys.fluent.core.exceptions import DisallowedValuesError
from ansys.fluent.core.variable_strategies import (
    FluentExprNamingStrategy as naming_strategy,
)


class Weight(Enum):
    """Weight for sum."""

    AREA = "Area"
    VOLUME = "Volume"
    MASS = "Mass"
    MASS_FLOW_RATE = "MassFlowRate"
    ABS_MASS_FLOW_RATE = "AbsMassFlowRate"

    def __str__(self):
        return self.value


class BadReductionRequest(Exception):
    """Raised on an attempt to make a bad reduction request."""

    def __init__(self, err):
        """__init__ method of BadReductionRequest class."""
        super().__init__(f"Could not complete reduction function request: {err}")


def _is_iterable(obj):
    return hasattr(type(obj), "__iter__")


def _expand_locn_container(locns):
    try:
        return [[locn, locns] for locn in locns]
    except TypeError as ex:
        raise BadReductionRequest(ex)


def _locn_name_and_obj(locn, locns):
    if isinstance(locn, str):
        return [locn, locns]
    # should call locn_get_name()
    if _is_iterable(locn):
        return _locn_names_and_objs(locn)
    else:
        return [locn.obj_name, locn]


def _locn_names_and_objs(locns):
    if _is_iterable(locns):
        names_and_objs = []
        if locns.__class__.__name__ == "CombinedNamedObject":
            return locns.items()

        for locn in locns:
            if isinstance(locn, Iterable) and not isinstance(locn, (str, bytes)):
                raise DisallowedValuesError("location", locn, list(locn))
            name_and_obj = _locn_name_and_obj(locn, locns)
            if _is_iterable(name_and_obj):
                if isinstance(name_and_obj[0], str):
                    names_and_objs.append(name_and_obj)
                else:
                    names_and_objs.extend(name_and_obj)
        return names_and_objs
    else:
        return _expand_locn_container(locns)


def _root(obj):
    return (
        None
        if isinstance(obj, list)
        else obj if not getattr(obj, "obj_name", None) else _root(obj._parent)
    )


def _validate_locn_list(locn_list, ctxt):
    if not all(locn[0] for locn in locn_list) and (
        any(locn[0] for locn in locn_list) or not ctxt
    ):
        raise BadReductionRequest("Invalid combination of arguments")


def _locns(locns, ctxt):
    if locns == []:
        # Raising 'RuntimeError' instead of 'ValueError' to address a limitation in the server-side implementation.
        raise RuntimeError("No locations specified.")
    locn_names_and_objs = _locn_names_and_objs(locns)
    locn_list = []
    for name, obj in locn_names_and_objs:
        root = _root(obj)
        found = False
        for locn in locn_list:
            if locn[0] is root:
                locn[1].append(name)
                found = True
                break
        if not found:
            locn_list.append([root, [name]])
    _validate_locn_list(locn_list, ctxt)
    return locn_list


def _eval_expr(solver, expr_str):
    named_exprs = solver.setup.named_expressions
    expr_name = "temp_expr_1"
    named_exprs[expr_name] = {}
    # request feature: anonymous name object creation
    expr_obj = named_exprs["temp_expr_1"]
    expr_obj.definition = expr_str
    val = expr_obj.get_value()
    named_exprs.pop(expr_name)
    return val


def _expr_to_expr_str(expr):
    return getattr(expr, "definition", expr) if expr is not None else expr


def _eval_reduction(
    solver, reduction, locations, expr=None, weight=None, condition=None
):
    if weight:
        weight = "Weight=" + str(weight)
        locations = str(locations) + ", " + weight

    expr_str = _expr_to_expr_str(naming_strategy().to_string(expr))
    if condition:
        expr_str = expr_str + ", " + condition
    return _eval_expr(
        solver,
        (
            f"{reduction}({locations})"
            if expr_str is None
            else f"{reduction}({expr_str},{locations})"
        ),
    )


def _extent_expression(
    f_string, extent_name, expr, locations, ctxt, weight=None, condition=None
):
    locns = _locns(locations, ctxt)
    numerator = 0.0
    denominator = 0.0
    for solver, names in locns:
        solver = solver or _root(ctxt)
        val = _eval_reduction(
            solver, f_string, names, expr, weight=weight, condition=condition
        )
        extent = (
            _eval_reduction(
                solver, extent_name, names, weight=weight, condition=condition
            )
            if len(locns) > 1
            else 1
        )
        try:
            numerator += val * extent
            denominator += extent
        except TypeError:
            if isinstance(val, list):
                numerator += np.multiply(val, extent)
                denominator += extent
            else:
                raise RuntimeError(val)
    if denominator == 0.0:
        raise BadReductionRequest("Zero extent computed for average")
    return numerator / denominator


def _extent_moment_vector(f_string, expr, locations, ctxt):
    locns = _locns(locations, ctxt)
    total = array([0.0, 0.0, 0.0])
    for solver, names in locns:
        solver = solver or _root(ctxt)
        extent = _eval_reduction(solver, f_string, names, expr)
        try:
            total += array(extent)
        except TypeError:
            raise RuntimeError(extent)
    return tuple(total)


def _extent_average(extent_name, expr, locations, ctxt):
    return _extent_expression(f"{extent_name}Ave", extent_name, expr, locations, ctxt)


def _extent_integrated_average(extent_name, expr, locations, ctxt):
    return _extent_expression(f"{extent_name}Int", extent_name, expr, locations, ctxt)


def _extent(extent_name, locations, ctxt):
    locns = _locns(locations, ctxt)
    total = 0.0
    for solver, names in locns:
        solver = solver or _root(ctxt)
        extent = _eval_expr(solver, f"{extent_name}({names})")
        try:
            total += extent
        except TypeError:
            raise RuntimeError(extent)
    return total


def _extent_vectors(extent_name, locations, ctxt):
    locns = _locns(locations, ctxt)
    total = array([0.0, 0.0, 0.0])
    for solver, names in locns:
        solver = solver or _root(ctxt)
        extent = _eval_expr(solver, f"{extent_name}({names})")
        try:
            total += array(extent)
        except TypeError:
            raise RuntimeError(extent)
    return tuple(total)


def _limit(limit, expr, locations, ctxt):
    locns = _locns(locations, ctxt)
    limit_val = None
    for solver, names in locns:
        solver = solver or _root(ctxt)
        val = _eval_reduction(
            solver, "Minimum" if limit is min else "Maximum", names, expr
        )
        limit_val = val if limit_val is None else limit(val, limit_val)
    return limit_val


# Weight for sum
weight = Weight


def area_average(expression, locations, ctxt=None):
    """Compute the area averaged value of the specified expression over the specified
    locations.

    Parameters
    ----------
    expression : Any
    locations : Any
    ctxt : Any, optional
    Returns
    -------
    float
    """
    return _extent_average("Area", expression, locations, ctxt)


def area_integral(expression, locations, ctxt=None):
    """Compute the area integrated averaged of the specified expression over the
    specified locations.

    Parameters
    ----------
    expression : Any
    locations : Any
    ctxt : Any, optional
    Returns
    -------
    float
    """
    return _extent_integrated_average("Area", expression, locations, ctxt)


def volume_average(expression, locations, ctxt=None):
    """Compute the volume-weighted average value of the specified expression over the
    specified locations.

    Parameters
    ----------
    expression : Any
    locations : Any
    ctxt : Any, optional
    Returns
    -------
    float
    """
    return _extent_average("Volume", expression, locations, ctxt)


def volume_integral(expression, locations, ctxt=None):
    """Compute the volume-weighted total of the specified expression over the specified
    locations.

    Parameters
    ----------
    expression : Any
    locations : Any
    ctxt : Any, optional
    Returns
    -------
    float
    """
    return _extent_integrated_average("Volume", expression, locations, ctxt)


def area(locations, ctxt=None):
    """Compute the total area of the specified locations.

    Parameters
    ----------
    locations : Any
    ctxt : Any, optional
    Returns
    -------
    float
    """
    return _extent("Area", locations, ctxt)


def volume(locations, ctxt=None):
    """Compute the total volume of the specified locations.

    Parameters
    ----------
    locations : Any
    ctxt : Any, optional
    Returns
    -------
    float
    """
    return _extent("Volume", locations, ctxt)


def count(locations, ctxt=None):
    """Compute the total number of cells included in the specified locations.

    Parameters
    ----------
    locations : Any
    ctxt : Any, optional
    Returns
    -------
    float
    """
    return _extent("Count", locations, ctxt)


def centroid(locations, ctxt=None):
    """Compute the geometric centroid of the specified location(s) as a vector.

    Parameters
    ----------
    locations : Any
    ctxt : Any, optional
    Returns
    -------
    tuple
    """
    return _extent_vectors("Centroid", locations, ctxt)


def force(locations, ctxt=None):
    """Compute the force acting on the location(s) specified (should be walls) as a
    vector.

    Parameters
    ----------
    locations : Any
    ctxt : Any, optional
    Returns
    -------
    tuple
    """
    return _extent_vectors("Force", locations, ctxt)


def pressure_force(locations, ctxt=None):
    """Compute the pressure force acting on the location(s) specified (should be walls)
    as a vector.

    Parameters
    ----------
    locations : Any
    ctxt : Any, optional
    Returns
    -------
    tuple
    """
    return _extent_vectors("PressureForce", locations, ctxt)


def viscous_force(locations, ctxt=None):
    """Compute the viscous force acting on the location(s) specified (should be walls)
    as a vector.

    Parameters
    ----------
    locations : Any
    ctxt : Any, optional
    Returns
    -------
    tuple
    """
    return _extent_vectors("ViscousForce", locations, ctxt)


def moment(expression, locations, ctxt=None):
    """Compute  the moment vector about the specified point (which can be single-valued
    expression) for the specified location(s).

    Parameters
    ----------
    expression : Any
    locations : Any
    ctxt : Any, optional
    Returns
    -------
    tuple
    """
    return _extent_moment_vector("Moment", expression, locations, ctxt)


def minimum(expression, locations, ctxt=None):
    """Compute the minimum of the specified expression over the specified locations.

    Parameters
    ----------
    expression : Any
    locations : Any
    ctxt : Any, optional
    Returns
    -------
    float
    """
    return _limit(min, expression, locations, ctxt)


def maximum(expression, locations, ctxt=None):
    """Compute the maximum of the specified expression over the specified locations.

    Parameters
    ----------
    expression : Any
    locations : Any
    ctxt : Any, optional
    Returns
    -------
    float
    """
    return _limit(max, expression, locations, ctxt)


def mass_average(expression, locations, ctxt=None):
    """Compute the mass-weighted average value of the specified expression over the
    specified locations.

    Parameters
    ----------
    expression : Any
    locations : Any
    ctxt : Any, optional
    Returns
    -------
    float
    """
    return _extent_average("Mass", expression, locations, ctxt)


def mass_integral(expression, locations, ctxt=None):
    """Compute the total mass-weighted value of the specified expression over the
    specified locations.

    Parameters
    ----------
    expression : Any
    locations : Any
    ctxt : Any, optional
    Returns
    -------
    float
    """
    return _extent_integrated_average("Mass", expression, locations, ctxt)


def mass_flow_average(expression, locations, ctxt=None):
    """Compute the mass-flow-weighted average value of the specified expression over the
    specified locations.

    Parameters
    ----------
    expression : Any
    locations : Any
    ctxt : Any, optional
    Returns
    -------
    float
    """
    return _extent_average("MassFlow", expression, locations, ctxt)


def mass_flow_integral(expression, locations, ctxt=None):
    """Compute the total mass flow over the specified locations.

    Parameters
    ----------
    expression : Any
    locations : Any
    ctxt : Any, optional
    Returns
    -------
    float
    """
    return _extent_integrated_average("MassFlow", expression, locations, ctxt)


def mass_flow(locations, ctxt=None):
    """Compute the total mass flow rate of the specified locations.

    Parameters
    ----------
    locations : Any
    ctxt : Any, optional
    Returns
    -------
    float
    """
    return _extent("MassFlow", locations, ctxt)


def sum(expression, locations, weight: str | Weight, ctxt=None):
    """Compute the sum of the specified expression over the specified locations.

    Parameters
    ----------
    expression : Any
    locations : Any
    weight: str | Weight
    ctxt : Any, optional
    Returns
    -------
    float
    """
    return _extent_expression("Sum", "Sum", expression, locations, ctxt, weight=weight)


def sum_if(expression, condition, locations, weight: str | Weight, ctxt=None):
    """Compute the sum of the specified expression over the specified locations if a
    condition is satisfied.

    Parameters
    ----------
    expression : Any
    condition: str
    locations : Any
    weight: str | Weight
    ctxt : Any, optional
    Returns
    -------
    float
    """
    return _extent_expression(
        "SumIf",
        "SumIf",
        expression,
        locations,
        ctxt,
        weight=weight,
        condition=condition,
    )
