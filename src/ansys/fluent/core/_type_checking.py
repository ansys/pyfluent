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

"""Mark PyFluent objects to skip runtime type-checking.

PyFluent ships type annotations but does not auto-install type-checkers.
Users apply their own checker (e.g., ``beartype.claw`` or ``typeguard``)
and can mark incompatible objects with :func:`no_runtime_type_check`.

Example::

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

    Uses :func:`typing.no_type_check` to mark an object so type-checkers skip it.

    Parameters
    ----------
    obj
        Object to mark (function, class, method, etc.).

    Returns
    -------
    obj
        The input object unchanged.
    """
    import typing

    try:
        typing.no_type_check(obj)
    except (AttributeError, TypeError, ValueError):
        # Object doesn't support attribute assignment, return unchanged
        pass

    return obj
