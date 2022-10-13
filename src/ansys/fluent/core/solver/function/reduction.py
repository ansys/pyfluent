

class BadReductionRequest(Exception):
    def __init__(self, ex):
        super().__init__(f"Could not complete reduction function request: {ex}")


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


def area_average(expr, locations, ctxt=None):
    locn_names_and_objs = _locn_names_and_objs(locations)