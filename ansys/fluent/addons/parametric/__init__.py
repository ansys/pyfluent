"""
Classes for running a parametric study in Fluent.

Example
-------
>>> from ansys.fluent.addons.parametric import ParametricStudy

Instantiate the study from a Fluent session which has already read a case

>>> study1 = ParametricStudy(session)

Access and modify the input parameters of base design point

>>> ip = study1.design_points["Base DP"].input_parameters
>>> ip['vel_hot'] = 0.2
>>> study1.design_points["Base DP"].input_parameters = ip

Update the base design point

>>> study1.design_points["Base DP"].update()

Access the output parameters of base design point

>>> study1.design_points["Base DP"].output_parameters

Create, update more design points and delete them

>>> dp1 = study1.add_design_point()
>>> dp2 = study1.duplicate_design_point(dp1)
>>> study1.update_all_design_points()
>>> study1.delete_design_points([dp1, dp2])

Create, rename, delete parametric studies

>>> study2 = study1.duplicate()
>>> study2.name = "abc"
>>> study1.delete()

Project workflow

>>> from ansys.fluent.addons.parametric import ParametricProject
>>> proj = ParametricProject(session)
>>> proj.open(project_filename="nozzle_para_named.flprj")
>>> proj.save()
>>> proj.save_as(project_filename="nozzle_para_named1.flprj")
>>> proj.export(project_filename="nozzle_para_named2.flprj")
>>> proj.archive(archive_name="nozzle_para_named.flprz")

"""

import atexit
import os
import re
import shutil
import tempfile
from pathlib import Path
from typing import Dict, List, Optional

from ansys.fluent import LOG, Session

BASE_DP_NAME = "Base DP"


def _get_parametric_study_tui(tui: Session.SolverTui):
    if "parametric_study" not in dir(tui):
        if "enable_parametric_study" not in dir(tui.preferences.general):
            tui.define.beta_feature_access("yes", "OK")
        tui.preferences.general.enable_parametric_study()
    return tui.parametric_study


def _get_parametric_project_tui(tui: Session.SolverTui):
    if "parametric_project" not in dir(tui.file):
        if "enable_parametric_study" not in dir(tui.preferences.general):
            tui.define.beta_feature_access("yes", "OK")
        tui.preferences.general.enable_parametric_study()
    return tui.file.parametric_project


class DesignPoint:
    """
    Design point in a parametric study

    Attributes
    ----------
    name : str
        Name of the design point
    is_current : bool
        Whether the design point is the current design point
    input_parameters : Dict[str, float]
        Input parameters values by name
    output_parameters : Dict[str, float]
        Output parameters values by name
    write_data_enabled : bool
        Whether to write data for the design point
    capture_simulation_report_data_enabled : bool
        Whether to capture simulation report data for the design point

    Methods
    -------
    update()
        Update the design point

    """

    def __init__(self, name: str, tui: Session.SolverTui):
        self.name = name
        self.__tui = tui

    @property
    def is_current(self) -> bool:
        """
        bool: Whether the design point is the current design point
        """
        dp_tui = _get_parametric_study_tui(self.__tui).design_points
        out = dp_tui.get_current_design_point()
        current_dp = out.result.strip().strip('"')
        return current_dp == self.name

    @is_current.setter
    def is_current(self, value: bool) -> None:
        dp_tui = _get_parametric_study_tui(self.__tui).design_points
        dp_tui.set_as_current(f'"{self.name if value else BASE_DP_NAME}"')

    @property
    def input_parameters(self) -> Dict[str, float]:
        """Dict[str, float]: Input parameters values by name."""
        dp_tui = _get_parametric_study_tui(self.__tui).design_points
        out = dp_tui.get_input_parameters_of_dp(f'"{self.name}"')
        return DesignPoint.__convert_scheme_string_to_parameter_dict(
            out.result.strip()
        )

    @input_parameters.setter
    def input_parameters(self, value: Dict[str, float]) -> None:
        dp_tui = _get_parametric_study_tui(self.__tui).design_points
        dp_tui.set_input_parameters_of_dp(
            f'"{self.name}"', *[v for _, v in value.items()]
        )

    @property
    def output_parameters(self) -> Dict[str, float]:
        """Dict[str, float]: Output parameters values by name"""
        dp_tui = _get_parametric_study_tui(self.__tui).design_points
        out = dp_tui.get_output_parameters_of_dp(f'"{self.name}"')
        return DesignPoint.__convert_scheme_string_to_parameter_dict(
            out.result.strip()
        )

    @property
    def write_data_enabled(self) -> bool:
        """bool: Whether to write data for the design point"""
        dp_tui = _get_parametric_study_tui(self.__tui).design_points
        out = dp_tui.get_write_data(f'"{self.name}"')
        return out.result.strip().strip('"') == "True"

    @write_data_enabled.setter
    def write_data_enabled(self, value: bool) -> None:
        dp_tui = _get_parametric_study_tui(self.__tui).design_points
        dp_tui.set_write_data(f'"{self.name}"', "yes" if value else "no")

    @property
    def capture_simulation_report_data_enabled(self) -> bool:
        """
        bool: Whether to capture simulation report data for the design
        point
        """
        dp_tui = _get_parametric_study_tui(self.__tui).design_points
        out = dp_tui.get_capture_simulation_report_data(f'"{self.name}"')
        return out.result.strip().strip('"') == "True"

    @capture_simulation_report_data_enabled.setter
    def capture_simulation_report_data_enabled(self, value: bool):
        dp_tui = _get_parametric_study_tui(self.__tui).design_points
        dp_tui.set_capture_simulation_report_data(
            f'"{self.name}"', "yes" if value else "no"
        )

    def update(self) -> None:
        """Update the design point"""
        update_tui = _get_parametric_study_tui(self.__tui).update
        update_tui.update_selected_design_points([f'"{self.name}"'])

    @staticmethod
    def __convert_scheme_string_to_parameter_dict(
        inp: str,
    ) -> Dict[str, float]:
        parameters = {}
        for pair in re.findall("\((.*?)\)", inp[1:-1]):
            pair = pair.split(".", 1)
            key = pair[0].strip().strip('"')
            val = float(pair[1].strip())
            parameters[key] = val
        return parameters


class ParametricStudy:
    """
    Parametric study that manages design points to parametrize a
    Fluent solver set-up. Provides ability to run Fluent for a series
    of design points, and access/modify the input and output parameters.

    Attributes
    ----------
    name : str
        Name of the parametric study
    is_current : bool
        Whether the parametric study is the current parametric study
    design_points : Dict[str, DesignPoint]
        Design points under the parametric study by name
    current_design_point : DesignPoint
        The current design point within the design points under the
        parametric study

    Methods
    -------
    set_as_current()
        Set the parametric study as the current parametric study
    duplicate(copy_design_points)
        Duplicate the parametric study
    delete()
        Delete the parametric study
    use_base_data()
        Use base data for the parametric study
    export_design_table(filepath)
        Export the design table for the parametric study
    add_design_point(write_data, capture_simulation_report_data)
        Add a new design point under the parametric study
    delete_design_points(design_points)
        Delete a list of design points
    duplicate_design_point(design_point)
        Duplicate the design point
    save_journals(separate_journal)
        Save journals
    clear_generated_data(design_points)
        Clear generated data for a list of design points
    load_current_design_point_case_data()
        Load case-data of the current design point
    update_current_design_point()
        Update the current design point
    update_all_design_points()
        Update all design points
    update_selected_design_points(design_points)
        Update a list of design points

    """

    _current_study_name = None
    _project_dirs: List[Path] = []

    def __init__(self, session: Session):
        self.__tui = session.tui.solver
        if self.__is_initialized():
            LOG.error("Parametric study is already initialized.")
        elif not self.__is_init_available():
            LOG.error(
                "Parametric study is not available. Please try reading a case."
            )
        else:
            self.__project_dir = Path(
                tempfile.mkdtemp(
                    prefix="project-",
                    suffix=".cffdb",
                    dir=str(Path.cwd()),  # TODO: should be cwd of server
                )
            )
            self.__project_dir.rmdir()
            tui_output = (
                _get_parametric_study_tui(self.__tui)
                .initialize("yes", self.__project_dir.stem)
                .result
            )
            self._name = self.__extract_study_name(tui_output)
            base_design_point = DesignPoint(BASE_DP_NAME, self.__tui)
            base_design_point.is_current = True
            self.design_points = {BASE_DP_NAME: base_design_point}
            ParametricStudy._current_study_name = self._name
            ParametricStudy._project_dirs.append(self.__project_dir)

    @property
    def name(self) -> str:
        """str: Name of the parametric study"""
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        _get_parametric_study_tui(self.__tui).rename_study(self.name, new_name)
        self._name = new_name

    @property
    def is_current(self) -> bool:
        """
        bool: Whether the parametric study is the current parametric
        study
        """
        return ParametricStudy._current_study_name == self.name

    def set_as_current(self) -> None:
        """Set the parametric study as the current parametric study."""
        if not self.is_current:
            _get_parametric_study_tui(self.__tui).set_as_current_study(
                self.name, "yes"
            )
            ParametricStudy._current_study_name = self.name

    def duplicate(self, copy_design_points: bool = True) -> "ParametricStudy":
        """
        Duplicate the design point

        Parameters
        ----------
        copy_design_points : bool
            Whether to copy the design points

        Returns
        -------
        ParametricStudy
            New parametric study instance
        """
        tui_output = (
            _get_parametric_study_tui(self.__tui)
            .duplicate_study("yes" if copy_design_points else "no")
            .result
        )
        cls = self.__class__
        clone = cls.__new__(cls)
        clone.__dict__.update(self.__dict__)
        clone._name = self.__extract_study_name(tui_output)
        if copy_design_points:
            clone.design_points = self.design_points.copy()
        else:
            base_design_point = DesignPoint(BASE_DP_NAME, self.__tui)
            base_design_point.is_current = True
            self.design_points = {BASE_DP_NAME: base_design_point}
        ParametricStudy._current_study_name = clone.name
        return clone

    def delete(self) -> None:
        """
        Delete the parametric study
        """
        if self.is_current:
            LOG.error("Cannot delete the current study %s", self.name)
        else:
            _get_parametric_study_tui(self.__tui).delete_study(
                self.name, "yes"
            )
            del self

    @classmethod
    def cleanup_project_dirs(cls) -> None:
        for project_dir in cls._project_dirs:
            flprj = os.path.splitext(str(project_dir))[0] + ".flprj"
            shutil.rmtree(str(project_dir))
            Path(flprj).unlink()

    def use_base_data(self) -> None:
        """Use base data for the parametric study"""
        _get_parametric_study_tui(self.__tui).use_base_data("yes")

    def export_design_table(self, filepath: str) -> None:
        """
        Export the design table for the parametric study

        Parameters
        ----------
        filepath : str
            Output filepath
        """
        _get_parametric_study_tui(self.__tui).export_design_table(filepath)

    def __is_init_available(self) -> bool:
        return "initialize" in dir(_get_parametric_study_tui(self.__tui))

    def __is_initialized(self) -> bool:
        return "delete_study" in dir(_get_parametric_study_tui(self.__tui))

    def __extract_study_name(self, tui_output: str) -> str:
        project_dirname = self.__project_dir.name
        for line in tui_output.split("\n"):
            if project_dirname in line:
                comps = line.replace("\\", "/").split("/")
                index = comps.index(project_dirname)
                return comps[index + 1]
        LOG.error("Study name cannot be retrieved")
        return ""

    @property
    def current_design_point(self) -> DesignPoint:
        """
        DesignPoint: The current design point within the design points
        under the parametric study.
        """
        dp_tui = _get_parametric_study_tui(self.__tui).design_points
        out = dp_tui.get_current_design_point()
        dp_name = out.result.strip().strip('"')
        return self.design_points[dp_name]

    def add_design_point(
        self,
        write_data: bool = False,
        capture_simulation_report_data: bool = True,
    ) -> DesignPoint:
        """
        Add a new design point under the parametric study

        Parameters
        ----------
        write_data : bool, optional
            Whether to write data for the design point, by default False
        capture_simulation_report_data : bool, optional
            Whether to capture simulation report data for the design
            point, by default True

        Returns
        -------
        DesignPoint
            The new design point
        """
        self.set_as_current()
        dps_before = self.__extract_design_point_names()
        base_input_params = self.design_points[BASE_DP_NAME].input_parameters
        dp_tui = _get_parametric_study_tui(self.__tui).design_points
        dp_tui.add_design_point(
            *[v for _, v in base_input_params.items()],
            "yes" if write_data else "no",
            "yes" if capture_simulation_report_data else "no",
        )
        dps_after = self.__extract_design_point_names()
        dp_name = set(dps_after).difference(set(dps_before)).pop()
        design_point = DesignPoint(dp_name, self.__tui)
        self.design_points[dp_name] = design_point
        return design_point

    def delete_design_points(self, design_points: List[DesignPoint]) -> None:
        """
        Delete a list of design points

        Parameters
        ----------
        design_points : List[DesignPoint]
            List of design points to delete
        """
        if self.current_design_point in design_points:
            LOG.error(
                "Cannot delete the current design point %s",
                self.current_design_point.name
            )
            design_points.remove(self.current_design_point)
        dp_tui = _get_parametric_study_tui(self.__tui).design_points
        dp_tui.delete_design_point(
            [f'"{dp.name}"' for dp in design_points], "yes"
        )
        for design_point in design_points:
            self.design_points.pop(design_point.name)
            del design_point

    def duplicate_design_point(self, design_point: DesignPoint) -> DesignPoint:
        """
        Duplicate the design point

        Parameters
        ----------
        design_point : DesignPoint
            Design point to duplicate

        Returns
        -------
        DesignPoint
            The new design point
        """
        dps_before = self.__extract_design_point_names()
        dp_tui = _get_parametric_study_tui(self.__tui).design_points
        dp_tui.duplicate_design_point(f'"{design_point.name}"')
        dps_after = self.__extract_design_point_names()
        new_dp_name = set(dps_after).difference(set(dps_before)).pop()
        new_dp = DesignPoint(new_dp_name, self.__tui)
        self.design_points[new_dp_name] = new_dp
        return new_dp

    def save_journals(self, separate_journal: bool) -> None:
        """
        Save journals

        Parameters
        ----------
        separate_journal : bool
            Whether to save separate journal per design point.
        """
        _get_parametric_study_tui(self.__tui).design_points.save_journals(
            "yes", 1 if separate_journal else 2
        )

    def clear_generated_data(self, design_points: List[DesignPoint]) -> None:
        """
        Clear generated data for a list of design points

        Parameters
        ----------
        design_points : List[DesignPoint]
            List of design points
        """
        dp_tui = _get_parametric_study_tui(self.__tui).design_point
        dp_tui.clear_generated_data(
            [f'"{dp.name}"' for dp in design_points], "yes"
        )

    def load_current_design_point_case_data(self) -> None:
        """Load case-data of the current design point"""
        dp_tui = _get_parametric_study_tui(self.__tui).design_points
        dp_tui.load_case_data_for_current_dp()

    def update_current_design_point(self) -> None:
        """Update the current design point"""
        _get_parametric_study_tui(self.__tui).update.update_current()

    def update_all_design_points(self) -> None:
        """Update all design points"""
        _get_parametric_study_tui(self.__tui).update.update_all()

    def update_selected_design_points(
        self, design_points: List[DesignPoint]
    ) -> None:
        """
        Update a list of design points

        Parameters
        ----------
        design_points : List[str]
            List of design points to update
        """
        update_tui = _get_parametric_study_tui(self.__tui).update
        update_tui.update_selected_design_points(
            [f'"{dp.name}"' for dp in design_points]
        )

    def __extract_design_point_names(self) -> List[str]:
        fd, filepath = tempfile.mkstemp(suffix=".csv")
        os.close(fd)
        self.export_design_table(filepath)
        design_points = []
        with open(filepath) as f:
            f.readline()
            f.readline()
            for line in f.readlines():
                line = line.strip()
                if line:
                    design_points.append(line.split(",")[0])
        Path(filepath).unlink()
        return design_points


class ParametricProject:
    """
    Parametric project workflow

    Methods
    -------
    create(project_filename)
        Create a new project
    open(project_filename, load_current_case, open_lock)
        Open a project
    save(project_filename)
        Save project
    save_as(project_filename)
        Save as project
    export(project_filename)
        Save project as a copy
    archive(archive_name)
        Archive project

    """

    def __init__(self, session: Session):
        self.__tui = session.tui.solver

    def create(self, project_filename: str = "default.flprj") -> None:
        """
        Create a new project

        Parameters
        ----------
        project_filename : str, optional
            project filename, by default "default.flprj"
        """
        _get_parametric_project_tui(self.__tui).new(project_filename)

    def open(
        self,
        project_filename: str = "default.flprj",
        load_current_case: bool = True,
        open_lock: bool = False,
    ) -> None:
        """
        Open a project

        Parameters
        ----------
        project_filename : str, optional
            project filename, by default "default.flprj"
        load_current_case : bool, optional
            Specifies whether to load the current case, by default True
        open_lock : bool, optional
            Specifies whether to open the lock if project file is
            locked, by default False
        """
        args = ["yes" if load_current_case else "no", project_filename]
        if open_lock:
            args.append("yes")

        _get_parametric_project_tui(self.__tui).open(*args)

    def save(self, project_filename: Optional[str] = None) -> None:
        """
        Save project

        Parameters
        ----------
        project_filename : Optional[str], optional
            project filename, by default None
        """
        args = () if project_filename is None else (project_filename,)
        _get_parametric_project_tui(self.__tui).save(*args)

    def save_as(self, project_filename: str) -> None:
        """
        Save as project

        Parameters
        ----------
        project_filename : str
            project filename
        """
        _get_parametric_project_tui(self.__tui).save_as(project_filename)

    def export(self, project_filename: str) -> None:
        """
        Save project as a copy

        Parameters
        ----------
        project_filename : str
            project filename
        """
        _get_parametric_project_tui(self.__tui).save_as_copy(project_filename)

    def archive(self, archive_name: str) -> None:
        """
        Archive project

        Parameters
        ----------
        archive_name : str
            archive name
        """
        _get_parametric_project_tui(self.__tui).archive(archive_name)


atexit.register(ParametricStudy.cleanup_project_dirs)
