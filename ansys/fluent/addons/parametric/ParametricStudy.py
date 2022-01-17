###
### Copyright 1987-2022 ANSYS, Inc. All Rights Reserved.
###   


class ParametricStudy(object):
    def __init__(self, launcher, case_file_name):
        self.__launcher = launcher
        self.__case_file_name = case_file_name
        self.__design_points = [(dict(), dict())]

    def update_all(self):
        for design_point in self.__design_points:
            self.__run_design_point(design_point)
            
    def update_design_point(self, design_point):
        self.__run_design_point(design_point)

    def new_design_points(self, count):
        self.__design_points.extend(count * [(dict(), dict())])
        
    def set_parameter(self, idx, name, value):
        self.__design_points[idx][0][name] = value
        
    def input_parameter(self, idx, name):
        if idx == 0:
            return self.__base_dp_parameter(name)
        return self.__design_points[idx][0][name]
        
    def output_parameter(self, idx, name):
        if idx == 0:
            return None # self.__base_dp_parameter(name)
        return self.__design_points[idx][1][name]

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
