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

from ansys.fluent.core.generated.datamodel_251.preferences import (
    Root as preferences_root,
)
from ansys.fluent.core.generated.datamodel_251.workflow import Root as workflow_root
import ansys.fluent.core.generated.solver.settings_251 as settings_root
from ansys.fluent.core.generated.solver.tui_251 import main_menu
from ansys.fluent.core.system_coupling import SystemCoupling

class Solver:
    @property
    def version(self): ...
    @property
    def tui(self) -> main_menu: ...
    @property
    def workflow(self) -> workflow_root: ...
    @property
    def system_coupling(self) -> SystemCoupling: ...
    @property
    def preferences(self) -> preferences_root: ...
    def read_case_lightweight(self, file_name: str): ...
    def read_case(self, file_name: str): ...
    def write_case(self, file_name: str): ...
    @property
    def settings(self) -> settings_root.root: ...
