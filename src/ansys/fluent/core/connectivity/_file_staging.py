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

"""Exchange files between the client and Fluent sessions.

Fluent runs on the client's machine, in a container that mounts a client folder,
or on a remote machine reached through a file transfer service. The functions in
this module let a session write or read a file in any of these setups, so that
callers only deal with paths on the client.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from contextlib import contextmanager
from enum import Enum
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import tempfile
from typing import Any
import uuid

_PREFIX = "pyfluent-"
_UNIQUE_NAME = re.compile(rf"{_PREFIX}[0-9a-f]{{12}}\..+")


class FileLocation(Enum):
    """Where a Fluent session reads and writes files, seen from the client."""

    LOCAL = "local"
    """Fluent reads and writes the client's file system."""
    TRANSFER = "transfer"
    """Files move through the session's file transfer service."""
    MOUNT = "mount"
    """Fluent runs in a container that mounts a client folder."""
    UNREACHABLE = "unreachable"
    """Fluent cannot exchange files with the client."""


def instance_attr(obj: Any, name: str) -> Any:
    """Return ``obj.name`` without ``__getattr__`` fallbacks, or ``None``.

    Sessions forward unknown attributes to their settings tree, so their own
    attributes are read with this function.
    """
    try:
        return object.__getattribute__(obj, name)
    except AttributeError:
        return None


def file_location(session: Any) -> FileLocation:
    """Return where ``session`` reads and writes files."""
    if instance_attr(session, "_file_transfer_service") is not None:
        return FileLocation.TRANSFER
    connection = instance_attr(session, "_fluent_connection")
    if connection is None or getattr(connection, "_remote_instance", None) is not None:
        return FileLocation.UNREACHABLE
    properties = getattr(connection, "connection_properties", None)
    if getattr(properties, "inside_container", False):
        return FileLocation.MOUNT
    return FileLocation.LOCAL


def require_reachable(session: Any) -> FileLocation:
    """Return where ``session`` reads and writes files, if the client can reach it.

    Raises
    ------
    RuntimeError
        If the session has exited, or Fluent runs on a remote machine without a
        file transfer service.
    """
    location = file_location(session)
    if location is FileLocation.UNREACHABLE:
        if instance_attr(session, "_fluent_connection") is None:
            reason = "the session is not connected to Fluent (it may have exited)"
        else:
            reason = (
                "Fluent runs on a remote machine and the session has no file "
                "transfer service. Pass file_transfer_service when launching or "
                "connecting to Fluent"
            )
        raise RuntimeError(f"Cannot exchange files with the session: {reason}.")
    return location


def container_mount(session: Any) -> tuple[Path, PurePosixPath]:
    """Return the client folder mounted into the session's container.

    Returns
    -------
    tuple[pathlib.Path, pathlib.PurePosixPath]
        The folder on the client, and its path inside the container.

    Raises
    ------
    RuntimeError
        If the mounted folder is unknown.
    """
    mount = _mount_of(instance_attr(session, "_container"))
    if mount is None:
        from ansys.fluent.core.module_config import config

        if not config.container_mount_source:
            raise RuntimeError(
                "Cannot exchange files with the Fluent container: the client folder "
                "mounted into it is unknown. Set "
                "pyfluent.config.container_mount_source to that folder, and "
                "pyfluent.config.container_mount_target to its path in the "
                "container if it is not the default."
            )
        mount = (config.container_mount_source, config.container_mount_target)
    source, target = mount
    return Path(source), PurePosixPath(str(target))


def _mount_of(container: Any) -> tuple[str, str] | None:
    """Return the working-directory mount of a container started by PyFluent."""
    if container is None:
        return None
    # Docker Compose keeps the resolved mount in its container options.
    options = instance_attr(container, "_container_dict")
    if isinstance(options, dict):
        source, target = options.get("mount_source"), options.get("mount_target")
        if source and target:
            return str(source), str(target)
    # A Docker container records its working directory and its bind mounts.
    attrs = getattr(container, "attrs", None)
    if not isinstance(attrs, dict):
        return None
    target = ((attrs.get("Config") or {}).get("WorkingDir") or "").rstrip("/")
    if not target:
        return None
    for bind in (attrs.get("HostConfig") or {}).get("Binds") or []:
        source = _bind_source(bind, target)
        if source:
            return source, target
    return None


def _bind_source(bind: str, target: str) -> str | None:
    """Return the client side of the Docker bind ``source:target[:mode]``."""
    marker = f":{target}"
    index = bind.rfind(marker)
    if index <= 0:
        return None
    rest = bind[index + len(marker) :]
    return bind[:index] if rest in ("", "/") or rest.startswith(":") else None


def _unique_name(suffix: str) -> str:
    return f"{_PREFIX}{uuid.uuid4().hex[:12]}{suffix}"


def _suffix(file: Path) -> str:
    return "".join(file.suffixes)


def write_file(
    session: Any, write: Callable[[str], Any], *, directory: Path, suffix: str
) -> Path:
    """Have ``session`` write a file, and return the client copy of it.

    Parameters
    ----------
    session : Any
        The session that writes the file.
    write : Callable[[str], Any]
        Called with the file name the session must write, for example
        ``lambda name: session.settings.file.write_case(file_name=name)``.
    directory : pathlib.Path
        Client folder that receives the file.
    suffix : str
        Suffix of the file, such as ``".cas.h5"``.

    Returns
    -------
    pathlib.Path
        The file in ``directory``. Its name is unique.

    Raises
    ------
    RuntimeError
        If the file does not reach the client.
    """
    location = require_reachable(session)
    name = _unique_name(suffix)
    destination = Path(directory) / name
    if location is FileLocation.LOCAL:
        write(str(destination))
        written = destination
    elif location is FileLocation.MOUNT:
        client_dir, container_dir = container_mount(session)
        write(str(container_dir / name))
        written = client_dir / name
    else:
        # Fluent writes into its working directory, and the settings API
        # downloads the file to the client.
        write(name)
        written = _downloaded(session, name)
    if not written.is_file():
        raise RuntimeError(
            f"Fluent wrote {name!r}, but the file did not reach the client at "
            f"{written}."
        )
    if written != destination:
        shutil.move(str(written), str(destination))
    return destination


def _downloaded(session: Any, name: str) -> Path:
    """Return where the file transfer service downloaded the file ``name``."""
    service = instance_attr(session, "_file_transfer_service")
    for folder in (
        getattr(service, "pyfluent_cwd", None),
        getattr(service, "cwd", None),
        os.getcwd(),
    ):
        if folder and (Path(folder) / name).is_file():
            return Path(folder) / name
    return Path(os.getcwd()) / name


def read_file(session: Any, read: Callable[[str], Any], file: Path) -> None:
    """Have ``session`` read the client file ``file``.

    Parameters
    ----------
    session : Any
        The session that reads the file.
    read : Callable[[str], Any]
        Called with the file name the session must read, for example
        ``lambda name: session.settings.file.read_case(file_name=name)``.
    file : pathlib.Path
        The file on the client. It is never modified.
    """
    location = require_reachable(session)
    file = Path(file).resolve()
    if location is FileLocation.LOCAL:
        read(str(file))
        _wait_for_standbys(session)
    elif location is FileLocation.MOUNT:
        client_dir, container_dir = container_mount(session)
        try:
            relative = file.relative_to(client_dir.resolve())
        except ValueError:
            with _unique_copy(file, client_dir) as staged:
                read(str(container_dir / staged.name))
                _wait_for_standbys(session)
        else:
            read(str(container_dir.joinpath(*relative.parts)))
            _wait_for_standbys(session)
    elif _UNIQUE_NAME.fullmatch(file.name):
        # The settings API uploads the file under its name before reading it.
        read(str(file))
        _wait_for_standbys(session)
    else:
        # A file of the same name may already be on the server, and file
        # transfer services keep that one: upload under a unique name instead.
        with _unique_copy(file, None) as staged:
            read(str(staged))
            _wait_for_standbys(session)


def _wait_for_standbys(session: Any) -> None:
    """Wait until resilient standbys of ``session`` also read the file.

    Resilient mode repeats the read on its standby sessions in the background;
    the file must still exist then.
    """
    wait = getattr(instance_attr(session, "resilient"), "wait_for_standbys", None)
    if callable(wait):
        wait()


@contextmanager
def _unique_copy(file: Path, directory: Path | None) -> Iterator[Path]:
    """Copy ``file`` under a unique name, and delete the copy afterwards."""
    folder = Path(directory) if directory else Path(tempfile.mkdtemp(prefix=_PREFIX))
    staged = folder / _unique_name(_suffix(file))
    shutil.copyfile(file, staged)
    try:
        yield staged
    finally:
        staged.unlink(missing_ok=True)
        if directory is None:
            shutil.rmtree(folder, ignore_errors=True)
