###
### Copyright 1987-2022 ANSYS, Inc. All Rights Reserved.
###   

from enum import Enum

class DesignPointStatus(Enum):
    needs_update = 1
    updating = 2
    updated = 3
    failed = 4
    do_not_update = 5


class DesignPoint(object):

    def __init__(self, name: str, base_design_point=None):
        self.__name = name
        if base_design_point:
            self.__inputs = base_design_point.inputs().copy()
            self.__outputs = base_design_point.outputs().copy()
        else:
            self.__inputs = dict()
            self.__outputs = dict()
        self.__status = DesignPointStatus.needs_update

    def name(self):
        return self.__name

    def inputs(self):
        return self.__inputs
        
    def outputs(self):
        return self.__outputs
        
    def set_input(self, parameter_name, value):
        self.__inputs[parameter_name] = value
        
    def update_intputs(self, inputs):
        self.__inputs = inputs

    def update_outputs(self, outputs):
        self.__outputs = outputs


class DesignPointTable(list):

    def __init__(self, base_design_point: DesignPoint):
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


class FluentParameterAccessor(object):

    def __init__(self, fluent_session):
        self.__list_parameters = fluent_session.tui.define.parameters.list_parameters
        
    def input_parameters(self) -> dict:
        return self.__parameter_table_to_dict(self.__list_parameters.input_parameters())
        
    def output_parameters(self) -> dict:
        return self.__parameter_table_to_dict(self.__list_parameters.output_parameters())
    
    # static
    def __parameter_table_to_dict(self, table: str) -> dict:
        data_lines = table.splitlines()[3:]
        table_as_dict = {}
        for line in data_lines:
            line_as_list = line.split()
            table_as_dict[line_as_list[0]] = line_as_list[1]
        return table_as_dict
            

class ParametricSession(object):

    def __init__(self, fluent_session):
        self.__fluent_session = fluent_session
        self.__parameter_accessor = FluentParameterAccessor(fluent_session)

    def input_parameters(self):
        return self.__parameter_accessor.input_parameters()
        
    def output_parameters(self):
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

class FluentLauncher(object):

    def __call__(self):
        import ansys.fluent.solver as pyfluent
        session = pyfluent.launch_fluent()
        parametric_session = ParametricSession(fluent_session=session)
        return parametric_session


class ParametricStudy(object):

    def __init__(self, case_file_name: str, base_design_point_name: str = "Base DP", launcher = FluentLauncher()):
        self.__session = launcher()
        self.__session.initialize_with_case(case_file_name)
        base_design_point = DesignPoint(base_design_point_name)
        base_design_point.update_intputs(self.__session.input_parameters().copy())
        self.__design_point_table = DesignPointTable(base_design_point)

    def update_all(self):
        for design_point in self.__design_point_table:
            self.update_design_point(design_point)

    def update_design_point(self, design_point):
        for parameter_name, value in design_point.inputs().items():
            self.__session.set_input_parameter(parameter_name, value)
        self.__session.update()
        outputs = self.__session.output_parameters()
        design_point.update_outputs(outputs.copy())

    def add_design_point(self, design_point_name: str) -> DesignPoint:
        return self.__design_point_table.add_design_point(design_point_name)

    def set_input_parameter(self, design_point_idx_or_name, parameter_name, value):
        self.design_point(design_point_idx_or_name).set_input(parameter_name, value)

    def design_point(self, idx_or_name) -> DesignPoint:
        return self.__design_point_table.find_design_point(idx_or_name)
