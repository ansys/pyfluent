"""Module providing remote and local objects handle."""

from typing import List, Optional, Tuple, Union

from ansys.fluent.gui.components.sessions_handle import SessionsHandle
from ansys.fluent.post.matplotlib import Plots
from ansys.fluent.post.pyvista import Graphics

SETTINGS_ID = "settings"
LOCAL_ID = "local"


class SettingsObjectsHandle:
    """Settings objects handle."""

    def get_object_and_static_info(
        self, user_id: str, session_id: str, object_path: str, object_name: str
    ) -> Tuple:

        """Get settings object and static info.
        Parameters
        ----------
        user_id : str
            User ID.
        session_id : str
            Session ID.
        object_path : str
            Settings object path e.g. setup/boundary_conditions/velocity_inlet
        object_name : str
            Object name.
        Returns
        --------
        Tuple
            Tuple containing settings object and static info.
        """

        session_handle = SessionsHandle(user_id, session_id)
        static_info = session_handle.static_info
        settings_root = session_handle.settings_root
        return self.extract_object_and_static_info(
            settings_root, static_info, object_path
        )

    def extract_object_and_static_info(
        self, obj, static_info: dict, path: str
    ) -> Tuple:

        """Extract settings object and static info from another object for a given path.
        Parameters
        ----------
        obj : object
            Settings object.
        static_info : dict
            Settings object static info.
        path : str
            Path for which settings object and static info is required.
        Returns
        --------
        Tuple
            Tuple containing settings object and static info.
        """

        path_list = path.split("/")
        for path in path_list:
            if static_info["type"] == "named-object":
                obj = obj[path]
                static_info = static_info["object-type"]
            else:
                obj = getattr(obj, path)
                static_info = static_info["children"][obj.obj_name]
        return obj, static_info


class LocalObjectsHandle:
    """Local objects handle."""

    def __init__(self):
        self._graphics_object_handle = _GraphicsObjectHandle()
        self._plots_object_handle = _PlotsObjectHandle()

    def add_outline_mesh(self, user_id: str, session_id: str) -> None:

        """Add outline mesh.
        Parameters
        ----------
        user_id : str
            User ID.
        session_id : str
            Session ID.

        Returns
        --------
        None
        """
        outline_mesh = self.get_object(user_id, session_id, "Mesh", "outline")
        outline_mesh.update(
            Graphics(SessionsHandle(user_id, session_id).session).add_outline_mesh()()
        )
        outline_mesh.show_edges = True

    def get_handle(
        self, object_path: str
    ) -> Union["_GraphicsObjectHandle", "_PlotsObjectHandle"]:
        """Get Object handle.
        Parameters
        ----------
        object_path : str
            Object path i.e. Contour, Vector, Mesh, Surface or XYPlot.

        Returns
        --------
        Union[_GraphicsObjectHandle, _PlotsObjectHandle]
            Object handle.
        """
        return (
            self._graphics_object_handle
            if self._graphics_object_handle._is_path_supported(object_path)
            else self._plots_object_handle
        )

    def get_object_names(
        self, user_id: str, session_id: str, object_path: str
    ) -> List[str]:
        """Get object names.
        Parameters
        ----------
        user_id : str
            User ID.
        session_id : str
            Session ID.
        object_path : str
            Object path i.e. Contour, Vector, Mesh, Surface or XYPlot.
        Returns
        --------
        List[str]
            List of child names.
        """
        collection = self.get_handle(object_path)._get_collection(
            user_id, session_id, object_path
        )
        indices = []
        if collection is not None:
            base_name = self._get_name(user_id, session_id, object_path, "")
            base_name_length = len(base_name)
            return [
                name[base_name_length:]
                for name in list(collection)
                if name.startswith(base_name)
            ]

    def create_object(
        self,
        user_id: str,
        session_id: str,
        object_path: str,
        from_name: Optional[str] = None,
    ) -> object:
        """Create a new object.
        Parameters
        ----------
        user_id : str
            User ID.
        session_id : str
            Session ID.
        object_path : str
            Object path i.e. Contour, Vector, Mesh, Surface, XYPlot
        from_name : str, optional
            If specified, properties of this object will be copied to new object.
        Returns
        --------
        object
            New object.
        """
        object_name = self._get_next_available_name(user_id, session_id, object_path)
        new_object = self.get_object(user_id, session_id, object_path, object_name)
        if new_object and from_name:
            from_object = self.get_object(user_id, session_id, object_path, from_name)
            new_object.update(from_object())
        return new_object

    def get_object(
        self, user_id: str, session_id: str, object_path: str, object_name: str
    ) -> object:
        """Get object.
        Parameters
        ----------
        user_id : str
            User ID.
        session_id : str
            Session ID.
        object_path : str
            Object path i.e. Contour, Vector, Mesh, Surface, XYPlot
        object_name : str
            Object name.
        Returns
        --------
        object
            Object.
        """
        collection = self.get_handle(object_path)._get_collection(
            user_id, session_id, object_path
        )
        if collection is not None:
            object_name = self._get_name(user_id, session_id, object_path, object_name)
            return collection[object_name]

    def delete_object(
        self, user_id: str, session_id: str, object_path: str, object_name: str
    ):
        """Delete object.
        Parameters
        ----------
        user_id : str
            User ID.
        session_id : str
            Session ID.
        object_path : str
            Object path i.e. Contour, Vector, Mesh, Surface, XYPlot
        object_name : str
            Object name.
        Returns
        --------
        None
        """
        collection = self.get_handle(object_path)._get_collection(
            user_id, session_id, object_path
        )
        if collection is not None:
            object_name = self._get_name(user_id, session_id, object_path, object_name)
            del collection[object_name]

    def _get_name(self, user_id, session_id, object_path, object_name):
        return f"{SessionsHandle(user_id, session_id)._unique_id}-{object_path}-{object_name}"

    def _get_next_available_name(self, user_id, session_id, object_path):
        collection = self.get_handle(object_path)._get_collection(
            user_id, session_id, object_path
        )
        if collection is not None:
            id = 0
            while True:
                object_name = self._get_name(
                    user_id, session_id, object_path, f"{object_path}-{id}"
                )
                if object_name not in list(collection):
                    break
                id = id + 1
            return f"{object_path.split('/')[-1]}-{id}"


class _GraphicsObjectHandle:
    @property
    def type(self):
        return "graphics"

    def _is_path_supported(self, type):
        return type in ("Contour", "Mesh", "Vector", "Surface")

    def _get_collection(self, user_id, session_id, object_path):
        session = SessionsHandle(user_id, session_id).session
        if session:
            graphics_session = Graphics(session)
            if object_path == "Contour":
                return graphics_session.Contours
            if object_path == "Mesh":
                return graphics_session.Meshes
            if object_path == "Vector":
                return graphics_session.Vectors
            if object_path == "Surface":
                return graphics_session.Surfaces


class _PlotsObjectHandle:
    def _is_path_supported(self, type):
        return type in ("XYPlot")

    @property
    def type(self):
        return "plot"

    def _get_collection(self, user_id, session_id, object_path):
        session = SessionsHandle(user_id, session_id).session
        plots_session = Plots(session)
        if object_path == "XYPlot":
            return plots_session.XYPlots
