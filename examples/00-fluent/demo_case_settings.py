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

""".. _ref_case_settings_demo:

CaseSettings walkthrough
------------------------
This script shows how :class:`~ansys.fluent.core.solver.case_settings.CaseSettings`
moves the complete setup of a case between Fluent solver sessions, one chapter at
a time:

1. Capture a setup, including a value that the settings API does not expose.
2. Apply it to several sessions in parallel.
3. Run variants of the setup side by side.
4. Save the setup to a case file and reuse it.
5. Apply the settings to the mesh of a session, and refuse mismatched zones.
6. Undo an apply with resilient mode.

Run it from a terminal::

    python demo_case_settings.py [--auto] [--no-gui]

``--auto`` runs without pausing between chapters. ``--no-gui`` runs Fluent
without its GUI. The script launches three Fluent sessions with two processes
each.

See :ref:`ref_data_transfer_guide` for details.
"""

# %%
# Helpers
# ~~~~~~~

import argparse
from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path
import textwrap
import time
import warnings

import ansys.fluent.core as pyfluent
from ansys.fluent.core import CaseSettings, examples
from ansys.fluent.core.diagnostics.exceptions import DeprecatedSettingWarning
from ansys.fluent.core.resilient import (
    CheckpointConfig,
    ResilientConfig,
    enable_resilient_mode,
)

# Development builds of Fluent suggest newer names for some settings. The demo
# keeps the names of the released versions so that it runs on all of them.
warnings.simplefilter("ignore", DeprecatedSettingWarning)

WIDTH = 78

INTRO = """\
PyFluent CaseSettings walkthrough

CaseSettings captures the complete setup of a case, all its settings and its
mesh, and applies it to other solver sessions. While you read the output:
  > lines           what the script does next
  indented lines    values read back from Fluent"""

# A Scheme variable saved in case files. The settings API does not expose it.
MARKER = "pyfluent/demo-marker"


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


def show_text(label: str, text: str, separator: str = ": ") -> None:
    """Print a long message, wrapped."""
    print(
        textwrap.fill(
            text,
            WIDTH,
            initial_indent=f"    {label}{separator}",
            subsequent_indent=" " * 8,
            break_long_words=False,
            break_on_hyphens=False,
        )
    )


def show_event(event) -> None:
    """Print a resilient-mode event with a short checkpoint file name."""
    message = event.message
    checkpoint = event.data.get("checkpoint")
    if checkpoint:
        message = message.replace(
            checkpoint["path"], os.path.basename(checkpoint["path"])
        )
    show_text(f"[resilient: {event.kind.value}]", message, separator=" ")


def launch(ui_mode: str, count: int) -> list:
    """Launch ``count`` solver sessions in parallel."""

    def launch_one(_):
        return pyfluent.launch_fluent(
            mode=pyfluent.FluentMode.SOLVER,
            precision=pyfluent.Precision.DOUBLE,
            processor_count=2,
            ui_mode=ui_mode,
            start_transcript=False,
        )

    with ThreadPoolExecutor(max_workers=count) as pool:
        futures = [pool.submit(launch_one, index) for index in range(count)]
    sessions = [future.result() for future in futures if not future.exception()]
    if len(sessions) < count:
        for session in sessions:
            session.exit()
        raise next(f.exception() for f in futures if f.exception())
    return sessions


def viscous(solver):
    """Return the viscous model settings."""
    models = solver.settings.setup.models
    # Newer Fluent versions name the viscous model "turbulence".
    return models.turbulence if "turbulence" in models.child_names else models.viscous


def cold_inlet(solver):
    """Return the cold-inlet settings."""
    return solver.settings.setup.boundary_conditions.velocity_inlet["cold-inlet"]


def pressure_outlets(solver) -> list:
    """Return the names of the pressure outlets."""
    return solver.settings.setup.boundary_conditions.pressure_outlet.get_object_names()


def set_marker(solver, value: int) -> None:
    """Set the Scheme variable that the settings API does not expose."""
    solver.scheme.eval(f"(rpsetvar '{MARKER} {value})")


def describe(solver) -> str:
    """Summarize the setup of a session in one line."""
    velocity = cold_inlet(solver).momentum.velocity_magnitude.value()
    marker = solver.scheme.eval(f"(rpgetvar '{MARKER})")
    return (
        f"{viscous(solver).model()}, cold inlet {velocity:g} m/s, "
        f"Scheme variable {marker}"
    )


def outlet_area(solver) -> str:
    """Return the area of the outlet, which shows the size of the mesh."""
    area = solver.fields.reduction.area(locations=["outlet"])
    return f"{area * 1e4:.1f} cm2"


def outlet_temperature(solver) -> str:
    """Return the mass-averaged temperature at the outlet."""
    temperature = solver.fields.reduction.mass_average(
        expression="StaticTemperature", locations=["outlet"]
    )
    return f"{temperature:.2f} K"


def solve(solver, velocity: float) -> None:
    """Set the cold-inlet velocity, initialize and run 50 iterations."""
    cold_inlet(solver).momentum.velocity_magnitude.value = velocity
    solver.settings.solution.initialization.hybrid_initialize()
    solver.settings.solution.run_calculation.iterate(iter_count=50)


# %%
# Chapters
# ~~~~~~~~


def run(ui_mode: str, auto: bool) -> None:
    """Run the chapters on the mixing elbow."""
    folder = Path.cwd() / "case_settings_demo"
    folder.mkdir(exist_ok=True)
    case_file = examples.download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")

    step("Launch three Fluent solver sessions in parallel: a source and two workers.")
    started = time.time()
    source, worker_1, worker_2 = launch(ui_mode, 3)
    show("ready after", f"{time.time() - started:.0f} s")
    workers = {"worker 1": worker_1, "worker 2": worker_2}
    try:
        chapter(1, "Capture a setup", auto)
        step(
            "Read the mixing elbow case into the source, then change its setup: the "
            "k-epsilon viscous model, a cold-inlet velocity of 0.4 m/s, and a Scheme "
            "variable that the settings API does not expose."
        )
        source.settings.file.read_case(file_name=case_file)
        viscous(source).model = "k-epsilon"
        cold_inlet(source).momentum.velocity_magnitude.value = 0.4
        source.scheme.eval(f"(rp-var-define '{MARKER} 0 'integer #f)")
        set_marker(source, 42)
        show("source", describe(source))
        step("Capture the setup: CaseSettings.from_session(source).")
        setup = CaseSettings.from_session(source)
        show("captured", setup)
        step("Change the source afterwards. The captured setup does not change.")
        viscous(source).model = "laminar"
        cold_inlet(source).momentum.velocity_magnitude.value = 0.9
        set_marker(source, 7)
        show("source", describe(source))

        chapter(2, "Apply to several sessions", auto)
        step("The workers start without a case.")
        for name, worker in workers.items():
            loaded = worker.scheme.eval("(case-valid?)")
            show(name, "a case is loaded" if loaded else "no case loaded")
        step(
            "Apply the setup to both workers: setup.apply_to(worker_1, worker_2). "
            "Both are checked first, then they load the setup in parallel."
        )
        started = time.time()
        setup.apply_to(*workers.values())
        show("applied after", f"{time.time() - started:.1f} s")
        for name, worker in workers.items():
            show(name, describe(worker))
        step("Apply it to the source too, which brings it back to the captured setup.")
        setup.apply_to(source)
        show("source", describe(source))

        chapter(3, "Run variants side by side", auto)
        velocities = {"worker 1": 0.3, "worker 2": 0.6}
        step(
            "Give each worker its own cold-inlet velocity (0.3 and 0.6 m/s), then "
            "initialize and run 50 iterations on both at the same time."
        )
        with ThreadPoolExecutor(max_workers=2) as pool:
            for future in [
                pool.submit(solve, workers[name], velocity)
                for name, velocity in velocities.items()
            ]:
                future.result()
        for name, worker in workers.items():
            show(
                name,
                f"cold inlet {velocities[name]:g} m/s, outlet temperature "
                f"{outlet_temperature(worker)}",
            )

        chapter(4, "Save the setup and reuse it", auto)
        step(
            "Save the setup to a case file. Any script can create CaseSettings from "
            "it later, without the source session."
        )
        saved = setup.save(folder / "elbow_k_epsilon.cas.h5")
        show("saved", saved.name)
        template = CaseSettings.from_file(saved)
        show("loaded", template)
        step("Apply it to worker 2, which goes back to the saved setup.")
        template.apply_to(worker_2)
        show("worker 2", describe(worker_2))

        chapter(5, "Keep the mesh of a session", auto)
        step(
            "Scale the mesh of worker 1 by 2. It stands in for a different mesh "
            "with the same zone names."
        )
        show("worker 1 outlet area", outlet_area(worker_1))
        worker_1.settings.mesh.scale(x_scale=2, y_scale=2, z_scale=2)
        show("worker 1 outlet area", outlet_area(worker_1))
        step(
            "Apply the setup with keep_mesh=True. Worker 1 takes the settings and "
            "keeps its own mesh."
        )
        setup.apply_to(worker_1, keep_mesh=True)
        show("worker 1", describe(worker_1))
        show("worker 1 outlet area", outlet_area(worker_1))
        step(
            "Rename the outlet zone of worker 2, then apply with keep_mesh=True. The "
            "zone names no longer match, so nothing is guessed: the error names the "
            "zones, and worker 2 is not changed."
        )
        outlets = worker_2.settings.setup.boundary_conditions.pressure_outlet
        outlets.rename(new="outlet-2", old="outlet")
        try:
            setup.apply_to(worker_2, keep_mesh=True)
        except ValueError as error:
            show_text("error", str(error))
        show("worker 2 pressure outlets", pressure_outlets(worker_2))

        chapter(6, "Undo an apply with resilient mode", auto)
        step(
            "Enable resilient mode on worker 2 and apply the setup. Resilient mode "
            "writes a checkpoint before reading the setup, and CaseSettings writes "
            "one after."
        )
        enable_resilient_mode(
            worker_2,
            ResilientConfig(
                checkpoint=CheckpointConfig(directory=folder / "checkpoints")
            ),
        )
        worker_2.resilient.on_event(show_event)
        setup.apply_to(worker_2)
        show("worker 2 pressure outlets", pressure_outlets(worker_2))
        step(
            "Roll back to the checkpoint written before the read. Worker 2 gets its "
            "renamed outlet back."
        )
        worker_2.resilient.rollback("auto-read_case")
        show("worker 2 pressure outlets", pressure_outlets(worker_2))
    finally:
        for session in (source, worker_1, worker_2):
            session.exit()


# %%
# Run the demo
# ~~~~~~~~~~~~


def main() -> None:
    """Parse the command line and run the chapters."""
    parser = argparse.ArgumentParser(description="PyFluent CaseSettings demo.")
    parser.add_argument("--auto", action="store_true", help="do not pause")
    parser.add_argument("--no-gui", action="store_true", help="hide the Fluent GUI")
    args = parser.parse_args()
    print(INTRO)
    run("no_gui" if args.no_gui else "gui", args.auto)


if __name__ == "__main__":
    main()
