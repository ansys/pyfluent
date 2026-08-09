# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""REST settings service wrapper."""

from typing import Any

from ansys.fluent.core.rest.client import FluentRestClient
from ansys.fluent.core.services.abstract_settings import AbstractSettings
from ansys.fluent.core.services.settings import _trace

_REST_STATIC_INFO_KEY_MAP: dict[str, str] = {
    "object-type": "object_type",
    "include-child-named-objects?": "include_child_named_objects",
    "user-creatable?": "user_creatable",
    "has-allowed-values": "has_allowed_values",
    "file-purpose": "file_purpose",
    "api-exposure-level": "api_exposure_level",
    "deprecated-version": "deprecated_version",
    "return-type": "return_type",
    "child-aliases": "child_aliases",
    "command-aliases": "command_aliases",
    "query-aliases": "query_aliases",
    "arguments-aliases": "arguments_aliases",
    "allowed-values": "allowed_values",
    "has-migration-adapter?": "has_migration_adapter",
}

_REST_STATIC_INFO_CONTAINER_KEYS = ("children", "commands", "queries", "arguments")


def _normalize_static_info_keys(info: dict[str, Any]) -> dict[str, Any]:
    """Recursively translate REST's hyphenated schema keys to underscore form.

    Returns a new dict equivalent to *info* but with every key found in
    :data:`_REST_STATIC_INFO_KEY_MAP` renamed to its underscore form, applied
    recursively through ``children``/``commands``/``queries``/``arguments``
    (each a mapping of name -> nested schema dict) and ``object_type`` (a
    single nested schema dict). Keys not present in the map (e.g. ``type``,
    ``help``) are left untouched. Does not mutate *info*.
    """
    if not isinstance(info, dict):
        return info
    normalized = {}
    for key, value in info.items():
        new_key = _REST_STATIC_INFO_KEY_MAP.get(key, key)
        normalized[new_key] = value
    for container_key in _REST_STATIC_INFO_CONTAINER_KEYS:
        container = normalized.get(container_key)
        if isinstance(container, dict):
            normalized[container_key] = {
                name: _normalize_static_info_keys(child)
                for name, child in container.items()
            }
    object_type = normalized.get("object_type")
    if isinstance(object_type, dict):
        normalized["object_type"] = _normalize_static_info_keys(object_type)
    return normalized


def _apply_schema_corrections(
    info: dict[str, Any], name: str | None = None
) -> dict[str, Any]:
    """Apply client-side corrections to REST schema to handle server gaps.

    Some fields/aliases are missing from the server's static-info schema
    even though they appear in live object state and wire responses. This
    function patches the schema to include these known missing aliases.

    Parameters
    ----------
    info : dict[str, Any]
        Normalized schema dictionary (keys already converted to underscore
        form).
    name : str | None, optional
        The object's own name, e.g. ``"contour"``. This is only available
        from the parent's ``children`` mapping key - it is NOT the same as
        the ``type`` field (which is a structural type like ``"group"`` or
        ``"named-object"``, shared by many unrelated objects). Threaded
        through recursion so the ``missing_aliases`` lookup below can key
        off the real object name instead of the structural type.

    Returns
    -------
    dict[str, Any]
        Schema with corrections applied.
    """
    if not isinstance(info, dict):
        return info

    # Recursively apply corrections to nested structures, passing the child's
    # own name (the "children" dict key) down so it's available at the next
    # recursion level.
    corrected = dict(info)
    for container_key in _REST_STATIC_INFO_CONTAINER_KEYS:
        container = corrected.get(container_key)
        if isinstance(container, dict):
            corrected[container_key] = {
                child_name: _apply_schema_corrections(child, name=child_name)
                for child_name, child in container.items()
            }
    object_type = corrected.get("object_type")
    if isinstance(object_type, dict):
        corrected["object_type"] = _apply_schema_corrections(object_type, name=name)

    return corrected


class RestSettings(AbstractSettings):
    """REST-based settings service wrapper.

    This class provides high-level settings operations by delegating to a
    FluentRestClient instance. It is used for accessing and modifying Fluent
    settings over HTTP/REST transport.

    Available from Fluent 27.1 onward (v1 proto API).

    Parameters
    ----------
    rest_client : FluentRestClient
        The REST client instance to use for all settings operations.
    """

    def __init__(self, rest_client: FluentRestClient) -> None:
        """Initialize the REST settings service.

        Parameters
        ----------
        rest_client : FluentRestClient
            The REST client instance.
        """
        self.service = rest_client

    @_trace
    def set_var(self, path: str, value: Any) -> None:
        """Set the value for the given path."""
        self.service.set_var(path, value)

    @_trace
    def get_var(self, path: str) -> Any:
        """Get the value for the given path."""
        return self.service.get_var(path)

    @_trace
    def rename(self, path: str, new: str, old: str) -> None:
        """Rename the object at the given path."""
        self.service.rename(path, new, old)

    @_trace
    def create(
        self, path: str, name: str, properties: dict[str, Any] | None = None
    ) -> Any:
        """Create a named object child for the given path.

        Parameters
        ----------
        path : str
            DataModel path where the object will be created.
        name : str
            Name for the created object.
        properties : dict[str, Any], optional
            Properties to set on creation. Defaults to None.

        Returns
        -------
        Any
            Server response containing details of the created object.
        """
        return self.service.create(path, name, properties)

    @_trace
    def delete(self, path: str, name: str) -> None:
        """Delete the object with the given name at the given path."""
        self.service.delete(path, name)

    @_trace
    def get_object_names(self, path: str) -> list[str]:
        """Get a list of named objects."""
        return self.service.get_object_names(path)

    @_trace
    def get_list_size(self, path: str) -> int:
        """Get the number of elements in a list object."""
        return self.service.get_list_size(path)

    @_trace
    def resize_list_object(self, path: str, size: int) -> None:
        """Resize a list object."""
        self.service.resize_list_object(path, size)

    @_trace
    def get_static_info(self) -> dict[str, Any]:
        """Get static-info for settings.

        Requests the full schema (``full=True``) from the server. The
        settings class tree is built once from this response at session
        startup (see ``flobject.get_root()``), so anything missing here
        (e.g. nested children like ``momentum``/``range``, or a
        NamedObject's ``object_type``) is permanently missing from every
        object built for the life of the session. The abbreviated
        (``full=False``) schema was observed to omit exactly this kind of
        nested detail, causing spurious ``AttributeError``s far away from
        this call - request the full schema unconditionally.

        The raw REST response uses Fluent's native hyphenated/``?``-suffixed
        Scheme key names (e.g. ``object-type``, ``user-creatable?``); these
        are normalized to the underscore form ``flobject.get_cls()`` expects
        (matching gRPC) via :func:`_normalize_static_info_keys` before being
        returned, so no other module needs to know about this REST-specific
        wire format.

        Raises
        ------
        RuntimeError
            If type is empty.
        """
        return _apply_schema_corrections(
            _normalize_static_info_keys(self.service.get_static_info(full=True))
        )

    @_trace
    def execute_cmd(self, path: str, command: str, **kwds) -> Any:
        """Execute a given command with the provided keyword arguments.

        Parameters
        ----------
        path : str
            DataModel path for the command.
        command : str
            Command name to execute.
        **kwds : dict
            Command arguments, passed through to the server unchanged.

        Returns
        -------
        Any
            Command result (may be None).

        Notes
        -----
        List-type arguments (e.g. ``report_defs=["surface-1"]``) must be
        sent as flat lists. Live-server evidence confirmed that wrapping
        each item in an extra list (``[["surface-1"]]``, under the
        mistaken assumption that the server wants Scheme "alist"/pair
        format here) breaks the server's ``symbol->string`` call with
        ``HTTP 500: wta(1st) to symbol->string`` - the server expects a
        plain list of strings/symbols for this kind of argument, not a
        list of one-item lists.
        """
        return self.service.execute_cmd(path, command, **kwds)

    @_trace
    def execute_query(self, path: str, query: str, **kwds) -> Any:
        """Execute a given query with the provided keyword arguments."""
        return self.service.execute_query(path, query, **kwds)

    @_trace
    def get_attrs(self, path: str, attrs: list[str], recursive: bool = False) -> Any:
        """Return values of given attributes."""
        return self.service.get_attrs(path, attrs, recursive)

    @_trace
    def is_interactive_mode(self) -> bool:
        """Checks whether commands can be executed interactively.

        Returns
        ------
        bool
            Always False for REST transport (REST is stateless and non-interactive).
        """
        return False

    @_trace
    def is_wildcard(self, input: str | None = None) -> bool:
        """Check whether a name contains fnmatch wildcard characters (*, ?, [, ])."""
        if input is None:
            return False
        return any(c in input for c in "*?[]")

    @_trace
    def has_wildcard(self, name: str) -> bool:
        """Check whether a name contains fnmatch wildcard characters (*, ?, [, ])."""
        return self.is_wildcard(name)
