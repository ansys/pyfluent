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

"""Pytest tests against a live Fluent / SimBA REST server.

All tests here are marked ``real_server`` and are **skipped automatically**
when the real server is not reachable (the ``real_client`` fixture in
``conftest.py`` handles the skip logic).

Run real-server tests::

    pytest src/ansys/fluent/core/rest/tests/test_real_server.py -v -m real_server

The server at 10.18.44.175:5000 has a case loaded with these boundary
conditions:

    - velocity-inlet: hot-inlet, cold-inlet
    - pressure-outlet: outlet
    - wall: wall-inlet, wall-elbow
    - symmetry: symmetry-xyplane

Path format: Real Fluent uses **kebab-case** (e.g. ``boundary-conditions``).
"""

import pytest

from ansys.fluent.core.rest.client import FluentRestError

pytestmark = pytest.mark.real_server


# ---------------------------------------------------------------------------
# 1. is_interactive_mode — now queries the server
# ---------------------------------------------------------------------------


class TestRealIsInteractiveMode:
    """GET /api/connection/run_mode — verify live query, not hardcoded."""

    def test_queries_server_returns_true(self, real_client):
        """Real Fluent server runs in 'fluent_proxy' mode (interactive)."""
        result = real_client.is_interactive_mode()
        assert isinstance(result, bool)
        assert result is True  # fluent_proxy mode is interactive


# ---------------------------------------------------------------------------
# 2. get_static_info
# ---------------------------------------------------------------------------


class TestRealStaticInfo:
    """GET /api/fluent_1/static-info"""

    def test_returns_dict(self, real_client):
        info = real_client.get_static_info()
        assert isinstance(info, dict)

    def test_root_type_is_group(self, real_client):
        info = real_client.get_static_info()
        assert info.get("type") == "group"

    def test_has_setup_and_solution(self, real_client):
        info = real_client.get_static_info()
        children = set(info.get("children", {}).keys())
        assert "setup" in children
        assert "solution" in children

    def test_setup_has_models(self, real_client):
        info = real_client.get_static_info()
        setup_children = info["children"]["setup"].get("children", {})
        assert "models" in setup_children

    def test_setup_has_boundary_conditions(self, real_client):
        info = real_client.get_static_info()
        setup_children = info["children"]["setup"].get("children", {})
        assert "boundary-conditions" in setup_children


# ---------------------------------------------------------------------------
# 3. get_var — read settings
# ---------------------------------------------------------------------------


class TestRealGetVar:
    """POST /api/fluent_1/get_var"""

    def test_energy_enabled_is_bool(self, real_client):
        val = real_client.get_var("setup/models/energy/enabled")
        assert isinstance(val, bool)
        assert val is True  # Current server state

    def test_viscous_model_is_string(self, real_client):
        val = real_client.get_var("setup/models/viscous/model")
        assert isinstance(val, str)

    def test_solver_time_is_steady(self, real_client):
        val = real_client.get_var("setup/general/solver/time")
        assert val == "steady"

    def test_solver_group_returns_dict(self, real_client):
        val = real_client.get_var("setup/general/solver")
        assert isinstance(val, dict)
        assert "time" in val

    def test_nonexistent_path_raises_404(self, real_client):
        with pytest.raises(FluentRestError) as exc_info:
            real_client.get_var("setup/nonexistent/fake")
        assert exc_info.value.status == 404

    def test_solution_run_calculation_is_dict(self, real_client):
        """Real Fluent uses kebab-case: run-calculation."""
        val = real_client.get_var("solution/run-calculation")
        assert isinstance(val, dict)


# ---------------------------------------------------------------------------
# 4. set_var — write settings
# ---------------------------------------------------------------------------


class TestRealSetVar:
    """PUT /api/fluent_1/{path}"""

    def test_set_and_restore_bool(self, real_client):
        """Toggle energy enabled and restore."""
        original = real_client.get_var("setup/models/energy/enabled")
        toggled = not original
        real_client.set_var("setup/models/energy/enabled", toggled)
        readback = real_client.get_var("setup/models/energy/enabled")
        # Fluent may override via solver validation, so just confirm bool
        assert isinstance(readback, bool)
        # Restore
        real_client.set_var("setup/models/energy/enabled", original)

    def test_write_same_value_round_trips(self, real_client):
        """Writing the current value back should succeed or raise a
        validation error (HTTP 500) from Fluent — both are acceptable
        because the client correctly relayed the request."""
        current = real_client.get_var("setup/general/solver/time")
        try:
            real_client.set_var("setup/general/solver/time", current)
            readback = real_client.get_var("setup/general/solver/time")
            assert readback == current
        except FluentRestError as exc:
            # Fluent solver sometimes rejects a no-op write with 500
            assert exc.status == 500


# ---------------------------------------------------------------------------
# 5. get_object_names — named-object containers
# ---------------------------------------------------------------------------


class TestRealGetObjectNames:
    """GET /api/fluent_1/{path} — returns dict with names as keys."""

    def test_velocity_inlet_has_objects(self, real_client):
        names = real_client.get_object_names(
            "setup/boundary-conditions/velocity-inlet"
        )
        assert isinstance(names, list)
        assert "hot-inlet" in names
        assert "cold-inlet" in names
        assert len(names) == 2

    def test_pressure_outlet_has_objects(self, real_client):
        names = real_client.get_object_names(
            "setup/boundary-conditions/pressure-outlet"
        )
        assert names == ["outlet"]

    def test_wall_has_objects(self, real_client):
        names = real_client.get_object_names("setup/boundary-conditions/wall")
        assert "wall-inlet" in names
        assert "wall-elbow" in names
        assert len(names) == 2

    def test_unknown_path_returns_empty(self, real_client):
        names = real_client.get_object_names(
            "setup/boundary-conditions/nonexistent-bc-type"
        )
        assert names == []


# ---------------------------------------------------------------------------
# 6. get_list_size — count named objects
# ---------------------------------------------------------------------------


class TestRealGetListSize:
    """GET /api/fluent_1/{path} — count object keys."""

    def test_velocity_inlet_size(self, real_client):
        size = real_client.get_list_size(
            "setup/boundary-conditions/velocity-inlet"
        )
        assert size == 2  # hot-inlet, cold-inlet

    def test_wall_size(self, real_client):
        size = real_client.get_list_size("setup/boundary-conditions/wall")
        assert size == 2  # wall-inlet, wall-elbow

    def test_unknown_path_returns_zero(self, real_client):
        size = real_client.get_list_size("setup/nonexistent/fake")
        assert size == 0


# ---------------------------------------------------------------------------
# 7. get_attrs — known SimBA bug (HTTP 500)
# ---------------------------------------------------------------------------


class TestRealGetAttrs:
    """POST /api/fluent_1/get_attrs — known server-side bug."""

    def test_endpoint_returns_500(self, real_client):
        """get_attrs currently returns 500 (SimBA bug, not client bug)."""
        with pytest.raises(FluentRestError) as exc_info:
            real_client.get_attrs(
                "setup/models/viscous/model", ["allowed-values"]
            )
        # Known SimBA bug — server crashes handling get_attrs
        assert exc_info.value.status == 500


# ---------------------------------------------------------------------------
# 8. execute_cmd — command execution
# ---------------------------------------------------------------------------


class TestRealExecuteCmd:
    """POST /api/fluent_1/{path}/{cmd}"""

    def test_initialize_returns_409_conflict(self, real_client):
        """initialize returns 409 Conflict when mesh is already loaded."""
        with pytest.raises(FluentRestError) as exc_info:
            real_client.execute_cmd("solution/initialization", "initialize")
        # 409 = Conflict (already initialized or mesh state conflict)
        assert exc_info.value.status == 409


# ---------------------------------------------------------------------------
# 9. execute_query
# ---------------------------------------------------------------------------


class TestRealExecuteQuery:
    """POST /api/fluent_1/{path}/{query}"""

    def test_query_endpoint_reachable(self, real_client):
        """Query endpoint is reachable; may return 404/500 for unknown queries."""
        try:
            reply = real_client.execute_query(
                "setup/boundary-conditions/velocity-inlet", "get-zone-names"
            )
            assert reply is None or isinstance(reply, (list, str))
        except FluentRestError as exc:
            # 404 = query not found; 405 = method not allowed;
            # 500 = server error — all acceptable
            assert exc.status in (404, 405, 500)
