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

"""Generic, solver-agnostic platform layer shared across Ansys solvers.

``ansys.framework`` is the public *platform* layer introduced by the
componentization effort (EPIC: https://github.com/ansys/pyfluent/issues/4618).
It holds the parts of the architecture that are not specific to Fluent: the
process-controller, the transport/service boundary, the generic object
framework and the generic session.

Architecture decision record
============================

Status: accepted (Phase 0, task 0.1).

Context
-------
PyFluent's client is tied to Fluent and to gRPC: ``FluentConnection`` mixes
connection lifecycle with gRPC channel setup, sessions reach into its service
factory, the service contracts depended on ``flobject``, and launching always
builds a gRPC connection and a session. This blocks swapping the communication
backend (gRPC/REST), using PyFluent as a lightweight process controller, and
reusing the architecture for other solvers.

Decision 1 - Namespace
----------------------
The platform is the public sibling namespace ``ansys.framework``, shipped in the
same ``ansys-fluent-core`` distribution as ``ansys.fluent.core`` (the wheel
packages the whole ``src/ansys`` tree). A private ``ansys.fluent.core._platform``
was rejected: it would tie the platform to Fluent's tree and conflict with the
multi-solver goal.

Decision 2 - Layers
-------------------
Platform layers (``ansys.framework``), lowest first:

* ``state_types`` - shared settings value types (``StateType`` and aliases).
* ``process`` - process controller: launch, monitor, terminate, readiness probe.
* ``connection`` / ``transport`` - backend-neutral connection lifecycle and the
  ``Transport`` protocol (metadata/auth, health, error state, connect, close).
* ``services`` - ``ServiceRegistry`` capability model; unsupported capabilities
  raise ``NotSupported``.
* ``objects`` - generic settings object framework and static-info schema.
* ``session`` - generic session owning the connection and services.

Solver-specific layers (``ansys.fluent.core``) sit on top: Fluent process
launchers, concrete transports (``transports.grpc``, ``transports.rest``),
``flobject`` as a Fluent extension of ``objects``, Fluent sessions and codegen.
Layers not yet present are added as their phase lands.

Decision 3 - Dependency rules
-----------------------------
Enforced by import-linter (``[tool.importlinter]`` in ``pyproject.toml``):

* ``ansys.framework`` MUST NOT import ``ansys.fluent.*``, ``grpc`` or
  ``ansys.api.*``. Solver layers may depend on the platform, never the reverse.
* Service contracts (``ansys.fluent.core.services``) MUST NOT import the object
  framework (``flobject``).
* ``ansys.framework.process`` imports only the standard library and minimal
  dependencies.

Contracts run report-only in CI until the hardening phase, then become blocking.

Decision 4 - gRPC dependency
----------------------------
The platform imports cleanly without ``grpc``. ``grpc`` and ``ansys-api-fluent``
are declared as the optional ``[grpc]`` extra, but stay in the default
dependencies so existing installs keep working.

Decision 5 - Backward-compatibility policy
------------------------------------------
Componentization must not break existing user code:

* Every moved module keeps a shim at its original ``ansys.fluent.core`` path that
  re-exports the moved names, so old imports still resolve. Shims for relocated
  modules emit ``PyFluentDeprecationWarning`` and are recorded in
  ``doc/deprecated_apis.py``; they are removed only through the standard PyFluent
  deprecation process.
* Existing ``sys.modules`` aliases in ``ansys.fluent.core`` are preserved.
* Public names, the ``launch_fluent`` signature, session class paths and
  ``isinstance``/pickling/``repr`` behaviour of settings objects are preserved.
  ``tests/test_public_api.py`` fails on any accidental change.
* The default install is unchanged.
* Each PR adds a ``doc/changelog.d`` fragment.

Consequences
------------
Modules move here incrementally in small PRs, each behind a shim, so the
import-linter baseline, the public API snapshot tests and the existing test
suite catch regressions at every step.
"""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _distribution_version

# Read the version from the distribution metadata rather than importing
# ``ansys.fluent.core`` (forbidden by the dependency rule above). This keeps a
# single source of truth and lets packaging smoke tests resolve ``__version__``
# from this top-level package, which is the shallowest in the distribution.
try:
    __version__ = _distribution_version("ansys-fluent-core")
except PackageNotFoundError:  # pragma: no cover - source tree without metadata
    __version__ = "0.0.0.dev0"
