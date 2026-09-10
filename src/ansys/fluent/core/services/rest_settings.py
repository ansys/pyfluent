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
from ansys.fluent.core.services.settings import BaseSettings, _trace

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
    """Recursively rename REST's hyphenated schema keys to underscore form.

    Applied through ``children``/``commands``/``queries``/``arguments`` and
    ``object_type``. Unmapped keys are left untouched. Does not mutate *info*.
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


class RestSettings(BaseSettings):
    """REST-based settings service wrapper.

    This class provides high-level settings operations by delegating to a
    FluentRestClient instance. It is used for accessing and modifying Fluent
    settings over HTTP/REST transport.

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
        super().__init__(rest_client)
        self._static_info_cache: dict[str, Any] | None = None

    @_trace
    def get_static_info(self) -> dict[str, Any]:
        """Get static-info for settings.

        Always requests the full schema (``full=True``); the abbreviated form
        omits nested details (e.g. ``momentum``/``range`` children, a
        NamedObject's ``object_type``) needed to build the settings class
        tree. Keys are normalized from REST's hyphenated/``?``-suffixed form
        to the underscore form ``flobject.get_cls()`` expects (matching gRPC).

        Raises
        ------
        RuntimeError
            If type is empty.
        """
        return _normalize_static_info_keys(self.service.get_static_info(full=True))

    @_trace
    def is_wildcard(self, input: str | None = None) -> bool:
        """Check whether a name contains a wildcard pattern.

        ``AbstractSettings`` requires this, but the REST API exposes no
        equivalent of the gRPC ``Settings.IsWildcard`` endpoint, so the
        fnmatch metacharacters are matched client-side instead.
        """
        if input is None:
            return False
        return any(c in input for c in "*?[]")

    @_trace
    def has_wildcard(self, name: str) -> bool:
        """Check whether a name has a wildcard pattern."""
        return self.is_wildcard(name)

    @_trace
    def execute_cmd(self, path: str, command: str, **kwds) -> Any:
        """Execute a given command with the provided keyword arguments.

        The REST endpoint wraps the actual return value in an envelope of
        the form ``{"result": <value>, "output": <console text>}``. Unwrap
        it here so callers see the same plain value that the gRPC service
        returns, instead of the raw envelope.
        """
        return _unwrap_result(self.service.execute_cmd(path, command, **kwds))

    @_trace
    def execute_query(self, path: str, query: str, **kwds) -> Any:
        """Execute a given query with the provided keyword arguments.

        See :meth:`execute_cmd` for why the response is unwrapped.
        """
        return _unwrap_result(self.service.execute_query(path, query, **kwds))

    @_trace
    def get_attrs(self, path: str, attrs: list[str], recursive: bool = False) -> Any:
        """Return values of given attributes.

        For ``recursive=False``, delegates to the raw service unchanged (zero
        behavior change for the common case). For ``recursive=True``, uses
        ``_reshape_recursive_attrs`` to normalize the server's response into
        the gRPC-compatible shape: ``{"attrs": {...}, "group_children":
        {name: {...}}}`` for both real settings groups (whose children the
        server nests under ``"children"``) and command-argument descendants
        (whose children the server never nests, requiring client-side
        recursive reconstruction).
        """
        raw = self.service.get_attrs(path, attrs, recursive)
        if not recursive:
            return raw
        return self._reshape_recursive_attrs(raw, path, attrs)

    def _cached_static_info(self) -> dict[str, Any]:
        """Memoized call to ``get_static_info()``.

        Caches the server's full schema to avoid repeated network round-trips
        during recursive ``_schema_node_for_path()`` lookups.
        """
        if self._static_info_cache is None:
            self._static_info_cache = self.get_static_info()
        return self._static_info_cache

    def _schema_node_for_path(self, path: str) -> dict[str, Any]:
        """Walk the cached static-info schema to find the node at a given path.

        Navigates the schema tree by splitting ``path`` on "/" and checking
        ``"children"``, ``"commands"``, and ``"queries"`` containers at each
        level.
        """
        schema = self._cached_static_info()
        node = schema
        for component in path.split("/"):
            if not component:
                continue
            # Try children, commands, queries in that order
            for container_key in ("children", "commands", "queries"):
                if container_key in node and component in node[container_key]:
                    node = node[container_key][component]
                    break
            else:
                # No matching container found, return empty dict as fallback
                return {}
        return node

    def _reshape_recursive_attrs(self, raw: Any, path: str, attrs: list[str]) -> Any:
        """Reshape a recursive ``get_attrs`` response into gRPC-compatible form.

        Converts the server's response (which uses ``"children"`` for real
        settings groups) into the gRPC-compatible shape ``{"attrs": {...},
        "group_children": {...}}``, and reconstructs ``"group_children"``
        entries for command-argument descendants that the server never nests.
        """
        if not isinstance(raw, dict):
            return raw

        # Extract existing "children" (for real settings groups)
        result = {"attrs": raw.get("attrs", {})}
        group_children = {}

        if "children" in raw:
            for child_name, child_data in raw["children"].items():
                # Recursively reshape each child
                reshaped_child = self._reshape_recursive_attrs(
                    child_data, f"{path}/{child_name}", attrs
                )
                group_children[child_name] = reshaped_child

        # Fetch command-argument descendants (schema nodes with "arguments")
        schema_node = self._schema_node_for_path(path)
        if "arguments" in schema_node:
            for arg_name in schema_node["arguments"]:
                if arg_name not in group_children:
                    # Recursively fetch this argument's attrs
                    arg_attrs = self.get_attrs(
                        f"{path}/{arg_name}", attrs, recursive=True
                    )
                    group_children[arg_name] = arg_attrs

        # Only include group_children if non-empty (mirrors gRPC behavior)
        if group_children:
            result["group_children"] = group_children

        return result

    @property
    def supports_deprecation_echo(self) -> bool:
        """REST has no scheme/TUI-eval endpoint to capture the deprecation echo.

        Confirmed empirically: ``GET api/fluent_1/{scheme-eval,tui,console,
        journal}`` all return HTTP 404, and the command envelope's
        ``"output"`` field (which does carry genuine console text for
        commands that print, e.g. ``list``) stays empty for aliased
        commands such as ``copy``/``make-a-copy`` -- there is no channel to
        toggle Scheme's ``api-echo-python-port`` over REST. See
        ``_Alias._print_newer_api`` for the gRPC-side mechanism this
        would otherwise mirror.
        """
        return False


def _unwrap_result(response: Any) -> Any:
    """Extract the ``"result"`` value from a command/query response envelope.

    The REST API returns ``{"result": <value>, "output": <text>}`` for
    command/query execution. Responses without a ``"result"`` key are
    returned unchanged (defensive fallback).
    """
    if isinstance(response, dict) and "result" in response:
        return response["result"]
    return response
