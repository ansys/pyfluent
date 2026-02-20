# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
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

from concurrent.futures import Future
from typing import Callable
import warnings

from _pytest.recwarn import WarningsRecorder
import pytest

import ansys.fluent.core as pyfluent
from ansys.fluent.core import config
from ansys.fluent.core.data_model_cache import DataModelCache
from ansys.fluent.core.examples import download_file
from ansys.fluent.core.launcher.slurm_launcher import SlurmFuture, _SlurmWrapper


def fluent_launcher_args(args: str):
    def fluent_launcher_args_inner(f: Callable):
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        wrapper.fluent_launcher_args = args
        return wrapper

    return fluent_launcher_args_inner


def mixing_elbow_geometry_filename(globals):
    return download_file(
        file_name="mixing_elbow.pmdb", directory="pyfluent/mixing_elbow"
    )


def exhaust_system_geometry_filename(globals):
    return download_file(
        file_name="exhaust_system.fmd", directory="pyfluent/exhaust_system"
    )


@fluent_launcher_args("3ddp -meshing")
def new_meshing_session(globals):
    meshing = globals["meshing"]
    return meshing


@fluent_launcher_args("3ddp -meshing")
def new_meshing_session_wo_exit(globals):
    return new_meshing_session(globals)


@fluent_launcher_args("3ddp -meshing")
def new_pure_meshing_session(globals):
    return new_meshing_session(globals)


@fluent_launcher_args("3ddp -meshing")
def watertight_workflow_session(globals):
    meshing = new_meshing_session(globals)
    meshing.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
    return meshing


@fluent_launcher_args("3ddp -meshing")
def watertight_workflow_session_wo_exit(globals):
    meshing = new_meshing_session_wo_exit(globals)
    meshing.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
    return meshing


@fluent_launcher_args("3ddp -meshing")
def fault_tolerant_workflow_session(globals):
    meshing = new_meshing_session(globals)
    meshing.workflow.InitializeWorkflow(WorkflowType="Fault-tolerant Meshing")
    return meshing


@fluent_launcher_args("3ddp -meshing")
def fault_tolerant_workflow_session_wo_exit(globals):
    meshing = new_meshing_session_wo_exit(globals)
    meshing.workflow.InitializeWorkflow(WorkflowType="Fault-tolerant Meshing")
    return meshing


@fluent_launcher_args("3ddp -meshing")
def mixing_elbow_watertight_pure_meshing_session(globals):
    meshing = new_pure_meshing_session(globals)
    geometry_filename = mixing_elbow_geometry_filename(globals)
    meshing.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
    meshing.workflow.TaskObject["Import Geometry"].Arguments = dict(
        FileName=geometry_filename, LengthUnit="in"
    )
    return meshing


@fluent_launcher_args("3ddp")
def new_solver_session(globals):
    solver = globals["solver"]
    return solver


@fluent_launcher_args("3ddp")
def new_solver_session_wo_exit(globals):
    return new_solver_session(globals)


@fluent_launcher_args("3ddp -t 4")
def new_solver_session_t4(globals):
    return new_solver_session(globals)


@fluent_launcher_args("3d")
def new_solver_session_sp(globals):
    return new_solver_session(globals)


@fluent_launcher_args("2ddp")
def new_solver_session_2d(globals):
    return new_solver_session(globals)


@fluent_launcher_args("3ddp")
def static_mixer_settings_session(globals):
    solver = new_solver_session(globals)
    case_name = download_file("Static_Mixer_main.cas.h5", "pyfluent/static_mixer")
    solver.file.read(
        file_type="case",
        file_name=case_name,
        lightweight_setup=True,
    )
    return solver


@fluent_launcher_args("3ddp")
def static_mixer_case_session(globals):
    solver = new_solver_session(globals)
    case_name = download_file("Static_Mixer_main.cas.h5", "pyfluent/static_mixer")
    solver.file.read(file_type="case", file_name=case_name)
    return solver


@fluent_launcher_args("3ddp")
def static_mixer_params_unitless_session(globals):
    solver = new_solver_session(globals)
    case_name = download_file(
        "Static_Mixer_Parameters_unitless.cas.h5", "pyfluent/static_mixer"
    )
    solver.settings.file.read(file_type="case", file_name=case_name)
    return solver


@fluent_launcher_args("3ddp")
def mixing_elbow_settings_session(globals):
    solver = new_solver_session(globals)
    case_name = download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    solver.settings.file.read(
        file_type="case",
        file_name=case_name,
        lightweight_setup=True,
    )
    return solver


@fluent_launcher_args("3ddp")
def mixing_elbow_case_session(globals):
    solver = new_solver_session(globals)
    case_name = download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    solver.settings.file.read(file_type="case", file_name=case_name)
    return solver


@fluent_launcher_args("3ddp")
def mixing_elbow_case_data_session(globals):
    solver = new_solver_session(globals)
    case_name = download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    download_file("mixing_elbow.dat.h5", "pyfluent/mixing_elbow")
    solver.settings.file.read(file_type="case-data", file_name=case_name)
    return solver


@fluent_launcher_args("3ddp -t 4")
def mixing_elbow_case_session_t4(globals):
    solver = new_solver_session_t4(globals)
    case_name = download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    solver.settings.file.read(file_type="case", file_name=case_name)
    return solver


@fluent_launcher_args("3ddp")
def mixing_elbow_param_case_data_session(globals):
    solver = new_solver_session(globals)
    case_name = download_file("elbow_param.cas.h5", "pyfluent/mixing_elbow")
    download_file("elbow_param.dat.h5", "pyfluent/mixing_elbow")
    solver.settings.file.read(file_type="case-data", file_name=case_name)
    return solver


@fluent_launcher_args("2ddp")
def disk_settings_session(globals):
    solver = new_solver_session_2d(globals)
    case_name = download_file("disk.cas.h5", "pyfluent/rotating_disk")
    solver.file.read(
        file_type="case",
        file_name=case_name,
        lightweight_setup=True,
    )
    return solver


@fluent_launcher_args("2ddp")
def disk_case_session(globals):
    solver = new_solver_session_2d(globals)
    case_name = download_file("disk.cas.h5", "pyfluent/rotating_disk")
    solver.file.read(file_type="case", file_name=case_name)
    return solver


@fluent_launcher_args("3ddp")
def periodic_rot_settings_session(globals):
    solver = new_solver_session(globals)
    case_name = download_file(
        "periodic_rot.cas.h5",
        "pyfluent/periodic_rot",
    )
    solver.file.read(
        file_type="case",
        file_name=case_name,
        lightweight_setup=True,
    )
    return solver


monkeypatch = pytest.MonkeyPatch()


def disable_datamodel_cache(globals):
    monkeypatch.setattr(pyfluent.config, "datamodel_use_state_cache", False)


def display_names_as_keys_in_cache(globals):
    DataModelCache.use_display_name = True


def new_meshing_session2(globals):
    session = pyfluent.launch_fluent(mode=pyfluent.LaunchMode.MESHING)
    return session


def new_solver_session2(globals):
    session = pyfluent.launch_fluent()
    return session


def static_mixer_case_session2(globals):
    session = new_solver_session2(globals)
    case_name = download_file("Static_Mixer_main.cas.h5", "pyfluent/static_mixer")
    session.file.read(file_type="case", file_name=case_name)
    return session


def reset_examples_path(globals):
    try:
        delattr(pyfluent, "EXAMPLES_PATH")
        delattr(pyfluent.config, "_examples_path")
    except AttributeError:
        pass


def slurm_future(globals) -> SlurmFuture:
    class _Env:
        def __init__(self):
            self.state = None

        def set_state(self, state):
            self.state = state

    _SlurmWrapper.is_available = staticmethod(lambda: True)
    env = _Env()
    fut = Future()
    fut.set_running_or_notify_cancel()
    sf = SlurmFuture(fut, 0)
    sf._get_state = lambda: env.state
    sf._cancel = lambda: env.set_state("")
    env.set_state("RUNNING")
    sf.env = env
    return sf


def disable_slurm_in_current_machine(globals):
    config.use_slurm_from_current_machine = False


def warning_record(globals):
    wrec = WarningsRecorder(_ispytest=True)
    wrec.__enter__()
    warnings.simplefilter("ignore", ResourceWarning)
    return wrec


def use_runtime_python_classes(globals):
    config.use_runtime_python_classes = True
