# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

""".. _ref_resilient_mode_demo:

Resilient mode walkthrough
--------------------------
This script shows each resilient-mode capability on live Fluent sessions, one
chapter at a time:

1. Repair of rejected values and activation of the energy model.
2. Undo and redo of settings changes.
3. Checkpoints before solves, and rollback.
4. Failover to a warm standby after the Fluent process is killed.
5. Automatic rollback of a diverging transient solve.

Run it from a terminal::

    python demo_resilient_mode.py [--auto] [--failover] [--no-gui]

``--auto`` runs without pausing between chapters. ``--failover`` adds chapter 4,
which launches a second Fluent session as a warm standby. ``--no-gui`` runs Fluent
without its GUI.

See :ref:`ref_resilient_guide` for details.
"""

# %%
# Helpers
# ~~~~~~~

import argparse
import contextlib
import subprocess
import warnings

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.core.resilient import PoolConfig, ResilientConfig, ResilientWarning

# Every repair is also reported as an event, which this demo prints.
warnings.simplefilter("ignore", ResilientWarning)


def chapter(number: int, title: str, auto: bool) -> None:
    """Print a chapter title, after waiting for Enter unless ``auto`` is set."""
    if not auto:
        input("\nPress Enter to continue...")
    print(f"\n{'=' * 72}\n  {number}. {title}\n{'=' * 72}")


def show_event(event) -> None:
    """Print a resilient-mode event."""
    print(f"  >> resilient mode [{event.kind.value}]: {event.message}")


# %%
# Mixing elbow: recovery, undo and redo, checkpoints and failover
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def mixing_elbow(ui_mode: str, auto: bool, failover: bool) -> None:
    """Run chapters 1 to 4 on the mixing elbow."""
    solver = pyfluent.launch_fluent(
        mode=pyfluent.FluentMode.SOLVER,
        precision=pyfluent.Precision.DOUBLE,
        processor_count=2,
        ui_mode=ui_mode,
        start_transcript=False,
        resilient_mode=True,
        resilient_config=ResilientConfig(
            allow_model_activation=True,
            pool=PoolConfig(size=2 if failover else 1),
        ),
    )
    solver.resilient.on_event(show_event)
    try:
        mesh = examples.download_file("mixing_elbow.msh.h5", "pyfluent/mixing_elbow")
        solver.settings.file.read_mesh(file_name=mesh)
        setup = solver.settings.setup
        cold_inlet = setup.boundary_conditions.velocity_inlet["cold-inlet"]
        hot_inlet = setup.boundary_conditions.velocity_inlet["hot-inlet"]

        chapter(1, "Repair of rejected values", auto)
        setup.models.energy.enabled = False
        print("Energy model enabled:", setup.models.energy.enabled())
        print("Setting the cold inlet temperature while the energy model is off.")
        cold_inlet.thermal.temperature.value = 293.15
        print("Energy model enabled:", setup.models.energy.enabled())
        print("Setting a turbulent intensity of 5 (the allowed range is 0 to 1).")
        cold_inlet.turbulence.turbulence_specification = (
            "Intensity and Hydraulic Diameter"
        )
        cold_inlet.turbulence.turbulent_intensity = 5
        print("Turbulent intensity:", cold_inlet.turbulence.turbulent_intensity())
        print("Setting the hot inlet specification with '&' instead of 'and'.")
        hot_inlet.turbulence.turbulence_specification = "Intensity & Hydraulic Diameter"
        print("Specification:", hot_inlet.turbulence.turbulence_specification())

        cold_inlet.momentum.velocity_magnitude.value = 0.4
        cold_inlet.turbulence.turbulent_intensity = 0.05
        cold_inlet.turbulence.hydraulic_diameter = "4 [in]"
        hot_inlet.momentum.velocity_magnitude.value = 1.2
        hot_inlet.turbulence.hydraulic_diameter = "1 [in]"
        hot_inlet.thermal.temperature.value = 313.15

        chapter(2, "Undo and redo", auto)
        viscous = setup.models.viscous
        print("Viscous model:", viscous.model())
        viscous.model = "laminar"
        print("Viscous model:", viscous.model())
        solver.resilient.undo()
        print("After undo:", viscous.model())
        solver.resilient.redo()
        print("After redo:", viscous.model())
        solver.resilient.undo()
        print("After a second undo:", viscous.model())

        chapter(3, "Checkpoints and rollback", auto)
        run_calculation = solver.settings.solution.run_calculation
        solver.settings.solution.initialization.hybrid_initialize()
        solver.resilient.checkpoint("initialized")
        cold_inlet.momentum.velocity_magnitude.value = 0.6
        print("Iterating; a checkpoint is written first.")
        run_calculation.iterate(iter_count=20)
        print("Checkpoints:", [c.name for c in solver.resilient.checkpoints])
        print("Rolling back to 'initialized'.")
        solver.resilient.rollback("initialized")
        print("Checkpoints:", [c.name for c in solver.resilient.checkpoints])
        print("Cold inlet velocity:", cold_inlet.momentum.velocity_magnitude.value())

        if failover:
            chapter(4, "Failover to a warm standby", auto)
            solver.resilient.checkpoint("before-crash")
            cold_inlet.momentum.velocity_magnitude.value = 0.5
            print("Killing the Fluent process of the active session.")
            # On Windows, Fluent's cleanup script can report a failure even though
            # it killed Fluent.
            with contextlib.suppress(subprocess.CalledProcessError):
                solver.force_exit()
            print("Setting the hot inlet velocity on the dead session.")
            hot_inlet.momentum.velocity_magnitude.value = 1.0
            standby = solver.resilient.active_session
            print("A different Fluent session took over:", standby is not solver)
            print(
                "Cold inlet velocity, replayed on the standby:",
                cold_inlet.momentum.velocity_magnitude.value(),
            )
            print("Iterating on the standby.")
            run_calculation.iterate(iter_count=10)
        print(solver.resilient)
    finally:
        solver.exit()


# %%
# Solidification: automatic rollback of a diverging solve
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def setup_solidification(solver) -> None:
    """Set up the solidification case and solve the steady conduction problem."""
    mesh = examples.download_file("solid.msh", "pyfluent/solidification")
    settings = solver.settings
    settings.file.read_mesh(file_name=mesh)
    general = settings.setup.general
    general.solver.two_dim_space = "swirl"
    general.operating_conditions.gravity = {"enable": True, "components": [-9.81]}
    settings.setup.models.viscous.model = "laminar"
    solver.tui.define.models.solidification_melting(
        "yes", "constant", "100000", "yes", "no"
    )
    materials = settings.setup.materials
    materials.database.copy_by_name(type="fluid", name="air", new_name="liquid-metal")
    materials.fluid["liquid-metal"] = {
        "density": {
            "polynomial": {"coefficients": [8000, -0.1], "function_of": "temperature"},
            "option": "polynomial",
        },
        "viscosity": {"value": 0.00553},
        "specific_heat": {"value": 680.0},
        "thermal_conductivity": {"value": 30.0},
        "melting_heat": {"value": 100000.0},
        "tsolidus": {"value": 1150.0},
        "tliqidus": {"value": 1150.0},
    }
    settings.setup.cell_zone_conditions.fluid["fluid"] = {
        "general": {"material": "liquid-metal"}
    }
    conditions = settings.setup.boundary_conditions
    inlet = conditions.velocity_inlet["inlet"]
    inlet.momentum.velocity_magnitude.value = 0.00101
    inlet.thermal.temperature.value = 1300
    outlet = conditions.velocity_inlet["outlet"]
    outlet.momentum.velocity_specification_method = "Components"
    outlet.momentum.swirl_angular_velocity = 1
    outlet.momentum.velocity_components = [0.001, 0, 0]
    outlet.thermal.temperature.value = 500
    conditions.wall["bottom-wall"] = {
        "thermal": {"thermal_condition": "Temperature", "temperature": 1300}
    }
    conditions.wall["free-surface"] = {
        "momentum": {
            "shear_condition": "Marangoni Stress",
            "surface_tension_gradient": -0.00036,
        },
        "thermal": {
            "thermal_condition": "Convection",
            "free_stream_temp": 1500,
            "heat_transfer_coeff": 100,
        },
    }
    conditions.wall["side-wall"] = {
        "thermal": {"thermal_condition": "Temperature", "temperature": 1400}
    }
    conditions.wall["solid-wall"] = {
        "momentum": {
            "wall_motion": "Moving Wall",
            "velocity_spec": "Rotational",
            "rotation_speed": 1,
        },
        "thermal": {"thermal_condition": "Temperature", "temperature": 500},
    }
    methods = settings.solution.methods
    methods.p_v_coupling.flow_scheme = "Coupled"
    methods.spatial_discretization.discretization_scheme = {"pressure": "presto!"}
    methods.pseudo_time_method.formulation = {"coupled_solver": "global-time-step"}
    controls = settings.solution.controls
    controls.equations = {"flow": False, "w-swirl": False}
    initialization = settings.solution.initialization
    initialization.hybrid_initialize()
    settings.results.custom_field_functions.create(
        name="omegar", custom_field_function="1 * radial_coordinate"
    )
    for variable, value in (("x-pull-velocity", 0.001), ("z-pull-velocity", None)):
        patch = {
            "cell_zones": ["fluid"],
            "variable": variable,
            "reference_frame": "Relative to Cell Zone",
            "use_custom_field_function": True,
            "custom_field_function_name": "omegar",
        }
        if value is not None:
            patch["value"] = value
        initialization.patch.calculate_patch(**patch)
    run_calculation = settings.solution.run_calculation
    run_calculation.pseudo_time_settings.time_step_method = {
        "time_step_method": "user-specified",
        "auto_time_size_calc_solid_zone": False,
    }
    run_calculation.iterate(iter_count=20)


def solidification(ui_mode: str, auto: bool) -> None:
    """Run chapter 5 on the solidification case."""
    chapter(5, "Automatic rollback of a diverging solve", auto)
    solver = pyfluent.launch_fluent(
        mode=pyfluent.FluentMode.SOLVER,
        precision=pyfluent.Precision.DOUBLE,
        dimension=pyfluent.Dimension.TWO,
        ui_mode=ui_mode,
        start_transcript=False,
        resilient_mode=True,
    )
    solver.resilient.on_event(show_event)
    try:
        print("Setting up the solidification case and solving the steady state.")
        setup_solidification(solver)
        settings = solver.settings
        settings.setup.general.solver.time = "unsteady-1st-order"
        controls = settings.solution.controls
        controls.equations = {"flow": True, "w-swirl": True}
        controls.under_relaxation = {"delh": 0.1}
        transient_controls = settings.solution.run_calculation.transient_controls
        transient_controls.time_step_size = 0.1
        transient_controls.time_step_count = 50

        print("Solving to 5 seconds with a time step of 0.1 s; the solve diverges.")
        try:
            settings.solution.run_calculation.calculate()
        except RuntimeError as error:
            print(f"The solve failed: {error}")
            print("Rolled back:", solver.resilient.last_outcome.rolled_back)
            print("Retrying from the restored steady state with a time step of 1 ms.")
            controls.under_relaxation = {"delh": 0.02}
            transient_controls.time_step_size = 0.001
            transient_controls.time_step_count = 5
            settings.solution.run_calculation.calculate()
            print("The retry completed.")
        else:
            print("The solve did not diverge this time.")
    finally:
        solver.exit()


# %%
# Run the demo
# ~~~~~~~~~~~~


def main() -> None:
    """Parse the command line and run the chapters."""
    parser = argparse.ArgumentParser(description="PyFluent resilient mode demo.")
    parser.add_argument("--auto", action="store_true", help="do not pause")
    parser.add_argument(
        "--failover", action="store_true", help="also demonstrate failover"
    )
    parser.add_argument("--no-gui", action="store_true", help="hide the Fluent GUI")
    args = parser.parse_args()
    ui_mode = "no_gui" if args.no_gui else "gui"
    mixing_elbow(ui_mode, args.auto, args.failover)
    solidification(ui_mode, args.auto)


if __name__ == "__main__":
    main()
