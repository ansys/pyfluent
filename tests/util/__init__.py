# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
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

from pathlib import Path
from tempfile import TemporaryDirectory
import uuid

from pytest import MonkeyPatch

import ansys.fluent.core as pyfluent
from ansys.fluent.core.codegen import StaticInfoType, datamodelgen
from ansys.fluent.core.utils import load_module


def create_datamodel_root_in_server(session, rules_str, app_name) -> None:
    rules_file_name = f"{uuid.uuid4()}.fdl"
    session.scheme_eval.scheme_eval(
        f'(with-output-to-file "{rules_file_name}" (lambda () (format "~a" "{rules_str}")))',
    )
    session.scheme_eval.scheme_eval(
        f'(state/register-new-state-engine "{app_name}" "{rules_file_name}")'
    )
    session.scheme_eval.scheme_eval(f'(remove-file "{rules_file_name}")')
    assert session.scheme_eval.scheme_eval(f'(state/find-root "{app_name}")') > 0


def create_root_using_datamodelgen(service, app_name):
    version = "252"
    static_info = service.get_static_info(app_name)
    with TemporaryDirectory() as temp_dir:
        with MonkeyPatch.context() as m:
            m.setattr(pyfluent, "CODEGEN_OUTDIR", Path(temp_dir))
            # TODO: Refactor datamdodelgen so we don't need to hardcode StaticInfoType
            datamodelgen.generate(
                version, static_infos={StaticInfoType.DATAMODEL_WORKFLOW: static_info}
            )
            gen_file = Path(temp_dir) / f"datamodel_{version}" / "workflow.py"
            module = load_module("datamodel", gen_file)
            return module.Root(service, app_name, [])
