from ansys.fluent.core.services.batch_ops import BatchOpsService
from ansys.fluent.core.services.datamodel_se import (
    DatamodelService as DatamodelService_SE,
)
from ansys.fluent.core.services.datamodel_tui import (
    DatamodelService as DatamodelService_TUI,
)
from ansys.fluent.core.services.events import EventsService
from ansys.fluent.core.services.field_data import FieldData, FieldInfo
from ansys.fluent.core.services.health_check import HealthCheckService
from ansys.fluent.core.services.monitor import MonitorsService
from ansys.fluent.core.services.reduction import Reduction
from ansys.fluent.core.services.scheme_eval import SchemeEval
from ansys.fluent.core.services.settings import SettingsService
from ansys.fluent.core.services.solution_variables import (
    SolutionVariableData,
    SolutionVariableService,
)
from ansys.fluent.core.services.transcript import TranscriptService

_service_cls_by_name = {
    "health_check": HealthCheckService,
    "datamodel": DatamodelService_SE,
    "tui": DatamodelService_TUI,
    "settings": SettingsService,
    "scheme_eval": SchemeEval,
    "events": EventsService,
    "field_data": FieldData,
    "field_info": FieldInfo,
    "monitors": MonitorsService,
    "reduction": Reduction,
    "svar": SolutionVariableService,
    "svar_data": SolutionVariableData,
    "transcript": TranscriptService,
    "batch_ops": BatchOpsService,
}


class service_creator:
    def __init__(self, service_name: str):
        self._service_cls = _service_cls_by_name[service_name]

    def create(self, *args, **kwargs):
        return self._service_cls(*args, **kwargs)
