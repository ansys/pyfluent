
from collections import defaultdict
from os import name

class BadReductionRequest(Exception):
    def __init__(self, err):
        super().__init__(f"Could not complete reduction function request: {err}")


def _is_iterable(obj):
    return hasattr(type(obj), '__iter__')


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
    name = getattr(obj, "obj_name", None)
    if name is None:
        return None
    if name == "":
        return obj
    return _root(obj._parent)


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
    val = 42 # expr.get_value()
    named_exprs.pop(expr_name)
    return val


def _eval_reduction(solver, reduction, locations, expr=None):
    return _eval_expr(
        solver,
        (f"{reduction}({locations})" if expr is None else
         f"{reduction}({expr},{locations})"
    ))


def _extent_average(extent_name, expr, locations, ctxt):
    locns = _locns(locations, ctxt)
    numerator = 0.0
    denominator = 0.0
    for solver, names in locns:
        solver = solver or _root(ctxt)
        val = _eval_reduction(solver, f"{extent_name}Average", names, expr)
        extent = _eval_reduction(solver, extent_name, names) if len(locns) > 1 else 1
        numerator += val * extent
        denominator += extent
    if denominator == 0.0:
        raise BadReductionRequest("Zero extent computed for average")
    return numerator / denominator


def _extent(extent_name, locations, ctxt):
    locns = _locns(locations, ctxt)
    total = 0.0
    for solver, names in locns:
        solver = solver or _root(ctxt)
        extent = _eval_expr(solver, f"{extent_name}({names})")
        total += extent
    return total


def _limit(limit, expr, locations, ctxt):
    locns = _locns(locations, ctxt)
    limit_val = None
    for solver, names in locns:
        solver = solver or _root(ctxt)
        val = _eval_reduction(
            solver,
            "Minimum" if limit is min else "Maximum", 
            names,
            expr
        )
        limit_val = val if limit_val is None else limit(val, limit_val)
    return limit_val


def _find_limit(limit, expr, locations, ctxt):
    locns = _locns(locations, ctxt)
    limit_val = None
    results = None
    for solver, names in locns:
        solver = solver or _root(ctxt)
        val = _eval_reduction(
            solver,
            "Minimum" if limit is min else "Maximum",
            names,
            expr
        )
        if limit_val is None or limit(val, limit_val) != limit_val:
            limit_val = val
            results = [(solver, names)]
        elif val == limit_val:
            results.append((solver, names))
    return results

# allow expr obj and extract defn

def area_average(expr, locations, ctxt=None):
    return _extent_average("Area", expr, locations, ctxt)


def volume_average(expr, locations, ctxt=None):
    return _extent_average("Volume", expr, locations, ctxt)


def area(locations, ctxt=None):
    return _extent("Area", locations, ctxt)


def volume(locations, ctxt=None):
    return _extent("Volume", locations, ctxt)


def minumum(expr, locations, ctxt=None):
    return _limit(min, expr, locations, ctxt)


def maximum(expr, locations, ctxt=None):
    return _limit(max, expr, locations, ctxt)


def find_minumum(expr, locations, ctxt=None):
    return _find_limit(min, expr, locations, ctxt)


def find_maximum(expr, locations, ctxt=None):
    return _find_limit(max, expr, locations, ctxt)
