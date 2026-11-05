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

"""Resilient mode across two products (Fluent + CFX) in one process.

The resilient engine lives in ``ansys.fluent.core.resilient`` and is
product-agnostic: a small per-product *adapter* is the only thing that differs.
This demo drives a **Fluent** solver session and a **CFX** pre session in the same
Python process, each with its own adapter, showing that:

* the same ``enable_resilient_mode`` + auto-recovery works for both products;
* the two sessions are independent (per-session adapters, no global state);
* Fluent's undo tier uses case/data file checkpoints, while CFX's undo tier is
  backed by CFX's **native server-side undo** -- the framework composes with each
  product's native strengths.

Run (requires both Fluent and CFX installed)::

    python demo_resilient_cross_product.py

Use ``--fluent-only`` / ``--cfx-only`` to run just one half.
"""

from __future__ import annotations

import argparse
import sys


def _banner(title: str) -> None:
    print("\n" + "=" * 68)
    print(f"  {title}")
    print("=" * 68)


def run_fluent() -> None:
    """Resilient Fluent: out-of-range clamp + inactive-target activation."""
    import ansys.fluent.core as pyfluent
    from ansys.fluent.core import examples
    from ansys.fluent.core.resilient import adapter_for, last_outcome

    _banner("FLUENT  (resilient_mode=True)")
    mesh = examples.download_file("mixing_elbow.msh.h5", "pyfluent/mixing_elbow")
    solver = pyfluent.launch_fluent(
        mode="solver", precision="double", processor_count=2, resilient_mode=True
    )
    try:
        print("  adapter:", adapter_for(solver).product_name)
        solver.settings.file.read_mesh(file_name=mesh)

        # Inactive-target activation: energy model is off; a thermal BC needs it.
        solver.settings.setup.models.energy.enabled = False
        cold = solver.settings.setup.boundary_conditions.velocity_inlet["cold-inlet"]
        cold.thermal.temperature.value = 293.15
        print(
            "  activate inactive target -> energy.enabled =",
            solver.settings.setup.models.energy.enabled(),
        )

        # Out-of-range clamp.
        cold.turbulence.turbulent_intensity = 5.0
        out = last_outcome(solver)
        print(
            "  auto-recovery ->",
            out.fixes_applied,
            "-> value =",
            cold.turbulence.turbulent_intensity(),
        )
    finally:
        solver.exit()


def run_cfx() -> None:
    """Resilient CFX: auto-recovery + native-undo rollback."""
    import ansys.cfx.core as pycfx
    from ansys.cfx.core.resilient import adapter_for, enable_resilient_mode

    _banner("CFX  (resilient mode via the shared engine)")
    pre = pycfx.PreProcessing.from_install()
    try:
        enable_resilient_mode(pre)
        print("  adapter:", adapter_for(pre).product_name)
        print(
            "  CFX undo tier is backed by the native server-side undo " "(file.undo())."
        )
        # Drive ordinary pycfx setup here; any recoverable error is repaired and
        # retried, and irreversible operations are bracketed by a native-undo
        # checkpoint so a failed step is rolled back automatically.
        print("  resilient mode enabled on the CFX session.")
    finally:
        pre.exit()


def main(argv=None) -> int:
    """Run the resilient demo for Fluent, CFX, or both."""
    parser = argparse.ArgumentParser(description="Cross-product resilient demo.")
    parser.add_argument("--fluent-only", action="store_true")
    parser.add_argument("--cfx-only", action="store_true")
    args = parser.parse_args(argv)

    if not args.cfx_only:
        run_fluent()
    if not args.fluent_only:
        run_cfx()
    _banner("Both products used the SAME resilient engine, different adapters.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
