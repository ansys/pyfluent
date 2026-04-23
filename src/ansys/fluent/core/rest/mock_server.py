# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
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

"""Lightweight in-process HTTP mock server for the Fluent DataModel REST API.

Uses only the Python standard library (``http.server``, ``threading``,
``socketserver``).  No Flask or any external packages are required.

The server mimics the SimBA (Simulation Bridge Application) embedded in the
Fluent solver and uses the same URL scheme::

    /api/{component}/...

where *component* defaults to ``"fluent_1"``.

Endpoints implemented
---------------------

.. code-block:: text

    GET  /api/fluent_1/static-info
    POST /api/fluent_1/get_var          body: {"path": ...}
    POST /api/fluent_1/get_attrs        body: {"path": ..., "attrs": [...]}
    GET  /api/fluent_1/{dmpath}         returns value, names or size
    PUT  /api/fluent_1/{dmpath}         set value / resize / rename
    POST /api/fluent_1/{dmpath}         create named object or execute cmd/query
    DELETE /api/fluent_1/{dmpath}       delete named object

Usage
-----
::

    from ansys.fluent.core.rest import FluentRestMockServer, FluentRestClient

    server = FluentRestMockServer().start()
    client = FluentRestClient(server.base_url)
    print(client.get_var("setup/models/energy/enabled"))  # True
    server.stop()

Pytest fixture
--------------
::

    import pytest
    from ansys.fluent.core.rest import FluentRestMockServer, FluentRestClient

    @pytest.fixture()
    def rest_client():
        server = FluentRestMockServer().start()
        yield FluentRestClient(server.base_url)
        server.stop()
"""

import copy
from http.server import BaseHTTPRequestHandler
import json
import socketserver
import threading
from typing import Any
import urllib.parse

# ---------------------------------------------------------------------------
# Pre-populated settings store
# ---------------------------------------------------------------------------

#: Default in-memory settings tree.  Keys are slash-delimited Fluent paths.
_DEFAULT_VARS: dict[str, Any] = {
    # General solver settings
    "setup/general/solver/time": "steady",
    "setup/general/solver/velocity_formulation": "absolute",
    "setup/general/gravity/enabled": False,
    # Energy model
    "setup/models/energy/enabled": True,
    # Viscous model
    "setup/models/viscous/model": "k-epsilon",
    "setup/models/viscous/k_epsilon_model": "standard",
    # Boundary conditions – velocity inlet
    "setup/boundary_conditions/velocity_inlet/inlet/momentum/velocity_magnitude/value": 1.0,
    "setup/boundary_conditions/velocity_inlet/inlet/momentum/velocity_magnitude/units": "m/s",
    # Boundary conditions – pressure outlet
    "setup/boundary_conditions/pressure_outlet/outlet/momentum/gauge_pressure/value": 0.0,
    # Solution controls
    "solution/methods/p_v_coupling/scheme": "simple",
    "solution/controls/under_relaxation/pressure": 0.3,
    "solution/controls/under_relaxation/velocity": 0.7,
    "solution/run_calculation/iter_count": 100,
    "solution/initialization/initialization_methods": "standard",
}

#: Named-object children for specific paths.
_DEFAULT_NAMED_OBJECTS: dict[str, list[str]] = {
    "setup/boundary_conditions/velocity_inlet": ["inlet"],
    "setup/boundary_conditions/pressure_outlet": ["outlet"],
    "setup/models": [],
}

#: List sizes for list-object paths.
_DEFAULT_LIST_SIZES: dict[str, int] = {
    "solution/run_calculation/pseudo_time_settings/timestepping_parameters/profile_update_interval": 1,
}

#: Attribute responses keyed by path.
#: Each value is a dict with optional keys ``attrs``, ``group_children``.
_DEFAULT_ATTRS: dict[str, dict] = {
    "setup/models/energy/enabled": {
        "attrs": {"allowed-values": [True, False], "active?": True},
    },
    "setup/models/viscous/model": {
        "attrs": {
            "allowed-values": ["laminar", "k-epsilon", "k-omega", "RSM"],
            "active?": True,
        },
    },
    "setup/general/solver/time": {
        "attrs": {
            "allowed-values": ["steady", "transient"],
            "active?": True,
        },
    },
}

#: Static info – a minimal subset of the full Fluent settings tree.
_STATIC_INFO: dict[str, Any] = {
    "type": "group",
    "children": {
        "setup": {
            "type": "group",
            "children": {
                "general": {
                    "type": "group",
                    "children": {
                        "solver": {
                            "type": "group",
                            "children": {
                                "time": {"type": "string"},
                                "velocity_formulation": {"type": "string"},
                            },
                        },
                        "gravity": {
                            "type": "group",
                            "children": {"enabled": {"type": "boolean"}},
                        },
                    },
                },
                "models": {
                    "type": "group",
                    "children": {
                        "energy": {
                            "type": "group",
                            "children": {"enabled": {"type": "boolean"}},
                        },
                        "viscous": {
                            "type": "group",
                            "children": {
                                "model": {"type": "string"},
                                "k_epsilon_model": {"type": "string"},
                            },
                        },
                    },
                },
                "boundary_conditions": {
                    "type": "group",
                    "children": {
                        "velocity_inlet": {
                            "type": "named-object",
                            "object-type": {
                                "type": "group",
                                "children": {
                                    "momentum": {
                                        "type": "group",
                                        "children": {
                                            "velocity_magnitude": {
                                                "type": "group",
                                                "children": {
                                                    "value": {"type": "real"},
                                                    "units": {"type": "string"},
                                                },
                                            }
                                        },
                                    }
                                },
                            },
                        },
                        "pressure_outlet": {
                            "type": "named-object",
                            "object-type": {
                                "type": "group",
                                "children": {
                                    "momentum": {
                                        "type": "group",
                                        "children": {
                                            "gauge_pressure": {
                                                "type": "group",
                                                "children": {
                                                    "value": {"type": "real"},
                                                },
                                            }
                                        },
                                    }
                                },
                            },
                        },
                    },
                },
            },
        },
        "solution": {
            "type": "group",
            "children": {
                "methods": {
                    "type": "group",
                    "children": {
                        "p_v_coupling": {
                            "type": "group",
                            "children": {"scheme": {"type": "string"}},
                        }
                    },
                },
                "controls": {
                    "type": "group",
                    "children": {
                        "under_relaxation": {
                            "type": "group",
                            "children": {
                                "pressure": {"type": "real"},
                                "velocity": {"type": "real"},
                            },
                        }
                    },
                },
                "run_calculation": {
                    "type": "group",
                    "children": {"iter_count": {"type": "integer"}},
                },
                "initialization": {
                    "type": "group",
                    "children": {
                        "initialization_methods": {"type": "string"},
                    },
                    "commands": {
                        "initialize": {
                            "type": "command",
                            "return-type": "string",
                            "arguments": {},
                        }
                    },
                },
            },
        },
    },
}

#: Command handlers: (path, command) → callable(store, **kwargs) → reply
_COMMAND_HANDLERS: dict[tuple[str, str], Any] = {
    (
        "solution/initialization",
        "initialize",
    ): lambda store, **kw: "Initialization complete",
}

#: Query handlers: (path, query) → callable(store, **kwargs) → reply
_QUERY_HANDLERS: dict[tuple[str, str], Any] = {
    (
        "setup/boundary_conditions/velocity_inlet",
        "get_zone_names",
    ): lambda store, **kw: list(
        store["named_objects"].get("setup/boundary_conditions/velocity_inlet", [])
    ),
}


# ---------------------------------------------------------------------------
# HTTP request handler
# ---------------------------------------------------------------------------


class _Handler(BaseHTTPRequestHandler):
    """HTTP request handler implementing the provisional REST contract."""

    # Suppress default request logging to keep test output clean.
    def log_message(self, format, *args):  # noqa: A002
        pass

    # -- helpers --------------------------------------------------------

    def _parse_url(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
        # Flatten single-value params; keep lists for multi-value params
        flat = {k: (v[0] if len(v) == 1 else v) for k, v in params.items()}
        return parsed.path.lstrip("/"), flat

    def _read_body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        if length:
            return json.loads(self.rfile.read(length))
        return {}

    def _send_json(self, data: Any, status: int = 200) -> None:
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_error(self, status: int, message: str) -> None:
        self._send_json({"detail": message}, status)

    @property
    def _store(self) -> dict:
        return self.server.store  # type: ignore[attr-defined]

    # -- helpers to strip component prefix --------------------------------

    _API_PREFIX = "api/"

    def _strip_prefix(self, path: str) -> str | None:
        """Strip ``api/<component>/`` and return the settings path, or None."""
        if not path.startswith(self._API_PREFIX):
            return None
        rest = path[len(self._API_PREFIX):]
        # rest is now "fluent_1/..."
        slash = rest.find("/")
        if slash == -1:
            # path is "api/<component>" with no trailing segment
            return ""
        return rest[slash + 1:]  # e.g. "static-info" or "setup/models/..."

    # -- GET ------------------------------------------------------------

    def do_GET(self):  # noqa: N802
        """Handle HTTP GET requests."""
        path, _params = self._parse_url()
        setting_path = self._strip_prefix(path)
        if setting_path is None:
            return self._send_error(404, f"Unknown endpoint: {path}")

        if setting_path == "static-info":
            self._send_json(self._store["static_info"])
            return

        # Lookup in vars (leaf or group)
        if setting_path in self._store["vars"]:
            self._send_json(self._store["vars"][setting_path])
            return

        # Named-object names
        if setting_path in self._store["named_objects"]:
            self._send_json(self._store["named_objects"][setting_path])
            return

        # List size
        if setting_path in self._store["list_sizes"]:
            self._send_json({"size": self._store["list_sizes"][setting_path]})
            return

        # Group-level read: aggregate all leaf paths under the prefix
        prefix = setting_path + "/"
        group = {}
        for k, v in self._store["vars"].items():
            if k.startswith(prefix):
                remainder = k[len(prefix):]
                parts = remainder.split("/")
                target = group
                for part in parts[:-1]:
                    target = target.setdefault(part, {})
                target[parts[-1]] = v
        if group:
            self._send_json(group)
            return

        self._send_error(404, f"Path not found: {setting_path}")

    # -- PUT ------------------------------------------------------------

    def do_PUT(self):  # noqa: N802
        """Handle HTTP PUT requests."""
        path, _params = self._parse_url()
        setting_path = self._strip_prefix(path)
        if setting_path is None:
            return self._send_error(404, f"Unknown endpoint: {path}")
        body = self._read_body()

        if "value" in body:
            # Set value
            value = body["value"]
            if isinstance(value, dict):
                def _flatten(prefix, d):
                    for k, v in d.items():
                        full = f"{prefix}/{k}"
                        if isinstance(v, dict):
                            _flatten(full, v)
                        else:
                            self._store["vars"][full] = v
                _flatten(setting_path, value)
            else:
                self._store["vars"][setting_path] = value
            self._send_json({})

        elif "size" in body:
            # Resize list object
            self._store["list_sizes"][setting_path] = body["size"]
            self._send_json({})

        elif "rename" in body:
            # Rename named object
            new_name = body["rename"].get("new")
            old_name = body["rename"].get("old")
            if not new_name or not old_name:
                return self._send_error(400, "Missing 'new' or 'old' in rename body")
            bucket = self._store["named_objects"].get(setting_path, [])
            if old_name not in bucket:
                return self._send_error(
                    404, f"Object '{old_name}' not found at path '{setting_path}'"
                )
            bucket[bucket.index(old_name)] = new_name
            self._send_json({})

        else:
            self._send_error(400, "PUT body must contain 'value', 'size', or 'rename'")

    # -- POST -----------------------------------------------------------

    def do_POST(self):  # noqa: N802
        """Handle HTTP POST requests."""
        path, _params = self._parse_url()
        setting_path = self._strip_prefix(path)
        if setting_path is None:
            return self._send_error(404, f"Unknown endpoint: {path}")
        body = self._read_body()

        if setting_path == "get_var":
            var_path = body.get("path")
            if var_path is None:
                return self._send_error(400, "Missing 'path' in request body")
            if var_path in self._store["vars"]:
                self._send_json(self._store["vars"][var_path])
                return
            # Group-level read
            prefix = var_path + "/"
            group = {}
            for k, v in self._store["vars"].items():
                if k.startswith(prefix):
                    remainder = k[len(prefix):]
                    parts = remainder.split("/")
                    target = group
                    for part in parts[:-1]:
                        target = target.setdefault(part, {})
                    target[parts[-1]] = v
            if group:
                self._send_json(group)
            else:
                self._send_error(404, f"Path not found: {var_path}")
            return

        if setting_path == "get_attrs":
            attr_path = body.get("path")
            if attr_path is None:
                return self._send_error(400, "Missing 'path' in request body")
            recursive = body.get("recursive", False)
            entry = self._store["attrs"].get(attr_path, {"attrs": {}})
            if recursive:
                self._send_json(entry)
            else:
                self._send_json({"attrs": entry.get("attrs", {})})
            return

        if "name" in body and "/" not in body.get("name", "/"):
            # Create named object: POST /api/fluent_1/{path}, body: {"name": ...}
            name = body["name"]
            bucket = self._store["named_objects"].setdefault(setting_path, [])
            if name not in bucket:
                bucket.append(name)
            self._send_json({})
            return

        # Command or query: last path segment is the command name
        # e.g. "solution/initialization/initialize"
        slash = setting_path.rfind("/")
        if slash == -1:
            return self._send_error(404, f"Unknown endpoint: {path}")
        parent_path = setting_path[:slash]
        command = setting_path[slash + 1:]

        handler = self._store["command_handlers"].get((parent_path, command))
        if handler is not None:
            reply = handler(self._store, **body)
            self._send_json({"reply": reply})
            return

        handler = self._store["query_handlers"].get((parent_path, command))
        if handler is not None:
            reply = handler(self._store, **body)
            self._send_json({"reply": reply})
            return

        # Generic fallback
        reply = f"Executed '{command}' at '{parent_path}'"
        self._send_json({"reply": reply})

    # -- DELETE ---------------------------------------------------------

    def do_DELETE(self):  # noqa: N802
        """Handle HTTP DELETE requests."""
        path, _params = self._parse_url()
        full_path = self._strip_prefix(path)
        if full_path is None:
            return self._send_error(404, f"Unknown endpoint: {path}")

        # DELETE /api/fluent_1/{parent_path}/{name}
        slash = full_path.rfind("/")
        if slash == -1:
            return self._send_error(400, "DELETE path must include parent and name")
        parent_path = full_path[:slash]
        name = full_path[slash + 1:]

        bucket = self._store["named_objects"].get(parent_path, [])
        if name not in bucket:
            return self._send_error(
                404, f"Object '{name}' not found at path '{parent_path}'"
            )
        bucket.remove(name)
        self._send_json({})


# ---------------------------------------------------------------------------
# Server class
# ---------------------------------------------------------------------------


class FluentRestMockServer:
    """In-process HTTP mock server for the provisional Fluent REST settings API.

    The server runs in a background daemon thread and can be started and stopped
    programmatically.  The in-memory settings store is a deep copy of the
    module-level defaults so each server instance starts with a clean state.

    Parameters
    ----------
    port : int, optional
        TCP port to listen on.  Defaults to ``0``, which lets the OS assign a
        free ephemeral port (recommended for tests to avoid port conflicts).
        The actual port is available via :attr:`port` after :meth:`start`.
    host : str, optional
        Hostname/IP to bind to.  Defaults to ``"127.0.0.1"``.

    Examples
    --------
    >>> server = FluentRestMockServer()
    >>> server.start()
    >>> print(server.port)          # OS-assigned port
    >>> server.stop()
    """

    def __init__(self, port: int = 0, host: str = "127.0.0.1") -> None:
        self._host = host
        self._port = port
        self._httpd: socketserver.TCPServer | None = None
        self._thread: threading.Thread | None = None

        # Build a fresh deep-copy of the default store.
        self.store: dict[str, Any] = {
            "vars": copy.deepcopy(_DEFAULT_VARS),
            "named_objects": copy.deepcopy(_DEFAULT_NAMED_OBJECTS),
            "list_sizes": copy.deepcopy(_DEFAULT_LIST_SIZES),
            "attrs": copy.deepcopy(_DEFAULT_ATTRS),
            "static_info": copy.deepcopy(_STATIC_INFO),
            "command_handlers": dict(_COMMAND_HANDLERS),
            "query_handlers": dict(_QUERY_HANDLERS),
        }

    @property
    def port(self) -> int:
        """The TCP port the server is listening on.

        Valid only after :meth:`start` has been called.
        """
        if self._httpd is None:
            return self._port
        return self._httpd.server_address[1]

    @property
    def base_url(self) -> str:
        """Convenience base URL, e.g. ``"http://127.0.0.1:54321"``."""
        return f"http://{self._host}:{self.port}"

    def start(self) -> "FluentRestMockServer":
        """Start the server in a background daemon thread.

        Returns *self* to allow chaining::

            client = FluentRestClient(FluentRestMockServer().start().base_url)

        Raises
        ------
        RuntimeError
            If the server is already running.
        """
        if self._httpd is not None:
            raise RuntimeError("Server is already running.")

        # Allow port reuse so tests can restart quickly.
        socketserver.TCPServer.allow_reuse_address = True
        httpd = socketserver.TCPServer((self._host, self._port), _Handler)
        # Inject the store reference into the server so handlers can access it.
        httpd.store = self.store  # type: ignore[attr-defined]
        self._httpd = httpd

        self._thread = threading.Thread(
            target=httpd.serve_forever, daemon=True, name="FluentRestMockServer"
        )
        self._thread.start()
        return self

    def stop(self) -> None:
        """Shut down the server and wait for the background thread to finish."""
        if self._httpd is None:
            return
        self._httpd.shutdown()
        self._httpd.server_close()
        if self._thread is not None:
            self._thread.join(timeout=5)
        self._httpd = None
        self._thread = None

    # Context-manager support ----------------------------------------

    def __enter__(self) -> "FluentRestMockServer":
        return self.start()

    def __exit__(self, *_) -> None:
        self.stop()
