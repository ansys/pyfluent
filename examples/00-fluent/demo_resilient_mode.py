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

1. Undo and redo of settings changes.
2. Checkpoints before solves, and rollback.
3. Failover to a warm standby after the Fluent process is killed.
4. Automatic rollback of a diverging transient solve.

Run it from a terminal::

    python demo_resilient_mode.py [--auto] [--failover] [--no-gui]

``--auto`` runs without pausing between chapters. ``--failover`` adds chapter 3,
which launches a second Fluent session as a warm standby. ``--no-gui`` runs Fluent
without its GUI.

See :ref:`ref_resilient_guide` for details.
"""

# %%
# Helpers
# ~~~~~~~

import argparse
import contextlib
import os
import re
import subprocess
import textwrap
import warnings

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.core.diagnostics.exceptions import DeprecatedSettingWarning
from ansys.fluent.core.resilient import PoolConfig, ResilientConfig, ResilientWarning

# Every repair is also reported as an event, which this demo prints.
warnings.simplefilter("ignore", ResilientWarning)
# Development builds of Fluent suggest newer names for some settings. The demo
# keeps the names of the released versions so that it runs on all of them.
warnings.simplefilter("ignore", DeprecatedSettingWarning)

WIDTH = 78

INTRO = """\
PyFluent resilient mode walkthrough

The script below is ordinary PyFluent code. While you read the output:
  > lines           what the script does next
  indented lines    values read back from Fluent
  [resilient: ...]  what resilient mode did, and why"""


def chapter(number: int, title: str, auto: bool) -> None:
    """Print a chapter title, after waiting for Enter unless ``auto`` is set."""
    if not auto:
        input("\nPress Enter for the next chapter...")
    print(f"\n{'=' * WIDTH}\n {number}. {title}\n{'=' * WIDTH}")


def step(text: str) -> None:
    """Print what the script does next."""
    print(
        "\n" + textwrap.fill(text, WIDTH, initial_indent="> ", subsequent_indent="  ")
    )


def show(label: str, value) -> None:
    """Print a value read back from Fluent."""
    print(f"    {label}: {value}")


def first_line(error: Exception) -> str:
    """Return the first line of an error message."""
    lines = str(error).strip().splitlines()
    return lines[0] if lines else type(error).__name__


def show_event(event) -> None:
    """Print a resilient-mode event, wrapped, with short checkpoint file names."""
    message = event.message
    checkpoint = event.data.get("checkpoint")
    if checkpoint:
        message = message.replace(
            checkpoint["path"], os.path.basename(checkpoint["path"])
        )
    # Keep quoted names such as ["cold-inlet"] on one line.
    message = re.sub(r'"[^"]*"', lambda m: m.group(0).replace(" ", "\xa0"), message)
    text = textwrap.fill(
        message,
        WIDTH,
        initial_indent=f"    [resilient: {event.kind.value}] ",
        subsequent_indent=" " * 8,
        break_long_words=False,
        break_on_hyphens=False,
    )
    print(text.replace("\xa0", " "))


# %%
# Mixing elbow: recovery, undo and redo, checkpoints and failover
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def mixing_elbow(ui_mode: str, auto: bool, failover: bool) -> None:
    """Run chapters 1 to 3 on the mixing elbow."""
    solver = pyfluent.Solver.from_install(
        precision=pyfluent.Precision.DOUBLE,
        processor_count=2,
        ui_mode=ui_mode,
        start_transcript=False,
        resilient_mode=True,
        resilient_config=ResilientConfig(
            pool=PoolConfig(size=2 if failover else 1),
        ),
    )
    solver.resilient.on_event(show_event)
    try:
        mesh = examples.download_file("mixing_elbow.msh.h5", "pyfluent/mixing_elbow")
        solver.settings.file.read_mesh(file_name=mesh)
        # Built-in solver objects:
        viscous = pyfluent.solver.Viscous(settings_source=solver)
        energy = pyfluent.solver.Energy(settings_source=solver)
        cold_inlet = pyfluent.solver.VelocityInlet(
            settings_source=solver, name="cold-inlet"
        )
        hot_inlet = pyfluent.solver.VelocityInlet(
            settings_source=solver, name="hot-inlet"
        )
        initialization = pyfluent.solver.Initialization(settings_source=solver)
        run_calculation = pyfluent.solver.RunCalculation(settings_source=solver)
        # Aliasing reused objects:
        cold_turbulence = cold_inlet.turbulence
        hot_turbulence = hot_inlet.turbulence
        cold_velocity = cold_inlet.momentum.velocity_magnitude
        hot_velocity = hot_inlet.momentum.velocity_magnitude
        resilient = solver.resilient

        chapter(1, "Undo and redo", auto)
        step("Switch the viscous model to laminar, then undo, redo and undo again.")
        show("viscous model", viscous.model())
        viscous.model = "laminar"
        show("viscous model", viscous.model())
        resilient.undo()
        show("after undo", viscous.model())
        resilient.redo()
        show("after redo", viscous.model())
        resilient.undo()
        show("after a second undo", viscous.model())

        chapter(2, "Checkpoints and rollback", auto)
        step(
            "Enable the energy model and set the inlet conditions for the solve: "
            "0.4 m/s, 5 % turbulent intensity and 293.15 K at the cold inlet, "
            "1.2 m/s and 313.15 K at the hot inlet. The settings API takes the "
            "turbulent intensity as a fraction, so 5 % is 0.05."
        )
        energy.enabled = True
        cold_velocity.value = 0.4
        cold_turbulence.turbulence_specification = "Intensity and Hydraulic Diameter"
        cold_turbulence.turbulent_intensity = 0.05
        cold_turbulence.hydraulic_diameter = "4 [in]"
        cold_inlet.thermal.temperature.value = 293.15
        hot_velocity.value = 1.2
        hot_turbulence.turbulence_specification = "Intensity and Hydraulic Diameter"
        hot_turbulence.hydraulic_diameter = "1 [in]"
        hot_inlet.thermal.temperature.value = 313.15
        show(
            "cold inlet",
            f"{cold_velocity.value():g} m/s, turbulent intensity "
            f"{cold_turbulence.turbulent_intensity():g}, "
            f"{cold_inlet.thermal.temperature.value():g} K",
        )
        show(
            "hot inlet",
            f"{hot_velocity.value():g} m/s, "
            f"{hot_inlet.thermal.temperature.value():g} K",
        )
        initialization.hybrid_initialize()
        step("Write a checkpoint named 'initialized'.")
        checkpoint = resilient.checkpoint("initialized")
        show("checkpoint folder", os.path.dirname(checkpoint.path))
        step(
            "Change the cold-inlet velocity to 0.6 and iterate. Iterating cannot be "
            "undone, so resilient mode writes a checkpoint first."
        )
        cold_velocity.value = 0.6
        run_calculation.iterate(iter_count=20)
        show("checkpoints", [c.name for c in resilient.checkpoints])
        step("Roll back to 'initialized'.")
        resilient.rollback("initialized")
        show("checkpoints", [c.name for c in resilient.checkpoints])
        show("cold-inlet velocity", cold_velocity.value())

        if failover:
            chapter(3, "Failover to a warm standby", auto)
            step("Write a checkpoint, then change the cold-inlet velocity to 0.5.")
            resilient.checkpoint("before-crash")
            cold_velocity.value = 0.5
            step("Kill the Fluent process of the active session.")
            # On Windows, Fluent's cleanup script can report a failure even though
            # it killed Fluent.
            with contextlib.suppress(subprocess.CalledProcessError):
                solver.force_exit()
            step("Change the hot-inlet velocity on the session that was just killed.")
            hot_velocity.value = 1.0
            standby = resilient.active_session
            show("served by another Fluent session", standby is not solver)
            show("cold-inlet velocity (replayed)", cold_velocity.value())
            show("hot-inlet velocity", hot_velocity.value())
            step("Iterate on the standby.")
            run_calculation.iterate(iter_count=10)
        step("Summary of this resilient session.")
        show("checkpoints", len(resilient.checkpoints))
        show("journaled operations", len(resilient.journal))
    finally:
        solver.exit()


# %%
# Solidification: automatic rollback of a diverging solve
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def setup_solidification(solver) -> None:
    """Set up the solidification case and solve the steady conduction problem."""
    mesh = examples.download_file("solid.msh", "pyfluent/solidification")
    solver.settings.file.read_mesh(file_name=mesh)
    # Built-in solver objects:
    general = pyfluent.solver.General(settings_source=solver)
    viscous = pyfluent.solver.Viscous(settings_source=solver)
    materials = pyfluent.solver.Materials(settings_source=solver)
    fluid = pyfluent.solver.FluidCellZone(settings_source=solver, name="fluid")
    inlet = pyfluent.solver.VelocityInlet(settings_source=solver, name="inlet")
    outlet = pyfluent.solver.VelocityInlet(settings_source=solver, name="outlet")
    methods = pyfluent.solver.Methods(settings_source=solver)
    controls = pyfluent.solver.Controls(settings_source=solver)
    initialization = pyfluent.solver.Initialization(settings_source=solver)
    results = pyfluent.solver.Results(settings_source=solver)
    run_calculation = pyfluent.solver.RunCalculation(settings_source=solver)
    # Aliasing reused objects:
    outlet_momentum = outlet.momentum

    general.solver.two_dim_space = "swirl"
    general.operating_conditions.gravity = {"enable": True, "components": [-9.81]}
    viscous.model = "laminar"
    solver.tui.define.models.solidification_melting(
        "yes", "constant", "100000", "yes", "no"
    )
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
    fluid.general.material = "liquid-metal"
    inlet.momentum.velocity_magnitude.value = 0.00101
    inlet.thermal.temperature.value = 1300
    outlet_momentum.velocity_specification_method = "Components"
    outlet_momentum.swirl_angular_velocity = 1
    outlet_momentum.velocity_components = [0.001, 0, 0]
    outlet.thermal.temperature.value = 500
    walls = {
        "bottom-wall": {
            "thermal": {"thermal_condition": "Temperature", "temperature": 1300}
        },
        "free-surface": {
            "momentum": {
                "shear_condition": "Marangoni Stress",
                "surface_tension_gradient": -0.00036,
            },
            "thermal": {
                "thermal_condition": "Convection",
                "free_stream_temp": 1500,
                "heat_transfer_coeff": 100,
            },
        },
        "side-wall": {
            "thermal": {"thermal_condition": "Temperature", "temperature": 1400}
        },
        "solid-wall": {
            "momentum": {
                "wall_motion": "Moving Wall",
                "velocity_spec": "Rotational",
                "rotation_speed": 1,
            },
            "thermal": {"thermal_condition": "Temperature", "temperature": 500},
        },
    }
    for name, state in walls.items():
        pyfluent.solver.WallBoundary(settings_source=solver, name=name).set_state(state)
    methods.p_v_coupling.flow_scheme = "Coupled"
    methods.spatial_discretization.discretization_scheme = {"pressure": "presto!"}
    methods.pseudo_time_method.formulation = {"coupled_solver": "global-time-step"}
    controls.equations = {"flow": False, "w-swirl": False}
    initialization.hybrid_initialize()
    results.custom_field_functions.create(
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
    run_calculation.pseudo_time_settings.time_step_method = {
        "time_step_method": "user-specified",
        "auto_time_size_calc_solid_zone": False,
    }
    run_calculation.iterate(iter_count=20)


def solidification(ui_mode: str, auto: bool) -> None:
    """Run chapter 4 on the solidification case."""
    chapter(4, "Automatic rollback of a diverging solve", auto)
    solver = pyfluent.Solver.from_install(
        precision=pyfluent.Precision.DOUBLE,
        dimension=pyfluent.Dimension.TWO,
        ui_mode=ui_mode,
        start_transcript=False,
        resilient_mode=True,
    )
    solver.resilient.on_event(show_event)
    try:
        step("Set up the solidification case and solve the steady state.")
        setup_solidification(solver)
        # Built-in solver objects:
        general = pyfluent.solver.General(settings_source=solver)
        controls = pyfluent.solver.Controls(settings_source=solver)
        run_calculation = pyfluent.solver.RunCalculation(settings_source=solver)
        # Aliasing reused objects:
        transient_controls = run_calculation.transient_controls

        general.solver.time = "unsteady-1st-order"
        controls.equations = {"flow": True, "w-swirl": True}
        controls.under_relaxation = {"delh": 0.1}
        transient_controls.time_step_size = 0.1
        transient_controls.time_step_count = 50

        step(
            "Solve to 5 s with a time step of 0.1 s. The time step is too large, so "
            "the solve diverges; resilient mode wrote a checkpoint before it."
        )
        try:
            run_calculation.calculate()
        except RuntimeError as error:
            show("Fluent error", first_line(error))
            show("rolled back", solver.resilient.last_outcome.rolled_back)
            step("Retry from the restored steady state with a time step of 1 ms.")
            controls.under_relaxation = {"delh": 0.02}
            transient_controls.time_step_size = 0.001
            transient_controls.time_step_count = 5
            run_calculation.calculate()
            show("retry", "completed")
        else:
            show("retry", "not needed; the solve did not diverge this time")
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
    print(INTRO)
    mixing_elbow(ui_mode, args.auto, args.failover)
    solidification(ui_mode, args.auto)


if __name__ == "__main__":
    main()
