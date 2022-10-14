
from collections import defaultdict

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

'''
API objects no hashable so avoid dict
def _locns(locns):
    locn_names_and_objs = _locn_names_and_objs(locns)
    locn_dict = defaultdict(list)
    for name, obj in locn_names_and_objs:
        locn_dict[_root(obj)].append(name)
    return locn_dict
'''

def _locns(locns):
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
    return locn_list

def area_average(expr, locations, ctxt=None):
    locns = _locns(locations)
    if not all(locn[0] for locn in locns) and (
        any(locn[0] for locn in locns) or not ctxt
        ):
        raise BadReductionRequest("Invlaid combination of arguments")
    multi_solver = len(locns) > 1
    numerator = 0.0
    denominator = 0.0
    for solver, names in locns:
        solver = solver or _root(ctxt)
        named_exprs = solver.setup.named_expressions
        expr_name = "temp_expr_1"
        named_exprs[expr_name] = {}
        expr = named_exprs["temp_expr_1"] # request anonymous name object creation
        expr.definition = f"AreaAverage({expr},{names})"
        val = 42 # expr.get_value()
        if multi_solver:
            expr_name_2 = "temp_expr_2"
            expr = named_exprs[expr_name_2]
            expr.definition = f"Area({names})"
            extent = 1 # expr.get_value()
            named_exprs.pop(expr_name_2)
        else:
            extent = 1
        numerator += val * extent
        denominator += extent
        named_exprs.pop(expr_name)
    if denominator == 0.0:
        raise BadReductionRequest("Zero extent computed for average")
    return numerator / denominator
