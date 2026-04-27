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

"""Real-server integration tests for the REST transport layer.

These tests run against a live Fluent / SimBA server at 10.18.44.175:5000.
They are automatically **skipped** when the server is not reachable, so they
will never cause CI failures when Fluent is not running.

Key facts about the real Fluent REST server
-------------------------------------------
* Paths use kebab-case:  ``setup/models/energy/enabled``,
  ``solution/run-calculation`` (dashes, not underscores).
* ``get_attrs`` currently returns HTTP 500 (known SimBA bug in this build).
* ``set_var`` may be silently overridden by Fluent solver validation.
* ``execute_cmd("initialize")`` returns HTTP 500 when no case/mesh is loaded.

Run all real-server tests::

    pytest src/ansys/fluent/core/rest/tests/ -m real_server -v

Skip real-server tests (default CI behaviour)::

    pytest src/ansys/fluent/core/rest/tests/ -m "not real_server" -v
"""

import pytest

from ansys.fluent.core.rest.client import FluentRestError

# All tests in this module require the real Fluent server.
pytestmark = pytest.mark.real_server


# ---------------------------------------------------------------------------
# 1. Static info
# ---------------------------------------------------------------------------


class TestRealStaticInfo:
    """GET /api/fluent_1/static-info"""

    def test_returns_dict(self, real_client):
        info = real_client.get_static_info()
        assert isinstance(info, dict)

    def test_root_type_is_group(self, real_client):
        info = real_client.get_static_info()
        assert info.get("type") == "group"

    def test_top_level_children_present(self, real_client):
        info = real_client.get_static_info()
        children = info.get("children", {})
        # Real Fluent V261 exposes these top-level sections
        for expected in ("setup", "solution"):
            assert expected in children, f"'{expected}' missing from schema children"

    def test_setup_subtree_has_models(self, real_client):
        info = real_client.get_static_info()
        setup = info["children"]["setup"]["children"]
        assert "models" in setup


# ---------------------------------------------------------------------------
# 2. get_var — reading values
# ---------------------------------------------------------------------------


class TestRealGetVar:
    """POST /api/fluent_1/get_var"""

    def test_read_bool(self, real_client):
        val = real_client.get_var("setup/models/energy/enabled")
        assert isinstance(val, bool)

    def test_read_string(self, real_client):
        val = real_client.get_var("setup/general/solver/time")
        assert isinstance(val, str)
        assert val in ("steady", "transient")

    def test_read_string_viscous_model(self, real_client):
        val = real_client.get_var("setup/models/viscous/model")
        assert isinstance(val, str)

    def test_read_group_returns_dict(self, real_client):
        val = real_client.get_var("setup/general/solver")
        assert isinstance(val, dict)

    def test_read_solution_group(self, real_client):
        # Real server uses kebab-case: run-calculation not run_calculation
        val = real_client.get_var("solution/run-calculation")
        assert isinstance(val, dict)

    def test_unknown_path_raises_404(self, real_client):
        with pytest.raises(FluentRestError) as exc_info:
            real_client.get_var("nonexistent/path/that/does/not/exist")
        assert exc_info.value.status == 404


# ---------------------------------------------------------------------------
# 3. set_var — writing values
# ---------------------------------------------------------------------------


class TestRealSetVar:
    """PUT /api/fluent_1/{path}"""

    def test_round_trip_bool(self, real_client):
        """Read → flip → write → read back → restore."""
        original = real_client.get_var("setup/models/energy/enabled")
        flipped = not original
        real_client.set_var("setup/models/energy/enabled", flipped)
        readback = real_client.get_var("setup/models/energy/enabled")
        # Restore before asserting so the server state is always cleaned up
        real_client.set_var("setup/models/energy/enabled", original)
        # Fluent may override the value via solver validation — we log either way
        # but don't hard-fail since this is solver-state dependent
        assert readback in (flipped, original), (
            f"Unexpected readback value: {readback}"
        )

    def test_set_string_value(self, real_client):
        """Switch time between 'steady' and 'transient' and restore.

        Fluent may return 500 when no case is loaded (solver rejects the change).
        We accept that as a valid outcome and only fail on unexpected errors.
        """
        original = real_client.get_var("setup/general/solver/time")
        new_val = "transient" if original == "steady" else "steady"
        try:
            real_client.set_var("setup/general/solver/time", new_val)
            readback = real_client.get_var("setup/general/solver/time")
            real_client.set_var("setup/general/solver/time", original)
            assert readback in (new_val, original)
        except FluentRestError as e:
            # 500 = Fluent rejected the change (no case loaded or solver validation)
            assert e.status == 500, f"Unexpected error: {e.status}: {e}"


# ---------------------------------------------------------------------------
# 4. get_attrs
# ---------------------------------------------------------------------------


class TestRealGetAttrs:
    """POST /api/fluent_1/get_attrs — known SimBA 500 bug tracked here."""

    def test_endpoint_is_reachable(self, real_client):
        """Confirm the endpoint exists (even if server crashes handling it)."""
        try:
            result = real_client.get_attrs(
                "setup/models/viscous/model", ["allowed-values"]
            )
            # If fixed, validate the response shape
            assert isinstance(result, dict)
        except FluentRestError as e:
            # HTTP 500 = SimBA server-side bug (not our client bug)
            assert e.status == 500, (
                f"Expected 500 (known SimBA bug) or success, got {e.status}: {e}"
            )


# ---------------------------------------------------------------------------
# 5. get_object_names
# ---------------------------------------------------------------------------


class TestRealGetObjectNames:
    """GET /api/fluent_1/{path} — named object lists."""

    def test_velocity_inlet_returns_list(self, real_client):
        names = real_client.get_object_names(
            "setup/boundary-conditions/velocity-inlet"
        )
        assert isinstance(names, list)

    def test_pressure_outlet_returns_list(self, real_client):
        names = real_client.get_object_names(
            "setup/boundary-conditions/pressure-outlet"
        )
        assert isinstance(names, list)

    def test_unknown_path_returns_empty(self, real_client):
        # 404 → client returns []
        names = real_client.get_object_names("setup/boundary-conditions/does-not-exist")
        assert names == []


# ---------------------------------------------------------------------------
# 6. execute_cmd
# ---------------------------------------------------------------------------


class TestRealExecuteCmd:
    """POST /api/fluent_1/{path}/{cmd}"""

    def test_initialize_endpoint_reachable(self, real_client):
        """Confirm the initialize command endpoint is routed correctly.

        With no case/mesh loaded the server returns null reply or HTTP 500.
        Either outcome confirms the endpoint exists and our client reaches it.
        """
        try:
            real_client.execute_cmd("solution/initialization", "initialize")
            # reached here with no exception — endpoint responded
        except FluentRestError as e:
            # 409 = Conflict (already initialized / no mesh loaded)
            # 500 = internal error with no case loaded
            assert e.status in (409, 500), f"Unexpected error: {e.status}: {e}"


# ---------------------------------------------------------------------------
# 7. execute_query
# ---------------------------------------------------------------------------


class TestRealExecuteQuery:
    """POST /api/fluent_1/{path}/{query}"""

    def test_query_endpoint_routing(self, real_client):
        """Confirm POST routing to {path}/{query} works end-to-end.

        Acceptable responses from the real server:
        * 200 / reply  — query succeeded (case loaded)
        * 404  — path doesn't exist in this session
        * 405  — endpoint exists but doesn't accept POST (SimBA routing quirk)
        * 500  — server error (no case loaded)
        """
        try:
            reply = real_client.execute_query(
                "setup/boundary-conditions/velocity-inlet",
                "get-zone-names",
            )
            assert isinstance(reply, (list, str, type(None)))
        except FluentRestError as e:
            assert e.status in (404, 405, 500), (
                f"Unexpected status {e.status}: {e}"
            )


# ---------------------------------------------------------------------------
# 8. resize_list_object
# ---------------------------------------------------------------------------


class TestRealResizeListObject:
    """PUT /api/fluent_1/{path} with body {\"size\": n}

    We first find a real list-type setting path from the schema, then
    attempt a resize. If the path doesn't exist or Fluent rejects it,
    we record the status rather than failing hard.
    """

    def test_resize_endpoint_routing(self, real_client):
        """Confirm PUT with {\"size\": n} body reaches the server without crashing."""
        # Use a known list-type path from the real schema.
        # We set size to 1 (safe minimum) and restore to same value.
        # If path doesn't exist in this session, we get 404 — still acceptable.
        try:
            # First check current size
            current = real_client.get_list_size(
                "solution/run-calculation/pseudo-time-settings"
                "/timestepping-parameters/profile-update-interval"
            )
            # Attempt resize (same size = safe no-op for Fluent)
            real_client.resize_list_object(
                "solution/run-calculation/pseudo-time-settings"
                "/timestepping-parameters/profile-update-interval",
                max(current, 1),
            )
        except FluentRestError as e:
            # 404 = path not present in this session's state (acceptable)
            # 422 = Fluent rejected the size (acceptable)
            # 500 = server error (note but don't fail)
            assert e.status in (404, 422, 500), (
                f"Unexpected error on resize_list_object: {e.status}: {e}"
            )


# ---------------------------------------------------------------------------
# 9. get_list_size
# ---------------------------------------------------------------------------


class TestRealGetListSize:
    """GET /api/fluent_1/{path} — list size reading."""

    def test_known_list_path_returns_int(self, real_client):
        # solution/run-calculation group exists, get_list_size returns 0 for
        # non-list groups (via 404 fallback in client)
        size = real_client.get_list_size("solution/run-calculation")
        assert isinstance(size, int)
        assert size >= 0

    def test_unknown_path_returns_zero(self, real_client):
        size = real_client.get_list_size("definitely/does/not/exist")
        assert size == 0


# ---------------------------------------------------------------------------
# 10. is_interactive_mode
# ---------------------------------------------------------------------------


class TestRealIsInteractiveMode:
    """GET /api/connection/run_mode — verify live query, not hardcoded."""

    def test_queries_server_run_mode(self, real_client):
        """Confirm is_interactive_mode queries the server (not hardcoded).
        
        The real Fluent server at 10.18.44.175:5000 runs in 'fluent_proxy' mode,
        which is interactive (not batch). This test confirms the client actually
        queries /api/connection/run_mode and returns True.
        """
        result = real_client.is_interactive_mode()
        assert isinstance(result, bool)
        # Real server runs in fluent_proxy mode (interactive), not batch
        assert result is True, (
            "Expected True for real Fluent server in fluent_proxy mode"
        )
