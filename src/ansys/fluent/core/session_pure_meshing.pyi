from ansys.fluent.core.datamodel_241.PMFileManagement import (
    Root as pmfilemanagement_root,
)
from ansys.fluent.core.datamodel_241.PartManagement import Root as partmanagement_root
from ansys.fluent.core.datamodel_241.meshing import Root as meshing_root
from ansys.fluent.core.datamodel_241.meshing_utilities import (
    Root as meshing_utilities_root,
)
from ansys.fluent.core.datamodel_241.preferences import Root as preferences_root
from ansys.fluent.core.datamodel_241.workflow import Root as workflow_root
from ansys.fluent.core.solver.tui_241 import main_menu

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
