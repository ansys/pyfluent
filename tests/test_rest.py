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

"""Unit tests for the Fluent REST transport layer.

This suite targets the actual public surface of the
``ansys.fluent.core.rest`` package:

* :class:`ansys.fluent.core.rest.client.FluentRestClient` — the settings API
  client (``client.py``).
* :class:`ansys.fluent.core.rest.transport.HttpRequestStrategy` — the real
  HTTP transport (``transport.py``).
* The package re-exports in ``ansys/fluent/core/rest/__init__.py``.

Test structure
--------------
- API-layer unit tests: use :class:`FakeStrategy` to verify endpoint, method,
  and body without any I/O.  Run anywhere, no server required.
- Transport unit tests: instantiate :class:`HttpRequestStrategy` directly and
  patch ``ansys.fluent.core.rest.transport.urllib.request.urlopen``.

Run all unit tests::

    pytest tests/test_rest.py -v
"""

import hashlib
import io
import json
from typing import Any
from unittest.mock import patch
import urllib.error

import pytest

import ansys.fluent.core.rest as rest_pkg
from ansys.fluent.core.rest import (
    FluentRestClient,
    FluentRestError,
    HttpRequestStrategy,
    RequestStrategy,
    connect_to_webserver,
)
from ansys.fluent.core.rest.client import FluentRestClient as FluentRestClientDirect
from ansys.fluent.core.rest.transport import _make_auth_headers

connect_to_webserver_direct = FluentRestClientDirect.connect

_BASE_URL = "http://127.0.0.1:5000"


# ============================================================================
# Mock helpers
# ============================================================================


class _FakeResponse:
    """Context-manager stand-in for ``urllib.request.urlopen`` return value."""

    def __init__(self, body: object, status: int = 200, raw: bytes | None = None):
        if raw is not None:
            self._raw = raw
        else:
            self._raw = json.dumps(body).encode("utf-8")
        self.status = status

    def read(self) -> bytes:
        return self._raw

    def __enter__(self) -> "_FakeResponse":
        return self

    def __exit__(self, *exc) -> bool:
        return False


def _make_response(body: object, status: int = 200) -> _FakeResponse:
    """Return a fake urlopen response carrying a JSON *body*."""
    return _FakeResponse(body, status=status)


def _make_raw_response(raw: bytes) -> _FakeResponse:
    """Return a fake urlopen response carrying arbitrary *raw* bytes."""
    return _FakeResponse(None, raw=raw)


def _make_http_error(
    status: int, body: object | None = None, reason: str = "Error"
) -> urllib.error.HTTPError:
    """Construct an ``HTTPError`` with a readable body."""
    data = json.dumps(body).encode("utf-8") if body else b""
    return urllib.error.HTTPError(
        url=_BASE_URL, code=status, msg=reason, hdrs={}, fp=io.BytesIO(data)
    )


class FakeStrategy:
    """Lightweight :class:`~ansys.fluent.core.rest.transport.RequestStrategy`
    test double for API-layer unit tests.

    All calls are recorded in ``calls`` as ``(method, endpoint, body)`` tuples.
    Return values (or exceptions) are consumed from a FIFO queue added via
    :meth:`add_response` / :meth:`add_error`; once the queue is empty the
    ``default`` value is returned.
    """

    def __init__(self, default: Any = None) -> None:
        self.calls: list[tuple[str, str, Any]] = []
        self._default = default
        self._queue: list[Any] = []

    def add_response(self, value: Any) -> "FakeStrategy":
        """Enqueue a return value."""
        self._queue.append(value)
        return self

    def add_error(self, exc: Exception) -> "FakeStrategy":
        """Enqueue an exception to raise on the next call."""
        self._queue.append(exc)
        return self

    def request(self, method: str, endpoint: str, *, body: Any = None) -> Any:
        self.calls.append((method, endpoint, body))
        if self._queue:
            item = self._queue.pop(0)
            if isinstance(item, Exception):
                raise item
            return item
        return self._default


def _client(**kwargs) -> FluentRestClient:
    """Return a ``FluentRestClient`` backed by a ``FakeStrategy``.

    Pass ``default=<value>`` to set the value returned by every strategy call,
    or use ``FluentRestClient(FakeStrategy().add_response(...))`` for finer
    control per call.
    """
    default = kwargs.pop("default", None)
    strategy = FakeStrategy(default=default)
    return FluentRestClient(strategy, **kwargs)


def _http_strategy(**kwargs) -> HttpRequestStrategy:
    """Return an ``HttpRequestStrategy`` with sensible test defaults."""
    kwargs.setdefault("auth_token", "tok123")
    kwargs.setdefault("retry_delay", 0)  # keep retry tests fast
    return HttpRequestStrategy(_BASE_URL, **kwargs)


# ============================================================================
# Package API — __init__.py re-exports
# ============================================================================


class TestRestPackageApi:
    """The ``ansys.fluent.core.rest`` package exposes the public surface."""

    def test_all_exports(self):
        """``__all__`` lists exactly the supported public names."""
        assert set(rest_pkg.__all__) == {
            "FluentRestClient",
            "connect_to_webserver",
            "FluentRestError",
            "HttpRequestStrategy",
            "RequestStrategy",
        }

    def test_reexports_are_the_real_objects(self):
        """Package-level names are the same objects as their submodules."""
        assert FluentRestClient is FluentRestClientDirect
        assert connect_to_webserver.__func__ is connect_to_webserver_direct.__func__

    def test_error_is_runtimeerror_subclass(self):
        """``FluentRestError`` stays a ``RuntimeError`` for broad ``except``."""
        assert issubclass(FluentRestError, RuntimeError)


# ============================================================================
# Unit tests — HttpRequestStrategy and FluentRestClient initialization
# ============================================================================


class TestHttpRequestStrategyInit:
    """HttpRequestStrategy initialization and attribute defaults."""

    def test_init_with_defaults(self):
        strategy = HttpRequestStrategy("http://localhost:5000")
        assert strategy._base_url == "http://localhost:5000"
        assert strategy._headers == {}
        assert strategy._timeout == 30.0
        assert strategy._max_retries == 2
        assert strategy._retry_delay == 1.0

    def test_init_strips_trailing_slash(self):
        strategy = HttpRequestStrategy("http://localhost:5000/")
        assert strategy._base_url == "http://localhost:5000"

    def test_init_with_auth_token(self):
        strategy = HttpRequestStrategy("http://localhost:5000", auth_token="secret")
        expected = hashlib.sha256(b"secret").hexdigest()
        assert strategy._headers["Authorization"] == "Bearer " + expected

    def test_init_with_custom_timeout(self):
        strategy = HttpRequestStrategy("http://localhost:5000", timeout=60.0)
        assert strategy._timeout == 60.0

    def test_init_with_custom_max_retries(self):
        strategy = HttpRequestStrategy("http://localhost:5000", max_retries=5)
        assert strategy._max_retries == 5

    def test_client_default_component(self):
        client = FluentRestClient(FakeStrategy())
        assert client._api_base == "api/fluent_1"

    def test_client_custom_component(self):
        client = FluentRestClient(FakeStrategy(), component="fluent_meshing_1")
        assert client._api_base == "api/fluent_meshing_1"


# ============================================================================
# Unit tests — FluentRestError
# ============================================================================


class TestFluentRestError:
    """FluentRestError construction and transport translation."""

    def test_status_and_message(self):
        exc = FluentRestError(404, "Not found", retryable=False)
        assert exc.status == 404
        assert exc.retryable is False
        assert "HTTP 404" in str(exc)
        assert "Not found" in str(exc)

    def test_retryable_flag(self):
        exc = FluentRestError(503, "Service unavailable", retryable=True)
        assert exc.retryable is True

    def test_from_transport_plain_oserror_is_retryable(self):
        exc = FluentRestError.from_transport(OSError("Connection refused"))
        assert exc.status == 0
        assert exc.retryable is True

    def test_from_transport_urlerror_is_retryable(self):
        exc = FluentRestError.from_transport(urllib.error.URLError("reset"))
        assert exc.status == 0
        assert exc.retryable is True

    @pytest.mark.parametrize("status", [502, 503, 504])
    def test_from_transport_gateway_errors_are_retryable(self, status):
        exc = FluentRestError.from_transport(_make_http_error(status, {"d": "x"}))
        assert exc.status == status
        assert exc.retryable is True

    @pytest.mark.parametrize("status", [400, 401, 403, 404, 409, 500])
    def test_from_transport_other_http_errors_not_retryable(self, status):
        exc = FluentRestError.from_transport(_make_http_error(status))
        assert exc.status == status
        assert exc.retryable is False

    def test_from_transport_uses_body_as_message(self):
        exc = FluentRestError.from_transport(
            _make_http_error(400, {"detail": "bad path"})
        )
        assert "bad path" in str(exc)


# ============================================================================
# Unit tests — authentication headers
# ============================================================================


class TestAuthHelpers:
    """_make_auth_headers helper lives in the transport module."""

    def test_make_auth_headers_no_token(self):
        assert _make_auth_headers(None) == {}
        assert _make_auth_headers("") == {}

    def test_make_auth_headers_with_token(self):
        token = "mysecret"
        headers = _make_auth_headers(token)
        # Verify structure, not by duplicating the implementation
        assert "Authorization" in headers
        assert headers["Authorization"].startswith("Bearer ")
        assert len(headers["Authorization"].split()[-1]) == 64  # SHA-256 hex = 64 chars


class TestHttpRequestStrategyAuth:
    """Authorization header is attached to real HTTP requests."""

    @patch("ansys.fluent.core.rest.transport.urllib.request.urlopen")
    def test_auth_header_attached_to_requests(self, mock_urlopen):
        mock_urlopen.return_value = _make_response(True)
        strategy = HttpRequestStrategy(_BASE_URL, auth_token="abc")
        strategy.request("POST", "api/fluent_1/get_var", body={"path": "setup/x"})
        req = mock_urlopen.call_args[0][0]
        expected = hashlib.sha256(b"abc").hexdigest()
        assert req.get_header("Authorization") == "Bearer " + expected

    @patch("ansys.fluent.core.rest.transport.urllib.request.urlopen")
    def test_no_auth_header_when_token_absent(self, mock_urlopen):
        mock_urlopen.return_value = _make_response(True)
        strategy = HttpRequestStrategy(_BASE_URL)
        strategy.request("POST", "api/fluent_1/get_var", body={"path": "setup/x"})
        req = mock_urlopen.call_args[0][0]
        assert req.get_header("Authorization") is None


# ============================================================================
# Unit tests — read endpoints
# ============================================================================


class TestFluentRestClientReads:
    """get_static_info / get_var / get_attrs and list/name normalization."""

    def test_get_static_info_path(self):
        strategy = FakeStrategy(default={"type": "group"})
        result = FluentRestClient(strategy).get_static_info()
        method, endpoint, body = strategy.calls[0]
        assert method == "GET"
        assert endpoint == "api/fluent_1/static-info"
        assert result == {"type": "group"}

    def test_get_static_info_full_query(self):
        strategy = FakeStrategy(default={"type": "group"})
        FluentRestClient(strategy).get_static_info(full=True)
        _, endpoint, _ = strategy.calls[0]
        assert endpoint == "api/fluent_1/static-info?full=true"

    def test_get_var_returns_value(self):
        strategy = FakeStrategy(default=True)
        assert FluentRestClient(strategy).get_var("setup/models/energy/enabled") is True

    def test_get_var_uses_post_and_strips_leading_slash(self):
        strategy = FakeStrategy(default=42)
        FluentRestClient(strategy).get_var("/setup/general/setting")
        method, endpoint, body = strategy.calls[0]
        assert method == "POST"
        assert endpoint == "api/fluent_1/get_var"
        assert body == {"path": "setup/general/setting"}

    def test_get_var_raises_on_404(self):
        strategy = FakeStrategy()
        strategy.add_error(FluentRestError(404, "Not found"))
        with pytest.raises(FluentRestError) as exc_info:
            FluentRestClient(strategy).get_var("setup/nonexistent")
        assert exc_info.value.status == 404

    def test_get_attrs_builds_query(self):
        strategy = FakeStrategy(default={"min": 0, "max": 1})
        FluentRestClient(strategy).get_attrs("setup/x", ["min", "max"], recursive=True)
        method, endpoint, body = strategy.calls[0]
        assert method == "GET"
        assert "attrs=min%2Cmax" in endpoint
        assert "recursive=true" in endpoint

    def test_get_object_names_from_list(self):
        strategy = FakeStrategy(default=["a", "b"])
        assert FluentRestClient(strategy).get_object_names(
            "setup/bc/velocity-inlet"
        ) == ["a", "b"]

    def test_get_object_names_from_dict_keys(self):
        strategy = FakeStrategy(default={"a": {}, "b": {}})
        assert sorted(FluentRestClient(strategy).get_object_names("setup/bc/wall")) == [
            "a",
            "b",
        ]

    def test_get_list_size_from_list(self):
        strategy = FakeStrategy(default=[1, 2, 3])
        assert FluentRestClient(strategy).get_list_size("setup/list") == 3

    def test_get_list_size_uses_explicit_size_field(self):
        strategy = FakeStrategy(default={"size": 7, "a": {}})
        assert FluentRestClient(strategy).get_list_size("setup/container") == 7

    def test_names_from_handles_unexpected_type(self):
        from ansys.fluent.core.rest.client import _names_from

        assert _names_from(None) == []
        assert _names_from(5) == []

    def test_size_from_handles_unexpected_type(self):
        from ansys.fluent.core.rest.client import _size_from

        assert _size_from(None) == 0
        assert _size_from("x") == 0


# ============================================================================
# Unit tests — write endpoints
# ============================================================================


class TestFluentRestClientWrites:
    """set_var / resize_list_object."""

    def test_set_var_sends_put(self):
        strategy = FakeStrategy(default={})
        FluentRestClient(strategy).set_var("setup/models/energy/enabled", True)
        method, endpoint, body = strategy.calls[0]
        assert method == "PUT"
        assert "setup/models/energy/enabled" in endpoint
        assert body is True

    def test_set_var_with_dict_value(self):
        strategy = FakeStrategy(default={})
        value = {"a": 1, "b": 2}
        FluentRestClient(strategy).set_var("setup/some/dict", value)
        _, _, body = strategy.calls[0]
        assert body == value

    def test_resize_list_object(self):
        strategy = FakeStrategy(default={})
        FluentRestClient(strategy).resize_list_object("setup/list", 4)
        method, endpoint, body = strategy.calls[0]
        assert method == "POST"
        assert body == {"new-size": 4}


# ============================================================================
# Unit tests — named-object CRUD
# ============================================================================


class TestFluentRestClientNamedObjects:
    """create / delete / rename / bulk delete."""

    def test_create_sends_post_with_name(self):
        strategy = FakeStrategy(default={})
        FluentRestClient(strategy).create("setup/boundary-conditions/wall", "new-wall")
        method, endpoint, body = strategy.calls[0]
        assert method == "POST"
        assert body["name"] == "new-wall"

    def test_create_merges_properties(self):
        strategy = FakeStrategy(default={})
        FluentRestClient(strategy).create(
            "setup/boundary-conditions/wall", "w", properties={"enabled": True}
        )
        _, _, body = strategy.calls[0]
        assert body == {"enabled": True, "name": "w"}

    def test_create_without_name_omits_name_key(self):
        strategy = FakeStrategy(default={})
        FluentRestClient(strategy).create("setup/bc/wall")
        _, _, body = strategy.calls[0]
        assert "name" not in body

    def test_delete_sends_delete(self):
        strategy = FakeStrategy(default={})
        FluentRestClient(strategy).delete("setup/boundary-conditions/wall", "wall-1")
        method, endpoint, body = strategy.calls[0]
        assert method == "DELETE"
        assert endpoint.endswith("wall/wall-1")

    def test_delete_url_encodes_name(self):
        strategy = FakeStrategy(default={})
        FluentRestClient(strategy).delete("setup/bc/wall", "wall 1/special")
        _, endpoint, _ = strategy.calls[0]
        assert "wall%201%2Fspecial" in endpoint

    def test_delete_ignore_not_found_swallows_404(self):
        strategy = FakeStrategy()
        strategy.add_error(FluentRestError(404, "Not found"))
        FluentRestClient(strategy).delete("setup/bc/wall", "w", ignore_not_found=True)

    def test_delete_raises_on_404_by_default(self):
        strategy = FakeStrategy()
        strategy.add_error(FluentRestError(404, "Not found"))
        with pytest.raises(FluentRestError) as exc_info:
            FluentRestClient(strategy).delete("setup/bc/wall", "w")
        assert exc_info.value.status == 404

    def test_delete_ignore_not_found_still_raises_500(self):
        strategy = FakeStrategy()
        strategy.add_error(FluentRestError(500, "Server error"))
        with pytest.raises(FluentRestError):
            FluentRestClient(strategy).delete(
                "setup/bc/wall", "w", ignore_not_found=True
            )

    def test_rename_sends_put(self):
        strategy = FakeStrategy(default={})
        FluentRestClient(strategy).rename(
            "setup/boundary-conditions/wall", "new", "old"
        )
        method, endpoint, body = strategy.calls[0]
        assert method == "PUT"
        assert body["name"] == "new"
        assert endpoint.endswith("wall/old")

    def test_delete_child_objects_iterates(self):
        strategy = FakeStrategy(default={})
        FluentRestClient(strategy).delete_child_objects("setup/bc", "wall", ["a", "b"])
        delete_endpoints = [ep for _, ep, _ in strategy.calls]
        assert any("wall/a" in ep for ep in delete_endpoints)
        assert any("wall/b" in ep for ep in delete_endpoints)

    def test_delete_all_child_objects(self):
        strategy = FakeStrategy(default=None)
        strategy.add_response(["x", "y"])  # for get_object_names
        FluentRestClient(strategy).delete_all_child_objects("setup/bc", "wall")
        delete_calls = [c for c in strategy.calls if c[0] == "DELETE"]
        assert len(delete_calls) == 2


# ============================================================================
# Unit tests — command / query execution
# ============================================================================


class TestFluentRestClientExecute:
    """execute_cmd / execute_query."""

    def test_execute_cmd_appends_force(self):
        strategy = FakeStrategy(default={})
        FluentRestClient(strategy).execute_cmd("solution/initialization", "initialize")
        method, endpoint, body = strategy.calls[0]
        assert method == "POST"
        assert endpoint.endswith("initialization/initialize?force=true")

    def test_execute_cmd_without_force(self):
        strategy = FakeStrategy(default={})
        FluentRestClient(strategy).execute_cmd(
            "solution/init", "initialize", force=False
        )
        _, endpoint, _ = strategy.calls[0]
        assert "?force=true" not in endpoint

    def test_execute_cmd_passes_kwargs_as_body(self):
        strategy = FakeStrategy(default={})
        FluentRestClient(strategy).execute_cmd("p", "cmd", iters=5)
        _, _, body = strategy.calls[0]
        assert body == {"iters": 5}

    def test_execute_query(self):
        strategy = FakeStrategy(default={"result": 1})
        out = FluentRestClient(strategy).execute_query("reports/x", "evaluate", arg=2)
        method, endpoint, body = strategy.calls[0]
        assert endpoint.endswith("x/evaluate")
        assert body == {"arg": 2}
        assert out == {"result": 1}


# ============================================================================
# Unit tests — transport: JSON decoding and retry behavior
# ============================================================================


class TestHttpRequestStrategyTransport:
    """Response decoding and retry policy for HttpRequestStrategy."""

    @patch("ansys.fluent.core.rest.transport.urllib.request.urlopen")
    def test_empty_body_returns_none(self, mock_urlopen):
        mock_urlopen.return_value = _make_raw_response(b"")
        assert _http_strategy().request("GET", "api/fluent_1/setup/x") is None

    @patch("ansys.fluent.core.rest.transport.urllib.request.urlopen")
    def test_non_json_body_returns_empty_dict(self, mock_urlopen):
        mock_urlopen.return_value = _make_raw_response(b"not json")
        assert _http_strategy().request("GET", "api/fluent_1/setup/x") == {}

    @patch("ansys.fluent.core.rest.transport.urllib.request.urlopen")
    def test_get_retries_on_502_then_succeeds(self, mock_urlopen):
        mock_urlopen.side_effect = [
            _make_http_error(502, {"detail": "bad gateway"}),
            _make_response(["inlet-1", "inlet-2"]),
        ]
        result = _http_strategy().request("GET", "api/fluent_1/setup/bc/velocity-inlet")
        assert result == ["inlet-1", "inlet-2"]
        assert mock_urlopen.call_count == 2

    @patch("ansys.fluent.core.rest.transport.urllib.request.urlopen")
    def test_post_does_not_retry_on_502(self, mock_urlopen):
        mock_urlopen.side_effect = _make_http_error(502)
        with pytest.raises(FluentRestError) as exc_info:
            _http_strategy().request("POST", "api/fluent_1/get_var", body={"path": "x"})
        assert exc_info.value.status == 502
        assert mock_urlopen.call_count == 1

    @patch("ansys.fluent.core.rest.transport.urllib.request.urlopen")
    def test_get_retry_exhaustion(self, mock_urlopen):
        mock_urlopen.side_effect = _make_http_error(503)
        strategy = HttpRequestStrategy(
            _BASE_URL, auth_token="t", max_retries=2, retry_delay=0
        )
        with pytest.raises(FluentRestError) as exc_info:
            strategy.request("GET", "api/fluent_1/test")
        assert exc_info.value.status == 503
        assert mock_urlopen.call_count == 3  # 1 initial + 2 retries

    @patch("ansys.fluent.core.rest.transport.urllib.request.urlopen")
    def test_connection_error_on_get_retries(self, mock_urlopen):
        mock_urlopen.side_effect = [
            OSError("connection refused"),
            _make_response([]),
        ]
        result = _http_strategy().request("GET", "api/fluent_1/setup/x")
        assert result == []
        assert mock_urlopen.call_count == 2


# ============================================================================
# Unit tests — FluentRestClient.connect factory
# ============================================================================


class TestConnectToWebserver:
    """FluentRestClient.connect factory returns a properly configured client."""

    def test_returns_fluent_rest_client(self):
        client = connect_to_webserver(url=_BASE_URL, auth_token="secret")
        assert isinstance(client, FluentRestClient)

    def test_strategy_is_http_request_strategy(self):
        client = connect_to_webserver(url=_BASE_URL, auth_token="secret")
        assert isinstance(client._strategy, HttpRequestStrategy)

    def test_strategy_stores_base_url(self):
        client = connect_to_webserver(url="http://host:1234/", auth_token="secret")
        assert client._strategy._base_url == "http://host:1234"

    def test_strategy_builds_auth_header(self):
        client = connect_to_webserver(url=_BASE_URL, auth_token="secret")
        expected = hashlib.sha256(b"secret").hexdigest()
        assert client._strategy._headers["Authorization"] == "Bearer " + expected

    def test_defaults_to_solver_component(self):
        client = connect_to_webserver(url=_BASE_URL, auth_token="secret")
        assert client._api_base == "api/fluent_1"

    def test_positional_arguments(self):
        client = connect_to_webserver(_BASE_URL, "secret")
        assert isinstance(client, FluentRestClient)
        assert isinstance(client._strategy, HttpRequestStrategy)

    def test_satisfies_request_strategy_protocol(self):
        client = connect_to_webserver(url=_BASE_URL, auth_token="secret")
        assert isinstance(client._strategy, RequestStrategy)

    def test_reexport_is_same_as_classmethod(self):
        assert connect_to_webserver.__func__ is connect_to_webserver_direct.__func__
