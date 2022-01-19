###
### Copyright 1987-2022 ANSYS, Inc. All Rights Reserved.
###   
"""
Classes for running a parametric study in Fluent.

Example
-------
from ansys.fluent.addons.parametric.ParametricStudy import ParametricStudy, DesignPointStatus
# instantiate the study, specifying the case
study = ParametricStudy(case_file_name=my_case_file_name)
# add one new design point and set an input parameter
dp1 = study.add_design_point('DP1')
dp1.set_input('parameter_1', 0.235)
dp1.set_input('velocity_inlet_5_y_velocity', 0.772)
# the solver has not been run yet so no ouputs are computed
# the design point is out of date
assert(dp1.status() == DesignPointStatus.out_of_date)
# get the base design point
base = study.design_point('Base DP')
# check that block updates works
dp1.block_updates()
base.block_updates()
assert(dp1.status() == DesignPointStatus.blocked)
study.update_all()
assert(dp1.outputs() == base.outputs())
# update the design points
dp1.allow_updates()
base.allow_updates()
assert(dp1.status() == DesignPointStatus.out_of_date)
study.update_all()
# check that dp1 is up to date and that its outputs differ from the base design point
assert(dp1.status() == DesignPointStatus.updated)
assert(dp1.outputs() != base.outputs())
"""

from enum import Enum

class DesignPointStatus(Enum):
    """
    Status of a design point in a parametric study.

    Attributes
    ----------
    out_of_date : int
    updating : int
    updated : int
    failed : int
    blocked : int
    """
    out_of_date = 1
    updating = 2
    updated = 3
    failed = 4
    blocked = 5


class DesignPoint:
    """
    Design point in a parametric study.

    Methods
    -------
    name()
        Get name of the design point as a str.
    outputs() -> dict
        Get dict of output parameters (name of parameter to value).
    inputs() -> dict
        Get dict of input parameters (name of parameter to value).
    status() -> DesignPointStatus
        Get the current status of the design point.
    set_input(parameter_name: str, value)
        Set one parameter in the design point to the value provided.
    update_intputs(inputs :dict)
        Overwrite the input parameters with the provided inputs.
    on_end_updating(outputs: dict)
        Inform the design point that it is in an updated state and provides
        the associated output parameters.
    block_updates()
        Move the design point into a do not update state.
    block_updates()
        Move the design point into a needs update state.
    """
    def __init__(self, design_point_name: str, base_design_point=None):
        self.__name = design_point_name
        if base_design_point:
            self.__inputs = base_design_point.inputs().copy()
            self.__outputs = base_design_point.outputs().copy()
        else:
            self.__inputs = dict()
            self.__outputs = dict()
        # TODO add listener for __status:
        self.__status = DesignPointStatus.out_of_date

    def name(self) -> str:
        return self.__name

    def inputs(self) -> dict:
        return self.__inputs
        
    def outputs(self) -> dict:
        return self.__outputs

    def status(self) -> DesignPointStatus:
        return self.__status
        
    def set_input(self, parameter_name: str, value):
        self.__status = DesignPointStatus.out_of_date
        self.__inputs[parameter_name] = value
        
    def update_intputs(self, inputs: dict):
        self.__status = DesignPointStatus.out_of_date
        self.__inputs = inputs

    def on_end_updating(self, outputs):
        self.__outputs = outputs
        self.__status = DesignPointStatus.updated

    def on_start_updating(self):
        self.__status = DesignPointStatus.updating

    def block_updates(self):
        self.__status = DesignPointStatus.blocked
        
    def allow_updates(self):
        self.__status = DesignPointStatus.out_of_date


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
            if idx_or_name == design_point.name():
                return design_point
        raise RuntimeError("Design point not found: " + repr(idx_or_name))


class FluentParameterAccessor:
    """
    Extracts parameter name to value dicts from table strs currenty returned by the API 

    Methods
    -------
    input_parameters() -> dict
        Get the current input parameter dict.
    output_parameters() -> dict
        Get the current input parameter dict.
    """

    def __init__(self, fluent_session):
        self.__list_parameters = fluent_session.tui.define.parameters.list_parameters
        
    def input_parameters(self) -> dict:
        return FluentParameterAccessor.__parameter_table_to_dict(self.__list_parameters.input_parameters())
        
    def output_parameters(self) -> dict:
        return FluentParameterAccessor.__parameter_table_to_dict(self.__list_parameters.output_parameters())
    
    @staticmethod
    def __parameter_table_to_dict(table: str) -> dict:
        data_lines = table.splitlines()[3:]
        table_as_dict = {}
        for line in data_lines:
            line_as_list = line.split()
            table_as_dict[line_as_list[0]] = line_as_list[1]
        return table_as_dict
            

class ParametricSession:
    """
    Full set of interactions with Fluent inthe context of a parametric study

    Methods
    -------
    input_parameters() -> dict
        Get the current input parameter dict.
    output_parameters() -> dict
        Get the current input parameter dict.
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

    def input_parameters(self) -> dict:
        return self.__parameter_accessor.input_parameters()
        
    def output_parameters(self) -> dict:
        return self.__parameter_accessor.output_parameters()

    def set_input_parameter(self, parameter_name: str, value):
        self.__fluent_session.tui.define.parameters.input_parameters.edit(parameter_name, parameter_name, value)

    def initialize_with_case(self, case_file_name: str):
        self.__fluent_session.tui.file.read_case(case_file_name=case_file_name)

    def update(self):
        self.__fluent_session.tui.solve.initialize.initialize_flow()
        self.__fluent_session.tui.solve.iterate()
        
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
        import ansys.fluent.solver as pyfluent
        return ParametricSession(fluent_session=pyfluent.launch_fluent())


class ParametricStudy:
    """
    Parametric study that manages design points to parametrize a Fluent solver
    set-up. Provides ability to run Fluent for a series of design points, and
    access the inputs and outputs.

    Methods
    -------
    update_all()
        Bring all design point outputs up to date by running the solver on each design point.
        Ignores blocked design points (not yet implemented).
    update_design_point()
        Bring the outputs of the specified design point up to date by running the solver.
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
    def __init__(self, case_file_name: str, base_design_point_name: str = "Base DP", launcher = FluentLauncher()):
        self.__session = launcher()
        self.__session.initialize_with_case(case_file_name)
        base_design_point = DesignPoint(base_design_point_name)
        base_design_point.update_intputs(self.__session.input_parameters().copy())
        self.__design_point_table = DesignPointTable(base_design_point)

    def update_all(self):
        for design_point in self.__design_point_table:
            if design_point.status() != DesignPointStatus.blocked:
                self.update_design_point(design_point)

    def update_design_point(self, design_point: DesignPoint):
        design_point.on_start_updating()
        for parameter_name, value in design_point.inputs().items():
            self.__session.set_input_parameter(parameter_name, value)
        self.__session.update()
        design_point.on_end_updating(outputs=self.__session.output_parameters().copy())

    def add_design_point(self, design_point_name: str) -> DesignPoint:
        return self.__design_point_table.add_design_point(design_point_name)

    def design_point(self, idx_or_name) -> DesignPoint:
        return self.__design_point_table.find_design_point(idx_or_name)
