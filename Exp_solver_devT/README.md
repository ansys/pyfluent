# Independent FVM Reference

This project is a small, independent numerical reference implementation for
validating CFD problem-setup software. It is not intended to become a
production CFD solver. The design prioritizes understandable discretization,
repeatable results, and tests that isolate numerical behavior.

For step-by-step setup, execution, output interpretation, and post-processing,
start with the [solver user guide](docs/using_the_solver.md).

The initial benchmark is the two-dimensional incompressible lid-driven cavity:
a 1 m by 1 m domain, density 1 kg/m^3, dynamic viscosity 0.01 Pa.s, a top-lid
speed of 1 m/s, and Reynolds number 100. The solution will be advanced in time
from rest toward steady state.

## Numerical Approach

- Finite Volume Method on a uniform Cartesian grid.
- Staggered MAC storage: pressure at cell centers, `u` on vertical faces, and
    `v` on horizontal faces.
- Transient projection method for pressure-velocity coupling.
- Explicit convection and implicit diffusion for the initial momentum
    predictor, subject to stability and verification tests.
- SciPy sparse matrices and direct solves for the momentum predictor.

For `nx` by `ny` cells, arrays use NumPy `(row, column)` order:

| Quantity | Shape | Location |
| --- | --- | --- |
| Pressure / cell scalar | `(ny, nx)` | Cell centers |
| `u` velocity | `(ny, nx + 1)` | Vertical faces |
| `v` velocity | `(ny + 1, nx)` | Horizontal faces |

The first array index is the y/row index; the second is the x/column index.
Coordinate properties return `(x, y)` arrays matching their associated field.
At the moving-lid corners, the lid and side-wall conditions meet
discontinuously; those corners will not be treated as ordinary smooth
benchmark points.

## Milestone Status

| Milestone | Scope | Status |
| --- | --- | --- |
| M1 | Mesh, staggered fields, and boundary-condition storage | Complete |
| M2 | Finite-volume operators and manufactured-solution tests | Complete |
| M3 | Momentum prediction and sparse equation assembly | Complete |
| M4 | Pressure-correction Poisson equation | Complete |
| M5 | Velocity correction and continuity checks | Complete |
| M6 | Transient execution, time-step control, and convergence | Complete |
| M7 | Post-processing and cavity benchmark validation | Complete |
| M8 | Setup-software input/output integration | Complete |
| M9 | Checkpointing and restartable solver state | Complete |

The checklists below are the implementation record. They will be updated as
each milestone is implemented and verified.

### M1 - Mesh and Data Structures - Complete

- [x] Generate uniform Cartesian geometry and cell/face coordinates.
- [x] Store cell-centered scalar fields and staggered `u` and `v` fields.
- [x] Expose cell and face areas, boundary-face indices, counts, and normals.
- [x] Define fixed-value, zero-gradient, stationary-wall, and moving-wall
    boundary conditions and store them by field and boundary.
- [x] Verify dimensions, indexing, coordinates, areas, invalid inputs, and a
    64 by 64 cavity setup with unit tests.

Boundary conditions are stored by field and side. The M3 momentum predictor
consumes velocity wall conditions, and M4 applies homogeneous-Neumann pressure
correction boundaries. A general boundary-condition application framework is
not yet part of the solver.

### M2 - Finite-Volume Operators - Complete

- [x] Implement cell-to-face central interpolation and face pressure/scalar
    gradients.
- [x] Implement finite-volume velocity divergence and conservative face-flux
    divergence.
- [x] Implement constant-diffusivity fluxes and the cell-centered diffusion
    operator.
- [x] Implement central and first-order upwind scalar convection fluxes.
- [x] Verify constant, linear, and quadratic manufactured fields, upwind
    direction, conservation, and grid-refinement accuracy.

The public operators are in [`src/fvm/operators.py`](src/fvm/operators.py).
`interpolate_to_faces` uses arithmetic averages internally and nearest-cell
extrapolation at boundaries unless side values are supplied. `face_gradient`
uses homogeneous Neumann values by default; supplied Dirichlet face values use
one-sided reconstruction at boundaries. Diffusion and convection return
cell-centered flux divergences. Convection supports `central` and `upwind`
schemes, with upwind as the default. Inflow boundary values should be supplied
for convection when the nearest-cell fallback is not the intended physical
condition.

The operators have unit tests and manufactured-solution checks, but they are
not yet assembled into momentum or pressure equations.

### M3 - Momentum Prediction - Complete

- [x] Define and test sparse finite-volume matrix assembly and source terms.
- [x] Assemble the `u` and `v` momentum equations using transient storage,
    explicit upwind convection, implicit diffusion, and pressure-gradient sources.
- [x] Apply velocity wall values at the matching normal faces and tangential
    control-volume boundaries.
- [x] Verify matrix coefficients and solve stationary, pressure-driven, and
    moving-lid cases.

[`src/fvm/momentum.py`](src/fvm/momentum.py) provides `MomentumPredictor`.
Call `assemble` to inspect the two CSR matrices, right-hand sides, explicit
convection terms, and pressure gradients; call `solve` for a new predicted
`VectorField` and normalized linear residuals. The interior unknown shapes are
`u: (ny, nx - 1)` and `v: (ny - 1, nx)` because boundary-aligned normal
velocities are prescribed directly.

The predictor solves one momentum step only. It accepts the current
cell-centered pressure and does not compute pressure correction, enforce
post-projection continuity, or run a time loop. Convection is first-order
upwind and explicit; viscous diffusion is implicit with wall contributions in
the RHS. The moving lid's tangential speed enters the adjacent `u` control
volumes, while wall-normal components are fixed on boundary-aligned faces.

### M4 - Pressure-Correction Equation - Complete

- [x] Assemble the finite-volume pressure-correction Poisson equation from
    predicted face-velocity divergence.
- [x] Apply homogeneous Neumann pressure-correction conditions at impermeable
    walls.
- [x] Check global boundary-flux compatibility and fix the pressure nullspace
    using a configurable reference cell.
- [x] Verify sparse coefficients, known-solution recovery, compatibility
    rejection, and the linear residual.

[`src/fvm/pressure_correction.py`](src/fvm/pressure_correction.py) provides
`PressureCorrectionSolver`. Its positive-system convention is
`-laplacian(p') = -(rho / dt) * div(u*)`. The Neumann boundary contributes no
normal correction flux; the reference-cell equation is replaced by
`p'(reference) = 0`. Before assembly, the solver checks that predicted velocity
has zero net outward boundary flux within the configured tolerance. It reports
incompatible flux instead of silently adjusting the RHS. `solve` returns a
cell-centered correction and normalized sparse residual; it deliberately does
not alter velocity, which is the M5 step.

### M5 - Velocity Correction and Conservation - Complete

- [x] Correct interior face velocities using the pressure correction.
- [x] Use the same two-point pressure gradient represented by the M4
    five-point Poisson matrix.
- [x] Update physical pressure and report cell divergence and global mass
    imbalance.
- [x] Verify continuity reduction and unchanged wall-normal velocities.

[`src/fvm/projection.py`](src/fvm/projection.py) provides
`ProjectionCorrector`. It applies `u = u* - dt/rho grad(p')` on interior MAC
faces, preserves boundary-normal values for homogeneous-Neumann pressure
correction, updates pressure as `p + p'`, and returns before/after divergence
fields plus the integrated global mass imbalance. The pressure matrix uses
two-point differences, so the corrector deliberately uses that same stencil
rather than the higher-order general-purpose M2 `face_gradient` operator.
Velocity and pressure inputs are left unchanged.

### M6 - Transient Solver and Convergence - Complete

- [x] Run momentum prediction, pressure solve, and projection in a documented
    per-step order.
- [x] Limit each step with an explicit-convection CFL estimate, including
    moving-wall speeds; diffusion is implicit and adds no explicit limit.
- [x] Record time step, CFL, velocity change, momentum/pressure residuals,
    cell divergence, and global mass imbalance.
- [x] Require configured steady, continuity, mass, and linear-solver
    tolerances to converge; report maximum-step termination otherwise.
- [x] Verify that the stationary zero-flow cavity converges without developing
    motion.

[`src/fvm/simulation.py`](src/fvm/simulation.py) provides `TransientSolver`.
`max_time_step` is a cap, with each step additionally constrained by
`dt * (max|u|/dx + max|v|/dy) <= cfl_limit`. The solver records immutable
`StepDiagnostics` entries and returns final fields, convergence state, reason,
and history. Steady state requires velocity change, post-projection maximum
divergence, global mass imbalance, both momentum residuals, and pressure
residual to meet their respective tolerances. `maximum_steps_reached` is an
explicit non-converged result rather than an implicit success.

M7 adds the tools for Ghia comparison and grid studies. A run is benchmark-valid
only when it meets the convergence criteria; the short example is for
demonstration and is explicitly marked diagnostic.

### M7 - Post-Processing and Benchmark Validation - Complete

- [x] Export staggered and cell-centered velocity, pressure, mesh, run settings,
    and convergence history.
- [x] Interpolate MAC fields to both geometric centerlines and compare all
    interior Re=100 samples with Ghia et al.
- [x] Exclude wall endpoints, including the discontinuous lid corners, from RMS
    comparisons.
- [x] Report centerline RMS errors, component/speed extrema, divergence, and
    global mass imbalance.
- [x] Add an opt-in 16/32/64/128 grid-study runner that records convergence
    eligibility along with each grid's profile errors.
- [x] Add Matplotlib plots for speed/pressure/streamlines, Ghia profiles, and
    transient convergence history.

[`src/fvm/postprocessing.py`](src/fvm/postprocessing.py) provides
`centerline_profiles`, `compare_ghia_re100`, `velocity_extrema`,
`export_simulation_result`, and the plotting helpers. Ghia's tabulated Re=100
values are cited in the module; RMS comparisons use interior profile points and
the reports preserve whether the simulation converged. A capped run can still
be inspected, but its `benchmark_valid` flag is false.

`run_lid_driven_grid_study()` runs the planned 16/32/64/128 meshes and returns
one row per grid. It is intentionally not run by the default example because
fully converging the finer grids may take substantial time. Use converged runs
before drawing grid-independence or benchmark-acceptance conclusions.

### M8 - Setup-Software Integration - Complete

- [x] Define a versioned JSON input contract and stable result summary.
- [x] Translate supported geometry, mesh, material, initial/boundary
    conditions, and solver controls into internal solver objects.
- [x] Keep the backend independent of setup-framework imports and APIs.
- [x] Reject malformed, unsupported, or incompatible setup documents before
    starting the numerical solve.
- [x] Verify file/mapping input, solver execution, and reproducible artifacts
    end to end.

The contract is defined by
[`src/fvm/schemas/case-v1.schema.json`](src/fvm/schemas/case-v1.schema.json),
with a complete example at
[`cases/lid_driven_cavity_re100.json`](cases/lid_driven_cavity_re100.json).
The version 1.0 contract uses SI units and supports rectangular uniform
Cartesian meshes, transient incompressible laminar Newtonian flow, constant
properties, uniform initial fields, no-slip/moving walls, and homogeneous
Neumann pressure correction. Unsupported models, inlets/outlets, mesh types,
and unknown keys are rejected explicitly. Breaking contract changes require a
new schema version so setup software can target a stable boundary.

`PythonFVMBackend` in [`src/fvm/integration.py`](src/fvm/integration.py) accepts
either a validated mapping or JSON case file. It returns a `BackendRun` with
the native simulation and a JSON-compatible summary. When given an output
directory it writes `case.json`, `summary.json`, `fields.npz`, `metadata.json`,
and `history.csv`. The setup application only needs to emit the documented
contract and read these versioned outputs; it does not need to import solver
internals.

### M9 - Checkpointing and Restart - Complete

- [x] Capture complete solver state at completed-step boundaries and resume
    with global step numbering, physical/pseudo-time, and diagnostics history.
- [x] Write compressed field checkpoints atomically, maintain a SHA-256-verified
    latest pointer, and retain a configurable number of recent files.
- [x] Reject incompatible case changes while permitting increased step and
    finite-transient end-time limits.
- [x] Verify split-run equivalence, checkpoint integrity, retention, and failed
    writes that preserve the previous latest checkpoint.

`CheckpointManager` in [`src/fvm/checkpoint.py`](src/fvm/checkpoint.py) stores
restart state under `OUTPUT/checkpoints/`; `case.json` remains the explicit
problem input and `fields.npz`/`history.csv` remain post-processing outputs.
Run with `--checkpoint-every N` and resume with `--restart latest` or a selected
checkpoint filename. The [solver user guide](docs/using_the_solver.md) documents
the file layout, compatibility rules, command-line examples, and Python API.

## Examples

The examples are kept together in
[`examples/end_to_end_examples.py`](examples/end_to_end_examples.py). It
currently includes:

- A stationary, closed cavity with no moving walls. With no forcing and zero
    initial velocity, this is a useful zero-flow baseline for later milestones.
- A Re = 100 lid-driven cavity setup with a moving north wall and stationary
    remaining walls.
- A non-square mesh demonstration that prints coordinates and array shapes to
    make staggered field locations easy to inspect.
- A manufactured-field operator demonstration that checks linear gradients,
    quadratic diffusion, face divergence, and upwind convection.
- A one-step momentum predictor demonstration for a stationary cavity and the
    Re = 100 lid-driven cavity, including sparse solve residuals.
- A pressure-correction solve from the lid-driven predictor velocity, reporting
    its compatibility, divergence, correction magnitude, and linear residual.
- A M5 projection that applies the correction and reports divergence reduction,
    updated pressure, and global mass imbalance.
- An M6 stationary run that converges at rest, plus a bounded lid-driven run
    that reports its CFL and final convergence status.
- M7 result export and Matplotlib plots, plus interior-point Ghia RMS errors
    clearly marked as diagnostic if the short example run has not converged.
- An M8 setup-backend run that reads the versioned case file and writes a
    setup-facing result summary and field/history artifacts.
- A focused user workflow at [`examples/run_user_case.py`](examples/run_user_case.py)
    that runs the longer-budget Re=100 case, verifies convergence, exports all
    artifacts, and generates the three post-processing plots.

Run the milestone catalog from the project root after installing the package:

```powershell
python -m pip install -e ".[test]"
python examples/end_to_end_examples.py
```

For a focused full user workflow with a converged Re=100 cavity, run
`python examples/run_user_case.py`. Select `--mode save` (default) to write PNGs
without windows, or `--mode live` to show the geometry before solving and update
velocity, pressure, and convergence plots at every step. Live mode still saves
all image and data files and requires an interactive Matplotlib backend. See the
[user guide](docs/using_the_solver.md) for the case contract and output details.

The example writes compressed fields, metadata, history, a Ghia report, and
three PNG plots under `results/m7_preview/`. The full four-grid run is opt-in:
call `run_lid_driven_grid_study()` from `fvm.postprocessing` when ready to spend
the additional time needed to converge the finer meshes.

The cavity and grid examples create setup data. The M2 demonstration verifies
operators against manufactured fields; M3 computes one momentum predictor;
M4 solves its pressure correction; M5 corrects velocity and pressure and
checks continuity; M6 runs bounded transient simulations; M7 exports and plots
results and compares centerlines to Ghia; M8 loads a setup-generated contract
and returns versioned machine-readable results; M9 persists restartable solver
state and resumes interrupted runs. The optional full grid study is available
through `run_lid_driven_grid_study()`.

## Testing

Install the package and test dependencies, then run the test suite:

```powershell
python -m pip install -e ".[test]"
python -m pytest
```

The current tests cover mesh geometry and indexing, staggered field storage,
input validation, boundary-condition storage, the 64 by 64 cavity foundation,
numerical-operator accuracy and conservation, sparse momentum coefficients and
source terms, wall behavior, predictor residuals, pressure-Poisson coefficients,
gauge recovery, flux compatibility, pressure/velocity correction consistency,
continuity reduction, global mass imbalance, CFL selection, convergence,
termination behavior, benchmark interpolation/eligibility, exports, plots,
grid-study reporting, case-schema validation, negative setup inputs, adapter
mapping, backend artifacts, checkpoint serialization and integrity, restart
compatibility, split-run equivalence, retention, and atomic failure recovery.