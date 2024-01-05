from ansys.fluent.core.services.datamodel_se import (
    DatamodelService as DatamodelService_SE,
)
from ansys.fluent.core.services.field_data import FieldData, FieldInfo
from ansys.fluent.core.services.scheme_eval import SchemeEval
from ansys.fluent.core.services.settings import SettingsService

_service_cls_by_name = {
    "datamodel": DatamodelService_SE,
    "settings": SettingsService,
    "scheme_eval": SchemeEval,
    "field_data": FieldData,
    "field_info": FieldInfo,
}


class service_creator:
    def __init__(self, service_name: str):
        self._service_cls = _service_cls_by_name[service_name]

    def create(self, *args, **kwargs):
        return self._service_cls(*args, **kwargs)
