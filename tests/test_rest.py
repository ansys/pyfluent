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

"""Unit and integration tests for the Fluent REST transport layer.

This suite targets the actual public surface of the
``ansys.fluent.core.rest`` package on this branch:

* :class:`ansys.fluent.core.rest.client.FluentRestClient` — the settings API
  client (``client.py``).  The constructor takes an injected
  :class:`~ansys.fluent.core.rest.transport.RequestStrategy`; use
  :meth:`~ansys.fluent.core.rest.client.FluentRestClient.connect` (aliased as
  ``connect_to_webserver``) to assemble the real stack.
* :class:`ansys.fluent.core.rest.transport.HttpRequestStrategy` — the real
  HTTP transport (``transport.py``).
* The package re-exports in ``ansys/fluent/core/rest/__init__.py``.

Test structure
--------------
- API-layer unit tests (``FakeStrategy``): exercise ``FluentRestClient`` in
  isolation without touching ``urllib`` at all.
- Transport unit tests (patched ``transport.urllib``): verify retry policy,
  auth headers, and JSON decoding inside ``HttpRequestStrategy``.
- Integration tests (marked ``real_server``): run against a live Fluent REST
  server.  They use the ``real_client`` fixture from ``conftest.py`` and
  auto-skip when ``FLUENT_WEBSERVER_TOKEN`` / ``FLUENT_REST_PORT`` are unset
  or the server is unreachable.

Run all unit tests (no server)::

    pytest tests/test_rest.py -v -m "not real_server"

Run integration tests::

    pytest tests/test_rest.py -v -m real_server
"""

import hashlib
import io
import json
from unittest.mock import patch
import urllib.error

import pytest

import ansys.fluent.core.rest as rest_pkg
from ansys.fluent.core.rest import (
    FluentRestClient,
    FluentRestError,
    connect_to_webserver,
)
from ansys.fluent.core.rest.client import FluentRestClient as FluentRestClientDirect
from ansys.fluent.core.rest.client import _names_from, _size_from
from ansys.fluent.core.rest.transport import HttpRequestStrategy, _make_auth_headers

connect_to_webserver_direct = FluentRestClientDirect.connect

_BASE_URL = "http://127.0.0.1:5000"


# ============================================================================
# Test doubles
# ============================================================================


class FakeStrategy:
    """Minimal RequestStrategy test-double for API-layer unit tests.

    Records every ``request()`` call and returns preset responses in FIFO
    order; falls back to the *default* value (``{}`` by default) once the
    queue is exhausted.  An ``Exception`` instance in the queue is raised
    rather than returned.
    """

    def __init__(self, *responses, default=None):
        self._queue = list(responses)
        self._default = {} if default is None else default
        self.calls: list[tuple[str, str, object]] = []

    # ------------------------------------------------------------------
    # Convenience accessors for assertions
    # ------------------------------------------------------------------

    @property
    def last_method(self) -> str | None:
        return self.calls[-1][0] if self.calls else None

    @property
    def last_endpoint(self) -> str | None:
        return self.calls[-1][1] if self.calls else None

    @property
    def last_body(self) -> object:
        return self.calls[-1][2] if self.calls else None

    # ------------------------------------------------------------------
    # RequestStrategy protocol
    # ------------------------------------------------------------------

    def request(self, method: str, endpoint: str, *, body=None):
        self.calls.append((method, endpoint, body))
        item = self._queue.pop(0) if self._queue else self._default
        if isinstance(item, BaseException):
            raise item
        return item


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


def _client(*responses) -> FluentRestClient:
    """Create a FluentRestClient backed by a FakeStrategy with preset *responses*.

    The underlying strategy is accessible via ``client._strategy`` to verify
    which endpoint, method, and body the client passed through.
    """
    return FluentRestClient(FakeStrategy(*responses))


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
        }

    def test_reexports_are_the_real_objects(self):
        """Package-level names are the same objects as their submodules."""
        assert FluentRestClient is FluentRestClientDirect
        assert connect_to_webserver.__func__ is connect_to_webserver_direct.__func__

    def test_error_is_runtimeerror_subclass(self):
        """``FluentRestError`` stays a ``RuntimeError`` for broad ``except``."""
        assert issubclass(FluentRestError, RuntimeError)


# ============================================================================
# Unit tests — FluentRestClient construction
# ============================================================================


class TestFluentRestClientInit:
    """FluentRestClient construction — strategy injection."""

    def test_init_stores_strategy_and_api_base(self):
        strategy = FakeStrategy()
        client = FluentRestClient(strategy)
        assert client._strategy is strategy
        assert client._api_base == "api/fluent_1"

    def test_init_with_custom_component(self):
        strategy = FakeStrategy()
        client = FluentRestClient(strategy, component="fluent_meshing_1")
        assert client._api_base == "api/fluent_meshing_1"


# ============================================================================
# Unit tests — HttpRequestStrategy construction
# ============================================================================


class TestHttpRequestStrategyInit:
    """HttpRequestStrategy construction."""

    def test_init_with_defaults(self):
        strategy = HttpRequestStrategy("http://localhost:5000")
        assert strategy._base_url == "http://localhost:5000"
        assert strategy._timeout == 30.0
        assert strategy._max_retries == 2
        assert strategy._retry_delay == 1.0
        assert strategy._headers == {}

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


class TestHttpRequestStrategyAuth:
    """Authorization header generation in HttpRequestStrategy."""

    def test_make_auth_headers_no_token(self):
        assert _make_auth_headers(None) == {}
        assert _make_auth_headers("") == {}

    def test_make_auth_headers_with_token(self):
        token = "mysecret"
        headers = _make_auth_headers(token)
        expected = hashlib.sha256(token.encode()).hexdigest()
        assert headers["Authorization"] == "Bearer " + expected

    @patch("ansys.fluent.core.rest.transport.urllib.request.urlopen")
    def test_auth_header_attached_to_requests(self, mock_urlopen):
        mock_urlopen.return_value = _make_response(True)
        strategy = HttpRequestStrategy(_BASE_URL, auth_token="abc")
        FluentRestClient(strategy).get_var("setup/x")
        req = mock_urlopen.call_args[0][0]
        expected = hashlib.sha256(b"abc").hexdigest()
        assert req.get_header("Authorization") == "Bearer " + expected

    @patch("ansys.fluent.core.rest.transport.urllib.request.urlopen")
    def test_no_auth_header_when_token_absent(self, mock_urlopen):
        mock_urlopen.return_value = _make_response(True)
        strategy = HttpRequestStrategy(_BASE_URL)  # no token
        FluentRestClient(strategy).get_var("setup/x")
        req = mock_urlopen.call_args[0][0]
        assert req.get_header("Authorization") is None

# ============================================================================
# Unit tests — read endpoints
# ============================================================================


class TestFluentRestClientReads:
    """get_static_info / get_var / get_attrs and list/name normalization."""

    def test_get_static_info_path(self):
        client = _client({"type": "group"})
        result = client.get_static_info()
        assert client._strategy.last_method == "GET"
        assert client._strategy.last_endpoint == "api/fluent_1/static-info"
        assert result == {"type": "group"}

    def test_get_static_info_full_query(self):
        client = _client({"type": "group"})
        client.get_static_info(full=True)
        assert client._strategy.last_endpoint == "api/fluent_1/static-info?full=true"

    def test_get_var_returns_value(self):
        assert _client(True).get_var("setup/models/energy/enabled") is True

    def test_get_var_uses_post_and_strips_leading_slash(self):
        client = _client(42)
        client.get_var("/setup/general/setting")
        assert client._strategy.last_method == "POST"
        assert client._strategy.last_body == {"path": "setup/general/setting"}

    def test_get_var_raises_on_404(self):
        client = _client(FluentRestError(404, "Not found", retryable=False))
        with pytest.raises(FluentRestError) as exc_info:
            client.get_var("setup/nonexistent")
        assert exc_info.value.status == 404

    def test_get_attrs_builds_query(self):
        client = _client({"min": 0, "max": 1})
        client.get_attrs("setup/x", ["min", "max"], recursive=True)
        assert client._strategy.last_method == "GET"
        assert "attrs=min%2Cmax" in client._strategy.last_endpoint
        assert "recursive=true" in client._strategy.last_endpoint

    def test_get_object_names_from_list(self):
        assert _client(["a", "b"]).get_object_names("setup/bc/velocity-inlet") == ["a", "b"]

    def test_get_object_names_from_dict_keys(self):
        assert sorted(_client({"a": {}, "b": {}}).get_object_names("setup/bc/wall")) == ["a", "b"]

    def test_get_list_size_from_list(self):
        assert _client([1, 2, 3]).get_list_size("setup/list") == 3

    def test_get_list_size_uses_explicit_size_field(self):
        assert _client({"size": 7, "a": {}}).get_list_size("setup/container") == 7

    def test_names_from_handles_unexpected_type(self):
        assert _names_from(None) == []
        assert _names_from(5) == []

    def test_size_from_handles_unexpected_type(self):
        assert _size_from(None) == 0
        assert _size_from("x") == 0

# ============================================================================
# Unit tests — write endpoints
# ============================================================================


class TestFluentRestClientWrites:
    """set_var / resize_list_object."""

    def test_set_var_sends_put(self):
        client = _client()
        client.set_var("setup/models/energy/enabled", True)
        assert client._strategy.last_method == "PUT"
        assert client._strategy.last_body is True

    def test_set_var_with_dict_value(self):
        value = {"a": 1, "b": 2}
        client = _client()
        client.set_var("setup/some/dict", value)
        assert client._strategy.last_body == value

    def test_resize_list_object(self):
        client = _client()
        client.resize_list_object("setup/list", 4)
        assert client._strategy.last_method == "POST"
        assert client._strategy.last_body == {"new-size": 4}

# ============================================================================
# Unit tests — named-object CRUD
# ============================================================================


class TestFluentRestClientNamedObjects:
    """create / delete / rename / bulk delete."""

    def test_create_sends_post_with_name(self):
        client = _client()
        client.create("setup/boundary-conditions/wall", "new-wall")
        assert client._strategy.last_method == "POST"
        assert client._strategy.last_body == {"name": "new-wall"}

    def test_create_merges_properties(self):
        client = _client()
        client.create(
            "setup/boundary-conditions/wall", "w", properties={"enabled": True}
        )
        assert client._strategy.last_body == {"enabled": True, "name": "w"}

    def test_create_without_name_omits_name_key(self):
        client = _client()
        client.create("setup/bc/wall")
        assert "name" not in client._strategy.last_body

    def test_delete_sends_delete(self):
        client = _client()
        client.delete("setup/boundary-conditions/wall", "wall-1")
        assert client._strategy.last_method == "DELETE"
        assert client._strategy.last_endpoint.endswith("wall/wall-1")

    def test_delete_url_encodes_name(self):
        client = _client()
        client.delete("setup/bc/wall", "wall 1/special")
        assert "wall%201%2Fspecial" in client._strategy.last_endpoint

    def test_delete_ignore_not_found_swallows_404(self):
        client = _client(FluentRestError(404, "Not found", retryable=False))
        client.delete("setup/bc/wall", "w", ignore_not_found=True)  # no raise

    def test_delete_raises_on_404_by_default(self):
        client = _client(FluentRestError(404, "Not found", retryable=False))
        with pytest.raises(FluentRestError) as exc_info:
            client.delete("setup/bc/wall", "w")
        assert exc_info.value.status == 404

    def test_delete_ignore_not_found_still_raises_500(self):
        client = _client(FluentRestError(500, "Server error", retryable=False))
        with pytest.raises(FluentRestError):
            client.delete("setup/bc/wall", "w", ignore_not_found=True)

    def test_rename_sends_put(self):
        client = _client()
        client.rename("setup/boundary-conditions/wall", "new", "old")
        assert client._strategy.last_method == "PUT"
        assert client._strategy.last_body == {"name": "new"}
        assert client._strategy.last_endpoint.endswith("wall/old")

    @patch.object(FluentRestClient, "delete")
    def test_delete_child_objects_iterates(self, mock_delete):
        _client().delete_child_objects("setup/bc", "wall", ["a", "b"])
        assert [call.args[1] for call in mock_delete.call_args_list] == ["a", "b"]

    @patch.object(FluentRestClient, "delete")
    @patch.object(FluentRestClient, "get_object_names", return_value=["x", "y"])
    def test_delete_all_child_objects(self, _mock_names, mock_delete):
        _client().delete_all_child_objects("setup/bc", "wall")
        assert mock_delete.call_count == 2

# ============================================================================
# Unit tests — command / query execution
# ============================================================================


class TestFluentRestClientExecute:
    """execute_cmd / execute_query."""

    def test_execute_cmd_appends_force(self):
        client = _client()
        client.execute_cmd("solution/initialization", "initialize")
        assert client._strategy.last_method == "POST"
        assert client._strategy.last_endpoint.endswith("initialization/initialize?force=true")

    def test_execute_cmd_without_force(self):
        client = _client()
        client.execute_cmd("solution/init", "initialize", force=False)
        assert "?force=true" not in client._strategy.last_endpoint

    def test_execute_cmd_passes_kwargs_as_body(self):
        client = _client()
        client.execute_cmd("p", "cmd", iters=5)
        assert client._strategy.last_body == {"iters": 5}

    def test_execute_query(self):
        client = _client({"result": 1})
        out = client.execute_query("reports/x", "evaluate", arg=2)
        assert client._strategy.last_endpoint.endswith("x/evaluate")
        assert client._strategy.last_body == {"arg": 2}
        assert out == {"result": 1}

# ============================================================================
# Unit tests — HttpRequestStrategy transport: JSON decoding and retry behavior
# ============================================================================


class TestHttpRequestStrategyTransport:
    """Response decoding and retry policy inside HttpRequestStrategy."""

    @patch("ansys.fluent.core.rest.transport.urllib.request.urlopen")
    def test_empty_body_returns_none(self, mock_urlopen):
        mock_urlopen.return_value = _make_raw_response(b"")
        strategy = HttpRequestStrategy(_BASE_URL)
        assert FluentRestClient(strategy).get_var("setup/x") is None

    @patch("ansys.fluent.core.rest.transport.urllib.request.urlopen")
    def test_non_json_body_returns_empty_dict(self, mock_urlopen):
        mock_urlopen.return_value = _make_raw_response(b"not json")
        strategy = HttpRequestStrategy(_BASE_URL)
        assert FluentRestClient(strategy).get_var("setup/x") == {}

    @patch("ansys.fluent.core.rest.transport.urllib.request.urlopen")
    def test_get_retries_on_502_then_succeeds(self, mock_urlopen):
        mock_urlopen.side_effect = [
            _make_http_error(502, {"detail": "bad gateway"}),
            _make_response(["inlet-1", "inlet-2"]),
        ]
        strategy = HttpRequestStrategy(_BASE_URL, retry_delay=0)
        result = FluentRestClient(strategy).get_object_names("setup/bc/velocity-inlet")
        assert result == ["inlet-1", "inlet-2"]
        assert mock_urlopen.call_count == 2

    @patch("ansys.fluent.core.rest.transport.urllib.request.urlopen")
    def test_post_does_not_retry_on_502(self, mock_urlopen):
        mock_urlopen.side_effect = _make_http_error(502)
        strategy = HttpRequestStrategy(_BASE_URL, retry_delay=0)
        with pytest.raises(FluentRestError) as exc_info:
            FluentRestClient(strategy).get_var("setup/test")  # POST -> not retryable
        assert exc_info.value.status == 502
        assert mock_urlopen.call_count == 1

    @patch("ansys.fluent.core.rest.transport.urllib.request.urlopen")
    def test_get_retry_exhaustion(self, mock_urlopen):
        mock_urlopen.side_effect = _make_http_error(503)
        strategy = HttpRequestStrategy(_BASE_URL, auth_token="t", max_retries=2, retry_delay=0)
        with pytest.raises(FluentRestError) as exc_info:
            FluentRestClient(strategy).get_object_names("setup/test")  # GET -> retryable
        assert exc_info.value.status == 503
        assert mock_urlopen.call_count == 3  # 1 initial + 2 retries

    @patch("ansys.fluent.core.rest.transport.urllib.request.urlopen")
    def test_connection_error_on_get_retries(self, mock_urlopen):
        mock_urlopen.side_effect = [
            OSError("connection refused"),
            _make_response([]),
        ]
        strategy = HttpRequestStrategy(_BASE_URL, retry_delay=0)
        assert FluentRestClient(strategy).get_object_names("setup/x") == []
        assert mock_urlopen.call_count == 2

# ============================================================================
# Unit tests — FluentRestClient.connect / connect_to_webserver
# ============================================================================


class TestConnectToWebserver:
    """The connection factory returns a configured FluentRestClient."""

    def test_returns_fluent_rest_client(self):
        client = connect_to_webserver(url=_BASE_URL, auth_token="secret")
        assert isinstance(client, FluentRestClient)

    def test_passes_url_through(self):
        client = connect_to_webserver(url="http://host:1234/", auth_token="secret")
        assert client._strategy._base_url == "http://host:1234"

    def test_stores_auth_token_and_builds_header(self):
        client = connect_to_webserver(url=_BASE_URL, auth_token="secret")
        expected = hashlib.sha256(b"secret").hexdigest()
        assert client._strategy._headers["Authorization"] == "Bearer " + expected

    def test_defaults_to_solver_component(self):
        client = connect_to_webserver(url=_BASE_URL, auth_token="secret")
        assert client._api_base == "api/fluent_1"

    def test_positional_arguments(self):
        client = connect_to_webserver(_BASE_URL, "secret")
        assert isinstance(client, FluentRestClient)
        expected = hashlib.sha256(b"secret").hexdigest()
        assert client._strategy._headers["Authorization"] == "Bearer " + expected

# ============================================================================
# Integration tests — real server (auto-skip without env/server)
# ============================================================================


@pytest.mark.real_server
class TestRealServerStaticInfo:
    """get_static_info against a live server."""

    def test_returns_dict(self, real_client):
        assert isinstance(real_client.get_static_info(), dict)

    def test_root_is_group(self, real_client):
        assert real_client.get_static_info().get("type") == "group"

    def test_has_setup_and_solution(self, real_client):
        children = set(real_client.get_static_info().get("children", {}).keys())
        assert {"setup", "solution"} <= children


@pytest.mark.real_server
class TestRealServerGetVar:
    """get_var against a live server."""

    def test_energy_enabled_is_bool(self, real_client):
        assert isinstance(real_client.get_var("setup/models/energy/enabled"), bool)

    def test_viscous_model_is_string(self, real_client):
        val = real_client.get_var("setup/models/viscous/model")
        assert isinstance(val, str) and val

    def test_nonexistent_path_raises_error(self, real_client):
        with pytest.raises(FluentRestError) as exc_info:
            real_client.get_var("setup/nonexistent/fake/path")
        assert exc_info.value.status in (404, 500)


@pytest.mark.real_server
class TestRealServerSetVar:
    """set_var against a live server (toggles then restores)."""

    def test_set_and_restore_bool(self, real_client):
        path = "setup/models/energy/enabled"
        original = real_client.get_var(path)
        assert isinstance(original, bool)
        real_client.set_var(path, not original)
        try:
            assert real_client.get_var(path) == (not original)
        finally:
            real_client.set_var(path, original)
            assert real_client.get_var(path) == original


@pytest.mark.real_server
class TestRealServerObjectListing:
    """get_object_names / get_list_size against a live server."""

    def test_velocity_inlet_returns_list(self, real_client):
        names = real_client.get_object_names("setup/boundary-conditions/velocity-inlet")
        assert isinstance(names, list)
        assert all(isinstance(n, str) for n in names)

    def test_size_matches_names(self, real_client):
        path = "setup/boundary-conditions/velocity-inlet"
        assert real_client.get_list_size(path) == len(
            real_client.get_object_names(path)
        )


@pytest.mark.real_server
class TestRealServerExecuteCmd:
    """execute_cmd against a live server."""

    def test_initialize_succeeds_or_conflicts(self, real_client):
        try:
            real_client.execute_cmd("solution/initialization", "initialize")
        except FluentRestError as exc:
            assert exc.status in (409, 500)


@pytest.mark.real_server
class TestRealServerContextManager:
    """Context-manager flow against a live server."""

    def test_context_manager_with_real_connection(self, real_client):
        with real_client:
            assert isinstance(real_client.get_var("setup/models/energy/enabled"), bool)
        assert real_client._is_closed
