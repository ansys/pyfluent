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
