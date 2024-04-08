"""Module providing visualization objects to facilitate integration with libraries like
Matplotlib and pyvista."""

import inspect

from ansys.fluent.core.post_objects.meta import PyLocalContainer


class Container:
    """Base class for containers, for example, Plots, Graphics.

    Parameters
        ----------
        session : object
            Session object.
        container_type: object
            Container type (for example, Plots, Graphics)
        module: object
            Python module containing post definitions
        post_api_helper: object
            Provides helper APIs for post-processing
        local_surfaces_provider : object, optional
            Object providing local surfaces so that user can access surfaces
            created in other modules, such as PyVista. The default is ``None``.
    """

    def __init__(
        self,
        session,
        container_type,
        module,
        post_api_helper,
        local_surfaces_provider=None,
    ):
        """__init__ method of Container class."""
        session_state = container_type._sessions_state.get(session)
        self._path = container_type.__name__
        if not session_state:
            session_state = self.__dict__
            container_type._sessions_state[session] = session_state
            self.session = session
            self._init_module(self, module, post_api_helper)
        else:
            self.__dict__ = session_state
        self._local_surfaces_provider = lambda: local_surfaces_provider or getattr(
            self, "Surfaces", []
        )

    def get_path(self):
        """Get container path."""
        return self._path

    @property
    def type(self):
        """Type."""
        return "object"

    def update(self, value):
        """Update the value."""
        for name, val in value.items():
            o = getattr(self, name)
            o.update(val)

    def __call__(self, show_attributes=False):
        state = {}
        for name, cls in self.__dict__.items():
            o = getattr(self, name)
            if o is None or name.startswith("_") or name.startswith("__"):
                continue

            if cls.__class__.__name__ == "PyLocalContainer":
                container = o
                if getattr(container, "is_active", True):
                    state[name] = {}
                    for child_name in container:
                        o = container[child_name]
                        if getattr(o, "is_active", True):
                            state[name][child_name] = o()

        return state

    def _init_module(self, obj, mod, post_api_helper):
        for name, cls in mod.__dict__.items():
            if cls.__class__.__name__ in (
                "PyLocalNamedObjectMetaAbstract",
            ) and not inspect.isabstract(cls):
                setattr(
                    obj,
                    cls.PLURAL,
                    PyLocalContainer(self, cls, post_api_helper, cls.PLURAL),
                )


class Plots(Container):
    """Provides the Matplotlib ``Plots`` objects manager.

    This class provides access to ``Plots`` object containers for a given
    session so that plots can be created.

    Parameters
        ----------
        session : obj
            Session object.
        module: object
            Python module containing post definitions
        post_api_helper: object
            Provides helper APIs for post-processing
        local_surfaces_provider : object, optional
            Object providing local surfaces so that you can access surfaces
            created in other modules, such as pyvista. The default is ``None``.

    Attributes
    ----------
    XYPlots : dict
        Container for XY plot objects.
    MonitorPlots : dict
        Container for monitor plot objects.
    """

    _sessions_state = {}

    def __init__(self, session, module, post_api_helper, local_surfaces_provider=None):
        """__init__ method of Plots class."""
        super().__init__(
            session, self.__class__, module, post_api_helper, local_surfaces_provider
        )


class Graphics(Container):
    """Provides the pyvista ``Graphics`` objects manager.

    This class provides access to ``Graphics`` object containers for a given
    session so that graphics objects can be created.

    Parameters
    ----------
    session : obj
        Session object.
    module: object
        Python module containing post definitions
    post_api_helper: object
        Provides helper APIs for post-processing
    local_surfaces_provider : object, optional
        Object providing local surfaces so that you can access surfaces
        created in other modules, such as pyvista. The default is ``None``.

    Attributes
    ----------
    Meshes : dict
        Container for mesh objects.
    Surfaces : dict
        Container for surface objects.
    Contours : dict
        Container for contour objects.
    Vectors : dict
        Container for vector objects.
    """

    _sessions_state = {}

    def __init__(self, session, module, post_api_helper, local_surfaces_provider=None):
        """__init__ method of Graphics class."""
        super().__init__(
            session, self.__class__, module, post_api_helper, local_surfaces_provider
        )

    def add_outline_mesh(self):
        """Add a mesh outline.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        meshes = getattr(self, "Meshes", None)
        if meshes is not None:
            outline_mesh_id = "mesh-outline"
            outline_mesh = meshes[outline_mesh_id]
            outline_mesh.surfaces_list = [
                k
                for k, v in outline_mesh._api_helper.field_info()
                .get_surfaces_info()
                .items()
                if v["type"] == "zone-surf" and v["zone_type"] != "interior"
            ]
            return outline_mesh
