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

    def to_solver_kwargs(self) -> dict[str, float | int]:
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
            else:
                boundaries[side] = {
                    "type": spec.boundary_type,
                    "velocity_m_s": list(spec.velocity),
                }
        boundaries["pressure_correction"] = self.pressure_correction_boundary
        return {
            "schema_version": self.schema_version,
            "case_id": self.case_id,
            "description": self.description,
            "units": "SI",
            "physics": {"model": "incompressible_laminar", "transient": True},
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
            "solver": {
                "max_time_step_s": self.solver.max_time_step,
                "minimum_time_step_s": self.solver.minimum_time_step,
                "max_steps": self.solver.max_steps,
                "cfl_limit": self.solver.cfl_limit,
                "velocity_tolerance_m_s": self.solver.velocity_tolerance,
                "continuity_tolerance_s_inv": self.solver.continuity_tolerance,
                "mass_tolerance_m2_s": self.solver.mass_tolerance,
                "momentum_residual_tolerance": self.solver.momentum_residual_tolerance,
                "pressure_residual_tolerance": self.solver.pressure_residual_tolerance,
            },
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
        maximum = solver.get("max_time_step_s")
        minimum = solver.get("minimum_time_step_s")
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
    if isinstance(boundary_conditions, Mapping):
        for side in ("west", "east"):
            wall = boundary_conditions.get(side)
            if isinstance(wall, Mapping) and wall.get("type") == "moving_wall":
                velocity = wall.get("velocity_m_s")
                if isinstance(velocity, list) and len(velocity) == 2 and velocity[0] != 0.0:
                    errors.append(
                        f"/boundary_conditions/{side}/velocity_m_s/0: "
                        "wall-normal velocity must be zero"
                    )
        for side in ("south", "north"):
            wall = boundary_conditions.get(side)
            if isinstance(wall, Mapping) and wall.get("type") == "moving_wall":
                velocity = wall.get("velocity_m_s")
                if isinstance(velocity, list) and len(velocity) == 2 and velocity[1] != 0.0:
                    errors.append(
                        f"/boundary_conditions/{side}/velocity_m_s/1: "
                        "wall-normal velocity must be zero"
                    )

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
            if boundary_type == "moving_wall"
            else (0.0, 0.0)
        )
        velocity_boundaries.append(
            (side, VelocityBoundarySpec(boundary_type, velocity))
        )

    settings = SolverSettings(
        max_time_step=float(solver["max_time_step_s"]),
        minimum_time_step=float(solver["minimum_time_step_s"]),
        max_steps=int(solver["max_steps"]),
        cfl_limit=float(solver["cfl_limit"]),
        velocity_tolerance=float(solver["velocity_tolerance_m_s"]),
        continuity_tolerance=float(solver["continuity_tolerance_s_inv"]),
        mass_tolerance=float(solver["mass_tolerance_m2_s"]),
        momentum_residual_tolerance=float(solver["momentum_residual_tolerance"]),
        pressure_residual_tolerance=float(solver["pressure_residual_tolerance"]),
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