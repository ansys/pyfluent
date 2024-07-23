from ansys.fluent.core.generated.solver.settings_222 import root as settings_root_222
from ansys.fluent.core.generated.solver.settings_231 import root as settings_root_231
from ansys.fluent.core.generated.solver.settings_232 import root as settings_root_232
from ansys.fluent.core.generated.solver.settings_241 import root as settings_root_241
from ansys.fluent.core.generated.solver.settings_242 import root as settings_root_242
from ansys.fluent.core.generated.solver.settings_251 import root as settings_root_251

class viscous(
    type(settings_root_222.setup.models.viscous),
    type(settings_root_231.setup.models.viscous),
    type(settings_root_232.setup.models.viscous),
    type(settings_root_241.setup.models.viscous),
    type(settings_root_242.setup.models.viscous),
    type(settings_root_251.setup.models.viscous),
): ...
class boundary_conditions(
    type(settings_root_222.setup.boundary_conditions),
    type(settings_root_231.setup.boundary_conditions),
    type(settings_root_232.setup.boundary_conditions),
    type(settings_root_241.setup.boundary_conditions),
    type(settings_root_242.setup.boundary_conditions),
    type(settings_root_251.setup.boundary_conditions),
): ...
class velocity_inlet(
    type(settings_root_222.setup.boundary_conditions.velocity_inlet.child_object_type),
    type(settings_root_231.setup.boundary_conditions.velocity_inlet.child_object_type),
    type(settings_root_232.setup.boundary_conditions.velocity_inlet.child_object_type),
    type(settings_root_241.setup.boundary_conditions.velocity_inlet.child_object_type),
    type(settings_root_242.setup.boundary_conditions.velocity_inlet.child_object_type),
    type(settings_root_251.setup.boundary_conditions.velocity_inlet.child_object_type),
): ...
