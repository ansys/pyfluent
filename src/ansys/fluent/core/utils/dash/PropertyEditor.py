from dash.dependencies import Input, Output, State, MATCH, ALL
import dash
from dash.exceptions import PreventUpdate
from dash import html
from local_property_editor import LocalPropertyEditor
from settings_property_editor import SettingsPropertyEditor
from ansys.fluent.core.utils.generic import SingletonMeta
from ansys.fluent.core.solver.flobject import to_python_name


class PropertyEditor(metaclass=SingletonMeta):
    def __init__(self, app, SessionsManager):
        self._app = app
        self._remote_property_editor = SettingsPropertyEditor(app, SessionsManager)
        self._local_property_editor = LocalPropertyEditor(app, SessionsManager)
