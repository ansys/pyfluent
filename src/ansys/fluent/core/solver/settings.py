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

"""Convenient access to the solver settings hierarchy.

This module exposes the solver settings namespace directly under
:mod:`ansys.fluent.core.solver`, so the :ref:`settings root <ref_root>` can be
reached without importing a version-specific generated module:

.. code-block:: python

    from ansys.fluent.core.solver import settings

Its purpose is to make the settings API easy to access. Attribute access is
resolved in one of two ways:

- **Active session** - when a Fluent session is active (entered with
  :func:`~ansys.fluent.core.using`), attributes resolve to the live
  :ref:`settings root <ref_root>` objects of that session, so state can be
  queried or set and commands can be run.
- **No active session** - attributes resolve to the version-specific generated
  settings classes (selected from ``config.fluent_release_version``, defaulting
  to the current release). This is a static view of the hierarchy: class
  metadata such as ``child_names`` and ``_child_classes`` is available, but live
  queries and commands raise an error until a session is active.

Examples
--------
Configure and query the live settings of an active session:

>>> import ansys.fluent.core as pyfluent
>>> from ansys.fluent.core import using
>>> from ansys.fluent.core.solver import settings
>>> solver = pyfluent.launch_fluent()
>>> with using(solver):
...     settings.setup.models.energy.enabled = True
...     settings.setup.boundary_conditions.get_active_child_names()

Inspect the settings hierarchy statically, without a session:

>>> from ansys.fluent.core.solver import settings
>>> "boundary_conditions" in settings.setup.child_names
True

See the :ref:`settings root <ref_root>` for the complete solver settings
hierarchy and the available configuration objects.
"""

from importlib import import_module
import inspect
import logging
from pathlib import Path
import warnings

from ansys.fluent.core.diagnostics.exceptions import PyFluentUserWarning

logger = logging.getLogger("pyfluent.general")

_CODEGEN_MSG = (
    "No generated solver settings classes were found. Please run "
    "`python codegen/allapigen.py` from the top-level pyfluent directory to "
    "generate the local settings API classes."
)

_generated_module = None


class _StaticSettingsProxy:
    """Static, session-less view of a generated settings class.

    Class-level metadata (for example ``child_names`` and ``_child_classes``) is
    exposed directly. Live queries and commands are unavailable without a
    session and raise a descriptive error when called.
    """

    def __init__(self, cls: type) -> None:
        object.__setattr__(self, "_cls", cls)

    def __getattr__(self, name: str):
        cls = object.__getattribute__(self, "_cls")
        value = getattr(cls, name)
        if inspect.isroutine(value):

            def _requires_live_session(*args, **kwargs):
                raise RuntimeError(
                    f"'{cls.__name__}.{name}' requires a live Fluent session. "
                    "Without an active session, 'ansys.fluent.core.solver."
                    "settings' only lists the settings hierarchy statically "
                    "(for example 'child_names' and '_child_classes'). To run "
                    "active queries or commands, use it within the context of "
                    "a live session, e.g. 'with using(session): ...'."
                )

            return _requires_live_session
        return value

    def __dir__(self):
        return dir(object.__getattribute__(self, "_cls"))

    def __repr__(self) -> str:
        cls = object.__getattribute__(self, "_cls")
        return f"<static settings view of {cls.__module__}.{cls.__qualname__}>"


def _resolve_default_version() -> str:
    """Return the version (e.g. ``"261"``) of the generated settings to proxy.

    Prefers the current release; falls back to the newest generated version
    available under the codegen output directory.
    """
    from ansys.fluent.core.module_config import config
    from ansys.fluent.core.utils.fluent_version import FluentVersion

    outdir = Path(config.codegen_outdir)
    preferred = str(FluentVersion.current_release().number)
    if (outdir / f"v{preferred}" / "solver" / "settings.py").is_file():
        return preferred
    available = sorted(
        (
            path.parent.parent.name[1:]
            for path in outdir.glob("v*/solver/settings.py")
            if path.parent.parent.name[1:].isdigit()
        ),
        key=int,
        reverse=True,
    )
    if available:
        return available[0]
    raise RuntimeError(_CODEGEN_MSG)


def _default_generated_module():
    """Import and cache the version-specific generated settings module."""
    global _generated_module
    if _generated_module is None:
        version = _resolve_default_version()
        _generated_module = import_module(
            f"ansys.fluent.core.generated.v{version}.solver.settings"
        )
    return _generated_module


def __getattr__(name: str):
    if name.startswith("__") and name.endswith("__"):
        raise AttributeError(name)

    from ansys.fluent.core.execution.session.session import _get_active_session

    settings_source = getattr(_get_active_session(), "settings", None)
    if settings_source is not None:
        try:
            return getattr(settings_source, name)
        except AttributeError:
            pass
    else:
        warnings.warn(
            "No active Fluent session; falling back to the version-specific "
            "generated settings classes. The returned object is a class "
            "definition, not a live settings object connected to Fluent.",
            PyFluentUserWarning,
            stacklevel=2,
        )

    module = _default_generated_module()
    try:
        value = getattr(module, name)
    except AttributeError:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from None
    return _StaticSettingsProxy(value) if isinstance(value, type) else value


def __dir__():
    try:
        return sorted(
            name
            for name in dir(_default_generated_module())
            if not name.startswith("_")
        )
    except RuntimeError:
        return []
