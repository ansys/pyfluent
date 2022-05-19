"""Module providing outline component."""

import os
from typing import Optional

from app_defn import app
import dash
from dash import ALL, Input, Output, html
from dash.exceptions import PreventUpdate
from pyfluent_dash_components import Outline as RCTree
import yaml

from ansys.fluent.gui.components.component_base import ComponentBase
from ansys.fluent.gui.components.objects_handle import (
    LOCAL_ID,
    SETTINGS_ID,
    LocalObjectsHandle,
    SettingsObjectsHandle,
)
from ansys.fluent.gui.components.sessions_handle import SessionsHandle


class Outline(ComponentBase):
    """``Outline`` component.

    Component for rendering hierarchy.
    """

    _objects = {}

    def __init__(self, user_id, session_id, index=None):
        unique_id = f"{user_id}-{session_id}-{'defaut' if index is None else index}"
        outline = Outline._objects.get(unique_id)
        if not outline:
            Outline._objects[unique_id] = self.__dict__
            self._unique_id = unique_id
            self._user_id = user_id
            self._session_id = session_id
            self._index = index
            self._yaml_file = None

            @app.callback(
                Output(f"outline-container-{unique_id}", "children"),
                Input(
                    {"type": "graphics-button", "index": ALL},
                    "n_clicks",
                ),
                prevent_initial_call=True,
            )
            def update_outline(graphics_button_clicks):
                if not graphics_button_clicks or graphics_button_clicks[0] == 0:
                    raise PreventUpdate

                ctx = dash.callback_context
                triggered_data = eval(ctx.triggered[0]["prop_id"].split(".")[0])
                (
                    user_id,
                    session_id,
                    location_id,
                    object_path,
                    object_name,
                    operation,
                    editor_id,
                ) = triggered_data["index"].split(":")
                if operation == "new":
                    handle = LocalObjectsHandle()
                    handle.create_object(user_id, session_id, object_path, object_name)
                elif operation == "delete":
                    handle = LocalObjectsHandle()
                    handle.delete_object(user_id, session_id, object_path, object_name)

                return self.render()

        else:
            self.__dict__ = outline

    def render(self) -> RCTree:
        """Render ``Outline`` component.
        Parameters
        ----------
        None

        Returns
        --------
        RCTree
            RCTree component.
        """
        if self._yaml_file is None:
            return []
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(
            os.path.join(dir_path, os.path.pardir, "assets", "outline", self._yaml_file)
        ) as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
            tree_nodes, keys = self._extract_outline_data(data)

        return RCTree(
            id={
                "type": "outline",
                "index": f"{self._user_id}:{self._session_id}:{self._index}",
            },
            data=tree_nodes[0],
            selected=[],
            expandedKeys=["Root"] + keys,
        )

    def __call__(self, yaml_file: Optional[str] = "outline.yaml") -> html.Div:
        """Render customized ``Outline`` component within container.
        Parameters
        ----------
        yaml_file : str
            YAML file name describing outline hierarchy. It must reside inside
            assets/outline folder.

        Returns
        --------
        html.Div
            Customized ``Outline`` component within html.Div container.
        """
        self._yaml_file = yaml_file
        return html.Div(self.render(), id=f"outline-container-{self._unique_id}")

    def _extract_outline_data(self, data):
        children = []
        keys = []
        for item_name, item_data in data.items():
            tree_data = {}
            tree_data["title"] = item_name
            icon = item_data.get("icon")
            settings_path = item_data.get("settings-path")
            local_path = item_data.get("local-path")
            object_name = item_data.get("object-name", "")

            key = item_name
            if local_path:
                key = f"{LOCAL_ID}:{local_path}:{object_name}"
            elif settings_path:
                key = f"{SETTINGS_ID}:{settings_path}:{object_name}"

            tree_data["key"] = key
            tree_data["icon"] = icon
            keys.append(key)

            if item_data.get("children"):
                tree_data["children"], child_keys = self._extract_outline_data(
                    item_data["children"]
                )
                keys = keys + child_keys
            elif local_path:
                if not object_name:
                    handle = LocalObjectsHandle()
                    child_names = handle.get_object_names(
                        self._user_id, self._session_id, local_path
                    )
                    if child_names:
                        children_data = {
                            child_name: {
                                "local-path": f"{local_path}",
                                "object-name": f"{child_name}",
                                "icon": icon,
                            }
                            for child_name in child_names
                            if child_name
                        }
                        tree_data["children"], child_keys = self._extract_outline_data(
                            children_data
                        )
                        keys = keys + child_keys
            elif settings_path:
                session_handle = SessionsHandle(self._user_id, self._session_id)
                static_info = session_handle.static_info
                root = session_handle.settings_root
                handle = SettingsObjectsHandle()
                obj, static_info = handle.extract_object_and_static_info(
                    root, static_info, settings_path
                )
                if static_info["type"] == "named-object":
                    tree_data["key"] = item_name
                    if not obj.is_active():
                        continue
                    children_name = obj.get_object_names()
                    if children_name:
                        children_data = {
                            child: {
                                "settings-path": f"{settings_path}/{child}",
                                "icon": icon,
                            }
                            for child in children_name
                        }
                        tree_data["children"], child_keys = self._extract_outline_data(
                            children_data
                        )
                        keys = keys + child_keys
            children.append(tree_data)

        return children, keys
