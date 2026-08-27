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

"""Meshing-only Fluent session (:class:`PureMeshing`).

Inheritance
-----------
::

    BaseSession (private)
    └── BaseMeshing (private)
        └── PureMeshing          ← this class
"""

from ansys.fluent.core.session.base_meshing import BaseMeshing


class PureMeshing(BaseMeshing):
    """Fluent meshing session without solver-switching capability.

    Designed for deployments where meshing and solving run as separate
    processes (e.g. containerised pipelines).  All public API is provided
    by :class:`~ansys.fluent.core.session.base_meshing.BaseMeshing`.

    Use :class:`~ansys.fluent.core.session.meshing.Meshing` when you also
    need :meth:`~ansys.fluent.core.session.meshing.Meshing.switch_to_solver`.
    """
