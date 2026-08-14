# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
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

from collections import UserList
import os
import warnings

from conftest import SKIP_INVESTIGATING
import pytest
from pytest import WarningsRecorder

from ansys.fluent.core import config
from ansys.fluent.core.examples import download_file
from ansys.fluent.core.exceptions import DeprecatedSettingWarning, PyFluentUserWarning
from ansys.fluent.core.session_http_solver import HttpSolver
from ansys.fluent.core.session.solver import Solver
from ansys.fluent.core.solver import VelocityInlets, Viscous
from ansys.fluent.core.solver.flobject import (
    InactiveObjectError,
    NamedObject,
    ReadOnlyActionError,
    _Alias,
    _InputFile,
    _OutputFile,
    to_python_name,
)
from ansys.fluent.core.utils.execution import timeout_loop
from ansys.fluent.core.utils.fluent_version import FluentVersion

# ============================================================================
# Helpers for transport-parametrized tests (gRPC vs REST)
# ============================================================================


def _is_rest(session_fixture_name: str) -> bool:
    """Check if session fixture is REST-based (contains 'rest' in name)."""
    return "rest" in session_fixture_name


# This run targets a live REST server when both env vars are configured (same
# check used by conftest.py's new_solver_session_rest fixture). Used below to
# decide, per test, which transport this run is actually exercising.
_REST_ACTIVE = bool(os.environ.get("FLUENT_REST_URL")) and bool(
    os.environ.get("FLUENT_REST_TOKEN")
)


@pytest.fixture(autouse=True)
def _skip_wrong_transport(request):
    """Skip a test when it doesn't match the transport active for this run.

    - If FLUENT_REST_URL/FLUENT_REST_TOKEN are set, this run targets a live
      REST server, so gRPC-only tests/params (which assume a local/launchable
      Fluent install) are skipped instead of erroring out trying to launch one.
    - Otherwise (default), this run targets local/launched Fluent via gRPC, so
      REST-only params are skipped (this mirrors, as a fast pre-launch check,
      what new_solver_session_rest already enforces via its own env-var check).

    Autouse fixtures run before explicitly-requested same-scope fixtures, so
    this executes before new_solver_session/new_solver_session_rest and
    prevents a wasted Fluent launch or REST connection attempt.
    """
    callspec = getattr(request.node, "callspec", None)
    session_fixture_name = (
        callspec.params.get("session_fixture_name") if callspec else None
    )
    if session_fixture_name is not None:
        is_rest_test = _is_rest(session_fixture_name)
    else:
        is_rest_test = any("rest" in name for name in request.fixturenames)

    if is_rest_test and not _REST_ACTIVE:
        pytest.skip(
            "REST server not configured for this run "
            "(FLUENT_REST_URL/FLUENT_REST_TOKEN not set); skipping REST test."
        )
    if not is_rest_test and _REST_ACTIVE:
        pytest.skip(
            "REST-only run active (FLUENT_REST_URL/FLUENT_REST_TOKEN set); "
            "skipping gRPC-only test."
        )


# ============================================================================
# Transport adapter infrastructure (abstract factory pattern)
# ============================================================================
from abc import ABC, abstractmethod


class SettingsTestAdapter(ABC):
    """Abstract adapter for transport-specific settings API operations.

    Isolates gRPC vs REST differences so test bodies remain uniform,
    delegating to concrete adapters for transport-specific details.
    """

    def __init__(self, solver):
        self.solver = solver

    @abstractmethod
    def create_named_object(self, path: str, name: str, properties=None) -> None:
        """Create a named object (e.g., iso_clip, surface)."""
        pass

    @abstractmethod
    def delete_named_object(self, path: str, name: str) -> None:
        """Delete a named object."""
        pass

    @abstractmethod
    def rename_named_object(self, collection_path: str, old: str, new: str) -> None:
        """Rename a named object."""
        pass

    @abstractmethod
    def create_contour(self, name: str):
        """Create a contour object; returns the contour object."""
        pass

    @abstractmethod
    def get_range_config_for_contour(self, base_dict: dict) -> dict:
        """Return transport-specific contour range config dict."""
        pass

    @abstractmethod
    def search_in_attrs_result(self, result, key: str) -> bool:
        """Check if key is found in get_attrs result (transport-specific shape)."""
        pass


class GrpcSettingsAdapter(SettingsTestAdapter):
    """Adapter for gRPC transport; uses settings API directly."""

    def create_named_object(self, path: str, name: str, properties=None) -> None:
        # For gRPC, navigate to the collection and direct assignment
        # path is like "results/surfaces/iso_clip" -> solver.settings.results.surfaces.iso_clip
        parts = path.split("/")
        obj = self.solver.settings
        for part in parts:
            obj = getattr(obj, part)
        obj[name] = properties if properties else {}

    def delete_named_object(self, path: str, name: str) -> None:
        # Navigate to collection and use del
        parts = path.split("/")
        obj = self.solver.settings
        for part in parts:
            obj = getattr(obj, part)
        del obj[name]

    def rename_named_object(self, collection_path: str, old: str, new: str) -> None:
        # Navigate to collection and call .rename()
        parts = collection_path.split("/")
        obj = self.solver.settings
        for part in parts:
            obj = getattr(obj, part)
        obj.rename(new=new, old=old)

    def create_contour(self, name: str):
        # gRPC: use .create() method on contour collection
        return self.solver.settings.results.graphics.contour.create(name)

    def get_range_config_for_contour(self, base_dict: dict) -> dict:
        # gRPC uses "range_option" (singular) with nested structure
        return {
            **base_dict,
            "range_option": {
                "option": "auto-range-off",
                "auto_range_off": {
                    "maximum": 400.0,
                    "minimum": 300,
                    "clip_to_range": False,
                },
            },
        }

    def search_in_attrs_result(self, result, key: str) -> bool:
        # gRPC: search recursively through nested attrs/group_children structure
        return _contains_key_or_name(result, key)


class RestSettingsAdapter(SettingsTestAdapter):
    """Adapter for REST transport; uses REST client methods."""

    def create_named_object(self, path: str, name: str, properties=None) -> None:
        # REST: use solver.create_named_object()
        self.solver.create_named_object(path, name, properties=properties)

    def delete_named_object(self, path: str, name: str) -> None:
        # REST: use solver.delete_named_object()
        self.solver.delete_named_object(path, name)

    def rename_named_object(self, collection_path: str, old: str, new: str) -> None:
        # REST: use solver.rename_named_object()
        self.solver.rename_named_object(collection_path, old, new)

    def create_contour(self, name: str):
        # REST: create via endpoint, then retrieve from settings
        self.solver.create_named_object("results/graphics/contour", name)
        return self.solver.settings.results.graphics.contour[name]

    def get_range_config_for_contour(self, base_dict: dict) -> dict:
        # REST uses "range_options" (plural) with flat structure
        return {
            **base_dict,
            "range_options": {
                "auto_range": False,
                "maximum": 400.0,
                "minimum": 300,
                "clip_to_range": False,
            },
        }

    def search_in_attrs_result(self, result, key: str) -> bool:
        # REST: use recursive _contains_key_or_name() search
        return _contains_key_or_name(result, key)


class SettingsTestAdapterFactory:
    """Factory to create the appropriate transport adapter."""

    @staticmethod
    def create(session_fixture_name: str, solver) -> SettingsTestAdapter:
        """Create adapter based on transport type.

        Parameters
        ----------
        session_fixture_name : str
            Parametrized fixture name (e.g., "new_solver_session" or "new_solver_session_rest")
        solver : Solver
            The solver session instance.

        Returns
        -------
        SettingsTestAdapter
            Concrete adapter for the transport used in this test.
        """
        if _is_rest(session_fixture_name):
            return RestSettingsAdapter(solver)
        else:
            return GrpcSettingsAdapter(solver)


def _contains_key_or_name(obj, key: str) -> bool:
    """Recursively search dicts/lists for a matching dict key or ``"name"`` entry.

    The REST server's exact JSON shape for some responses (e.g. recursive
    ``get_attrs``) is not documented/confirmed. Rather than assert a single
    guessed shape, search the whole structure for *key* - either as a dict
    key, or as the value of a ``"name"``/``"key"`` entry.
    """
    if isinstance(obj, dict):
        if key in obj:
            return True
        if obj.get("name") == key or obj.get("key") == key:
            return True
        return any(_contains_key_or_name(v, key) for v in obj.values())
    if isinstance(obj, list):
        return any(_contains_key_or_name(item, key) for item in obj)
    return False


@pytest.mark.nightly
def test_setup_models_viscous_model_settings(new_solver_session) -> None:
    solver_session = new_solver_session
    case_path = download_file("elbow_source_terms.cas.h5", "pyfluent/mixing_elbow")
    solver_session.file.read(
        file_name=case_path, file_type="case", lightweight_setup=True
    )

    viscous_model = solver_session.setup.models.viscous

    assert viscous_model.model() == "k-epsilon"
    assert "inviscid" in viscous_model.model.get_attr("allowed-values")
    viscous_model.model = "inviscid"

    assert viscous_model.model() == "inviscid"


def test_wildcard(new_solver_session):
    solver = new_solver_session
    case_path = download_file("elbow_source_terms.cas.h5", "pyfluent/mixing_elbow")
    solver.file.read(file_name=case_path, file_type="case", lightweight_setup=True)
    boundary_conditions = solver.setup.boundary_conditions
    if solver.get_fluent_version() >= FluentVersion.v251:
        assert boundary_conditions.velocity_inlet[
            "inl*"
        ].momentum.velocity_magnitude() == {
            "inlet2": {
                "momentum": {"velocity_magnitude": {"option": "value", "value": 15}}
            },
            "inlet1": {
                "momentum": {"velocity_magnitude": {"option": "value", "value": 5}}
            },
        }
        assert boundary_conditions.velocity_inlet[
            "inl*"
        ].momentum.velocity_magnitude.value() == {
            "inlet2": {"momentum": {"velocity_magnitude": {"value": 15}}},
            "inlet1": {"momentum": {"velocity_magnitude": {"value": 5}}},
        }
        boundary_conditions.velocity_inlet["inl*"].momentum.velocity_magnitude = 10
        assert boundary_conditions.velocity_inlet[
            "inl*"
        ].momentum.velocity_magnitude() == {
            "inlet2": {
                "momentum": {"velocity_magnitude": {"option": "value", "value": 10}}
            },
            "inlet1": {
                "momentum": {"velocity_magnitude": {"option": "value", "value": 10}}
            },
        }
        boundary_conditions.velocity_inlet = boundary_conditions.velocity_inlet[
            "inl*"
        ].momentum.velocity_magnitude()
        assert boundary_conditions.velocity_inlet[
            "inl*"
        ].momentum.velocity_magnitude() == {
            "inlet2": {
                "momentum": {"velocity_magnitude": {"option": "value", "value": 10}}
            },
            "inlet1": {
                "momentum": {"velocity_magnitude": {"option": "value", "value": 10}}
            },
        }
        state = boundary_conditions.velocity_inlet["inl*"]()
        assert state["inlet1"]["momentum"]["velocity_magnitude"]["value"] == 10
        assert state["inlet2"]["momentum"]["velocity_magnitude"]["value"] == 10
        boundary_conditions.velocity_inlet["inl*"] = {
            "momentum": {"velocity_magnitude": {"value": 15}}
        }
        state = boundary_conditions.velocity_inlet["inl*"]()
        assert state["inlet1"]["momentum"]["velocity_magnitude"]["value"] == 15
        assert state["inlet2"]["momentum"]["velocity_magnitude"]["value"] == 15
    else:
        assert boundary_conditions.velocity_inlet["inl*"].momentum.velocity() == {
            "inlet2": {"momentum": {"velocity": {"option": "value", "value": 15}}},
            "inlet1": {"momentum": {"velocity": {"option": "value", "value": 5}}},
        }
        assert boundary_conditions.velocity_inlet["inl*"].momentum.velocity.value() == {
            "inlet2": {"momentum": {"velocity": {"value": 15}}},
            "inlet1": {"momentum": {"velocity": {"value": 5}}},
        }
        boundary_conditions.velocity_inlet["inl*"].momentum.velocity = 10
        assert boundary_conditions.velocity_inlet["inl*"].momentum.velocity() == {
            "inlet2": {"momentum": {"velocity": {"option": "value", "value": 10}}},
            "inlet1": {"momentum": {"velocity": {"option": "value", "value": 10}}},
        }
        boundary_conditions.velocity_inlet = boundary_conditions.velocity_inlet[
            "inl*"
        ].momentum.velocity()
        assert boundary_conditions.velocity_inlet["inl*"].momentum.velocity() == {
            "inlet2": {"momentum": {"velocity": {"option": "value", "value": 10}}},
            "inlet1": {"momentum": {"velocity": {"option": "value", "value": 10}}},
        }
    cell_zone_conditions = solver.setup.cell_zone_conditions
    sources = cell_zone_conditions.fluid["*"].sources.terms
    sources_key = "sources"
    terms_key = "terms"
    assert sources["*mom*"]() == {
        "fluid": {
            sources_key: {
                terms_key: {
                    "x-momentum": [{"option": "value", "value": 1}],
                    "y-momentum": [{"option": "value", "value": 2}],
                    "z-momentum": [{"option": "value", "value": 3}],
                }
            }
        }
    }
    sources["*mom*"] = [{"option": "value", "value": 2}]
    assert sources["*mom*"]() == {
        "fluid": {
            sources_key: {
                terms_key: {
                    "x-momentum": [{"option": "value", "value": 2}],
                    "y-momentum": [{"option": "value", "value": 2}],
                    "z-momentum": [{"option": "value", "value": 2}],
                }
            }
        }
    }

    with pytest.raises(AttributeError):
        boundary_conditions.velocity_inlet["inl*"].moment


def test_wildcard_fnmatch(new_solver_session):
    solver = new_solver_session
    case_path = download_file("elbow_source_terms.cas.h5", "pyfluent/mixing_elbow")
    solver.file.read_case(file_name=case_path)

    solver.solution.initialization.hybrid_initialize()

    mesh = solver.results.graphics.mesh
    assert mesh.create("mesh-a").name() == "mesh-a"
    mesh.create("mesh-bc")
    if solver.get_fluent_version() >= FluentVersion.v251:
        assert mesh.create(name="mesh-2").name() == "mesh-2"
        assert mesh.create().name() == "mesh-3"
    else:
        assert mesh.create("mesh-2").name() == "mesh-2"
        assert mesh.create("mesh-3").name() == "mesh-3"

    assert sorted(mesh["mesh-*"]()) == sorted(
        ["mesh-1", "mesh-2", "mesh-3", "mesh-a", "mesh-bc"]
    )

    assert list(mesh["mesh-?c"]().keys()) == ["mesh-bc"]

    assert list(mesh["mesh-[2-5]"]().keys()) == ["mesh-2", "mesh-3"]

    assert sorted(mesh["mesh-[!2-5]"]()) == sorted(["mesh-1", "mesh-a"])


def test_wildcard_path_is_iterable(new_solver_session):
    solver = new_solver_session
    case_path = download_file("elbow_source_terms.cas.h5", "pyfluent/mixing_elbow")
    solver.file.read(file_name=case_path, file_type="case", lightweight_setup=True)

    velocity_inlet = solver.setup.boundary_conditions.velocity_inlet
    assert [x for x in velocity_inlet] == ["inlet2", "inlet1"]
    assert [x for x in velocity_inlet["*let*"]] == ["inlet2", "inlet1"]
    assert [x for x in velocity_inlet["*1*"]] == ["inlet1"]

    test_data = []
    for k, v in velocity_inlet.items():
        test_data.append((k, v))

    assert test_data[0][0] == "inlet2"
    assert test_data[0][1].path == r"setup/boundary-conditions/velocity-inlet/inlet2"
    assert test_data[1][0] == "inlet1"
    assert test_data[1][1].path == r"setup/boundary-conditions/velocity-inlet/inlet1"

    test_data = []
    for k, v in velocity_inlet["*let*"].items():
        test_data.append((k, v))

    assert test_data[0][0] == "inlet2"
    assert test_data[0][1].path == r"setup/boundary-conditions/velocity-inlet/inlet2"
    assert test_data[1][0] == "inlet1"
    assert test_data[1][1].path == r"setup/boundary-conditions/velocity-inlet/inlet1"


def test_api_upgrade(new_solver_session, capsys):
    solver = new_solver_session
    case_path = download_file("Static_Mixer_main.cas.h5", "pyfluent/static_mixer")
    solver.tui.file.read_case(case_path)
    timeout_loop(
        lambda: "<solver_session>.settings.file.read_case" in capsys.readouterr().out,
        timeout=5,
    )


# Custom aliases are not tested with 25.1 or later due to conflicts with the actual aliases
# defined in the settings API
@pytest.mark.fluent_version("==24.2")
def test_deprecated_settings_with_custom_aliases(new_solver_session):
    solver = new_solver_session
    case_path = download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    download_file("mixing_elbow.dat.h5", "pyfluent/mixing_elbow")
    solver.file._setattr("_child_aliases", {"rcd": ("read_case_data", "rcd")})
    with pytest.warns(DeprecatedSettingWarning):
        solver.file.rcd(file_name=case_path)

    solver.setup.boundary_conditions.velocity_inlet.child_object_type._child_aliases[
        "mom"
    ] = ("momentum", "mom")
    with pytest.warns(DeprecatedSettingWarning):
        solver.setup.boundary_conditions.velocity_inlet["hot-inlet"].mom.velocity = 20
    assert (
        solver.setup.boundary_conditions.velocity_inlet[
            "hot-inlet"
        ].momentum.velocity.value()
        == 20
    )
    with pytest.warns(DeprecatedSettingWarning):
        solver.setup.boundary_conditions.velocity_inlet["cold-inlet"].mom.velocity = 2
    assert (
        solver.setup.boundary_conditions.velocity_inlet[
            "cold-inlet"
        ].momentum.velocity.value()
        == 2
    )

    solver.setup.boundary_conditions.wall["wall-inlet"].thermal.thermal_bc = (
        "Temperature"
    )
    assert (
        len(
            solver.setup.boundary_conditions.wall[
                "wall-inlet"
            ].thermal.temperature._child_aliases
        )
        > 0
    )
    assert solver.setup.boundary_conditions.wall[
        "wall-inlet"
    ].thermal.temperature._child_aliases["constant"] == ("value", "constant")
    with pytest.warns(DeprecatedSettingWarning):
        solver.setup.boundary_conditions.wall[
            "wall-inlet"
        ].thermal.temperature.constant = 400

    assert (
        solver.setup.boundary_conditions.wall["wall-inlet"].thermal.temperature.value()
        == 400
    )
    assert (
        len(
            solver.setup.boundary_conditions.wall[
                "wall-inlet"
            ].thermal.temperature._child_aliases
        )
        > 0
    )
    assert isinstance(
        solver.setup.boundary_conditions.wall[
            "wall-inlet"
        ].thermal.temperature._child_alias_objs["constant"],
        _Alias,
    )
    with pytest.warns(DeprecatedSettingWarning):
        solver.setup.boundary_conditions.wall["wall-inlet"].thermal.t.value = 410

    assert (
        solver.setup.boundary_conditions.wall["wall-inlet"].thermal.temperature.value()
        == 410
    )

    solver.setup.boundary_conditions._setattr("_child_aliases", {"w": ("wall", "w")})
    with pytest.warns(DeprecatedSettingWarning):
        solver.setup.boundary_conditions.w["wall-inlet"].thermal.temperature.value = 420

    assert (
        solver.setup.boundary_conditions.wall["wall-inlet"].thermal.temperature.value()
        == 420
    )

    solver.setup._setattr("_child_aliases", {"bc": ("boundary_conditions", "bc")})
    with pytest.warns(DeprecatedSettingWarning):
        solver.setup.bc.wall["wall-inlet"].thermal.temperature.value = 430

    assert (
        solver.setup.boundary_conditions.wall["wall-inlet"].thermal.temperature.value()
        == 430
    )

    with pytest.warns(DeprecatedSettingWarning):
        solver.setup.boundary_conditions.wall[
            "wall-inlet"
        ].thermal.temperature.constant = 400

    assert (
        solver.setup.boundary_conditions.wall["wall-inlet"].thermal.temperature.value()
        == 400
    )

    solver.results._setattr("_child_aliases", {"gr": ("graphics", "gr")})
    with pytest.warns(DeprecatedSettingWarning):
        solver.results.gr.contour.create("c1")

    with pytest.warns(DeprecatedSettingWarning):
        solver.results.gr.contour["c1"].field = "pressure"

    assert solver.results.graphics.contour["c1"].field() == "pressure"

    with pytest.warns(DeprecatedSettingWarning):
        del solver.results.gr.contour["c1"]

    assert "c1" not in solver.results.graphics.contour

    solver.setup.boundary_conditions.velocity_inlet[
        "hot-inlet"
    ].momentum.velocity._child_aliases["hd"] = (
        "../../turbulence/hydraulic_diameter",
        "hd",
    )
    with pytest.warns(DeprecatedSettingWarning):
        solver.setup.boundary_conditions.velocity_inlet[
            "hot-inlet"
        ].momentum.velocity.hd = 10
    assert (
        solver.setup.boundary_conditions.velocity_inlet[
            "hot-inlet"
        ].turbulence.hydraulic_diameter()
        == 10
    )

    solver.setup.cell_zone_conditions.fluid["elbow-fluid"] = {"material": "air"}

    solver.setup.boundary_conditions.wall["wall-inlet"] = {
        "thermal": {"q_dot": {"value": 2000000000}, "wall_thickness": {"value": 0.002}}
    }


@pytest.mark.parametrize(
    "session_fixture_name",
    [
        pytest.param(
            "mixing_elbow_case_data_session", marks=pytest.mark.fluent_version(">=25.1")
        ),
        pytest.param(
            "mixing_elbow_case_data_session_rest",
            marks=[pytest.mark.rest_server, pytest.mark.fluent_version(">=27.1")],
        ),
    ],
)
def test_deprecated_settings_with_settings_api_aliases(session_fixture_name, request):
    """Test deprecated settings API aliases."""
    solver = request.getfixturevalue(session_fixture_name)
    adapter = SettingsTestAdapterFactory.create(session_fixture_name, solver)

    # Create iso_clip object
    adapter.create_named_object("results/surfaces/iso_clip", "clip-1")

    assert solver.settings.results.surfaces.iso_clip["clip-1"].range() == {
        "minimum": 0,
        "maximum": 0,
    }
    solver.settings.results.surfaces.iso_clip["clip-1"] = {
        "min": -0.0001,
        "max": 0.0001,
    }
    assert solver.settings.results.surfaces.iso_clip["clip-1"].range() == {
        "minimum": -0.0001,
        "maximum": 0.0001,
    }
    solver.settings.results.graphics.contour["temperature"] = {}

    # Build range config using adapter (encapsulates transport-specific shape)
    base_config = {
        "field": "temperature",
        "surfaces_list": "wall*",
        "color_map": {
            "visible": True,
            "size": 100,
            "color": "field-velocity",
            "log_scale": False,
            "format": "%0.1f",
            "user_skip": 9,
            "show_all": True,
            "position": 1,
            "font_name": "Helvetica",
            "font_automatic": True,
            "font_size": 0.032,
            "length": 0.54,
            "width": 6,
            "bground_transparent": True,
            "bground_color": "#CCD3E2",
            "title_elements": "Variable and Object Name",
        },
    }
    range_config = adapter.get_range_config_for_contour(base_config)

    solver.settings.results.graphics.contour["temperature"] = range_config
    assert solver.settings.results.graphics.contour["temperature"].range_options() == {
        "global_range": True,
        "auto_range": False,
        "clip_to_range": False,
        "minimum": 300,
        "maximum": 400.0,
    }


@pytest.mark.parametrize(
    "session_fixture_name",
    [
        "new_solver_session",
        pytest.param(
            "new_solver_session_rest",
            marks=[
                pytest.mark.rest_server,
                pytest.mark.fluent_version(">=27.1"),
                pytest.mark.xfail(
                    strict=False,
                    reason="REST server bug: string-list command args fail with HTTP 500",
                ),
            ],
        ),
    ],
)
def test_command_return_type(session_fixture_name, request):
    """Test command return types."""
    solver = request.getfixturevalue(session_fixture_name)
    adapter = SettingsTestAdapterFactory.create(session_fixture_name, solver)
    case_path = download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    download_file("mixing_elbow.dat.h5", "pyfluent/mixing_elbow")
    assert solver.file.read_case_data(file_name=case_path) is None
    adapter.create_named_object(
        "solution/report_definitions/surface",
        "surface-1",
        properties={"surface_names": ["cold-inlet"]},
    )
    ret = solver.solution.report_definitions.compute(report_defs=["surface-1"])
    assert ret is not None


@pytest.fixture
def warning_record():
    wrec = WarningsRecorder(_ispytest=True)
    with wrec:
        warnings.simplefilter("ignore", ResourceWarning)
        yield wrec


def test_generated_code_special_cases(new_solver_session):
    solver = new_solver_session
    icing_cls = solver.setup.boundary_conditions._child_classes[
        "velocity_inlet"
    ].child_object_type._child_classes["icing"]
    fensapice_drop_vrh_cls = icing_cls._child_classes["fensapice_drop_vrh"]
    fensapice_drop_vrh_1_cls = icing_cls._child_classes["fensapice_drop_vrh_1"]
    assert fensapice_drop_vrh_cls.fluent_name != fensapice_drop_vrh_1_cls.fluent_name
    assert to_python_name(fensapice_drop_vrh_cls.fluent_name) == to_python_name(
        fensapice_drop_vrh_1_cls.fluent_name
    )
    assert fensapice_drop_vrh_cls.__name__ != fensapice_drop_vrh_1_cls.__name__

    assert (
        solver.file.read_case.file_name.fluent_name
        == solver.file.write_case.file_name.fluent_name
    )
    assert (
        solver.file.read_case.file_name.__class__.__name__
        != solver.file.write_case.file_name.__class__.__name__
    )
    read_file_bases = solver.file.read_case.file_name.__class__.__bases__
    assert _InputFile in read_file_bases
    assert _OutputFile not in read_file_bases
    write_file_bases = solver.file.write_case.file_name.__class__.__bases__
    assert _InputFile not in write_file_bases
    assert _OutputFile in write_file_bases


@pytest.mark.fluent_version(">=25.1")
def test_child_alias_with_parent_path(mixing_elbow_settings_session):
    solver = mixing_elbow_settings_session

    # Following set_state should not throw InactiveObjectError
    solver.settings.setup.materials.fluid["air"] = {
        "density": {"option": "ideal-gas"},
        "specific_heat": {"value": 1006.43, "option": "constant"},
        "thermal_conductivity": {"value": 0.0242, "option": "constant"},
        "molecular_weight": {"value": 28.966, "option": "constant"},
    }
    assert solver.settings.setup.materials.fluid["air"].density.option() == "ideal-gas"
    assert solver.settings.setup.materials.fluid["air"].specific_heat.value() == 1006.43
    assert (
        solver.settings.setup.materials.fluid["air"].thermal_conductivity.value()
        == 0.0242
    )
    assert (
        solver.settings.setup.materials.fluid["air"].molecular_weight.value() == 28.966
    )

    solver.settings.solution.initialization.hybrid_initialize()
    if solver.get_fluent_version() >= FluentVersion.v261:
        solver.settings.setup.models.multiphase.model = "eulerian"
        solver.tui.define.models.multiphase.hybrid_models.ddpm("yes")
    assert (
        solver.settings.setup.models.discrete_phase.numerics.node_based_averaging.kernel._child_aliases
        == {
            "gaussian_factor": ("../gaussian_factor", "gaussian-factor"),
            "option": ("../kernel_type", "option"),
        }
    )
    solver.settings.setup.models.discrete_phase.numerics.node_based_averaging.enabled = (
        True
    )
    solver.settings.setup.models.discrete_phase.numerics.node_based_averaging.kernel_type = (
        "inverse-distance"
    )
    solver.settings.setup.models.discrete_phase.numerics.node_based_averaging.kernel = {
        "option": "gaussian",
        "gaussian_factor": 0.5,
    }
    assert (
        solver.settings.setup.models.discrete_phase.numerics.node_based_averaging.kernel_type()
        == "gaussian"
    )
    assert (
        solver.settings.setup.models.discrete_phase.numerics.node_based_averaging.gaussian_factor()
        == 0.5
    )
    with pytest.warns(
        DeprecatedSettingWarning,
        match=(
            "A newer syntax is available to perform the last operation:\n"
            "solver.settings.setup.models.discrete_phase.numerics.node_based_averaging.gaussian_factor = 0.6"
        ),
    ):
        solver.settings.setup.models.discrete_phase.numerics.node_based_averaging.kernel.gaussian_factor = (
            0.6
        )
    assert (
        solver.settings.setup.models.discrete_phase.numerics.node_based_averaging.gaussian_factor()
        == 0.6
    )


@pytest.mark.fluent_version(">=25.2,<=26.1")
def test_nested_alias_till_26r1(mixing_elbow_settings_session):
    solver = mixing_elbow_settings_session
    solver.settings.setup.models.viscous.model = "k-omega"
    solver.settings.setup.models.viscous.k_omega_model = "standard"
    # k_omega_options is alias of k_omega
    # kw_low_re_correction is alias of k_omega_low_re_correction
    # Testing all 4 combinations
    solver.settings.setup.models.viscous.k_omega.k_omega_low_re_correction = True
    with pytest.warns(
        DeprecatedSettingWarning,
        match=(
            "A newer syntax is available to perform the last operation:\n"
            "solver.settings.setup.models.viscous.k_omega.k_omega_low_re_correction = False"
        ),
    ):
        solver.settings.setup.models.viscous.k_omega_options.k_omega_low_re_correction = (
            False
        )
    with pytest.warns(
        DeprecatedSettingWarning,
        match=(
            "A newer syntax is available to perform the last operation:\n"
            "solver.settings.setup.models.viscous.k_omega.k_omega_low_re_correction = True"
        ),
    ):
        solver.settings.setup.models.viscous.k_omega_options.kw_low_re_correction = True
    with pytest.warns(
        DeprecatedSettingWarning,
        match=(
            "A newer syntax is available to perform the last operation:\n"
            "solver.settings.setup.models.viscous.k_omega.k_omega_low_re_correction = False"
        ),
    ):
        solver.settings.setup.models.viscous.k_omega.kw_low_re_correction = False


@pytest.mark.fluent_version(">=27.1")
def test_nested_alias(mixing_elbow_settings_session):
    solver = mixing_elbow_settings_session
    solver.settings.setup.models.viscous.model = "k-omega"
    solver.settings.setup.models.viscous.k_omega_model = "standard"
    # k_omega_options is alias of k_omega
    # kw_low_re_correction is alias of k_omega_low_re_correction
    # Testing all 4 combinations
    solver.settings.setup.models.viscous.k_omega.k_omega_low_re_correction.enabled = (
        True
    )
    with pytest.warns(
        DeprecatedSettingWarning,
        match=(
            "A newer syntax is available to perform the last operation:\n"
            "solver.settings.setup.models.turbulence.k_omega.k_omega_low_re_correction.enabled = False"
        ),
    ):
        solver.settings.setup.models.viscous.k_omega_options.k_omega_low_re_correction.enabled = (
            False
        )
    with pytest.warns(
        DeprecatedSettingWarning,
        match=(
            "A newer syntax is available to perform the last operation:\n"
            "solver.settings.setup.models.turbulence.k_omega.k_omega_low_re_correction.enabled = True"
        ),
    ):
        solver.settings.setup.models.viscous.k_omega_options.kw_low_re_correction.enabled = (
            True
        )
    with pytest.warns(
        DeprecatedSettingWarning,
        match=(
            "A newer syntax is available to perform the last operation:\n"
            "solver.settings.setup.models.turbulence.k_omega.k_omega_low_re_correction.enabled = False"
        ),
    ):
        solver.settings.setup.models.viscous.k_omega.kw_low_re_correction.enabled = (
            False
        )


@pytest.mark.parametrize(
    "session_fixture_name",
    [
        pytest.param("new_solver_session", marks=pytest.mark.fluent_version(">=25.1")),
        pytest.param(
            "new_solver_session_rest",
            marks=[pytest.mark.rest_server, pytest.mark.fluent_version(">=27.1")],
        ),
    ],
)
def test_commands_not_in_settings(session_fixture_name, request):
    """Verify that 'exit' and other top-level commands are not in settings.dir()."""
    solver = request.getfixturevalue(session_fixture_name)

    assert "exit" not in dir(solver.settings)
    with pytest.raises(AttributeError):
        solver.settings.exit()


@pytest.mark.fluent_version(">=25.1")
def test_deprecated_command_arguments(mixing_elbow_case_data_session):
    solver = mixing_elbow_case_data_session
    with pytest.warns(
        PyFluentUserWarning,
        match=(
            "Unknown keyword 'all_boundary_zones' for command '<session>.settings.results.report.fluxes.mass_flow'. "
            "It will be ignored."
        ),
    ):
        solver.settings.results.report.fluxes.mass_flow(
            all_boundary_zones=False, zones=["cold-inlet", "hot-inlet", "outlet"]
        )

    solver.settings.results.graphics.mesh.create("m1")
    solver.settings.results.graphics.mesh.make_a_copy(from_="m1", to="m2")
    with pytest.warns(DeprecatedSettingWarning) as record:
        solver.settings.results.graphics.mesh.copy(from_name="m1", new_name="m3")
    first, second = str(record[0].message).splitlines()[0:2]
    assert first == ("A newer syntax is available to perform the last operation:")
    # It seems that the order of the arguments is not consistent (from Fluent)
    assert second.startswith("solver.settings.results.graphics.mesh.make_a_copy(")
    assert "from_ = " in second
    assert "to = " in second
    assert set(solver.settings.results.graphics.mesh.get_object_names()) == {
        "m1",
        "m2",
        "m3",
    }


@pytest.mark.skip(reason=SKIP_INVESTIGATING)
# https://github.com/ansys/pyfluent/issues/4298
@pytest.mark.fluent_version(">=25.2")
def test_return_types_of_operations_on_named_objects(mixing_elbow_settings_session):
    solver = mixing_elbow_settings_session

    var1 = solver.settings.setup.materials.fluid.create("air-created")
    assert var1 == solver.settings.setup.materials.fluid["air-created"]
    assert var1.obj_name == "air-created"

    var2 = solver.settings.setup.materials.fluid.rename(
        old="air-created", new="air-renamed"
    )
    assert var2 is None

    var3 = solver.settings.setup.materials.fluid.make_a_copy(
        from_="air-renamed", to="air-copied"
    )
    assert var3 == solver.settings.setup.materials.fluid["air-copied"]
    assert var3.obj_name == "air-copied"


@pytest.mark.fluent_version(">=25.1")
def test_settings_with_deprecated_flag(mixing_elbow_settings_session):
    solver = mixing_elbow_settings_session
    solver.settings.solution.initialization.hybrid_initialize()
    graphics = solver.settings.results.graphics
    graphics.contour["contour-velocity"] = {
        "field": "velocity-magnitude",
        "surfaces_list": ["wall-elbow"],
    }
    # In the line below, "range_option" and "coloring" are deprecated.
    if solver.get_fluent_version() <= FluentVersion.v251:
        # From v252 'get_state' behaviour is to be corrected in Fluent.
        assert {"range_option", "range_options", "coloring", "colorings"}.issubset(
            set(graphics.contour["contour-velocity"]())
        )
    assert (
        graphics.contour["contour-velocity"].range_option.get_attr("deprecated-version")
        == "25.1"
    )
    assert (
        graphics.contour["contour-velocity"].coloring.get_attr("deprecated-version")
        == "25.1"
    )

    # User won't normally find deprecated objects in the settings API, so it is OK to leave them active.
    assert graphics.contour["contour-velocity"].range_options.is_active()

    # https://github.com/ansys/pyfluent/issues/3813
    # in 'get_state'
    # if solver.get_fluent_version() >= FluentVersion.v252:
    #     # From v252 'get_state' behaviour is to be corrected in Fluent.
    #     assert not {"range_option", "coloring"}.issubset(
    #         set(graphics.contour["contour-velocity"].get_state())
    #     )
    #     assert {"range_options", "colorings"}.issubset(
    #         set(graphics.contour["contour-velocity"].get_state())
    #     )
    # else:
    #     assert {"range_option", "range_options", "coloring", "colorings"}.issubset(
    #         set(graphics.contour["contour-velocity"].get_state())
    #     )

    # in 'child_names'
    # 'child_names', 'command_names' and 'query_names' will remain unchanged.
    assert {"range_option", "range_options", "coloring", "colorings"}.issubset(
        set(graphics.contour["contour-velocity"].child_names)
    )

    # in 'get_active_child_names'
    assert not {"range_option", "coloring"}.issubset(
        set(graphics.contour["contour-velocity"].get_active_child_names())
    )
    assert {"range_options", "colorings"}.issubset(
        set(graphics.contour["contour-velocity"].get_active_child_names())
    )

    # in 'dir'
    assert not {"range_option", "coloring"}.issubset(
        set(dir(graphics.contour["contour-velocity"]))
    )
    assert {"range_options", "colorings"}.issubset(
        set(dir(graphics.contour["contour-velocity"]))
    )

    # This should be True, as attribute is present, just not exposed.
    for item in ["range_option", "range_options", "coloring", "colorings"]:
        assert hasattr(graphics.contour["contour-velocity"], item)

    # Named-object
    solver.settings.solution.report_definitions.surface["report-def-1"] = {}
    solver.settings.solution.report_definitions.surface["report-def-1"].report_type = (
        "surface-area"
    )
    solver.settings.solution.report_definitions.surface[
        "report-def-1"
    ].surface_names = ["cold-inlet", "hot-inlet"]
    assert "create_output_parameter" not in dir(
        solver.settings.solution.report_definitions.surface["report-def-1"]
    )
    assert hasattr(
        solver.settings.solution.report_definitions.surface["report-def-1"],
        "create_output_parameter",
    )

    v1 = solver.settings.results.graphics.vector.create()
    assert v1.scale.scale_f() == 1.0
    v1.scale.scale_f = 2.0
    assert v1.scale.scale_f() == 2.0
    assert "scale" not in dir(v1)


@pytest.fixture
def use_runtime_python_classes(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(config, "use_runtime_python_classes", True)


def test_runtime_python_classes(
    use_runtime_python_classes, mixing_elbow_settings_session
):
    solver = mixing_elbow_settings_session
    solver.setup.materials.database.copy_by_name(type="fluid", name="water-liquid")
    solver.settings.setup.cell_zone_conditions.fluid["elbow-fluid"] = {
        "material": "water-liquid"
    }
    assert (
        solver.settings.setup.cell_zone_conditions.fluid[
            "elbow-fluid"
        ].general.material()
        == "water-liquid"
    )


@pytest.mark.fluent_version(">=26.1")
def test_setting_string_constants(mixing_elbow_settings_session):
    from ansys.fluent.core.solver import Viscous

    solver = mixing_elbow_settings_session
    viscous = Viscous(solver)

    # viscous.model.INVISCID is a string constant
    assert viscous.model.INVISCID == "inviscid"
    assert isinstance(viscous.model.INVISCID, str)
    with pytest.raises(AttributeError):
        viscous.model.INVISCID = "invalid"

    # Setting using string constants
    viscous.model = viscous.model.INVISCID
    assert viscous.model() == "inviscid"
    viscous.model = viscous.model.K_EPSILON
    assert viscous.model() == "k-epsilon"
    viscous.k_epsilon_model = viscous.k_epsilon_model.RNG
    assert viscous.k_epsilon_model.RNG.is_active() is True
    assert viscous.k_epsilon_model() == "rng"
    assert viscous.k_epsilon_model.EASM.is_active() is False

    with pytest.raises(ValueError):
        viscous.k_epsilon_model = viscous.k_epsilon_model.EASM


def test_named_object_commands(mixing_elbow_settings_session):
    from ansys.fluent.core.solver import VelocityInlets

    solver = mixing_elbow_settings_session
    inlets = VelocityInlets(solver)
    inlets.list()
    inlets.list_properties(object_name="hot-inlet")
    if solver.get_fluent_version() >= FluentVersion.v261:
        NamedObject.list(inlets)
        NamedObject.list_properties(inlets, object_name="hot-inlet")


# ============================================================================
# Phase 3: Parametrized CRUD test coverage (merged from REST file)
# ============================================================================


@pytest.mark.parametrize(
    "session_fixture_name",
    [
        "mixing_elbow_case_data_session",
        pytest.param(
            "mixing_elbow_case_data_session_rest",
            marks=[pytest.mark.rest_server, pytest.mark.fluent_version(">=27.1")],
        ),
    ],
)
def test_named_object_create_via_setitem(session_fixture_name, request):
    """Test creating a named object via direct assignment or REST endpoint."""
    solver = request.getfixturevalue(session_fixture_name)
    adapter = SettingsTestAdapterFactory.create(session_fixture_name, solver)
    # Create a new surface in report_definitions
    adapter.create_named_object(
        "solution/report_definitions/surface",
        "test_surface",
        properties={"surface_names": ["cold-inlet"]},
    )
    # Verify it exists
    assert (
        "test_surface"
        in solver.settings.solution.report_definitions.surface.get_object_names()
    )
    # Verify state round-trips
    state = solver.settings.solution.report_definitions.surface[
        "test_surface"
    ].get_state()
    assert state is not None


@pytest.mark.parametrize(
    "session_fixture_name",
    [
        "mixing_elbow_case_data_session",
        pytest.param(
            "mixing_elbow_case_data_session_rest",
            marks=[pytest.mark.rest_server, pytest.mark.fluent_version(">=27.1")],
        ),
    ],
)
def test_named_object_delete_via_delitem(session_fixture_name, request):
    """Test deleting a named object via direct deletion or REST endpoint."""
    solver = request.getfixturevalue(session_fixture_name)
    adapter = SettingsTestAdapterFactory.create(session_fixture_name, solver)
    # Create via endpoint then delete
    adapter.create_named_object(
        "solution/report_definitions/surface",
        "deleteme",
        properties={"surface_names": ["cold-inlet"]},
    )
    assert (
        "deleteme"
        in solver.settings.solution.report_definitions.surface.get_object_names()
    )
    # Delete via adapter
    adapter.delete_named_object("solution/report_definitions/surface", "deleteme")
    # Verify it's gone
    assert (
        "deleteme"
        not in solver.settings.solution.report_definitions.surface.get_object_names()
    )


@pytest.mark.parametrize(
    "session_fixture_name",
    [
        "mixing_elbow_settings_session",
        pytest.param(
            "mixing_elbow_settings_session_rest",
            marks=[pytest.mark.rest_server, pytest.mark.fluent_version(">=27.1")],
        ),
    ],
)
def test_named_object_overwrite_existing(session_fixture_name, request):
    """Test overwriting an existing named object's state.

    Uses ``cold-inlet``, an existing boundary condition from the case -
    velocity_inlet is a physical mesh zone and is not user-creatable.
    """
    solver = request.getfixturevalue(session_fixture_name)
    inlet = solver.settings.setup.boundary_conditions.velocity_inlet["cold-inlet"]
    # Set initial state via bracket assignment on the EXISTING object
    solver.settings.setup.boundary_conditions.velocity_inlet["cold-inlet"] = {
        "momentum": {"velocity": 1.0}
    }
    assert inlet.momentum.velocity.value() == 1.0
    # Overwrite with new values
    solver.settings.setup.boundary_conditions.velocity_inlet["cold-inlet"] = {
        "momentum": {"velocity": 2.0}
    }
    assert inlet.momentum.velocity.value() == 2.0


@pytest.mark.parametrize(
    "session_fixture_name",
    [
        "mixing_elbow_settings_session",
        pytest.param(
            "mixing_elbow_settings_session_rest",
            marks=[pytest.mark.rest_server, pytest.mark.fluent_version(">=27.1")],
        ),
    ],
)
def test_named_object_rename_command(session_fixture_name, request):
    """Test renaming a named object via command or REST endpoint.

    Uses ``cold-inlet`` (an existing boundary condition).
    """
    solver = request.getfixturevalue(session_fixture_name)
    adapter = SettingsTestAdapterFactory.create(session_fixture_name, solver)
    adapter.rename_named_object(
        "setup/boundary_conditions/velocity_inlet", "cold-inlet", "renamed_inlet"
    )
    obj_names = (
        solver.settings.setup.boundary_conditions.velocity_inlet.get_object_names()
    )
    assert "cold-inlet" not in obj_names
    assert "renamed_inlet" in obj_names


@pytest.mark.parametrize(
    "session_fixture_name",
    [
        "mixing_elbow_settings_session",
        pytest.param(
            "mixing_elbow_settings_session_rest",
            marks=[pytest.mark.rest_server, pytest.mark.fluent_version(">=27.1")],
        ),
    ],
)
def test_named_object_make_a_copy_command(session_fixture_name, request):
    """Test copying a named object via command or REST endpoint.

    Uses ``report_definitions.surface`` (a virtual, user-creatable collection).
    """
    solver = request.getfixturevalue(session_fixture_name)
    adapter = SettingsTestAdapterFactory.create(session_fixture_name, solver)
    # Create a source object to copy
    adapter.create_named_object(
        "solution/report_definitions/surface",
        "surface-1",
        properties={"surface_names": ["cold-inlet"]},
    )
    # Make a copy via command (same for both transports)
    solver.settings.solution.report_definitions.surface.make_a_copy(
        from_="surface-1", to="copy_of_surface_1"
    )
    obj_names = solver.settings.solution.report_definitions.surface.get_object_names()
    assert "copy_of_surface_1" in obj_names


@pytest.mark.fluent_version(">=26.1")
def test_migration_adapter_for_strings(mixing_elbow_settings_session):
    solver = mixing_elbow_settings_session
    solver.settings.setup.general.solver.time = "unsteady-2nd-order"
    solver.settings.setup.models.discrete_phase.general_settings.interaction.enabled = (
        True
    )

    solver.settings.setup.models.discrete_phase.general_settings.unsteady_tracking.enabled = (
        True
    )
    solver.settings.setup.models.discrete_phase.general_settings.unsteady_tracking.option = (
        "particle-time-step"
    )
    solver.settings.setup.models.discrete_phase.general_settings.unsteady_tracking.dpm_time_step_size = (
        0.0002
    )

    # Migration adapter is set on the 'create_particles_at' to accept boolean values as well besides string
    solver.settings.setup.models.discrete_phase.general_settings.unsteady_tracking.create_particles_at = (
        False
    )
    assert (
        solver.settings.setup.models.discrete_phase.general_settings.unsteady_tracking.create_particles_at()
        == "fluid-flow-time-step"
    )

    solver.settings.setup.models.discrete_phase.general_settings.unsteady_tracking.create_particles_at = (
        True
    )
    assert (
        solver.settings.setup.models.discrete_phase.general_settings.unsteady_tracking.create_particles_at()
        == "particle-time-step"
    )


def test_set_state_via_call(mixing_elbow_settings_session):
    solver = mixing_elbow_settings_session
    solver.settings.results.graphics.views.camera.position(xyz=[1.70, 1.14, 0.29])


@pytest.mark.parametrize(
    "session_fixture_name",
    [
        pytest.param(
            "mixing_elbow_case_session", marks=pytest.mark.fluent_version(">=26.1")
        ),
        pytest.param(
            "mixing_elbow_case_session_rest",
            marks=[pytest.mark.rest_server, pytest.mark.fluent_version(">=27.1")],
        ),
    ],
)
def test_read_only_command_execution(session_fixture_name, request):
    """Test read-only command execution."""
    solver = request.getfixturevalue(session_fixture_name)
    adapter = SettingsTestAdapterFactory.create(session_fixture_name, solver)
    # Create contour via adapter (transport-agnostic)
    contour = adapter.create_contour("test_contour")

    assert contour.display.is_active() is False
    with pytest.raises(InactiveObjectError):
        contour.display.is_read_only()
        # Same behaviour for attribute access of command arguments

    contour.surfaces_list = ["wall-elbow"]
    assert contour.display.is_active() is True
    assert contour.display.is_read_only() is True
    with pytest.raises(ReadOnlyActionError):
        contour.display()


@pytest.mark.parametrize(
    "session_fixture_name",
    [
        "mixing_elbow_settings_session",
        pytest.param(
            "mixing_elbow_settings_session_rest",
            marks=[pytest.mark.rest_server, pytest.mark.fluent_version(">=27.1")],
        ),
    ],
)
def test_copy_accepts_sequence_types(session_fixture_name, request):
    """Test that copy operations accept sequence types."""
    solver = request.getfixturevalue(session_fixture_name)
    hot_inlet = solver.settings.setup.boundary_conditions.velocity_inlet["hot-inlet"]
    cold_inlet = solver.settings.setup.boundary_conditions.velocity_inlet["cold-inlet"]
    hot_inlet.momentum.velocity = 1.0
    cold_inlet.momentum.velocity = 2.0

    assert cold_inlet.momentum.velocity.value() == 2.0

    seq = UserList(["cold-inlet"])
    solver.settings.setup.boundary_conditions.copy(from_="hot-inlet", to=seq)
    assert cold_inlet.momentum.velocity.value() == 1.0


@pytest.mark.parametrize(
    "session_fixture_name",
    [
        pytest.param(
            "mixing_elbow_case_session", marks=pytest.mark.fluent_version(">=26.1")
        ),
        pytest.param(
            "mixing_elbow_case_session_rest",
            marks=[pytest.mark.rest_server, pytest.mark.fluent_version(">=27.1")],
        ),
    ],
)
def test_action_behavior(session_fixture_name, request):
    """Test action behavior (commands with parameters)."""
    solver = request.getfixturevalue(session_fixture_name)
    adapter = SettingsTestAdapterFactory.create(session_fixture_name, solver)
    with pytest.raises(AttributeError, match="command/query object"):
        solver.settings.solution.run_calculation.iterate.get_state()
    assert isinstance(
        solver.settings.solution.run_calculation.iterate.iter_count(), int
    )
    solver.settings.solution.run_calculation.iterate.iter_count = 55
    assert solver.settings.solution.run_calculation.iterate.iter_count() == 55
    result = solver.settings.solution.run_calculation.iterate.get_attrs(
        ["active?"], recursive=True
    )
    # Use adapter for transport-specific result search
    assert adapter.search_in_attrs_result(
        result, "active?"
    ), f"'active?' not found in: {result!r}"
