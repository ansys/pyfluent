"""Wrappers over TUI-based datamodel gRPC service of Fluent."""

import keyword
import logging
from typing import Any

from google.protobuf.json_format import MessageToDict
import grpc

from ansys.api.fluent.v0 import datamodel_tui_pb2 as DataModelProtoModule
from ansys.api.fluent.v0 import datamodel_tui_pb2_grpc as DataModelGrpcModule
from ansys.api.fluent.v0.variant_pb2 import Variant
from ansys.fluent.core.services.api_upgrade import ApiUpgradeAdvisor
from ansys.fluent.core.services.interceptors import (
    BatchInterceptor,
    ErrorStateInterceptor,
    GrpcErrorInterceptor,
    TracingInterceptor,
)

Path = list[str]

logger: logging.Logger = logging.getLogger("pyfluent.tui")


class DatamodelServiceImpl:
    """Class wrapping the TUI-based datamodel gRPC service of Fluent."""

    def __init__(
        self, channel: grpc.Channel, metadata: list[tuple[str, str]], fluent_error_state
    ) -> None:
        """__init__ method of DatamodelServiceImpl class."""
        self._channel = channel
        self._fluent_error_state = fluent_error_state
        intercept_channel = grpc.intercept_channel(
            self._channel,
            GrpcErrorInterceptor(),
            ErrorStateInterceptor(self._fluent_error_state),
            TracingInterceptor(),
            BatchInterceptor(),
        )
        self._stub = DataModelGrpcModule.DataModelStub(intercept_channel)
        self._metadata = metadata

    def get_attribute_value(
        self, request: DataModelProtoModule.GetAttributeValueRequest
    ) -> DataModelProtoModule.GetAttributeValueResponse:
        """GetAttributeValue RPC of DataModel service."""
        return self._stub.GetAttributeValue(request, metadata=self._metadata)

    def get_state(
        self, request: DataModelProtoModule.GetStateRequest
    ) -> DataModelProtoModule.GetStateResponse:
        """GetState RPC of DataModel service."""
        return self._stub.GetState(request, metadata=self._metadata)

    def set_state(
        self, request: DataModelProtoModule.SetStateRequest
    ) -> DataModelProtoModule.SetStateResponse:
        """SetState RPC of DataModel service."""
        return self._stub.SetState(request, metadata=self._metadata)

    def execute_command(
        self, request: DataModelProtoModule.ExecuteCommandRequest
    ) -> DataModelProtoModule.ExecuteCommandResponse:
        """ExecuteCommand RPC of DataModel service."""
        return self._stub.ExecuteCommand(request, metadata=self._metadata)

    def execute_query(
        self, request: DataModelProtoModule.ExecuteQueryRequest
    ) -> DataModelProtoModule.ExecuteQueryResponse:
        """ExecuteQuery RPC of DataModel service."""
        return self._stub.ExecuteQuery(request, metadata=self._metadata)

    def get_static_info(self, request):
        """GetStaticInfo RPC of DataModel service."""
        return self._stub.GetStaticInfo(request, metadata=self._metadata)


def _convert_value_to_gvalue(val: Any, gval: Variant) -> None:
    """Convert Python datatype to Value type of google/protobuf/struct.proto."""
    if isinstance(val, bool):
        gval.bool_value = val
    elif isinstance(val, int) or isinstance(val, float):
        gval.number_value = val
    elif isinstance(val, str):
        gval.string_value = val
    elif isinstance(val, list) or isinstance(val, tuple):
        # set the one_of to list_value
        gval.list_value.values.add()
        gval.list_value.values.pop()
        for item in val:
            item_gval = gval.list_value.values.add()
            _convert_value_to_gvalue(item, item_gval)
    elif isinstance(val, dict):
        for k, v in val.items():
            _convert_value_to_gvalue(v, gval.struct_value.fields[k])


def _convert_gvalue_to_value(gval: Variant) -> Any:
    """Convert Value type of google/protobuf/struct.proto to Python datatype."""
    if gval.HasField("bool_value"):
        return gval.bool_value
    elif gval.HasField("number_value"):
        return gval.number_value
    elif gval.HasField("string_value"):
        return gval.string_value
    elif gval.HasField("list_value"):
        val = []
        for item in gval.list_value.values:
            val.append(_convert_gvalue_to_value(item))
        return val
    elif gval.HasField("struct_value"):
        val = {}
        for k, v in gval.struct_value.fields.items():
            val[k] = _convert_gvalue_to_value(v)
        return val


class DatamodelService:
    """Pure Python wrapper of DatamodelServiceImpl."""

    def __init__(
        self,
        channel: grpc.Channel,
        metadata: list[tuple[str, str]],
        fluent_error_state,
        app_utilities,
        scheme_eval,
    ) -> None:
        """__init__ method of DatamodelService class."""
        self._impl = DatamodelServiceImpl(channel, metadata, fluent_error_state)
        self._app_utilities = app_utilities
        self._scheme_eval = scheme_eval

    def get_attribute_value(
        self, path: str, attribute: str, include_unavailable: bool
    ) -> Any:
        """Get the attribute value."""
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.path = path
        request.attribute = DataModelProtoModule.Attribute.Value(attribute.upper())
        if include_unavailable:
            request.args["include_unavailable"] = 1
        response = self._impl.get_attribute_value(request)
        return _convert_gvalue_to_value(response.value)

    def execute_command(self, path: str, *args, **kwargs) -> Any:
        """Execute the command."""
        request = DataModelProtoModule.ExecuteCommandRequest()
        request.path = path
        if kwargs:
            for k, v in kwargs.items():
                _convert_value_to_gvalue(v, request.args.fields[k])
        else:
            _convert_value_to_gvalue(args, request.args.fields["tui_args"])
        return self._impl.execute_command(request)

    def execute_query(self, path: str, *args, **kwargs) -> Any:
        """Execute the query."""
        request = DataModelProtoModule.ExecuteQueryRequest()
        request.path = path
        if kwargs:
            for k, v in kwargs.items():
                _convert_value_to_gvalue(v, request.args.fields[k])
        else:
            _convert_value_to_gvalue(args, request.args.fields["tui_args"])
        return self._impl.execute_query(request)

    def get_static_info(self, path: str):
        """Get static info."""
        request = DataModelProtoModule.GetStaticInfoRequest()
        request.path = path
        response = self._impl.get_static_info(request)
        # Note: MessageToDict's parameter names are different in different protobuf versions
        return MessageToDict(response.info, True)


class PyMenu:
    """Pythonic wrapper of TUI-based DatamodelService class. Use this class instead of
    directly calling the DatamodelService's method.

    Methods
    -------
    get_child_names(include_unavailable):
        Get child menu names.
    execute(*args, **kwargs)
        Execute a command or query at a menu with positional or keyword
        arguments.
    get_doc_string(include_unavailable)
        Get docstring for a menu.
    """

    def __init__(
        self, service: DatamodelService, version, mode, path: Path | str
    ) -> None:
        """__init__ method of PyMenu class."""
        self._service = service
        self._version = version
        self._mode = mode
        self._path = path if isinstance(path, str) else convert_path_to_grpc_path(path)

    def get_child_names(self, include_unavailable: bool = False) -> list[str]:
        """Get the names of child menus.

        Parameters
        ----------
        include_unavailable : bool, optional
            Whether to query over static TUI metadata. The default is ``False``.

        Returns
        -------
        List[str]
            Names of child menus.
        """
        attribute = DataModelProtoModule.Attribute.Name(
            DataModelProtoModule.Attribute.CHILD_NAMES
        ).lower()
        return self._service.get_attribute_value(
            self._path, attribute, include_unavailable
        )

    def execute(self, *args, **kwargs) -> Any:
        """Execute a command or query at a path with positional or keyword arguments.

        Parameters
        ----------
        *args
            Positional arguments of the command or qyery.
        **kwargs
            Keyword arguments of the command or query.

        Returns
        -------
        Any
            Query result (any Python datatype)
        """
        with ApiUpgradeAdvisor(
            self._service._app_utilities,
            self._version,
            self._mode,
        ):
            if self._path.startswith("/query/"):
                return self._service.execute_query(self._path, *args, **kwargs)
            else:
                return self._service.execute_command(self._path, *args, **kwargs)

    def get_doc_string(self, include_unavailable: bool = False) -> str:
        """Get docstring for a menu.

        Parameters
        ----------
        include_unavailable : bool, optional
            Whether to query over static TUI metadata. The default is ``False``.

        Returns
        -------
        str
        """
        attribute = DataModelProtoModule.Attribute.Name(
            DataModelProtoModule.Attribute.HELP_STRING
        ).lower()
        return self._service.get_attribute_value(
            self._path, attribute, include_unavailable
        )

    def get_static_info(self) -> dict[str, Any]:
        """Get static info at menu level.

        Returns
        -------
        DataModelProtoModule.StaticInfo
            static info
        """
        try:
            return self._service.get_static_info(self._path)
        except RuntimeError:
            return _get_static_info_at_level(self)


def _get_static_info_at_level(menu: PyMenu) -> dict[str, Any]:
    info = {}
    info["help"] = menu.get_doc_string(include_unavailable=True)
    info["menus"] = {}
    info["commands"] = {}
    child_names = menu.get_child_names(include_unavailable=True)
    if child_names:
        for child_name in child_names:
            if child_name:
                child_menu = PyMenu(
                    menu._service,
                    menu._version,
                    menu._mode,
                    menu._path + ("" if menu._path.endswith("/") else "/") + child_name,
                )
                child_info = _get_static_info_at_level(child_menu)
                if child_info.pop("is_command", False):
                    info["commands"][child_name] = child_info
                else:
                    info["menus"][child_name] = child_info
    else:
        info["is_command"] = True
    return info


class TUIMethod:
    """Base class for the generated menu methods.

    Methods like ___repr__ are inserted at PyConsole side.
    """

    def __init__(self, service, version, mode, path):
        """Initialize TUIMethod."""
        self._service = service
        self._version = version
        self._mode = mode
        self._path = path

    def __call__(self, *args, **kwargs):
        return PyMenu(self._service, self._version, self._mode, self._path).execute(
            *args, **kwargs
        )


class TUIMenu:
    """Base class for the generated menu classes."""

    def __init__(self, service, version, mode, path) -> None:
        """__init__ method of TUIMenu class."""
        self._service = service
        self._version = version
        self._mode = mode
        self._path = path

    def __dir__(self) -> list[str]:
        return [
            convert_tui_menu_to_func_name(x)
            for x in PyMenu(
                self._service, self._version, self._mode, self._path
            ).get_child_names()
            if x not in ["exit", "switch_to_meshing_mode"]
        ]

    def __getattribute__(self, name) -> Any:
        if name in ["exit", "switch_to_meshing_mode"] and not self._path:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            )
        try:
            attr = super().__getattribute__(name)
            if isinstance(attr, TUIMethod):
                # some runtime submenus are generated as methods during codegen
                path = self._path + [name]
                if PyMenu(
                    self._service, self._version, self._mode, path
                ).get_child_names():
                    return TUIMenu(self._service, self._version, self._mode, path)
            return attr
        except AttributeError as ex:
            if name in dir(self):
                # for runtime submenus and commands which are not available during codegen
                path = self._path + [name]
                if PyMenu(
                    self._service, self._version, self._mode, path
                ).get_child_names():
                    return TUIMenu(self._service, self._version, self._mode, path)
                else:
                    return TUICommand(self._service, self._version, self._mode, path)
            else:
                raise ex


class TUICommand(TUIMenu):
    """Generic command class for when the explicit menu classes aren't available."""

    def __call__(self, *args, **kwargs) -> Any:
        return PyMenu(self._service, self._version, self._mode, self._path).execute(
            *args, **kwargs
        )


def convert_tui_menu_to_func_name(menu: str) -> str:
    """Convert a TUI menu string to a Python function name.

    Parameters
    ----------
    menu : str
       TUI menu string.

    Returns
    -------
    str
    """
    if keyword.iskeyword(menu):
        return menu + "_"
    if menu.endswith("[beta]"):
        menu = menu[:-6]
    menu = menu.rstrip("?")
    return menu


def convert_path_to_grpc_path(path: Path) -> str:
    """Convert a path structure to a string that can be passed to the data model gRPC
    service.

    Parameters
    ----------
    path : Path
        Path structure.

    Returns
    -------
    str
        gRPC path.
    """
    return "/" + "/".join(x for x in path)
