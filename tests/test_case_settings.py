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

"""CaseSettings against an in-memory model of Fluent (no Fluent needed)."""

import gc
import json
from pathlib import Path, PurePosixPath
import shutil
from types import SimpleNamespace
import uuid

import pytest

import ansys.fluent.core as pyfluent
from ansys.fluent.core import CaseSettings
from ansys.fluent.core.connectivity import _file_staging as staging
from ansys.fluent.core.resilient import ResilientWarning
from ansys.fluent.core.solver.session.solver import Solver

CONTAINER_DIR = PurePosixPath("/home/container/workdir")
ZONES = ("fluid", "inlet", "outlet")


def case(model="k-omega", *, mesh="mesh-a", zones=ZONES):
    return {"settings": {"viscous": model}, "mesh": mesh, "zones": list(zones)}


# -- where Fluent runs ---------------------------------------------------------


class Local:
    """Fluent reads and writes the client's file system."""

    fts = container = remote = None
    inside_container = False

    def __init__(self, root):
        pass

    def fluent_path(self, name):
        return Path(name)

    def after_write(self, name):
        pass

    def before_read(self, name):
        return name


class Mount(Local):
    """Fluent runs in a container that mounts a client folder."""

    inside_container = True

    def __init__(self, root):
        self.client_dir = root / "mount"
        self.client_dir.mkdir()
        self.container = SimpleNamespace(
            attrs={
                "Config": {"WorkingDir": str(CONTAINER_DIR)},
                "HostConfig": {"Binds": [f"{self.client_dir}:{CONTAINER_DIR}:rw"]},
            }
        )

    def fluent_path(self, name):
        # Fails for client paths, which a container cannot see.
        relative = PurePosixPath(name).relative_to(CONTAINER_DIR)
        return self.client_dir.joinpath(*relative.parts)


class Transfer(Local):
    """Files move through a file transfer service, as in the settings API."""

    def __init__(self, root):
        self.server_dir = root / "server"
        self.server_dir.mkdir()
        downloads = root / "downloads"
        downloads.mkdir()
        self.fts = SimpleNamespace(pyfluent_cwd=downloads)

    def fluent_path(self, name):
        assert "/" not in name and "\\" not in name, "Fluent got a client path"
        return self.server_dir / name

    def after_write(self, name):
        # The settings API downloads written files.
        shutil.copyfile(self.server_dir / name, self.fts.pyfluent_cwd / name)

    def before_read(self, name):
        # The settings API uploads files under their name, but keeps a file of
        # that name that is already on the server.
        client = Path(name)
        if not (self.server_dir / client.name).exists():
            shutil.copyfile(client, self.server_dir / client.name)
        return client.name


class Remote(Local):
    """Fluent runs remotely without a file transfer service."""

    remote = object()


ENVIRONMENTS = {"local": Local, "mount": Mount, "transfer": Transfer, "remote": Remote}


# -- Fluent ----------------------------------------------------------------------


class FakeFluent:
    """The Fluent state that CaseSettings reads and changes."""

    def __init__(self, env, case=None, version="27.1.0", dimension=3):
        self.env = env
        self.case = case
        self.version = version
        self.dimension = dimension
        self.commands = ["write_case", "read_case", "replace"]
        self.fail = set()
        self.calls = []

    def write(self, name):
        self.calls.append("write_case")
        self.env.fluent_path(name).write_text(json.dumps(self.case))
        self.env.after_write(name)

    def load(self, command, name):
        self.calls.append(command)
        if command in self.fail:
            raise RuntimeError(f"Fluent rejected {command}.")
        loaded = json.loads(
            self.env.fluent_path(self.env.before_read(name)).read_text()
        )
        if command == "replace":
            # Fluent's mesh.replace keeps the settings and takes the file's mesh.
            self.case = {**self.case, "mesh": loaded["mesh"], "zones": loaded["zones"]}
        else:
            self.case = loaded


class FakeScheme:
    def __init__(self, fluent):
        self._fluent = fluent

    @property
    def version(self):
        return self._fluent.version

    def eval(self, expression):
        fluent = self._fluent
        if expression == "(case-valid?)":
            return fluent.case is not None
        if expression == "(rp-3d?)":
            return fluent.dimension == 3
        if "thread-name" in expression:
            return list(fluent.case["zones"]) if fluent.case else []
        raise AssertionError(f"Unexpected Scheme expression: {expression}")


class FakeFileMenu:
    def __init__(self, fluent):
        self._fluent = fluent

    def write_case(self, file_name):
        self._fluent.write(file_name)

    def read_case(self, file_name):
        self._fluent.load("read_case", file_name)


class FakeMeshMenu:
    def __init__(self, fluent):
        self._fluent = fluent

    @property
    def command_names(self):
        return [name for name in self._fluent.commands if name == "replace"]

    def replace(self, file_name):
        self._fluent.load("replace", file_name)


class FakeSolver(Solver):
    """A solver session of a FakeFluent."""

    def __init__(self, fluent):
        env = fluent.env
        self.fake = fluent
        self._fluent_connection = SimpleNamespace(
            _remote_instance=env.remote,
            connection_properties=SimpleNamespace(
                inside_container=env.inside_container
            ),
        )
        self._file_transfer_service = env.fts
        self._container = env.container
        self.scheme = FakeScheme(fluent)
        self._settings = SimpleNamespace(
            file=FakeFileMenu(fluent), mesh=FakeMeshMenu(fluent)
        )


@pytest.fixture
def solver(tmp_path):
    def make(kind="local", **state):
        root = tmp_path / f"{kind}-{uuid.uuid4().hex[:6]}"
        root.mkdir()
        return FakeSolver(FakeFluent(ENVIRONMENTS[kind](root), **state))

    return make


def case_file(path, content):
    path.write_text(json.dumps(content))
    return path


# -- capture and apply -----------------------------------------------------------


def test_the_constructor_points_to_the_factory_methods():
    with pytest.raises(TypeError, match="from_session.*from_file"):
        CaseSettings(session=object())


def test_settings_are_captured_when_created(solver):
    source, target = solver(case=case("laminar")), solver()
    settings = CaseSettings.from_session(source)
    source.fake.case = case("k-epsilon")
    settings.apply_to(target)
    assert target.fake.case == case("laminar")
    assert settings.fluent_version == pyfluent.FluentVersion.v271
    assert repr(settings) == "<CaseSettings from session, Ansys Fluent 2027 R1, 3D>"


def test_settings_are_applied_to_several_sessions(solver):
    source = solver(case=case("laminar"))
    targets = [solver(), solver(case=case())]
    settings = CaseSettings.from_session(source)
    source.fake.case = case("k-epsilon")
    # The source session itself goes back to the captured state.
    settings.apply_to(*targets, source)
    for session in (*targets, source):
        assert session.fake.case == case("laminar")


def test_a_session_given_twice_is_applied_once(solver):
    target = solver()
    CaseSettings.from_session(solver(case=case())).apply_to(target, target)
    assert target.fake.calls == ["read_case"]


def test_a_failure_on_a_single_session_raises_the_original_error(solver):
    target = solver()
    target.fake.fail.add("read_case")
    with pytest.raises(RuntimeError, match="rejected read_case"):
        CaseSettings.from_session(solver(case=case())).apply_to(target)


def test_failures_on_several_sessions_are_grouped(solver):
    good, bad = solver(), solver()
    bad.fake.fail.add("read_case")
    with pytest.raises(ExceptionGroup) as info:
        CaseSettings.from_session(solver(case=case())).apply_to(good, bad)
    assert good.fake.case == case()
    (error,) = info.value.exceptions
    assert "rejected read_case" in str(error)
    assert "session 2 of 2" in error.__notes__[0]


def test_sessions_are_checked_before_any_is_changed(solver):
    good, older = solver(), solver(version="25.2.0")
    settings = CaseSettings.from_session(solver(case=case()))
    with pytest.raises(ValueError, match="2027 R1.*2025 R2"):
        settings.apply_to(good, older)
    assert good.fake.calls == older.fake.calls == []


def test_the_dimension_must_match(solver):
    settings = CaseSettings.from_session(solver(case=case()))
    with pytest.raises(ValueError, match="3D case.*2D"):
        settings.apply_to(solver(dimension=2))


def test_only_solver_sessions_are_accepted(solver):
    with pytest.raises(TypeError, match="needs a Fluent solver session"):
        CaseSettings.from_session(SimpleNamespace())
    settings = CaseSettings.from_session(solver(case=case()))
    with pytest.raises(TypeError, match="needs a Fluent solver session"):
        settings.apply_to(SimpleNamespace())
    with pytest.raises(TypeError, match="at least one session"):
        settings.apply_to()


def test_capturing_needs_a_case(solver):
    with pytest.raises(RuntimeError, match="no case loaded"):
        CaseSettings.from_session(solver())


# -- case files ------------------------------------------------------------------


def test_a_case_file_is_read_in_place_and_never_deleted(solver, tmp_path):
    file = case_file(tmp_path / "setup.cas.h5", case("laminar"))
    target = solver()
    with CaseSettings.from_file(file) as settings:
        settings.apply_to(target)
        assert settings.fluent_version is None
        assert repr(settings) == "<CaseSettings from file 'setup.cas.h5'>"
    assert target.fake.case == case("laminar")
    assert file.is_file()


def test_only_existing_case_files_are_accepted(tmp_path):
    with pytest.raises(FileNotFoundError, match="not found"):
        CaseSettings.from_file(tmp_path / "missing.cas.h5")
    with pytest.raises(ValueError, match="not a Fluent case file"):
        CaseSettings.from_file(case_file(tmp_path / "elbow.dat.h5", {}))


def test_settings_can_be_saved(solver, tmp_path):
    settings = CaseSettings.from_session(solver(case=case("laminar")))
    saved = settings.save(tmp_path / "copies" / "setup.cas.h5")
    assert saved == (tmp_path / "copies" / "setup.cas.h5").resolve()
    target = solver()
    CaseSettings.from_file(saved).apply_to(target)
    assert target.fake.case == case("laminar")
    with pytest.raises(ValueError, match="'.cas.h5'"):
        settings.save(tmp_path / "setup.cas")


def test_closing_deletes_the_captured_copy(solver):
    with CaseSettings.from_session(solver(case=case())) as settings:
        folder = settings._file.parent
        assert folder.is_dir()
    assert not folder.exists()
    settings.close()
    assert repr(settings).endswith("closed>")
    with pytest.raises(RuntimeError, match="closed"):
        settings.apply_to(solver())


def test_the_captured_copy_is_deleted_with_the_object(solver):
    settings = CaseSettings.from_session(solver(case=case()))
    folder = settings._file.parent
    del settings
    gc.collect()
    assert not folder.exists()


# -- keep_mesh -------------------------------------------------------------------


def test_keep_mesh_keeps_the_mesh_of_the_session(solver):
    target = solver(case=case("k-omega", mesh="refined"))
    CaseSettings.from_session(solver(case=case("laminar"))).apply_to(
        target, keep_mesh=True
    )
    assert target.fake.case == case("laminar", mesh="refined")
    assert target.fake.calls == ["write_case", "read_case", "replace"]


def test_keep_mesh_checks_zone_names_before_changing_anything(solver):
    target = solver(case=case(zones=("fluid", "inlet", "outlet-2")))
    settings = CaseSettings.from_session(solver(case=case("laminar")))
    with pytest.raises(ValueError, match="settings only: outlet.*mesh only: outlet-2"):
        settings.apply_to(target, keep_mesh=True)
    assert target.fake.calls == []


def test_keep_mesh_restores_the_session_when_a_case_file_has_other_zones(
    solver, tmp_path
):
    original = case(zones=("fluid", "inlet", "outlet-2"))
    target = solver(case=original)
    file = case_file(tmp_path / "setup.cas.h5", case("laminar"))
    with pytest.raises(ValueError, match="same zone names") as info:
        CaseSettings.from_file(file).apply_to(target, keep_mesh=True)
    assert "restored to its previous case" in info.value.__notes__[0]
    assert target.fake.case == original


def test_keep_mesh_restores_the_session_when_replacing_the_mesh_fails(solver):
    original = case(mesh="refined")
    target = solver(case=original)
    target.fake.fail.add("replace")
    with pytest.raises(RuntimeError, match="rejected replace"):
        CaseSettings.from_session(solver(case=case("laminar"))).apply_to(
            target, keep_mesh=True
        )
    assert target.fake.case == original


def test_keep_mesh_needs_a_mesh_and_mesh_replace(solver):
    settings = CaseSettings.from_session(solver(case=case()))
    with pytest.raises(RuntimeError, match="no case loaded"):
        settings.apply_to(solver(), keep_mesh=True)
    older = solver(case=case())
    older.fake.commands.remove("replace")
    with pytest.raises(RuntimeError, match="mesh.replace command"):
        settings.apply_to(older, keep_mesh=True)


# -- where Fluent runs -----------------------------------------------------------


@pytest.mark.parametrize("source_kind", ["local", "mount", "transfer"])
@pytest.mark.parametrize("target_kind", ["local", "mount", "transfer"])
def test_settings_move_between_any_kind_of_sessions(solver, source_kind, target_kind):
    source = solver(source_kind, case=case("laminar"))
    plain, meshed = solver(target_kind), solver(target_kind, case=case(mesh="fine"))
    settings = CaseSettings.from_session(source)
    settings.apply_to(plain)
    settings.apply_to(meshed, keep_mesh=True)
    assert plain.fake.case == case("laminar")
    assert meshed.fake.case == case("laminar", mesh="fine")


def test_a_case_file_outside_the_mount_is_copied_in_and_removed(solver, tmp_path):
    target = solver("mount")
    file = case_file(tmp_path / "setup.cas.h5", case("laminar"))
    CaseSettings.from_file(file).apply_to(target)
    assert target.fake.case == case("laminar")
    assert list(target.fake.env.client_dir.iterdir()) == []


def test_a_case_file_inside_the_mount_is_read_where_it_is(solver):
    target = solver("mount")
    file = case_file(target.fake.env.client_dir / "setup.cas.h5", case("laminar"))
    CaseSettings.from_file(file).apply_to(target)
    assert target.fake.case == case("laminar")
    assert [p.name for p in target.fake.env.client_dir.iterdir()] == ["setup.cas.h5"]


def test_an_older_file_of_the_same_name_on_the_server_is_never_read(solver, tmp_path):
    target = solver("transfer")
    case_file(target.fake.env.server_dir / "setup.cas.h5", case("k-epsilon"))
    file = case_file(tmp_path / "setup.cas.h5", case("laminar"))
    CaseSettings.from_file(file).apply_to(target)
    assert target.fake.case == case("laminar")


def test_sessions_that_cannot_exchange_files_are_rejected(solver):
    with pytest.raises(RuntimeError, match="file transfer service"):
        CaseSettings.from_session(solver("remote", case=case()))
    exited = solver(case=case())
    exited._fluent_connection = None
    settings = CaseSettings.from_session(solver(case=case()))
    with pytest.raises(RuntimeError, match="not connected"):
        settings.apply_to(exited)


def test_the_container_mount_is_read_from_the_container(monkeypatch):
    def session(container):
        return SimpleNamespace(_container=container)

    docker = SimpleNamespace(
        attrs={
            "Config": {"WorkingDir": "/home/container/workdir/"},
            "HostConfig": {
                "Binds": [
                    "C:\\certs:/tmp/certs:ro",
                    "D:\\work\\run:/home/container/workdir",
                ]
            },
        }
    )
    assert staging.container_mount(session(docker)) == (
        Path("D:\\work\\run"),
        PurePosixPath("/home/container/workdir"),
    )
    compose = SimpleNamespace(
        _container_dict={"mount_source": "/data", "mount_target": "/mnt/work"}
    )
    assert staging.container_mount(session(compose)) == (
        Path("/data"),
        PurePosixPath("/mnt/work"),
    )
    monkeypatch.setattr(pyfluent.config, "container_mount_source", "/host")
    assert staging.container_mount(session(None))[0] == Path("/host")
    monkeypatch.setattr(pyfluent.config, "container_mount_source", None)
    with pytest.raises(RuntimeError, match="container_mount_source"):
        staging.container_mount(session(None))


# -- resilient sessions ----------------------------------------------------------


@pytest.fixture
def resilient(monkeypatch):
    import ansys.fluent.core.resilient as resilient_module

    monkeypatch.setattr(resilient_module, "is_resilient", lambda session: True)

    def attach(session, active=None, fail=False):
        names = []

        def checkpoint(name):
            if fail:
                raise RuntimeError("disk full")
            names.append(name)

        session.resilient = SimpleNamespace(
            active_session=active or session, checkpoint=checkpoint
        )
        return names

    return attach


def test_a_resilient_session_is_checkpointed_after_apply(solver, resilient):
    target = solver()
    checkpoints = resilient(target)
    CaseSettings.from_session(solver(case=case("laminar"))).apply_to(target)
    assert checkpoints == ["case-settings"]


def test_a_failed_resilient_checkpoint_is_reported(solver, resilient):
    target = solver()
    resilient(target, fail=True)
    with pytest.warns(ResilientWarning, match="disk full"):
        CaseSettings.from_session(solver(case=case("laminar"))).apply_to(target)
    assert target.fake.case == case("laminar")


def test_queries_go_to_the_standby_after_a_failover(solver, resilient):
    standby = solver(case=case("laminar"))
    original = solver(case=case())
    original.scheme = None  # its Fluent process is gone
    original._settings = standby._settings  # settings calls go to the standby
    resilient(original, active=standby)
    target = solver()
    CaseSettings.from_session(original).apply_to(target)
    assert target.fake.case == case("laminar")
