"""
Classes for running a parametric study in Fluent.

Example
-------
>>> from ansys.fluent.addons.parametric import ParametricStudy, DesignPointStatus  # noqa: E501

Instantiate the study, specifying the case

>>> study = ParametricStudy(case_file_name=my_case_file_name)

Add one new design point and set an input parameter

>>> dp1 = study.add_design_point("DP1")
>>> dp1.set_input("parameter_1", 0.235)
>>> dp1.set_input("velocity_inlet_5_y_velocity", 0.772)

The solver has not been run yet so no outputs are computed
The design point is out of date

>>> assert(dp1.status == DesignPointStatus.OUT_OF_DATE)

Get the base design point

>>> base = study.design_point("Base DP")

Check that block updates works

>>> dp1.block_updates()
>>> base.block_updates()
>>> assert(dp1.status == DesignPointStatus.BLOCKED)
>>> study.update_all()
>>> assert(dp1.outputs == base.outputs)

Update the design points

>>> dp1.allow_updates()
>>> base.allow_updates()
>>> assert(dp1.status == DesignPointStatus.OUT_OF_DATE)
>>> study.update_all()

Check that dp1 is up to date and that the outputs differ

>>> assert(dp1.status == DesignPointStatus.UPDATED)
>>> assert(dp1.outputs != base.outputs)

It's important to clean up any studies to help ensure that
all Fluent sessions are cleaned up

>>> del study
"""

from enum import Enum

import ansys.fluent.solver as pyfluent


class DesignPointStatus(Enum):
    """
    Status of a design point in a parametric study.

    Attributes
    ----------
    OUT_OF_DATE : int
    UPDATING : int
    UPDATED : int
    FAILED : int
    BLOCKED : int
    """

    OUT_OF_DATE = 1
    UPDATING = 2
    UPDATED = 3
    FAILED = 4
    BLOCKED = 5


class DesignPoint:
    """
    Design point in a parametric study.

    Attributes
    ----------
    name : str
        Name of the design point as a str.
    outputs : dict
        Dict of output parameters
        (name of parameter to value).
    inputs : dict
        Dict of input parameters
        (name of parameter to value).
    status : DesignPointStatus
        Current status of the design point.

    Methods
    -------
    set_input(parameter_name: str, value)
        Set one parameter in the design point to the value provided.
    on_end_updating(outputs: dict)
        Inform the design point that it is in an UPDATED state and
        provides the associated output parameters.
    block_updates()
        Move the design point into a do not update state.
    block_updates()
        Move the design point into a needs update state.
    """

    def __init__(self, design_point_name: str, base_design_point=None):
        self.name = design_point_name
        if base_design_point:
            self.__inputs = base_design_point.inputs.copy()
            self.__outputs = base_design_point.outputs.copy()
        else:
            self.__inputs = {}
            self.__outputs = {}
        # TODO add listener for __status:
        self.__status = DesignPointStatus.OUT_OF_DATE

    @property
    def inputs(self) -> dict:
        return self.__inputs

    @inputs.setter
    def inputs(self, inputs: dict):
        self.__status = DesignPointStatus.OUT_OF_DATE
        self.__inputs = inputs

    @property
    def outputs(self) -> dict:
        return self.__outputs

    @outputs.setter
    def outputs(self, outputs: dict):
        self.__status = DesignPointStatus.OUT_OF_DATE
        self.__outputs = outputs

    @property
    def status(self) -> DesignPointStatus:
        return self.__status

    def set_input(self, parameter_name: str, value):
        self.__status = DesignPointStatus.OUT_OF_DATE
        self.__inputs[parameter_name] = value

    def on_start_updating(self):
        self.__status = DesignPointStatus.UPDATING

    def on_end_updating(self, outputs: dict):
        self.__outputs = outputs
        self.__status = DesignPointStatus.UPDATED

    def block_updates(self):
        self.__status = DesignPointStatus.BLOCKED

    def allow_updates(self):
        self.__status = DesignPointStatus.OUT_OF_DATE


class DesignPointTable(list):
    """
    Design point study in a parametric study

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

    def __init__(self, base_design_point: DesignPoint):
        super().__init__()
        self.append(base_design_point)

    def add_design_point(self, design_point_name: str) -> DesignPoint:
        self.append(DesignPoint(design_point_name, self[0]))
        return self[-1]

    def find_design_point(self, idx_or_name) -> DesignPoint:
        if isinstance(idx_or_name, int):
            return self[idx_or_name]
        for design_point in self:
            if idx_or_name == design_point.name:
                return design_point
        raise RuntimeError(f"Design point not found: {idx_or_name}")

    def remove_design_point(self, idx_or_name):
        design_point = self.find_design_point(idx_or_name)
        if design_point is self[0]:
            raise RuntimeError("Cannot remove base design point")
        self.remove(self.find_design_point(idx_or_name))


class FluentParameterAccessor:
    """
    Extracts parameter name to value dicts from table strs
    currently returned by the API

    Attributes
    ----------
    input_parameters : dict
        The current input parameter dict.
    output_parameters : dict
        The current input parameter dict.
    """

    def __init__(self, fluent_session):
        self.__list_parameters = (
            fluent_session.tui.solver.define.parameters.list_parameters
        )

    @property
    def input_parameters(self) -> dict:
        return FluentParameterAccessor.__parameter_table_to_dict(
            self.__list_parameters.input_parameters()
        )

    @property
    def output_parameters(self) -> dict:
        return FluentParameterAccessor.__parameter_table_to_dict(
            self.__list_parameters.output_parameters()
        )

    @staticmethod
    def __parameter_table_to_dict(table: str) -> dict:
        # this code has become more complex now. Originally table was
        # str here - now ExecuteCommandResult is returned by the calls
        # to (in|out)put_parameters()
        table_str = table
        if not isinstance(table, str):
            try:
                table_str = table.result
            except AttributeError as attr_err:
                raise RuntimeError(
                    "Unexpected design point table "
                    f"type in parse: {type(table)}"
                ) from attr_err
        data_lines = table_str.splitlines()[3:]
        table_as_dict = {}
        for line in data_lines:
            line_as_list = line.split()
            table_as_dict[line_as_list[0]] = line_as_list[1]
        return table_as_dict


class ParametricSession:
    """
    Full set of interactions with Fluent in the context of a parametric study

    Attributes
    ----------
    input_parameters : dict
        The current input parameter dict.
    output_parameters : dict
        The current input parameter dict.

    Methods
    -------
    set_input_parameter(parameter_name: str)
        Set a single input parameter value in the Fluent session.
    initialize_with_case(case_file_name: str)
        Read the specified case into Fluent.
    update()
        Run the solver until convergence.
    """

    def __init__(self, fluent_session):
        self.__fluent_session = fluent_session
        self.__parameter_accessor = FluentParameterAccessor(fluent_session)

    @property
    def input_parameters(self) -> dict:
        return self.__parameter_accessor.input_parameters

    @property
    def output_parameters(self) -> dict:
        return self.__parameter_accessor.output_parameters

    def set_input_parameter(self, parameter_name: str, value):
        self.__fluent_session.tui.solver.define.parameters.input_parameters.edit(  # noqa: E501
            parameter_name, parameter_name, value
        )

    def initialize_with_case(self, case_file_name: str):
        self.__fluent_session.tui.solver.file.read_case(
            case_file_name=case_file_name
        )

    def update(self):
        self.__fluent_session.tui.solver.solve.initialize.initialize_flow()
        self.__fluent_session.tui.solver.solve.iterate()

    def __del__(self):
        self.__fluent_session.exit()


class FluentLauncher:
    """
    Launches fluent sessions.

    Methods
    -------
    __call__()
        Launch a session
    """

    def __call__(self):
        return ParametricSession(fluent_session=pyfluent.launch_fluent())


class ParametricStudy:
    """
    Parametric study that manages design points to parametrize a
    Fluent solver set-up. Provides ability to run Fluent for a series
    of design points, and access the inputs and outputs.

    Methods
    -------
    update_all()
        Bring all design point outputs up to date by running the
        solver on each design point. Ignores BLOCKED design points.
    update_design_point()
        Bring the outputs of the specified design point up to date
        by running the solver.
    add_design_point(design_point_name: str) -> DesignPoint
        Add a design point
    design_point(idx_or_name)
        Get a design point, either by name (str) or an index
        indicating the position in the table (by order of insertion).
        Raises
        ------
        RuntimeError
            If the design point is not found.
    """

    def __init__(
        self,
        case_file_name: str = "",
        base_design_point_name: str = "Base DP",
        launcher=FluentLauncher(),
    ):
        self.__session = launcher()
        if case_file_name:
            self.__session.initialize_with_case(case_file_name)
        base_design_point = DesignPoint(base_design_point_name)
        base_design_point.inputs = self.__session.input_parameters.copy()
        base_design_point.outputs = self.__session.output_parameters.copy()
        self.__design_point_table = DesignPointTable(base_design_point)

    def update_all(self):
        for design_point in self.__design_point_table:
            if design_point.status != DesignPointStatus.BLOCKED:
                self.update_design_point(design_point)

    def update_design_point(self, design_point: DesignPoint):
        design_point.on_start_updating()
        for parameter_name, value in design_point.inputs.items():
            self.__session.set_input_parameter(parameter_name, value)
        self.__session.update()
        design_point.on_end_updating(
            outputs=self.__session.output_parameters.copy()
        )

    def add_design_point(self, design_point_name: str) -> DesignPoint:
        return self.__design_point_table.add_design_point(design_point_name)

    def design_point(self, idx_or_name) -> DesignPoint:
        return self.__design_point_table.find_design_point(idx_or_name)
