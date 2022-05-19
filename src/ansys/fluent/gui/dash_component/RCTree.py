# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class RCTree(Component):
    """A RCTree component.

    Keyword arguments:

    - id (optional):
        The ID used to identify this component in Dash callbacks.

    - data (optional):
        Tree data.

    - expandedKeys (optional):
        List of keys of expanded nodes.

    - selected (optional):
        List of keys of selected nodes.

    - setProps (optional):
        Dash-assigned callback that should be called whenever any of the
        properties change.
    """

    @_explicitize_args
    def __init__(
        self,
        id=Component.UNDEFINED,
        selected=Component.UNDEFINED,
        expandedKeys=Component.UNDEFINED,
        data=Component.UNDEFINED,
        **kwargs
    ):
        self._prop_names = ["id", "data", "expandedKeys", "selected", "setProps"]
        self._type = "RCTree"
        self._namespace = "dash_component"
        self._valid_wildcard_attributes = []
        self.available_properties = [
            "id",
            "data",
            "expandedKeys",
            "selected",
            "setProps",
        ]
        self.available_wildcard_properties = []
        _explicit_args = kwargs.pop("_explicit_args")
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != "children"}
        for k in []:
            if k not in args:
                raise TypeError("Required argument `" + k + "` was not specified.")
        super(RCTree, self).__init__(**args)
