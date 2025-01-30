# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
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

import pytest


@pytest.mark.fluent_version(">=25.1")
def test_systemcoupling_mixing_elbow_settings_apis(mixing_elbow_case_data_session):
    """Test System Coupling related settings APIs"""
    solver = mixing_elbow_case_data_session
    # enable the feature flag to be able to make the queries
    solver.scheme_eval.scheme_eval("(enable-feature 'sc/participant-info)")
    elbow_fluid = "elbow-fluid"
    region_names = solver.settings.setup.models.system_coupling.get_all_regions()
    assert elbow_fluid in region_names
    # elbow fluid must be a volume
    assert (
        solver.settings.setup.models.system_coupling.get_topology(
            region_name=elbow_fluid
        )
        == "Volume"
    )


def _test_systemcoupling_mixing_elbow_settings_common(mixing_elbow_case_data_session):
    solver = mixing_elbow_case_data_session
    # check participant type, analysis type, regions, and variables
    assert solver.system_coupling.participant_type == "FLUENT"
    assert solver.system_coupling.get_analysis_type() == "Steady"
    regions = solver.system_coupling.get_regions()
    variables = solver.system_coupling.get_variables()
    # [wall-inlet, wall-elbow, elbow-fluid, hot-inlet, cold-inlet, outlet]
    assert len(regions) >= 6
    # [force, temp, htc, hflow, nwt, hrate, e-cond, lorentz-force]
    assert len(variables) >= 8


@pytest.mark.fluent_version(">=25.1")
def test_systemcoupling_mixing_elbow_settings(mixing_elbow_case_data_session):
    """Very superficial test of System Coupling related settings."""
    _test_systemcoupling_mixing_elbow_settings_common(mixing_elbow_case_data_session)


@pytest.mark.fluent_version(">=24.1,<25.1")
def test_systemcoupling_mixing_elbow_settings_legacy(mixing_elbow_case_data_session):
    """Test legacy implementation of getting System Coupling related settings."""
    _test_systemcoupling_mixing_elbow_settings_common(mixing_elbow_case_data_session)
