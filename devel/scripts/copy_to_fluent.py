"""Script to copy PyFluent files to Fluent and print Fluent Manifest."""

import argparse
import os
from pathlib import Path
import shutil

parser = argparse.ArgumentParser(
    description="Copy Pyfluent files to Fluent and print Fluent Manifest"
)
parser.add_argument(
    "--pyfluent-path",
    dest="pyfluent_path",
    type=str,
    help="Path to site-packages directory containing pyfluent",
    required=True,
)
parser.add_argument(
    "--fluent-path",
    dest="fluent_path",
    type=str,
    help="Path to Fluent git repository",
    required=True,
)

args = parser.parse_args()
pyfluent_core_src = Path(args.pyfluent_path) / "ansys" / "fluent" / "core"
pyfluent_core_dst = (
    Path(args.fluent_path)
    / "fluent"
    / "cortex"
    / "pylib"
    / "pyfluent"
    / "ansys"
    / "fluent"
    / "core"
)

# First, copy PyFluent's ansys/fluent/core directory to the Fluent repository
# We need update this in future when we include more pyfluent-related libraries like visualization
if pyfluent_core_dst.exists():
    shutil.rmtree(pyfluent_core_dst)
shutil.copytree(pyfluent_core_src, pyfluent_core_dst)

# Next, remove all __pycache__ directories from the copied files
for root, dirs, files in os.walk(pyfluent_core_dst):
    for dir in dirs:
        if dir == "__pycache__":
            shutil.rmtree(Path(root) / dir)

# Remove some unnecessary data files
(pyfluent_core_dst / "codegen" / "data" / "static_info_222_meshing.pickle").unlink()
(pyfluent_core_dst / "codegen" / "data" / "static_info_222_solver.pickle").unlink()

# Finally, print the Fluent manifest code of the copied files.
# Copy and replace this output in the following section in packageManifest/cortex/manifest.pkg in Fluent repository
# # PyFluent sources START
# <manifest code>
# # PyFluent sources END

prefix = "fluent/fluentRampantReleaseMajor.RampantReleaseMinor.RampantReleaseRevision/cortex/pylib/pyfluent/ansys/fluent/core"
for root, dirs, files in os.walk(pyfluent_core_dst):
    root_path = Path(root)
    if root_path.name == "__pycache__":
        continue
    for file in files:
        file_path = root_path / file
        rel_path = file_path.relative_to(pyfluent_core_dst).as_posix()
        print(f"{prefix}/{rel_path}")
