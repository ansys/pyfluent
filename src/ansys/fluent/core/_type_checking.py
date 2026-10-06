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


def no_runtime_type_check(obj):
    """Apply no_runtime_type_check safely, ignoring attribute errors on generic aliases.

    Sets ``__no_type_check__ = True`` on the object to signal type-checkers to skip it.
    In Python 3.10+, some objects like ``GenericAlias`` don't support setting this
    attribute directly. This wrapper catches those errors gracefully.

    This is used for PyFluent proxy classes (Base, SettingsBase, Group, etc.) that
    rely on dynamic ``__getattr__``/``__setattr__`` proxying or are parameterized
    generics, which most runtime type-checkers cannot check safely.

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
    try:
        obj.__no_type_check__ = True
    except (AttributeError, TypeError):
        # Object doesn't support attribute assignment (e.g., generic alias)
        # This is safe behavior—return the object unchanged
        pass
    return obj
