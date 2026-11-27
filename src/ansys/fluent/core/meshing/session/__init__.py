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

"""Fluent meshing session classes.

Import either session class from ``ansys.fluent.core.meshing.session``:

* :class:`~ansys.fluent.core.meshing.session.meshing.Meshing` supports switching
    the running Fluent process to solver mode with ``switch_to_solver()``.
* :class:`~ansys.fluent.core.meshing.session.pure_meshing.PureMeshing` provides
    meshing capabilities without solver switching, for workflows where meshing
    and solving run separately.

Both session types provide the same workflow methods. Start a workflow with
:meth:`watertight() <ansys.fluent.core.meshing.session.base_meshing.BaseMeshing.watertight>`
or resume a saved one with
:meth:`load_workflow() <ansys.fluent.core.meshing.session.base_meshing.BaseMeshing.load_workflow>`.
Browse the :class:`shared meshing methods <ansys.fluent.core.meshing.session.base_meshing.BaseMeshing>`
for the full list, or follow the :ref:`meshing workflows guide <ref_meshing_guide>`.
"""

from ansys.fluent.core.meshing.session.meshing import Meshing
from ansys.fluent.core.meshing.session.pure_meshing import PureMeshing

__all__ = ("Meshing", "PureMeshing")
