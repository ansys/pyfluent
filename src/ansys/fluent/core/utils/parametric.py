"""
Classes for locally defining a parametric study for Fluent without
running Fluent. The study can then be submitted to be executed in
parallel.

Example
-------

Set up a local study

>>> from ansys.fluent.core import LocalParametricStudy
>>> local_study = LocalParametricStudy(case_filepath="E:/elbow1_param.cas.h5")
>>> design_point = local_study.design_point("Base DP")
>>> design_point.input_parameters['v1'] = 0.0
>>> for idx in range(1, 20):
>>>   design_point = local_study.add_design_point("dp_"+str(idx))
>>>   design_point.input_parameters['v1'] = float(idx)/10.0

Run in Fluent

>>> local_study.run_in_fluent(5)

Display results

>>> for design_point in local_study.design_point_table:
>>>   for k, v in design_point.input_parameters.items():
>>>     print("input parameter", k, v)
>>>   for k, v in design_point.output_parameters.items():
>>>     print("output parameter", k, v)
>>> print(72 * "-")

"""

import logging
from math import ceil
from pathlib import Path, PurePosixPath, PureWindowsPath
import tempfile
from typing import Any, Dict, List, Optional, Union

import ansys.fluent.core as pyfluent
from ansys.fluent.core.filereader.casereader import CaseReader
from ansys.fluent.core.utils.execution import asynchronous

BASE_DP_NAME = "Base DP"


class DesignPoint:
    """Provides for accessing and modifying design points in a parametric study.

    Parameters
    ----------
    name : str
        Name of the design point.
    dp_settings

    """

    def __init__(self, name: str, study: Any):
        self.name = name
        self._study = study
        self._dp_settings = study.design_points[name]

    @property
    def input_parameters(self) -> Dict[str, float]:
        """Dictionary of input parameter values by name."""
        return self._dp_settings.input_parameters()

    @input_parameters.setter
    def input_parameters(self, value: Dict[str, float]) -> None:
        self._dp_settings.input_parameters = value

    @property
    def output_parameters(self) -> Dict[str, float]:
        """Dictionary of output parameter values by name."""
        return self._dp_settings.output_parameters()

    @property
    def write_data_enabled(self) -> bool:
        """Whether to write data for the design point."""
        return self._dp_settings.write_data()

    @write_data_enabled.setter
    def write_data_enabled(self, value: bool) -> None:
        self._dp_settings.write_data = value

    @property
    def capture_simulation_report_data_enabled(self) -> bool:
        """Whether to capture simulation report data for the design point."""
        return self._dp_settings.capture_simulation_report_data()

    @capture_simulation_report_data_enabled.setter
    def capture_simulation_report_data_enabled(self, value: bool) -> None:
        self._dp_settings.capture_simulation_report_data = value

    def set_as_current(self) -> None:
        """Set the design point as the current design point."""
        self._study.design_points.set_as_current(design_point=self.name)


class ParametricStudy:
    """Provides for managing parametric studies and their respective design points.

    A parametric study is used to parametrize design points in a Fluent solver
    set up. This class provides the ability to run Fluent for a series of
    design points and access or modify input and output parameters.

    Parameters
    ----------
    parametric_studies : Session.parametric_studies
        ``parametric_studies`` object of a Fluent session.
    session : Session, optional
        Connected Fluent session. The default is ``None``.
    name : str, optional
        Name of the parametric study. The default is ``None``.
    design_points : Dict[str, DesignPoint], optional
        Dictionary of design points under the parametric study by name.
        The default is ``None``.
    initialize : bool, optional
        Whether to initialize the parametric study. The default is ``True``.
    """

    def __init__(
        self,
        parametric_studies,
        session=None,
        name: Optional[str] = None,
        design_points: Dict[str, DesignPoint] = None,
        initialize: Optional[bool] = True,
    ):
        self._parametric_studies = parametric_studies
        self.session = (
            session if session is not None else (_shared_parametric_study_registry())
        )
        self.name = name
        self.design_points = {}
        if design_points is not None:
            self.design_points = design_points
        self.project_filepath = None
        self.session.register_study(self)
        if initialize:
            if self._parametric_studies.initialize.is_active():
                self.project_filepath = Path(
                    tempfile.mkdtemp(
                        prefix="project-",
                        suffix=".cffdb",
                        dir=str(Path.cwd()),  # TODO: should be cwd of server
                    )
                )
                self.project_filepath.rmdir()
                old_study_names = self._parametric_studies.get_object_names()
                self._parametric_studies.initialize(
                    project_filename=self.project_filepath.stem
                )
                new_study_names = self._parametric_studies.get_object_names()
                self.name = set(new_study_names).difference(set(old_study_names)).pop()
                base_design_point = DesignPoint(
                    BASE_DP_NAME,
                    self._parametric_studies[self.name],
                )
                self.design_points = {BASE_DP_NAME: base_design_point}
                self.session.current_study_name = self.name
            else:
                logging.error("Initialize is not available.")

    def get_all_studies(self) -> Dict[str, "ParametricStudy"]:
        """Get all currently active studies.

        Returns
        -------
        Dict[str, "ParametricStudy"]
            Dictionary of all currently active studies.
        """
        return {v.name: v for _, v in self.session._all_studies.items()}

    def reset_study_registry(self):
        """Reset parametric studies registry."""
        self.session.clear_registry()
        self.session.register_study(self)

    def rename(self, new_name: str) -> None:
        """Rename the parametric study.

        Parameters
        ----------
        new_name : str
            New name.
        """
        self._parametric_studies[self.name].rename(new_name)
        self.name = new_name
        self.design_points = {
            k: DesignPoint(k, self._parametric_studies[self.name])
            for k, _ in self.design_points.items()
        }

    @property
    def is_current(self) -> bool:
        """Whether the parametric study is the current parametric study."""
        return self.session.current_study_name == self.name

    def set_as_current(self) -> None:
        """Set the parametric study as the current parametric study."""
        if not self.is_current:
            self._parametric_studies.set_as_current(self.name)
            self.session.current_study_name = self.name

    def duplicate(self, copy_design_points: bool = True) -> "ParametricStudy":
        """Duplicate the current study.

        Parameters
        ----------
        copy_design_points : bool, optional
            Whether to copy the design points from the current study. The
            default is ``True``.

        Returns
        -------
        ParametricStudy
            New instance of the parametric study.
        """
        old_study_names = self._parametric_studies.get_object_names()
        self._parametric_studies.duplicate(copy_design_points=copy_design_points)
        new_study_names = self._parametric_studies.get_object_names()
        clone_name = set(new_study_names).difference(set(old_study_names)).pop()
        current_study = self.get_all_studies()[self.session.current_study_name]
        if copy_design_points:
            clone_design_points = {
                k: DesignPoint(k, self._parametric_studies[clone_name])
                for k, _ in current_study.design_points.items()
            }
        else:
            base_design_point = DesignPoint(
                BASE_DP_NAME,
                self._parametric_studies[clone_name],
            )
            clone_design_points = {BASE_DP_NAME: base_design_point}
        clone = ParametricStudy(
            self._parametric_studies,
            self.session,
            clone_name,
            clone_design_points,
            initialize=False,
        )
        self.session.current_study_name = clone.name
        return clone

    def delete(self) -> None:
        """Delete the parametric study."""
        if self.is_current:
            logging.error("Cannot delete the current study %s", self.name)
        else:
            del self._parametric_studies[self.name]
            self.session._all_studies.pop(id(self))
            del self

    def use_base_data(self) -> None:
        """Use base data for the parametric study."""
        self._parametric_studies.use_base_data()

    def import_design_table(self, filepath: str) -> None:
        """Import the design table for the parametric study.

        Parameters
        ----------
        filepath : str
            Filepath for the design table.
        """
        self._parametric_studies.import_design_table(filepath=filepath)

    def export_design_table(self, filepath: str) -> None:
        """Export the design table for the parametric study.

        Parameters
        ----------
        filepath : str
            Filepath to export the design table to.
        """
        self._parametric_studies.export_design_table(filepath=filepath)

    @property
    def current_design_point(self) -> DesignPoint:
        """Get the current design point.

        This is the current design point within the design points under the
        parametric study.
        """
        dp_name = self._parametric_studies[self.name].current_design_point()
        return self.design_points[dp_name]

    def add_design_point(
        self,
        write_data: bool = False,
        capture_simulation_report_data: bool = True,
    ) -> DesignPoint:
        """Add a new design point under the parametric study.

        Parameters
        ----------
        write_data : bool, optional
            Whether to write data for the design point. The default
            is ``False``.
        capture_simulation_report_data : bool, optional
            Whether to capture simulation report data for the design
            point. The default is ``True``.

        Returns
        -------
        DesignPoint
            New design point.
        """
        self.set_as_current()
        dp_settings = self._parametric_studies[self.name].design_points
        dps_before = dp_settings.get_object_names()
        dp_settings.create_1(
            write_data=write_data,
            capture_simulation_report_data=capture_simulation_report_data,
        )
        dps_after = dp_settings.get_object_names()
        dp_name = set(dps_after).difference(set(dps_before)).pop()
        design_point = DesignPoint(
            dp_name,
            self._parametric_studies[self.name],
        )
        self.design_points[dp_name] = design_point
        return design_point

    def delete_design_points(self, design_points: List[DesignPoint]) -> None:
        """Delete a list of design points.

        Parameters
        ----------
        design_points : List[DesignPoint]
            List of design points to delete.
        """
        if self.current_design_point in design_points:
            logging.error(
                "Cannot delete the current design point %s",
                self.current_design_point.name,
            )
            design_points.remove(self.current_design_point)
        dp_settings = self._parametric_studies[self.name].design_points
        dp_settings.delete_design_points(
            design_points=[dp.name for dp in design_points]
        )
        for design_point in design_points:
            self.design_points.pop(design_point.name)
            del design_point

    def duplicate_design_point(self, design_point: DesignPoint) -> DesignPoint:
        """Duplicate the design point.

        Parameters
        ----------
        design_point : DesignPoint
            Design point.

        Returns
        -------
        DesignPoint
            New design point.
        """
        dp_settings = self._parametric_studies[self.name].design_points
        dps_before = dp_settings.get_object_names()
        dp_settings.duplicate(design_point=design_point.name)
        dps_after = dp_settings.get_object_names()
        new_dp_name = set(dps_after).difference(set(dps_before)).pop()
        new_dp = DesignPoint(
            new_dp_name,
            self._parametric_studies[self.name],
        )
        self.design_points[new_dp_name] = new_dp
        return new_dp

    def save_journals(self, separate_journals: bool) -> None:
        """Save journals.

        Parameters
        ----------
        separate_journals : bool
            Whether to save a separate journal for each design point.
        """
        dp_settings = self._parametric_studies[self.name].design_points
        dp_settings.save_journals(separate_journals=separate_journals)

    def clear_generated_data(self, design_points: List[DesignPoint]) -> None:
        """Clear the generated data for a list of design points.

        Parameters
        ----------
        design_points : List[DesignPoint]
            List of design points.
        """
        dp_settings = self._parametric_studies[self.name].design_points
        dp_settings.clear_generated_data(
            design_points=[dp.name for dp in design_points]
        )

    def load_current_design_point_case_data(self) -> None:
        """Load case data of the current design point."""
        dp_settings = self._parametric_studies[self.name].design_points
        dp_settings.load_case_data()

    def update_current_design_point(self) -> None:
        """Update the current design point."""
        dp_settings = self._parametric_studies[self.name].design_points
        dp_settings.update_current()

    def update_all_design_points(self) -> None:
        """Update all design points."""
        dp_settings = self._parametric_studies[self.name].design_points
        dp_settings.update_all()

    def update_selected_design_points(self, design_points: List[DesignPoint]) -> None:
        """Update a list of design points.

        Parameters
        ----------
        design_points : List[str]
            List of design points.
        """
        dp_settings = self._parametric_studies[self.name].design_points
        dp_settings.update_selected(design_points=[dp.name for dp in design_points])


class ParametricProject:
    """Provides the parametric project workflow.

    Attributes
    ----------
    project_filepath : str
        Filepath of the project.

    Methods
    -------
    open(project_filepath, load_case)
        Open a project.
    save()
        Save a project.
    save_as(project_filepath)
        Save a project as another project.
    export(project_filepath, convert_to_managed)
        Save a project as a copy.
    archive(archive_name)
        Archive a project.
    """

    def __init__(
        self,
        parametric_project,
        parametric_studies,
        project_filepath: str,
        session=None,
        open_project: bool = True,
    ):
        self._parametric_project = parametric_project
        self._parametric_studies = parametric_studies
        self.project_filepath = project_filepath
        self.session = (
            session if session is not None else (_shared_parametric_study_registry())
        )
        if open_project:
            self.open(project_filepath=project_filepath)

    def open(
        self, project_filepath: str = "default.flprj", load_case: bool = True
    ) -> None:
        """Open a project.

        Parameters
        ----------
        project_filepath : str, optional
            Project filename. The default is ``"default.flprj"``.
        load_case : bool, optional
            Whether to load the current case. The default ``True``.
        """
        if (
            not PureWindowsPath(project_filepath).is_absolute()
            or not PurePosixPath(project_filepath).is_absolute()
        ):
            project_filepath = str(Path(project_filepath).resolve())
        self._parametric_project.open(
            project_filename=project_filepath,
            load_case=load_case,
        )
        self.project_filepath = project_filepath
        for study_name in self._parametric_studies.get_object_names():
            study = ParametricStudy(
                self._parametric_studies, self.session, study_name, initialize=False
            )
            dps_settings = self._parametric_studies[study_name].design_points
            for dp_name in dps_settings.get_object_names():
                study.design_points[dp_name] = DesignPoint(
                    dp_name, self._parametric_studies[study_name]
                )

    def save(self) -> None:
        """Save the project."""
        self._parametric_project.save()

    def save_as(self, project_filepath: str) -> None:
        """Save the project as another project.

        Parameters
        ----------
        project_filepath : str
            Filepath to save the new project to.
        """
        self._parametric_project.save_as(project_filename=project_filepath)

    def export(self, project_filepath: str, convert_to_managed: bool = False) -> None:
        """Save the project as a copy.

        Parameters
        ----------
        project_filepath : str
            Name for the new project.
        convert_to_managed : bool
            Whether to convert the project to a managed project.
        """
        self._parametric_project.save_as_copy(
            project_filename=project_filepath,
            convert_to_managed=convert_to_managed,
        )

    def archive(self, archive_path: Optional[str] = None) -> None:
        """Archive the project.

        Parameters
        ----------
        archive_path : str, optional
            Path of the archive file.
        """
        if not archive_path:
            archive_path = str(Path(self.project_filepath).with_suffix(".flprz"))
        self._parametric_project.archive(archive_name=archive_path)


class ParametricSessionLauncher:
    """Provides for launcheing Fluent for parametric sessions.

    Methods
    -------
    __call__(*args, **kwargs)
        Launch a Fluent session.
    """

    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs

    def __call__(self):
        self._kwargs["mode"] = "solver"
        return pyfluent.launch_fluent(*self._args, **self._kwargs)


class ParametricStudyRegistry:
    """Registers parametric study."""

    def __init__(self):
        self._all_studies: Dict[int, "ParametricStudy"] = {}
        self.current_study_name = None

    def register_study(self, study):
        """Register study."""
        self._all_studies[id(study)] = study

    def clear_registry(self):
        """Clear study."""
        self._all_studies = {}


class ParametricSession(ParametricStudyRegistry):
    """Provides for encapsulating studies and projects.

    Attributes
    ----------
    studies : Dict[str, ParametricStudy]
        Dictionary of parametric studies by their names within the session.
    project : ParametricProject
        Name of the parametric project if a project file is to be read.

    Methods
    -------
    new_study()
        Create a study.
    delete_study(self, study_name)
        Delete a study.
    rename_study(self, new_name, old_name)
        Rename a study.
    start_transcript()
        Start streaming of a Fluent transcript.
    stop_transcript()
        Stop streaming of a Fluent transcript.
    """

    def __init__(
        self,
        case_filepath: str = None,
        project_filepath: str = None,
        launcher: Any = ParametricSessionLauncher(),
        start_transcript: bool = False,
        initialize: bool = True,
    ):
        """Instantiate a ParametricSession.

        Parameters
        ----------
        case_filepath : str, optional
            Case file name. The default is ``None``.
        project_filepath : str, optional
            Project file name. The default is ``None``.
        launcher : _type_, optional
            Fluent launcher. The default is ``ParametricSessionLauncher()``.
        start_transcript : bool, optional
            Whether to start streaming of a Fluent transcript. The default
            is ``False``.
        initialize : bool, optional
            Whether to initialize the ParametricStudy instances created. Default is ``True``.
        """
        super().__init__()
        self.studies = {}
        self.project = None
        self._session = launcher()
        self.scheme_eval = self._session.scheme_eval.scheme_eval
        self.scheme_eval(
            "(set parametric-study-dependents-manager " "save-project-at-exit? #f)"
        )
        if not start_transcript:
            self.stop_transcript()
        if case_filepath is not None:
            self._session.file.read(file_name=case_filepath, file_type="case")
            study = ParametricStudy(
                self._session.parametric_studies, self, initialize=initialize
            )
            self.studies[study.name] = study
            self.project = ParametricProject(
                parametric_project=self._session.file.parametric_project,
                parametric_studies=self._session.parametric_studies,
                project_filepath=str(study.project_filepath),
                open_project=False,
                session=self,
            )
        elif project_filepath is not None:
            self.project = ParametricProject(
                parametric_project=self._session.file.parametric_project,
                parametric_studies=self._session.parametric_studies,
                project_filepath=project_filepath,
                session=self,
            )
            studies_settings = self._session.parametric_studies
            for study_name in studies_settings.get_object_names():
                study = ParametricStudy(
                    studies_settings, self, study_name, initialize=initialize
                )
                dps_settings = studies_settings[study_name].design_points
                for dp_name in dps_settings.get_object_names():
                    study.design_points[dp_name] = DesignPoint(
                        dp_name, studies_settings[study_name]
                    )
                self.studies[study_name] = study
            self.current_study_name = self._session.current_parametric_study()

    def new_study(self) -> ParametricStudy:
        """Create a new study.

        Returns
        -------
        ParametricStudy
            New study.
        """
        study = self.studies[self.current_study_name].duplicate()
        self.studies[study.name] = study
        return study

    def delete_study(self, study_name: str) -> None:
        """Delete a study.

        Parameters
        ----------
        study_name : str
            Study name.
        """
        study = self.studies[study_name]
        if study.is_current:
            logging.error("Cannot delete the current study %s", study_name)
        else:
            study.delete()
            self.studies.pop(study_name)

    def rename_study(self, new_name: str, old_name: str) -> None:
        """Rename a study.

        Parameters
        ----------
        new_name : str
            New name.
        old_name : str
            Current name.
        """
        study = self.studies.pop(old_name)
        study.rename(new_name)
        self.studies[new_name] = study

    def exit(self) -> None:
        """Exit parametric session."""
        self._session.exit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        self._session.exit()

    def start_transcript(self) -> None:
        """Start streaming of a Fluent transcript."""
        self._session.transcript.start()

    def stop_transcript(self) -> None:
        """Stop streaming of a Fluent transcript."""
        self._session.transcript.stop()


def _shared_parametric_study_registry():
    if _shared_parametric_study_registry.instance is None:
        _shared_parametric_study_registry.instance = ParametricStudyRegistry()
    return _shared_parametric_study_registry.instance


_shared_parametric_study_registry.instance = None


def convert_design_point_parameter_units(
    value: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int]]:
    """Convert design point parameter units."""

    def conv(val):
        if type(val) in (float, int):
            return val
        if type(val) is not str:
            raise RuntimeError("Invalid value type for input parameter", val, type(val))
        pos = val.find(" [")
        if pos == -1:
            return float(val)
        return float(val[:pos])

    return {k: conv(v) for k, v in value.items()}


class LocalDesignPoint:
    """
    Purely local version of a design point in a parametric study.

    Attributes
    ----------
    name : str
        Name of the design point.
    output_parameters : dict
        Dictionary of output parameters (name of parameter to value).
    input_parameters : dict
        Dictionary of input parameters (name of parameter to value).
    status : DesignPointStatus
        Current status of the design point.
    """

    def __init__(self, design_point_name: str, base_design_point=None):
        self.name = design_point_name
        if base_design_point:
            self.__inputs = base_design_point.input_parameters.copy()
            self.__outputs = base_design_point.output_parameters.copy()
        else:
            self.__inputs = {}
            self.__outputs = {}

    @property
    def input_parameters(self) -> dict:
        """Get input parameters."""
        return self.__inputs

    @input_parameters.setter
    def input_parameters(self, inputs: dict):
        self.__inputs = inputs

    @property
    def output_parameters(self) -> dict:
        """Get output parameters."""
        return self.__outputs

    @output_parameters.setter
    def output_parameters(self, outputs: dict):
        self.__outputs = outputs


class LocalDesignPointTable(list):
    """
    Local version of the design point table in a parametric study.

    Methods
    -------
    add_design_point(design_point_name: str) -> DesignPoint
        Add a new design point to the table with the provided name.
    find_design_point(idx_or_name)
        Get a design point, either by name (str) or an index
        indicating the position in the table (by order of insertion).
        Raises
        ------
        RuntimeError
            If the design point is not found.
    remove_design_point(idx_or_name)
        Remove a design point, either by name (str) or an index
        indicating the position in the table (by order of insertion).
        Raises
        ------
        RuntimeError
            If the design point is not found.
    """

    def __init__(self, base_design_point: LocalDesignPoint):
        super().__init__()
        self.append(base_design_point)

    def add_design_point(self, design_point_name: str) -> LocalDesignPoint:
        """Add design point."""
        self.append(LocalDesignPoint(design_point_name, self[0]))
        return self[-1]

    def find_design_point(self, idx_or_name) -> LocalDesignPoint:
        """Find design point.

        Raises
        ------
        RuntimeError
            If given design point does not exist.
        """
        if isinstance(idx_or_name, int):
            return self[idx_or_name]
        for design_point in self:
            if idx_or_name == design_point.name:
                return design_point
        raise RuntimeError(f"This design point is not found: {idx_or_name}")

    def remove_design_point(self, idx_or_name):
        """Remove design point.

        Raises
        ------
        RuntimeError
            If given design point can not be removed.
        """
        design_point = self.find_design_point(idx_or_name)
        if design_point is self[0]:
            raise RuntimeError("You cannot remove the base design point.")
        self.remove(self.find_design_point(idx_or_name))


def _run_local_study_in_fluent(
    local_study,
    num_servers: int,
    launcher: Any,
    start_transcript: bool,
    capture_report_data: bool,
):
    source_table_size = len(local_study.design_point_table)

    def make_input_for_study(design_point_range) -> None:
        if design_point_range is None:
            design_point_range = range(0, source_table_size)
        study_input = []
        for idx in design_point_range:
            design_point = local_study.design_point(idx_or_name=idx)
            study_input.append(design_point.input_parameters.copy())
        return study_input

    def make_input_for_studies(num_servers) -> None:
        study_inputs = []
        total_num_points = num_points = source_table_size
        for i in range(num_servers):
            count = ceil(num_points / num_servers)
            range_base = total_num_points - num_points
            num_points -= count
            num_servers -= 1
            study_inputs.append(
                make_input_for_study(range(range_base, range_base + count))
            )
        return study_inputs

    @asynchronous
    def make_parametric_session(case_filepath):
        return ParametricSession(
            case_filepath=case_filepath,
            launcher=launcher,
            start_transcript=start_transcript,
        )

    @asynchronous
    def apply_to_study(study, inputs):
        first = True
        for input in inputs:
            if first:
                design_point = study.design_points[BASE_DP_NAME]
                design_point.capture_simulation_report_data_enabled = (
                    capture_report_data
                )
                first = False
            else:
                design_point = study.add_design_point(
                    capture_simulation_report_data=capture_report_data
                )
            design_point.input_parameters = convert_design_point_parameter_units(
                input.copy()
            )

    @asynchronous
    def update_design_point(study):
        study.update_all_design_points()

    def apply_to_studies(studies, inputs) -> None:
        results = []
        for item in list(zip(studies, inputs)):
            study, input = item
            results.append(apply_to_study(study, input))
        for result in results:
            result.result()

    study_inputs = make_input_for_studies(num_servers)

    sessions = []
    studies = []
    for i in range(num_servers):
        sessions.append(
            make_parametric_session(case_filepath=local_study.case_filepath)
        )

    for session in sessions:
        studies.append(next(iter(session.result().studies.values())))

    apply_to_studies(studies, study_inputs)

    updates = []
    for study in studies:
        updates.append(update_design_point(study))

    for update in updates:
        update.result()

    it = iter(local_study.design_point_table)

    for study in studies:
        for _, design_point in study.design_points.items():
            next(it).output_parameters = design_point.output_parameters.copy()


class LocalParametricStudy:
    """
    Local version of a parametric study that manages design points to parametrize a
    Fluent solver setup.

    Methods
    -------
    add_design_point(design_point_name: str) -> LocalDesignPoint
        Add a design point.
    design_point(idx_or_name)
        Get a design point, either by name (str) or an index
        indicating the position in the table (by order of insertion).
        Raises
        ------
        RuntimeError
            If the design point is not found.
    run_in_fluent
        Run the study in Fluent
    """

    def __init__(self, case_filepath: str, base_design_point_name: str = "Base DP"):
        self.case_filepath = case_filepath
        base_design_point = LocalDesignPoint(base_design_point_name)
        case_reader = CaseReader(case_file_name=case_filepath)

        base_design_point.input_parameters = {
            p.name: p.value for p in case_reader.input_parameters()
        }

        base_design_point.output_parameters = {
            p.name: None for p in case_reader.output_parameters()
        }

        self.design_point_table = LocalDesignPointTable(base_design_point)

    def add_design_point(self, design_point_name: str) -> LocalDesignPoint:
        """Add design point."""
        return self.design_point_table.add_design_point(design_point_name)

    def design_point(self, idx_or_name) -> LocalDesignPoint:
        """Get design point."""
        return self.design_point_table.find_design_point(idx_or_name)

    def run_in_fluent(
        self,
        num_servers: int,
        launcher: Any = ParametricSessionLauncher(),
        start_transcript: bool = False,
        capture_report_data: bool = False,
    ):
        """Run local study in Fluent."""
        _run_local_study_in_fluent(
            local_study=self,
            num_servers=num_servers,
            launcher=launcher,
            start_transcript=start_transcript,
            capture_report_data=capture_report_data,
        )
