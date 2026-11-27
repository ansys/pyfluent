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

"""Type-checking utilities for PyFluent.

Provides decorators and helpers for marking objects to skip runtime type-checking
by external checkers like beartype and typeguard.
"""

__all__ = ("no_runtime_type_check",)


def _mark(obj) -> None:
    try:
        obj.__no_type_check__ = True
    except (AttributeError, TypeError):
        # Some objects (e.g. generic aliases) reject attribute assignment.
        pass


def _mark_class(cls: type) -> None:
    # beartype.claw decorates each member separately and only reads the flag on
    # the function itself, so the members must be flagged as well as the class.
    for member in list(vars(cls).values()):
        if isinstance(member, (classmethod, staticmethod)):
            _mark(member.__func__)
        elif isinstance(member, property):
            for accessor in (member.fget, member.fset, member.fdel):
                if accessor is not None:
                    _mark(accessor)
        elif isinstance(member, type):
            if member.__qualname__.startswith(f"{cls.__qualname__}."):
                _mark_class(member)
        elif callable(member) and hasattr(member, "__code__"):
            _mark(member)
    _mark(cls)


def no_runtime_type_check(obj):
    """Exclude an object from runtime type-checking by external checkers.

    Sets ``__no_type_check__ = True``, the flag set by :func:`typing.no_type_check`
    and honored by checkers such as beartype and typeguard. For a class, the flag is
    also set on its own methods, class and static methods, property accessors and
    nested classes. For a ``classmethod`` or ``staticmethod`` object, the flag is set
    on the underlying function, so the decorator works in either stacking order.

    This is used for PyFluent proxy classes (Base, SettingsBase, Group, etc.) that
    rely on dynamic ``__getattr__``/``__setattr__`` proxying or are parameterized
    generics, and for callables whose hints cannot be resolved at runtime.

    Parameters
    ----------
    obj
        Object to mark (function, class, method, etc.).

    Returns
    -------
    obj
        The input object unchanged.

    Examples
    --------
    >>> from typing import Generic, TypeVar
    >>> from ansys.fluent.core._type_checking import no_runtime_type_check
    >>> T = TypeVar("T")
    >>> @no_runtime_type_check
    ... class MyClass(Generic[T]):
    ...     pass
    """
    if isinstance(obj, type):
        _mark_class(obj)
    elif isinstance(obj, (classmethod, staticmethod)):
        _mark(obj.__func__)
        _mark(obj)
    else:
        _mark(obj)
    return obj
