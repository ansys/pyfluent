"""Classes for locally defining a parametric study for Fluent without running Fluent.
The study can then be submitted to be executed in parallel.

Example
-------

Set up a local study

>>> from ansys.fluent.core.parametric import LocalParametricStudy
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

from math import ceil
from typing import Any, Dict

from ansys.fluent.core.launcher.launcher import launch_fluent
from ansys.fluent.core.utils.execution import asynchronous

BASE_DP_NAME = "Base DP"


def convert_design_point_parameter_units(
    value: Dict[str, float | int | str]
) -> Dict[str, float | int]:
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
    """Purely local version of a design point in a parametric study.

    Parameters
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
        """Initialize LocalDesignPoint."""
        self.name = design_point_name
        if base_design_point:
            self.__inputs = base_design_point.input_parameters.copy()
            self.__outputs = base_design_point.output_parameters.copy()
        else:
            self.__inputs = {}
            self.__outputs = {}

    @property
    def input_parameters(self) -> dict:
        """Get the input parameters."""
        return self.__inputs

    @input_parameters.setter
    def input_parameters(self, inputs: dict):
        self.__inputs = inputs

    @property
    def output_parameters(self) -> dict:
        """Get the output parameters."""
        return self.__outputs

    @output_parameters.setter
    def output_parameters(self, outputs: dict):
        self.__outputs = outputs


class LocalDesignPointTable(list):
    """Local version of the design point table in a parametric study.

    Methods
    -------
    add_design_point(design_point_name: str) -> DesignPoint
        Add a new design point to the table with the provided name.
    find_design_point(idx_or_name)
        Get a design point, either by name (str) or an index
        indicating the position in the table (by order of insertion).
    remove_design_point(idx_or_name)
        Remove a design point, either by name (str) or an index
        indicating the position in the table (by order of insertion).

    Raises
    ------
    RuntimeError
        If the design point is not found.
    """

    def __init__(self, base_design_point: LocalDesignPoint):
        """Initialize LocalDesignPointTable."""
        super().__init__()
        self.append(base_design_point)

    def add_design_point(self, design_point_name: str) -> LocalDesignPoint:
        """Add the design point."""
        self.append(LocalDesignPoint(design_point_name, self[0]))
        return self[-1]

    def find_design_point(self, idx_or_name) -> LocalDesignPoint:
        """Find the design point.

        Raises
        ------
        RuntimeError
            If the design point is not found.
        """
        if isinstance(idx_or_name, int):
            return self[idx_or_name]
        for design_point in self:
            if idx_or_name == design_point.name:
                return design_point
        raise RuntimeError(f"This design point is not found: {idx_or_name}")

    def remove_design_point(self, idx_or_name):
        """Remove the design point.

        Raises
        ------
        RuntimeError
            If the design point can not be removed.
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
        return launcher(case_file_name=case_filepath, start_transcript=start_transcript)

    @asynchronous
    def apply_to_study(study, inputs):
        for input in inputs:
            dp_names = set([*study.design_points.keys()])
            try:
                study.design_points.create_1()
            except AttributeError:
                study.design_points.create()
            dp1_name = set([*study.design_points.keys()]).difference(dp_names).pop()
            dp = study.design_points[dp1_name]
            dp.capture_simulation_report_data = capture_report_data
            dp.input_parameters = convert_design_point_parameter_units(input.copy())

    @asynchronous
    def update_design_point(study):
        study.design_points.update_all()

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
        session.result().settings.parametric_studies.initialize(
            project_filename=session.result().id
        )
        for study in session.result().settings.parametric_studies.values():
            studies.append(study)

    apply_to_studies(studies, study_inputs)

    updates = []
    for study in studies:
        updates.append(update_design_point(study))

    for update in updates:
        update.result()

    for study in studies:
        for _, design_point in study.design_points.items():
            for local_design_point in local_study.design_point_table:
                local_design_point.output_parameters = (
                    design_point.output_parameters.get_state()
                )


class LocalParametricStudy:
    """Local version of a parametric study that manages design points to parametrize a
    Fluent solver setup.

    Methods
    -------
    add_design_point(design_point_name)
        Add a design point.
    design_point(idx_or_name)
        Get a design point, either by name (str) or an index
        indicating the position in the table (by order of insertion).
    run_in_fluent()
        Run the study in Fluent

    Raises
    ------
    RuntimeError
        If the design point is not found.
    """

    def __init__(self, case_filepath: str, base_design_point_name: str = "Base DP"):
        """Initialize LocalParametricStudy."""
        from ansys.fluent.core.filereader.casereader import CaseReader

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
        """Add the design point."""
        return self.design_point_table.add_design_point(design_point_name)

    def design_point(self, idx_or_name) -> LocalDesignPoint:
        """Get the design point."""
        return self.design_point_table.find_design_point(idx_or_name)

    def run_in_fluent(
        self,
        num_servers: int,
        launcher: Any = launch_fluent,
        start_transcript: bool = False,
        capture_report_data: bool = False,
    ):
        """Run the local study in fluent."""
        _run_local_study_in_fluent(
            local_study=self,
            num_servers=num_servers,
            launcher=launcher,
            start_transcript=start_transcript,
            capture_report_data=capture_report_data,
        )
