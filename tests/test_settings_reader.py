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

from ansys.fluent.core import examples
from ansys.fluent.core.filereader.case_file import SettingsFile as SettingsReader


def call_settings_reader(
    settings_file_name: str | None = None, expected: dict | None = None
):
    reader = SettingsReader(settings_file_name=settings_file_name)
    if expected is not None:
        assert reader.precision() == expected["precision"]
        assert reader.num_dimensions() == expected["num_dimensions"]
        assert reader.iter_count() == expected["iter_count"]
        assert {
            p.name: (p.numeric_value, p.units) for p in reader.input_parameters()
        } == expected["input_parameters"]
        assert {p.name: p.units for p in reader.output_parameters()} == expected[
            "output_parameters"
        ]


def call_settings_reader_static_mixer(
    settings_file_name: str | None = None,
):
    call_settings_reader(
        settings_file_name=settings_file_name,
        expected=dict(
            precision=2,
            num_dimensions=3,
            iter_count=100,
            input_parameters=dict(
                inlet1_temp=(300, "K"),
                inlet1_vel=(1, "m/s"),
                inlet2_temp=(350, "K"),
                inlet2_vel=(1, "m/s"),
            ),
            output_parameters={
                "outlet-temp-avg-op": "K",
                "outlet-vel-avg-op": "m s^-1",
            },
        ),
    )


def static_mixer_settings_file():
    return examples.download_file(
        "Static_Mixer_Params",
        "pyfluent/static_mixer",
        return_without_path=False,
    )


def test_settings_reader_static_mixer_h5():
    call_settings_reader_static_mixer(settings_file_name=static_mixer_settings_file())


def test_meshing_unavailable():
    reader = SettingsReader(settings_file_name=static_mixer_settings_file())
    with pytest.raises(AttributeError):
        reader.get_mesh()


def test_settings_reader_get_rp_and_config_vars():
    reader = SettingsReader(settings_file_name=static_mixer_settings_file())
    rp_vars = reader.rp_vars()
    assert rp_vars
    assert hasattr(rp_vars, "__getitem__")
    config_vars = reader.config_vars()
    assert config_vars
    assert hasattr(config_vars, "__getitem__")
    assert config_vars["rp-3d?"] is True
    assert reader.config_var("rp-3d?") is True
    assert reader.config_var.rp_3d__q() is True
    assert len(reader.rp_var.context.map_r17__plus()) == 53

    with pytest.raises(RuntimeError) as msg:
        reader.rp_var.defaults.pre_r19__dot0_early()

    with pytest.raises(ValueError) as msg:
        reader.config_var("rp-3d")
    assert (
        msg.value.args[0] == "'config-vars' has no attribute 'rp-3d'.\n"
        "The most similar names are: rp-3d?, rp-des?."
    )
