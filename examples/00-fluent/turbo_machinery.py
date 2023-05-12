""".. _xxx:

Turbomachinery Setup and Analysis Using the Turbo Workflow
----------------------------------------------------------
This example sets up and solves a three-dimensional fluid flow through the
first three rows of a one and a half stage axial compressor, courtesy of
TFD Hannover. The compressor configuration is encountered in the aerospace
and turbomachinery industry. It is often important to predict the flow field
through the various components of a compressor in order to properly design
the turbomachine.

This example uses the guided workflow for turbomachinery setup and analysis
because it is appropriate for describing the type of turbo machine and its
configuration, importing the geometry, and defining turbo-related mappings
and physics conditions, before finally creating a turbo-specific topology
and reporting tools.

**Workflow tasks**

The Turbomachinery Setup and Analysis Using the Turbo Workflow guides you through these tasks:

- Describe and configure the turbomachinery
- Import the turbo-specific geometry
- Define the turbo-related mappings and physics conditions
- Create turbo-specific topology and reporting tools for postprocessing

**Problem description**

The first three rows of the 4.5 stage axial Hannover compressor (Courtesy of TFD Hannover) have an
inlet guide vane, rotor and stator. The inlet guide vane has 26 vanes, the rotor has 23 blades and
rotates at a velocity of 17,100 RPM and the stator has 30 passages. The total pressure at the inlet
is 60,000 Pa and a radial equilibrium distribution of static pressure at the outlet, with a static
pressure of 60500 Pa at the outlet along the hub.
"""
