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

from types import SimpleNamespace

import ansys.fluent.core as pyfluent
from ansys.fluent.core.execution.docker.utils import get_grpc_launcher_args_for_gh_runs
from ansys.fluent.core.solver.session.solver_icing import SolverIcing


def test_icing_datamodel_module_path(monkeypatch):
    imports = []
    root = object()

    def import_module(name):
        imports.append(name)
        return SimpleNamespace(Root=lambda service, rules, path: root)

    monkeypatch.setattr(
        "ansys.fluent.core.solver.session.solver_icing.importlib.import_module",
        import_module,
    )
    session = SimpleNamespace(
        _flserver_root=None, _datamodel_service_se=object(), _version="271"
    )

    assert SolverIcing._flserver.fget(session) is root
    assert imports == ["ansys.fluent.core.generated.v271.object_model.flicing"]


def test_icing_session():
    grpc_kwds = get_grpc_launcher_args_for_gh_runs()
    icing_session = pyfluent.launch_fluent(
        mode=pyfluent.FluentMode.SOLVER_ICING, **grpc_kwds
    )
    assert "icing" in dir(icing_session)
