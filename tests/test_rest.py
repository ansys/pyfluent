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

* :class:`ansys.fluent.core.rest.client.FluentRestClient` — the pure-stdlib
  HTTP client (``client.py``).
* :func:`ansys.fluent.core.rest.rest_connect.connect_to_webserver` — the thin
  connection helper that returns a ``FluentRestClient`` (``rest_connect.py``).
* The package re-exports in ``ansys/fluent/core/rest/__init__.py``.

Test structure
--------------
- Unit tests (mocked ``urllib``): run anywhere, no server required.
- Integration tests (marked ``real_server``): run against a live Fluent REST
  server. They use the ``real_client`` fixture from ``conftest.py`` and
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
from ansys.fluent.core.rest.client import (
    FluentRestClient as FluentRestClientDirect,
)
from ansys.fluent.core.rest.rest_connect import (
    connect_to_webserver as connect_to_webserver_direct,
)

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


def _client(**kwargs) -> FluentRestClient:
    """Convenience constructor with sensible defaults (no retry back-off wait)."""
    kwargs.setdefault("auth_token", "tok123")
    kwargs.setdefault("retry_delay", 0)  # keep retry tests fast
    return FluentRestClient(_BASE_URL, **kwargs)


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
        assert connect_to_webserver is connect_to_webserver_direct

    def test_error_is_runtimeerror_subclass(self):
        """``FluentRestError`` stays a ``RuntimeError`` for broad ``except``."""
        assert issubclass(FluentRestError, RuntimeError)


# ============================================================================
# Unit tests — FluentRestClient construction
# ============================================================================


class TestFluentRestClientInit:
    """FluentRestClient initialization."""

    def test_init_with_defaults(self):
        client = FluentRestClient("http://localhost:5000")
        assert client._base_url == "http://localhost:5000"
        assert client._auth_token is None
        assert client._component == "fluent_1"
        assert client._api_base == "api/fluent_1"
        assert client._timeout == 30.0
        assert client._max_retries == 2
        assert client._retry_delay == 1.0
        assert not client._is_closed

    def test_init_strips_trailing_slash(self):
        client = FluentRestClient("http://localhost:5000/")
        assert client._base_url == "http://localhost:5000"

    def test_init_with_auth_token(self):
        client = FluentRestClient("http://localhost:5000", auth_token="secret")
        assert client._auth_token == "secret"

    def test_init_with_custom_component(self):
        client = FluentRestClient("http://localhost:5000", component="fluent_meshing_1")
        assert client._component == "fluent_meshing_1"
        assert client._api_base == "api/fluent_meshing_1"

    def test_init_with_custom_timeout(self):
        client = FluentRestClient("http://localhost:5000", timeout=60.0)
        assert client._timeout == 60.0

    def test_init_with_custom_max_retries(self):
        client = FluentRestClient("http://localhost:5000", max_retries=5)
        assert client._max_retries == 5


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


class TestFluentRestClientAuth:
    """Authorization header generation."""

    def test_make_auth_headers_no_token(self):
        assert FluentRestClient._make_auth_headers(None) == {}
        assert FluentRestClient._make_auth_headers("") == {}

    def test_make_auth_headers_with_token(self):
        token = "mysecret"
        headers = FluentRestClient._make_auth_headers(token)
        expected = hashlib.sha256(token.encode()).hexdigest()
        assert headers["Authorization"] == f"Bearer {expected}"

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_auth_header_attached_to_requests(self, mock_urlopen):
        mock_urlopen.return_value = _make_response(True)
        c = _client(auth_token="abc")
        c.get_var("setup/x")
        req = mock_urlopen.call_args[0][0]
        expected = hashlib.sha256(b"abc").hexdigest()
        assert req.get_header("Authorization") == f"Bearer {expected}"

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_no_auth_header_when_token_absent(self, mock_urlopen):
        mock_urlopen.return_value = _make_response(True)
        c = FluentRestClient(_BASE_URL)  # no token
        c.get_var("setup/x")
        req = mock_urlopen.call_args[0][0]
        assert req.get_header("Authorization") is None


# ============================================================================
# Unit tests — read endpoints
# ============================================================================


class TestFluentRestClientReads:
    """get_static_info / get_var / get_attrs and list/name normalization."""

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_get_static_info_path(self, mock_urlopen):
        mock_urlopen.return_value = _make_response({"type": "group"})
        result = _client().get_static_info()
        req = mock_urlopen.call_args[0][0]
        assert req.get_method() == "GET"
        assert req.full_url.endswith("api/fluent_1/static-info")
        assert result == {"type": "group"}

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_get_static_info_full_query(self, mock_urlopen):
        mock_urlopen.return_value = _make_response({"type": "group"})
        _client().get_static_info(full=True)
        req = mock_urlopen.call_args[0][0]
        assert req.full_url.endswith("static-info?full=true")

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_get_var_returns_value(self, mock_urlopen):
        mock_urlopen.return_value = _make_response(True)
        assert _client().get_var("setup/models/energy/enabled") is True

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_get_var_uses_post_and_strips_leading_slash(self, mock_urlopen):
        mock_urlopen.return_value = _make_response(42)
        _client().get_var("/setup/general/setting")
        req = mock_urlopen.call_args[0][0]
        assert req.get_method() == "POST"
        assert json.loads(req.data)["path"] == "setup/general/setting"

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_get_var_raises_on_404(self, mock_urlopen):
        mock_urlopen.side_effect = _make_http_error(404, {"detail": "Not found"})
        with pytest.raises(FluentRestError) as exc_info:
            _client().get_var("setup/nonexistent")
        assert exc_info.value.status == 404

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_get_attrs_builds_query(self, mock_urlopen):
        mock_urlopen.return_value = _make_response({"min": 0, "max": 1})
        _client().get_attrs("setup/x", ["min", "max"], recursive=True)
        req = mock_urlopen.call_args[0][0]
        assert req.get_method() == "GET"
        assert "attrs=min%2Cmax" in req.full_url
        assert "recursive=true" in req.full_url

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_get_object_names_from_list(self, mock_urlopen):
        mock_urlopen.return_value = _make_response(["a", "b"])
        assert _client().get_object_names("setup/bc/velocity-inlet") == ["a", "b"]

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_get_object_names_from_dict_keys(self, mock_urlopen):
        mock_urlopen.return_value = _make_response({"a": {}, "b": {}})
        assert sorted(_client().get_object_names("setup/bc/wall")) == ["a", "b"]

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_get_list_size_from_list(self, mock_urlopen):
        mock_urlopen.return_value = _make_response([1, 2, 3])
        assert _client().get_list_size("setup/list") == 3

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_get_list_size_uses_explicit_size_field(self, mock_urlopen):
        mock_urlopen.return_value = _make_response({"size": 7, "a": {}})
        assert _client().get_list_size("setup/container") == 7

    def test_names_from_handles_unexpected_type(self):
        assert FluentRestClient._names_from(None) == []
        assert FluentRestClient._names_from(5) == []

    def test_size_from_handles_unexpected_type(self):
        assert FluentRestClient._size_from(None) == 0
        assert FluentRestClient._size_from("x") == 0


# ============================================================================
# Unit tests — write endpoints
# ============================================================================


class TestFluentRestClientWrites:
    """set_var / resize_list_object."""

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_set_var_sends_put(self, mock_urlopen):
        mock_urlopen.return_value = _make_response({})
        _client().set_var("setup/models/energy/enabled", True)
        req = mock_urlopen.call_args[0][0]
        assert req.get_method() == "PUT"
        assert json.loads(req.data) is True

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_set_var_with_dict_value(self, mock_urlopen):
        mock_urlopen.return_value = _make_response({})
        value = {"a": 1, "b": 2}
        _client().set_var("setup/some/dict", value)
        assert json.loads(mock_urlopen.call_args[0][0].data) == value

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_resize_list_object(self, mock_urlopen):
        mock_urlopen.return_value = _make_response({})
        _client().resize_list_object("setup/list", 4)
        req = mock_urlopen.call_args[0][0]
        assert req.get_method() == "POST"
        assert json.loads(req.data) == {"new-size": 4}


# ============================================================================
# Unit tests — named-object CRUD
# ============================================================================


class TestFluentRestClientNamedObjects:
    """create / delete / rename / bulk delete."""

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_create_sends_post_with_name(self, mock_urlopen):
        mock_urlopen.return_value = _make_response({})
        _client().create("setup/boundary-conditions/wall", "new-wall")
        req = mock_urlopen.call_args[0][0]
        assert req.get_method() == "POST"
        assert json.loads(req.data)["name"] == "new-wall"

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_create_merges_properties(self, mock_urlopen):
        mock_urlopen.return_value = _make_response({})
        _client().create(
            "setup/boundary-conditions/wall", "w", properties={"enabled": True}
        )
        body = json.loads(mock_urlopen.call_args[0][0].data)
        assert body == {"enabled": True, "name": "w"}

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_create_without_name_omits_name_key(self, mock_urlopen):
        mock_urlopen.return_value = _make_response({})
        _client().create("setup/bc/wall")
        assert "name" not in json.loads(mock_urlopen.call_args[0][0].data)

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_delete_sends_delete(self, mock_urlopen):
        mock_urlopen.return_value = _make_response({})
        _client().delete("setup/boundary-conditions/wall", "wall-1")
        req = mock_urlopen.call_args[0][0]
        assert req.get_method() == "DELETE"
        assert req.full_url.endswith("wall/wall-1")

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_delete_url_encodes_name(self, mock_urlopen):
        mock_urlopen.return_value = _make_response({})
        _client().delete("setup/bc/wall", "wall 1/special")
        assert "wall%201%2Fspecial" in mock_urlopen.call_args[0][0].full_url

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_delete_ignore_not_found_swallows_404(self, mock_urlopen):
        mock_urlopen.side_effect = _make_http_error(404)
        _client().delete("setup/bc/wall", "w", ignore_not_found=True)  # no raise

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_delete_raises_on_404_by_default(self, mock_urlopen):
        mock_urlopen.side_effect = _make_http_error(404)
        with pytest.raises(FluentRestError) as exc_info:
            _client().delete("setup/bc/wall", "w")
        assert exc_info.value.status == 404

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_delete_ignore_not_found_still_raises_500(self, mock_urlopen):
        mock_urlopen.side_effect = _make_http_error(500)
        with pytest.raises(FluentRestError):
            _client().delete("setup/bc/wall", "w", ignore_not_found=True)

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_rename_sends_put(self, mock_urlopen):
        mock_urlopen.return_value = _make_response({})
        _client().rename("setup/boundary-conditions/wall", "new", "old")
        req = mock_urlopen.call_args[0][0]
        assert req.get_method() == "PUT"
        assert json.loads(req.data)["name"] == "new"
        assert req.full_url.endswith("wall/old")

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

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_execute_cmd_appends_force(self, mock_urlopen):
        mock_urlopen.return_value = _make_response({})
        _client().execute_cmd("solution/initialization", "initialize")
        req = mock_urlopen.call_args[0][0]
        assert req.get_method() == "POST"
        assert req.full_url.endswith("initialization/initialize?force=true")

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_execute_cmd_without_force(self, mock_urlopen):
        mock_urlopen.return_value = _make_response({})
        _client().execute_cmd("solution/init", "initialize", force=False)
        assert "?force=true" not in mock_urlopen.call_args[0][0].full_url

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_execute_cmd_passes_kwargs_as_body(self, mock_urlopen):
        mock_urlopen.return_value = _make_response({})
        _client().execute_cmd("p", "cmd", iters=5)
        assert json.loads(mock_urlopen.call_args[0][0].data) == {"iters": 5}

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_execute_query(self, mock_urlopen):
        mock_urlopen.return_value = _make_response({"result": 1})
        out = _client().execute_query("reports/x", "evaluate", arg=2)
        req = mock_urlopen.call_args[0][0]
        assert req.full_url.endswith("x/evaluate")
        assert json.loads(req.data) == {"arg": 2}
        assert out == {"result": 1}


# ============================================================================
# Unit tests — session lifecycle / context manager
# ============================================================================


class TestFluentRestClientLifecycle:
    """exit, closed-state guarding, and context-manager protocol."""

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_exit_sends_post_to_app_exit(self, mock_urlopen):
        mock_urlopen.return_value = _make_response({})
        c = _client()
        c.exit()
        req = mock_urlopen.call_args[0][0]
        assert req.get_method() == "POST"
        assert "api/app/exit" in req.full_url
        assert c._is_closed

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_exit_is_idempotent(self, mock_urlopen):
        mock_urlopen.return_value = _make_response({})
        c = _client()
        c.exit()
        c.exit()
        assert mock_urlopen.call_count == 1

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_exit_raises_on_server_error(self, mock_urlopen):
        mock_urlopen.side_effect = _make_http_error(500)
        with pytest.raises(FluentRestError):
            _client().exit()

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_closed_client_blocks_requests(self, mock_urlopen):
        mock_urlopen.return_value = _make_response({})
        c = _client()
        c.exit()
        with pytest.raises(FluentRestError, match="Session is closed"):
            c.get_var("setup/general/solver")

    def test_context_manager_enter_returns_self(self):
        c = _client()
        assert c.__enter__() is c

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_context_manager_calls_exit_on_block_close(self, mock_urlopen):
        """``with client:`` must close the session (regression: __exit__ args)."""
        mock_urlopen.return_value = _make_response({})
        c = _client()
        with c as entered:
            assert entered is c
            assert not c._is_closed
        assert c._is_closed
        assert "api/app/exit" in mock_urlopen.call_args[0][0].full_url

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_context_manager_exits_on_exception(self, mock_urlopen):
        """The session is still closed when the body raises."""
        mock_urlopen.return_value = _make_response({})
        c = _client()
        with pytest.raises(ValueError):
            with c:
                raise ValueError("boom")
        assert c._is_closed


# ============================================================================
# Unit tests — transport: JSON decoding and retry behavior
# ============================================================================


class TestFluentRestClientTransport:
    """Response decoding and retry policy."""

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_empty_body_returns_none(self, mock_urlopen):
        mock_urlopen.return_value = _make_raw_response(b"")
        assert _client().get_var("setup/x") is None

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_non_json_body_returns_empty_dict(self, mock_urlopen):
        mock_urlopen.return_value = _make_raw_response(b"not json")
        assert _client().get_var("setup/x") == {}

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_get_retries_on_502_then_succeeds(self, mock_urlopen):
        mock_urlopen.side_effect = [
            _make_http_error(502, {"detail": "bad gateway"}),
            _make_response(["inlet-1", "inlet-2"]),
        ]
        result = _client().get_object_names("setup/bc/velocity-inlet")
        assert result == ["inlet-1", "inlet-2"]
        assert mock_urlopen.call_count == 2

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_post_does_not_retry_on_502(self, mock_urlopen):
        mock_urlopen.side_effect = _make_http_error(502)
        with pytest.raises(FluentRestError) as exc_info:
            _client().get_var("setup/test")  # get_var is POST -> not retryable
        assert exc_info.value.status == 502
        assert mock_urlopen.call_count == 1

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_get_retry_exhaustion(self, mock_urlopen):
        mock_urlopen.side_effect = _make_http_error(503)
        c = FluentRestClient(_BASE_URL, auth_token="t", max_retries=2, retry_delay=0)
        with pytest.raises(FluentRestError) as exc_info:
            c.get_object_names("setup/test")  # GET -> retryable
        assert exc_info.value.status == 503
        assert mock_urlopen.call_count == 3  # 1 initial + 2 retries

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_connection_error_on_get_retries(self, mock_urlopen):
        mock_urlopen.side_effect = [
            OSError("connection refused"),
            _make_response([]),
        ]
        assert _client().get_object_names("setup/x") == []
        assert mock_urlopen.call_count == 2


# ============================================================================
# Unit tests — connect_to_webserver (rest_connect.py)
# ============================================================================


class TestConnectToWebserver:
    """The connection helper returns a configured FluentRestClient."""

    def test_returns_fluent_rest_client(self):
        client = connect_to_webserver(url=_BASE_URL, auth_token="secret")
        assert isinstance(client, FluentRestClient)

    def test_passes_url_through(self):
        client = connect_to_webserver(url="http://host:1234/", auth_token="secret")
        assert client._base_url == "http://host:1234"

    def test_stores_auth_token_and_builds_header(self):
        client = connect_to_webserver(url=_BASE_URL, auth_token="secret")
        assert client._auth_token == "secret"
        expected = hashlib.sha256(b"secret").hexdigest()
        assert client._headers["Authorization"] == f"Bearer {expected}"

    def test_defaults_to_solver_component(self):
        client = connect_to_webserver(url=_BASE_URL, auth_token="secret")
        assert client._component == "fluent_1"

    def test_positional_arguments(self):
        client = connect_to_webserver(_BASE_URL, "secret")
        assert isinstance(client, FluentRestClient)
        assert client._auth_token == "secret"


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
        names = real_client.get_object_names(
            "setup/boundary-conditions/velocity-inlet"
        )
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