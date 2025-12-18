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


@pytest.mark.settings_only
@pytest.mark.fluent_version("latest")
def test_solver_models(mixing_elbow_settings_session):
    solver_session = mixing_elbow_settings_session
    models = solver_session.setup.models
    assert models.energy.enabled()
    models.energy.enabled = False
    assert not models.energy.enabled()
    models.multiphase.models = "vof"
    assert models.multiphase.models() == "vof"
    models.viscous.model = "laminar"
    assert models.viscous.model() == "laminar"
    models.viscous.model = "k-epsilon"
    assert models.viscous.model() == "k-epsilon"

    models.viscous.near_wall_treatment.wall_treatment = "enhanced-wall-treatment"
    models.multiphase.models = "eulerian"
    assert models.multiphase.models() == "eulerian"


@pytest.mark.settings_only
@pytest.mark.fluent_version("latest")
def test_disk_2d_models(disk_settings_session):
    solver_session = disk_settings_session
    models = solver_session.setup.models
    solver_session.setup.general.solver.two_dim_space = "axisymmetric"
    solver_session.setup.general.solver.two_dim_space = "swirl"

    models.viscous.model = "k-epsilon"
    near_wall = models.viscous.near_wall_treatment
    assert models.viscous.model() == "k-epsilon"
    near_wall.wall_treatment = "enhanced-wall-treatment"
    assert near_wall.wall_treatment() == "enhanced-wall-treatment"
    assert near_wall.wall_treatment.get_attr("allowed-values") == [
        "standard-wall-fn",
        "non-equilibrium-wall-fn",
        "enhanced-wall-treatment",
        "menter-lechner",
        "scalable-wall-functions",
    ]

    near_wall.wall_treatment = "standard-wall-fn"
    assert near_wall.wall_treatment() == "standard-wall-fn"
    near_wall.wall_treatment = "non-equilibrium-wall-fn"
    assert near_wall.wall_treatment() == "non-equilibrium-wall-fn"
    near_wall.wall_treatment = "menter-lechner"
    assert near_wall.wall_treatment() == "menter-lechner"
    near_wall.wall_treatment = "scalable-wall-functions"
    assert near_wall.wall_treatment() == "scalable-wall-functions"

    models.viscous.model = "k-omega"
    assert models.viscous.model() == "k-omega"
    assert models.viscous.k_omega_model.get_attr("allowed-values") == [
        "standard",
        "geko",
        "bsl",
        "sst",
    ]

    assert models.viscous.k_omega_model() == "standard"
    models.viscous.k_omega_model = "geko"
    assert models.viscous.k_omega_model() == "geko"
    models.viscous.k_omega_model = "bsl"
    assert models.viscous.k_omega_model() == "bsl"
    models.viscous.k_omega_model = "sst"
    assert models.viscous.k_omega_model() == "sst"
    assert models.viscous.model.get_attr("allowed-values") == [
        "inviscid",
        "laminar",
        "k-epsilon",
        "k-omega",
        "mixing-length",
        "spalart-allmaras",
        "k-kl-w",
        "transition-sst",
        "reynolds-stress",
        "scale-adaptive-simulation",
        "detached-eddy-simulation",
    ]
    k_omega_options = models.viscous.k_omega_options
    k_omega_options.kw_low_re_correction = True
    assert k_omega_options.kw_low_re_correction() is True

    turb_options = models.viscous.options
    turb_options.production_kato_launder_enabled = True
    assert turb_options.production_kato_launder_enabled() is True
    turb_options.production_limiter.clip_factor = 9
    assert turb_options.production_limiter.clip_factor() == 9
    turb_expert = models.viscous.turbulence_expert
    turb_expert.turb_non_newtonian = True
    assert turb_expert.turb_non_newtonian() is True

    models.viscous.model = "laminar"
    assert models.viscous.model() == "laminar"
    models.viscous.model = "spalart-allmaras"
    assert models.viscous.model() == "spalart-allmaras"
