# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
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

"""Capture the complete setup of a Fluent case and apply it to solver sessions."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from concurrent.futures import ThreadPoolExecutor
import logging
import os
from pathlib import Path
import shutil
import tempfile
from typing import TYPE_CHECKING, Any
import warnings
import weakref

from ansys.fluent.core.connectivity import _file_staging as staging

if TYPE_CHECKING:
    from ansys.fluent.core._types import PathType
    from ansys.fluent.core.solver.session.solver import Solver
    from ansys.fluent.core.utils.fluent_version import FluentVersion

__all__ = ["CaseSnapshot"]

logger = logging.getLogger("pyfluent.networking")

_CASE_SUFFIXES = (".cas.h5", ".cas.gz", ".cas")
_WRITE_SUFFIX = ".cas.h5"
_ZONE_NAMES = "(map (lambda (t) (symbol->string (thread-name t))) (get-all-threads))"
_RESILIENT_CHECKPOINT = "case-snapshot"
_TEMP_PREFIX = "pyfluent-case-snapshot-"


class CaseSnapshot:
    """A snapshot of the complete setup of a Fluent case: all its settings and its mesh.

    Capture a snapshot once, with :meth:`from_session` or :meth:`from_file`, and
    apply it to any number of solver sessions with :meth:`apply_to`. The snapshot
    is carried by a Fluent case file, Fluent's own complete record of a case, so it
    includes settings that the settings API does not expose. The case file is
    handled for you, whether Fluent runs locally, in a container, or remotely
    through a file transfer service. Solution data is not included.

    Examples
    --------
    >>> import ansys.fluent.core as pyfluent
    >>> snapshot = pyfluent.CaseSnapshot.from_session(solver)
    >>> snapshot.apply_to(worker_1, worker_2)
    >>> template = pyfluent.CaseSnapshot.from_file("elbow_setup.cas.h5")
    >>> template.apply_to(refined_solver, include_mesh=False)
    """

    _file: Path
    _source: str
    _fluent_version: FluentVersion | None
    _dimension: int | None
    _zones: frozenset[str] | None
    _closed: bool
    _cleanup: weakref.finalize | None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Reject direct construction.

        Raises
        ------
        TypeError
            Always: use :meth:`from_session` or :meth:`from_file`.
        """
        raise TypeError(
            "Create a CaseSnapshot with CaseSnapshot.from_session(session) or "
            "CaseSnapshot.from_file(file_name)."
        )

    @classmethod
    def _create(
        cls,
        file: Path,
        *,
        owned: bool,
        source: str,
        fluent_version: FluentVersion | None = None,
        dimension: int | None = None,
        zones: frozenset[str] | None = None,
    ) -> CaseSnapshot:
        self = cls.__new__(cls)
        self._file = file
        self._source = source
        self._fluent_version = fluent_version
        self._dimension = dimension
        self._zones = zones
        self._closed = False
        # Only a local folder is deleted: never a call to Fluent.
        self._cleanup = (
            weakref.finalize(self, shutil.rmtree, str(file.parent), ignore_errors=True)
            if owned
            else None
        )
        return self

    @classmethod
    def from_session(cls, session: Solver) -> CaseSnapshot:
        """Capture the current setup of a solver session.

        The snapshot is taken immediately: later changes to ``session`` are not
        included, and the snapshot remains usable after the session exits.

        Parameters
        ----------
        session : Solver
            Solver session with a case or mesh loaded.

        Returns
        -------
        CaseSnapshot
            The snapshot.

        Raises
        ------
        TypeError
            If ``session`` is not a solver session.
        RuntimeError
            If the session has no case loaded, or cannot exchange files with the
            client.
        """
        _require_solver(session, "from_session")
        serving = _serving(session)
        staging.require_reachable(serving)
        if not _case_loaded(serving):
            raise RuntimeError(
                "The session has no case loaded. Read a case or mesh before "
                "taking a snapshot of it."
            )
        directory = Path(tempfile.mkdtemp(prefix=_TEMP_PREFIX))
        captured = False
        try:
            file = staging.write_file(
                serving,
                _command(session, "file", "write_case"),
                directory=directory,
                suffix=_WRITE_SUFFIX,
            )
            version = serving.get_fluent_version()
            dimension = _dimension(serving)
            zones = _zone_names(serving)
            captured = True
        finally:
            if not captured:
                shutil.rmtree(directory, ignore_errors=True)
        logger.info(f"Captured a case snapshot from a {version} session.")
        return cls._create(
            file,
            owned=True,
            source="session",
            fluent_version=version,
            dimension=dimension,
            zones=zones,
        )

    @classmethod
    def from_file(cls, file_name: PathType) -> CaseSnapshot:
        """Create a snapshot from the setup stored in a case file.

        The file is read each time the snapshot is applied, so it must stay in
        place. It is never modified or deleted.

        Parameters
        ----------
        file_name : os.PathLike | str
            Path of a Fluent case file (``.cas.h5``, ``.cas`` or ``.cas.gz``).

        Returns
        -------
        CaseSnapshot
            The snapshot of the case file.

        Raises
        ------
        FileNotFoundError
            If the file does not exist.
        ValueError
            If the file is not a Fluent case file.
        """
        file = Path(os.fspath(file_name)).expanduser().resolve()
        if not file.is_file():
            raise FileNotFoundError(f"Case file not found: {file}")
        if _case_suffix(file.name) is None:
            raise ValueError(
                f"{file.name!r} is not a Fluent case file: its name must end with "
                ".cas.h5, .cas or .cas.gz."
            )
        return cls._create(file, owned=False, source=f"file {file.name!r}")

    @property
    def fluent_version(self) -> FluentVersion | None:
        """Fluent version that wrote this snapshot, when known.

        It is known for snapshots captured from a session.
        """
        return self._fluent_version

    def apply_to(self, *sessions: Solver, include_mesh: bool = True) -> None:
        """Apply this snapshot to one or more solver sessions.

        The case of each session is replaced. By default, each session also gets
        the mesh of the snapshot. With ``include_mesh=False``, each session keeps
        its current mesh, whose zone names must match those of the snapshot.

        Every session is checked before any is changed, and several sessions are
        loaded in parallel.

        Parameters
        ----------
        *sessions : Solver
            Solver sessions to apply the snapshot to.
        include_mesh : bool, optional
            Whether each session gets the mesh of the snapshot. The default is
            ``True``. With ``False``, each session keeps its current mesh.

        Raises
        ------
        TypeError
            If no session is given, or a session is not a solver session.
        ValueError
            If a session runs an older Fluent version than the one that wrote
            this snapshot, has a different dimension, or, with
            ``include_mesh=False``, has a mesh with different zone names.
        RuntimeError
            If this snapshot is closed, a session cannot exchange files with
            the client, or, with ``include_mesh=False``, a session has no mesh or
            cannot replace its mesh.
        ExceptionGroup
            If applying fails for some of several sessions. It holds the original
            error of each of them.
        """
        self._check_open()
        if not sessions:
            raise TypeError("apply_to() needs at least one session.")
        targets = _distinct(sessions)
        for target in targets:
            self._check_target(target, include_mesh)
        if len(targets) == 1:
            self._apply(targets[0], include_mesh)
            return
        with ThreadPoolExecutor(
            max_workers=len(targets), thread_name_prefix="pyfluent-case-snapshot"
        ) as pool:
            futures = [
                pool.submit(self._apply, target, include_mesh) for target in targets
            ]
        errors = []
        for number, future in enumerate(futures, start=1):
            error = future.exception()
            if error is None:
                continue
            if not isinstance(error, Exception):
                raise error
            error.add_note(
                f"Raised while applying the case snapshot to session {number} of "
                f"{len(targets)}."
            )
            errors.append(error)
        if errors:
            raise ExceptionGroup(
                f"The case snapshot could not be applied to {len(errors)} of "
                f"{len(targets)} sessions.",
                errors,
            )

    def save(self, file_name: PathType) -> Path:
        """Write this snapshot to a case file.

        Parameters
        ----------
        file_name : os.PathLike | str
            Path of the case file to write. Its name must end with the same
            suffix as the snapshot, such as ``.cas.h5``.

        Returns
        -------
        pathlib.Path
            The absolute path of the written file.

        Raises
        ------
        RuntimeError
            If this snapshot is closed.
        ValueError
            If the name of ``file_name`` ends with a different suffix.
        """
        self._check_open()
        destination = Path(os.fspath(file_name)).expanduser().resolve()
        suffix = _case_suffix(self._file.name)
        if _case_suffix(destination.name) != suffix:
            raise ValueError(
                f"The file name must end with {suffix!r}, the format of this "
                "snapshot."
            )
        if destination != self._file:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(self._file, destination)
        return destination

    def close(self) -> None:
        """Delete the temporary copy of a snapshot captured from a session.

        Snapshots created with :meth:`from_file` never delete that file. Closing
        twice is harmless.
        """
        self._closed = True
        if self._cleanup is not None:
            self._cleanup()

    def __enter__(self) -> CaseSnapshot:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    def __repr__(self) -> str:
        details = [f"from {self._source}"]
        if self._fluent_version is not None:
            details.append(str(self._fluent_version))
        if self._dimension is not None:
            details.append(f"{self._dimension}D")
        if self._closed:
            details.append("closed")
        return f"<CaseSnapshot {', '.join(details)}>"

    def _check_open(self) -> None:
        if self._closed:
            raise RuntimeError(
                "This case snapshot is closed. Take a new one with "
                "CaseSnapshot.from_session() or CaseSnapshot.from_file()."
            )

    def _check_target(self, session: Any, include_mesh: bool) -> None:
        """Check that this snapshot can be applied to ``session``.

        Raises
        ------
        ValueError
            If the session's version, dimension or zone names do not fit.
        RuntimeError
            If, without the snapshot's mesh, the session has no mesh or cannot
            replace it.
        """
        _require_solver(session, "apply_to")
        serving = _serving(session)
        staging.require_reachable(serving)
        version = serving.get_fluent_version()
        if self._fluent_version is not None and version < self._fluent_version:
            raise ValueError(
                f"This snapshot was written by {self._fluent_version}, but the "
                f"session runs {version}, which cannot read cases written by newer "
                f"versions. Apply it to a session of {self._fluent_version} or "
                "newer."
            )
        if self._dimension is not None:
            dimension = _dimension(serving)
            if dimension != self._dimension:
                raise ValueError(
                    f"This snapshot is of a {self._dimension}D case, but the "
                    f"session is {dimension}D."
                )
        if include_mesh:
            return
        if not _case_loaded(serving):
            raise RuntimeError(
                "include_mesh=False needs a mesh in the session, but it has no "
                "case loaded."
            )
        mesh = getattr(session.settings, "mesh", None)
        if mesh is None or "replace" not in mesh.command_names:
            raise RuntimeError(
                f"include_mesh=False needs Fluent's mesh.replace command, which "
                f"{version} does not provide."
            )
        if self._zones is not None:
            _check_zones(self._zones, _zone_names(serving))

    def _apply(self, session: Any, include_mesh: bool) -> None:
        serving = _serving(session)
        read_case = _command(session, "file", "read_case")
        if include_mesh:
            staging.read_file(serving, read_case, self._file)
        else:
            self._apply_without_mesh(session, serving, read_case)
        _checkpoint_if_resilient(session)
        logger.info(f"Applied the case snapshot from {self._source}.")

    def _apply_without_mesh(
        self, session: Any, serving: Any, read_case: Callable[[str], None]
    ) -> None:
        """Read this snapshot, then put the session's own mesh back.

        Raises
        ------
        Exception
            Any error after reading this snapshot, raised once the session's
            previous case is restored.
        """
        directory = Path(tempfile.mkdtemp(prefix=_TEMP_PREFIX))
        try:
            own_zones = _zone_names(serving)
            own_case = staging.write_file(
                serving,
                _command(session, "file", "write_case"),
                directory=directory,
                suffix=_WRITE_SUFFIX,
            )
            staging.read_file(serving, read_case, self._file)
            try:
                _check_zones(_zone_names(serving), own_zones)
                # mesh.replace keeps the settings. file.replace_mesh does too,
                # but it crashes Fluent 2027 R1 with turbulence models.
                staging.read_file(
                    serving, _command(session, "mesh", "replace"), own_case
                )
            except Exception as error:
                try:
                    staging.read_file(serving, read_case, own_case)
                except Exception as restore_error:  # noqa: BLE001
                    error.add_note(
                        "Restoring the previous case of the session also failed: "
                        f"{restore_error}"
                    )
                else:
                    error.add_note("The session was restored to its previous case.")
                raise
        finally:
            shutil.rmtree(directory, ignore_errors=True)


def _require_solver(session: Any, method: str) -> None:
    from ansys.fluent.core.solver.session.solver import Solver

    if not isinstance(session, Solver):
        raise TypeError(
            f"CaseSnapshot.{method}() needs a Fluent solver session, not "
            f"{type(session).__name__}."
        )


def _serving(session: Any) -> Any:
    """Return the session that serves calls: a standby after a resilient failover."""
    resilient = staging.instance_attr(session, "resilient")
    active = getattr(resilient, "active_session", None)
    return active if active is not None else session


def _command(session: Any, group: str, name: str) -> Callable[[str], None]:
    """Return a function that runs ``session.settings.<group>.<name>(file_name=...)``."""

    def run(file_name: str) -> None:
        getattr(getattr(session.settings, group), name)(file_name=file_name)

    return run


def _distinct(sessions: Iterable[Any]) -> list[Any]:
    seen: set[int] = set()
    distinct = []
    for session in sessions:
        if id(session) not in seen:
            seen.add(id(session))
            distinct.append(session)
    return distinct


def _case_suffix(name: str) -> str | None:
    lower = name.lower()
    for suffix in _CASE_SUFFIXES:
        if lower.endswith(suffix):
            return suffix
    return None


def _case_loaded(session: Any) -> bool:
    return bool(session.scheme.eval("(case-valid?)"))


def _dimension(session: Any) -> int:
    return 3 if session.scheme.eval("(rp-3d?)") else 2


def _zone_names(session: Any) -> frozenset[str]:
    return frozenset(session.scheme.eval(_ZONE_NAMES) or ())


def _check_zones(snapshot_zones: frozenset[str], mesh_zones: frozenset[str]) -> None:
    """Check that the snapshot and the session's mesh have the same zones.

    Raises
    ------
    ValueError
        If the zone names differ.
    """
    if snapshot_zones == mesh_zones:
        return
    details = []
    if snapshot_only := sorted(snapshot_zones - mesh_zones):
        details.append(f"In the snapshot only: {', '.join(snapshot_only)}.")
    if mesh_only := sorted(mesh_zones - snapshot_zones):
        details.append(f"In the session's mesh only: {', '.join(mesh_only)}.")
    raise ValueError(
        "include_mesh=False needs a mesh with the same zone names as the "
        "snapshot. " + " ".join(details)
    )


def _checkpoint_if_resilient(session: Any) -> None:
    """Checkpoint a resilient session, so that failover restores the applied case.

    Failover replays operations recorded after the newest checkpoint, and the
    temporary case file read by ``apply_to`` does not outlive it.
    """
    if staging.instance_attr(session, "resilient") is None:
        return
    from ansys.fluent.core.resilient import ResilientWarning, is_resilient

    if not is_resilient(session):
        return
    try:
        session.resilient.checkpoint(_RESILIENT_CHECKPOINT)
    except Exception as error:  # noqa: BLE001
        warnings.warn(
            "The case snapshot was applied, but resilient mode could not write a "
            "checkpoint afterwards, so a failover would restore an older state: "
            f"{error}",
            ResilientWarning,
            stacklevel=4,
        )
