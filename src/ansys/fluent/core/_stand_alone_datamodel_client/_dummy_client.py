from ansys.fluent.core._stand_alone_datamodel_client._datamodel_client import (
    _DataModelClient,
)


class _DummyClient(_DataModelClient):
    def __init__(self):
        super().__init__("dummy")
