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
It is a sibling namespace to ``ansys.fluent.core`` that holds the parts of the
architecture that are not specific to Fluent: the process-controller, the
transport/service boundary, the generic object framework and the generic
session.

Dependency rule (enforced by import-linter; see the architecture page in the
docs):

    ``ansys.framework`` MUST NOT import ``ansys.fluent.*``, ``grpc`` or
    ``ansys.api.*``.

Solver-specific layers (such as ``ansys.fluent.core``) may depend on this
package, never the reverse.

This package is currently a stub. Modules are moved here incrementally, each
behind a backward-compatible shim at the original ``ansys.fluent.core`` path.
"""
