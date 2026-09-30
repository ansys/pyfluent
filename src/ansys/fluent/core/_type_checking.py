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

"""Support for marking PyFluent objects as incompatible with runtime type-checking.

PyFluent does not install or activate any runtime type-checker itself. Users who
want runtime type-checking apply their own checker (e.g. ``beartype.claw`` or
``typeguard``'s import hook) across their own environment, the same way they
would for any other dependency, for example::

    from beartype.claw import beartype_package

    beartype_package("ansys.fluent.core")

    import ansys.fluent.core

Note that ``ansys`` and ``ansys.fluent`` are :pep:`420` namespace packages, so
``beartype_this_package()`` cannot be used for this: it derives its target from
the parent of ``__name__``, which resolves to the ``ansys.fluent`` namespace
package and fails. Call ``beartype_package("ansys.fluent.core")`` (or the
equivalent for another checker) explicitly instead.

Some PyFluent classes rely on dynamic ``__getattr__``/``__setattr__`` proxying or
are parameterized generics, which most runtime type-checkers cannot check
safely. :func:`no_runtime_type_check` marks such objects so that any checker a
user applies skips them.
"""

__all__ = ("no_runtime_type_check",)


def no_runtime_type_check(obj):
    """Disable runtime type-checking for an object.

    Marks an object so that beartype (or other type-checking backends) skip
    validation. This is useful for disabling type-checks on specific callables
    or classes that may cause issues with type-checking or have incompatible
    type annotations.

    This function directly sets the ``__no_type_check__`` attribute that beartype
    and other type-checking libraries recognize, without relying on the standard
    library's :func:`typing.no_type_check` which has issues with generic class
    definitions.

    Parameters
    ----------
    obj : Callable, type, or object
        Object to mark for skipping runtime type-checking. Can be a function,
        class, method, or other callable.

    Returns
    -------
    Callable, type, or object
        The input object unchanged, or with the ``__no_type_check__`` attribute
        set if the object supports attribute assignment.

    Notes
    -----
    Objects that cannot have attributes assigned (e.g., types.GenericAlias,
    built-in types) are returned unchanged. This is acceptable because these
    objects are typically not directly callable or type-checkable anyway.
    """
    import types

    # Skip GenericAlias objects (e.g., SettingsBase[DictStateType])
    # as they don't support attribute assignment
    if isinstance(obj, types.GenericAlias):
        return obj

    # Try to set __no_type_check__ directly on objects that support it
    # Skip objects that don't support attribute assignment
    if hasattr(obj, "__dict__") or isinstance(obj, type):
        try:
            obj.__no_type_check__ = True  # type: ignore[attr-defined]
        except (AttributeError, TypeError):
            # Object doesn't support attribute assignment, return unchanged
            # This is acceptable - such objects typically aren't type-checkable anyway
            pass

    return obj
