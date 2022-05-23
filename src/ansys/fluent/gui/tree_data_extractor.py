import os

from objects_handle import LocalObjectsHandle, SettingsObjectsHandle
from sessions_handle import SessionsHandle
import yaml


class TreeDataExtractor:
    def __init__(self, user_id, session_id):
        self._user_id = user_id
        self._session_id = session_id

    def extract_tree_data(self, data):
        children = []
        keys = []
        for item_name, item_data in data.items():
            tree_data = {}
            tree_data["title"] = item_name
            icon = item_data.get("icon")
            remote = item_data.get("remote")
            local = item_data.get("local")
            index = item_data.get("index", "")

            key = item_name
            if local:
                key = f"local:{local}:{index}"
            elif remote:
                key = f"remote:{remote}:{index}"

            tree_data["key"] = key
            keys.append(key)
            tree_data["icon"] = icon

            if item_data.get("children"):
                tree_data["children"], child_keys = self.extract_tree_data(
                    item_data["children"]
                )
                keys = keys + child_keys
            elif local:
                handle = LocalObjectsHandle()
                indices = handle.get_child_indices(
                    self._user_id,
                    self._session_id,
                    f"{local}-{index}" if index else local,
                )
                if indices:
                    children_data = {
                        f"{local}-{index}": {
                            "local": f"{local}",
                            "index": f"{index}",
                            "icon": icon,
                        }
                        for index in indices
                        if index
                    }
                    tree_data["children"], child_keys = self.extract_tree_data(
                        children_data
                    )
                    keys = keys + child_keys
            elif remote:
                session_handle = SessionsHandle(
                    self._user_id, self._session_id
                )
                static_info = session_handle.static_info
                root = session_handle.settings_root                           
                handle = SettingsObjectsHandle()
                obj, static_info = handle.extract_object_and_static_info(root, static_info, remote)  
                if static_info["type"] == "named-object":
                    tree_data["key"] = item_name
                    if not obj.is_active():
                        continue
                    children_name = obj.get_object_names()
                    if children_name:                   
                        children_data = {
                            child: {"remote": f"{remote}/{child}", "icon": icon}
                            for child in children_name
                        }
                        tree_data["children"], child_keys = self.extract_tree_data(
                            children_data
                        )
                        keys = keys + child_keys
            children.append(tree_data)

        return children, keys

    def get_tree_nodes(
        self,
        yaml_file="outline.yaml",
    ):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(dir_path, "assets", "outline", yaml_file)) as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
            tree_nodes, keys = self.extract_tree_data(data)
        return tree_nodes[0], keys
