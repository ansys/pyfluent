"""Portable, validated snapshots that do not depend on solver classes."""

from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
from io import BytesIO
import json
from math import isfinite
from numbers import Integral, Real
import re
from types import MappingProxyType
from typing import Mapping

import numpy as np
from numpy.typing import NDArray


FloatArray = NDArray[np.float64]
_RUN_ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")


def validate_run_id(run_id: str) -> str:
    """Reject identifiers that are unsafe as filesystem path components."""
    if not isinstance(run_id, str) or _RUN_ID_PATTERN.fullmatch(run_id) is None:
        raise ValueError(
            "run_id must be 1-128 characters using letters, digits, dot, "
            "underscore, or hyphen, and start with a letter or digit"
        )
    return run_id


@dataclass(frozen=True, slots=True)
class StepSnapshot:
    """Immutable numerical fields and diagnostics for one completed solver step."""

    run_id: str
    step: int
    mesh: Mapping[str, float | int]
    diagnostics: Mapping[str, int | float | None]
    x_cell_centers: FloatArray
    y_cell_centers: FloatArray
    pressure: FloatArray
    u_faces: FloatArray
    v_faces: FloatArray

    def __post_init__(self) -> None:
        validate_run_id(self.run_id)
        if (
            isinstance(self.step, bool)
            or not isinstance(self.step, Integral)
            or self.step <= 0
        ):
            raise ValueError("step must be a positive integer")
        object.__setattr__(self, "step", int(self.step))
        required_mesh_keys = {"nx", "ny", "width", "height"}
        if set(self.mesh) != required_mesh_keys:
            raise ValueError("mesh must contain nx, ny, width, and height")
        nx, ny = self.mesh["nx"], self.mesh["ny"]
        width, height = self.mesh["width"], self.mesh["height"]
        if (
            isinstance(nx, bool)
            or not isinstance(nx, Integral)
            or nx <= 0
            or isinstance(ny, bool)
            or not isinstance(ny, Integral)
            or ny <= 0
        ):
            raise ValueError("mesh dimensions must be positive integers")
        if (
            isinstance(width, bool)
            or not isinstance(width, Real)
            or isinstance(height, bool)
            or not isinstance(height, Real)
        ):
            raise ValueError("mesh width and height must be finite positive numbers")
        if not isfinite(float(width)) or float(width) <= 0.0:
            raise ValueError("mesh width must be finite and positive")
        if not isfinite(float(height)) or float(height) <= 0.0:
            raise ValueError("mesh height must be finite and positive")
        normalized_mesh = {
            "nx": int(nx),
            "ny": int(ny),
            "width": float(width),
            "height": float(height),
        }
        object.__setattr__(self, "mesh", MappingProxyType(normalized_mesh))
        normalized_diagnostics: dict[str, int | float | None] = {}
        for name, value in self.diagnostics.items():
            if value is not None and (
                isinstance(value, bool) or not isinstance(value, Real)
            ):
                raise TypeError(f"diagnostic {name} must be a number or None")
            if value is not None and not isfinite(float(value)):
                raise ValueError(f"diagnostic {name} must be finite")
            normalized_diagnostics[name] = (
                int(value)
                if isinstance(value, Integral)
                else (None if value is None else float(value))
            )
        object.__setattr__(
            self, "diagnostics", MappingProxyType(normalized_diagnostics)
        )
        shapes = {
            "x_cell_centers": (nx,),
            "y_cell_centers": (ny,),
            "pressure": (ny, nx),
            "u_faces": (ny, nx + 1),
            "v_faces": (ny + 1, nx),
        }
        for name, shape in shapes.items():
            values = np.ascontiguousarray(getattr(self, name), dtype=np.float64)
            if values.shape != shape:
                raise ValueError(f"{name} must have shape {shape}")
            if not np.all(np.isfinite(values)):
                raise ValueError(f"{name} must contain only finite values")
            values = np.frombuffer(values.tobytes(), dtype=np.float64).reshape(shape)
            object.__setattr__(self, name, values)

        diagnostic_step = self.diagnostics.get("step", self.step)
        if (
            isinstance(diagnostic_step, bool)
            or not isinstance(diagnostic_step, Integral)
            or diagnostic_step != self.step
        ):
            raise ValueError("diagnostics step must match snapshot step")

    @classmethod
    def from_solver_step(
        cls, run_id: str, diagnostics: object, velocity: object, pressure: object
    ) -> StepSnapshot:
        """Adapt solver observer objects at the one-way integration boundary."""
        if not is_dataclass(diagnostics):
            raise TypeError("diagnostics must be a dataclass instance")
        diagnostic_values = {
            item.name: getattr(diagnostics, item.name) for item in fields(diagnostics)
        }
        mesh_object = getattr(velocity, "mesh", None)
        if mesh_object is None:
            raise TypeError("velocity snapshot must provide a mesh")
        mesh = {
            "nx": int(mesh_object.nx),
            "ny": int(mesh_object.ny),
            "width": float(mesh_object.width),
            "height": float(mesh_object.height),
        }
        return cls(
            run_id=run_id,
            step=int(diagnostic_values["step"]),
            mesh=mesh,
            diagnostics=diagnostic_values,
            x_cell_centers=mesh_object.x_cell_centers,
            y_cell_centers=mesh_object.y_cell_centers,
            pressure=pressure.values,
            u_faces=velocity.u.values,
            v_faces=velocity.v.values,
        )

    def to_bytes(self) -> bytes:
        """Serialize one versioned snapshot without pickle or solver imports."""
        metadata = {
            "format_version": 1,
            "run_id": self.run_id,
            "step": self.step,
            "mesh": dict(self.mesh),
            "diagnostics": dict(self.diagnostics),
        }
        buffer = BytesIO()
        np.savez_compressed(
            buffer,
            metadata=np.asarray(json.dumps(metadata, allow_nan=False)),
            x_cell_centers=self.x_cell_centers,
            y_cell_centers=self.y_cell_centers,
            pressure=self.pressure,
            u_faces=self.u_faces,
            v_faces=self.v_faces,
        )
        return buffer.getvalue()

    @classmethod
    def from_bytes(cls, payload: bytes) -> StepSnapshot:
        """Decode a snapshot and validate its schema and array dimensions."""
        with np.load(BytesIO(payload), allow_pickle=False) as archive:
            metadata = json.loads(str(archive["metadata"].item()))
            if metadata.get("format_version") != 1:
                raise ValueError("unsupported snapshot format version")
            return cls(
                run_id=metadata["run_id"],
                step=metadata["step"],
                mesh=metadata["mesh"],
                diagnostics=metadata["diagnostics"],
                x_cell_centers=archive["x_cell_centers"],
                y_cell_centers=archive["y_cell_centers"],
                pressure=archive["pressure"],
                u_faces=archive["u_faces"],
                v_faces=archive["v_faces"],
            )
