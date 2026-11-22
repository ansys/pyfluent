"""End-to-end examples for the staged development of the independent FVM solver.

Run this file from the project root with ``python examples/end_to_end_examples.py``.
The examples are ordered to show the current workflow:

1. Construct mesh, pressure, and staggered velocity fields.
2. Assign boundary conditions to each physical side.
3. Inspect the resulting geometry and field locations.
4. Exercise M2 operators with manufactured fields and compare to exact values.
5. Assemble and solve one M3 momentum-prediction step for cavity setups.
6. Solve the M4 pressure correction and report its compatibility and residual.
7. Apply the M5 correction, update pressure, and check continuity and mass.
8. Run M6 transient steps with a CFL cap and explicit convergence status.
9. Export fields/history and generate M7 plots and Ghia diagnostics.
10. Load a versioned setup-software case through the M8 backend adapter.

The cavity setup examples stop after configuration. The manufactured case
checks M2 operators; M3 solves the momentum predictor; M4 solves pressure
correction; M5 applies it and checks conservation; M6 runs the transient loop;
M7 exports and plots results and evaluates the Ghia profiles. The default M6
run is intentionally short, so its Ghia errors are diagnostic rather than a
claim of benchmark validation. M8 demonstrates the separate setup-software
boundary: a JSON contract is validated, translated, executed, and exported
without importing any setup-framework code.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from fvm import (
    BOUNDARY_NAMES,
    BoundaryConditions,
    CartesianMesh,
    MovingWall,
    MomentumPredictor,
    MomentumPrediction,
    NoSlipWall,
    PressureCorrectionResult,
    PressureCorrectionSolver,
    ProjectionCorrector,
    PythonFVMBackend,
    ScalarField,
    SimulationResult,
    TransientSolver,
    VectorField,
    ZeroGradient,
    convection_operator,
    diffusion_operator,
    divergence,
    compare_ghia_re100,
    export_ghia_comparison,
    export_simulation_result,
    face_gradient,
    interpolate_to_faces,
    plot_cavity_fields,
    plot_convergence_history,
    plot_ghia_comparison,
    velocity_extrema,
)


@dataclass(frozen=True, slots=True)
class ExampleSetup:
    """Mesh, fields, and boundary conditions for one configured example.

    This is a lightweight container for demonstrations, not the versioned case
    input format planned for setup-software integration.
    """

    name: str
    mesh: CartesianMesh
    pressure: ScalarField
    velocity: VectorField
    boundary_conditions: BoundaryConditions


def _cavity_setup(name: str, nx: int, ny: int, lid_velocity: float) -> ExampleSetup:
    """Build the mesh, zero fields, and side conditions for a unit-square cavity.

    All walls are stationary except the north wall when ``lid_velocity`` is
    nonzero. Pressure uses zero-gradient conditions on all sides. These
    conditions are stored here. M3 applies velocity wall values in its
    predictor, while M4/M5 enforce pressure-correction and continuity behavior.
    """
    mesh = CartesianMesh(nx=nx, ny=ny, width=1.0, height=1.0)
    pressure = ScalarField(mesh, name="pressure")
    velocity = VectorField(mesh, name="velocity")
    conditions = BoundaryConditions()

    for side in BOUNDARY_NAMES:
        if side == "north" and lid_velocity != 0.0:
            conditions.set("velocity", side, MovingWall((lid_velocity, 0.0)))
        else:
            conditions.set("velocity", side, NoSlipWall())
        conditions.set("pressure", side, ZeroGradient())

    return ExampleSetup(name, mesh, pressure, velocity, conditions)


def stationary_cavity() -> ExampleSetup:
    """Create a zero-flow baseline with all four walls stationary."""
    return _cavity_setup("stationary cavity", nx=32, ny=32, lid_velocity=0.0)


def lid_driven_cavity_re100() -> ExampleSetup:
    """Create the 64 by 64 Re=100 cavity mesh and boundary setup.

    The Re=100 material values are rho=1 kg/m^3 and mu=0.01 Pa.s. The project
    does not yet define material models, so these values are passed directly to
    the momentum predictor in the M3 example.
    """
    return _cavity_setup("lid-driven cavity Re=100", nx=64, ny=64, lid_velocity=1.0)


def staggered_grid_demonstration() -> ExampleSetup:
    """Create a non-square mesh to make MAC shapes and coordinates visible."""
    mesh = CartesianMesh(nx=4, ny=2, width=2.0, height=1.0)
    pressure = ScalarField(mesh, name="pressure")
    velocity = VectorField(mesh, name="velocity")
    conditions = BoundaryConditions()

    for side in BOUNDARY_NAMES:
        conditions.set("velocity", side, NoSlipWall())
        conditions.set("pressure", side, ZeroGradient())

    return ExampleSetup(
        "rectangular staggered-grid demonstration",
        mesh,
        pressure,
        velocity,
        conditions,
    )


def finite_volume_operator_demonstration() -> None:
    """Run M2 operators and compare each result with its analytic solution.

    The linear field checks interpolation and gradients, ``x^2 + y^2`` checks
    the Laplacian, and ``u=x, v=y`` checks divergence and conservative upwind
    convection of a constant scalar.
    """
    mesh = CartesianMesh(nx=16, ny=12, width=2.0, height=1.5)
    cell_x, cell_y = mesh.cell_center_coordinates
    u_x, u_y = mesh.u_face_coordinates
    v_x, v_y = mesh.v_face_coordinates

    linear = ScalarField(mesh, name="linear")
    linear.set_values(2.0 * cell_x + 3.0 * cell_y)
    linear_boundaries = {
        "west": 3.0 * mesh.y_cell_centers,
        "east": 2.0 * mesh.width + 3.0 * mesh.y_cell_centers,
        "south": 2.0 * mesh.x_cell_centers,
        "north": 2.0 * mesh.x_cell_centers + 3.0 * mesh.height,
    }
    interpolated_x, interpolated_y = interpolate_to_faces(linear, linear_boundaries)
    gradient_x, gradient_y = face_gradient(linear, linear_boundaries)
    interpolation_error = max(
        float(np.max(np.abs(interpolated_x - (2.0 * u_x + 3.0 * u_y)))),
        float(np.max(np.abs(interpolated_y - (2.0 * v_x + 3.0 * v_y)))),
    )
    gradient_error = max(
        float(np.max(np.abs(gradient_x - 2.0))),
        float(np.max(np.abs(gradient_y - 3.0))),
    )

    quadratic = ScalarField(mesh, name="quadratic")
    quadratic.set_values(cell_x**2 + cell_y**2)
    quadratic_boundaries = {
        "west": mesh.y_cell_centers**2,
        "east": mesh.width**2 + mesh.y_cell_centers**2,
        "south": mesh.x_cell_centers**2,
        "north": mesh.x_cell_centers**2 + mesh.height**2,
    }
    laplacian = diffusion_operator(quadratic, boundary_values=quadratic_boundaries)
    laplacian_error = float(np.max(np.abs(laplacian - 4.0)))

    expanding_velocity = VectorField(mesh)
    expanding_velocity.set_values(u_x, v_y)
    velocity_divergence = divergence(expanding_velocity)
    constant = ScalarField(mesh, name="constant", initial_value=2.0)
    convective_divergence = convection_operator(
        constant,
        expanding_velocity,
        scheme="upwind",
        boundary_values={side: 2.0 for side in BOUNDARY_NAMES},
    )
    divergence_error = float(np.max(np.abs(velocity_divergence - 2.0)))
    convection_error = float(np.max(np.abs(convective_divergence - 4.0)))

    print("\nM2 manufactured-field operator demonstration")
    print(f"  interpolation max error for linear field: {interpolation_error:.3e}")
    print(f"  face-gradient max error for linear field: {gradient_error:.3e}")
    print(f"  diffusion max error for x^2 + y^2: {laplacian_error:.3e}")
    print(f"  divergence max error for u=x, v=y: {divergence_error:.3e}")
    print(f"  upwind convection max error for constant scalar: {convection_error:.3e}")


def momentum_prediction_demonstration() -> tuple[MomentumPrediction, ScalarField]:
    """Assemble and solve one momentum predictor step for two cavity cases.

    The stationary case should remain exactly at rest. The lid-driven case
    creates a nonzero intermediate velocity through tangential wall diffusion.
    Neither result has undergone pressure correction, so it is not yet a
    divergence-free Navier-Stokes time step.
    """
    predictor = MomentumPredictor(density=1.0, viscosity=0.01, time_step=0.001)

    stationary = stationary_cavity()
    rest_prediction = predictor.predict(
        stationary.velocity, stationary.pressure, stationary.boundary_conditions
    )

    cavity = lid_driven_cavity_re100()
    assembly = predictor.assemble(cavity.velocity, cavity.pressure, cavity.boundary_conditions)
    lid_prediction = predictor.solve(assembly)

    max_u = float(np.max(np.abs(lid_prediction.velocity.u.values)))
    max_v = float(np.max(np.abs(lid_prediction.velocity.v.values)))
    print("\nM3 one-step momentum prediction")
    print(
        "  stationary cavity max speed: "
        f"{max(np.max(np.abs(rest_prediction.velocity.u.values)), np.max(np.abs(rest_prediction.velocity.v.values))):.3e}"
    )
    print(f"  lid-driven sparse system sizes: {assembly.u_matrix.shape}, {assembly.v_matrix.shape}")
    print(f"  predicted max |u|: {max_u:.3e}; max |v|: {max_v:.3e}")
    print(
        "  relative linear residuals: "
        f"u={lid_prediction.u_relative_residual:.3e}, "
        f"v={lid_prediction.v_relative_residual:.3e}"
    )
    return lid_prediction, cavity.pressure


def pressure_correction_demonstration(
    prediction: MomentumPrediction,
) -> PressureCorrectionResult:
    """Solve M4 for a predictor result, leaving velocity unchanged."""
    solver = PressureCorrectionSolver(density=1.0, time_step=0.001)
    assembly = solver.assemble(prediction.velocity)
    result = solver.solve(assembly)
    divergence_before = divergence(prediction.velocity)

    print("\nM4 pressure-correction solve")
    print(f"  net outward boundary flux: {result.net_boundary_flux:.3e}")
    print(f"  max predicted divergence: {np.max(np.abs(divergence_before)):.3e}")
    print(f"  max |pressure correction|: {np.max(np.abs(result.correction.values)):.3e}")
    print(f"  relative linear residual: {result.relative_residual:.3e}")
    print("  predicted velocity is unchanged by the pressure solve")
    return result


def velocity_correction_demonstration(
    prediction: MomentumPrediction,
    pressure: ScalarField,
    pressure_correction: PressureCorrectionResult,
) -> None:
    """Apply M5 and report divergence and global mass before/after correction."""
    corrector = ProjectionCorrector(density=1.0, time_step=0.001)
    result = corrector.project(prediction.velocity, pressure, pressure_correction)

    print("\nM5 velocity and pressure correction")
    print(f"  max divergence before: {result.max_divergence_before:.3e}")
    print(f"  max divergence after: {result.max_divergence_after:.3e}")
    print(f"  global mass imbalance: {result.global_mass_imbalance:.3e}")
    print(f"  max |updated pressure|: {np.max(np.abs(result.pressure.values)):.3e}")


def transient_simulation_demonstration() -> SimulationResult:
    """Run M6 on a rest case and a short, deliberately bounded cavity case."""
    stationary = stationary_cavity()
    stationary_solver = TransientSolver(
        density=1.0,
        viscosity=0.01,
        max_time_step=0.01,
        max_steps=5,
    )
    rest_result = stationary_solver.run(
        stationary.velocity,
        stationary.pressure,
        stationary.boundary_conditions,
    )

    cavity = lid_driven_cavity_re100()
    cavity_solver = TransientSolver(
        density=1.0,
        viscosity=0.01,
        max_time_step=0.001,
        max_steps=3,
        cfl_limit=0.5,
        velocity_tolerance=1e-14,
    )
    cavity_result = cavity_solver.run(
        cavity.velocity,
        cavity.pressure,
        cavity.boundary_conditions,
    )
    final_step = cavity_result.history[-1]

    print("\nM6 transient execution")
    print(
        "  stationary cavity: "
        f"{rest_result.termination_reason} after {rest_result.steps} step(s), "
        f"max divergence={rest_result.history[-1].max_divergence_after:.3e}"
    )
    print(
        f"  lid-driven cavity: {cavity_result.termination_reason} after "
        f"{cavity_result.steps} steps, t={cavity_result.final_time:.3e} s"
    )
    print(
        f"  last step dt={final_step.time_step:.3e} s, CFL={final_step.cfl_number:.3f}, "
        f"velocity change={final_step.velocity_change:.3e} m/s"
    )
    print(
        f"  max divergence={final_step.max_divergence_after:.3e}, "
        f"global mass imbalance={final_step.global_mass_imbalance:.3e}"
    )
    return cavity_result


def postprocessing_demonstration(simulation: SimulationResult) -> None:
    """Export the run and generate field, profile, and convergence visuals."""
    output_directory = Path("results") / "m7_preview"
    comparison = compare_ghia_re100(simulation)
    extrema = velocity_extrema(simulation.velocity)

    export_simulation_result(simulation, output_directory)
    export_ghia_comparison(comparison, output_directory / "ghia_re100.json")
    plot_cavity_fields(simulation, output_directory / "fields.png")
    plot_ghia_comparison(comparison, output_directory / "ghia_profiles.png")
    plot_convergence_history(simulation, output_directory / "convergence.png")

    print("\nM7 post-processing")
    print(f"  benchmark eligible: {comparison.benchmark_valid}")
    print(
        f"  Ghia Re=100 centerline RMS: u={comparison.u_rms_error:.3e}, "
        f"v={comparison.v_rms_error:.3e}"
    )
    print(
        f"  max cell-centered speed: {extrema.maximum_speed:.3e} m/s at "
        f"({extrema.maximum_speed_location[0]:.3f}, "
        f"{extrema.maximum_speed_location[1]:.3f}) m"
    )
    print(f"  fields, metadata, history, reports, and plots: {output_directory}")
    print("  grid study API: run_lid_driven_grid_study() for 16/32/64/128 cells")


def setup_backend_integration_demonstration() -> None:
    """Run the canonical JSON case through the setup-facing M8 backend."""
    case_path = Path("cases") / "lid_driven_cavity_re100.json"
    output_directory = Path("results") / "m8_backend"
    run = PythonFVMBackend().run_file(case_path, output_directory)

    print("\nM8 setup-software backend integration")
    print(f"  case ID: {run.case_id}; schema: {run.summary['schema_version']}")
    print(
        f"  backend: {run.summary['backend']}; status: {run.summary['status']}; "
        f"Re={run.summary['reynolds_number']:.1f}"
    )
    print(f"  solver artifacts: {run.artifact_directory}")


def _describe(example: ExampleSetup) -> None:
    """Print the mesh, array shapes, and stored velocity boundary conditions."""
    mesh = example.mesh
    print(f"\n{example.name}")
    print(f"  domain: {mesh.width:g} m x {mesh.height:g} m")
    print(f"  cells: {mesh.nx} x {mesh.ny}; total area: {mesh.cell_areas.sum():g} m^2")
    print(f"  pressure shape: {example.pressure.values.shape}")
    print(f"  u shape: {example.velocity.u.values.shape}")
    print(f"  v shape: {example.velocity.v.values.shape}")
    print(f"  velocity boundaries: {dict(example.boundary_conditions.for_field('velocity'))}")

    if example.name == "rectangular staggered-grid demonstration":
        cell_x, cell_y = mesh.cell_center_coordinates
        u_x, u_y = mesh.u_face_coordinates
        v_x, v_y = mesh.v_face_coordinates
        print(f"  first pressure center: ({cell_x[0, 0]:g}, {cell_y[0, 0]:g}) m")
        print(f"  first u location: ({u_x[0, 0]:g}, {u_y[0, 0]:g}) m")
        print(f"  first v location: ({v_x[0, 0]:g}, {v_y[0, 0]:g}) m")


def main() -> None:
    """Run setup, solver stages, post-processing, and M8 backend integration.

    Future end-to-end solver examples should follow the same readable order:
    construct case, inspect fields, execute the supported numerical steps, and
    report verification quantities.
    """
    examples = (
        stationary_cavity(),
        lid_driven_cavity_re100(),
        staggered_grid_demonstration(),
    )
    for example in examples:
        _describe(example)

    # Keep numerical verification after setup output so each example's inputs
    # are visible before its computed operator checks.
    finite_volume_operator_demonstration()
    prediction, pressure = momentum_prediction_demonstration()
    pressure_correction = pressure_correction_demonstration(prediction)
    velocity_correction_demonstration(prediction, pressure, pressure_correction)
    simulation = transient_simulation_demonstration()
    postprocessing_demonstration(simulation)
    setup_backend_integration_demonstration()
    print("\nRun the full grid-refinement study separately when ready for validation.")


if __name__ == "__main__":
    main()