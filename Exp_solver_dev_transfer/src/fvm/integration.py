"""Adapter between setup-software case documents and the Python FVM backend."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from numbers import Integral
from typing import Mapping

import numpy as np

from .boundary_conditions import BoundaryConditions, MovingWall, NoSlipWall
from .checkpoint import CheckpointManager
from .case_definition import CaseDefinition, CaseDocument, load_case_file, parse_case_definition
from .fields import ScalarField, VectorField
from .mesh import BOUNDARY_NAMES, CartesianMesh
from .postprocessing import velocity_extrema
from .simulation import SimulationResult, SimulationState, StepObserver, TransientSolver


@dataclass(frozen=True, slots=True)
class PreparedCase:
    """Solver-owned objects translated from a framework-neutral definition."""

    definition: CaseDefinition
    mesh: CartesianMesh
    initial_velocity: VectorField
    initial_pressure: ScalarField
    boundary_conditions: BoundaryConditions
    solver: TransientSolver


@dataclass(frozen=True, slots=True)
class BackendRun:
    """Simulation output returned to a caller, with a JSON-compatible summary."""

    case_id: str
    simulation: SimulationResult
    summary: dict[str, object]
    artifact_directory: Path | None


class PythonFVMBackend:
    """Prepare and execute the capabilities described by a v1 case document.

    The setup framework only needs to emit the documented JSON contract (or a
    mapping with the same keys). This adapter performs no framework imports;
    unsupported models and boundary types are rejected by the case validator.
    """

    backend_id = "independent-fvm-python"
    supported_schema_version = "1.0"

    def prepare(self, case: CaseDefinition | CaseDocument) -> PreparedCase:
        """Translate validated case data to mesh, fields, BCs, and solver."""
        definition = case if isinstance(case, CaseDefinition) else parse_case_definition(case)
        if definition.schema_version != self.supported_schema_version:
            raise ValueError(f"unsupported schema version: {definition.schema_version}")

        mesh = CartesianMesh(
            nx=definition.nx,
            ny=definition.ny,
            width=definition.width,
            height=definition.height,
        )
        velocity = VectorField(
            mesh,
            name="velocity",
            initial_value=(definition.initial_u, definition.initial_v),
        )
        pressure = ScalarField(
            mesh,
            name="pressure",
            initial_value=definition.initial_pressure,
        )
        boundaries = _case_boundary_conditions(definition, 0.0)
        solver = TransientSolver(
            density=definition.density,
            viscosity=definition.dynamic_viscosity,
            transient=definition.transient,
            **definition.solver.to_solver_kwargs(),
        )
        return PreparedCase(definition, mesh, velocity, pressure, boundaries, solver)

    def run(
        self,
        case: CaseDefinition | CaseDocument,
        output_directory: str | Path | None = None,
        *,
        step_observer: StepObserver | None = None,
        checkpoint_every: int | None = None,
        restart: str | Path | None = None,
        retain_checkpoints: int = 5,
    ) -> BackendRun:
        """Run a case and optionally checkpoint or resume from a run workspace."""
        prepared = self.prepare(case)
        output_path = None if output_directory is None else Path(output_directory)
        if checkpoint_every is not None and (
            isinstance(checkpoint_every, bool)
            or not isinstance(checkpoint_every, Integral)
            or checkpoint_every <= 0
        ):
            raise ValueError("checkpoint_every must be a positive integer")
        if (checkpoint_every is not None or restart is not None) and output_path is None:
            raise ValueError("checkpointing and restart require output_directory")
        if restart is not None and checkpoint_every is None:
            raise ValueError("restart requires checkpoint_every to continue periodic saves")

        checkpoint_manager = (
            CheckpointManager(output_path / "checkpoints", retain_checkpoints)
            if output_path is not None and checkpoint_every is not None
            else None
        )
        case_document = prepared.definition.to_mapping()
        restart_state = (
            checkpoint_manager.load(restart, case_document, prepared.mesh)
            if checkpoint_manager is not None and restart is not None
            else None
        )
        if output_path is not None:
            output_path.mkdir(parents=True, exist_ok=True)
            with (output_path / "case.json").open("w", encoding="utf-8") as case_file:
                json.dump(case_document, case_file, indent=2)

        last_checkpoint_step = restart_state.completed_steps if restart_state else 0

        def checkpoint_state(state: SimulationState) -> None:
            nonlocal last_checkpoint_step
            if (
                checkpoint_manager is not None
                and checkpoint_every is not None
                and state.completed_steps % checkpoint_every == 0
            ):
                checkpoint_manager.save(state, case_document)
                last_checkpoint_step = state.completed_steps

        simulation = prepared.solver.run(
            prepared.initial_velocity,
            prepared.initial_pressure,
            prepared.boundary_conditions,
            step_observer=step_observer,
            state_observer=(checkpoint_state if checkpoint_manager is not None else None),
            state_observer_interval=checkpoint_every or 1,
            restart_state=restart_state,
            boundary_conditions_at_time=(
                lambda time: _case_boundary_conditions(prepared.definition, time)
            ),
            boundary_conditions_over_interval=(
                lambda start, end: _case_boundary_conditions(
                    prepared.definition, end, interval=(start, end)
                )
            ),
        )
        if (
            checkpoint_manager is not None
            and simulation.history
            and simulation.termination_reason != "time_step_not_converged"
        ):
            final_step = simulation.history[-1].step
            if final_step > last_checkpoint_step:
                final_diagnostics = simulation.history[-1]
                final_velocity = VectorField(simulation.velocity.mesh, name="velocity")
                final_velocity.set_values(
                    simulation.velocity.u.values, simulation.velocity.v.values
                )
                final_pressure = ScalarField(
                    simulation.pressure.mesh, name="pressure"
                )
                final_pressure.set_values(simulation.pressure.values)
                final_state = SimulationState(
                    velocity=final_velocity,
                    pressure=final_pressure,
                    completed_steps=final_step,
                    elapsed_time=final_diagnostics.time or 0.0,
                    pseudo_time=final_diagnostics.pseudo_time or 0.0,
                    steady_time_step=(
                        simulation.history[0].time_step
                        if not prepared.definition.transient
                        else None
                    ),
                    history=simulation.history,
                )
                checkpoint_manager.save(final_state, case_document)
        summary = self._result_summary(prepared.definition, simulation)
        if restart_state is not None:
            summary["restarted_from_step"] = restart_state.completed_steps
        artifact_path: Path | None = None
        if output_path is not None:
            from .postprocessing import export_simulation_result

            artifact_path = export_simulation_result(simulation, output_path)
            with (artifact_path / "summary.json").open("w", encoding="utf-8") as summary_file:
                json.dump(summary, summary_file, indent=2)
        return BackendRun(
            case_id=prepared.definition.case_id,
            simulation=simulation,
            summary=summary,
            artifact_directory=artifact_path,
        )

    def run_file(
        self,
        path: str | Path,
        output_directory: str | Path | None = None,
        *,
        step_observer: StepObserver | None = None,
        checkpoint_every: int | None = None,
        restart: str | Path | None = None,
        retain_checkpoints: int = 5,
    ) -> BackendRun:
        """Load a JSON case file, execute it, and optionally export artifacts."""
        return self.run(
            load_case_file(path),
            output_directory,
            step_observer=step_observer,
            checkpoint_every=checkpoint_every,
            restart=restart,
            retain_checkpoints=retain_checkpoints,
        )

    def _result_summary(
        self, definition: CaseDefinition, simulation: SimulationResult
    ) -> dict[str, object]:
        """Create a unit-labeled, stable summary suitable for setup software."""
        extrema = velocity_extrema(simulation.velocity)
        lid_speed = max(
            float(np.hypot(*velocity))
            for side in BOUNDARY_NAMES
            for velocity in (
                definition.boundary_for(side).velocity_profile
                and tuple(
                    point_velocity
                    for _, point_velocity in definition.boundary_for(side).velocity_profile
                )
                or (definition.boundary_for(side).velocity,)
            )
        )
        reynolds_number = (
            definition.density * lid_speed * definition.width / definition.dynamic_viscosity
        )
        summary: dict[str, object] = {
            "result_format_version": "1.0",
            "backend": self.backend_id,
            "case_id": definition.case_id,
            "schema_version": definition.schema_version,
            "status": "converged" if simulation.converged else "not_converged",
            "converged": simulation.converged,
            "termination_reason": simulation.termination_reason,
            "temporal_mode": "transient" if definition.transient else "steady",
            "steps": simulation.steps,
            "final_time_s": simulation.final_time,
            "final_pseudo_time_s": simulation.final_pseudo_time,
            "mesh": {
                "nx": definition.nx,
                "ny": definition.ny,
                "width_m": definition.width,
                "height_m": definition.height,
            },
            "reynolds_number": reynolds_number,
            "velocity_extrema": {
                "u_min_m_s": extrema.u.minimum,
                "u_min_location_m": list(extrema.u.minimum_location),
                "u_max_m_s": extrema.u.maximum,
                "u_max_location_m": list(extrema.u.maximum_location),
                "v_min_m_s": extrema.v.minimum,
                "v_min_location_m": list(extrema.v.minimum_location),
                "v_max_m_s": extrema.v.maximum,
                "v_max_location_m": list(extrema.v.maximum_location),
                "speed_max_m_s": extrema.maximum_speed,
                "speed_max_location_m": list(extrema.maximum_speed_location),
            },
        }
        if simulation.history:
            last_step = simulation.history[-1]
            summary["conservation"] = {
                "max_divergence_s_inv": last_step.max_divergence_after,
                "global_mass_imbalance_m2_s": last_step.global_mass_imbalance,
            }
            summary["residuals"] = {
                "u_momentum": last_step.u_momentum_residual,
                "v_momentum": last_step.v_momentum_residual,
                "pressure": last_step.pressure_residual,
            }
        return summary


def _case_boundary_conditions(
    definition: CaseDefinition,
    time: float,
    *,
    interval: tuple[float, float] | None = None,
) -> BoundaryConditions:
    """Materialize the case wall schedule at a time or its interval maximum."""
    boundaries = BoundaryConditions()
    for side in BOUNDARY_NAMES:
        wall = definition.boundary_for(side)
        if wall.boundary_type != "moving_wall":
            boundaries.set("velocity", side, NoSlipWall())
        else:
            velocity = (
                wall.maximum_velocity_between(*interval)
                if interval is not None
                else wall.velocity_at(time)
            )
            boundaries.set("velocity", side, MovingWall(velocity))
    return boundaries