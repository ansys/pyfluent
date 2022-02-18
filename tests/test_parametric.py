import pytest
from pytest_mock import MockerFixture

from ansys.fluent.addons.parametric import ParametricProject
from ansys.fluent.solver.flobject import Command, NamedObject
from ansys.fluent.solver.settings import root


@pytest.fixture(autouse=True)
def mock_settings_service(mocker: MockerFixture) -> None:
    Command.__call__ = mocker.Mock(return_value=None)
    NamedObject.get_object_names = mocker.Mock(return_value=[])


@pytest.fixture(name="parametric_project")
def fixture_parametric_project():
    return ParametricProject(
        root.file.parametric_project(), root.parametric_studies(), "abc.flprj"
    )


class TestParamtericProject:

    def test_open(
        self,
        mocker: MockerFixture,
        parametric_project: ParametricProject,
    ) -> None:
        spy = mocker.spy(root.file.parametric_project.open, "__call__")
        parametric_project.open(project_filepath="abc.flprj")
        spy.assert_called_once_with(
            project_filename="abc.flprj",
            load_case=True
        )

    def test_save(
        self,
        mocker: MockerFixture,
        parametric_project: ParametricProject,
    ) -> None:
        spy = mocker.spy(root.file.parametric_project.save, "__call__")
        parametric_project.save()
        spy.assert_called_once_with()

    def test_save_as(
        self,
        mocker: MockerFixture,
        parametric_project: ParametricProject,
    ) -> None:
        spy = mocker.spy(root.file.parametric_project.save_as, "__call__")
        parametric_project.save_as(project_filepath="abc.flprj")
        spy.assert_called_once_with(project_filename="abc.flprj")

    def test_export(
        self,
        mocker: MockerFixture,
        parametric_project: ParametricProject,
    ) -> None:
        spy = mocker.spy(root.file.parametric_project.save_as_copy, "__call__")
        parametric_project.export(project_filepath="abc.flprj")
        spy.assert_called_once_with(
            project_filename="abc.flprj", convert_to_managed=False
        )

    def test_archive(
        self,
        mocker: MockerFixture,
        parametric_project: ParametricProject,
    ) -> None:
        spy = mocker.spy(root.file.parametric_project.archive, "__call__")
        parametric_project.archive()
        spy.assert_called_once_with(archive_name="abc.flprz")
