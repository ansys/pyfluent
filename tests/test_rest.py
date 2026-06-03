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

"""Pytest tests against a live Fluent REST server.

All tests here are marked ``real_server`` and are **skipped automatically**
when the real server is not reachable (the ``real_client`` fixture in
``conftest.py`` handles the skip logic).

Run real-server tests::

    pytest tests/test_rest.py -v -m real_server

Tests are **case-agnostic** — they validate types, structure, and API
contracts dynamically.  No boundary-condition names, model values, or
object counts are hardcoded.

Path format: Real Fluent uses **kebab-case** (e.g. ``boundary-conditions``).
"""

import io
import json
from unittest.mock import MagicMock, patch
import urllib.error

import pytest

from ansys.fluent.core.rest.client import FluentRestClient, FluentRestError

pytestmark = pytest.mark.real_server

_BASE_URL = "http://127.0.0.1:5000"


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


# ---------------------------------------------------------------------------
# 1. get_static_info
# ---------------------------------------------------------------------------


class TestRealStaticInfo:
    """GET /api/fluent_1/static-info"""

    def test_returns_dict(self, real_client):
        """Verify that ``get_static_info()`` returns a dictionary."""
        info = real_client.get_static_info()
        assert isinstance(info, dict)

    def test_root_type_is_group(self, real_client):
        """Verify that the root of the settings tree is a 'group'."""
        info = real_client.get_static_info()
        assert info.get("type") == "group"

    def test_has_setup_and_solution(self, real_client):
        """Verify that 'setup' and 'solution' are top-level children."""
        info = real_client.get_static_info()
        children = set(info.get("children", {}).keys())
        assert "setup" in children
        assert "solution" in children

    def test_setup_has_models(self, real_client):
        """Verify that 'setup' contains 'models'."""
        info = real_client.get_static_info()
        setup_children = info["children"]["setup"].get("children", {})
        assert "models" in setup_children

    def test_setup_has_boundary_conditions(self, real_client):
        """Verify that 'setup' contains 'boundary-conditions'."""
        info = real_client.get_static_info()
        setup_children = info["children"]["setup"].get("children", {})
        assert "boundary-conditions" in setup_children


# ---------------------------------------------------------------------------
# 2. get_var — read settings
# ---------------------------------------------------------------------------


class TestRealGetVar:
    """POST /api/{component}/get_var — body: {"path": "<path>"}"""

    def test_energy_enabled_is_bool(self, real_client):
        """Verify that reading the energy model state returns a boolean."""
        val = real_client.get_var("setup/models/energy/enabled")
        assert isinstance(val, bool)

    def test_viscous_model_is_string(self, real_client):
        """Verify that reading the viscous model returns a non-empty string."""
        val = real_client.get_var("setup/models/viscous/model")
        assert isinstance(val, str)
        assert len(val) > 0

    def test_solver_time_is_string(self, real_client):
        """Verify that reading the solver time returns a non-empty string."""
        val = real_client.get_var("setup/general/solver/time")
        assert isinstance(val, str)
        assert len(val) > 0

    def test_solver_group_returns_dict(self, real_client):
        """Verify that reading a settings group returns a dictionary."""
        val = real_client.get_var("setup/general/solver")
        assert isinstance(val, dict)
        assert "time" in val

    def test_nonexistent_path_raises_error(self, real_client):
        """Verify that reading a nonexistent path raises an error."""
        with pytest.raises(FluentRestError) as exc_info:
            real_client.get_var("setup/nonexistent/fake")
        assert exc_info.value.status in (404, 500)

    def test_solution_run_calculation_is_dict(self, real_client):
        """Verify that reading a command group returns a dictionary."""
        val = real_client.get_var("solution/run-calculation")
        assert isinstance(val, dict)


# ---------------------------------------------------------------------------
# 3. set_var — write settings (read-modify-restore pattern)
# ---------------------------------------------------------------------------


class TestRealSetVar:
    """PUT /api/fluent_1/{path}"""

    def test_set_and_restore_bool(self, real_client):
        """Toggle energy enabled, verify change, then restore original."""
        path = "setup/models/energy/enabled"
        original = real_client.get_var(path)
        assert isinstance(original, bool)

        toggled = not original
        real_client.set_var(path, toggled)
        try:
            readback = real_client.get_var(path)
            assert (
                readback == toggled
            ), f"set_var did not take effect: expected {toggled}, got {readback}"
        finally:
            # Restore
            real_client.set_var(path, original)
            restored = real_client.get_var(path)
            assert restored == original

    def test_write_same_value_round_trips(self, real_client):
        """Writing the current value back should succeed or raise a
        validation error — both are acceptable."""
        path = "setup/general/solver/time"
        current = real_client.get_var(path)
        try:
            real_client.set_var(path, current)
            readback = real_client.get_var(path)
            assert readback == current
        except FluentRestError as exc:
            assert exc.status in (500, 409)


# ---------------------------------------------------------------------------
# 4. get_object_names — named-object containers (dynamic)
# ---------------------------------------------------------------------------


class TestRealGetObjectNames:
    """GET /api/fluent_1/{path} — returns dict with names as keys."""

    def test_velocity_inlet_returns_string_list(self, real_client):
        """Verify that a named-object container returns a list of strings."""
        names = real_client.get_object_names("setup/boundary-conditions/velocity-inlet")
        assert isinstance(names, list)
        assert len(names) > 0
        assert all(isinstance(n, str) for n in names)

    def test_pressure_outlet_returns_list(self, real_client):
        """Verify that another named-object container also returns a list."""
        names = real_client.get_object_names(
            "setup/boundary-conditions/pressure-outlet"
        )
        assert isinstance(names, list)
        assert len(names) > 0

    def test_wall_returns_list(self, real_client):
        """Verify that the 'wall' container returns a list of names when present."""
        names = real_client.get_object_names("setup/boundary-conditions/wall")
        assert isinstance(names, list)
        assert all(isinstance(n, str) for n in names)

    def test_unknown_path_returns_empty(self, real_client):
        """Verify that a nonexistent container path returns an empty list."""
        names = real_client.get_object_names(
            "setup/boundary-conditions/nonexistent-bc-type"
        )
        assert names == []

    def test_no_duplicates(self, real_client):
        """Verify that object names within a container are unique."""
        names = real_client.get_object_names("setup/boundary-conditions/velocity-inlet")
        assert len(names) == len(set(names))


# ---------------------------------------------------------------------------
# 5. get_list_size — cross-validated against get_object_names
# ---------------------------------------------------------------------------


class TestRealGetListSize:
    """GET /api/fluent_1/{path} — count object keys."""

    def test_velocity_inlet_size_positive(self, real_client):
        """Verify that a named-object container has a positive size."""
        size = real_client.get_list_size("setup/boundary-conditions/velocity-inlet")
        assert isinstance(size, int)
        assert size > 0

    def test_size_matches_object_names(self, real_client):
        """Verify that get_list_size agrees with len(get_object_names)."""
        path = "setup/boundary-conditions/wall"
        size = real_client.get_list_size(path)
        names = real_client.get_object_names(path)
        assert size == len(names)

    def test_unknown_path_returns_zero(self, real_client):
        """Verify that a nonexistent path returns a size of zero."""
        size = real_client.get_list_size("setup/nonexistent/fake")
        assert size == 0


# ---------------------------------------------------------------------------
# 6. get_attrs — dynamic validation
# ---------------------------------------------------------------------------


class TestRealGetAttrs:
    """GET /api/fluent_1/{path}?attrs=... — attribute retrieval."""

    def test_allowed_values_is_nonempty_string_list(self, real_client):
        """allowed-values must be a non-empty list of strings."""
        result = real_client.get_attrs("setup/models/viscous/model", ["allowed-values"])
        assert isinstance(result, dict)
        attrs = result.get("attrs", {})
        allowed = attrs.get("allowed-values", [])
        assert isinstance(allowed, list)
        assert len(allowed) > 0
        assert all(isinstance(v, str) for v in allowed)

    def test_current_value_in_allowed_values(self, real_client):
        """The current viscous model must be one of its allowed values."""
        current = real_client.get_var("setup/models/viscous/model")
        result = real_client.get_attrs("setup/models/viscous/model", ["allowed-values"])
        allowed = result.get("attrs", {}).get("allowed-values", [])
        assert (
            current in allowed
        ), f"Current model '{current}' not in allowed values: {allowed}"

    def test_set_var_respects_allowed_values(self, real_client):
        """Pick a different allowed value, set it, verify, restore."""
        path = "setup/models/viscous/model"
        original = real_client.get_var(path)
        result = real_client.get_attrs(path, ["allowed-values"])
        allowed = result.get("attrs", {}).get("allowed-values", [])

        alternatives = [v for v in allowed if v != original]
        if not alternatives:
            pytest.skip("Only one allowed viscous model — nothing to toggle")

        new_value = alternatives[0]
        try:
            real_client.set_var(path, new_value)
            readback = real_client.get_var(path)
            assert readback == new_value
        except FluentRestError as exc:
            if getattr(exc, "status", None) in (400, 409):
                pytest.skip(
                    f"Solver rejected allowed value '{new_value}' for '{path}' "
                    f"due to runtime constraints: {exc}"
                )
            pytest.fail(
                f"Unexpected REST failure while setting allowed value '{new_value}' "
                f"for '{path}': {exc}"
            )
        finally:
            try:
                real_client.set_var(path, original)
            except FluentRestError as exc:
                pytest.fail(
                    f"Failed to restore '{path}' to original value "
                    f"'{original}': {exc}"
                )


# ---------------------------------------------------------------------------
# 7. execute_cmd — command execution
# ---------------------------------------------------------------------------


class TestRealExecuteCmd:
    """POST /api/fluent_1/{path}/{cmd}"""

    def test_initialize_does_not_crash(self, real_client):
        """initialize either succeeds or returns a conflict/server error."""
        try:
            real_client.execute_cmd("solution/initialization", "initialize")
        except FluentRestError as exc:
            assert exc.status in (409, 500)


# ---------------------------------------------------------------------------
# 8. execute_query
# ---------------------------------------------------------------------------


class TestRealExecuteQuery:
    """POST /api/fluent_1/{path}/{query}"""

    def test_query_endpoint_reachable(self, real_client):
        """Query endpoint is reachable; may return error for unknown queries."""
        try:
            reply = real_client.execute_query(
                "setup/boundary-conditions/velocity-inlet", "get-zone-names"
            )
            assert reply is None or isinstance(reply, (list, str))
        except FluentRestError as exc:
            assert exc.status in (404, 405, 500)


# ===================================================================
# 9. exit / context manager
# ===================================================================


class TestExit:
    """Verify exit() sends POST to /api/connection/exit."""

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_exit_sends_post_to_connection_exit(self, mock_urlopen):
        mock_urlopen.return_value = _make_response({})
        c = _client()
        c.exit()
        req = mock_urlopen.call_args[0][0]
        assert req.get_method() == "POST"
        assert "api/connection/exit" in req.full_url

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_exit_force_true_appends_query_param(self, mock_urlopen):
        mock_urlopen.return_value = _make_response({})
        c = _client()
        c.exit(force=True)
        req = mock_urlopen.call_args[0][0]
        assert "force=true" in req.full_url

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_exit_force_false_no_query_param(self, mock_urlopen):
        mock_urlopen.return_value = _make_response({})
        c = _client()
        c.exit(force=False)
        req = mock_urlopen.call_args[0][0]
        assert "force=true" not in req.full_url
        assert req.full_url.endswith("api/connection/exit")

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_exit_raises_on_403(self, mock_urlopen):
        mock_urlopen.side_effect = _make_http_error(
            403, body={"detail": "Exit is not allowed."}
        )
        c = _client()
        with pytest.raises(FluentRestError, match="403"):
            c.exit()

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_exit_raises_on_409(self, mock_urlopen):
        mock_urlopen.side_effect = _make_http_error(
            409, body={"show-prompt": "Save changes?"}
        )
        c = _client()
        with pytest.raises(FluentRestError, match="409"):
            c.exit(force=False)

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_exit_swallows_connection_error(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("Connection refused")
        c = _client()
        c.exit()  # should not raise

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_exit_swallows_other_http_errors(self, mock_urlopen):
        mock_urlopen.side_effect = _make_http_error(500)
        c = _client()
        c.exit()  # should not raise (server may be down)

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_context_manager_calls_exit(self, mock_urlopen):
        mock_urlopen.return_value = _make_response({})
        c = _client()
        with c:
            pass
        req = mock_urlopen.call_args[0][0]
        assert "api/connection/exit" in req.full_url

    def test_context_manager_enter_returns_self(self):
        c = _client()
        assert c.__enter__() is c


# ===================================================================
# API endpoint wiring — create / delete / rename
# ===================================================================


class TestNamedObjectMutation:
    """Verify create/delete/rename build the correct HTTP requests."""

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_create_sends_post_with_name(self, mock_urlopen):
        mock_urlopen.return_value = _make_response({})
        c = _client()
        c.create("setup/bc/wall", "new-wall")
        req = mock_urlopen.call_args[0][0]
        assert req.get_method() == "POST"
        assert json.loads(req.data) == {"name": "new-wall"}
        assert "setup/bc/wall" in req.full_url

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_delete_sends_delete(self, mock_urlopen):
        mock_urlopen.return_value = _make_response({})
        c = _client()
        c.delete("setup/bc/wall", "wall-1")
        req = mock_urlopen.call_args[0][0]
        assert req.get_method() == "DELETE"
        assert "setup/bc/wall/wall-1" in req.full_url

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_delete_ignore_not_found(self, mock_urlopen):
        mock_urlopen.side_effect = _make_http_error(404, {"detail": "gone"})
        c = _client()
        # Must not raise
        c.delete("setup/bc/wall", "wall-1", ignore_not_found=True)

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_delete_raises_on_404_by_default(self, mock_urlopen):
        mock_urlopen.side_effect = _make_http_error(404, {"detail": "gone"})
        c = _client()
        with pytest.raises(FluentRestError) as exc_info:
            c.delete("setup/bc/wall", "wall-1")
        assert exc_info.value.status == 404

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_rename_sends_put_with_new_name(self, mock_urlopen):
        mock_urlopen.return_value = _make_response({})
        c = _client()
        c.rename("setup/bc/wall", "new-name", "old-name")
        req = mock_urlopen.call_args[0][0]
        assert req.get_method() == "PUT"
        assert json.loads(req.data) == {"name": "new-name"}
        assert "setup/bc/wall/old-name" in req.full_url

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_delete_child_objects_calls_delete_for_each(self, mock_urlopen):
        mock_urlopen.return_value = _make_response({})
        c = _client()
        c.delete_child_objects("setup/bc", "wall", ["w1", "w2"])
        assert mock_urlopen.call_count == 2
        urls = [call[0][0].full_url for call in mock_urlopen.call_args_list]
        assert any("wall/w1" in u for u in urls)
        assert any("wall/w2" in u for u in urls)

    @patch("ansys.fluent.core.rest.client.urllib.request.urlopen")
    def test_delete_all_child_objects(self, mock_urlopen):
        """delete_all discovers names via GET, then deletes each."""
        # First call: GET returns object names
        get_resp = _make_response({"w1": {}, "w2": {}})
        delete_resp = _make_response({})
        mock_urlopen.side_effect = [get_resp, delete_resp, delete_resp]
        c = _client()
        c.delete_all_child_objects("setup/bc", "wall")
        # 1 GET + 2 DELETEs
        assert mock_urlopen.call_count == 3
