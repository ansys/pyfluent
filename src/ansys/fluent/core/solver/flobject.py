# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
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

"""Module for accessing and modifying hierarchy of Fluent settings.

The only useful method is '`get_root``, which returns the root object for
accessing Fluent settings.

Child objects can be generally accessed or modified using attribute access.
Named child objects can be accessed or modified using index operators.

Calling an object will return its current value.

Example
-------
>>> r = flobject.get_root(proxy)
>>> is_energy_on = r.setup.models.energy.enabled()
>>> r.setup.models.energy.enabled = True
>>> r.boundary_conditions.velocity_inlet['inlet'].vmag.constant = 20
"""

from __future__ import annotations

import collections
import collections.abc  # needed so `collections.abc.X` resolves for the type checker
from collections.abc import (
    Callable,
    ItemsView,
    Iterator,
    KeysView,
    ValuesView,
)
from contextlib import contextmanager, nullcontext, suppress
from enum import Enum
import fnmatch
from functools import total_ordering
import hashlib
import keyword
import logging
import os
import os.path
import pickle
import string
import sys
import types
from typing import (
    TYPE_CHECKING,
    Any,
    ForwardRef,
    Generic,
    Iterable,
    NewType,
    NoReturn,
    TextIO,
    TypeVar,
    Union,
    _eval_type,
    get_args,
    get_origin,
)
import warnings
import weakref

if TYPE_CHECKING:
    from ansys.fluent.core.connectivity.file_transfer_service import (
        FileTransferStrategy,
    )

from ansys.fluent.core._type_checking import no_runtime_type_check
from ansys.fluent.core._variable_strategies import (
    FluentFieldDataNamingStrategy as naming_strategy,
)
from ansys.fluent.core.utils.fluent_version import FluentVersion
from ansys.fluent.core.utils.get_completer_info import (
    get_completer_info as _get_completer_info,
)
import ansys.units
from ansys.units import VariableDescriptor

from . import _docstrings
from .error_message import allowed_name_error_message, allowed_values_error
from .flunits import UnhandledQuantity, get_si_unit_for_fluent_quantity
from .settings_external import expand_api_file_argument

settings_logger: logging.Logger = logging.getLogger("pyfluent.settings_api")


_static_class_attributes = [
    "_version",
    "exposure_level",
    "_deprecated_version",
    "_python_name",
    "fluent_name",
    "_parent_class",
]


# --------------------------------------------------------------------------- #
# Settings-expression protocol                                                #
# --------------------------------------------------------------------------- #
#
# Any Python value can behave as an "expression object" at a settings leaf by
# implementing the small, domain-neutral protocol below.  The settings layer
# deliberately knows *nothing* about Fluent expressions (or any other concrete
# expression implementation): it only talks to these dunder methods.
#
#   __settings_str__(self) -> str
#       REQUIRED.  Render the object to the string the settings leaf stores.
#       Validation (see below) always runs *before* this is called.
#
#   __settings_kind__(self) -> str | None
#       OPTIONAL.  Describe the *shape* of the produced value using one of the
#       neutral tags in :data:`_EXPRESSION_KINDS` ("scalar", "vector",
#       "boolean", "quantity", "location_list").  Return ``None`` when the kind
#       is unknown, in which case the structural check is skipped.
#
#   __settings_dimensions__(self) -> dict[str, float] | None
#       OPTIONAL.  Describe the physical dimensions of the produced value as a
#       mapping of base-dimension name (e.g. ``"MASS"``) to exponent.  Return
#       ``None`` when unknown, in which case the dimensional check is skipped.
#
# This keeps the generic settings layer decoupled from the Fluent expression
# builder: the builder's AST nodes simply implement these methods.
_EXPRESSION_KINDS = ("scalar", "vector", "boolean", "quantity", "location_list")


def _is_settings_expression(state) -> bool:
    """Return ``True`` when ``state`` implements the settings-expression protocol.

    Duck-typed on :func:`__settings_str__` -- a cheap ``getattr`` that
    short-circuits for the overwhelmingly common case of plain values.
    """
    return callable(getattr(state, "__settings_str__", None))


def _normalize_dimensions(dimensions) -> dict[str, float]:
    """Normalize a dimensions mapping to ``{name: exponent}``.

    Accepts either an ``ansys.units`` ``Dimensions`` object (whose keys are
    ``BaseDimensions`` enum members) or a plain ``{name: exponent}`` dict, so
    the settings layer can compare values coming from different sources.  Zero
    exponents are dropped.
    """
    normalized: dict[str, float] = {}
    for key, exponent in dict(dimensions).items():
        if not exponent:
            continue
        # ``BaseDimensions`` enum members expose ``.name``; plain string keys
        # are used as-is.
        name = getattr(key, "name", key)
        normalized[str(name)] = float(exponent)
    return normalized


def _leaf_dimensions(leaf) -> dict[str, float] | None:
    """Best-effort physical dimensions implied by a leaf's units, or ``None``.

    Only numerical leaves (those exposing a ``units()`` method, e.g.
    :class:`RealNumerical`) carry unit information.  Any failure to resolve the
    units into dimensions is treated as "unknown" (returns ``None``) so the
    dimensional check never blocks a legitimate assignment.

    A ``None`` units string means the units are unknown (unresolved) and yields
    ``None``.  An empty units string (``""``) means a *known* dimensionless
    setting -- ``get_si_unit_for_fluent_quantity`` returns ``""`` for
    dimensionless quantities such as turbulent intensity -- and yields an empty
    ``{}`` mapping so that a dimensional expression (e.g. a pressure-valued one)
    is correctly rejected rather than silently skipped.
    """
    units = getattr(leaf, "units", None)
    if not callable(units):
        return None
    try:
        unit_str = units()
        if unit_str is None:
            return None
        return _normalize_dimensions(ansys.units.Quantity(1, unit_str).dimensions)
    except Exception:
        return None


def _leaf_label(leaf) -> str:
    """Return a human-readable label for ``leaf`` in error messages.

    ``leaf`` may be a leaf *instance* (whose ``python_path`` is a string) or a
    leaf *class* (reached via the shared ``to_scheme_keys`` conversion path,
    where ``python_path``/``python_name`` resolve to property descriptors rather
    than strings).  Falls back to the class name so the message stays readable.
    """
    for attr in ("python_path", "python_name"):
        value = getattr(leaf, attr, None)
        if isinstance(value, str):
            return value
    return getattr(leaf, "__name__", None) or str(leaf)


# Sentinel distinguishing "leaf dimensions were not precomputed" (resolve them
# via an RPC) from a resolved value of ``None`` (units are genuinely unknown).
_LEAF_DIMS_UNRESOLVED = object()


def _validate_expression_quantity(
    leaf, state, accepted_kinds=None, leaf_dims=_LEAF_DIMS_UNRESOLVED
) -> None:
    """Validate an expression object against ``leaf`` *before* it is rendered.

    Performs two independent, best-effort "quantity-type" checks so that an
    obviously incompatible expression is rejected in the client settings layer
    rather than producing a string that Fluent would later reject:

    1. **Structural kind** -- compares the expression's ``__settings_kind__``
       against the kinds the leaf accepts (``leaf._expression_kinds``, or
       ``accepted_kinds`` when supplied -- e.g. the scalar kinds used for each
       element of a real-list leaf).  This catches, for example, a vector or
       boolean expression assigned to a scalar real leaf.  Skipped when either
       side does not declare its kind.
    2. **Physical dimension** -- compares the expression's
       ``__settings_dimensions__`` against the dimensions implied by the leaf's
       units.  Only a *confident* mismatch (both sides known and different)
       raises; unknown dimensions are tolerated so that composite expressions
       (whose dimensions cannot be inferred) are never blocked.

    ``leaf_dims`` lets a caller pass the leaf's already-resolved dimensions so a
    bulk assignment (e.g. a :class:`RealList`) resolves the leaf's units once
    instead of once per element -- each resolution is an uncached RPC.  When
    left unset the dimensions are resolved here on demand.

    Raises
    ------
    TypeError
        If the expression's kind or dimensions are incompatible with ``leaf``.
    """
    leaf_label = _leaf_label(leaf)

    # 1. Structural kind check.
    if accepted_kinds is None:
        accepted_kinds = getattr(leaf, "_expression_kinds", None)
    kind_getter = getattr(state, "__settings_kind__", None)
    kind = kind_getter() if callable(kind_getter) else None
    if accepted_kinds is not None and kind is not None and kind not in accepted_kinds:
        raise TypeError(
            f"Expression of kind '{kind}' is not valid for '{leaf_label}', "
            f"which accepts {', '.join(accepted_kinds)} expressions."
        )

    # 2. Physical dimension check (best-effort, only on confident mismatch).
    dims_getter = getattr(state, "__settings_dimensions__", None)
    raw_expr_dims = dims_getter() if callable(dims_getter) else None
    if raw_expr_dims is None:
        return
    expr_dims = _normalize_dimensions(raw_expr_dims)
    if leaf_dims is _LEAF_DIMS_UNRESOLVED:
        leaf_dims = _leaf_dimensions(leaf)
    if leaf_dims is None:
        # Leaf units are unknown (unresolved) -- do not block.  An empty
        # ``expr_dims`` ({}) is a *known* dimensionless expression (the protocol
        # uses ``None`` for unknown, handled above), so it is still compared
        # against the leaf below rather than skipped here.
        return
    if expr_dims != leaf_dims:
        raise TypeError(
            f"Expression with dimensions {expr_dims} is not compatible with "
            f"'{leaf_label}', which expects dimensions {leaf_dims}."
        )


def _render_settings_expression(
    leaf, state, accepted_kinds=None, leaf_dims=_LEAF_DIMS_UNRESOLVED
) -> str | None:
    """Validate and render ``state`` when it is a settings-expression object.

    Returns the rendered string, or ``None`` when ``state`` is not an
    expression object (so callers fall through to their normal handling).  The
    quantity-type validation always runs *before* the string is produced,
    satisfying the "check the quantity type prior to ``str`` conversion"
    contract.  ``accepted_kinds`` overrides the leaf's declared kinds for the
    kind check (used when validating individual elements of a list leaf).
    ``leaf_dims`` optionally supplies the leaf's already-resolved dimensions so
    repeated element validation does not re-resolve the leaf's units per call.

    Raises
    ------
    TypeError
        If validation fails, or if the object does not render to a string.
    """
    if not _is_settings_expression(state):
        return None
    _validate_expression_quantity(leaf, state, accepted_kinds, leaf_dims)
    rendered = state.__settings_str__()
    if not isinstance(rendered, str):
        raise TypeError(
            f"Expression object {state!r} did not render to a string "
            f"(got {type(rendered).__name__})."
        )
    return rendered


def _render_settings_expression_list(leaf, state, accepted_kinds) -> list | None:
    """Render a ``list`` whose elements may be settings-expression objects.

    A list leaf holds a *container* of values, so each element is an independent
    expression rather than a single expression describing the whole assignment.
    Every expression element is validated (against ``accepted_kinds`` -- the
    kinds a single element may take -- and the leaf's units, when it has any) and
    rendered to its string form, while plain values are left untouched,
    preserving the list structure.  ``accepted_kinds`` differs by leaf: a
    real-list element is scalar, whereas a string/filename-list element may be
    any expression-string kind.

    The leaf's dimensions are resolved *once* for the whole assignment and
    reused for every element: each resolution is an uncached ``units()`` RPC, so
    resolving per element would add one network round trip per element.

    Returns the rebuilt list, or ``None`` when ``state`` is not a ``list`` or
    carries no expression element, so callers fall through to normal handling.
    A ``tuple`` is deliberately *not* treated as an element container because a
    real leaf interprets a tuple as a ``(value, units)`` quantity.
    """
    if not isinstance(state, list):
        return None
    if not any(_is_settings_expression(element) for element in state):
        return None
    leaf_dims = _leaf_dimensions(leaf)
    return [
        (
            _render_settings_expression(leaf, element, accepted_kinds, leaf_dims)
            if _is_settings_expression(element)
            else element
        )
        for element in state
    ]


def _textual_list_set_state(self, state=None, **kwargs) -> None:
    """``set_state`` for ``Textual`` list leaves (``StringList``/``FilenameList``).

    These leaves subclass ``SettingsBase`` *before* :class:`Textual` in the MRO,
    so a bare ``set_state`` would resolve to ``SettingsBase.set_state`` and skip
    the settings-expression protocol -- serializing expression objects with
    ``str()`` instead of rendering/validating them.  Each element of the list
    may be an independent expression (e.g. a named-expression definition), so
    they are validated against the leaf's per-element accepted kinds and
    rendered to their string form before delegating to the inherited setter.
    Plain values and non-list states are passed through unchanged.
    """
    rendered_list = _render_settings_expression_list(
        self, state, getattr(self, "_element_expression_kinds", None)
    )
    if rendered_list is not None:
        return self.base_set_state(state=rendered_list, **kwargs)
    return self.base_set_state(state=state, **kwargs)


def _settings_expression_to_scheme(leaf_cls, value):
    """Render/validate settings-expression objects in a leaf's scheme value.

    This is the *shared* conversion path used by every state-setting flow --
    direct leaf ``set_state``, :class:`Group` dict updates, and command
    arguments -- so an expression object is rendered via ``__settings_str__``
    (not serialized with ``str()``) and kind-checked consistently, regardless of
    how it reaches the leaf.

    Only leaves that opt into the protocol act: ``_expression_kinds`` gates
    whole-value expressions and ``_element_expression_kinds`` gates per-element
    expressions in a list.  Plain values (and leaves that do not opt in) are
    returned unchanged.

    ``leaf_cls`` is a leaf *class* here (``to_scheme_keys`` is a classmethod), so
    the physical-dimension check -- which needs a live instance's units -- is
    skipped; that check still runs on direct leaf assignment where the instance
    is available.
    """
    whole_kinds = getattr(leaf_cls, "_expression_kinds", None)
    if whole_kinds is not None:
        rendered = _render_settings_expression(leaf_cls, value, whole_kinds)
        if rendered is not None:
            return rendered
    element_kinds = getattr(leaf_cls, "_element_expression_kinds", None)
    if element_kinds is not None:
        rendered_list = _render_settings_expression_list(leaf_cls, value, element_kinds)
        if rendered_list is not None:
            return rendered_list
    return value


class InactiveObjectError(RuntimeError):
    """Inactive object access."""

    def __init__(self, python_path: str):
        """Initialize InactiveObjectError."""
        super().__init__(f"'{python_path}' is currently inactive.")


class ReadOnlyActionError(RuntimeError):
    """Read-only action execution."""

    def __init__(self, python_path: str):
        """Initialize ReadOnlyActionError."""
        super().__init__(f"'{python_path}' is read-only and cannot be executed.")


@total_ordering
class ExposureLevel(Enum):
    """API exposure level of a settings object."""

    ALPHA = "alpha"
    BETA = "beta"
    STABLE = "stable"

    def __lt__(self, other: object) -> bool:
        """Compare exposure levels by their order: ALPHA < BETA < STABLE."""
        if isinstance(other, ExposureLevel):
            order = {
                ExposureLevel.ALPHA: 0,
                ExposureLevel.BETA: 1,
                ExposureLevel.STABLE: 2,
            }
            return order[self] < order[other]
        return NotImplemented


def _is_hidden_by_exposure_level(child_cls, parent_obj) -> bool:
    """Whether a child settings class should be hidden based on exposure level.

    Parameters
    ----------
    child_cls : type
        The child settings class to check.
    parent_obj : Base
        The parent object instance, used to traverse to the root for activation flags.

    Returns
    -------
    bool
        True if the child should be hidden from dir and attribute access; False otherwise.
    """
    return child_cls.exposure_level < getattr(
        parent_obj._root, "_global_exposure_level", ExposureLevel.STABLE
    )


def _set_exposure_level(self, level: ExposureLevel) -> None:
    """Set the minimum exposure level for accessible settings objects.

    Parameters
    ----------
    level : ExposureLevel
        The minimum exposure level to make accessible.
        ``ExposureLevel.STABLE`` (default) hides all beta and alpha objects.
        ``ExposureLevel.BETA`` also exposes beta objects.
        ``ExposureLevel.ALPHA`` exposes all objects.
    """
    self._setattr("_global_exposure_level", level)


def _get_hidden_names(names, child_classes, obj) -> set:
    """Return names that should be hidden due to exposure level or deprecation."""
    hidden = set()
    for name in names:
        child_cls = child_classes.get(name)
        if child_cls is not None and _is_hidden_by_exposure_level(child_cls, obj):
            hidden.add(name)
        elif _is_deprecated(object.__getattribute__(obj, name)):
            hidden.add(name)
    return hidden


def _get_active_names(obj, names: list) -> list:
    """Return entries from ``names`` that are active and visible at the current exposure level."""
    ret = []
    child_classes = type(obj)._child_classes
    for name in names:
        child_cls = child_classes.get(name)
        if child_cls is not None and _is_hidden_by_exposure_level(child_cls, obj):
            continue
        child = getattr(obj, name)
        if child.is_active() and not _is_deprecated(child):
            ret.append(name)
    return ret


def _raise_if_exposure_hidden(name, child_classes, obj) -> None:
    """Raise AttributeError if name is hidden due to exposure level."""
    child_cls = child_classes.get(name)
    if child_cls is not None and _is_hidden_by_exposure_level(child_cls, obj):
        raise AttributeError(
            f"'{name}' is not available at the current exposure level. "
            f"Call 'set_exposure_level(ExposureLevel.BETA)' or "
            f"'set_exposure_level(ExposureLevel.ALPHA)' on the settings root "
            f"to enable access to beta or alpha objects."
        )


class _InlineConstants:
    is_active = "active?"
    is_read_only = "read-only?"
    default_value = "default"
    min = "min"
    max = "max"
    user_creatable = "user-creatable?"
    allowed_values = "allowed-values"
    file_purpose = "file-purpose"


# Type hints
RealType = NewType("real", float | str)  # constant or expression
RealListType = list[RealType]
RealVectorType = tuple[RealType, RealType, RealType]
IntListType = list[int]
StringListType = list[str]
BoolListType = list[bool]
PrimitiveStateType = Union[
    str,
    RealType,
    int,
    bool,
    RealListType,
    IntListType,
    StringListType,
    BoolListType,
]
DictStateType = dict[str, "StateType"]
ListStateType = list["StateType"]
StateType = Union[PrimitiveStateType, DictStateType, ListStateType]


def check_type(val: Any, tp: Any) -> bool:
    """Check type of object."""
    if hasattr(tp, "__supertype__"):
        return check_type(val, tp.__supertype__)
    if isinstance(tp, str):
        try:
            return check_type(val, _eval_type(ForwardRef(tp), globals(), locals()))
        except Exception:
            return False
    if isinstance(tp, ForwardRef):
        return check_type(val, _eval_type(tp, globals(), locals()))
    origin = get_origin(tp)
    if origin == list:
        return isinstance(val, list) and all(
            check_type(x, get_args(tp)[0]) for x in val
        )
    elif origin == tuple:
        return isinstance(val, tuple) and all(
            check_type(x, t) for x, t in zip(val, get_args(tp))
        )
    elif origin in (Union, types.UnionType):
        return any(check_type(val, t) for t in get_args(tp))
    elif origin == dict:
        k_t, k_v = get_args(tp)
        return isinstance(val, dict) and all(
            check_type(k, k_t) and check_type(v, k_v) for k, v in val.items()
        )
    elif origin is None:
        try:
            return isinstance(val, tp)
        except TypeError:
            return False
    else:
        return False


def assert_type(val: Any, tp: Any) -> None:
    """Assert type.

    Raises
    ------
    TypeError
        If the given value is not of the given type.
    """
    if not check_type(val, tp):
        raise TypeError(f"{val} is not of type {tp}.")


_ttable = str.maketrans(string.punctuation, "_" * len(string.punctuation), "?'")


def to_python_name(fluent_name: str) -> str:
    """Convert a scheme string to a Python variable name.

    This function replaces symbols with _. ``'`` and ``?`` symbols are
    ignored.
    """
    if not fluent_name:
        return fluent_name
    name = fluent_name.translate(_ttable)
    while name in keyword.kwlist:
        name = name + "_"
    return name


def to_constant_name(fluent_name: str) -> str:
    """Convert a scheme string to a Python constant name.

    This function replaces symbols and spaces with _ and converts the name to uppercase.
    ``'`` and ``?`` symbols are ignored.
    """
    fluent_name = fluent_name.replace(" ", "_")
    name = fluent_name.translate(_ttable).upper()
    if not name:
        return "EMPTY_STRING"
    if name[0].isdigit():
        # If the first character is a digit, prepend "CASE_"
        name = "CASE_" + name
    return name


_to_field_name_str = naming_strategy().to_string


def _get_python_path_comps(obj):
    """Get python path components for traversing class hierarchy."""
    comps = []
    while obj is not None:
        python_name = obj.python_name
        obj = obj._parent
        if isinstance(obj, (NamedObject, ListObject)):
            comps.append(obj.python_name)
            obj = obj._parent
        else:
            comps.append(python_name)
    comps.reverse()
    return comps[1:]


def get_full_path(base_path: list[str], relative_path: list[str]) -> list[str]:
    """
    Get full path by applying relative path to base path.

    Parameters
    ----------
    base_path: list[str]
        The base path.

    relative_path: list[str]
        The relative path, which can contain ".." to indicate going up one level in the hierarchy.

    Returns
    -------
    list[str]
        The full path obtained by applying the relative path to the base path.

    Raises
    ------
    ValueError
        If the relative path tries to go beyond the root of the hierarchy.
    """
    base_path = base_path.copy()
    relative_path = relative_path.copy()
    while relative_path and relative_path[0] == "..":
        if not base_path:
            raise ValueError("Relative path goes beyond root.")
        base_path.pop()
        relative_path.pop(0)
    return base_path + relative_path


def _get_class_from_paths(
    root_cls, base_path: list[str], relative_path: list[str]
) -> tuple[type, list[str]]:
    """
    Get the settings class from a base path and a relative path.

    Parameters
    ----------
    root_cls: type
        The root class to start from.

    base_path: list[str]
        The base path from the root class to the base of the relative path.

    relative_path: list[str]
        The relative path from the base to the target class. This can contain ".." to
        indicate going up one level in the hierarchy.

    Returns
    -------
    tuple[type, list[str]]
        The target class and the full path from the root class to the target class.
    """

    full_path = get_full_path(base_path, relative_path)
    cls = root_cls
    for comp in full_path:
        cls = cls._child_classes[comp]
        if issubclass(cls, (NamedObject, ListObject)):
            cls = cls.child_object_type
    return cls, full_path


def _is_deprecated(obj) -> bool | None:
    """Whether the object is deprecated in a specific Fluent version."""
    if FluentVersion(obj._version) >= FluentVersion.v252:
        # "_deprecated_version" is part of generated data since 25R2
        deprecated_version = getattr(obj, "_deprecated_version", None)
    else:
        deprecated_version = obj.get_attrs(["deprecated-version"])
        if deprecated_version:
            deprecated_version = deprecated_version.get("attrs", deprecated_version)
        deprecated_version = (
            deprecated_version.get("deprecated-version") if deprecated_version else None
        )
    return deprecated_version and FluentVersion(obj._version) >= FluentVersion(
        deprecated_version
    )


@no_runtime_type_check
class Base:
    """Provides the base class for settings and command objects.

    Parameters
    ----------
    name : str
        Name of the object if a child of a named object.
    parent: Base
           Parent of the object.

    Attributes
    ----------
    flproxy
    obj_name
    fluent_name
    """

    def __init__(self, name: str | None = None, parent: "Base | None" = None):
        """__init__ of Base class."""
        self._setattr("_parent", weakref.proxy(parent) if parent is not None else None)
        self._setattr("_flproxy", None)
        self._setattr("_file_transfer_service", None)
        if name is not None:
            self._setattr("_name", name)
        self._setattr("_child_alias_objs", {})

    @property
    def _root(self):
        if self._parent is None:
            return self
        else:
            return self._parent._root

    def set_flproxy(self, flproxy: Any) -> None:
        """Set flproxy object."""
        self._setattr("_flproxy", flproxy)

    def _set_on_interrupt(self, on_interrupt):
        """Set interrupt method."""
        self._setattr("_on_interrupt", on_interrupt)

    def _set_is_interruptible_command(self, is_interruptible_command):
        """Set interruptible command checker."""
        self._setattr("_is_interruptible_command", is_interruptible_command)

    def _set_file_transfer_service(self, file_transfer_service):
        """Set file_transfer_service."""
        self._setattr("_file_transfer_service", file_transfer_service)

    @property
    def flproxy(self) -> Any:
        """Proxy object.

        The proxy object is set at the root level and accessed via the parent for the
        child classes.
        """
        if self._flproxy is None:
            return self._parent.flproxy
        return self._flproxy

    @property
    def _file_transfer_handler(self):
        """Remote file handler.

        Supports file upload and download.
        """
        if self._file_transfer_service:
            return self._file_transfer_service
        elif self._parent:
            return self._parent._file_transfer_handler

    _name = None
    fluent_name = None
    _python_name = None

    @property
    def parent(self) -> "Base | None":
        """Parent (container) object."""
        return self._parent

    @property
    def obj_name(self) -> str:
        """Name of the scheme of this object.

        By default, this returns the object's static name. If the object is a child of a
        named object, the object's name is returned.
        """
        if self._name is None:
            return self.fluent_name
        return self._name

    @property
    def python_name(self) -> str:
        """Python name of this object.

        By default, this returns the object's static name. If the object is a child of a
        named object, the object's name is returned.
        """
        return getattr(self, "_python_name", None) or self.__class__.__name__

    @property
    def path(self) -> str:
        """Path of the object.

        Constructed from the ``obj_name`` of self and the path of
        parent.
        """
        if self._parent is None:
            return self.obj_name
        ppath = self._parent.path
        if not ppath:
            return self.obj_name
        return ppath + "/" + self.obj_name

    @property
    def python_path(self) -> str:
        """Path of the object.

        Constructed in python syntax from 'python_path' and the parents python path.
        """
        if self._parent is None:
            if FluentVersion(self._version).number < 251:
                return "<session>"
            else:
                return "<session>.settings"
        ppath = self._parent.python_path
        if not ppath:
            return self.python_name
        if self.python_name[0] == "[":
            return ppath + self.python_name
        return ppath + "." + self.python_name

    def get_attrs(self, attrs: list[str], recursive: bool = False) -> StateType:
        """Get the requested attributes for the object.

        Parameters
        ----------
        attrs : list
            List of attribute names to retrieve.
        recursive : bool, optional
            Whether to retrieve attributes recursively, by default False.

        Returns
        -------
        StateType
            Requested attributes.
        """
        return self.flproxy.get_attrs(self.path, attrs, recursive)

    def get_attr(
        self,
        attr: str,
        attr_type_or_types: type | tuple[type] | None = None,
    ) -> StateType:
        """Get the requested attribute for the object.

        Parameters
        ----------
        attr : str
            attribute name
        attr_type_or_types : type or tuple of type, optional
            attribute type, by default None

        Returns
        -------
        StateType
            attribute value

        Raises
        ------
        InactiveObjectError
            If any attribute other than ``"active?`` is queried when the object is not active.
        """
        attrs = self.get_attrs([attr])
        if attrs:
            attrs = attrs.get("attrs", attrs)
        if attr != "active?" and attrs and attrs.get("active?", True) is False:
            raise InactiveObjectError(self.python_path)
        val = None
        if attrs:
            val = attrs[attr]

        if attr_type_or_types:
            if not isinstance(attr_type_or_types, tuple):
                attr_type_or_types = (attr_type_or_types,)
            if isinstance(val, attr_type_or_types):
                return val
            if val is not None and any(
                issubclass(x, bool) for x in attr_type_or_types
            ):  # cast to bool for boolean attributes
                return bool(val)
            return None
        return val

    def is_active(self) -> bool:
        """Whether the object is active."""
        attr = self.get_attr(_InlineConstants.is_active)
        return False if attr is False else True

    def is_read_only(self) -> bool:
        """Whether the object is read-only."""
        attr = self.get_attr(_InlineConstants.is_read_only)
        return False if attr is None else attr

    def __setattr__(self, name: str, value: Any) -> NoReturn:
        raise AttributeError(name)

    # __setattr__ is overridden to prevent creation of new attributes or
    # overriding existing ones. _setattr is the backdoor to set attributes
    def _setattr(self, name, value):
        super().__setattr__(name, value)

    def find_object(self, relative_path: str) -> "Base":
        """Find object."""
        obj = self
        for comp in relative_path.split("/"):
            if comp == "..":
                obj = obj.parent
            else:
                obj = getattr(obj, comp)
        return obj

    def before_execute(
        self, command_name: str, value: StateType, kwargs: dict[str, StateType]
    ) -> StateType:
        """Executes before command execution."""
        if hasattr(self, "_do_before_execute"):
            base_file_name = self._do_before_execute(
                command_name=command_name, value=value, kwargs=kwargs
            )
            return base_file_name
        else:
            return value

    def after_execute(
        self, command_name: str, value: StateType, kwargs: dict[str, StateType]
    ) -> StateType:
        """Executes after command execution."""
        if hasattr(self, "_do_after_execute"):
            base_file_name = self._do_after_execute(
                command_name=command_name, value=value, kwargs=kwargs
            )
            return base_file_name
        else:
            return value

    def _while_setting_state(self):
        """Avoid additional processing while setting the state."""
        return nullcontext()

    def _while_renaming(self):
        """Avoid additional processing while renaming."""
        return nullcontext()

    def _while_deleting(self):
        """Avoid additional processing while deleting."""
        return nullcontext()

    def _while_creating(self):
        """Avoid additional processing while creating."""
        return nullcontext()

    def _while_resizing(self):
        """Avoid additional processing while resizing."""
        return nullcontext()

    def _while_executing_command(self):
        """Avoid additional processing while executing a command."""
        return nullcontext()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.flproxy == other.flproxy and self.path == other.path

    def get_completer_info(
        self, prefix: str = "", excluded: Iterable[str] | None = None
    ) -> list[list[str]]:
        """Get completer information of all children.

        Returns
        -------
        list[list[str]]
            Name, type and docstring of all children.
        """

        def filter_deprecated(v) -> bool:
            if isinstance(v, Base):
                return not _is_deprecated(v)
            return True

        return _get_completer_info(
            obj=self,
            base_class=Base,
            prefix=prefix,
            excluded=excluded,
            filter_function=filter_deprecated,
            type_name_map=_type_name_map,
        )


StateT = TypeVar("StateT")


class Property(Base):
    """Exposes attribute accessor on settings object."""

    def default_value(self) -> StateType:
        """Gets the default value of the object."""
        return self.get_attr(_InlineConstants.default_value)


class Numerical(Property):
    """Exposes attribute accessor on settings object - specific to numerical objects."""

    def min(self) -> float | int | None:
        """Get the minimum value of the object."""
        val = self.get_attr(_InlineConstants.min, (float, int))
        return None if isinstance(val, bool) else val

    def max(self) -> float | int | None:
        """Get the maximum value of the object."""
        val = self.get_attr(_InlineConstants.max, (float, int))
        return None if isinstance(val, bool) else val


QuantityT = TypeVar("QuantityT")


class RealNumerical(Numerical):
    """A ``RealNumerical`` object representing a real value setting, including single
    real values and containers of real values, such as lists.

    Methods
    -------
    as_quantity()
        Get the current state of the object as an ansys.units.Quantity.

    set_state(state)
        Set the state of the object.

    units()
        Get the units string.
    """

    # Real-valued leaves accept expression strings (see ``RealType``); a scalar
    # real therefore accepts scalar / value-with-units expression objects.
    # Containers (e.g. :class:`RealList`) widen this -- see their override.
    _expression_kinds: tuple[str, ...] = ("scalar", "quantity")

    def as_quantity(self) -> QuantityT | None:
        """Get the state of the object as an ansys.units.Quantity."""
        error = None
        if not error:
            quantity = self.get_attr("units-quantity")
            units = get_si_unit_for_fluent_quantity(quantity)
            if units is not None:
                try:
                    return ansys.units.Quantity(
                        value=self.get_state(),
                        units=units,
                    )
                except (TypeError, ValueError) as e:
                    error = e
            else:
                error = "Could not determine units."
        warnings.warn(f"Unable to construct 'Quantity'. {error}")

    def set_state(self, state: StateT | None = None, **kwargs: StateType) -> None:
        """Set the state of the object.

        Parameters
        ----------
        state
            The type of state can be float, str (representing either
            an expression or a value with units), an ansys.units.Quantity,
            or any object implementing the settings-expression protocol
            (``__settings_str__``) -- for example an ``Expr`` produced by the
            expression builder. Expression objects are validated against this
            leaf's kind and units before being rendered to a string.
        kwargs : StateType
            Keyword arguments.

        Raises
        ------
        UnhandledQuantity
            If the quantity object cannot be handled for the given path. This can
            happen if the quantity attribute specifies an unsupported quantity, or if
            the units specified for the quantity are not supported.
        TypeError
            If an expression object's kind or dimensions are incompatible with
            this leaf.
        """
        # Expression-object support: an object implementing the
        # settings-expression protocol is validated (kind + dimensions) and
        # rendered to its string form *before* any quantity handling below.
        # Real-valued leaves accept expression strings, so this is where an
        # ``Expr`` becomes a valid assignment for them.
        rendered = _render_settings_expression(self, state)
        if rendered is not None:
            return self.base_set_state(state=rendered, **kwargs)

        # List leaves (e.g. ``RealList``) accept a container of reals whose
        # elements may themselves be expression objects. Each element is an
        # independent scalar, so validate/render them with the per-element kinds
        # and this leaf's units while preserving the list structure.
        element_kinds = getattr(self, "_element_expression_kinds", None)
        if element_kinds is not None:
            rendered_list = _render_settings_expression_list(self, state, element_kinds)
            if rendered_list is not None:
                return self.base_set_state(state=rendered_list, **kwargs)

        try:

            def get_units():
                units = self.units()
                if units is None:
                    raise UnhandledQuantity(self.path, state)
                return units

            if isinstance(state, (ansys.units.Quantity, tuple)):
                state = (
                    ansys.units.Quantity(*state) if isinstance(state, tuple) else state
                )
                state = state.to(get_units()).value
            elif isinstance(state, tuple):
                if state[1] == get_units():
                    state = state[0]
                else:
                    raise UnhandledQuantity(self.path, state)
        except Exception as ex:
            raise UnhandledQuantity(self.path, state) from ex

        return self.base_set_state(state=state, **kwargs)

    def units(self) -> str | None:
        """Get the physical units of the object as a string."""
        quantity = self.get_attr("units-quantity")
        return get_si_unit_for_fluent_quantity(quantity)


class Textual(Property):
    """Exposes attribute accessor on settings object - specific to string objects."""

    # String leaves broadly accept Fluent expression strings (named-expression
    # definitions, boundary-condition profiles, and so on). A definition may be
    # scalar, vector, boolean, or a value-with-units, so all of those kinds are
    # accepted; a bare location list is not a valid string value.
    _expression_kinds: tuple[str, ...] = ("scalar", "vector", "boolean", "quantity")

    def set_state(self, state: StateT | None = None, **kwargs: StateType) -> None:
        """Set the state of the object.

        Parameters
        ----------
        state
            Either ``str``, ``VariableDescriptor``, or any object implementing
            the settings-expression protocol (``__settings_str__``) -- for
            example an ``Expr`` produced by the expression builder. Expression
            objects are validated against this leaf's accepted kinds before
            being rendered to their string form and stored.
        kwargs : StateType
            Keyword arguments.

        Raises
        ------
        TypeError
            If state is not a string, or if an expression object's kind is
            incompatible with this leaf.
        """
        # Expression-object support: an object implementing the
        # settings-expression protocol is validated and rendered to its string
        # form before the plain-string handling below. ``VariableDescriptor``
        # does not implement the protocol, so it falls through unchanged.
        rendered = _render_settings_expression(self, state)
        if rendered is not None:
            return self.base_set_state(state=rendered, **kwargs)

        allowed_types = (str, VariableDescriptor)

        if not isinstance(state, allowed_types):
            if self._has_migration_adapter:
                return self.base_set_state(state=state, **kwargs)
            raise TypeError(
                f"Expected state to be {' or '.join(t.__name__ for t in allowed_types)}, "
                f"got {type(state).__name__}."
            )
        return self.base_set_state(state=_to_field_name_str(state), **kwargs)


_show_warning_orig = warnings.showwarning


def _show_warning(message, category, *args, **kwargs):
    from ansys.fluent.core.diagnostics.exceptions import DeprecatedSettingWarning

    if category == DeprecatedSettingWarning:
        print(message)
    else:
        _show_warning_orig(message, category, *args, **kwargs)


warnings.showwarning = _show_warning


class _Alias:
    scheme_eval = None
    once = False

    @contextmanager
    def _print_newer_api(self):
        scheme_eval = _Alias.scheme_eval
        if scheme_eval:
            scheme_eval("(define pyfluent-journal-str-port (open-output-string))")
            scheme_eval("(api-echo-python-port pyfluent-journal-str-port)")
        try:
            yield
        finally:
            if scheme_eval:
                scheme_eval("(api-unecho-python-port pyfluent-journal-str-port)")
                journal_str = scheme_eval(
                    "(close-output-port pyfluent-journal-str-port)"
                )
                from ansys.fluent.core.diagnostics.exceptions import (
                    DeprecatedSettingWarning,
                )

                if isinstance(journal_str, str):
                    warnings.warn(
                        "A newer syntax is available to perform the last operation:\n"
                        f"{journal_str.strip()}",
                        DeprecatedSettingWarning,
                    )
                if not _Alias.once:
                    warnings.warn(
                        "\nExecute the following code to suppress future warnings like the above:\n\n"
                        ">>> import warnings\n"
                        '>>> warnings.filterwarnings("ignore", category=DeprecatedSettingWarning)',
                        DeprecatedSettingWarning,
                    )
                    _Alias.once = True

    def _while_setting_state(self):
        return self._print_newer_api()

    def _while_renaming(self):
        return self._print_newer_api()

    def _while_deleting(self):
        return self._print_newer_api()

    def _while_creating(self):
        return self._print_newer_api()

    def _while_resizing(self):
        return self._print_newer_api()

    def _while_executing_command(self):
        return self._print_newer_api()


def _create_child(cls, name, parent: weakref.CallableProxyType, alias_path=None):
    if alias_path or isinstance(parent, _Alias):
        bases = (cls,)
        # True child of parent alias is already derived from _Alias.
        # Avoiding duplicate derivation and mro resolution issue.
        if _Alias not in cls.__mro__:
            bases = (_Alias, cls)
        alias_cls = type(
            f"{cls.__name__}_alias",
            bases,
            dict(cls.__dict__) | {"alias_path": alias_path},
        )
        return alias_cls(name, parent.__repr__.__self__)
    return cls(name, parent)


@no_runtime_type_check
class SettingsBase(Base, Generic[StateT]):
    """Base class for settings objects.

    Methods
    -------
    get_state()
        Get the current state of the object.

    set_state(state)
        Set the state of the object.
    """

    def __init_subclass__(cls, **kwargs):
        """Enforce correct wiring of the settings-expression protocol.

        A leaf opts into the protocol by declaring ``_expression_kinds``.  Because
        ``SettingsBase`` precedes the behaviour mixins (:class:`Textual`,
        :class:`RealNumerical`) in every leaf's MRO, a bare ``set_state`` resolves
        to :meth:`SettingsBase.set_state`, which stores the value directly and
        *bypasses* expression rendering/validation -- silently serializing an
        expression object with ``str()``.  Such a leaf must therefore route
        ``set_state`` through an expression-aware setter and expose the core
        setter as ``base_set_state``.

        This hook turns that easy-to-forget wiring from a silent runtime bug into
        a loud, immediate failure at class-definition (import) time.
        """
        super().__init_subclass__(**kwargs)
        if getattr(cls, "_expression_kinds", None) is None:
            return
        if cls.set_state is SettingsBase.set_state:
            raise TypeError(
                f"{cls.__name__} declares '_expression_kinds' (opting into the "
                f"settings-expression protocol) but its 'set_state' resolves to "
                f"'SettingsBase.set_state', which bypasses expression handling. "
                f"Wire an expression-aware setter in the class body, e.g.\n"
                f"    base_set_state = SettingsBase[...].set_state\n"
                f"    set_state = RealNumerical.set_state  # or Textual.set_state "
                f"/ _textual_list_set_state"
            )
        if getattr(cls, "base_set_state", None) is not SettingsBase.set_state:
            raise TypeError(
                f"{cls.__name__} routes 'set_state' through an expression-aware "
                f"setter but does not expose the core setter as "
                f"'base_set_state = SettingsBase[...].set_state'. The "
                f"expression-aware setter delegates to 'base_set_state', so it "
                f"must point at 'SettingsBase.set_state'."
            )

    @classmethod
    def to_scheme_keys(cls, value: StateT, root_cls: type, path: list[str]) -> StateT:
        """Convert value to have keys with scheme names.

        This is overridden in the ``Group``, ``NamedObject``, and
        ``ListObject`` classes.  For a leaf, this is the shared conversion path
        reached by direct assignment, :class:`Group` dict updates, and command
        arguments alike, so settings-expression objects are rendered/validated
        here consistently rather than being serialized with ``str()``.
        """
        return _settings_expression_to_scheme(cls, value)

    @classmethod
    def to_python_keys(cls, value: StateT) -> StateT:
        """Convert value to have keys with Python names.

        This is overridden in the ``Group``, ``NamedObject``, and
        ``ListObject`` classes.
        """
        return value

    def __call__(self, *args: StateType, **kwargs: StateType) -> StateT | None:
        """Get or set the state of the object."""
        if kwargs:
            # Send value of the first key only
            if len(kwargs) > 1:
                from ansys.fluent.core.diagnostics.exceptions import PyFluentUserWarning

                warnings.warn(
                    f"Only the first keyword argument is used when setting state at {self.python_path}.",
                    PyFluentUserWarning,
                )
            self.set_state(next(iter(kwargs.values())))
        elif args:
            self.set_state(args)
        else:
            return self.get_state()

    def get_state(self) -> StateT:
        """Get the state of the object."""
        return self.to_python_keys(self.flproxy.get_var(self.path))

    def set_state(self, state: StateT | None = None, **kwargs: StateType) -> None:
        """Set the state of the object."""
        with self._while_setting_state():
            if isinstance(state, (tuple, ansys.units.Quantity)) and hasattr(
                self, "value"
            ):
                self.value.set_state(state, **kwargs)
            else:
                self.flproxy.set_var(
                    self.path,
                    self.to_scheme_keys(
                        kwargs or state,
                        self._root.__class__,
                        _get_python_path_comps(self),
                    ),
                )

    @staticmethod
    def _print_state_helper(state, out, indent=0, indent_factor=2):
        if isinstance(state, dict):
            out.write("\n")
            for key, value in state.items():
                if value is not None:
                    out.write(f'{indent*indent_factor*" "}{key} : ')
                    SettingsBase._print_state_helper(
                        value, out, indent + 1, indent_factor
                    )
        elif isinstance(state, list):
            out.write("\n")
            for index, value in enumerate(state):
                out.write(f'{indent*indent_factor*" "}{index} : ')
                SettingsBase._print_state_helper(value, out, indent + 1, indent_factor)
        else:
            out.write(f"{state}\n")

    def print_state(self, out: TextIO | None = None, indent_factor: int = 2) -> None:
        """Print the state of the object."""
        out = sys.stdout if out is None else out
        self._print_state_helper(self.get_state(), out, indent_factor=indent_factor)

    def state_with_units(self) -> StateT:
        """Get the state of the object with units where available."""
        state = self.get_state()
        if isinstance(self, RealNumerical):
            return (state, self.units())
        elif isinstance(state, collections.abc.Mapping):
            self._add_units_to_state(state)
        return state

    def _add_units_to_state(self, state):
        if isinstance(state, collections.abc.Mapping):
            for k, v in state.items():
                child = None
                if isinstance(self, collections.abc.Mapping):
                    try:
                        child = self[k]
                    except KeyError:
                        pass
                child = child or getattr(self, k, None)
                if child is None:
                    raise RuntimeError(
                        "Unexpected None child {k} encountered while getting units for state."
                    )
                elif isinstance(child, RealNumerical):
                    state[k] = (state[k], child.units())
                else:
                    child._add_units_to_state(state[k])


class Integer(SettingsBase[int], Numerical):
    """An ``Integer`` object representing an integer value setting."""

    _state_type = int


class Real(SettingsBase[RealType], RealNumerical):
    """A ``Real`` object representing a real value setting.

    Some ``Real`` objects also accept string arguments representing
    expression values.
    """

    base_set_state: Callable[..., None] = SettingsBase[RealType].set_state
    set_state: Callable[..., None] = RealNumerical.set_state

    _state_type = RealType


class String(SettingsBase[str], Textual):
    """A ``String`` object representing a string value setting."""

    _state_type = str

    base_set_state: Callable[..., None] = SettingsBase[str].set_state
    set_state: Callable[..., None] = Textual.set_state


class Filename(SettingsBase[str], Textual):
    """A ``Filename`` object representing a file name."""

    _state_type = str

    # ``SettingsBase`` precedes ``Textual`` in the MRO, so a bare ``set_state``
    # would resolve to ``SettingsBase.set_state`` and skip the
    # settings-expression protocol conversion. Keep delegating to that inherited
    # setter, but render/validate an expression object first.
    base_set_state: Callable[..., None] = SettingsBase[str].set_state

    def set_state(self, state: StateT | None = None, **kwargs: StateType) -> None:
        """Set the state of the object.

        Parameters
        ----------
        state
            Either ``str`` or any object implementing the settings-expression
            protocol (``__settings_str__``) -- for example an ``Expr`` produced
            by the expression builder. Expression objects are validated against
            this leaf's accepted kinds before being rendered to their string
            form and stored.
        kwargs : StateType
            Keyword arguments.

        Raises
        ------
        TypeError
            If an expression object's kind is incompatible with this leaf.
        """
        # Expression-object support: an object implementing the
        # settings-expression protocol is validated and rendered to its string
        # form before the inherited setter runs.
        rendered = _render_settings_expression(self, state)
        if rendered is not None:
            return self.base_set_state(state=rendered, **kwargs)
        return self.base_set_state(state=state, **kwargs)

    def file_purpose(self) -> StateType:
        """Specifies whether this file is used as input or output by Fluent."""
        return self.get_attr(_InlineConstants.file_purpose)


class FilenameList(SettingsBase[StringListType], Textual):
    """A FilenameList object represents a list of file names."""

    _state_type = StringListType

    # ``SettingsBase`` precedes ``Textual`` in the MRO, so route expression
    # elements through the protocol before delegating to the inherited setter.
    base_set_state: Callable[..., None] = SettingsBase[StringListType].set_state
    set_state: Callable[..., None] = _textual_list_set_state

    # Each element is an independent expression-string, accepting the same kinds
    # as a scalar :class:`Textual` leaf.
    _element_expression_kinds: tuple[str, ...] = Textual._expression_kinds

    def file_purpose(self) -> StateType:
        """Specifies whether this file is used as input or output by Fluent."""
        return self.get_attr(_InlineConstants.file_purpose)


class FileName(Base):
    """Resolves MRO for child classes."""

    pass


class _InputFile(FileName):
    """Mixin providing upload behavior for settings backed by an input file."""

    def _do_before_execute(self, command_name, value, kwargs):
        file_names = expand_api_file_argument(command_name, value, kwargs)
        if self._file_transfer_handler:
            for file_name in file_names:
                self._file_transfer_handler.upload(file_name=file_name)
            return os.path.basename(value)
        else:
            return value


class _OutputFile(FileName):
    """Mixin providing download behavior for settings backed by an output file."""

    def _do_after_execute(self, command_name, value, kwargs):
        file_names = expand_api_file_argument(command_name, value, kwargs)
        if self._file_transfer_handler:
            for file_name in file_names:
                self._file_transfer_handler.download(file_name=file_name)
            return os.path.basename(value)
        else:
            return value


class _InOutFile(_InputFile, _OutputFile):
    """Mixin providing both upload and download behavior for in/out file settings."""

    pass


class Boolean(SettingsBase[bool], Property):
    """A ``Boolean`` object representing a Boolean value setting."""

    _state_type = bool


class RealList(SettingsBase[RealListType], RealNumerical):
    """A ``RealList`` object representing a real list setting."""

    base_set_state: Callable[..., None] = SettingsBase[RealListType].set_state
    set_state: Callable[..., None] = RealNumerical.set_state

    # A real-list leaf holds a container of reals, so (in addition to the scalar
    # / value-with-units kinds inherited from :class:`RealNumerical`) it also
    # accepts vector-valued expressions.
    _expression_kinds: tuple[str, ...] = ("scalar", "vector", "quantity")

    # Each element of the container is an independent scalar real.
    _element_expression_kinds: tuple[str, ...] = ("scalar", "quantity")

    _state_type = RealListType


class IntegerList(SettingsBase[IntListType], Numerical):
    """An ``Integer`` object representing an integer list setting."""

    _state_type = IntListType


class RealVector(SettingsBase[RealVectorType], Numerical):
    """An object representing a 3D vector.

    A ``RealVector`` object representing a real vector setting
    consisting of three real values.
    """

    _state_type = RealVectorType


class StringList(SettingsBase[StringListType], Textual):
    """A ``StringList`` object representing a string list setting."""

    _state_type = StringListType

    # ``SettingsBase`` precedes ``Textual`` in the MRO, so route expression
    # elements through the protocol before delegating to the inherited setter.
    base_set_state: Callable[..., None] = SettingsBase[StringListType].set_state
    set_state: Callable[..., None] = _textual_list_set_state

    # Each element is an independent expression-string, accepting the same kinds
    # as a scalar :class:`Textual` leaf.
    _element_expression_kinds: tuple[str, ...] = Textual._expression_kinds


class BooleanList(SettingsBase[BoolListType], Property):
    """A ``BooleanList`` object representing a Boolean list setting."""

    _state_type = BoolListType


_type_name_map = {
    (FileName, _InputFile): "InputFilename",
    (FileName, _OutputFile): "OutputFilename",
    (FileName, _InOutFile): "InOutFilename",
    (FilenameList, _InputFile): "InputFilenameList",
    (FilenameList, _OutputFile): "OutputFilenameList",
    (FilenameList, _InOutFile): "InOutFilenameList",
}


@no_runtime_type_check
class Group(SettingsBase[DictStateType]):
    """A ``Group`` container object.

    A ``Group`` object is a container similar to a C++ structure object.
    Child objects can be accessed via attribute access.

    Attributes
    ----------
    child_names: list[str]
        Names of the child objects
    command_names: list[str]
        Names of the commands
    """

    _state_type = DictStateType

    def __init__(self, name: str | None = None, parent: "Base | None" = None):
        """__init__ of Group class."""
        super().__init__(name, parent)
        for child in self.child_names:
            cls = self.__class__._child_classes[child]
            self._setattr(child, _create_child(cls, None, self))
        for cmd in self.command_names:
            cls = self.__class__._child_classes[cmd]
            self._setattr(cmd, _create_child(cls, None, self))
        for query in self.query_names:
            cls = self.__class__._child_classes[query]
            self._setattr(query, _create_child(cls, None, self))

    def __call__(self, *args: StateType, **kwargs: StateType) -> DictStateType | None:
        if kwargs:
            self.set_state(kwargs)
        elif args:
            self.set_state(args)
        else:
            return self.get_state()

    @classmethod
    def to_scheme_keys(
        cls, value: DictStateType, root_cls: type, path: list[str]
    ) -> DictStateType:
        """Convert value to have keys with scheme names.

        Raises
        ------
        ValueError
            If key is invalid.
        """
        if isinstance(value, collections.abc.Mapping):
            ret = {}
            for k, v in value.items():
                if k in cls.child_names:
                    ccls = cls._child_classes[k]
                    ret[ccls.fluent_name] = ccls.to_scheme_keys(v, root_cls, path + [k])
                elif k in cls._child_aliases:
                    alias, scm_alias_name = cls._child_aliases[k]
                    alias_cls, alias_path = _get_class_from_paths(
                        root_cls, path.copy(), alias.split("/")
                    )
                    ret[scm_alias_name] = alias_cls.to_scheme_keys(
                        v, root_cls, alias_path
                    )
                else:
                    raise ValueError("Key '" + str(k) + "' is invalid")
            return ret
        else:
            return value

    @classmethod
    def to_python_keys(cls, value: DictStateType) -> DictStateType:
        """Convert value to have keys with Python names."""
        if isinstance(value, collections.abc.Mapping):
            ret = {}
            undef = object()
            for mname in cls.child_names:
                ccls = cls._child_classes[mname]
                mvalue = value.get(ccls.fluent_name, undef)
                if mvalue is not undef:
                    ret[mname] = ccls.to_python_keys(mvalue)
            return ret
        else:
            return {}

    _child_classes = {}
    child_names: list[str] = []
    command_names: list[str] = []
    query_names: list[str] = []
    _child_aliases = {}

    def get_active_child_names(self) -> list[str]:
        """Names of children that are currently active."""
        ret = []
        child_classes = type(self)._child_classes
        for child_name in self.child_names:
            child_cls = child_classes.get(child_name)
            if child_cls is not None and _is_hidden_by_exposure_level(child_cls, self):
                continue
            child = getattr(self, child_name)
            if child.is_active() and not _is_deprecated(child):
                ret.append(child_name)
        return ret

    def get_active_command_names(self) -> list[str]:
        """Names of commands that are currently active."""
        return _get_active_names(self, self.command_names)

    def get_active_query_names(self) -> list[str]:
        """Names of queries that are currently active."""
        return _get_active_names(self, self.query_names)

    def __dir__(self) -> set[str]:
        dir_list = set(list(self.__dict__.keys()) + dir(type(self)))
        hidden = _get_hidden_names(
            self.child_names + self.command_names + self.query_names,
            type(self)._child_classes,
            self,
        )
        return dir_list - hidden

    def __getattribute__(self, name: str) -> Any:
        # Avoiding server queries for static attributes
        if name in _static_class_attributes:
            return super().__getattribute__(name)
        if (
            name in super().__getattribute__("child_names")
            and self.is_active() is False
        ):
            raise InactiveObjectError(self.python_path)
        _raise_if_exposure_hidden(
            name, super().__getattribute__("_child_classes"), self
        )
        try:
            return super().__getattribute__(name)
        except AttributeError as ex:
            alias = self._child_aliases.get(name)
            if alias is not None:
                alias = alias[0]
                alias_obj = self._child_alias_objs.get(name)
                if alias_obj is None:
                    obj = self.find_object(alias)
                    alias_obj = self._child_alias_objs[name] = _create_child(
                        obj.__class__, None, obj.parent, alias
                    )
                return alias_obj
            error_msg = allowed_name_error_message(
                trial_name=name,
                message=ex.args[0],
                allowed_values=sorted(set(self.child_names + self.command_names)),
            )
            ex.args = (error_msg,)
            raise

    def __setattr__(self, name: str, value: StateType) -> None:
        # 'settings_source' will be set to settings object when they are created from builtin settings classes.
        # We don't allow overwriting it.
        if name == "settings_source":
            raise AttributeError("Cannot overwrite settings_source after it is set.")
        attr = None
        try:
            attr = getattr(self, name)
        except AttributeError as ex:
            error_msg = allowed_name_error_message(
                trial_name=name,
                allowed_values=super().__getattribute__("child_names"),
                message=ex.args[0],
            )
            ex.args = (error_msg,)
            raise
        try:
            return attr.set_state(value)
        except Exception as ex:
            if hasattr(attr, "allowed_values"):
                allowed = attr.allowed_values()
                if allowed and value not in allowed:
                    raise allowed_values_error(name, value, allowed) from ex
            else:
                raise


@no_runtime_type_check
class WildcardPath(Group):
    """Class wrapping a wildcard path to perform get_var and set_var on flproxy."""

    def __init__(
        self,
        flproxy: Any,
        path: str,
        state_cls: type,
        settings_cls: type,
        parent: "Base",
    ):
        """__init__ of WildcardPath class."""
        self._setattr("_flproxy", flproxy)
        self._setattr("_path", path)
        # _state_cls is the settings class at which the state is constructed.
        # _state_cls isn't changed after the first wildcard, i.e.
        # a.b["*"], a.b["*"].c, a.b["*"].c.d["*"] have the same _state_cls.
        # It is used to convert between python and scheme keys within the state.
        self._setattr("_state_cls", state_cls)
        # _settings_cls is the settings cls at the wildcard path level. It is used to
        # construct the scheme path for children.
        self._setattr("_settings_cls", settings_cls)
        self._setattr("_parent", parent)

    @property
    def flproxy(self) -> Any:
        """Proxy object."""
        return self._flproxy

    @property
    def path(self) -> str:
        """Path with wildcards."""
        return self._path

    def __getattr__(self, name: str) -> "WildcardPath":
        try:
            child_settings_cls = self._settings_cls._child_classes[name]
            scheme_name = child_settings_cls.fluent_name
            wildcard_cls = (
                NamedObjectWildcardPath
                if issubclass(child_settings_cls, NamedObject)
                else WildcardPath
            )
            return wildcard_cls(
                self.flproxy,
                self.path + "/" + scheme_name,
                self._state_cls,
                child_settings_cls,
                self,
            )
        except KeyError as ex:
            raise AttributeError(
                allowed_name_error_message(
                    context=self._state_cls._python_name,
                    trial_name=name,
                    allowed_values=self.get_active_child_names(),
                )
            ) from ex

    def items(self) -> Iterator[tuple[str, StateType]]:
        """Items."""
        for key, value in self._parent.items():
            if fnmatch.fnmatch(key, self._path.rsplit(sep="/", maxsplit=1)[-1]):
                yield key, value

    def __iter__(self) -> Iterator[str]:
        for item in self._parent:
            if fnmatch.fnmatch(item, self._path.rsplit(sep="/", maxsplit=1)[-1]):
                yield item

    # Note that following 2 are not symmetric as get_state and set_state
    # are not symmetric.
    # get_state example: a.b["*"].c.d.get_state() == {"<bN>" {"c": {"d": <d_value>}}}
    # set_state example: a.b["*"].set_state({"c": {"d": <d_value>}})

    def to_scheme_keys(
        self, value: StateType, root_cls: type, path: list[str]
    ) -> StateType:
        """Convert value to have keys with scheme names."""
        return self._settings_cls.to_scheme_keys(value, root_cls, path)

    def to_python_keys(self, value: StateType) -> StateType:
        """Convert value to have keys with Python names."""
        return self._state_cls.to_python_keys(value)


class NamedObjectWildcardPath(WildcardPath):
    """WildcardPath at a NamedObject path, so it can be looked up by wildcard again."""

    def __getitem__(self, name: str) -> WildcardPath:
        return WildcardPath(
            self.flproxy,
            self.path + "/" + name,
            self._state_cls,
            self._settings_cls.child_object_type,
            self,
        )

    def __setitem__(self, name: str, value: StateType) -> None:
        self[name].set_state(value)


ChildTypeT = TypeVar("ChildTypeT")


@no_runtime_type_check
class NamedObject(SettingsBase[DictStateType], Generic[ChildTypeT]):
    """A ``NamedObject`` container is a container object similar to a Python dictionary
    object. Generally, many such objects can be created with different names.

    Attributes
    ----------
    command_names: list[str]
        Names of the commands
    """

    # New objects could get inserted by other operations, so we cannot assume
    # that the local cache in self._objects is always up-to-date
    def __init__(self, name: str | None = None, parent: "Base | None" = None):
        """__init__ of NamedObject class."""
        super().__init__(name, parent)
        self._setattr("_objects", {})
        for cmd in self.command_names:
            cls = self.__class__._child_classes[cmd]
            self._setattr(cmd, _create_child(cls, None, self))
        for query in self.query_names:
            cls = self.__class__._child_classes[query]
            self._setattr(query, _create_child(cls, None, self))
        if not hasattr(
            self, "rename"
        ):  # if rename command is not available from settings API
            self._setattr(
                "rename",
                types.MethodType(lambda obj, new, old: _rename(obj, new, old), self),
            )

    @classmethod
    def to_scheme_keys(
        cls, value: DictStateType, root_cls: type, path: list[str]
    ) -> DictStateType:
        """Convert value to have keys with scheme names."""
        if isinstance(value, collections.abc.Mapping):
            ret = {}
            for k, v in value.items():
                ret[k] = cls.child_object_type.to_scheme_keys(v, root_cls, path)
            return ret
        else:
            return value

    @classmethod
    def to_python_keys(cls, value: DictStateType) -> DictStateType:
        """Convert value to have keys with Python names."""
        if isinstance(value, collections.abc.Mapping):
            ret = {}
            for k, v in value.items():
                ret[k] = cls.child_object_type.to_python_keys(v)
            return ret
        else:
            return {}

    _child_classes = {}
    command_names: list[str] = []
    query_names: list[str] = []
    _child_aliases = {}

    def __dir__(self) -> set[str]:
        dir_list = set(list(self.__dict__.keys()) + dir(type(self)))
        hidden = _get_hidden_names(
            self.command_names + self.query_names, type(self)._child_classes, self
        )
        return dir_list - hidden

    def __getattribute__(self, name: str) -> Any:
        if name in _static_class_attributes:
            return super().__getattribute__(name)
        _raise_if_exposure_hidden(
            name, super().__getattribute__("_child_classes"), self
        )
        return super().__getattribute__(name)

    def _create_child_object(self, cname: str):
        ret = self._objects.get(cname)
        if not ret:
            cls = self.__class__.child_object_type
            ret = self._objects[cname] = _create_child(cls, cname, self)
        ret._setattr("_python_name", f'["{cname}"]')
        ret._setattr(
            "rename",
            types.MethodType(lambda obj, name: _rename(self, name, cname), ret),
        )
        return ret

    def _update_objects(self):
        names = self.get_object_names()
        for name in list(self._objects.keys()):
            if name not in names:
                del self._objects[name]
        for name in names:
            if name not in self._objects:
                self._create_child_object(name)

    def __delitem__(self, name: str) -> None:
        with self._while_deleting():
            self.flproxy.delete(self.path, name)
        if name in self._objects:
            del self._objects[name]

    def __contains__(self, name: str) -> bool:
        return name in self.get_object_names()

    def __len__(self) -> int:
        return len(self.keys())

    def __iter__(self) -> Iterator[str]:
        self._update_objects()
        return iter(self._objects)

    def keys(self) -> KeysView[str]:
        """Object names."""
        self._update_objects()
        return self._objects.keys()

    def values(self) -> ValuesView[ChildTypeT]:
        """Object values."""
        self._update_objects()
        return self._objects.values()

    def items(self) -> ItemsView[str, ChildTypeT]:
        """Items."""
        self._update_objects()
        return self._objects.items()

    def user_creatable(self) -> bool:
        """Whether the object is user-creatable."""
        return self.get_attr(_InlineConstants.user_creatable, bool)

    def get_object_names(self) -> list[str]:
        """Object names."""
        obj_names = self.flproxy.get_object_names(self.path)
        obj_names_list = obj_names if isinstance(obj_names, list) else list(obj_names)
        return obj_names_list

    def get_active_command_names(self) -> list[str]:
        """Names of commands that are currently active."""
        return _get_active_names(self, self.command_names)

    def get_active_query_names(self) -> list[str]:
        """Names of queries that are currently active."""
        return _get_active_names(self, self.query_names)

    def __getitem__(self, name: str) -> ChildTypeT:
        if name not in self.get_object_names():
            if self.flproxy.has_wildcard(name):
                child_cls = self.__class__.child_object_type
                # TODO: alias
                return WildcardPath(
                    self.flproxy,
                    self.path + "/" + name,
                    self.__class__,
                    child_cls,
                    self,
                )
            raise KeyError(
                allowed_name_error_message(
                    context=self.python_name,
                    trial_name=name,
                    allowed_values=self.get_object_names(),
                )
            )

        obj = self._objects.get(name)
        if not obj:
            obj = self._create_child_object(name)
        return obj

    def get(self, name: str) -> ChildTypeT:
        """Return the child object by key.

        Parameters
        ----------
        name : str
            Name of the child object.

        Returns
        -------
        ChildTypeT
            Child object.
        """
        try:
            return self.__getitem__(name)
        except Exception:
            return

    def __getattr__(self, name: str) -> Any:
        alias = self._child_aliases.get(name)
        if alias:
            alias = alias[0]
            alias_obj = self._child_alias_objs.get(name)
            if alias_obj is None:
                obj = self.find_object(alias)
                alias_obj = self._child_alias_objs[name] = _create_child(
                    obj.__class__, None, obj.parent, alias
                )
            return alias_obj
        else:
            try:
                return getattr(super(), name)
            except AttributeError as ex:
                raise AttributeError(
                    f"'{self.__class__.__name__}' has no attribute '{name}'"
                ) from ex

    def __add__(self, other: "NamedObject[Any]") -> "CombinedNamedObject":
        if not isinstance(other, NamedObject):
            raise TypeError(
                f"Can only add NamedObject to NamedObject, not {type(other).__name__}"
            )
        return CombinedNamedObject([self, other])

    def list(self) -> Any:
        """Print the object names."""
        if FluentVersion(self._version) >= FluentVersion.v261:
            return self._root.list(object_path=self.path)
        else:
            return self.list_1()

    def list_properties(self, object_name: str) -> Any:
        """Print the properties of the given object name.

        Parameters
        ----------
        object_name : str
            Name of the object whose properties are to be listed.
        """
        if FluentVersion(self._version) >= FluentVersion.v261:
            return self._root.list_properties(object_path=f"{self.path}/{object_name}")
        else:
            return self.list_properties_1(object_name=object_name)


class CombinedNamedObject:
    """A ``CombinedNamedObject`` contains the concatenated named-objects."""

    def __init__(self, objects: list[NamedObject[Any]]):
        """__init__ of CombinedNamedObject."""
        self.objects: list[NamedObject[Any]] = []
        self._items: list[tuple[str, Any]] = []
        for obj in objects:
            if isinstance(obj, CombinedNamedObject):
                self.objects.extend(obj.objects)
            else:
                self.objects.append(obj)
        for obj in self.objects:
            self._items.extend(obj.items())

    def items(self) -> list[tuple[str, Any]]:
        """Return items like a dictionary."""
        return self._items

    def __iter__(self) -> Iterator[Any]:
        for obj in self.objects:
            yield from obj

    def __add__(self, other: NamedObject[Any]) -> "CombinedNamedObject":
        if not isinstance(other, NamedObject):
            raise TypeError(f"Cannot add {type(self)} to NamedObject")
        return CombinedNamedObject(self.objects + [other])

    def __call__(self) -> dict[str, Any]:
        temp_dict = {}
        for obj in self.objects:
            temp_dict.update(obj())
        return temp_dict


def _rename(obj: NamedObject | _Alias, new: str, old: str):
    """Rename a named object.

    Parameters
    ----------
    obj: NamedObject
        named-object to be renamed
    new: str
        New name.
    old : str
        Current name.
    """
    with obj._while_renaming():
        obj.flproxy.rename(obj.path, new, old)
    if old in obj._objects:
        del obj._objects[old]
    obj._create_child_object(new)


def _parse_quantity(path, state):
    """Parse *state* into an ``ansys.units.Quantity``, or return ``None``.

    Accepts either a concrete ``Quantity`` instance or a ``(sequence, units)``
    tuple shorthand.  Raises ``UnhandledQuantity`` if the conversion fails.
    """
    try:
        if isinstance(state, ansys.units.Quantity):
            return state
        if (
            isinstance(state, tuple)
            and len(state) == 2
            and isinstance(state[0], collections.abc.Sequence)
            and not isinstance(state[0], (str, bytes, bytearray))
        ):
            return ansys.units.Quantity(*state)
        return None
    except Exception as ex:
        raise UnhandledQuantity(path, state) from ex


def _materialize_quantity_values(path, state, quantity):
    """Return ``list(quantity.value)``, or raise ``UnhandledQuantity``."""
    try:
        return list(quantity.value)
    except Exception as ex:
        raise UnhandledQuantity(path, state) from ex


def _convert_to_target_units(path, state, quantity, target_units):
    """Convert *quantity* to *target_units* and return a plain ``float`` list.

    Raises ``UnhandledQuantity`` on failure.
    """
    try:
        return [float(v) for v in quantity.to(target_units).value]
    except Exception as ex:
        raise UnhandledQuantity(path, state) from ex


@no_runtime_type_check
class ListObject(SettingsBase[ListStateType], Generic[ChildTypeT]):
    """A ``ListObject`` container is a container object, similar to a Python list
    object. Generally, many such objects can be created.

    Attributes
    ----------
    command_names: list[str]
        Names of the commands.

    Methods
    -------
    get_size()
       Get the size of the list.
    """

    # New objects could get inserted by other operations, so we cannot assume
    # that the local cache in self._objects is always up-to-date
    def __init__(self, name: str | None = None, parent: "Base | None" = None):
        """__init__ of ListObject class."""
        super().__init__(name, parent)
        self._setattr("_objects", [])
        for cmd in self.command_names:
            cls = self.__class__._child_classes[cmd]
            self._setattr(cmd, _create_child(cls, None, self))
        for query in self.query_names:
            cls = self.__class__._child_classes[query]
            self._setattr(query, _create_child(cls, None, self))

    @classmethod
    def to_scheme_keys(
        cls, value: ListStateType, root_cls: type, path: list[str]
    ) -> ListStateType:
        """Convert value to have keys with scheme names."""
        if isinstance(value, collections.abc.Sequence):
            return [
                cls.child_object_type.to_scheme_keys(v, root_cls, path) for v in value
            ]
        else:
            return value

    @classmethod
    def to_python_keys(cls, value: ListStateType) -> ListStateType:
        """Convert value to have keys with scheme names."""
        if isinstance(value, collections.abc.Sequence):
            return [cls.child_object_type.to_python_keys(v) for v in value]
        else:
            return []

    _child_classes = {}
    command_names: list[str] = []
    query_names: list[str] = []
    _child_aliases = {}

    def __dir__(self) -> set[str]:
        dir_list = set(list(self.__dict__.keys()) + dir(type(self)))
        hidden = _get_hidden_names(
            self.command_names + self.query_names, type(self)._child_classes, self
        )
        return dir_list - hidden

    def __getattribute__(self, name: str) -> Any:
        if name in _static_class_attributes:
            return super().__getattribute__(name)
        _raise_if_exposure_hidden(
            name, super().__getattribute__("_child_classes"), self
        )
        return super().__getattribute__(name)

    def _update_objects(self):
        cls = self.__class__.child_object_type
        self._setattr(
            "_objects",
            [_create_child(cls, str(x), self) for x in range(self.get_size())],
        )

    def __len__(self) -> int:
        return self.get_size()

    def __iter__(self) -> Iterator[ChildTypeT]:
        self._update_objects()
        return iter(self._objects)

    def get_active_command_names(self) -> list[str]:
        """Names of commands that are currently active."""
        return _get_active_names(self, self.command_names)

    def get_active_query_names(self) -> list[str]:
        """Names of queries that are currently active."""
        return _get_active_names(self, self.query_names)

    def get_size(self) -> int:
        """Return the number of elements in a list object.

        Returns
        -------
        int
        """
        return self.flproxy.get_list_size(self.path)

    def __getitem__(self, index: int) -> ChildTypeT:
        size = self.get_size()
        if index >= size:
            raise IndexError(index)
        if len(self._objects) != size:
            self._update_objects()
        return self._objects[index]

    def __setitem__(self, index: int, value: StateType) -> None:
        child = self[index]
        child.set_state(value)

    def __getattr__(self, name: str) -> Any:
        alias = self._child_aliases.get(name)
        if alias:
            alias = alias[0]
            alias_obj = self._child_alias_objs.get(name)
            if alias_obj is None:
                obj = self.find_object(alias)
                alias_obj = self._child_alias_objs[name] = _create_child(
                    obj.__class__, None, obj.parent, alias
                )
            return alias_obj
        else:
            return getattr(super(), name)

    def _sync_list_size(self, size: int) -> None:
        # Keep list-object cardinality in sync before the final bulk set.
        if self.get_size() != size:
            with self._while_resizing():
                self.flproxy.resize_list_object(self.path, size)
        if len(self._objects) != size:
            self._update_objects()

    def _resolve_child_units(self, size: int):
        # Return the target units string from the first child, or None.
        if size == 0:
            return None
        child = self[0]
        # First support direct numerical list children.
        if isinstance(child, RealNumerical):
            return child.units()
        # Then support wrapped schemas where units live under .value.
        child_value = getattr(child, "value", None)
        if isinstance(child_value, RealNumerical):
            return child_value.units()
        return None

    def set_state(self, state: StateT | None = None, **kwargs: StateType) -> None:
        """Set the state of the list object.

        For Quantity-like inputs containing sequence values, convert once to the
        child target units (when available) and apply in a single bulk update.

        Raises
        ------
        UnhandledQuantity
            If a Quantity-like input cannot be interpreted or converted to
            target units.
        """
        if kwargs or state is None:
            return super().set_state(state=state, **kwargs)

        quantity = _parse_quantity(self.path, state)
        if quantity is None:
            return super().set_state(state=state, **kwargs)

        values = _materialize_quantity_values(self.path, state, quantity)
        self._sync_list_size(len(values))
        target_units = self._resolve_child_units(len(values))
        if target_units is not None:
            values = _convert_to_target_units(self.path, state, quantity, target_units)
        return super().set_state(state=values, **kwargs)


class Dict(SettingsBase[DictStateType]):
    """A ``Dict`` object representing key-value settings."""

    _state_type = DictStateType


def _get_new_keywords(obj, *args, **kwds):
    newkwds = {}
    unknown_keywords = set()
    # Convert positional arguments to keyword arguments
    if args:
        argNames = obj.argument_names[:]
        for arg in args:
            argName = argNames.pop(0)
            newkwds[argName] = arg
    if kwds:
        # Convert deprecated keywords through aliases
        if FluentVersion(obj._version) >= FluentVersion.v252:
            argument_aliases = {k: v[0] for k, v in obj._child_aliases.items()}
        else:
            # Arguments-aliases was not statically available before v252.
            argument_aliases_scm = obj.get_attr("arguments-aliases") or {}
            argument_aliases = {}
            for k, v in argument_aliases_scm.items():
                argument_aliases[to_python_name(k)] = to_python_name(
                    v.removeprefix("'")
                )
        for k, v in kwds.items():
            alias = argument_aliases.get(k)
            if alias:
                newkwds[alias] = v
            elif k in obj.argument_names:
                newkwds[k] = v
            else:
                unknown_keywords.add(k)
    for k in unknown_keywords:
        # Noisily ignore unknown keywords
        from ansys.fluent.core.diagnostics.exceptions import PyFluentUserWarning

        warnings.warn(
            f"Unknown keyword '{k}' for command '{obj.python_path}'. "
            "It will be ignored.",
            PyFluentUserWarning,
        )
    return newkwds


@no_runtime_type_check
class Action(Base):
    """Intermediate Base class for Command and Query class."""

    _child_classes = {}
    _child_aliases = {}
    argument_names: list[str] = []

    def __init__(self, name: str | None = None, parent: "Base | None" = None):
        """__init__ of Action class."""
        super().__init__(name, parent)
        if hasattr(self, "argument_names"):
            for argument in self.argument_names:
                cls = self.__class__._child_classes[argument]
                self._setattr(argument, _create_child(cls, None, self))

    def __dir__(self) -> set[str]:
        dir_list = set(list(self.__dict__.keys()) + dir(type(self)))
        hidden = _get_hidden_names(self.argument_names, type(self)._child_classes, self)
        return dir_list - hidden

    def __getattribute__(self, name: str) -> Any:
        if name in _static_class_attributes:
            return super().__getattribute__(name)
        _raise_if_exposure_hidden(
            name, super().__getattribute__("_child_classes"), self
        )
        return super().__getattribute__(name)

    def __getattr__(self, name: str) -> Any:
        alias = self._child_aliases.get(name)
        if alias:
            alias = alias[0]
            alias_obj = self._child_alias_objs.get(name)
            if alias_obj is None:
                obj = self.find_object(alias)
                alias_obj = self._child_alias_objs[name] = _create_child(
                    obj.__class__, None, obj.parent, alias
                )
            return alias_obj
        else:
            try:
                return getattr(super(), name)
            except AttributeError:
                raise AttributeError(
                    f"'{self.python_path}' is a command/query object and has no attribute '{name}'"
                ) from None

    def __setattr__(self, name: str, value: StateType) -> None:
        attr = getattr(self, name)
        try:
            return attr.set_state(value)
        except Exception as ex:
            if hasattr(attr, "allowed_values"):
                allowed = attr.allowed_values()
                if allowed and value not in allowed:
                    raise allowed_values_error(name, value, allowed) from ex
            raise


class BaseCommand(Action):
    """Executes command."""

    def _execute_command(self, *args, **kwds):
        """Execute a command with the specified positional and keyword arguments."""
        from ansys.fluent.core.module_config import config

        if self.flproxy.is_interactive_mode():
            prompt = self.flproxy.get_command_confirmation_prompt(
                self._parent.path, self.obj_name, **kwds
            )
            if prompt:
                valid_responses = {"y": True, "yes": True, "n": False, "no": False}
                while True:
                    response = input(prompt + ": y[es]/n[o] ").strip().lower()
                    if response in valid_responses:
                        if not valid_responses[response]:
                            return
                        break
                    else:
                        print("Please enter 'y[es]' or 'n[o]'.")
        with self._while_executing_command():
            if "path" in kwds:
                kwds["path_1"] = kwds.pop("path")
            ret = self.flproxy.execute_cmd(self._parent.path, self.obj_name, **kwds)
            if (
                not config.disable_parameter_list_return_fix
                and FluentVersion(self._version) <= FluentVersion.v252
                and self.path
                in [
                    "parameters/input-parameters/list",
                    "parameters/output-parameters/list",
                ]
            ):
                ret = _fix_parameter_list_return(ret)
            return ret

    def execute_command(self, *args: StateType, **kwds: StateType) -> StateType:
        """Execute command."""
        kwds = _get_new_keywords(self, *args, **kwds)
        # Normalize any settings-expression arguments to their rendered string
        # form *before* the file hooks run. ``before_execute`` / ``after_execute``
        # (and ``expand_api_file_argument``) operate on plain strings, so a
        # protocol object -- e.g. an expression passed as a Filename argument to
        # ``read_case_data`` -- would otherwise raise ``AttributeError`` there.
        # Storing the rendered value back into ``kwds`` reuses it for the scheme
        # conversion and for ``after_execute`` as well.
        for arg in list(kwds):
            kwds[arg] = _settings_expression_to_scheme(getattr(self, arg), kwds[arg])
        scmKwds = {}
        for arg, value in kwds.items():
            argument = getattr(self, arg)
            # Convert path-like values for possible file transfer
            value = argument.before_execute(
                command_name=self.python_name, value=value, kwargs=kwds
            )
            # Convert key-value to Scheme key-value
            scmKwds[argument.fluent_name] = argument.to_scheme_keys(
                value,
                argument._root.__class__,
                _get_python_path_comps(argument),
            )
        ret = self._execute_command(*args, **scmKwds)
        for arg, value in kwds.items():
            argument = getattr(self, arg)
            argument.after_execute(
                command_name=self.python_name, value=value, kwargs=kwds
            )
        if (
            self.obj_name in ["create", "make-a-copy"]
            and isinstance(self._parent, NamedObject)
            and ret in self._parent
        ):
            return self._parent[ret]
        return_t = getattr(self, "return_type", None)
        if return_t:
            base_t = _baseTypes.get(return_t)
            if base_t:
                assert_type(ret, base_t._state_type)
            return ret


# TODO: Remove this after parameter list() method is fixed from Fluent side
def _fix_parameter_list_return(val):
    if isinstance(val, dict):
        new_val = {}
        for name, v in val.items():
            value, units = v
            if len(units) > 0 and isinstance(units[0], str):
                # Symbols are not stripped in the command return in PyConsole.
                # Following code will work in both PyConsole and PyFluent.
                unit = units[0].lstrip("'")
                if unit != "*null*":
                    try:
                        unit_labels = _fix_parameter_list_return.scheme_eval(
                            f"(units/inquire-available-label-strings-for-quantity '{unit})"
                        )
                    except RuntimeError:
                        unit_labels = []
                    unit_label = unit_labels[0] if len(unit_labels) > 0 else ""
                else:
                    unit_label = ""
            else:
                unit_label = ""
            new_val[name] = [value, unit_label]
        return new_val
    return val


_fix_parameter_list_return.scheme_eval = None


class Command(BaseCommand):
    """Command object."""

    def __call__(self, **kwds: Any) -> StateType | None:
        """Call a command with the specified keyword arguments."""
        if not self.is_active():
            raise InactiveObjectError(self.python_path)
        if self.is_read_only():
            raise ReadOnlyActionError(self.python_path)
        try:
            return self.execute_command(**kwds)
        except KeyboardInterrupt:
            self._root._on_interrupt(self)
            raise KeyboardInterrupt
        except RuntimeError as ex:
            # TODO: Remove this Fluent specific logic during later refactoring.
            # RuntimeError("()") is Fluent's gRPC signal for a clean solver stop
            # via interrupt() or via manual stop from a GUI in connected instances.
            # Suppress it for interruptible commands so that
            # workflow code following iterate()/calculate() continues normally.
            _is_interruptible = getattr(self._root, "_is_interruptible_command", None)
            if (
                _is_interruptible is not None
                and ex.args
                and ex.args[0] == "()"
                and _is_interruptible(self)
            ):
                return None
            raise


class CommandWithPositionalArgs(BaseCommand):
    """Command Object supporting positional arguments."""

    def __call__(self, *args: Any, **kwds: Any) -> StateType | None:
        """Call a command with the specified positional and keyword arguments."""
        if not self.is_active():
            raise InactiveObjectError(self.python_path)
        if self.is_read_only():
            raise ReadOnlyActionError(self.python_path)
        try:
            return self.execute_command(*args, **kwds)
        except KeyboardInterrupt:
            self._root._on_interrupt(self)
            raise KeyboardInterrupt
        except RuntimeError as ex:
            # TODO: Remove this Fluent specific logic during later refactoring.
            # RuntimeError("()") is Fluent's gRPC signal for a clean solver stop
            # via interrupt() or via manual stop from a GUI in connected instances.
            # Suppress it for interruptible commands so that
            # workflow code following iterate()/calculate() continues normally.
            _is_interruptible = getattr(self._root, "_is_interruptible_command", None)
            if (
                _is_interruptible is not None
                and ex.args
                and ex.args[0] == "()"
                and _is_interruptible(self)
            ):
                return None
            raise


class Query(Action):
    """Query object."""

    def __call__(self, **kwds: Any) -> StateType | None:
        """Call a query with the specified keyword arguments."""
        if not self.is_active():
            raise InactiveObjectError(self.python_path)
        if self.is_read_only():
            raise ReadOnlyActionError(self.python_path)
        kwds = _get_new_keywords(self, **kwds)
        scmKwds = {}
        for arg, value in kwds.items():
            argument = getattr(self, arg)
            # Convert key-value to Scheme key-value
            scmKwds[argument.fluent_name] = argument.to_scheme_keys(
                value,
                argument._root.__class__,
                _get_python_path_comps(argument),
            )
        return self.flproxy.execute_query(self._parent.path, self.obj_name, **scmKwds)


_baseTypes = {
    "group": Group,
    "integer": Integer,
    "real": Real,
    "string/symbol": String,
    "string": String,
    "boolean": Boolean,
    "real-list": RealList,
    "integer-list": IntegerList,
    "string-list": StringList,
    "boolean-list": BooleanList,
    "named-object": NamedObject,
    "vector": RealVector,
    "command": Command,
    "query": Query,
    "material-property": String,
    "thread-var": String,
    "list-object": ListObject,
    "file": Filename,
    "file-list": FilenameList,
    "dict": Dict,
}


def _clean_helpinfo(helpinfo):
    helpinfo = helpinfo.strip("\n").lstrip(" ")
    if not helpinfo.endswith("."):
        helpinfo += "."
    helpinfo = helpinfo[0].upper() + helpinfo[1:]
    return helpinfo


def _fix_help_info(obj_type, helpinfo):
    # The else clause is just picking "object" due to our current
    # knowledge that the implementation only distinguishes between
    # "method" and everything else. This is fragile.
    api_item_type = "method" if obj_type in ("command", "query") else "object"
    fix = _docstrings._fixed_doc_string(api_item_type, helpinfo)
    return fix or helpinfo


class _ChildNamedObjectAccessorMixin(collections.abc.MutableMapping[str, "Base"]):
    """A mixin class to provide a dictionary interface at a Group class level if the
    Group has multiple named objects of a similar type. For example, boundary conditions
    are grouped by type but quite often we want to access them without the type context.

    The following can be used:
    for name, boundary in setup.boundary_conditions.items():
        print (name, boundary())

    even though actual boundary conditions are stored one level lower to
    boundary_conditions.
    """

    def __getitem__(self, name: str) -> "Base":
        """Get a child object."""
        for cname in self.child_names:
            cobj = getattr(self, cname)
            # Use suppress to ignore exceptions during child object lookup without triggering B110
            # TODO: Investigate why this exception handling is required?
            with suppress(Exception):
                return cobj[name]
        raise KeyError(name)

    def __setitem__(self, name: str, value: StateType) -> None:
        """Set the state of a child object."""
        self[name].set_state(value)

    def __delitem__(self, name: str) -> None:
        """Delete a child object."""
        for cname in self.child_names:
            cobj = getattr(self, cname)
            # Use suppress to ignore exceptions during child object deletion without triggering B110
            # TODO: Investigate why this exception handling is required?
            with suppress(Exception):
                del cobj[name]
                return
        raise KeyError(name)

    def __iter__(self) -> Iterator[str]:
        """Iterator for child named objects."""
        for cname in self.child_names:
            # Use suppress to ignore exceptions during child object iteration without triggering B110
            # TODO: Investigate why this exception handling is required?
            with suppress(Exception):
                for item in getattr(self, cname):
                    yield item

    def __len__(self) -> int:
        """Number of child named objects."""
        count = 0
        for cname in self.child_names:
            cobj = getattr(self, cname)
            if isinstance(cobj, NamedObject):
                count += len(cobj)
        return count


class CreatableNamedObjectMixin(collections.abc.MutableMapping[str, ChildTypeT]):
    """Provides creatable named objects for Fluent 2025 R1 and later."""

    def __setitem__(self, name: str, value: StateType) -> None:
        if name not in self.get_object_names():
            if self.flproxy.has_wildcard(name):
                child = WildcardPath(
                    self.flproxy,
                    self.path + "/" + name,
                    self.__class__,
                    self.__class__.child_object_type,
                    self,
                )
            else:
                with self._while_creating():
                    self.flproxy.create(self.path, name)
                child = self._create_child_object(name)
        else:
            child = self._objects.get(name)
            if not child:
                child = self._create_child_object(name)
        child.set_state(value)


class CreatableNamedObjectMixinOld(CreatableNamedObjectMixin[ChildTypeT]):
    """Provides creatable named objects for Fluent 2024 R2 and earlier."""

    # In Fluent 2025 R1, the ``create()`` method is available as commands in the ``NamedObject`` class.
    def create(self, name: str = "") -> ChildTypeT:
        """Create a named object.

        Parameters
        ----------
        name: str
            Name of the new object.

        Returns
        -------
        Object
            Object that has been created.
        """
        with self._while_creating():
            self.flproxy.create(self.path, name)
        return self._create_child_object(name)


class _NonCreatableNamedObjectMixin(collections.abc.MutableMapping[str, ChildTypeT]):
    def __setitem__(self, name: str, value: StateType) -> None:
        if name not in self.get_object_names():
            if self.flproxy.has_wildcard(name):
                child = WildcardPath(
                    self.flproxy,
                    self.path + "/" + name,
                    self.__class__,
                    self.__class__.child_object_type,
                    self,
                )
            else:
                raise KeyError(
                    allowed_name_error_message(
                        context=self.python_name,
                        trial_name=name,
                        allowed_values=self.get_object_names(),
                    )
                )
        else:
            child = self._objects.get(name)
            if not child:
                child = self._create_child_object(name)
        child.set_state(value)


class AllowedValuesMixin:
    """Provides allowed values."""

    def allowed_values(self) -> list[StateType] | str:
        """Get the allowed values of the object."""
        try:
            return self.get_attr(_InlineConstants.allowed_values, (list, str))
        except Exception:
            return []


class _MaybeActiveString(str):
    """A string class with an is_active() method."""

    def __new__(cls, value, is_active: Callable[[], bool]):
        return super().__new__(cls, value)

    def __init__(self, value, is_active: Callable[[], bool]):
        super().__init__()
        self.is_active = is_active


class _FlStringConstant:
    """A descriptor class to hold a constant string value."""

    def __init__(self, value):
        self._value = value

    def __get__(self, instance, owner):
        def is_active():
            return self._value in instance.allowed_values()

        return _MaybeActiveString(self._value, is_active=is_active)

    def __set__(self, instance, value):
        raise AttributeError("Cannot set a constant value.")


_bases_by_class = {}


def _resolve_base_class(name: str, obj_type: str):
    """Resolve the base class for a settings API node."""
    base = _baseTypes.get(obj_type)
    if obj_type == "command" and name in ["create", "rename", "delete", "resize"]:
        base = CommandWithPositionalArgs
    if base is None:
        settings_logger.warning(
            f"Unable to find base class for '{name}' "
            f"(type = '{obj_type}'). "
            f"Falling back to String."
        )
        base = String
    return base


def _set_generated_docstring(dct: dict, info: dict, obj_type: str, parent, pname: str):
    """Set the generated docstring for a runtime settings class."""
    helpinfo = info.get("help")
    if helpinfo:
        dct["__doc__"] = _fix_help_info(obj_type, _clean_helpinfo(helpinfo))
    elif parent is None:
        dct["__doc__"] = "'root' object."
    elif obj_type == "command":
        dct["__doc__"] = f"'{pname.strip('_')}' command."
    elif obj_type == "query":
        dct["__doc__"] = f"'{pname.strip('_')}' query."
    else:
        dct["__doc__"] = f"'{pname.strip('_')}' child."


def _augment_generated_bases(
    base,
    info: dict,
    obj_type: str,
    version: str | None,
    include_child_named_objects: bool,
    user_creatable: bool,
) -> tuple[type, ...]:
    """Compute mixin-augmented bases for the generated class."""
    bases = (base,)
    if include_child_named_objects:
        bases = bases + (_ChildNamedObjectAccessorMixin,)
    if obj_type == "named-object" and user_creatable:
        if version is not None and version < "251":
            bases = bases + (CreatableNamedObjectMixinOld,)
        else:
            bases = bases + (CreatableNamedObjectMixin,)
    elif obj_type == "named-object":
        bases = bases + (_NonCreatableNamedObjectMixin,)
    elif info.get("has_allowed_values"):
        bases += (AllowedValuesMixin,)
    elif info.get("file_purpose") == "input":
        bases += (_InputFile,)
    elif info.get("file_purpose") == "output":
        bases += (_OutputFile,)
    elif info.get("file_purpose") == "inout":
        bases += (_InOutFile,)
    return bases


def _resolve_generated_names(
    pname: str,
    bases: tuple[type, ...],
    file_purpose: str | None,
    parent_taboo: set | None,
) -> tuple[str, str]:
    """Resolve generated class name and parent attribute name."""
    original_pname = pname
    i = 1
    if parent_taboo:
        while pname in parent_taboo:
            pname = f"{original_pname}_{i}"
            i += 1
    parent_attr_name = pname
    if file_purpose:  # not generalizing for performance
        while pname in _bases_by_class and _bases_by_class[pname] != bases:
            pname = f"{original_pname}_{i}"
            i += 1
        _bases_by_class[pname] = bases
    if parent_taboo:
        parent_taboo.add(pname)
    return pname, parent_attr_name


def _set_generated_exposure_level(cls, parent, info: dict, fluent_path: str = ""):
    """Set class exposure level based on static info, overrides, and parent level.

    Parameters
    ----------
    cls : type
        The class being generated.
    parent : type or None
        The parent class (None if root).
    info : dict
        Static info dict for this class.
    fluent_path : str
        Optional pre-computed Fluent-name path for override lookup.
        If empty, will be reconstructed from the parent chain and current fluent_name.
    """
    # If root, set it to stable
    if parent is None:
        cls.exposure_level = ExposureLevel.STABLE
        return

    # Get the effective exposure level, applying overrides if found
    override_level = _get_override_exposure_level(cls, parent, info, fluent_path)

    # Use override if found, otherwise use server-reported level
    exposure_level_str = info.get("api_exposure_level")
    if override_level is not None:
        # Override found and applied
        effective_server = override_level
    elif exposure_level_str is None:
        # No server level and no override, inherit from parent
        effective_server = parent.exposure_level
    else:
        # Use server-reported level
        effective_server = ExposureLevel(exposure_level_str)

    # Combine with parent constraint: child can't be stricter than parent
    cls.exposure_level = min(effective_server, parent.exposure_level)


def _get_override_exposure_level(
    cls, parent, info: dict, fluent_path: str = ""
) -> ExposureLevel | None:
    """Look up the exposure level override for this class, if any.

    Parameters
    ----------
    cls : type
        The class being generated.
    parent : type or None
        The parent class.
    info : dict
        Static info dict for this class.
    fluent_path : str
        Pre-computed dotted fluent path (e.g., "setup.materials.database").

    Returns
    -------
    ExposureLevel or None
        The override level if found, or None if no override.
        Returning None when no override is found signals that the override
        should not affect the exposure level computation.
    """
    try:
        from ansys.fluent.core.solver import exposure_overrides
        from ansys.fluent.core.utils.fluent_version import FluentVersion

        version = info.get("version") or getattr(cls, "_version", "") or ""
        fluent_version = FluentVersion(version) if version else FluentVersion.v271

        if not fluent_path:
            return None

        # Look up in the overrides data
        if fluent_path in exposure_overrides.DATA:
            override_entry = exposure_overrides.DATA[fluent_path]

            # Check if entry is version-keyed (dict) or fixed (ExposureLevel)
            if isinstance(override_entry, dict):
                for version_predicate, override_level in override_entry.items():
                    # Version predicates are callables that check against fluent_version
                    if version_predicate(fluent_version):
                        return override_level
                # No matching version, no override applies
                return None
            else:
                return override_entry

        return None
    except (ImportError, AttributeError, ValueError):
        # If anything goes wrong with overrides, return None (no override)
        return None


def _set_generated_deprecated_version(cls, info: dict):
    """Set deprecation metadata for generated class."""
    deprecated_version = info.get("deprecated_version", None)
    if deprecated_version and float(deprecated_version) >= 22.2:
        cls._deprecated_version = deprecated_version
    else:
        cls._deprecated_version = ""


def _get_generation_taboo(cls, version: str | None) -> set[str]:
    """Get taboo names used while generating descendants of ``cls``."""
    taboo = set(dir(cls))
    if version and version >= "261":
        taboo -= {"list", "list_properties"}
    taboo |= {
        "child_names",
        "command_names",
        "query_names",
        "argument_names",
        "child_object_type",
    }
    return taboo


def _process_generated_children(info_dict, names, cls, taboo, version, doc_parts=None):
    """Generate child classes and register them on ``cls``."""
    for cname, cinfo in info_dict.items():
        ccls, parent_attr_name = get_cls(
            cname, cinfo, cls, version=version, parent_taboo=taboo
        )

        if doc_parts is not None:
            th = ccls._state_type
            th = th.__name__ if hasattr(th, "__name__") else str(th)
            doc_parts.append(f"    {ccls.__name__} : {th}\n")
            doc_parts.append(f"        {ccls.__doc__}\n")

        names.append(parent_attr_name)
        taboo.add(ccls.__name__)
        cls._child_classes[parent_attr_name] = ccls


def _register_generated_children_section(cls, info: dict, taboo: set[str], version):
    """Populate child names/classes on ``cls`` from static info."""
    children = info.get("children")
    if not children:
        return
    taboo.add("child_names")
    cls.child_names = []
    _process_generated_children(children, cls.child_names, cls, taboo, version)


def _register_generated_commands_section(
    cls, info: dict, taboo: set[str], version, user_creatable: bool
):
    """Populate command names/classes on ``cls`` from static info."""
    commands = info.get("commands")
    if not commands:
        return
    commands.pop("exit", None)
    if not user_creatable:
        commands.pop("create", None)
    if not commands:
        return
    cls.command_names = []
    _process_generated_children(commands, cls.command_names, cls, taboo, version)


def _register_generated_queries_section(cls, info: dict, taboo: set[str], version):
    """Populate query names/classes on ``cls`` from static info."""
    queries = info.get("queries")
    if not queries:
        return
    cls.query_names = []
    _process_generated_children(queries, cls.query_names, cls, taboo, version)


def _register_generated_arguments_section(cls, info: dict, taboo: set[str], version):
    """Populate argument names/classes and parameter docs on ``cls``."""
    arguments = info.get("arguments")
    if not arguments:
        return
    doc_parts = [cls.__doc__, "\n\n", "Parameters\n", "----------\n"]
    cls.argument_names = []
    _process_generated_children(
        arguments,
        cls.argument_names,
        cls,
        taboo,
        version,
        doc_parts=doc_parts,
    )
    cls.__doc__ = "".join(doc_parts)


def _set_generated_return_type(cls, info: dict, version: str | None):
    """Set return type metadata for generated command/query classes."""
    if version == "":
        # This is kept for backwards compatibility.
        cls.return_type = "object"
        return
    return_type = info.get("return_type")
    if return_type:
        cls.return_type = return_type


def _set_generated_child_object_type(cls, info: dict, version: str | None):
    """Set child object type metadata for container classes."""
    object_type = info.get("object_type", False)
    if not object_type:
        return
    cls.child_object_type, _ = get_cls(
        "child-object-type", object_type, cls, version=version
    )
    cls.child_object_type.get_name = lambda self: self._name


def _set_generated_aliases(cls, info: dict):
    """Set consolidated alias metadata on generated classes."""
    child_aliases = info.get("child_aliases", {})
    command_aliases = info.get("command_aliases", {})
    query_aliases = info.get("query_aliases", {})
    arguments_aliases = info.get("arguments_aliases", {})
    if not (child_aliases or command_aliases or query_aliases or arguments_aliases):
        return
    cls._child_aliases = {}
    # No need to differentiate in the Python implementation.
    for k, v in (
        child_aliases | command_aliases | query_aliases | arguments_aliases
    ).items():
        # Storing the original name as we don't have any other way
        # to recover it at runtime.
        cls._child_aliases[to_python_name(k)] = (
            "/".join(x if x == ".." else to_python_name(x) for x in v.split("/")),
            k,
        )


def _set_generated_allowed_values(cls, info: dict):
    """Attach allowed-value constants and cached allowed-values list."""
    allowed_values = info.get("allowed_values", [])
    if not allowed_values:
        return
    for allowed_value in allowed_values:
        setattr(
            cls,
            to_constant_name(allowed_value),
            _FlStringConstant(allowed_value),
        )
    cls._allowed_values = allowed_values


def _set_generated_migration_adapter(cls, info: dict):
    """Mark generated classes that support migration adapters."""
    has_migration_adapter = info.get("has_migration_adapter", False)
    if has_migration_adapter:
        cls._has_migration_adapter = True


def _build_fluent_path(name: str, parent) -> str:
    """Build the dotted fluent path for a class being generated.

    Parameters
    ----------
    name : str
        The fluent name of the class being created (empty string for root).
    parent : type or None
        The parent class.

    Returns
    -------
    str
        Dotted fluent path, e.g., "setup.materials.database"
    """
    if parent is None:
        return ""  # Root has no path

    path_parts = []
    # Walk up parent chain using fluent_name
    node = parent
    while node is not None:
        fname = getattr(node, "fluent_name", "")
        if fname:
            path_parts.insert(0, fname)
        # Check if parent has a way to get its parent (not standard, but try)
        node = getattr(node, "_parent_class", None)

    # Add current name
    if name:
        path_parts.append(name)

    return ".".join(path_parts)


def _create_generated_class(
    name: str,
    info: dict,
    parent,
    version: str | None,
    parent_taboo: set | None,
) -> tuple[type, str, set[str], bool]:
    """Build the base generated class and return context for further registration."""
    pname = "root" if name == "" else to_python_name(name)
    obj_type = info["type"]
    base = _resolve_base_class(name, obj_type)
    dct = {"fluent_name": name, "_version": version}
    _set_generated_docstring(dct, info, obj_type, parent, pname)

    include_child_named_objects = info.get("include_child_named_objects", False)
    user_creatable = info.get("user_creatable", False)

    bases = _augment_generated_bases(
        base,
        info,
        obj_type,
        version,
        include_child_named_objects,
        user_creatable,
    )

    pname, parent_attr_name = _resolve_generated_names(
        pname,
        bases,
        info.get("file_purpose"),
        parent_taboo,
    )

    dct["_child_classes"] = {}
    dct["_parent_class"] = parent  # Store reference to parent class for path building
    cls = type(pname, bases, dct)

    fluent_path = _build_fluent_path(name, parent)
    _set_generated_exposure_level(cls, parent, info, fluent_path)
    _set_generated_deprecated_version(cls, info)

    taboo = _get_generation_taboo(cls, version)
    return cls, parent_attr_name, taboo, user_creatable


# pylint: disable=missing-raises-doc
def get_cls(
    name: str,
    info: dict[str, Any],
    parent: type | None = None,
    version: str | None = None,
    parent_taboo: set[str] | None = None,
) -> tuple[type, str]:
    """Create a class for the object identified by "path"."""
    try:
        cls, parent_attr_name, taboo, user_creatable = _create_generated_class(
            name,
            info,
            parent,
            version,
            parent_taboo,
        )

        _register_generated_children_section(cls, info, taboo, version)
        _register_generated_commands_section(cls, info, taboo, version, user_creatable)
        _register_generated_queries_section(cls, info, taboo, version)
        _register_generated_arguments_section(cls, info, taboo, version)

        _set_generated_return_type(cls, info, version)
        _set_generated_child_object_type(cls, info, version)
        _set_generated_aliases(cls, info)
        _set_generated_allowed_values(cls, info)
        _set_generated_migration_adapter(cls, info)

    except Exception:
        print(
            f"Unable to construct class for '{name}' of "
            f"'{parent.fluent_name if parent else None}'"
        )
        raise
    return cls, parent_attr_name


def _gethash(obj_info):
    dhash = hashlib.sha256()
    dhash.update(pickle.dumps(obj_info))
    return dhash.hexdigest()


def get_root(
    flproxy: Any,
    version: str = "",
    interrupt: Any | None = None,
    is_interruptible_command: Callable[[str], bool] | None = None,
    file_transfer_service: "FileTransferStrategy | None" = None,
    scheme_eval: Callable[[str], StateType] | None = None,
) -> Group:
    """Get the root settings object.

    Parameters
    ----------
    flproxy: Proxy
        Object that interfaces with the Fluent backend.
    interrupt: optional
        To interrupt interruptible commands.
    is_interruptible_command : optional
        Callable ``(command) -> bool`` that returns True when *command* is an
        interruptible solver command (iterate, calculate, dual-time-iterate).
        Used to suppress the ``RuntimeError("()")`` that Fluent returns via
        gRPC when the solver is stopped cleanly by ``interrupt()``.
    file_transfer_service : optional
        File transfer service. Uploads/downloads files to/from the server.
    scheme_eval : Callable[[str], StateType], optional
        A gRPC service to execute Scheme code.
    version : str
        Fluent version.

    Returns
    -------
    root object
        The top-level :ref:`settings root <ref_root>` used to access the Fluent
        settings hierarchy.

    Raises
    ------
    RuntimeError
        If hash values are inconsistent.
    """
    from ansys.fluent.core.module_config import config
    from ansys.fluent.core.utils import load_module as _load_module

    if config.use_runtime_python_classes:
        obj_info = flproxy.get_static_info()
        root_cls, _ = get_cls("", obj_info, version=version)
    else:
        try:
            import ansys.fluent.core as pyfluent

            version_dir = pyfluent.codegen.get_codegen_version_dir(
                version, config.codegen_outdir
            )
            settings = _load_module(
                f"settings_{version}",
                version_dir / "solver" / "settings.py",
            )
            root_cls = settings.root
        except FileNotFoundError:
            obj_info = flproxy.get_static_info()
            root_cls, _ = get_cls("", obj_info, version=version)
    root = root_cls()
    root.set_flproxy(flproxy)
    root._set_on_interrupt(interrupt)
    if is_interruptible_command is not None:
        root._set_is_interruptible_command(is_interruptible_command)
    root._set_file_transfer_service(file_transfer_service)
    _Alias.scheme_eval = scheme_eval
    _fix_parameter_list_return.scheme_eval = scheme_eval
    default_level_str = config.default_exposure_level.lower()
    default_level = ExposureLevel(default_level_str)
    root._setattr("_global_exposure_level", default_level)
    root._setattr("set_exposure_level", types.MethodType(_set_exposure_level, root))
    root._setattr("_file_transfer_service", file_transfer_service)
    return root


def find_children(obj: Any, identifier: str = "*") -> list[str]:
    """Returns path of all the child objects matching an identifier.

    Parameters
    ----------
    obj: Object
        Object whose children need to be queried.
    identifier: str
        Identifier to find specific children.

    Returns
    -------
    list
    """
    list_of_children = []
    _list_children(obj.__class__, identifier, [], list_of_children)
    return list_of_children


def _list_children(cls, identifier, path, list_of_children):
    if issubclass(cls, (NamedObject, ListObject)):
        if hasattr(cls.child_object_type, "child_names"):
            _get_child_path(cls.child_object_type, path, identifier, list_of_children)
    if issubclass(cls, Group):
        _get_child_path(cls, path, identifier, list_of_children)


def _get_child_path(cls, path, identifier, list_of_children):
    for name in cls.child_names:
        path.append(name)
        if fnmatch.fnmatch(name, identifier):
            path_to_append = "/".join(path)
            if path_to_append not in list_of_children:
                list_of_children.append(path_to_append)
        _list_children(cls._child_classes[name], identifier, path, list_of_children)
        path.pop()
