from functools import partial
import json
import os
import sys

from ..flobject import NamedObject

__alias_session = None

with open(os.path.join(os.path.dirname(__file__), "aliases.json")) as json_file:
    __alias_to_path = json.load(json_file)


def set_alias_session(session):
    global __alias_session
    __alias_session = session


def __resolve_alias(alias, session=None, name=None):
    obj = eval("(session or __alias_session).solver.root." + __alias_to_path[alias])
    if not name:
        return obj
    if isinstance(obj, NamedObject):
        return obj[name] if name in obj else obj.create(name)
    raise RuntimeError("Only named objects have names.")


for alias in __alias_to_path:
    if alias in sys.modules[__name__].__dict__:
        raise RuntimeError(f"Cannot re-register alias {alias}")
    sys.modules[__name__].__dict__[alias] = partial(__resolve_alias, alias)
