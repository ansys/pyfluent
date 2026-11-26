"""Boundary-condition definitions and per-field boundary storage."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from numbers import Real
from types import MappingProxyType
from typing import Mapping, TypeAlias

from .mesh import BOUNDARY_NAMES

Velocity: TypeAlias = tuple[float, float]
BoundaryValue: TypeAlias = float | Velocity


def _velocity_pair(value: tuple[float, float], name: str) -> Velocity:
    """Normalize and validate a two-component velocity."""
    if not isinstance(value, (tuple, list)) or len(value) != 2:
        raise ValueError(f"{name} must contain exactly two components")
    if any(
        isinstance(component, bool)
        or not isinstance(component, Real)
        or not isfinite(component)
        for component in value
    ):
        raise ValueError(f"{name} components must be finite numbers")
    return (float(value[0]), float(value[1]))


@dataclass(frozen=True, slots=True)
class FixedValue:
    """A prescribed scalar value or two-component vector value."""

    value: BoundaryValue

    def __post_init__(self) -> None:
        if isinstance(self.value, bool):
            raise TypeError("fixed value must be numeric")
        if isinstance(self.value, Real):
            if not isfinite(self.value):
                raise ValueError("fixed value must be finite")
            object.__setattr__(self, "value", float(self.value))
        else:
            object.__setattr__(self, "value", _velocity_pair(self.value, "fixed value"))


@dataclass(frozen=True, slots=True)
class ZeroGradient:
    """A homogeneous normal-gradient boundary condition."""


@dataclass(frozen=True, slots=True)
class NoSlipWall:
    """Stationary no-slip wall, represented by its prescribed velocity."""

    velocity: Velocity = (0.0, 0.0)

    def __post_init__(self) -> None:
        object.__setattr__(self, "velocity", _velocity_pair(self.velocity, "velocity"))


@dataclass(frozen=True, slots=True)
class MovingWall:
    """Moving no-slip wall, represented by its prescribed velocity."""

    velocity: Velocity

    def __post_init__(self) -> None:
        object.__setattr__(self, "velocity", _velocity_pair(self.velocity, "velocity"))


BoundaryCondition: TypeAlias = FixedValue | ZeroGradient | NoSlipWall | MovingWall


class BoundaryConditions:
    """Store conditions by `(field_name, side)` without applying them yet.

    A field can be a scalar such as ``pressure`` or a vector such as
    ``velocity``. The numerical discretization will interpret each condition.
    """

    def __init__(self) -> None:
        self._conditions: dict[tuple[str, str], BoundaryCondition] = {}

    def set(
        self, field_name: str, boundary: str, condition: BoundaryCondition
    ) -> None:
        """Add or replace a condition for one field on one domain boundary."""
        if not isinstance(field_name, str) or not field_name.strip():
            raise ValueError("field_name must be a non-empty string")
        if boundary not in BOUNDARY_NAMES:
            raise ValueError(f"boundary must be one of {BOUNDARY_NAMES}")
        if not isinstance(condition, (FixedValue, ZeroGradient, NoSlipWall, MovingWall)):
            raise TypeError("unsupported boundary condition type")
        self._conditions[(field_name, boundary)] = condition

    def get(self, field_name: str, boundary: str) -> BoundaryCondition:
        """Return a stored condition or raise `KeyError` if it is not defined."""
        return self._conditions[(field_name, boundary)]

    def for_field(self, field_name: str) -> Mapping[str, BoundaryCondition]:
        """Return a read-only mapping of the conditions defined for a field."""
        conditions = {
            boundary: condition
            for (stored_field, boundary), condition in self._conditions.items()
            if stored_field == field_name
        }
        return MappingProxyType(conditions)

    def __len__(self) -> int:
        """Return the number of stored field-boundary conditions."""
        return len(self._conditions)