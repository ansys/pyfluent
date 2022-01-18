###
### Copyright 1987-2022 ANSYS, Inc. All Rights Reserved.
###   


class ParametricStudy(object):

    def __init__(self, launcher, case_file_name, design_point_count):
        self.__launcher = launcher
        self.__case_file_name = case_file_name
        self.__design_points = design_point_count * [(dict(), dict())]

    def update_all(self):
        for design_point in self.__design_points:
            self.__run_design_point(design_point)
            
    def update_design_point(self, design_point):
        self.__run_design_point(design_point)

    def set_parameter(self, design_point_idx, name, value):
        self.__design_points[design_point_idx][0][name] = value
        
    def input_parameter(self, design_point_idx, name):
        return self.__parameter(design_point_idx, True, name)
        
    def output_parameter(self, design_point_idx, name):
        return self.__parameter(design_point_idx, False, name)

    # can be static
    def __run_design_point(self, design_point):
        import ansys.fluent.solver as pyfluent
        session = pyfluent.launch_fluent()
        session.tui.file.read_case(case_file_name=self.__case_file_name)
        edit = session.tui.define.parameters.input_parameters.edit
        for name, value in design_point[0].items():
            edit(name, name, value)
        session.tui.solve.initialize.initialize_flow()
        session.tui.solve.iterate()
        #query parameter values here
        session.exit()

    def __parameter(self, design_point_idx, is_input, name):
        return self.__design_points[design_point_idx][0 if is_input else 1][name]
        
