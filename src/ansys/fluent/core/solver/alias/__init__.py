import json
import os
import sys

from ..flobject import NamedObject

__alias_session = None
__fns = sys.modules[__name__].__dict__

with open(os.path.join(os.path.dirname(__file__), "aliases.json")) as json_file:
    alias_to_path = json.load(json_file)


def set_alias_session(session):
    global __alias_session
    __alias_session = session


def _resolve_alias(path, session, name):
    session = session or __alias_session
    obj = eval("session.solver.root." + path)
    if not name:
        return obj
    if isinstance(obj, NamedObject):
        return obj[name]
    raise RuntimeError("Only named objects have names.")


for alias, path in alias_to_path.items():
    __fns[alias] = lambda session=None, name=None: _resolve_alias(path, session, name)
