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

"""CaseSnapshot between live Fluent solver sessions."""

from pathlib import Path
import warnings

import pytest

import ansys.fluent.core as pyfluent
from ansys.fluent.core.examples import download_file

# A Scheme variable saved in case files, which the settings API does not expose.
_MARKER = "pyfluent/case-snapshot-marker"


def _elbow_case() -> str:
    return download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")


def _set_marker(solver, value: int) -> None:
    solver.scheme.eval(f"(rp-var-define '{_MARKER} 0 'integer #f)")
    solver.scheme.eval(f"(rpsetvar '{_MARKER} {value})")


def _marker(solver) -> int:
    return solver.scheme.eval(f"(rpgetvar '{_MARKER})")


def _viscous_model(solver) -> str:
    return solver.settings.setup.models.viscous.model()


def _outlet_area(solver) -> float:
    return solver.fields.reduction.area(locations=["outlet"])


def test_settings_outside_the_settings_api_are_applied_to_several_sessions(
    new_solver_session, new_solver_session_wo_exit
):
    source, target = new_solver_session, new_solver_session_wo_exit
    try:
        source.settings.file.read_case(file_name=_elbow_case())
        source.settings.setup.models.viscous.model = "laminar"
        _set_marker(source, 42)
        snapshot = pyfluent.CaseSnapshot.from_session(source)
        source.settings.setup.models.viscous.model = "k-epsilon"
        _set_marker(source, 7)

        # Applying to the source session too brings it back to the captured state.
        snapshot.apply_to(target, source)

        for solver in (target, source):
            assert _viscous_model(solver) == "laminar"
            assert _marker(solver) == 42
    finally:
        target.exit()


def test_include_mesh_false_keeps_the_mesh_of_the_session(
    new_solver_session, new_solver_session_wo_exit
):
    source, target = new_solver_session, new_solver_session_wo_exit
    try:
        for solver in (source, target):
            solver.settings.file.read_case(file_name=_elbow_case())
        if "replace" not in target.settings.mesh.command_names:
            pytest.skip("This Fluent version cannot replace a mesh.")
        # A turbulence model: file.replace_mesh crashes Fluent 2027 R1 with one.
        source.settings.setup.models.viscous.model = "k-epsilon"
        target.settings.mesh.scale(x_scale=2, y_scale=2, z_scale=2)
        scaled_area = _outlet_area(target)

        pyfluent.CaseSnapshot.from_session(source).apply_to(target, include_mesh=False)

        assert _viscous_model(target) == "k-epsilon"
        assert _outlet_area(target) == pytest.approx(scaled_area)
        assert _outlet_area(source) == pytest.approx(scaled_area / 4)
    finally:
        target.exit()


def test_a_snapshot_of_a_case_file_can_be_saved(new_solver_session, tmp_path):
    solver = new_solver_session
    file = Path(_elbow_case())
    if not file.is_absolute():
        # Container sessions get the name of a file in the mounted folder.
        file = Path(pyfluent.config.examples_path) / file
    snapshot = pyfluent.CaseSnapshot.from_file(file)

    snapshot.apply_to(solver)
    saved = snapshot.save(tmp_path / "elbow_copy.cas.h5")

    assert "cold-inlet" in solver.settings.setup.boundary_conditions.velocity_inlet
    assert saved.read_bytes() == file.read_bytes()


@pytest.mark.standalone
def test_applying_to_a_resilient_session_can_be_rolled_back(
    new_solver_session, new_solver_session_wo_exit, tmp_path
):
    from ansys.fluent.core.resilient import (
        CheckpointConfig,
        PoolConfig,
        ResilientConfig,
        ResilientWarning,
        _enable_on_new_session,
    )

    source, target = new_solver_session, new_solver_session_wo_exit
    try:
        # As resilient_mode=True does for a session it launches, with a standby
        # that is kept up to date.
        _enable_on_new_session(
            target,
            ResilientConfig(
                checkpoint=CheckpointConfig(directory=tmp_path),
                pool=PoolConfig(size=2),
            ),
            launched=True,
        )
        (standby,) = target.resilient.pool.standbys
        for solver in (source, target):
            solver.settings.file.read_case(file_name=_elbow_case())
        source.settings.setup.models.viscous.model = "laminar"
        snapshot = pyfluent.CaseSnapshot.from_session(source)

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            snapshot.apply_to(target)
            assert _viscous_model(target) == "laminar"
            assert target.resilient.checkpoints[-1].name == "case-snapshot"
            target.resilient.rollback("auto-read_case")
            assert _viscous_model(target) == "k-omega"
            assert target.resilient.wait_for_standbys(timeout=300)
            assert _viscous_model(standby) == "k-omega"

            # The standby also reads the temporary case files, before they are
            # deleted.
            snapshot.apply_to(target, include_mesh=False)
            assert target.resilient.wait_for_standbys(timeout=300)
        assert _viscous_model(standby) == "laminar"
        assert not [w for w in caught if issubclass(w.category, ResilientWarning)]
    finally:
        target.exit()
