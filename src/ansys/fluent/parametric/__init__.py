"""Classes for running a parametric study in Fluent.

Example
-------
>>> root = session.get_settings_root()
>>> from ansys.fluent.parametric import ParametricStudy

Instantiate the study from a Fluent session which has already read a case

>>> study1 = ParametricStudy(root.parametric_studies).initialize()

Access and modify the input parameters of base design point

>>> ip = study1.design_points["Base DP"].input_parameters
>>> ip['vel_hot'] = 0.2
>>> study1.design_points["Base DP"].input_parameters = ip

Update the current design point

>>> study1.update_current_design_point()

Access the output parameters of base design point

>>> study1.design_points["Base DP"].output_parameters

Create, update more design points and delete them

>>> dp1 = study1.add_design_point()
>>> dp2 = study1.duplicate_design_point(dp1)
>>> study1.update_all_design_points()
>>> study1.delete_design_points([dp1, dp2])

Create, rename, delete parametric studies

>>> study2 = study1.duplicate()
>>> study2.rename("abc")
>>> study1.delete()

Project workflow

>>> root = session.get_settings_root()
>>> from ansys.fluent.parametric import ParametricProject
>>> proj = ParametricProject(root.file.parametric_project, root.parametric_studies, "nozzle_para_named.flprj")  # noqa: E501
>>> proj.save()
>>> proj.save_as(project_filepath="nozzle_para_named1.flprj")
>>> proj.export(project_filepath="nozzle_para_named2.flprj")
>>> proj.archive()

Using parametric session

>>> from ansys.fluent.parametric import ParametricSession
>>> session1 = ParametricSession(case_filepath="elbow_params_2.cas.h5")
>>> session1.studies['elbow_params_2-Solve'].design_points['Base DP'].input_parameters  # noqa: E501
>>> study2 = session1.new_study()
>>> session2 = ParametricSession(project_filepath="nozzle_para_named.flprj")
"""

from pathlib import Path
import tempfile
from typing import Any, Dict, List, Optional

import ansys.fluent.core as pyfluent
from ansys.fluent.core import LOG
from ansys.fluent.core.solver.settings import root

BASE_DP_NAME = "Base DP"


class DesignPoint:
    """Design point in a parametric study.

    Attributes
    ----------
    name : str
        Name of the design point.
    input_parameters : Dict[str, float]
        Input parameters values by name.
    output_parameters : Dict[str, float]
        Output parameters values by name.
    write_data_enabled : bool
        Whether to write data for the design point.
    capture_simulation_report_data_enabled : bool
        Whether to capture simulation report data for the design point.
    """

    def __init__(self, name: str, dp_settings: Any):
        self.name = name
        self._dp_settings = dp_settings

    @property
    def input_parameters(self) -> Dict[str, float]:
        """Input parameters values by name."""
        return self._dp_settings.input_parameters()

    @input_parameters.setter
    def input_parameters(self, value: Dict[str, float]) -> None:
        self._dp_settings.input_parameters = value

    @property
    def output_parameters(self) -> Dict[str, float]:
        """Output parameters values by name."""
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


class ParametricStudy:
    """Class to manage design points.

    Parametric study that manages design points to parametrize a
    Fluent solver set-up. Provides ability to run Fluent for a series
    of design points, and access/modify the input and output parameters.

    Attributes
    ----------
    name : str
        Name of the parametric study.
    is_current : bool
        Whether the parametric study is the current parametric study.
    design_points : Dict[str, DesignPoint]
        Design points under the parametric study by name.
    current_design_point : DesignPoint
        The current design point within the design points under the
        parametric study.
    project_filepath : Path
        Filepath of the associated project.

    Methods
    -------
    set_as_current()
        Set the parametric study as the current parametric study.
    get_all_studies()
        Get all currently active studies.
    initialize()
        Initialize parametric study.
    duplicate(copy_design_points)
        Duplicate the parametric study.
    rename(new_name)
        Rename the parametric study.
    delete()
        Delete the parametric study.
    use_base_data()
        Use base data for the parametric study.
    import_design_table(filepath)
        Import the design table for the parametric study.
    export_design_table(filepath)
        Export the design table for the parametric study.
    add_design_point(write_data, capture_simulation_report_data)
        Add a new design point under the parametric study.
    delete_design_points(design_points)
        Delete a list of design points.
    duplicate_design_point(design_point)
        Duplicate the design point.
    save_journals(separate_journals)
        Save journals.
    clear_generated_data(design_points)
        Clear generated data for a list of design points.
    load_current_design_point_case_data()
        Load case-data of the current design point.
    update_current_design_point()
        Update the current design point.
    update_all_design_points()
        Update all design points.
    update_selected_design_points(design_points)
        Update a list of design points.
    """

    _all_studies: Dict[int, "ParametricStudy"] = {}
    current_study_name = None

    def __init__(
        self,
        parametric_studies: root.parametric_studies,
        name: Optional[str] = None,
        design_points: Dict[str, DesignPoint] = None,
    ):
        self._parametric_studies = parametric_studies
        self.name = name
        self.design_points = {}
        if design_points is not None:
            self.design_points = design_points
        self.project_filepath = None
        ParametricStudy._all_studies[id(self)] = self

    @classmethod
    def get_all_studies(cls) -> Dict[str, "ParametricStudy"]:
        """Get all currently active studies.

        Returns
        -------
        Dict[str, "ParametricStudy"]
            currently active studies
        """
        return {v.name: v for _, v in cls._all_studies.items()}

    def initialize(self) -> "ParametricStudy":
        """Initialize parametric study."""
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
            self.name = (
                set(new_study_names).difference(set(old_study_names)).pop()
            )
            base_design_point = DesignPoint(
                BASE_DP_NAME,
                self._parametric_studies[self.name].design_points[
                    BASE_DP_NAME
                ],
            )
            self.design_points = {BASE_DP_NAME: base_design_point}
            ParametricStudy.current_study_name = self.name
            return self
        else:
            LOG.error("initialize is not available")

    def rename(self, new_name: str) -> None:
        """Rename the parametric study.

        Parameters
        ----------
        new_name : str
            new name
        """
        self._parametric_studies.rename(new_name, self.name)
        self.name = new_name
        self.design_points = {
            k: DesignPoint(
                k, self._parametric_studies[self.name].design_points[k]
            )
            for k, _ in self.design_points.items()
        }

    @property
    def is_current(self) -> bool:
        """Whether the parametric study is the current parametric study."""
        return ParametricStudy.current_study_name == self.name

    def set_as_current(self) -> None:
        """Set the parametric study as the current parametric study."""
        if not self.is_current:
            self._parametric_studies.set_as_current(self.name)
            ParametricStudy.current_study_name = self.name

    def duplicate(self, copy_design_points: bool = True) -> "ParametricStudy":
        """Duplicate the current study.

        Parameters
        ----------
        copy_design_points : bool
            Whether to copy the design points from the current study.

        Returns
        -------
        ParametricStudy
            New parametric study instance.
        """
        old_study_names = self._parametric_studies.get_object_names()
        self._parametric_studies.duplicate(
            copy_design_points=copy_design_points
        )
        new_study_names = self._parametric_studies.get_object_names()
        clone_name = (
            set(new_study_names).difference(set(old_study_names)).pop()
        )
        current_study = ParametricStudy.get_all_studies()[
            ParametricStudy.current_study_name
        ]
        if copy_design_points:
            clone_design_points = {
                k: DesignPoint(
                    k, self._parametric_studies[clone_name].design_points[k]
                )
                for k, _ in current_study.design_points.items()
            }
        else:
            base_design_point = DesignPoint(
                BASE_DP_NAME,
                self._parametric_studies[clone_name].design_points[
                    BASE_DP_NAME
                ],
            )
            clone_design_points = {BASE_DP_NAME: base_design_point}
        clone = ParametricStudy(
            self._parametric_studies, clone_name, clone_design_points
        )
        ParametricStudy.current_study_name = clone.name
        return clone

    def delete(self) -> None:
        """Delete the parametric study."""
        if self.is_current:
            LOG.error("Cannot delete the current study %s", self.name)
        else:
            del self._parametric_studies[self.name]
            ParametricStudy._all_studies.pop(id(self))
            del self

    def use_base_data(self) -> None:
        """Use base data for the parametric study."""
        self._parametric_studies.use_base_data()

    def import_design_table(self, filepath: str) -> None:
        """Import the design table for the parametric study.

        Parameters
        ----------
        filepath : str
            Input filepath.
        """
        self._parametric_studies.import_design_table(filepath=filepath)

    def export_design_table(self, filepath: str) -> None:
        """Export the design table for the parametric study.

        Parameters
        ----------
        filepath : str
            Output filepath.
        """
        self._parametric_studies.export_design_table(filepath=filepath)

    @property
    def current_design_point(self) -> DesignPoint:
        """Return the current design point.

        Current design point within the design points under the
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
            Whether to write data for the design point, by default
            False.
        capture_simulation_report_data : bool, optional
            Whether to capture simulation report data for the design
            point, by default True.

        Returns
        -------
        DesignPoint
            The new design point.
        """
        self.set_as_current()
        dp_settings = self._parametric_studies[self.name].design_points
        dps_before = dp_settings.get_object_names()
        dp_settings.create(
            write_data=write_data,
            capture_simulation_report_data=capture_simulation_report_data,
        )
        dps_after = dp_settings.get_object_names()
        dp_name = set(dps_after).difference(set(dps_before)).pop()
        design_point = DesignPoint(
            dp_name,
            self._parametric_studies[self.name].design_points[dp_name],
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
            LOG.error(
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
            Design point to duplicate.

        Returns
        -------
        DesignPoint
            The new design point.
        """
        dp_settings = self._parametric_studies[self.name].design_points
        dps_before = dp_settings.get_object_names()
        dp_settings.duplicate(design_point=design_point.name)
        dps_after = dp_settings.get_object_names()
        new_dp_name = set(dps_after).difference(set(dps_before)).pop()
        new_dp = DesignPoint(
            new_dp_name,
            self._parametric_studies[self.name].design_points[new_dp_name],
        )
        self.design_points[new_dp_name] = new_dp
        return new_dp

    def save_journals(self, separate_journals: bool) -> None:
        """Save journals.

        Parameters
        ----------
        separate_journals : bool
            Whether to save separate journal per design point.
        """
        dp_settings = self._parametric_studies[self.name].design_points
        dp_settings.save_journals(separate_journals=separate_journals)

    def clear_generated_data(self, design_points: List[DesignPoint]) -> None:
        """Clear generated data for a list of design points.

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
        """Load case-data of the current design point."""
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

    def update_selected_design_points(
        self, design_points: List[DesignPoint]
    ) -> None:
        """Update a list of design points.

        Parameters
        ----------
        design_points : List[str]
            List of design points to update.
        """
        dp_settings = self._parametric_studies[self.name].design_points
        dp_settings.update_selected(
            design_points=[dp.name for dp in design_points]
        )


class ParametricProject:
    """Parametric project workflow.

    Attributes
    ----------
    project_filepath : str
        Filepath of the project.

    Methods
    -------
    open(project_filepath, load_case)
        Open a project.
    save()
        Save project.
    save_as(project_filepath)
        Save as project.
    export(project_filepath, convert_to_managed)
        Save project as a copy.
    archive(archive_name)
        Archive project.
    """

    def __init__(
        self,
        parametric_project: root.file.parametric_project,
        parametric_studies: root.parametric_studies,
        project_filepath: str,
        open_project: bool = True,
    ):
        self._parametric_project = parametric_project
        self._parametric_studies = parametric_studies
        self.project_filepath = project_filepath
        if open_project:
            self.open(project_filepath=project_filepath)

    def open(
        self, project_filepath: str = "default.flprj", load_case: bool = True
    ) -> None:
        """Open a project.

        Parameters
        ----------
        project_filepath : str, optional
            Project filename, by default "default.flprj".
        load_case : bool, optional
            Specifies whether to load the current case, by default True.
        """
        self._parametric_project.open(
            project_filename=str(Path(project_filepath).resolve()),
            load_case=load_case,
        )
        self.project_filepath = project_filepath
        for study_name in self._parametric_studies.get_object_names():
            study = ParametricStudy(self._parametric_studies, study_name)
            dps_settings = self._parametric_studies[study_name].design_points
            for dp_name in dps_settings.get_object_names():
                study.design_points[dp_name] = DesignPoint(
                    dp_name, dps_settings[dp_name]
                )

    def save(self) -> None:
        """Save project."""
        self._parametric_project.save()

    def save_as(self, project_filepath: str) -> None:
        """Save as project.

        Parameters
        ----------
        project_filepath : str
            Project filename.
        """
        self._parametric_project.save_as(project_filename=project_filepath)

    def export(
        self, project_filepath: str, convert_to_managed: bool = False
    ) -> None:
        """Save project as a copy.

        Parameters
        ----------
        project_filepath : str
            Project filename.
        convert_to_managed : bool
            Specifies whether to convert to managed project.
        """
        self._parametric_project.save_as_copy(
            project_filename=project_filepath,
            convert_to_managed=convert_to_managed,
        )

    def archive(self, archive_path: str = None) -> None:
        """Archive project.

        Parameters
        ----------
        archive_name : str, optional
            Archive name.
        """
        if not archive_path:
            archive_path = str(
                Path(self.project_filepath).with_suffix(".flprz")
            )
        self._parametric_project.archive(archive_name=archive_path)


class ParametricSessionLauncher:
    """Launches fluent for parametric sessions.

    Methods
    -------
    __call__(*args, **kwargs)
        Launch a session.
    """

    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs

    def __call__(self):
        return pyfluent.launch_fluent(*self._args, **self._kwargs)


class ParametricSession:
    """ParametricSession class which encapsulates studies and project.

    Attributes
    ----------
    studies : Dict[str, ParametricStudy]
        Parametric studies by their name within the session.
    project : ParametricProject
        Parametric project if a project file is read.

    Methods
    -------
    new_study()
        Create new study.
    delete_study(self, study_name)
        Delete study.
    rename_study(self, new_name, old_name)
        Rename study.
    start_transcript()
        Start streaming of Fluent transcript.
    stop_transcript()
        Stop streaming of Fluent transcript.
    """

    def __init__(
        self,
        case_filepath: str = None,
        project_filepath: str = None,
        launcher: Any = ParametricSessionLauncher(),
        start_transcript: bool = False,
    ):
        """Instantiate a ParametricSession.

        Parameters
        ----------
        case_filepath : str, optional
            Case file name, by default None.
        project_filepath : str, optional
            Project file name, by default None.
        launcher : _type_, optional
            Fluent launcher, by default ParametricSessionLauncher().
        start_transcript : bool, optional
            Whether to start streaming of Fluent transcript, by default
            False.
        """
        self.studies = {}
        self.project = None
        self._session = launcher()
        self.scheme_eval = self._session.scheme_eval.scheme_eval
        self.scheme_eval(
            "(set parametric-study-dependents-manager "
            "save-project-at-exit? #f)"
        )
        if start_transcript:
            self.start_transcript()
        self._root = self._session.get_settings_root()
        if case_filepath is not None:
            self._root.file.read(file_name=case_filepath, file_type="case")
            study = ParametricStudy(self._root.parametric_studies).initialize()
            self.studies[study.name] = study
            self.project = ParametricProject(
                parametric_project=self._root.file.parametric_project,
                parametric_studies=self._root.parametric_studies,
                project_filepath=str(study.project_filepath),
                open_project=False,
            )
        elif project_filepath is not None:
            self.project = ParametricProject(
                parametric_project=self._root.file.parametric_project,
                parametric_studies=self._root.parametric_studies,
                project_filepath=project_filepath,
            )
            studies_settings = self._root.parametric_studies
            for study_name in studies_settings.get_object_names():
                study = ParametricStudy(studies_settings, study_name)
                dps_settings = studies_settings[study_name].design_points
                for dp_name in dps_settings.get_object_names():
                    study.design_points[dp_name] = DesignPoint(
                        dp_name, dps_settings[dp_name]
                    )
                self.studies[study_name] = study
            ParametricStudy.current_study_name = (
                self._root.current_parametric_study()
            )

    def new_study(self) -> ParametricStudy:
        """Create new study.

        Returns
        -------
        ParametricStudy
            New study.
        """
        study = self.studies[ParametricStudy.current_study_name].duplicate()
        self.studies[study.name] = study
        return study

    def delete_study(self, study_name: str) -> None:
        """Delete study.

        Parameters
        ----------
        study_name : str
            Study name.
        """
        study = self.studies[study_name]
        if study.is_current:
            LOG.error("Cannot delete the current study %s", study_name)
        else:
            study.delete()
            self.studies.pop(study_name)

    def rename_study(self, new_name: str, old_name: str) -> None:
        """Rename study.

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
        self._session.exit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        self._session.exit()

    def start_transcript(self) -> None:
        """Start streaming of Fluent transcript."""
        self._session.start_transcript()

    def stop_transcript(self) -> None:
        """Stop streaming of Fluent transcript."""
        self._session.stop_transcript()
