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

from ansys.fluent.core.generated.datamodel_252.meshing import Root as meshing_root
from ansys.fluent.core.generated.datamodel_252.meshing_utilities import (
    Root as meshing_utilities_root,
)
from ansys.fluent.core.generated.datamodel_252.part_management import (
    Root as partmanagement_root,
)
from ansys.fluent.core.generated.datamodel_252.pm_file_management import (
    Root as pmfilemanagement_root,
)
from ansys.fluent.core.generated.datamodel_252.preferences import (
    Root as preferences_root,
)
from ansys.fluent.core.generated.datamodel_252.workflow import Root as workflow_root
from ansys.fluent.core.generated.meshing.tui_252 import main_menu

class PureMeshing:
    @property
    def tui(self) -> main_menu: ...
    @property
    def meshing(self) -> meshing_root: ...
    @property
    def meshing_utilities(self) -> meshing_utilities_root: ...
    @property
    def workflow(self) -> workflow_root: ...
    def watertight(self): ...
    def fault_tolerant(self): ...
    def two_dimensional_meshing(self): ...
    def topology_based(self): ...
    def load_workflow(self, file_path: str): ...
    def create_workflow(self): ...
    @property
    def PartManagement(self) -> partmanagement_root: ...
    @property
    def PMFileManagement(self) -> pmfilemanagement_root: ...
    @property
    def preferences(self) -> preferences_root: ...
    def transfer_mesh_to_solvers(
        self,
        solvers,
        file_type: str = ...,
        file_name_stem: str = ...,
        num_files_to_try: int = ...,
        clean_up_mesh_file: bool = ...,
        overwrite_previous: bool = ...,
    ): ...
    def enable_beta_features(self): ...
