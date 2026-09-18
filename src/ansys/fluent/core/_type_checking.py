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
    "PyFluentTypeCheckingError",
    "install_import_hook",
    "is_type_checking_enabled",
    "no_runtime_type_check",
    "runtime_type_check",
)

#: Environment variable which activates runtime type-checking.
ENV_VAR = "PYFLUENT_RUNTIME_TYPE_CHECKING"


class PyFluentTypeCheckingError(TypeError):
    """Runtime type-checking violation in PyFluent API.

    Raised when a PyFluent function or method is called with arguments that do
    not match its declared type annotations, and runtime type-checking is
    enabled via the ``PYFLUENT_RUNTIME_TYPE_CHECKING`` environment variable.

    This exception wraps the underlying type-checking backend's exception,
    providing a stable PyFluent API that is independent of the backend
    implementation (e.g., ``beartype`` vs ``typeguard``).

    Users should not need to know or import the specific type-checking library.

    See Also
    --------
    :attr:`ansys.fluent.core.config.runtime_type_checking` : Configuration option
    """

    pass


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
    """Apply the ``beartype`` decorator to ``obj``, wrapping exceptions.

    Catches backend-specific exceptions and re-raises as PyFluentTypeCheckingError
    to maintain encapsulation and API stability.
    """
    import functools

    from beartype import beartype
    from beartype.roar import BeartypeException

    # Apply beartype decorator
    decorated = beartype(obj)

    # For callables (not classes), wrap to catch backend exceptions
    if callable(decorated) and not isinstance(decorated, type):

        @functools.wraps(decorated)
        def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            try:
                return decorated(*args, **kwargs)
            except BeartypeException as exc:
                raise PyFluentTypeCheckingError(
                    f"Type-checking violation: {exc}"
                ) from exc

        return wrapper  # type: ignore[return-value]

    # For classes and other objects, return as-is (claw handles them)
    return decorated


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


def no_runtime_type_check(obj):
    """Disable runtime type-checking for an object, with GenericAlias support.

    Marks an object so that runtime type-checking is skipped. This is useful for
    disabling type-checks on specific callables or classes that may cause issues
    with the type-checking backend.

    Unlike the standard library's :func:`typing.no_type_check`, this function
    handles ``types.GenericAlias`` objects (e.g., ``SettingsBase[DictStateType]``)
    which are commonly used in class inheritance. GenericAlias objects do not
    support attribute assignment, so applying ``typing.no_type_check()`` directly
    would raise ``AttributeError``. This function detects such objects and returns
    them unchanged.

    Parameters
    ----------
    obj : Callable, type, or types.GenericAlias
        Object to mark for skipping runtime type-checking. Can be a function,
        class, or generic alias.

    Returns
    -------
    Callable, type, or types.GenericAlias
        The input object unchanged, or with the ``__no_type_check__`` attribute
        set if it supports attribute assignment.

    Notes
    -----
    This function is a no-op when runtime type-checking is disabled via
    :func:`is_type_checking_enabled`.

    See Also
    --------
    :func:`typing.no_type_check` : Standard library equivalent
    :func:`runtime_type_check` : Enable runtime type-checking for an object
    """
    # Skip applying no_type_check to GenericAlias objects (e.g., SettingsBase[Type])
    # as they don't support attribute assignment
    import types

    if isinstance(obj, types.GenericAlias):
        return obj
    return typing.no_type_check(obj)
