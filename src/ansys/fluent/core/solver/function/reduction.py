"""Module providing reductions functions that can be applied to Fluent data
from one or across multiple remote Fluent sessions.

The following parameters are relevant for the reduction functions. The
expr parameter is not relevant to all reductions functions.

Parameters
----------
expr : Any
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
    (e.g., setup.boundary_conditions,
    or results.surfaces.plane_surface),
    or a list of such objects. If location strings are
    included in the list, then only string must be included
ctxt : Any, optional
    An optional API object (e.g., the root solver session
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
...     locations = [
...         solver1.setup.boundary_conditions.pressure_outlet,
...         solver2.setup.boundary_conditions.pressure_outlet
...     ])
19.28151
"""

from numpy import array


class BadReductionRequest(Exception):
    def __init__(self, err):
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
        for locn in locns:
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
        else obj
        if not getattr(obj, "obj_name", None)
        else _root(obj._parent)
    )


def _validate_locn_list(locn_list, ctxt):
    if not all(locn[0] for locn in locn_list) and (
        any(locn[0] for locn in locn_list) or not ctxt
    ):
        raise BadReductionRequest("Invalid combination of arguments")


def _locns(locns, ctxt):
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


def _eval_reduction(solver, reduction, locations, expr=None):
    expr_str = _expr_to_expr_str(expr)
    return _eval_expr(
        solver,
        (
            f"{reduction}({locations})"
            if expr_str is None
            else f"{reduction}({expr_str},{locations})"
        ),
    )


def _extent_expression(f_string, extent_name, expr, locations, ctxt):
    locns = _locns(locations, ctxt)
    numerator = 0.0
    denominator = 0.0
    for solver, names in locns:
        solver = solver or _root(ctxt)
        val = _eval_reduction(solver, f_string, names, expr)
        extent = _eval_reduction(solver, extent_name, names) if len(locns) > 1 else 1
        try:
            numerator += val * extent
            denominator += extent
        except TypeError:
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
    return total


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
    return total


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


def area_average(expr, locations, ctxt=None):
    """Compute the area averaged value of the specified expression over the
    specified locations.

    Parameters
    ----------
    expr : Any
    locations : Any
    ctxt : Any, optional
    Returns
    -------
    float
    """
    return _extent_average("Area", expr, locations, ctxt)


def area_integrated_average(expr, locations, ctxt=None):
    """Compute the area integrated averaged of the specified expression over
    the specified locations.

    Parameters
    ----------
    expr : Any
    locations : Any
    ctxt : Any, optional
    Returns
    -------
    float
    """
    return _extent_integrated_average("Area", expr, locations, ctxt)


def volume_average(expr, locations, ctxt=None):
    """Compute the volume-weighted average value of the specified expression
    over the specified locations.

    Parameters
    ----------
    expr : Any
    locations : Any
    ctxt : Any, optional
    Returns
    -------
    float
    """
    return _extent_average("Volume", expr, locations, ctxt)


def volume_integrated_average(expr, locations, ctxt=None):
    """Compute the volume-weighted total of the specified expression over the
    specified locations.

    Parameters
    ----------
    expr : Any
    locations : Any
    ctxt : Any, optional
    Returns
    -------
    float
    """
    return _extent_integrated_average("Volume", expr, locations, ctxt)


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
    float
    """
    return _extent_vectors("Centroid", locations, ctxt)


def force(locations, ctxt=None):
    """Compute the force acting on the location(s) specified (should be walls)
    as a vector.

    Parameters
    ----------
    locations : Any
    ctxt : Any, optional
    Returns
    -------
    float
    """
    return _extent_vectors("Force", locations, ctxt)


def pressure_force(locations, ctxt=None):
    """Compute the pressure force acting on the location(s) specified (should
    be walls) as a vector.

    Parameters
    ----------
    locations : Any
    ctxt : Any, optional
    Returns
    -------
    float
    """
    return _extent_vectors("PressureForce", locations, ctxt)


def viscous_force(locations, ctxt=None):
    """Compute the viscous force acting on the location(s) specified (should be
    walls) as a vector.

    Parameters
    ----------
    locations : Any
    ctxt : Any, optional
    Returns
    -------
    float
    """
    return _extent_vectors("ViscousForce", locations, ctxt)


def moment(expr, locations, ctxt=None):
    """Compute  the moment vector about the specified point (which can be
    single-valued expression) for the specified location(s).

    Parameters
    ----------
    expr : Any
    locations : Any
    ctxt : Any, optional
    Returns
    -------
    float
    """
    return _extent_moment_vector("Moment", expr, locations, ctxt)


def minimum(expr, locations, ctxt=None):
    """Compute the minimum of the specified expression over the specified
    locations.

    Parameters
    ----------
    expr : Any
    locations : Any
    ctxt : Any, optional
    Returns
    -------
    float
    """
    return _limit(min, expr, locations, ctxt)


def maximum(expr, locations, ctxt=None):
    """Compute the maximum of the specified expression over the specified
    locations.

    Parameters
    ----------
    expr : Any
    locations : Any
    ctxt : Any, optional
    Returns
    -------
    float
    """
    return _limit(max, expr, locations, ctxt)


def mass_average(expr, locations, ctxt=None):
    """Compute the mass-weighted average value of the specified expression over
    the specified locations.

    Parameters
    ----------
    expr : Any
    locations : Any
    ctxt : Any, optional
    Returns
    -------
    float
    """
    return _extent_average("Mass", expr, locations, ctxt)


def mass_integrated_average(expr, locations, ctxt=None):
    """Compute the total mass-weighted value of the specified expression over
    the specified locations.

    Parameters
    ----------
    expr : Any
    locations : Any
    ctxt : Any, optional
    Returns
    -------
    float
    """
    return _extent_integrated_average("Mass", expr, locations, ctxt)


def mass_flow_average(expr, locations, ctxt=None):
    """Compute the mass-flow-weighted average value of the specified expression
    over the specified locations.

    Parameters
    ----------
    expr : Any
    locations : Any
    ctxt : Any, optional
    Returns
    -------
    float
    """
    return _extent_average("MassFlow", expr, locations, ctxt)


def mass_flow_integrated_average(expr, locations, ctxt=None):
    """Compute the total mass flow over the specified locations.

    Parameters
    ----------
    expr : Any
    locations : Any
    ctxt : Any, optional
    Returns
    -------
    float
    """
    return _extent_integrated_average("MassFlow", expr, locations, ctxt)


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
