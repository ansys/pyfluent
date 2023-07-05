from ansys.fluent.core.datamodel_232.PMFileManagement import (
    Root as pmfilemanagement_root,
)
from ansys.fluent.core.datamodel_232.PartManagement import Root as partmanagement_root
from ansys.fluent.core.datamodel_232.meshing import Root as meshing_root
from ansys.fluent.core.datamodel_232.preferences import Root as preferences_root
from ansys.fluent.core.datamodel_232.workflow import Root as workflow_root
from ansys.fluent.core.solver.tui_232 import main_menu

class Meshing:
    @property
    def tui(self) -> main_menu: ...
    @property
    def meshing(self) -> meshing_root: ...
    @property
    def workflow(self) -> workflow_root: ...
    @property
    def PartManagement(self) -> partmanagement_root: ...
    @property
    def PMFileManagement(self) -> pmfilemanagement_root: ...
    @property
    def preferences(self) -> preferences_root: ...
