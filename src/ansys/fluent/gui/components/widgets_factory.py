"""Module providing widgets factory."""

from abc import ABCMeta, abstractmethod
from enum import Enum

from dash import dcc, html
import dash_bootstrap_components as dbc


class PropertyEditorDataType(Enum):
    UNDEFINED = 0
    STRING = 1
    INTEGER = 2
    REAL = 3
    BOOLEAN = 4
    STRING_LIST = 5
    STRING_LIST_MULTI_SELECT = 6


class WidgetsProviderBase(metaclass=ABCMeta):
    """Abstract class for WidgetsProvider."""

    @abstractmethod
    def get_widget(self) -> object:
        """Get widget."""


class WidgetsFactory:
    """Widgets factory."""

    def __init__(self):
        self._widgets_provider = {}

    def register_widgets_provider(
        self, name: str, widgets_provider: WidgetsProviderBase
    ) -> None:
        """Regsitare widgets provider with factory.
        Parameters
        ----------
        name : str
            Widgets provider name.

        widgets_provider : WidgetsProviderBase
            Widgets provider class.

        Returns
        --------
        None
        """
        self._widgets_provider[name] = widgets_provider

    def get_widgets_provider(self, name) -> object:
        """Get registered widgets provider.
        Parameters
        ----------
        name : str
            Widgets provider name.

        Returns
        --------
        object
            Widgets provider object.

        Raises
        --------
        ValueError if widgets provider is not registered.
        """
        provider = self._widgets_provider.get(name)
        if not provider:
            raise ValueError(f"{provider} is not registered.")
        return provider()


class DCCWidgetsProvider(WidgetsProviderBase):
    """Dash core component widgets provider."""

    _editor_data_type_to_widget_map = {
        PropertyEditorDataType.STRING_LIST: lambda id, **kwargs: dcc.Dropdown(
            id=id, **kwargs
        ),
        PropertyEditorDataType.BOOLEAN: lambda id, **kwargs: dcc.Checklist(
            id=id, **kwargs
        ),
        PropertyEditorDataType.REAL: lambda id, **kwargs: dcc.Input(id=id, **kwargs),
        PropertyEditorDataType.INTEGER: lambda id, **kwargs: dcc.Input(id=id, **kwargs),
        PropertyEditorDataType.STRING: lambda id, **kwargs: dcc.Input(id=id, **kwargs),
    }

    def get_widget(self, name, property_editor_data_type, id_type, id_index, **kwargs):
        widget_args = {}
        # print('_get_widget', name, type, kwargs)
        if property_editor_data_type == PropertyEditorDataType.STRING:
            allowed_values = kwargs.get("allowed-values")
            if allowed_values:
                options = (
                    allowed_values
                    if isinstance(allowed_values, list)
                    else [allowed_values]
                )
                widget_args.update({"options": options})
                property_editor_data_type = PropertyEditorDataType.STRING_LIST
            else:
                widget_args.update({"type": "text"})
        elif property_editor_data_type == PropertyEditorDataType.STRING_LIST:
            allowed_values = kwargs.get("allowed-values")
            options = (
                allowed_values if isinstance(allowed_values, list) else [allowed_values]
            )
            widget_args.update({"options": options, "multi": True})
        elif property_editor_data_type == PropertyEditorDataType.BOOLEAN:
            options = {
                "selected": name,
            }
            widget_args.update({"options": options})
        elif property_editor_data_type == PropertyEditorDataType.REAL:
            range = kwargs.get("range")
            if range:
                widget_args.update(
                    {
                        "type": "number",
                        "min": range[0] if range else None,
                        "max": range[1] if range else None,
                    }
                )
            else:
                widget_args.update({"type": "number"})
        elif property_editor_data_type == PropertyEditorDataType.INTEGER:
            range = kwargs.get("range")
            if range:
                widget_args.update(
                    {
                        "type": "number",
                        "min": range[0] if range else None,
                        "max": range[1] if range else None,
                    }
                )
            else:
                widget_args.update({"type": "number"})
        value = kwargs.get("value")
        if value:
            if isinstance(value, bool):
                value = ["selected"] if value else []
            widget_args.update({"value": value})

        widget_fun = self._editor_data_type_to_widget_map.get(property_editor_data_type)
        if widget_fun:
            widget = widget_fun(
                {"type": f"{id_type}", "index": f"{id_index}"}, **widget_args
            )
        else:
            widget = html.Div("Widget not found.")
        if property_editor_data_type == PropertyEditorDataType.BOOLEAN:
            widget = html.Div([widget], style={"padding": "10px 1px 2px"})
        else:
            widget = html.Div(
                [
                    html.Div(name),
                    widget,
                ],
                style={
                    "display": "flex",
                    "flex-direction": "column",
                    "padding": "4px",
                },
            )
        return widget


class DBCWidgetsProvider(WidgetsProviderBase):
    """Dash bootstrap component widgets provider."""

    _editor_data_type_to_widget_map = {
        # PropertyEditorDataType.STRING_LIST: lambda id, **kwargs: dbc.Select(
        #    id=id, size="sm", **kwargs
        # ),
        PropertyEditorDataType.STRING_LIST: lambda id, **kwargs: dcc.Dropdown(
            id=id, **kwargs, className="dash-bootstrap"
        ),
        PropertyEditorDataType.BOOLEAN: lambda id, **kwargs: dbc.Checklist(
            id=id, **kwargs
        ),
        PropertyEditorDataType.REAL: lambda id, **kwargs: dbc.Input(
            id=id, size="sm", **kwargs
        ),
        PropertyEditorDataType.INTEGER: lambda id, **kwargs: dbc.Input(
            id=id, size="sm", **kwargs
        ),
        PropertyEditorDataType.STRING: lambda id, **kwargs: dbc.Input(
            id=id, size="sm", **kwargs
        ),
        PropertyEditorDataType.STRING_LIST_MULTI_SELECT: lambda id, **kwargs: dcc.Dropdown(
            id=id, **kwargs, className="dash-bootstrap"
        ),
    }

    def get_widget(self, name, property_editor_data_type, id_type, id_index, **kwargs):
        widget_args = {}
        # print('_get_widget', name, type, kwargs)
        if property_editor_data_type == PropertyEditorDataType.STRING:
            allowed_values = kwargs.get("allowed-values")
            if allowed_values:
                allowed_values = (
                    allowed_values
                    if isinstance(allowed_values, list)
                    else [allowed_values]
                )
                options = [
                    {"label": allowed_value, "value": allowed_value}
                    for allowed_value in allowed_values
                ]
                widget_args.update({"options": options})
                property_editor_data_type = PropertyEditorDataType.STRING_LIST
            else:
                widget_args.update({"type": "text"})
        elif property_editor_data_type == PropertyEditorDataType.STRING_LIST:
            allowed_values = kwargs.get("allowed-values")
            allowed_values = (
                allowed_values if isinstance(allowed_values, list) else [allowed_values]
            )
            options = [
                {"label": allowed_value, "value": allowed_value}
                for allowed_value in allowed_values
            ]
            widget_args.update({"options": options, "multi": True})
            property_editor_data_type = PropertyEditorDataType.STRING_LIST_MULTI_SELECT
            # widget_args.update({"options": options})
        elif property_editor_data_type == PropertyEditorDataType.BOOLEAN:
            options = [
                {"label": name, "value": "selected"},
            ]
            widget_args.update({"options": options})
        elif property_editor_data_type == PropertyEditorDataType.REAL:
            range = kwargs.get("range")
            if range:
                widget_args.update(
                    {
                        "type": "number",
                        "min": range[0] if range else None,
                        "max": range[1] if range else None,
                    }
                )
            else:
                widget_args.update({"type": "number"})
        elif property_editor_data_type == PropertyEditorDataType.INTEGER:
            range = kwargs.get("range")
            if range:
                widget_args.update(
                    {
                        "type": "number",
                        "min": range[0] if range else None,
                        "max": range[1] if range else None,
                    }
                )
            else:
                widget_args.update({"type": "number"})
        value = kwargs.get("value")
        if value:
            if isinstance(value, bool):
                value = ["selected"] if value else []
            widget_args.update({"value": value})

        widget_fun = self._editor_data_type_to_widget_map.get(property_editor_data_type)
        if widget_fun:
            widget = widget_fun(
                {"type": f"{id_type}", "index": f"{id_index}"}, **widget_args
            )
        else:
            widget = html.Div("Widget not found.")
        if property_editor_data_type == PropertyEditorDataType.BOOLEAN:
            widget = html.Div(
                [
                    widget,
                ],
                style={
                    "padding": "10px 0px 0px 4px",
                    # "border":"1px solid"
                },
            )

        else:
            widget = html.Div(
                [
                    dbc.Label(name),
                    widget,
                ],
                style={
                    "display": "flex",
                    "flex-direction": "column",
                    "padding": "10px 0px 0px 0px",
                    # "border":"1px solid"
                },
            )
        return widget


widgets_factory = WidgetsFactory()
widgets_factory.register_widgets_provider("DCC", DCCWidgetsProvider)
widgets_factory.register_widgets_provider("DBC", DBCWidgetsProvider)
