from ansys.fluent.post.pyvista import Graphics
from ansys.fluent.post.matplotlib import Plots
from ansys.fluent.post.pyvista.pyvista_objects import (
    Contour,
    Mesh,
    Surface,
    Vector,
)


from app_defn import app

class LocalObjectsHandle:
    def __init__(self, session_manager):     
        self._session_manager = session_manager
        self._graphics_object_handle = GraphicsObjectHandle(session_manager)
        self._plots_object_handle = PlotsObjectHandle(session_manager) 

    def _get_name(self, connection_id, session_id, object_type, object_index):
        return f"{self._session_manager(app, connection_id, session_id)._complete_session_id}-{object_type}-{object_index}" 
        
    def add_outline_mesh(self, user_id, session_id):        
        outline_mesh = self._get_object(
            user_id, session_id, "Mesh", "outline"
        )
        outline_mesh.update(Graphics(self._session_manager(app, user_id, session_id).session).add_outline_mesh()())
        outline_mesh.show_edges = True    

    def get_handle(self, object_type):
        return (
            self._graphics_object_handle
            if self._graphics_object_handle.is_type_supported(object_type)
            else self._plots_object_handle
        )        
        
    def get_handle_type(self, object_type):
        return self.get_handle(object_type).get_handle_type()    
        
    def get_child_indices(self, connection_id, session_id, object_type):
        collection = self.get_handle(object_type).get_collection(
            connection_id, session_id, object_type
        )
        indices = []
        if collection is not None:
            base_name = self._get_name(connection_id, session_id, object_type, "")
            for name in list(collection):
                if name.startswith(base_name):
                    indices.append(name.split("-")[-1])
        return indices


    def create_new_object(self, connection_id, session_id, object_type, from_index):
        object_index = self.get_next_index(connection_id, session_id, object_type)
        new_object = self._get_object(
            connection_id, session_id, object_type, object_index
        )
        from_object = self._get_object(
            connection_id, session_id, object_type, from_index
        )
        new_object.update(from_object())
        return new_object

    def get_next_index(self, connection_id, session_id, object_type):
        collection = self.get_handle(object_type).get_collection(
            connection_id, session_id, object_type
        )
        if collection is not None:
            object_index = 0
            while True:
                object_name = self._get_name(
                    connection_id, session_id, object_type, object_index
                )
                if object_name not in list(collection):
                    break
                object_index = object_index + 1
            return object_index

    def _get_object(self, connection_id, session_id, object_type, object_index):
        collection = self.get_handle(object_type).get_collection(
            connection_id, session_id, object_type
        )
        if collection is not None:

            object_name = self._get_name(
                connection_id, session_id, object_type, object_index
            )
            return collection[object_name]

    def delete_object(self, connection_id, session_id, object_type, object_index):
        collection = self.get_handle(object_type).get_collection(
            connection_id, session_id, object_type
        )
        if collection is not None:
            object_name = self._get_name(
                connection_id, session_id, object_type, object_index
            )
            del collection[object_name]

    def get_object_and_static_info(
        self, connection_id, session_id, object_type, object_index
    ):
        return (
            self._get_object(connection_id, session_id, object_type, object_index),
            None,
        )
        
        

class GraphicsObjectHandle:
    def __init__(self, session_manager):       
        self.session_manager = session_manager
        
    def get_handle_type(self):
        return "graphics"

    def is_type_supported(self, type):
        return type in ("Contour", "Mesh", "Vector", "Surface")

    def get_collection(self, connection_id, session_id, object_type):
        session = self.session_manager(app, connection_id, session_id).session
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
    def __init__(self, session_manager):       
        self.session_manager = session_manager

    def is_type_supported(self, type):
        return type in ("XYPlot")
        
    def get_handle_type(self):
        return "plot"        

    def get_collection(self, connection_id, session_id, object_type):
        session = self.session_manager(app, connection_id, session_id).session
        plots_session = Plots(session)
        if object_type == "XYPlot":
            return plots_session.XYPlots           