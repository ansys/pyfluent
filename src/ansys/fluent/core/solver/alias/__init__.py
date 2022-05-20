from functools import partial
import json
import os
import sys

from ..flobject import NamedObject

print("aliases")

__alias_session = None

__alias_to_path = None
with open(os.path.join(os.path.dirname(__file__), "aliases.json")) as json_file:
    __alias_to_path = json.load(json_file)

print("__alias_to_path", __alias_to_path)


def set_alias_session(session):
    global __alias_session
    __alias_session = session


def __resolve_alias(alias, session=None, name=None):
    print("__resolve_alias", alias, session, name)
    print("__alias_to_path", __alias_to_path)
    path = __alias_to_path[alias]
    print("__resolve_alias", alias, path, session, name)
    session = session or __alias_session
    full_path = "session.solver.root." + path
    print("full_path", full_path)
    obj = eval(full_path)
    print("obj", obj)
    if not name:
        print("return obj")
        return obj
    if isinstance(obj, NamedObject):
        print("return obj[", name, "]")
        return obj[name]
    raise RuntimeError("Only named objects have names.")


print("__alias_to_path", __alias_to_path)

for alias in __alias_to_path:
    if alias in sys.modules[__name__].__dict__:
        raise RuntimeError(f"Cannot re-register alias {alias}")
    print("assign to module", alias)
    sys.modules[__name__].__dict__[alias] = partial(__resolve_alias, alias)

print("module", sys.modules[__name__].__dict__)
