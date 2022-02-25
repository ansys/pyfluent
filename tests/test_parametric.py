import pytest
from pytest_mock import MockerFixture

import ansys.fluent as pyfluent
from ansys.fluent.addons.parametric import ParametricProject
from ansys.fluent.services.datamodel_tui import PyMenu


@pytest.fixture(name="mock_session")
def fixture_mock_session(mocker: MockerFixture):
    session = mocker.Mock()
    session.tui = mocker.Mock()
    session.tui.solver = mocker.Mock()
    session.tui.solver.file = mocker.Mock()
    session.tui.solver.file.parametric_project = (
        pyfluent.solver_tui.file.parametric_project(
            "/file/parametric_project", None
        )
    )
    return session


@pytest.fixture(autouse=True)
def mock_pymenu_execute(mocker: MockerFixture) -> None:
    PyMenu.execute = mocker.Mock(return_value=None)


@pytest.fixture(name="parametric_project")
def fixture_parametric_project(mock_session):
    return ParametricProject(mock_session)


class TestParamtericProject:
    def test_create(
        self,
        mocker: MockerFixture,
        parametric_project: ParametricProject,
    ) -> None:
        spy = mocker.spy(PyMenu, "execute")
        parametric_project.create(project_filename="abc.flprj")
        spy.assert_called_once_with(
            "/file/parametric_project/new", "abc.flprj"
        )

    def test_open(
        self,
        mocker: MockerFixture,
        parametric_project: ParametricProject,
    ) -> None:
        spy = mocker.spy(PyMenu, "execute")
        parametric_project.open(project_filename="abc.flprj")
        spy.assert_called_once_with(
            "/file/parametric_project/open", "yes", "abc.flprj"
        )

    def test_open_with_lock(
        self,
        mocker: MockerFixture,
        parametric_project: ParametricProject,
    ) -> None:
        spy = mocker.spy(PyMenu, "execute")
        parametric_project.open(project_filename="abc.flprj", open_lock=True)
        spy.assert_called_once_with(
            "/file/parametric_project/open", "yes", "abc.flprj", "yes"
        )

    def test_save(
        self,
        mocker: MockerFixture,
        parametric_project: ParametricProject,
    ) -> None:
        spy = mocker.spy(PyMenu, "execute")
        parametric_project.save()
        spy.assert_called_once_with("/file/parametric_project/save")

    def test_save_as(
        self,
        mocker: MockerFixture,
        parametric_project: ParametricProject,
    ) -> None:
        spy = mocker.spy(PyMenu, "execute")
        parametric_project.save_as(project_filename="abc.flprj")
        spy.assert_called_once_with(
            "/file/parametric_project/save_as", "abc.flprj"
        )

    def test_export(
        self,
        mocker: MockerFixture,
        parametric_project: ParametricProject,
    ) -> None:
        spy = mocker.spy(PyMenu, "execute")
        parametric_project.export(project_filename="abc.flprj")
        spy.assert_called_once_with(
            "/file/parametric_project/save_as_copy", "abc.flprj"
        )

    def test_archive(
        self,
        mocker: MockerFixture,
        parametric_project: ParametricProject,
    ) -> None:
        spy = mocker.spy(PyMenu, "execute")
        parametric_project.archive(archive_name="abc.flprz")
        spy.assert_called_once_with(
            "/file/parametric_project/archive", "abc.flprz"
        )
