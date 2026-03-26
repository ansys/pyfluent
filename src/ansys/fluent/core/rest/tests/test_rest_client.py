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

"""Tests for the REST settings client and mock server (Step 1 exploration).

All REST transport components live under
``src/ansys/fluent/core/rest/``.  These tests run entirely in-process
with no Fluent instance required.

Run with::

    pytest src/ansys/fluent/core/rest/tests/ -v
"""

# pylint: disable=missing-class-docstring,missing-function-docstring

import pytest

from ansys.fluent.core.rest import FluentRestClient, FluentRestMockServer
from ansys.fluent.core.rest.client import FluentRestError

# ---------------------------------------------------------------------------
# FluentRestMockServer tests
# ---------------------------------------------------------------------------


class TestMockServer:
    def test_server_starts_and_stops(self):
        """Server can be started, queried, and stopped cleanly."""
        srv = FluentRestMockServer()
        srv.start()
        assert srv.port > 0
        assert srv.base_url.startswith("http://127.0.0.1:")
        srv.stop()
        assert srv._httpd is None

    def test_context_manager(self):
        """Server supports the context-manager protocol."""
        with FluentRestMockServer() as srv:
            assert srv.port > 0
        assert srv._httpd is None

    def test_start_twice_raises(self):
        with FluentRestMockServer() as srv:
            with pytest.raises(RuntimeError, match="already running"):
                srv.start()

    def test_each_instance_has_independent_store(self):
        """Two server instances do not share state."""
        with FluentRestMockServer() as srv1, FluentRestMockServer() as srv2:
            c1 = FluentRestClient(srv1.base_url)
            c2 = FluentRestClient(srv2.base_url)
            c1.set_var("setup/models/energy/enabled", False)
            # srv2 should still have the default True
            assert c2.get_var("setup/models/energy/enabled") is True


# ---------------------------------------------------------------------------
# get_static_info
# ---------------------------------------------------------------------------


class TestGetStaticInfo:
    def test_returns_dict(self, rest_client):
        info = rest_client.get_static_info()
        assert isinstance(info, dict)
        assert info["type"] == "group"

    def test_top_level_children(self, rest_client):
        info = rest_client.get_static_info()
        assert "setup" in info["children"]
        assert "solution" in info["children"]

    def test_nested_energy_node(self, rest_client):
        info = rest_client.get_static_info()
        energy = info["children"]["setup"]["children"]["models"]["children"]["energy"]
        assert energy["children"]["enabled"]["type"] == "boolean"


# ---------------------------------------------------------------------------
# get_var / set_var
# ---------------------------------------------------------------------------


class TestGetSetVar:
    def test_get_existing_bool(self, rest_client):
        assert rest_client.get_var("setup/models/energy/enabled") is True

    def test_get_existing_string(self, rest_client):
        assert rest_client.get_var("setup/general/solver/time") == "steady"

    def test_get_existing_int(self, rest_client):
        assert rest_client.get_var("solution/run_calculation/iter_count") == 100

    def test_get_existing_float(self, rest_client):
        val = rest_client.get_var(
            "setup/boundary_conditions/velocity_inlet/inlet/momentum/velocity_magnitude/value"
        )
        assert val == pytest.approx(1.0)

    def test_get_unknown_path_raises(self, rest_client):
        with pytest.raises(FluentRestError) as exc_info:
            rest_client.get_var("nonexistent/path")
        assert exc_info.value.status == 404

    def test_set_then_get_bool(self, rest_client):
        rest_client.set_var("setup/models/energy/enabled", False)
        assert rest_client.get_var("setup/models/energy/enabled") is False
        # Restore
        rest_client.set_var("setup/models/energy/enabled", True)

    def test_set_then_get_string(self, rest_client):
        rest_client.set_var("setup/general/solver/time", "transient")
        assert rest_client.get_var("setup/general/solver/time") == "transient"
        rest_client.set_var("setup/general/solver/time", "steady")

    def test_set_then_get_float(self, rest_client):
        rest_client.set_var("solution/controls/under_relaxation/pressure", 0.5)
        assert rest_client.get_var(
            "solution/controls/under_relaxation/pressure"
        ) == pytest.approx(0.5)
        rest_client.set_var("solution/controls/under_relaxation/pressure", 0.3)

    def test_set_creates_new_path(self, rest_client):
        """set_var should accept new paths (no pre-population required)."""
        rest_client.set_var("setup/new/custom/setting", 42)
        assert rest_client.get_var("setup/new/custom/setting") == 42

    def test_set_dict_value(self, rest_client):
        rest_client.set_var("setup/new/dict/setting", {"key": "val"})
        assert rest_client.get_var("setup/new/dict/setting") == {"key": "val"}

    def test_set_list_value(self, rest_client):
        rest_client.set_var("setup/new/list/setting", [1, 2, 3])
        assert rest_client.get_var("setup/new/list/setting") == [1, 2, 3]


# ---------------------------------------------------------------------------
# get_attrs
# ---------------------------------------------------------------------------


class TestGetAttrs:
    def test_known_path_returns_allowed_values(self, rest_client):
        result = rest_client.get_attrs(
            "setup/models/viscous/model", ["allowed-values", "active?"]
        )
        attrs = result["attrs"]
        assert "allowed-values" in attrs
        assert "k-epsilon" in attrs["allowed-values"]

    def test_unknown_path_returns_empty_attrs(self, rest_client):
        result = rest_client.get_attrs(
            "setup/models/viscous/non_existing", ["allowed-values"]
        )
        assert result["attrs"] == {}

    def test_recursive_flag_returns_attrs_key(self, rest_client):
        result = rest_client.get_attrs(
            "setup/models/energy/enabled", ["active?"], recursive=True
        )
        assert "attrs" in result


# ---------------------------------------------------------------------------
# get_object_names / create / delete / rename
# ---------------------------------------------------------------------------


class TestNamedObjects:
    def test_get_existing_object_names(self, rest_client):
        names = rest_client.get_object_names("setup/boundary_conditions/velocity_inlet")
        assert "inlet" in names

    def test_get_names_for_unknown_path_returns_empty(self, rest_client):
        names = rest_client.get_object_names("setup/boundary_conditions/wall")
        assert names == []

    def test_create_object(self, rest_client):
        rest_client.create("setup/boundary_conditions/wall", "wall-1")
        names = rest_client.get_object_names("setup/boundary_conditions/wall")
        assert "wall-1" in names

    def test_create_duplicate_is_idempotent(self, rest_client):
        rest_client.create("setup/boundary_conditions/wall", "wall-1")
        rest_client.create("setup/boundary_conditions/wall", "wall-1")
        names = rest_client.get_object_names("setup/boundary_conditions/wall")
        assert names.count("wall-1") == 1

    def test_delete_object(self, rest_client):
        rest_client.create("setup/boundary_conditions/wall", "wall-to-delete")
        rest_client.delete("setup/boundary_conditions/wall", "wall-to-delete")
        names = rest_client.get_object_names("setup/boundary_conditions/wall")
        assert "wall-to-delete" not in names

    def test_delete_nonexistent_raises(self, rest_client):
        with pytest.raises(FluentRestError) as exc_info:
            rest_client.delete("setup/boundary_conditions/wall", "ghost")
        assert exc_info.value.status == 404

    def test_rename_object(self, rest_client):
        rest_client.create("setup/boundary_conditions/wall", "old-name")
        rest_client.rename(
            "setup/boundary_conditions/wall", new="new-name", old="old-name"
        )
        names = rest_client.get_object_names("setup/boundary_conditions/wall")
        assert "new-name" in names
        assert "old-name" not in names

    def test_rename_nonexistent_raises(self, rest_client):
        with pytest.raises(FluentRestError) as exc_info:
            rest_client.rename(
                "setup/boundary_conditions/wall", new="x", old="does-not-exist"
            )
        assert exc_info.value.status == 404


# ---------------------------------------------------------------------------
# get_list_size
# ---------------------------------------------------------------------------


class TestListSize:
    def test_known_path(self, rest_client):
        size = rest_client.get_list_size(
            "solution/run_calculation/pseudo_time_settings"
            "/timestepping_parameters/profile_update_interval"
        )
        assert size == 1

    def test_unknown_path_returns_zero(self, rest_client):
        assert rest_client.get_list_size("solution/run_calculation/unknown_list") == 0


# ---------------------------------------------------------------------------
# execute_cmd
# ---------------------------------------------------------------------------


class TestExecuteCmd:
    def test_registered_command(self, rest_client):
        reply = rest_client.execute_cmd("solution/initialization", "initialize")
        assert reply == "Initialization complete"

    def test_unregistered_command_returns_generic_reply(self, rest_client):
        reply = rest_client.execute_cmd("some/path", "do_something", x=1)
        assert "do_something" in reply
        assert "some/path" in reply


# ---------------------------------------------------------------------------
# execute_query
# ---------------------------------------------------------------------------


class TestExecuteQuery:
    def test_registered_query(self, rest_client):
        reply = rest_client.execute_query(
            "setup/boundary_conditions/velocity_inlet", "get_zone_names"
        )
        assert isinstance(reply, list)
        assert "inlet" in reply

    def test_unregistered_query_returns_generic_reply(self, rest_client):
        reply = rest_client.execute_query("some/path", "info_query")
        assert "info_query" in reply


# ---------------------------------------------------------------------------
# Helper methods (no server round-trip)
# ---------------------------------------------------------------------------


class TestHelpers:
    def test_is_interactive_mode_returns_false(self, rest_client):
        assert rest_client.is_interactive_mode() is False

    @pytest.mark.parametrize(
        "name, expected",
        [
            ("*", True),
            ("inlet_*", True),
            ("?nlet", True),
            ("[abc]inlet", True),
            ("plain-name", False),
            ("inlet", False),
        ],
    )
    def test_has_wildcard(self, rest_client, name, expected):
        assert rest_client.has_wildcard(name) is expected


# ---------------------------------------------------------------------------
# FluentRestError
# ---------------------------------------------------------------------------


class TestFluentRestError:
    def test_str_representation(self):
        err = FluentRestError(404, "Not found")
        assert "404" in str(err)
        assert "Not found" in str(err)

    def test_status_attribute(self):
        err = FluentRestError(500, "Server error")
        assert err.status == 500
