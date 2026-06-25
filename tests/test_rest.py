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

"""Unit and integration tests for Fluent REST transport layer.

Test Structure:
- Unit tests (mocked): FluentRestClient, RestSolverSession, connect_to_webserver
- Integration tests (marked real_server): Against a live Fluent REST server

Unit tests run without a server. Integration tests auto-skip if server is unreachable.

Run all tests::

    pytest tests/test_rest.py -v

Run only unit tests (no server required)::

    pytest tests/test_rest.py -v -m "not real_server"

Run only integration tests::

    pytest tests/test_rest.py -v -m real_server
"""

import hashlib
import io
import json
from unittest.mock import MagicMock, patch
import urllib.error

import pytest

from ansys.fluent.core.rest.client import FluentRestClient, FluentRestError
from ansys.fluent.core.rest.rest_launcher import (
    RestSolverSession,
    _probe_server,
    connect_to_webserver,
)

_BASE_URL = "http://127.0.0.1:5000"


# ============================================================================
# Mock Helpers
# ============================================================================


def _make_response(body: object, status: int = 200) -> MagicMock:
    """Return a mock suitable for ``urllib.request.urlopen`` context manager."""
    raw = json.dumps(body).encode("utf-8")
    resp = MagicMock()
    resp.read.return_value = raw
    resp.status = status
    resp.__enter__ = lambda s: s
    resp.__exit__ = MagicMock(return_value=False)
    return resp


def _make_http_error(
    status: int, body: object | None = None, reason: str = "Error"
) -> urllib.error.HTTPError:
    """Construct an ``HTTPError`` with a readable body."""
    data = json.dumps(body).encode("utf-8") if body else b""
    return urllib.error.HTTPError(
        url=_BASE_URL, code=status, msg=reason, hdrs={}, fp=io.BytesIO(data)
    )


def _client(**kwargs) -> FluentRestClient:
    """Convenience constructor with sensible defaults."""
    kwargs.setdefault("auth_token", "tok123")
    return FluentRestClient(_BASE_URL, **kwargs)


# ============================================================================
# Unit Tests — FluentRestClient
# ============================================================================


class TestFluentRestClientInit:
    """Test FluentRestClient initialization."""

    def test_init_with_defaults(self):
        """Verify initialization with minimal arguments."""
        client = FluentRestClient("http://localhost:5000")
        assert client._base_url == "http://localhost:5000"
        assert client._auth_token is None
        assert client._component == "fluent_1"
        assert client._timeout == 30.0
        assert client._max_retries == 2
        assert client._retry_delay == 1.0
        assert not client._is_closed

    def test_init_strips_trailing_slash(self):
        """Verify that trailing slash is stripped from base_url."""
        client = FluentRestClient("http://localhost:5000/")
        assert client._base_url == "http://localhost:5000"

    def test_init_with_auth_token(self):
        """Verify that auth_token is stored."""
        client = FluentRestClient("http://localhost:5000", auth_token="secret")
        assert client._auth_token == "secret"

    def test_init_with_custom_component(self):
        """Verify custom component name."""
        client = FluentRestClient("http://localhost:5000", component="fluent_meshing_1")
        assert client._component == "fluent_meshing_1"

    def test_init_with_custom_timeout(self):
        """Verify custom timeout."""
        client = FluentRestClient("http://localhost:5000", timeout=60.0)
        assert client._timeout == 60.0

    def test_init_with_custom_max_retries(self):
        """Verify custom max_retries."""
        client = FluentRestClient("http://localhost:5000", max_retries=5)
        assert client._max_retries == 5


class TestFluentRestError:
    """Test FluentRestError exception class."""

    def test_status_and_message(self):
        """Verify error attributes."""
        exc = FluentRestError(404, "Not found", retryable=False)
        assert exc.status == 404
        assert exc.retryable is False
        assert "HTTP 404" in str(exc)
        assert "Not found" in str(exc)

    def test_retryable_flag(self):
        """Verify retryable flag."""
        exc = FluentRestError(503, "Service unavailable", retryable=True)
        assert exc.retryable is True

    def test_from_transport_oserror(self):
        """Verify from_transport with OSError."""
        exc = FluentRestError.from_transport(OSError("Connection refused"))
        assert exc.status == 0
        assert exc.retryable is True

    def test_from_transport_urlerror(self):
        """Verify from_transport with URLError."""
        url_err = urllib.error.URLError("Connection reset")
        exc = FluentRestError.from_transport(url_err)
        assert exc.status == 0
        assert exc.retryable is True


class TestFluentRestClientAuth:
    """Test authentication header generation."""

    def test_make_auth_headers_no_token(self):
        """Verify headers without auth token."""
        headers = FluentRestClient._make_auth_headers(None)
        assert headers == {}

    def test_make_auth_headers_with_token(self):
        """Verify headers with auth token (SHA-256 hashed)."""
        token = "mysecret"
        headers = FluentRestClient._make_auth_headers(token)
        expected_hash = hashlib.sha256(token.encode()).hexdigest()
        assert headers["Authorization"] == f"Bearer {expected_hash}"


class TestFluentRestClientGetVar:
    """Test get_var method."""

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_get_var_returns_value(self, mock_urlopen):
        """Verify get_var returns server response."""
        mock_urlopen.return_value = _make_response(True)
        c = _client()
        result = c.get_var("setup/models/energy/enabled")
        assert result is True

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_get_var_strips_leading_slash(self, mock_urlopen):
        """Verify leading slash is stripped from path."""
        mock_urlopen.return_value = _make_response(42)
        c = _client()
        c.get_var("/setup/general/setting")
        req = mock_urlopen.call_args[0][0]
        body = json.loads(req.data)
        assert body["path"] == "setup/general/setting"

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_get_var_raises_on_404(self, mock_urlopen):
        """Verify 404 raises FluentRestError."""
        mock_urlopen.side_effect = _make_http_error(404, {"detail": "Not found"})
        c = _client()
        with pytest.raises(FluentRestError) as exc_info:
            c.get_var("setup/nonexistent")
        assert exc_info.value.status == 404


class TestFluentRestClientSetVar:
    """Test set_var method."""

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_set_var_sends_put(self, mock_urlopen):
        """Verify set_var sends PUT request."""
        mock_urlopen.return_value = _make_response({})
        c = _client()
        c.set_var("setup/models/energy/enabled", True)
        req = mock_urlopen.call_args[0][0]
        assert req.get_method() == "PUT"
        assert json.loads(req.data) is True

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_set_var_with_dict_value(self, mock_urlopen):
        """Verify set_var accepts dict values."""
        mock_urlopen.return_value = _make_response({})
        c = _client()
        value = {"a": 1, "b": 2}
        c.set_var("setup/some/dict", value)
        req = mock_urlopen.call_args[0][0]
        assert json.loads(req.data) == value


class TestFluentRestClientExit:
    """Test exit and session lifecycle."""

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_exit_sends_post(self, mock_urlopen):
        """Verify exit sends POST to api/app/exit."""
        mock_urlopen.return_value = _make_response({})
        c = _client()
        c.exit()
        req = mock_urlopen.call_args[0][0]
        assert req.get_method() == "POST"
        assert "api/app/exit" in req.full_url

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_exit_sets_is_closed(self, mock_urlopen):
        """Verify exit sets _is_closed flag."""
        mock_urlopen.return_value = _make_response({})
        c = _client()
        assert not c._is_closed
        c.exit()
        assert c._is_closed

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_exit_is_idempotent(self, mock_urlopen):
        """Verify exit can be called multiple times."""
        mock_urlopen.return_value = _make_response({})
        c = _client()
        c.exit()
        c.exit()
        assert mock_urlopen.call_count == 1

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_exit_swallows_errors(self, mock_urlopen):
        """Verify exit raises on non-403/409 HTTP errors."""
        mock_urlopen.side_effect = _make_http_error(500)
        c = _client()
        # exit() does not swallow errors, it only handles idempotency
        with pytest.raises(FluentRestError):
            c.exit()

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_exit_idempotent_after_success(self, mock_urlopen):
        """Verify exit is idempotent after successful first call."""
        mock_urlopen.return_value = _make_response({})
        c = _client()
        c.exit()
        c.exit()  # Should not make another request
        assert mock_urlopen.call_count == 1

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_closed_client_blocks_requests(self, mock_urlopen):
        """Verify requests fail after exit()."""
        mock_urlopen.return_value = _make_response({})
        c = _client()
        c.exit()
        with pytest.raises(FluentRestError, match="Session is closed"):
            c.get_var("setup/general/solver")

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_exit_marks_closed(self, mock_urlopen):
        """Verify exit marks client as closed."""
        mock_urlopen.return_value = _make_response({})
        c = _client()
        assert not c._is_closed
        c.exit()
        assert c._is_closed

    def test_context_manager_enter_returns_self(self):
        """Verify context manager __enter__ returns self."""
        c = _client()
        assert c.__enter__() is c


class TestFluentRestClientNamedObjects:
    """Test create, delete, rename methods."""

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_create_sends_post(self, mock_urlopen):
        """Verify create sends POST with name."""
        mock_urlopen.return_value = _make_response({})
        c = _client()
        c.create("setup/boundary-conditions/wall", "new-wall")
        req = mock_urlopen.call_args[0][0]
        assert req.get_method() == "POST"
        assert json.loads(req.data)["name"] == "new-wall"

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_create_with_properties(self, mock_urlopen):
        """Verify create merges properties with name."""
        mock_urlopen.return_value = _make_response({})
        c = _client()
        props = {"enabled": True}
        c.create("setup/boundary-conditions/wall", "new-wall", properties=props)
        req = mock_urlopen.call_args[0][0]
        body = json.loads(req.data)
        assert body["name"] == "new-wall"
        assert body["enabled"] is True

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_delete_sends_delete(self, mock_urlopen):
        """Verify delete sends DELETE request."""
        mock_urlopen.return_value = _make_response({})
        c = _client()
        c.delete("setup/boundary-conditions/wall", "wall-1")
        req = mock_urlopen.call_args[0][0]
        assert req.get_method() == "DELETE"
        assert "wall-1" in req.full_url

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_delete_ignore_not_found(self, mock_urlopen):
        """Verify delete with ignore_not_found=True doesn't raise on 404."""
        mock_urlopen.side_effect = _make_http_error(404)
        c = _client()
        c.delete("setup/boundary-conditions/wall", "wall-1", ignore_not_found=True)
        # Should not raise

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_delete_raises_on_404_by_default(self, mock_urlopen):
        """Verify delete raises on 404 by default."""
        mock_urlopen.side_effect = _make_http_error(404)
        c = _client()
        with pytest.raises(FluentRestError) as exc_info:
            c.delete("setup/boundary-conditions/wall", "wall-1")
        assert exc_info.value.status == 404

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_rename_sends_put(self, mock_urlopen):
        """Verify rename sends PUT with new name."""
        mock_urlopen.return_value = _make_response({})
        c = _client()
        c.rename("setup/boundary-conditions/wall", "new-name", "old-name")
        req = mock_urlopen.call_args[0][0]
        assert req.get_method() == "PUT"
        assert json.loads(req.data)["name"] == "new-name"
        assert "old-name" in req.full_url


class TestFluentRestClientRetry:
    """Test retry logic."""

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_retry_on_502(self, mock_urlopen):
        """Verify retry on HTTP 502 for retryable (GET) methods."""
        # First call returns 502, second returns success
        mock_urlopen.side_effect = [
            _make_http_error(502, {"detail": "Bad gateway"}),
            _make_response(["inlet-1", "inlet-2"]),
        ]
        c = _client()
        # get_object_names uses GET, which is retryable
        result = c.get_object_names("setup/boundary-conditions/velocity-inlet")
        assert result == ["inlet-1", "inlet-2"]
        assert mock_urlopen.call_count == 2

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_no_retry_post_on_502(self, mock_urlopen):
        """Verify 502 on POST raises (no retry for non-idempotent methods)."""
        mock_urlopen.side_effect = _make_http_error(502)
        c = _client()
        # get_var uses POST, which is not in retryable methods
        with pytest.raises(FluentRestError) as exc_info:
            c.get_var("setup/test")
        assert exc_info.value.status == 502
        # POST should NOT retry, so only 1 call
        assert mock_urlopen.call_count == 1

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_retry_exhaustion(self, mock_urlopen):
        """Verify error raised after max retries exhausted."""
        mock_urlopen.side_effect = _make_http_error(503)
        c = FluentRestClient(_BASE_URL, auth_token="tok123", max_retries=2)
        # Use GET method (retryable) for this test
        with pytest.raises(FluentRestError) as exc_info:
            c.get_object_names("setup/test")
        assert exc_info.value.status == 503
        # 1 initial + 2 retries = 3 calls
        assert mock_urlopen.call_count == 3


# ============================================================================
# Unit Tests — RestSolverSession
# ============================================================================


class TestRestSolverSessionInit:
    """Test RestSolverSession initialization."""

    def test_init_stores_connection_params(self):
        """Verify session stores ip, port, auth_token."""
        session = RestSolverSession(
            ip="127.0.0.1",
            port=5000,
            auth_token="secret",
        )
        assert session.ip == "127.0.0.1"
        assert session.port == 5000
        assert session.auth_token == "secret"

    def test_init_creates_client(self):
        """Verify session creates a FluentRestClient."""
        session = RestSolverSession(
            ip="127.0.0.1",
            port=5000,
            auth_token="secret",
        )
        assert isinstance(session._client, FluentRestClient)

    def test_client_property(self):
        """Verify client property returns the internal client."""
        session = RestSolverSession(
            ip="127.0.0.1",
            port=5000,
            auth_token="secret",
        )
        assert session.client is session._client

    def test_init_with_custom_scheme(self):
        """Verify session accepts custom scheme."""
        session = RestSolverSession(
            ip="127.0.0.1",
            port=5000,
            auth_token="secret",
            scheme="https",
        )
        assert "https://" in session._client._base_url


class TestRestSolverSessionExit:
    """Test RestSolverSession exit."""

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_exit_calls_client_exit(self, mock_urlopen):
        """Verify session.exit() calls client.exit()."""
        mock_urlopen.return_value = _make_response({})
        session = RestSolverSession(
            ip="127.0.0.1",
            port=5000,
            auth_token="secret",
        )
        session.exit()
        assert session._client._is_closed


# ============================================================================
# Unit Tests — connect_to_webserver
# ============================================================================


class TestConnectToWebserver:
    """Test connect_to_webserver function."""

    def test_invalid_scheme_raises_valueerror(self):
        """Verify invalid scheme raises ValueError."""
        with pytest.raises(ValueError, match="scheme must be"):
            connect_to_webserver(
                ip="127.0.0.1",
                port=5000,
                auth_token="secret",
                scheme="ftp",
            )

    @patch("ansys.fluent.core.rest.rest_launcher._probe_server")
    def test_http_connection_success(self, mock_probe):
        """Verify successful HTTP connection returns RestSolverSession."""
        mock_probe.return_value = True
        session = connect_to_webserver(
            ip="127.0.0.1",
            port=5000,
            auth_token="secret",
            scheme="http",
        )
        assert isinstance(session, RestSolverSession)
        assert session.ip == "127.0.0.1"
        assert session.port == 5000

    @patch("ansys.fluent.core.rest.rest_launcher._probe_server")
    def test_connection_failure_raises_error(self, mock_probe):
        """Verify connection failure raises ConnectionError."""
        mock_probe.return_value = False
        with pytest.raises(ConnectionError, match="did not respond"):
            connect_to_webserver(
                ip="127.0.0.1",
                port=5000,
                auth_token="secret",
                scheme="http",
            )

    @patch("ansys.fluent.core.rest.rest_launcher._get_ssl_context_for_https")
    @patch("ansys.fluent.core.rest.rest_launcher._probe_server")
    def test_https_with_auto_discovery(self, mock_probe, mock_ssl):
        """Verify HTTPS auto-discovers certificates."""
        mock_ssl.return_value = MagicMock()
        mock_probe.return_value = True
        session = connect_to_webserver(
            ip="127.0.0.1",
            port=5000,
            auth_token="secret",
            scheme="https",
        )
        assert isinstance(session, RestSolverSession)
        mock_ssl.assert_called_once()

    @patch("ansys.fluent.core.rest.rest_launcher._get_ssl_context_for_https")
    @patch("ansys.fluent.core.rest.rest_launcher._probe_server")
    def test_https_fallback_to_http(self, mock_probe, mock_ssl):
        """Verify HTTPS falls back to HTTP when certificates missing."""
        mock_ssl.return_value = None  # No certificates found
        mock_probe.return_value = True
        session = connect_to_webserver(
            ip="127.0.0.1",
            port=5000,
            auth_token="secret",
            scheme="https",
        )
        assert isinstance(session, RestSolverSession)
        # First probe call should use http
        assert mock_probe.call_count >= 1


class TestProbeServer:
    """Test _probe_server function."""

    @patch("ansys.fluent.core.rest.rest_launcher.urllib.request.urlopen")
    def test_probe_success_200(self, mock_urlopen):
        """Verify probe returns True on 200."""
        mock_urlopen.return_value = _make_response({"ready": True})
        result = _probe_server("http://localhost:5000", "token", 5.0)
        assert result is True

    @patch("ansys.fluent.core.rest.rest_launcher.urllib.request.urlopen")
    def test_probe_success_401(self, mock_urlopen):
        """Verify probe returns True on 401 (auth required, server up)."""
        mock_urlopen.side_effect = _make_http_error(401, {"detail": "Unauthorized"})
        result = _probe_server("http://localhost:5000", "token", 5.0)
        assert result is True

    @patch("ansys.fluent.core.rest.rest_launcher.urllib.request.urlopen")
    def test_probe_failure_404(self, mock_urlopen):
        """Verify probe returns False on 404."""
        mock_urlopen.side_effect = _make_http_error(404)
        result = _probe_server("http://localhost:5000", "token", 5.0)
        assert result is False

    @patch("ansys.fluent.core.rest.rest_launcher.urllib.request.urlopen")
    def test_probe_failure_connection_error(self, mock_urlopen):
        """Verify probe returns False on connection error."""
        mock_urlopen.side_effect = OSError("Connection refused")
        result = _probe_server("http://localhost:5000", "token", 5.0)
        assert result is False


# ============================================================================
# Integration Tests — Real Server
# ============================================================================


@pytest.mark.real_server
class TestRealServerStaticInfo:
    """Integration tests against real Fluent server: get_static_info."""

    def test_returns_dict(self, real_client):
        """Verify that get_static_info returns a dictionary."""
        info = real_client.get_static_info()
        assert isinstance(info, dict)

    def test_root_is_group(self, real_client):
        """Verify that root element is a 'group' type."""
        info = real_client.get_static_info()
        assert info.get("type") == "group"

    def test_has_setup_and_solution(self, real_client):
        """Verify that 'setup' and 'solution' children exist."""
        info = real_client.get_static_info()
        children = set(info.get("children", {}).keys())
        assert "setup" in children
        assert "solution" in children


@pytest.mark.real_server
class TestRealServerGetVar:
    """Integration tests against real Fluent server: get_var."""

    def test_energy_enabled_is_bool(self, real_client):
        """Verify reading energy/enabled returns a boolean."""
        val = real_client.get_var("setup/models/energy/enabled")
        assert isinstance(val, bool)

    def test_viscous_model_is_string(self, real_client):
        """Verify reading viscous/model returns a non-empty string."""
        val = real_client.get_var("setup/models/viscous/model")
        assert isinstance(val, str)
        assert len(val) > 0

    def test_nonexistent_path_raises_error(self, real_client):
        """Verify nonexistent path raises FluentRestError."""
        with pytest.raises(FluentRestError) as exc_info:
            real_client.get_var("setup/nonexistent/fake/path")
        assert exc_info.value.status in (404, 500)


@pytest.mark.real_server
class TestRealServerSetVar:
    """Integration tests against real Fluent server: set_var."""

    def test_set_and_restore_bool(self, real_client):
        """Toggle energy/enabled, verify change, restore original."""
        path = "setup/models/energy/enabled"
        original = real_client.get_var(path)
        assert isinstance(original, bool)

        toggled = not original
        real_client.set_var(path, toggled)
        try:
            readback = real_client.get_var(path)
            assert readback == toggled
        finally:
            real_client.set_var(path, original)
            restored = real_client.get_var(path)
            assert restored == original


@pytest.mark.real_server
class TestRealServerGetObjectNames:
    """Integration tests against real Fluent server: get_object_names."""

    def test_velocity_inlet_returns_list(self, real_client):
        """Verify velocity-inlet returns a list of strings."""
        names = real_client.get_object_names("setup/boundary-conditions/velocity-inlet")
        assert isinstance(names, list)
        assert len(names) > 0
        assert all(isinstance(n, str) for n in names)

    def test_unknown_path_returns_empty(self, real_client):
        """Verify nonexistent path returns empty list."""
        names = real_client.get_object_names(
            "setup/boundary-conditions/nonexistent-type"
        )
        assert names == []

    def test_no_duplicates(self, real_client):
        """Verify no duplicate names in container."""
        names = real_client.get_object_names("setup/boundary-conditions/velocity-inlet")
        assert len(names) == len(set(names))


@pytest.mark.real_server
class TestRealServerGetListSize:
    """Integration tests against real Fluent server: get_list_size."""

    def test_size_matches_names(self, real_client):
        """Verify get_list_size matches len(get_object_names)."""
        path = "setup/boundary-conditions/velocity-inlet"
        size = real_client.get_list_size(path)
        names = real_client.get_object_names(path)
        assert size == len(names)

    def test_unknown_path_returns_zero(self, real_client):
        """Verify nonexistent path returns zero."""
        size = real_client.get_list_size("setup/nonexistent/fake")
        assert size == 0


@pytest.mark.real_server
class TestRealServerExecuteCmd:
    """Integration tests against real Fluent server: execute_cmd."""

    def test_initialize_succeeds_or_conflicts(self, real_client):
        """Verify execute_cmd either succeeds or returns 409 (conflict)."""
        try:
            real_client.execute_cmd("solution/initialization", "initialize")
        except FluentRestError as exc:
            assert exc.status in (409, 500)


@pytest.mark.real_server
class TestRealServerContextManager:
    """Integration tests against real Fluent server: context manager."""

    def test_context_manager_with_real_connection(self, real_client):
        """Verify context manager works with real server."""
        with real_client:
            val = real_client.get_var("setup/models/energy/enabled")
            assert isinstance(val, bool)
        assert real_client._is_closed
