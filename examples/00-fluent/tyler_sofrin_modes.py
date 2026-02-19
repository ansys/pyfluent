# /// script
# dependencies = [
#   "matplotlib",
#   "numpy",
#   "ansys-fluent-core",
# ]
# ///

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

""".. _ref_ts_mode_calculator:

Tyler-Sofrin Compressor Modes Post-Processing
---------------------------------------------
"""

#######################################################################################
# Objective
# ~~~~~~~~~
#
# This example demonstrates PyFluent API's for
#
# * Read a case and data file
# * Create monitor points to calculate Fourier coefficients
# * Write Fourier coefficients to a file
# * Tyler-Sofrin mode Plot using the matplotlib library
#
# Background
# ~~~~~~~~~~
#
# Tyler and Sofrin (1961) demonstrated that interactions between a rotor and a
# stator result in an infinite set of spinning modes. Each Tyler-Sofrin (TS)
# mode exhibits an m-lobed pattern and rotates at a speed given by the
# following equation:
#
# :math:`\text{speed} = \frac{BnΩ}{m}`
# Where:
#
# * m is the Tyler-Sofrin mode number, defined as 'm = nB + kV'
# * n is the impeller frequency harmonic
# * k is the vane harmonic
# * B is the number of rotating blades
# * V is the number of stationary vanes
# * Ω is the Rotor shaft speed, rad/s
#
# Example:
#
#         * 8-blade rotor interacting with a 6-vane stator
#         * 2-lobed pattern turning at (8)(1)/(2) = 4 times shaft speed
#
#
# Example Table
# ~~~~~~~~~~~~~
#
# .. image:: ../../_static/ExampleTable.jpg
#    :alt: Example Table
#
#
# Tyler-Sofrin Modes
# ~~~~~~~~~~~~~~~~~~
#
# .. image:: ../../_static/TSmode.jpg
#    :alt: Tyler-Sofrin Modes


#######################################################################################
# Example Note: Discrete Fourier Transform (DFT)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   + In order to calculate the pressure related to each TS-mode, extend the
#     simulation and perform the DFT of pressure at the desired blade passing
#     frequency harmonics.
#
#   + Disable the Hanning windowing (specifically for periodic flows like
#     this one) to avoid getting half the expected magnitudes for periodic flows.
#     Make sure to set the windowing parameter to 'None' when specifying
#     the Discrete Fourier Transform (DFT) in the graphical user interface (GUI).
#
#   + The DFT data will only be accurate if the sampling is done across the
#     entire specified sampling period.
#
#
# .. note::
#   The .cas/.dat file provided with this example is for demonstration purposes only.
#   A finer mesh is necessary for accurate acoustic analysis. This example uses data
#   sets generated with Ansys Fluent V2023R2.

#######################################################################################
# Post-Processing Implementation
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#######################################################################################
# Import required libraries/modules
# =====================================================================================
import csv
import math
from pathlib import Path
import random

import matplotlib.pyplot as plt
import numpy as np

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.core.solver import PointSurface, ReportDefinitions, read_case_data
from ansys.units.common import m

#######################################################################################
# Downloading cas/dat file
# =====================================================================================
import_filename = examples.download_file(
    "axial_comp_fullWheel_DFT_23R2.cas.h5",
    "pyfluent/examples/Tyler-Sofrin-Modes-Compressor",
    save_path=Path.cwd(),
)

examples.download_file(
    "axial_comp_fullWheel_DFT_23R2.dat.h5",
    "pyfluent/examples/Tyler-Sofrin-Modes-Compressor",
    save_path=Path.cwd(),
)

#######################################################################################
# Launch Fluent session and print Fluent version
# =====================================================================================
solver = pyfluent.Solver.from_install(processor_count=4)
print(solver.get_fluent_version())

#######################################################################################
# Reading case and data file
# =====================================================================================
#
# .. note::
#   The dat file should correspond to the already completed DFT simulation.
read_case_data(solver, file_name=import_filename)

#######################################################################################
# Define User constant/variables
# =====================================================================================
#
# .. note::
#   The variable names should match the ones written from the DFT and can be
#   identified by manually examining the solution variables as shown below:
#
# .. image:: ../../_static/var_names.jpg
#    :alt: variable names

var_names = [
    "mean-static-pressure-dataset",
    "dft-static-pressure_10.00kHz-ta",
    "dft-static-pressure-1_21.43kHz-ta",
    "dft-static-pressure-2_30.00kHz-ta",
]
n_mode = [0, 1, 2, 3]  # Impeller frequency harmonics
r = 0.082 * m
z = -0.037 * m
d_theta = 5  # degrees
m_max = 50  # maximum TS mode number

# Plot will be from -m_max to +m_max, incremented by m_inc
m_inc = 2  # TS mode increment

#######################################################################################
# Create monitor points
# =====================================================================================
for angle in range(0, 360, d_theta):
    x = math.cos(math.radians(angle)) * r
    y = math.sin(math.radians(angle)) * r
    PointSurface.create(solver, name=f"point-{angle}", point=(x, y, z))

#######################################################################################
# Compute Fourier coefficients at each monitor point (An, Bn)
# =====================================================================================
An = np.zeros((len(var_names), int(360 / d_theta)))
Bn = np.zeros((len(var_names), int(360 / d_theta)))
report_defs = ReportDefinitions(solver)

for angle_ind, angle in enumerate(range(0, 360, d_theta)):
    for n_ind, variable in enumerate(var_names):
        if variable.startswith("mean"):
            mag_report = report_defs.surface.create(
                name="mag-report",
                report_type="surface-vertexavg",
                surface_names=[f"point-{angle}"],
                field=variable,
            )
            mag_res = report_defs.compute(report_defs=[mag_report])
            mag = mag_res[0][mag_report.name][0]
            An[n_ind][angle_ind] = mag
            Bn[n_ind][angle_ind] = 0
        else:
            mag_report = report_defs.surface.create(
                name="mag-report",
                report_type="surface-vertexavg",
                surface_names=[f"point-{angle}"],
                field=f"{variable}-mag",
            )
            mag_res = report_defs.compute(report_defs=[mag_report])
            mag = mag_res[0][mag_report.name][0]
            phase_report = report_defs.surface.create(
                name="phase-report",
                report_type="surface-vertexavg",
                surface_names=[f"point-{angle}"],
                field=f"{variable}-phase",
            )
            phase_res = report_defs.compute(report_defs=[phase_report])
            phase = phase_res[0][phase_report.name][0]
            An[n_ind][angle_ind] = mag * math.cos(phase)
            Bn[n_ind][angle_ind] = -mag * math.sin(phase)


#######################################################################################
# Write Fourier coefficients to file
# =====================================================================================
#
# .. note::
#   This step is only required if data is to be processed with other standalone
#   tools. Update the path to the file accordingly.

with (Path.cwd() / "FourierCoefficients.csv").open("w") as f:
    writer = csv.writer(f)
    writer.writerow(["n", "theta", "An", "Bn"])

    for n_ind, variable in enumerate(var_names):
        for ind, _ in enumerate(An[n_ind, :]):
            writer.writerow(
                [n_mode[n_ind], ind * d_theta, An[n_ind, ind], Bn[n_ind, ind]]
            )

#######################################################################################
# Calculate Resultant Pressure Field
# =====================================================================================
#
# Create list of m values based on m_max and m_inc
#
# .. image:: ../../_static/TS_formulas.jpg
#    :alt: variable names

m_mode = range(-m_max, m_max + m_inc, m_inc)

# Initialize solution matrices with zeros
Anm = np.zeros((len(var_names), len(m_mode)))
Bnm = np.zeros((len(var_names), len(m_mode)))
Pnm = np.zeros((len(var_names), len(m_mode)))

for n_ind, variable in enumerate(var_names):  # loop over n modes
    for m_ind, _m in enumerate(m_mode):  # loop over m modes
        for angle_ind, angle in enumerate(
            np.arange(0, math.radians(360), math.radians(d_theta))
        ):  # loop over all angles, in radians
            Anm[n_ind][m_ind] += (  # fmt: skip
                An[n_ind][angle_ind] * math.cos(_m * angle)
                - Bn[n_ind][angle_ind] * math.sin(_m * angle)
            )
            Bnm[n_ind][m_ind] += (  # fmt: skip
                An[n_ind][angle_ind] * math.sin(_m * angle)
                + Bn[n_ind][angle_ind] * math.cos(_m * angle)
            )
        Anm[n_ind][m_ind] = Anm[n_ind][m_ind] / (2 * math.pi) * math.radians(d_theta)
        Bnm[n_ind][m_ind] = Bnm[n_ind][m_ind] / (2 * math.pi) * math.radians(d_theta)
        Pnm[n_ind][m_ind] = math.sqrt(Anm[n_ind][m_ind] ** 2 + Bnm[n_ind][m_ind] ** 2)

# P_00 is generally orders of magnitude larger than that of other modes.
# Giving focus to other modes by setting P_00 equal to zero
Pnm[0][int(len(m_mode) / 2)] = 0

#######################################################################################
# Plot Tyler-Sofrin modes
# =====================================================================================
#
fig = plt.figure()
ax = plt.axes(projection="3d")
ax.set_xlabel("Tyler-Sofrin Mode, m")
ax.set_ylabel("Imp Freq Harmonic, n")
ax.set_zlabel("Pnm [Pa]")
plt.yticks(n_mode)
for n_ind, n in enumerate(n_mode):
    x = m_mode
    y = np.full(Pnm.shape[1], n)
    z = Pnm[n_ind]
    rgb = (random.random(), random.random(), random.random())
    ax.plot3D(x, y, z, c=rgb)
plt.show()

#######################################################################################
# Tyler-Sofrin modes
# =====================================================================================
# .. image:: ../../_static/ts_modes.png
#    :alt: Tyler-Sofrin modes


#######################################################################################
# Close the session
# =====================================================================================
solver.exit()


#######################################################################################
# References
# =====================================================================================
#
# [1] J.M. Tyler and  T. G. Sofrin, Axial Flow Compressor Noise Studies,1961 Manly
# Memorial Award.

# sphinx_gallery_thumbnail_path = '_static/ts_modes.png'
