from ansys.fluent.core.generated.datamodel_242.MeshingUtilities import (
    Root as meshing_utilities_root,
)
from ansys.fluent.core.generated.datamodel_242.PMFileManagement import (
    Root as pmfilemanagement_root,
)
from ansys.fluent.core.generated.datamodel_242.PartManagement import (
    Root as partmanagement_root,
)
from ansys.fluent.core.generated.datamodel_242.meshing import Root as meshing_root
from ansys.fluent.core.generated.datamodel_242.preferences import (
    Root as preferences_root,
)
from ansys.fluent.core.generated.datamodel_242.workflow import Root as workflow_root
from ansys.fluent.core.generated.meshing.tui_242 import main_menu

class Meshing:
    @property
    def tui(self) -> main_menu: ...
    @property
    def meshing(self) -> meshing_root: ...
    @property
    def meshing_utilities(self) -> meshing_utilities_root: ...
    @property
    def workflow(self) -> workflow_root: ...
    @property
    def PartManagement(self) -> partmanagement_root: ...
    @property
    def PMFileManagement(self) -> pmfilemanagement_root: ...
    @property
    def preferences(self) -> preferences_root: ...
