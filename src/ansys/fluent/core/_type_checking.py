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

"""Runtime type-checking support for PyFluent.

This module is the single integration point for the third-party runtime
type-checking library, so that the library can be swapped without touching any
call site. ``beartype`` is the default backend.

Runtime type-checking is **disabled by default**. It is activated by setting the
``PYFLUENT_RUNTIME_TYPE_CHECKING`` environment variable to ``"1"`` before
importing PyFluent, and is reflected by
:attr:`ansys.fluent.core.config.runtime_type_checking`.

Notes
-----
The hook has to be installed before any PyFluent submodule is imported, because
it works by transforming module source at import time. Modules which are
already imported are never checked. This is why the switch is read from the
environment here instead of from the configuration object, which itself lives in
a PyFluent submodule.

This module must only depend on the standard library so that it can be imported
as the very first statement of ``ansys.fluent.core``.
"""

from collections.abc import Callable
import os
import typing
import warnings

__all__ = (
    "ENV_VAR",
    "PACKAGE_NAME",
    "install_import_hook",
    "is_type_checking_enabled",
    "no_runtime_type_check",
    "runtime_type_check",
)

#: Environment variable which activates runtime type-checking.
ENV_VAR = "PYFLUENT_RUNTIME_TYPE_CHECKING"

#: Package whose submodules are type-checked at import time.
#:
#: ``ansys`` and ``ansys.fluent`` are :pep:`420` namespace packages, so the
#: package has to be named explicitly. ``beartype_this_package()`` must not be
#: used here: it derives its target from the parent of ``__name__``, which
#: resolves to the ``ansys.fluent`` namespace package and fails.
PACKAGE_NAME = "ansys.fluent.core"

#: Name of the active backend.
BACKEND = "beartype"

_HOOK_INSTALLED = False

T = typing.TypeVar("T")


def _beartype_install_hook() -> bool:
    """Install the ``beartype`` import hook on the PyFluent package."""
    from beartype import BeartypeConf
    from beartype.claw import beartype_package

    beartype_package(
        PACKAGE_NAME,
        conf=BeartypeConf(
            # Do not check :pep:`526` annotated variable assignments. Only
            # callable parameters and return values are checked.
            claw_is_pep526=False,
        ),
    )
    return True


def _beartype_decorator(obj: T) -> T:
    """Apply the ``beartype`` decorator to ``obj``."""
    from beartype import beartype

    return beartype(obj)


def _no_op_install_hook() -> bool:
    """Do not install any import hook."""
    return False


def _no_op_decorator(obj: T) -> T:
    """Return ``obj`` unchanged."""
    return obj


#: Supported backends. Each entry maps a backend name to its import-hook
#: installer and its decorator, which is the only pair of operations the rest of
#: PyFluent relies on.
_BACKENDS: dict[str, dict[str, Callable]] = {
    "beartype": {
        "install_hook": _beartype_install_hook,
        "decorator": _beartype_decorator,
    },
    "none": {
        "install_hook": _no_op_install_hook,
        "decorator": _no_op_decorator,
    },
}


def is_type_checking_enabled() -> bool:
    """Whether runtime type-checking is active in the current process.

    Returns
    -------
    bool
        ``True`` if the import hook has been installed.
    """
    return _HOOK_INSTALLED


def install_import_hook() -> bool:
    """Install the runtime type-checking import hook.

    This is a no-op unless the ``PYFLUENT_RUNTIME_TYPE_CHECKING`` environment
    variable is set to ``"1"``. It never raises: if the backend is not
    installed, a warning is emitted and type-checking stays disabled.

    Returns
    -------
    bool
        ``True`` if the hook was installed by this call.
    """
    global _HOOK_INSTALLED
    if _HOOK_INSTALLED:
        return False
    if os.environ.get(ENV_VAR) != "1":
        return False
    try:
        _HOOK_INSTALLED = _BACKENDS[BACKEND]["install_hook"]()
    except ImportError:
        warnings.warn(
            f"{ENV_VAR} is set but the '{BACKEND}' package is not installed, so "
            "runtime type-checking is disabled. Install it with "
            "'pip install ansys-fluent-core[type-checking]'.",
            UserWarning,
        )
        _HOOK_INSTALLED = False
    return _HOOK_INSTALLED


def runtime_type_check(obj: T) -> T:
    """Type-check the annotations of ``obj`` at runtime.

    Use this decorator for objects which the import hook cannot reach, such as
    classes created dynamically. It is a no-op when runtime type-checking is
    disabled.

    Parameters
    ----------
    obj : Callable or type
        Object to type-check.

    Returns
    -------
    Callable or type
        The type-checked object, or ``obj`` unchanged when disabled.
    """
    if not _HOOK_INSTALLED:
        return obj
    return _BACKENDS[BACKEND]["decorator"](obj)


def no_runtime_type_check(obj: T) -> T:
    """Exclude ``obj`` from runtime type-checking.

    Use this decorator on objects whose annotations cannot be evaluated at
    runtime, for instance because they refer to names which only exist under
    :data:`typing.TYPE_CHECKING`.

    Parameters
    ----------
    obj : Callable or type
        Object to exclude.

    Returns
    -------
    Callable or type
        ``obj``, marked as excluded.
    """
    return typing.no_type_check(obj)
