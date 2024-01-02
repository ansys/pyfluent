from ansys.fluent.core.services.datamodel_se import (
    DatamodelService as DatamodelService_SE,
)
from ansys.fluent.core.services.scheme_eval import SchemeEval
from ansys.fluent.core.services.settings import SettingsService

_service_cls_by_name = {
    "datamodel": DatamodelService_SE,
    "settings": SettingsService,
    "scheme_eval": SchemeEval,
}


class service_creator:
    def create(self, service_name: str, *args, **kwargs):
        return _service_cls_by_name[service_name](*args, **kwargs)
