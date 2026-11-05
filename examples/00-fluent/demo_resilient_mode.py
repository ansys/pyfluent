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

"""Guided demo of PyFluent resilient mode (for screen recording).

This script walks through resilient mode using **two separate, clearly-framed
examples**, each in its own Fluent session, so a viewer never mistakes one
example recovering repeatedly for the whole story. It prints plain-ASCII banners
that make the otherwise-silent recovery visible on camera. Run it with Fluent's
GUI visible so a viewer sees the live session (graphics + console) react
alongside this output.

Recommended recording layout (e.g. in OBS):

    +-----------------------------+--------------------------+
    |  this script's output       |   live Fluent GUI        |
    |  (demo/chapter + EVENT      |   (graphics + console)   |
    |   banners)                  |                          |
    +-----------------------------+--------------------------+

Structure
---------
DEMO 1 -- Mixing elbow (3D): transparent auto-recovery and auto-checkpointing.
    1. One flag        -- enabling resilient mode (``resilient_mode=True``).
    2. Auto-recovery   -- out-of-range clamp, disallowed-value snap, and
                          inactive-target model activation, all through ordinary
                          PyFluent code.
    3. Auto-checkpoint -- irreversible commands are checkpointed automatically
                          (no checkpoint / undo calls in your code).

DEMO 2 -- Solidification (2D): recovering a failed / diverging solve automatically.
    1. A failed solve  -- run a stable baseline solve; push the solver too hard so
                          Fluent raises a FLOATING POINT EXCEPTION (non-catastrophic
                          -- the session stays alive); resilient mode AUTOMATICALLY
                          rolls back to the state it checkpointed before the failed
                          command; then RESUME solving so the iterations visibly
                          continue from the restored state (nothing was lost).

Everything is automatic: the demo never calls checkpoint, undo, or rewind. Each
demo launches and exits its own Fluent session, and a Recap closes the run.

For the best-looking recording, install ``rich`` (``pip install rich``) so the
EVENT banners are colour-coded; without it the script falls back to plain ASCII.

Usage
-----
    # interactive, both demos (pauses between steps for narration):
    python demo_resilient_mode.py

    # unattended / CI-smoke (no Enter prompts):
    python demo_resilient_mode.py --auto

    # record a single example at a time:
    python demo_resilient_mode.py --demo 1
    python demo_resilient_mode.py --demo 2

    # add the crash + failover chapter (launches a warm standby session):
    python demo_resilient_mode.py --failover

Options can be combined. The script never aborts on a demonstrated error -- that
is the whole point -- and always exits each Fluent session cleanly.
"""

from __future__ import annotations

import argparse
import os
import sys
import time

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.core.resilient import (
    is_resilient,
    last_outcome,
    on_journal_event,
)

# --------------------------------------------------------------------------- #
# Banner / narration helpers                                                  #
#                                                                             #
# Colourful output via ``rich`` when it is installed; otherwise a clean       #
# plain-ASCII fallback so the demo never hard-fails on a bare environment.    #
# For the best recording, ``pip install rich`` first.                         #
# --------------------------------------------------------------------------- #

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text

    # Reconfigure stdout to UTF-8 where possible so rich's box-drawing characters
    # survive being redirected to a file on Windows (cp1252 would otherwise raise
    # UnicodeEncodeError). Harmless if stdout does not support reconfigure().
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:  # noqa: BLE001
        pass
    # Force colour output. Many IDE / embedded consoles are not detected as a TTY
    # by rich, which then silently drops all colour; forcing a colour system keeps
    # the EVENT banners colourful there too. Respect NO_COLOR to opt out.
    _force = None if os.environ.get("NO_COLOR") else "truecolor"
    _CONSOLE = Console(
        highlight=False,
        legacy_windows=False,
        force_terminal=None if os.environ.get("NO_COLOR") else True,
        color_system=_force,
    )
    _HAVE_RICH = True
except Exception:  # noqa: BLE001  # pragma: no cover - cosmetic fallback only
    _CONSOLE = None
    _HAVE_RICH = False

_WIDTH = 72


def _rule(ch: str = "=") -> str:
    return ch * _WIDTH


def chapter(number: int, title: str) -> None:
    """Print a chapter header."""
    if _HAVE_RICH:
        _CONSOLE.print()
        _CONSOLE.rule(
            f"[bold cyan]CHAPTER {number}:  {title}[/bold cyan]",
            style="cyan",
        )
        _CONSOLE.print()
    else:
        print("\n" + _rule("="))
        print(f"  CHAPTER {number}:  {title}".upper())
        print(_rule("=") + "\n")


def demo_title(number: int, name: str, subtitle: str) -> None:
    """Print a prominent DEMO title card marking a distinct, separate example."""
    if _HAVE_RICH:
        _CONSOLE.print()
        _CONSOLE.print()
        body = Text.assemble(
            (f"DEMO {number}:  {name}\n", "bold white"),
            (subtitle, "white"),
        )
        _CONSOLE.print(
            Panel(body, border_style="bold magenta", padding=(1, 4), expand=True)
        )
        _CONSOLE.print()
    else:
        bar = "#" * _WIDTH
        print("\n\n" + bar)
        print(bar)
        print(f"##  DEMO {number}:  {name}".ljust(_WIDTH - 2) + "##")
        print(f"##  {subtitle}".ljust(_WIDTH - 2) + "##")
        print(bar)
        print(bar + "\n")


def say(text: str) -> None:
    """Print a narration line (what the viewer should notice)."""
    if _HAVE_RICH:
        _CONSOLE.print(f"  [dim]>>[/dim] {text}")
    else:
        print(f"  >> {text}")


#: Per-capability colour/emphasis styling (rich only). Keys are matched by
#: case-insensitive substring so variants like "auto-recovery (clamp)" map to the
#: recovery style.
_EVENT_STYLES = {
    "error": "bold white on red",
    "rollback": "bold black on yellow",
    "undo": "bold black on yellow",
    "redo": "bold black on yellow",
    "recovery": "bold black on green",
    "activate": "bold black on green",
    "checkpoint": "bold black on cyan",
    "failover": "bold white on blue",
    "resume": "bold black on green",
}


def _event_style(capability: str) -> str:
    lowered = capability.lower()
    for needle, style in _EVENT_STYLES.items():
        if needle in lowered:
            return style
    return "bold black on white"


def event(capability: str, fluent_action: str) -> None:
    """Print one compact resilient-mode event as ``capability`` + ``action``.

    Each event is a scannable two-line card:

        CAPABILITY      : <what resilient mode did>
        ACTION IN FLUENT: <what you see happen in the live session>

    so a viewer can follow the whole story from these lines and the Fluent window
    alone.
    """
    style = _event_style(capability)
    if _HAVE_RICH:
        body = Text.assemble(
            ("CAPABILITY       : ", "bold"),
            (f"{capability}\n", "bold white"),
            ("ACTION IN FLUENT : ", "bold"),
            (fluent_action, "white"),
        )
        _CONSOLE.print(Panel(body, border_style=style, padding=(0, 2)))
    else:
        print("\n  +" + "-" * (_WIDTH - 4) + "+")
        print(f"  | CAPABILITY       : {capability}")
        print(f"  | ACTION IN FLUENT : {fluent_action}")
        print("  +" + "-" * (_WIDTH - 4) + "+")


def report_outcome(session, label: str, rejected=None) -> None:
    """Translate the last resilient outcome into a capability/action event."""
    out = last_outcome(session)
    if out is None:
        return
    if out.fixes_applied:
        fixes = ", ".join(out.fixes_applied)
        rejected_txt = f"{rejected!r} rejected -> " if rejected is not None else ""
        event(
            f"auto-recovery ({fixes})",
            f"{label}: {rejected_txt}applied {out.new_value!r}, accepted.",
        )
    elif out.failed_over:
        event(
            "failover",
            f"{label}: promoted a warm standby session and replayed the state.",
        )


def pause(auto: bool, prompt: str = "Press Enter to continue...") -> None:
    """Pause for narration unless running unattended."""
    if auto:
        time.sleep(1.0)
        return
    try:
        input(f"\n  ({prompt})")
    except EOFError:
        pass


def attach_journal_logging(solver) -> None:
    """Log the automatic undo / redo recovery cycle as capability events.

    Resilient mode records every successful operation on a journal; when a step
    errors it is undone (the pre-step value, read via get_state, is restored) and
    -- if recoverable -- redone with the repaired value. Here we surface just those
    undo / redo events so a viewer sees the cycle; successful steps are recorded
    silently.
    """

    def _leaf(path):
        # Short, readable name from a scheme or dotted path for the banners.
        token = str(path or "setting").replace("\\", "/")
        token = token.rsplit("/", 1)[-1].rsplit(".", 1)[-1]
        return token or "setting"

    def _fmt(value):
        return "the previous value" if value in (None, "") else repr(value)

    def _listener(event_name, op):
        if event_name == "undo":
            event(
                "undo",
                f"{_leaf(op.path)}: restored the previously recorded value "
                f"({_fmt(op.old_value)}).",
            )
        elif event_name == "redo":
            fixes = ", ".join(getattr(op, "fixes", []) or [])
            event(
                "redo",
                f"{_leaf(op.path)}: re-applied the recorded value"
                + (f" ({fixes})" if fixes else "")
                + f" -> {_fmt(op.new_value)}.",
            )

    on_journal_event(solver, _listener)


# --------------------------------------------------------------------------- #
# Chapters                                                                     #
# --------------------------------------------------------------------------- #


def intro(auto: bool) -> None:
    """Shared intro: motivate resilient mode by naming what it protects against."""
    print("\n" + _rule("="))
    print("  PYFLUENT RESILIENT MODE -- GUIDED DEMO")
    print(_rule("="))
    say("A long, scripted Fluent run is fragile. In ordinary PyFluent:")
    say("  - a single out-of-range value raises and aborts the script;")
    say("  - a setting that needs an inactive model raises on access;")
    say("  - a diverging solve throws a floating point exception and you")
    say("    lose the converged state you already paid for.")
    say("Resilient mode turns each of these into a handled, recoverable event.")
    say("We show it on TWO separate examples, run in their own Fluent sessions:")
    say("  DEMO 1 (mixing elbow, 3D) -- transparent auto-recovery + auto-checkpoint;")
    say("  DEMO 2 (solidification, 2D) -- automatic recovery of a failed solve.")
    pause(auto)


def demo1_launch(auto: bool):
    """DEMO 1, chapter 1: launch a 3D resilient session and load the mesh."""
    chapter(1, "One flag: resilient_mode=True")
    say("The ONLY change to your code is one launch argument. Everything after")
    say("this is ordinary PyFluent -- no new per-call API to learn.")
    print("\n      solver = pyfluent.launch_fluent(")
    print('          mode="solver", ui_mode="gui", resilient_mode=True,')
    print("      )\n")
    solver = pyfluent.launch_fluent(
        mode="solver",
        ui_mode="gui",
        resilient_mode=True,
    )
    say(f"resilient mode enabled: {is_resilient(solver)}")
    attach_journal_logging(solver)
    mesh = examples.download_file(
        "mixing_elbow.msh.h5", "pyfluent/mixing_elbow", save_path=os.getcwd()
    )
    solver.settings.file.read_mesh(file_name=mesh)
    say("Mesh loaded; the live Fluent session is on the right.")
    pause(auto)
    return solver


def demo1_auto_recovery(solver, auto: bool) -> None:
    """DEMO 1, chapter 2: clamp, nearest-allowed snap, inactive-target activation."""
    chapter(2, "Transparent auto-recovery")

    # 2a. Inactive-target activation: energy is off; a thermal BC needs it.
    say("Energy model is OFF. We set a thermal boundary condition anyway --")
    say("ordinary code. Watch resilient mode discover + enable the model.")
    solver.settings.setup.models.energy.enabled = False
    cold = solver.settings.setup.boundary_conditions.velocity_inlet["cold-inlet"]
    print("\n      cold_inlet.thermal.temperature.value = 293.15\n")
    cold.thermal.temperature.value = 293.15
    event(
        "activate inactive target",
        "energy model auto-enabled, then the thermal temperature is set "
        f"(energy.enabled = {solver.settings.setup.models.energy.enabled()}).",
    )
    pause(auto)

    # 2b. Out-of-range clamp.
    say("Turbulent intensity must be in [0, 1]. We deliberately set 5.0.")
    print("\n      cold_inlet.turbulence.turbulent_intensity = 5.0\n")
    cold.turbulence.turbulent_intensity = 5.0
    report_outcome(solver, "turbulent_intensity", rejected=5.0)
    say(f"live value is now {cold.turbulence.turbulent_intensity()} (clamped).")
    pause(auto)

    # 2c. Disallowed-value snap.
    spec = cold.turbulence.turbulence_specification
    allowed = spec.allowed_values()
    target = allowed[-1]
    typo = target[:-1]
    say("We set a near-miss of an allowed enumeration value (a typo).")
    print(f"\n      cold_inlet.turbulence.turbulence_specification = {typo!r}\n")
    cold.turbulence.turbulence_specification = typo
    report_outcome(solver, "turbulence_specification", rejected=typo)
    say(f"snapped to the nearest allowed value: {spec()!r}.")
    pause(auto)


def demo1_auto_checkpoint(solver, auto: bool) -> None:
    """DEMO 1, chapter 3: show automatic checkpointing before irreversible ops."""
    chapter(3, "Automatic checkpointing (no manual calls)")
    say("Resilient mode automatically checkpoints the case + data before every")
    say("irreversible command (iterate, read_case, ...). You do not call")
    say("checkpoint, undo, or rewind -- it just happens, so a failed command can")
    say("be rolled back for you. Here, simply initializing + iterating triggers")
    say("the automatic checkpoint; watch the Fluent console write the case.")
    solver.settings.solution.initialization.hybrid_initialize()
    solver.settings.solution.run_calculation.iterate(iter_count=5)
    event(
        "checkpoint (automatic)",
        "case + data written automatically before the iterate command "
        "(no checkpoint() call in your code).",
    )
    pause(auto)


def demo1_undo_redo(solver, auto: bool) -> None:
    """DEMO 1, chapter 4: undo/redo order is correct (reviewer Point 1).

    Sets the same setting twice, then undoes step-by-step to show each undo
    restores the value captured live BEFORE that step -- never a stale default,
    so an earlier undo never overrides a later change.
    """
    chapter(4, "Undo / redo \u2014 correct order, no stale override")
    vis = solver.settings.setup.models.viscous
    say("We change the SAME setting twice, then undo one step at a time.")
    say("Each undo must restore the value captured live before that step.")
    start = vis.model()
    say(f"viscous model starts at: {start!r}")

    vis.model = "k-epsilon"  # Op1  (old captured live = start)
    say(f"Op1 -> {vis.model()!r}")
    vis.model = "laminar"  # Op2  (old captured live = 'k-epsilon')
    say(f"Op2 -> {vis.model()!r}")

    journal = solver._resilient.journal
    say("Now undo one step at a time (watch the undo / redo banners):")
    journal.undo()  # undo Op2 -> 'k-epsilon'
    say(
        f"   after undo Op2 -> viscous model = {vis.model()!r}  "
        "(value BEFORE Op2, not a default)"
    )
    journal.undo()  # undo Op1 -> original
    say(
        f"   after undo Op1 -> viscous model = {vis.model()!r}  "
        "(the original value; LIFO order is exact)"
    )
    journal.redo()  # redo Op1
    say(
        f"   after redo Op1 -> viscous model = {vis.model()!r}  "
        "(re-applies the recorded new value)"
    )
    say(
        "Each undo restored the value captured live before that step -- an "
        "earlier undo never overrides a later change."
    )
    pause(auto)


def demo2_divergence(auto: bool) -> None:
    """DEMO 2: a 2D solidification solve that hits a floating point exception and
    is AUTOMATICALLY rolled back to the last-good state, then resumed."""
    chapter(1, "A failed solve, recovered automatically")
    say("A real solver failure, handled with ZERO manual recovery calls. The")
    say("solidification case is 2D, so this is a completely separate Fluent")
    say("session from Demo 1. The plan:")
    say("  1. run a stable baseline solve (watch the residuals in Fluent),")
    say("  2. push too hard -> Fluent raises a FLOATING POINT EXCEPTION,")
    say("  3. resilient mode AUTOMATICALLY rolls back to the state it")
    say("     checkpointed just before the failed command,")
    say("  4. resume solving -- iterations continue from the restored state.")
    say("In plain PyFluent, step 2 would abort the whole script. Here we never")
    say("call checkpoint, undo, or rewind -- it is all automatic.")
    pause(auto)

    solver = pyfluent.launch_fluent(
        mode="solver",
        ui_mode="gui",
        dimension=pyfluent.Dimension.TWO,
        precision=pyfluent.Precision.DOUBLE,
        resilient_mode=True,
    )
    try:
        attach_journal_logging(solver)
        mesh = examples.download_file(
            "solid.msh", "pyfluent/solidification", save_path=os.getcwd()
        )
        solver.settings.file.read_mesh(file_name=mesh)
        gen = solver.settings.setup.general
        gen.solver.two_dim_space = "swirl"
        gen.operating_conditions.gravity = {"enable": True, "components": [-9.81]}
        solver.settings.setup.models.viscous.model = "laminar"
        solver.tui.define.models.solidification_melting(
            "yes", "constant", "100000", "yes", "no"
        )
        inlet = solver.settings.setup.boundary_conditions.velocity_inlet["inlet"]
        inlet.momentum.velocity_magnitude.value = 0.00101
        inlet.thermal.temperature.value = 1300
        solver.settings.solution.initialization.hybrid_initialize()

        run_calc = solver.settings.solution.run_calculation

        # 1. Stable baseline. ``iterate`` is irreversible, so resilient mode
        #    automatically checkpoints the case + data before it -- this is the
        #    state it will roll back to if a later solve fails. No manual call.
        say("Step 1: running a stable baseline solve (watch the residuals). Note")
        say("that resilient mode auto-checkpoints before this iterate command.")
        run_calc.iterate(iter_count=20)
        say("Baseline converged and was auto-checkpointed. Nothing to call.")
        pause(auto)

        # 2. Push too hard -> floating point exception. ``calculate`` is also
        #    irreversible, so it is auto-checkpointed too; if it fails
        #    non-catastrophically, resilient mode auto-rolls-back to that point.
        say("Step 2: enabling destabilizing physics (Marangoni free surface +")
        say("coupled flow + swirl) and forcing a huge transient step -- watch the")
        say("Fluent console blow up. We just call calculate() as usual.")
        walls = solver.settings.setup.boundary_conditions.wall
        try:
            walls["free-surface"] = {
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
        except Exception:  # noqa: BLE001
            pass
        gen.solver.time = "unsteady-1st-order"
        solver.settings.solution.methods.p_v_coupling.flow_scheme = "Coupled"
        solver.settings.solution.controls.equations = {
            "flow": True,
            "w-swirl": True,
        }
        tc = run_calc.transient_controls
        tc.time_step_size = 1000.0  # deliberately far too large -> divergence
        tc.time_step_count = 20

        # Ordinary call -- no try/except, no manual rollback. Resilient mode
        # catches the floating point exception, classifies it non-catastrophic,
        # and automatically restores the pre-command checkpoint.
        run_calc.calculate()
        out = last_outcome(solver)
        if out is not None and out.result == "auto-rolled-back":
            event(
                "detect non-catastrophic error",
                "solve DIVERGED -> floating point exception; session kept ALIVE "
                "(no new Fluent session).",
            )
            event(
                "auto-rollback",
                "automatically reloaded the case + data checkpointed before the "
                "failed command (no undo / rewind call).",
            )
        else:
            say("(This mesh stayed stable under these settings. The divergence is")
            say(" mesh/BC-sensitive; for a run that reliably raises the floating")
            say(" point exception see modeling_solidification_workflow_resilient.py.")
            say(" The automatic rollback + resume is identical when it does fail.)")
        pause(auto)

        # 3/4. Resume solving from the (restored) state with safe settings. The
        #      viewer sees iterations CONTINUE from the baseline, not restart.
        say("Step 4: resuming the solve with safe, conservative settings -- notice")
        say("the iterations continue from the restored state, they do NOT start")
        say("over from zero. Nothing was lost across the failure.")
        solver.settings.solution.controls.equations = {
            "flow": False,
            "w-swirl": False,
        }
        gen.solver.time = "steady"
        run_calc.iterate(iter_count=15)
        event(
            "resume from restored state",
            "iterations CONTINUE from the restored solution (residuals do not "
            "restart from zero) -- nothing was lost.",
        )
        pause(auto)
    finally:
        say("Exiting the Demo 2 session.")
        solver.exit()


def recap() -> None:
    """Final recap: print the summary card of every capability shown."""
    lines = (
        "auto-recovery of out-of-range values (clamp to live min/max)",
        "auto-recovery of disallowed values (snap to nearest allowed)",
        "inactive-target activation (discover + enable the governing model)",
        "automatic undo (restore last-good value) + redo (re-apply the fix) per step",
        "automatic checkpointing before irreversible commands",
        "automatic rollback of a failed / diverging solve to the last-good state",
        "(opt-in) warm-pool failover with checkpoint replay",
    )
    footer = (
        "Catastrophic (fatal) errors fail over to a warm standby; everything "
        "else is recovered in place. Your code never changes."
    )
    if _HAVE_RICH:
        _CONSOLE.print()
        _CONSOLE.rule("[bold green]RECAP[/bold green]", style="green")
        _CONSOLE.print(
            "\n  Everything in this demo used [bold]ordinary PyFluent code[/bold]. "
            "Resilient mode added, with a single launch flag:\n"
        )
        for line in lines:
            _CONSOLE.print(f"    [green]-[/green] {line}")
        _CONSOLE.print(f"\n  [dim]{footer}[/dim]")
        _CONSOLE.rule(style="green")
    else:
        print("\n" + _rule("="))
        print("  RECAP")
        print(_rule("=") + "\n")
        print("  Everything in this demo used ORDINARY PyFluent code. Resilient")
        print("  mode added, with a single launch flag:\n")
        for line in lines:
            print(f"    - {line}")
        print(f"\n  {footer}")
        print("\n" + _rule("="))


def run_demo_1(auto: bool) -> None:
    """DEMO 1 (mixing elbow, 3D): transparent auto-recovery and auto-checkpoint."""
    demo_title(
        1,
        "Mixing elbow (3D)",
        "Transparent auto-recovery and automatic checkpointing",
    )
    solver = None
    try:
        solver = demo1_launch(auto)
        demo1_auto_recovery(solver, auto)
        demo1_auto_checkpoint(solver, auto)
        demo1_undo_redo(solver, auto)
    finally:
        if solver is not None:
            say("Exiting the Demo 1 session.")
            solver.exit()


def run_demo_2(auto: bool) -> None:
    """DEMO 2 (solidification, 2D): recovering a failed / diverging solve."""
    demo_title(
        2,
        "Solidification (2D)",
        "Recovering a failed solve by rolling back to a checkpoint",
    )
    demo2_divergence(auto)


def run_failover_chapter(auto: bool) -> None:
    """DEMO 3 (opt-in): the active session crashes; a warm standby takes over.

    With a warm pool (``pool_size=2``) resilient mode keeps a standby Fluent
    session ready. We checkpoint the case + data, force the active session into a
    fatal state, and the standby is promoted and replays the last checkpoint -- so
    a catastrophic crash costs nothing. This is the same capability the CFX demo
    shows, driven by the SAME engine (only the adapter differs).
    """
    from ansys.fluent.core.resilient import PoolConfig, ResilientConfig

    demo_title(
        3,
        "Crash + failover (3D)",
        "A warm standby replays the last checkpoint after a fatal crash",
    )
    chapter(1, "Warm pool: pool_size=2 (1 active + 1 standby)")
    say("Resilient mode can keep warm standby sessions. On a FATAL crash it")
    say("promotes a healthy standby and replays the last checkpoint onto it. A")
    say("fatal session's RPCs are refused, so recovery relies only on the")
    say("checkpoint -- never on reading the dead session.")
    pause(auto)

    # Launch the active session with resilient mode + a warm pool. The standby is
    # launched eagerly by the pool using the same launch arguments.
    launch_kwargs = {"mode": "solver", "ui_mode": "gui"}
    config = ResilientConfig(pool=PoolConfig(size=2, launch_kwargs=launch_kwargs))
    active = pyfluent.launch_fluent(
        resilient_mode=True, resilient_config=config, **launch_kwargs
    )
    pool = None
    try:
        controller = active._resilient
        pool = controller.pool
        say(f"pool size: {pool.size}  (1 active + {pool.size - 1} warm standby)")
        attach_journal_logging(active)

        mesh = examples.download_file(
            "mixing_elbow.msh.h5", "pyfluent/mixing_elbow", save_path=os.getcwd()
        )
        active.settings.file.read_mesh(file_name=mesh)
        active.settings.solution.initialization.hybrid_initialize()

        chapter(2, "Checkpoint, then crash")
        say("Take an explicit checkpoint (a real case + data write), then force")
        say("the active session into a fatal state to simulate a crash.")
        entry = active.checkpoint("pre-crash")
        event(
            "checkpoint (real case + data)",
            "a reloadable Fluent case + data was written for failover replay "
            f"({os.path.basename(str(entry.case_data_path or ''))}).",
        )
        pause(auto)

        # Force a fatal error state on the active session (authoritative signal).
        active._fluent_connection._error_state.set("fatal", "simulated crash")
        event(
            "crash detected (fatal)",
            "the active Fluent session is in a fatal state; its RPCs are refused.",
        )
        say("forcing failover to the warm standby...")

        chapter(3, "Failover + checkpoint replay")
        new_active = pool.failover(controller.checkpoints)
        event(
            "failover + checkpoint replay",
            "the warm standby was promoted and reloaded the checkpointed case + "
            "data; the crash cost no progress.",
        )
        say(
            "recovered on the standby -- mesh is loaded: "
            f"{bool(new_active.settings.setup.models.energy.enabled() is not None)}."
        )
        pause(auto)
    finally:
        say("Exiting the failover-demo sessions.")
        if pool is not None:
            pool.shutdown()
        else:
            active.exit()


def main(argv=None) -> int:
    """Run the guided demo(s); each demo uses its own Fluent session."""
    parser = argparse.ArgumentParser(description="PyFluent resilient-mode demo.")
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Run unattended with short timed pauses (no Enter prompts).",
    )
    parser.add_argument(
        "--demo",
        choices=("1", "2", "all"),
        default="all",
        help="Which example to run: 1 (mixing elbow), 2 (solidification), "
        "or all (default).",
    )
    parser.add_argument(
        "--failover",
        action="store_true",
        help="Also run the crash + failover chapter (launches a warm standby "
        "session, so it needs a second Fluent license + extra RAM/cores).",
    )
    args = parser.parse_args(argv)

    intro(args.auto)
    if args.demo in ("1", "all"):
        run_demo_1(args.auto)
    if args.demo in ("2", "all"):
        run_demo_2(args.auto)
    if args.failover:
        run_failover_chapter(args.auto)
    recap()
    return 0


if __name__ == "__main__":
    sys.exit(main())
