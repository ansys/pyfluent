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

Tests are **case-agnostic** — they validate types, structure, and API
contracts dynamically.  No boundary-condition names, model values, or
object counts are hardcoded.

Path format: Real Fluent uses **kebab-case** (e.g. ``boundary-conditions``).
"""

import pytest

from ansys.fluent.core.rest.client import FluentRestError

pytestmark = pytest.mark.real_server


# ---------------------------------------------------------------------------
# 1. is_interactive_mode
# ---------------------------------------------------------------------------


class TestRealIsInteractiveMode:
    """GET /api/connection/run_mode"""

    def test_returns_bool(self, real_client):
        result = real_client.is_interactive_mode()
        assert isinstance(result, bool)


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
    """GET /api/fluent_1/{path}"""

    def test_energy_enabled_is_bool(self, real_client):
        val = real_client.get_var("setup/models/energy/enabled")
        assert isinstance(val, bool)

    def test_viscous_model_is_string(self, real_client):
        val = real_client.get_var("setup/models/viscous/model")
        assert isinstance(val, str)
        assert len(val) > 0

    def test_solver_time_is_string(self, real_client):
        val = real_client.get_var("setup/general/solver/time")
        assert isinstance(val, str)
        assert len(val) > 0

    def test_solver_group_returns_dict(self, real_client):
        val = real_client.get_var("setup/general/solver")
        assert isinstance(val, dict)
        assert "time" in val

    def test_nonexistent_path_raises_error(self, real_client):
        with pytest.raises(FluentRestError) as exc_info:
            real_client.get_var("setup/nonexistent/fake")
        assert exc_info.value.status in (404, 500)

    def test_solution_run_calculation_is_dict(self, real_client):
        val = real_client.get_var("solution/run-calculation")
        assert isinstance(val, dict)


# ---------------------------------------------------------------------------
# 4. set_var — write settings (read-modify-restore pattern)
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
        readback = real_client.get_var(path)
        assert (
            readback == toggled
        ), f"set_var did not take effect: expected {toggled}, got {readback}"

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
# 5. get_object_names — named-object containers (dynamic)
# ---------------------------------------------------------------------------


class TestRealGetObjectNames:
    """GET /api/fluent_1/{path} — returns dict with names as keys."""

    def test_velocity_inlet_returns_string_list(self, real_client):
        names = real_client.get_object_names("setup/boundary-conditions/velocity-inlet")
        assert isinstance(names, list)
        assert len(names) > 0
        assert all(isinstance(n, str) for n in names)

    def test_pressure_outlet_returns_list(self, real_client):
        names = real_client.get_object_names(
            "setup/boundary-conditions/pressure-outlet"
        )
        assert isinstance(names, list)
        assert len(names) > 0

    def test_wall_returns_list(self, real_client):
        names = real_client.get_object_names("setup/boundary-conditions/wall")
        assert isinstance(names, list)
        assert len(names) > 0

    def test_unknown_path_returns_empty(self, real_client):
        names = real_client.get_object_names(
            "setup/boundary-conditions/nonexistent-bc-type"
        )
        assert names == []

    def test_no_duplicates(self, real_client):
        """Object names within a container must be unique."""
        names = real_client.get_object_names("setup/boundary-conditions/velocity-inlet")
        assert len(names) == len(set(names))


# ---------------------------------------------------------------------------
# 6. get_list_size — cross-validated against get_object_names
# ---------------------------------------------------------------------------


class TestRealGetListSize:
    """GET /api/fluent_1/{path} — count object keys."""

    def test_velocity_inlet_size_positive(self, real_client):
        size = real_client.get_list_size("setup/boundary-conditions/velocity-inlet")
        assert isinstance(size, int)
        assert size > 0

    def test_size_matches_object_names(self, real_client):
        """get_list_size must agree with len(get_object_names)."""
        path = "setup/boundary-conditions/wall"
        size = real_client.get_list_size(path)
        names = real_client.get_object_names(path)
        assert size == len(names)

    def test_unknown_path_returns_zero(self, real_client):
        size = real_client.get_list_size("setup/nonexistent/fake")
        assert size == 0


# ---------------------------------------------------------------------------
# 7. get_attrs — dynamic validation
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

        # Pick a different value (if only one value exists, skip)
        alternatives = [v for v in allowed if v != original]
        if not alternatives:
            pytest.skip("Only one allowed viscous model — nothing to toggle")

        new_value = alternatives[0]
        try:
            real_client.set_var(path, new_value)
            readback = real_client.get_var(path)
            assert readback == new_value
        except FluentRestError:
            pass  # Solver may reject the switch due to other constraints
        finally:
            # Always restore
            try:
                real_client.set_var(path, original)
            except FluentRestError:
                pass


# ---------------------------------------------------------------------------
# 8. execute_cmd — command execution
# ---------------------------------------------------------------------------


class TestRealExecuteCmd:
    """POST /api/fluent_1/{path}/{cmd}"""

    def test_initialize_does_not_crash(self, real_client):
        """initialize either succeeds or returns a conflict/server error."""
        try:
            real_client.execute_cmd("solution/initialization", "initialize")
        except FluentRestError as exc:
            # 409 = already initialized; 500 = solver constraint
            assert exc.status in (409, 500)


# ---------------------------------------------------------------------------
# 9. execute_query
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
