"""Versioned, framework-neutral JSON case contract for solver integration."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path
from typing import Mapping, TypeAlias

from jsonschema import Draft202012Validator

from .mesh import BOUNDARY_NAMES

CaseDocument: TypeAlias = Mapping[str, object]
Velocity: TypeAlias = tuple[float, float]


class CaseValidationError(ValueError):
    """One or more schema or solver-capability errors in a case definition."""

    def __init__(self, errors: tuple[str, ...]) -> None:
        self.errors = errors
        super().__init__("Invalid case definition:\n- " + "\n- ".join(errors))


@dataclass(frozen=True, slots=True)
class VelocityBoundarySpec:
    """A supported no-slip or moving-wall velocity condition."""

    boundary_type: str
    velocity: Velocity
    velocity_profile: tuple[tuple[float, Velocity], ...] = ()

    def velocity_at(self, time: float) -> Velocity:
        """Interpolate a tabulated moving-wall velocity, holding its endpoints."""
        if not self.velocity_profile:
            return self.velocity
        if time <= self.velocity_profile[0][0]:
            return self.velocity_profile[0][1]
        for (start_time, start_velocity), (end_time, end_velocity) in zip(
            self.velocity_profile, self.velocity_profile[1:]
        ):
            if time <= end_time:
                fraction = (time - start_time) / (end_time - start_time)
                return tuple(
                    start + fraction * (end - start)
                    for start, end in zip(start_velocity, end_velocity)
                )
        return self.velocity_profile[-1][1]

    def maximum_velocity_between(self, start: float, end: float) -> Velocity:
        """Return component-wise absolute maxima over a piecewise-linear interval."""
        sample_times = [start, end]
        sample_times.extend(
            time for time, _ in self.velocity_profile if start < time < end
        )
        samples = [self.velocity_at(time) for time in sample_times]
        return tuple(max(abs(value[index]) for value in samples) for index in range(2))


@dataclass(frozen=True, slots=True)
class SolverSettings:
    """Transient solver controls accepted by the version 1.0 case contract."""

    max_time_step: float
    minimum_time_step: float
    max_steps: int
    cfl_limit: float
    velocity_tolerance: float
    continuity_tolerance: float
    mass_tolerance: float
    momentum_residual_tolerance: float
    pressure_residual_tolerance: float
    end_time: float | None = None
    max_inner_iterations_per_time_step: int = 100

    def to_solver_kwargs(self) -> dict[str, float | int | None]:
        """Map contract field names to `TransientSolver` keyword names."""
        return {
            "max_time_step": self.max_time_step,
            "minimum_time_step": self.minimum_time_step,
            "max_steps": self.max_steps,
            "cfl_limit": self.cfl_limit,
            "velocity_tolerance": self.velocity_tolerance,
            "continuity_tolerance": self.continuity_tolerance,
            "mass_tolerance": self.mass_tolerance,
            "momentum_residual_tolerance": self.momentum_residual_tolerance,
            "pressure_residual_tolerance": self.pressure_residual_tolerance,
            "end_time": self.end_time,
            "max_inner_iterations_per_time_step": self.max_inner_iterations_per_time_step,
        }


@dataclass(frozen=True, slots=True)
class CaseDefinition:
    """Validated, typed representation of a version 1.0 solver case."""

    case_id: str
    description: str
    nx: int
    ny: int
    width: float
    height: float
    density: float
    dynamic_viscosity: float
    initial_u: float
    initial_v: float
    initial_pressure: float
    velocity_boundaries: tuple[tuple[str, VelocityBoundarySpec], ...]
    pressure_correction_boundary: str
    solver: SolverSettings
    transient: bool = True
    schema_version: str = "1.0"

    def boundary_for(self, side: str) -> VelocityBoundarySpec:
        """Return the velocity wall definition for one cardinal side."""
        for boundary, spec in self.velocity_boundaries:
            if boundary == side:
                return spec
        raise KeyError(side)

    def to_mapping(self) -> dict[str, object]:
        """Return a fresh JSON-compatible document in canonical field order."""
        boundaries: dict[str, object] = {}
        for side, spec in self.velocity_boundaries:
            if spec.boundary_type == "no_slip_wall":
                boundaries[side] = {"type": spec.boundary_type}
            elif spec.velocity_profile:
                boundaries[side] = {
                    "type": spec.boundary_type,
                    "velocity_profile": [
                        {"time_s": time, "velocity_m_s": list(velocity)}
                        for time, velocity in spec.velocity_profile
                    ],
                }
            else:
                boundaries[side] = {
                    "type": spec.boundary_type,
                    "velocity_m_s": list(spec.velocity),
                }
        boundaries["pressure_correction"] = self.pressure_correction_boundary
        solver = {
            "max_time_step_s": self.solver.max_time_step,
            "minimum_time_step_s": self.solver.minimum_time_step,
            "max_steps": self.solver.max_steps,
            "cfl_limit": self.solver.cfl_limit,
            "velocity_tolerance_m_s": self.solver.velocity_tolerance,
            "continuity_tolerance_s_inv": self.solver.continuity_tolerance,
            "mass_tolerance_m2_s": self.solver.mass_tolerance,
            "momentum_residual_tolerance": self.solver.momentum_residual_tolerance,
            "pressure_residual_tolerance": self.solver.pressure_residual_tolerance,
            "max_inner_iterations_per_time_step": (
                self.solver.max_inner_iterations_per_time_step
            ),
        }
        if self.solver.end_time is not None:
            solver["end_time_s"] = self.solver.end_time
        return {
            "schema_version": self.schema_version,
            "case_id": self.case_id,
            "description": self.description,
            "units": "SI",
            "physics": {
                "model": "incompressible_laminar",
                "transient": self.transient,
            },
            "domain": {
                "type": "rectangle",
                "width_m": self.width,
                "height_m": self.height,
            },
            "mesh": {
                "type": "uniform_cartesian",
                "nx": self.nx,
                "ny": self.ny,
            },
            "material": {
                "type": "newtonian_fluid",
                "density_kg_m3": self.density,
                "dynamic_viscosity_pa_s": self.dynamic_viscosity,
            },
            "initial_conditions": {
                "u_m_s": self.initial_u,
                "v_m_s": self.initial_v,
                "pressure_pa": self.initial_pressure,
            },
            "boundary_conditions": boundaries,
            "solver": solver,
        }


def _case_schema() -> dict[str, object]:
    """Read the packaged schema so installed users validate the same contract."""
    schema_path = files("fvm").joinpath("schemas", "case-v1.schema.json")
    return json.loads(schema_path.read_text(encoding="utf-8"))


def _error_path(path: object) -> str:
    """Format a JSON Schema instance path as a user-readable JSON pointer."""
    parts = [str(part) for part in path]
    return "/" + "/".join(parts) if parts else "/"


def _format_schema_error(error: object) -> list[str]:
    """Point required/unknown-property errors at the actual offending key."""
    path_parts = list(error.absolute_path)
    base_path = _error_path(path_parts)
    if error.validator == "required" and isinstance(error.instance, Mapping):
        missing = sorted(set(error.validator_value) - set(error.instance))
        return [
            f"{_error_path(path_parts + [key])}: required property is missing"
            for key in missing
        ]
    if error.validator == "additionalProperties" and isinstance(error.instance, Mapping):
        declared = set(error.schema.get("properties", {}))
        unknown = sorted(set(error.instance) - declared)
        return [f"{_error_path(path_parts + [key])}: unknown property" for key in unknown]
    return [f"{base_path}: {error.message}"]


def _non_finite_paths(value: object, path: str = "") -> list[str]:
    """Catch NaN/Infinity values accepted by Python's permissive JSON decoder."""
    if isinstance(value, bool) or value is None:
        return []
    if isinstance(value, float) and not math.isfinite(value):
        return [path or "/"]
    if isinstance(value, Mapping):
        invalid: list[str] = []
        for key, child in value.items():
            invalid.extend(_non_finite_paths(child, f"{path}/{key}"))
        return invalid
    if isinstance(value, list):
        invalid = []
        for index, child in enumerate(value):
            invalid.extend(_non_finite_paths(child, f"{path}/{index}"))
        return invalid
    return []


def validate_case_document(document: CaseDocument) -> None:
    """Validate schema, finite values, and cross-field solver constraints.

    All schema failures are collected so setup-software callers can correct a
    document in one pass. Errors include JSON-pointer-like paths and reject
    unknown keys rather than silently ignoring likely misspellings.
    """
    if not isinstance(document, Mapping):
        raise CaseValidationError(("/: the case root must be a JSON object",))

    validator = Draft202012Validator(_case_schema())
    schema_errors = sorted(
        validator.iter_errors(document),
        key=lambda error: (_error_path(error.absolute_path), error.message),
    )
    errors = [message for error in schema_errors for message in _format_schema_error(error)]
    errors.extend(
        f"{path}: value must be finite"
        for path in _non_finite_paths(document)
    )

    solver = document.get("solver")
    if isinstance(solver, Mapping):
        maximum = solver.get("max_time_step_s", 0.01)
        minimum = solver.get("minimum_time_step_s", 1e-12)
        if (
            isinstance(maximum, (int, float))
            and not isinstance(maximum, bool)
            and isinstance(minimum, (int, float))
            and not isinstance(minimum, bool)
            and minimum > maximum
        ):
            errors.append(
                "/solver/minimum_time_step_s: must not exceed /solver/max_time_step_s"
            )

    boundary_conditions = document.get("boundary_conditions")
    physics = document.get("physics")
    transient = isinstance(physics, Mapping) and physics.get("transient") is True
    if isinstance(boundary_conditions, Mapping):
        for side in BOUNDARY_NAMES:
            wall = boundary_conditions.get(side)
            if isinstance(wall, Mapping) and wall.get("type") == "moving_wall":
                velocities = [wall.get("velocity_m_s")]
                profile = wall.get("velocity_profile")
                if isinstance(profile, list):
                    profile_times: list[float] = []
                    velocities.extend(
                        item.get("velocity_m_s")
                        for item in profile
                        if isinstance(item, Mapping)
                    )
                    for point in profile:
                        if not isinstance(point, Mapping):
                            continue
                        point_time = point.get("time_s")
                        if (
                            isinstance(point_time, (int, float))
                            and not isinstance(point_time, bool)
                        ):
                            if profile_times and point_time <= profile_times[-1]:
                                errors.append(
                                    f"/boundary_conditions/{side}/velocity_profile: "
                                    "time_s values must be strictly increasing"
                                )
                            profile_times.append(float(point_time))
                normal_component = 0 if side in ("west", "east") else 1
                if not transient and isinstance(profile, list):
                    errors.append(
                        f"/boundary_conditions/{side}/velocity_profile: "
                        "time-dependent walls require transient physics"
                    )
                for index, velocity in enumerate(velocities):
                    if (
                        isinstance(velocity, list)
                        and len(velocity) == 2
                        and velocity[normal_component] != 0.0
                    ):
                        errors.append(
                            f"/boundary_conditions/{side}/velocity_profile/{index}/"
                            f"velocity_m_s/{normal_component}: wall-normal velocity "
                            "must be zero"
                        )

    if isinstance(solver, Mapping):
        end_time = solver.get("end_time_s")
        if end_time is not None and not transient:
            errors.append("/solver/end_time_s: requires transient physics")

    if errors:
        raise CaseValidationError(tuple(errors))


def parse_case_definition(document: CaseDocument) -> CaseDefinition:
    """Validate a setup-software mapping and convert it to typed case data."""
    validate_case_document(document)
    domain = document["domain"]
    mesh = document["mesh"]
    material = document["material"]
    initial = document["initial_conditions"]
    boundaries = document["boundary_conditions"]
    solver = document["solver"]
    assert isinstance(domain, Mapping)
    assert isinstance(mesh, Mapping)
    assert isinstance(material, Mapping)
    assert isinstance(initial, Mapping)
    assert isinstance(boundaries, Mapping)
    assert isinstance(solver, Mapping)

    velocity_boundaries: list[tuple[str, VelocityBoundarySpec]] = []
    for side in BOUNDARY_NAMES:
        wall = boundaries[side]
        assert isinstance(wall, Mapping)
        boundary_type = str(wall["type"])
        velocity = (
            tuple(float(component) for component in wall["velocity_m_s"])
            if boundary_type == "moving_wall" and "velocity_m_s" in wall
            else (0.0, 0.0)
        )
        profile = tuple(
            (
                float(point["time_s"]),
                tuple(float(component) for component in point["velocity_m_s"]),
            )
            for point in wall.get("velocity_profile", [])
        )
        if profile and velocity == (0.0, 0.0):
            velocity = profile[0][1]
        velocity_boundaries.append(
            (side, VelocityBoundarySpec(boundary_type, velocity, profile))
        )

    settings = SolverSettings(
        max_time_step=float(solver.get("max_time_step_s", 0.01)),
        minimum_time_step=float(solver.get("minimum_time_step_s", 1e-12)),
        max_steps=int(solver["max_steps"]),
        cfl_limit=float(solver.get("cfl_limit", 0.5)),
        velocity_tolerance=float(solver.get("velocity_tolerance_m_s", 1e-6)),
        continuity_tolerance=float(solver.get("continuity_tolerance_s_inv", 1e-8)),
        mass_tolerance=float(solver.get("mass_tolerance_m2_s", 1e-10)),
        momentum_residual_tolerance=float(
            solver.get("momentum_residual_tolerance", 1e-10)
        ),
        pressure_residual_tolerance=float(
            solver.get("pressure_residual_tolerance", 1e-10)
        ),
        end_time=(
            float(solver["end_time_s"])
            if "end_time_s" in solver
            else None
        ),
        max_inner_iterations_per_time_step=int(
            solver.get("max_inner_iterations_per_time_step", 100)
        ),
    )
    return CaseDefinition(
        schema_version=str(document["schema_version"]),
        case_id=str(document["case_id"]),
        description=str(document.get("description", "")),
        nx=int(mesh["nx"]),
        ny=int(mesh["ny"]),
        width=float(domain["width_m"]),
        height=float(domain["height_m"]),
        density=float(material["density_kg_m3"]),
        dynamic_viscosity=float(material["dynamic_viscosity_pa_s"]),
        initial_u=float(initial["u_m_s"]),
        initial_v=float(initial["v_m_s"]),
        initial_pressure=float(initial["pressure_pa"]),
        velocity_boundaries=tuple(velocity_boundaries),
        pressure_correction_boundary=str(boundaries["pressure_correction"]),
        solver=settings,
        transient=bool(document["physics"]["transient"]),
    )


def load_case_file(path: str | Path) -> CaseDefinition:
    """Read, validate, and convert a versioned JSON case file."""
    case_path = Path(path)
    try:
        with case_path.open("r", encoding="utf-8") as case_file:
            document = json.load(case_file)
    except json.JSONDecodeError as error:
        raise CaseValidationError(
            (f"/: invalid JSON at line {error.lineno}, column {error.colno}: {error.msg}",)
        ) from error
    except OSError as error:
        raise CaseValidationError((f"/: cannot read case file {case_path}: {error}",)) from error
    return parse_case_definition(document)