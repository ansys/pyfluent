"""Module proving progress bar component."""

from typing import Optional

from app_defn import app
from dash import Input, Output, html
import dash_bootstrap_components as dbc

from ansys.fluent.gui.components.component_base import ComponentBase
from ansys.fluent.gui.components.sessions_handle import SessionsHandle


class ProgressBar(ComponentBase):
    """``ProgressBar`` component.

    Component for rendering solution progress.
    """

    _objects = {}

    def __init__(self, user_id, session_id, index=None):
        unique_id = f"{user_id}-{session_id}-{'defaut' if index is None else index}"
        progress_bar = ProgressBar._objects.get(unique_id)
        if not progress_bar:
            ProgressBar._objects[unique_id] = self.__dict__
            self._unique_id = unique_id
            self._user_id = user_id
            self._session_id = session_id

            @app.callback(
                Output(f"progress-bar-{unique_id}", "value"),
                Output(f"progress-bar-{unique_id}", "label"),
                Output(f"progress-messgae-{unique_id}", "children"),
                Input("interval-component", "n_intervals"),
                prevent_initial_call=True,
            )
            def on_progress_update(n_intervals):
                event_info = SessionsHandle(user_id, session_id).get_event_info(
                    "ProgressEvent"
                )
                return [
                    event_info.percentComplete if event_info else 0,
                    str(event_info.percentComplete) + "%" if event_info else "",
                    event_info.message if event_info else "",
                ]

        else:
            self.__dict__ = progress_bar

    def render(self) -> html.Div:
        """Render ``ProgressBar`` component.
        Parameters
        ----------
        None

        Returns
        --------
        html.Div
            html.Div as ``ProgressBar`` component.
        """
        return html.Div(
            [
                dbc.Label(
                    id=f"progress-messgae-{self._unique_id}",
                    style={"width": "auto", "height": f"{self._height}px"},
                ),
                dbc.Progress(
                    id=f"progress-bar-{self._unique_id}",
                    value=0,
                    label="",
                    style={
                        "width": "100%",
                        "height": f"{self._height}px",
                        "background-color": "#f8f9fa",
                    },
                ),
            ],
            style={
                "display": "flex",
                "flex-direction": "row",
                "height": f"{self._height}px",
                "width": "100%",
            },
        )

    def __call__(self, height: Optional[int] = 32) -> html.Div:
        """Render customized ``ProgressBar`` component.
        Parameters
        ----------
        height : int, optional
            ``ProgressBar`` height.

        Returns
        --------
        html.Div
            Customized ``ProgressBar`` component within html.Div container.
        """
        self._height = height
        return html.Div(
            self.render(),
            id=f"progress-container-{self._unique_id}",
        )
