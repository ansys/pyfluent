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

"""Integration tests: flobject.get_root(flproxy=FluentRestClient) builds a
working settings tree identical to the gRPC path.

These tests prove that:

1. ``get_root`` accepts a :class:`FluentRestClient` as *flproxy*.
2. The static-info schema returned by :class:`FluentRestMockServer` is
   understood by ``get_cls`` (the make-or-break validation).
3. Leaf values can be read and written through the settings tree.
4. Named-object children are accessible.
5. Commands can be executed.
6. The :class:`RestSolverSession` wrapper works end-to-end.
7. The :func:`launch_fluent_rest` convenience launcher works.
8. The :class:`SettingsProxy` protocol is satisfied at runtime.

Run with::

    pytest src/ansys/fluent/core/rest/tests/test_rest_integration.py -v
"""

import pytest

from ansys.fluent.core.rest.client import FluentRestClient
from ansys.fluent.core.rest.mock_server import FluentRestMockServer
from ansys.fluent.core.rest.protocol import SettingsProxy
from ansys.fluent.core.rest.rest_launcher import launch_fluent_rest
from ansys.fluent.core.rest.rest_session import RestSolverSession
from ansys.fluent.core.solver.flobject import get_root

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def mock_server():
    """Provide a fresh mock server per test for full isolation."""
    with FluentRestMockServer() as srv:
        yield srv


@pytest.fixture()
def rest_client(mock_server):
    """Return a FluentRestClient pointed at the per-test mock server."""
    return FluentRestClient(mock_server.base_url)


# ---------------------------------------------------------------------------
# 1. Protocol conformance
# ---------------------------------------------------------------------------


class TestProtocolConformance:
    """Verify that FluentRestClient satisfies SettingsProxy at runtime."""

    def test_client_is_settings_proxy(self, rest_client):
        """FluentRestClient must be a runtime instance of SettingsProxy."""
        assert isinstance(rest_client, SettingsProxy)


# ---------------------------------------------------------------------------
# 2. get_root builds a settings tree from static-info (the critical test)
# ---------------------------------------------------------------------------


class TestGetRootBuildsTrie:
    """The make-or-break test: flobject.get_root(flproxy=client) must work."""

    def test_get_root_returns_group(self, rest_client):
        """get_root should return a Group root with children."""
        root = get_root(rest_client)
        # The root must have a 'setup' child (from mock static-info).
        assert hasattr(root, "setup")

    def test_setup_subtree_exists(self, rest_client):
        """Verify the setup → models → energy path was built."""
        root = get_root(rest_client)
        assert hasattr(root.setup, "models")
        assert hasattr(root.setup.models, "energy")
        assert hasattr(root.setup.models.energy, "enabled")

    def test_solution_subtree_exists(self, rest_client):
        """Verify the solution → controls → under_relaxation path."""
        root = get_root(rest_client)
        assert hasattr(root.solution, "controls")
        assert hasattr(root.solution.controls, "under_relaxation")

    def test_named_object_subtree_exists(self, rest_client):
        """Verify named-object nodes (velocity_inlet) were built."""
        root = get_root(rest_client)
        assert hasattr(root.setup.boundary_conditions, "velocity_inlet")


# ---------------------------------------------------------------------------
# 3. Leaf value read / write through the tree
# ---------------------------------------------------------------------------


class TestLeafReadWrite:
    """Read and write leaf values via the settings tree over REST."""

    def test_read_boolean(self, rest_client):
        """Read a boolean leaf (energy/enabled)."""
        root = get_root(rest_client)
        assert root.setup.models.energy.enabled() is True

    def test_write_boolean(self, rest_client):
        """Write a boolean leaf and read it back."""
        root = get_root(rest_client)
        root.setup.models.energy.enabled.set_state(False)
        assert root.setup.models.energy.enabled() is False

    def test_read_string(self, rest_client):
        """Read a string leaf (viscous/model)."""
        root = get_root(rest_client)
        assert root.setup.models.viscous.model() == "k-epsilon"

    def test_write_string(self, rest_client):
        """Write a string leaf and verify round-trip."""
        root = get_root(rest_client)
        root.setup.models.viscous.model.set_state("laminar")
        assert root.setup.models.viscous.model() == "laminar"

    def test_read_real(self, rest_client):
        """Read a real-valued leaf (under_relaxation/pressure)."""
        root = get_root(rest_client)
        assert root.solution.controls.under_relaxation.pressure() == pytest.approx(0.3)

    def test_write_real(self, rest_client):
        """Write a real-valued leaf and verify round-trip."""
        root = get_root(rest_client)
        root.solution.controls.under_relaxation.pressure.set_state(0.5)
        assert root.solution.controls.under_relaxation.pressure() == pytest.approx(0.5)

    def test_read_integer(self, rest_client):
        """Read an integer leaf (run_calculation/iter_count)."""
        root = get_root(rest_client)
        assert root.solution.run_calculation.iter_count() == 100

    def test_write_integer(self, rest_client):
        """Write an integer leaf and verify round-trip."""
        root = get_root(rest_client)
        root.solution.run_calculation.iter_count.set_state(200)
        assert root.solution.run_calculation.iter_count() == 200


# ---------------------------------------------------------------------------
# 4. Group-level get/set
# ---------------------------------------------------------------------------


class TestGroupReadWrite:
    """Read and write group values (dict) via the settings tree."""

    def test_read_group(self, rest_client):
        """Read a group node as a dict."""
        root = get_root(rest_client)
        solver_dict = root.setup.general.solver()
        assert isinstance(solver_dict, dict)
        assert solver_dict["time"] == "steady"
        assert solver_dict["velocity_formulation"] == "absolute"

    def test_write_group(self, rest_client):
        """Write a group node via dict and verify round-trip."""
        root = get_root(rest_client)
        root.setup.general.solver.set_state(
            {"time": "transient", "velocity_formulation": "relative"}
        )
        assert root.setup.general.solver.time() == "transient"
        assert root.setup.general.solver.velocity_formulation() == "relative"


# ---------------------------------------------------------------------------
# 5. Named-object access
# ---------------------------------------------------------------------------


class TestNamedObjects:
    """Access named-object children through the settings tree."""

    def test_get_object_names(self, rest_client):
        """get_object_names should list 'inlet' under velocity_inlet."""
        root = get_root(rest_client)
        names = root.setup.boundary_conditions.velocity_inlet.get_object_names()
        assert "inlet" in names

    def test_access_named_child(self, rest_client):
        """Access a named child's nested value."""
        root = get_root(rest_client)
        vi = root.setup.boundary_conditions.velocity_inlet
        inlet = vi["inlet"]
        # The inlet should have the momentum subtree.
        assert hasattr(inlet, "momentum")


# ---------------------------------------------------------------------------
# 6. Command execution
# ---------------------------------------------------------------------------


class TestCommandExecution:
    """Execute commands through the settings tree."""

    def test_execute_initialize_command(self, rest_client, monkeypatch):
        """The initialization/initialize command should execute via REST."""
        # Force runtime class generation so flobject builds classes from
        # the mock server's static-info (which includes return-type for
        # the initialize command).  Without this, the pre-generated
        # settings_261 module is loaded and the command has no return_type.
        from ansys.fluent.core.module_config import config

        monkeypatch.setattr(config, "use_runtime_python_classes", True)

        root = get_root(rest_client, version="261")
        # The static-info registers 'initialize' as a command under
        # solution/initialization.
        result = root.solution.initialization.initialize()
        assert result == "Initialization complete"


# ---------------------------------------------------------------------------
# 7. RestSolverSession end-to-end
# ---------------------------------------------------------------------------


class TestRestSolverSession:
    """RestSolverSession wires everything together."""

    def test_session_has_settings(self, mock_server):
        """RestSolverSession.settings should be a populated root."""
        session = RestSolverSession(mock_server.base_url)
        assert hasattr(session.settings, "setup")
        assert hasattr(session.settings, "solution")

    def test_session_read_leaf(self, mock_server):
        """Read a leaf through the session."""
        session = RestSolverSession(mock_server.base_url)
        assert session.settings.setup.models.energy.enabled() is True

    def test_session_write_leaf(self, mock_server):
        """Write a leaf through the session and read back."""
        session = RestSolverSession(mock_server.base_url)
        session.settings.setup.models.energy.enabled.set_state(False)
        assert session.settings.setup.models.energy.enabled() is False

    def test_session_client_property(self, mock_server):
        """The client property should return the underlying FluentRestClient."""
        session = RestSolverSession(mock_server.base_url)
        assert isinstance(session.client, FluentRestClient)


# ---------------------------------------------------------------------------
# 8. launch_fluent_rest convenience launcher
# ---------------------------------------------------------------------------


class TestLaunchFluentRest:
    """launch_fluent_rest builds a RestSolverSession from host + port."""

    def test_launch_returns_session(self, mock_server):
        """launch_fluent_rest should return a RestSolverSession."""
        session = launch_fluent_rest("127.0.0.1", mock_server.port)
        assert isinstance(session, RestSolverSession)

    def test_launch_settings_work(self, mock_server):
        """Settings tree from launched session should be functional."""
        session = launch_fluent_rest("127.0.0.1", mock_server.port)
        assert session.settings.setup.models.energy.enabled() is True


# ---------------------------------------------------------------------------
# 9. Test isolation (deep-copy per test)
# ---------------------------------------------------------------------------


class TestIsolation:
    """Each mock server fixture gets a deep copy — mutations don't leak."""

    def test_mutation_does_not_leak_a(self, rest_client):
        """Mutate energy/enabled and verify it took effect."""
        root = get_root(rest_client)
        root.setup.models.energy.enabled.set_state(False)
        assert root.setup.models.energy.enabled() is False

    def test_mutation_does_not_leak_b(self, rest_client):
        """In a fresh fixture, energy/enabled should still be True."""
        root = get_root(rest_client)
        assert root.setup.models.energy.enabled() is True
