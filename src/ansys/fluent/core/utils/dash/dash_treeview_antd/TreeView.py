# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class TreeView(Component):
    """A TreeView component.
    TreeView component for Dash

    Keyword arguments:
    - id (string; optional): The ID used to identify this component in Dash callbacks
    - checkable (boolean; optional): Adds a Checkbox before the treeNodes (Default - false)
    - multiple (boolean; optional): Allows selecting multiple treeNodes (Default - false)
    - data (optional): Tree data
    - checked (list; optional): List of keys of checked nodes.
    - selected (list; optional): List of keys of selected nodes.
    - expanded (list; optional): List of keys of expanded nodes.

    Available events:"""

    @_explicitize_args
    def __init__(
        self,
        id=Component.UNDEFINED,
        checkable=Component.UNDEFINED,
        multiple=Component.UNDEFINED,
        data=Component.UNDEFINED,
        checked=Component.UNDEFINED,
        selected=Component.UNDEFINED,
        expanded=Component.UNDEFINED,
        **kwargs
    ):
        self._prop_names = [
            "id",
            "checkable",
            "multiple",
            "data",
            "checked",
            "selected",
            "expanded",
        ]
        self._type = "TreeView"
        self._namespace = "dash_treeview_antd"
        self._valid_wildcard_attributes = []
        self.available_events = []
        self.available_properties = [
            "id",
            "checkable",
            "multiple",
            "data",
            "checked",
            "selected",
            "expanded",
        ]
        self.available_wildcard_properties = []

        _explicit_args = kwargs.pop("_explicit_args")
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != "children"}

        for k in []:
            if k not in args:
                raise TypeError("Required argument `" + k + "` was not specified.")
        super(TreeView, self).__init__(**args)

    def __repr__(self):
        if any(
            getattr(self, c, None) is not None
            for c in self._prop_names
            if c is not self._prop_names[0]
        ) or any(
            getattr(self, c, None) is not None
            for c in self.__dict__.keys()
            if any(c.startswith(wc_attr) for wc_attr in self._valid_wildcard_attributes)
        ):
            props_string = ", ".join(
                [
                    c + "=" + repr(getattr(self, c, None))
                    for c in self._prop_names
                    if getattr(self, c, None) is not None
                ]
            )
            wilds_string = ", ".join(
                [
                    c + "=" + repr(getattr(self, c, None))
                    for c in self.__dict__.keys()
                    if any(
                        [
                            c.startswith(wc_attr)
                            for wc_attr in self._valid_wildcard_attributes
                        ]
                    )
                ]
            )
            return (
                "TreeView("
                + props_string
                + (", " + wilds_string if wilds_string != "" else "")
                + ")"
            )
        else:
            return "TreeView(" + repr(getattr(self, self._prop_names[0], None)) + ")"
