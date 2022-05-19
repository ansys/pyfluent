from ansys.fluent.post.matplotlib import Plots
from ansys.fluent.post.pyvista import Graphics
from ansys.fluent.post.pyvista.pyvista_objects import Contour, Mesh, Surface, Vector


class SettingsObjectsHandle:
    def __init__(self, sessions_handle):
        self._sessions_handle = sessions_handle

    def get_object_and_static_info(
        self, user_id, session_id, object_type, object_index
    ):
        session_handle = self._sessions_handle(user_id, session_id)
        static_info = session_handle.static_info
        settings_root = session_handle.settings_root
        return self.extract_object_and_static_info(
            settings_root, static_info, object_type
        )

    def extract_object_and_static_info(self, obj, static_info, path):
        path_list = path.split("/")
        for path in path_list:
            try:
                obj = getattr(obj, path)
                static_info = static_info["children"][obj.obj_name]
            except AttributeError:
                obj = obj[path]
                static_info = static_info["object-type"]
        return obj, static_info


class LocalObjectsHandle:
    def __init__(self, sessions_handle):
        self._sessions_handle = sessions_handle
        self._graphics_object_handle = GraphicsObjectHandle(sessions_handle)
        self._plots_object_handle = PlotsObjectHandle(sessions_handle)

    def _get_name(self, user_id, session_id, object_type, object_index):
        return f"{self._sessions_handle(user_id, session_id)._complete_session_id}-{object_type}-{object_index}"

    def add_outline_mesh(self, user_id, session_id):
        outline_mesh = self.get_object(user_id, session_id, "Mesh", "outline")
        outline_mesh.update(
            Graphics(
                self._sessions_handle(user_id, session_id).session
            ).add_outline_mesh()()
        )
        outline_mesh.show_edges = True

    def get_handle(self, object_type):
        return (
            self._graphics_object_handle
            if self._graphics_object_handle.is_type_supported(object_type)
            else self._plots_object_handle
        )

    def get_child_indices(self, user_id, session_id, object_type):
        collection = self.get_handle(object_type).get_collection(
            user_id, session_id, object_type
        )
        indices = []
        if collection is not None:
            base_name = self._get_name(user_id, session_id, object_type, "")
            for name in list(collection):
                if name.startswith(base_name):
                    indices.append(name.split("-")[-1])
        return indices

    def create_new_object(self, user_id, session_id, object_type, from_index):
        object_index = self.get_next_index(user_id, session_id, object_type)
        new_object = self.get_object(user_id, session_id, object_type, object_index)
        from_object = self.get_object(user_id, session_id, object_type, from_index)
        new_object.update(from_object())
        return new_object

    def get_next_index(self, user_id, session_id, object_type):
        collection = self.get_handle(object_type).get_collection(
            user_id, session_id, object_type
        )
        if collection is not None:
            object_index = 0
            while True:
                object_name = self._get_name(
                    user_id, session_id, object_type, object_index
                )
                if object_name not in list(collection):
                    break
                object_index = object_index + 1
            return object_index

    def get_object(self, user_id, session_id, object_type, object_index):
        collection = self.get_handle(object_type).get_collection(
            user_id, session_id, object_type
        )
        if collection is not None:

            object_name = self._get_name(user_id, session_id, object_type, object_index)
            return collection[object_name]

    def delete_object(self, user_id, session_id, object_type, object_index):
        collection = self.get_handle(object_type).get_collection(
            user_id, session_id, object_type
        )
        if collection is not None:
            object_name = self._get_name(user_id, session_id, object_type, object_index)
            del collection[object_name]


class GraphicsObjectHandle:
    def __init__(self, sessions_handle):
        self.sessions_handle = sessions_handle

    @property
    def type(self):
        return "graphics"

    def is_type_supported(self, type):
        return type in ("Contour", "Mesh", "Vector", "Surface")

    def get_collection(self, user_id, session_id, object_type):
        session = self.sessions_handle(user_id, session_id).session
        if session:
            graphics_session = Graphics(session)
            if object_type == "Contour":
                return graphics_session.Contours
            if object_type == "Mesh":
                return graphics_session.Meshes
            if object_type == "Vector":
                return graphics_session.Vectors
            if object_type == "Surface":
                return graphics_session.Surfaces


class PlotsObjectHandle:
    def __init__(self, sessions_handle):
        self.sessions_handle = sessions_handle

    def is_type_supported(self, type):
        return type in ("XYPlot")

    @property
    def type(self):
        return "plot"

    def get_collection(self, user_id, session_id, object_type):
        session = self.sessions_handle(user_id, session_id).session
        plots_session = Plots(session)
        if object_type == "XYPlot":
            return plots_session.XYPlots
