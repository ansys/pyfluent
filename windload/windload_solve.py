
import os

from ansys.fluent.core.async_execution import asynchronous

#@asynchronous
def create_workflow(read_mesh, input_object):
    import ansys.fluent as pyfluent
    session = pyfluent.launch_fluent()
    workflow = SolverWorkflow(
        session, 
        input_object=input_object or InputObject(),
        mesh_reader=read_mesh)
    return workflow


class InputObject:
    def __init__(self):       
        self.hydraulic_diameter = 1.25
        self.density = 1.25
        self.inlet_velocity = 41.67
        self.unit_length = 0.001
        self.unit_width = 0.001
        self.turbulence_model_name = "ke-realizable"
        self.iteration_for_average_report = 1
        self.iterations_number = 10
    

class SolverWorkflow:
    def __init__(self, session, input_object, mesh_reader):
        self.session = session
        self.solver = session.tui.solver
        self.api_root = session.get_settings_root()
        self.scheme_str_eval = session.scheme_eval.string_eval
        self.hydraulic_diameter = input_object.hydraulic_diameter
        self.density = input_object.density
        self.inlet_velocity = input_object.inlet_velocity
        self.unit_length = input_object.unit_length
        self.unit_width = input_object.unit_width
        self.turbulence_model_name = input_object.turbulence_model_name
        self.iteration_for_average_report = input_object.iteration_for_average_report
        self.iterations_number = input_object.iterations_number 
        self.mesh_reader = mesh_reader
       
    def read_mesh(self):
        self.mesh_reader(self.session)

    def calculate(self):
        self.solver.solve.iterate(self.iterations_number)
       
    def initialize(self):
        self.solver.solve.initialize.hyb_initialization()
       
    def create_report_definitions(self):
        
        reportCmd = """

        (ti-menu-load-string (format #f "solve/report-definition/add drag_unit lift average-over 1 scaled? no thread-names wallunit () q"))

        (ti-menu-load-string (format #f "solve/report-definition/add c_d_unit lift average-over 1 scaled? yes thread-names wallunit () q"))

        (ti-menu-load-string (format #f "solve/report-definition/add sideforce_unit drag average-over 1 scaled? no thread-names wallunit () q"))

        (ti-menu-load-string (format #f "solve/report-definition/add c_s_unit drag average-over 1 scaled? yes thread-names wallunit () q"))

        """
        self.scheme_str_eval(reportCmd)
        
        self.solver.define.parameters.output_parameters.create("report-definition", "drag_unit")

    def set_discretization_scheme(self):
        self.solver.solve.set.discretization_scheme("k", 1)
        if self.turbulence_model_name == "ke-realizable":
            self.solver.solve.set.discretization_scheme("epsilon", 1)
        else:
            self.solver.solve.set.discretization_scheme("omega", 1)
        
    def set_up_reference_values(self):
        self.solver.report.reference_values.area(self.unit_length * self.unit_width)
        self.solver.report.reference_values.density(self.density)
        self.solver.report.reference_values.velocity(self.inlet_velocity)
        self.solver.report.reference_values.zone("farfield")
        
    def set_up_turbulence_model(self):
        if self.turbulence_model_name == "ke-realizable":
            self.solver.define.models.viscous.ke_realizable("yes")
            self.solver.define.models.viscous.near_wall_treatment.enhanced_wall_treatment("yes")
        if self.turbulence_model_name == "kw-sst":
            self.solver.define.models.viscous.kw_sst("yes")
        
    def set_up_boundary_conditions(self):
        reynolds = (self.density * self.inlet_velocity * self.hydraulic_diameter)/1.7894e-5
        turbulence_intensity = 0.16*pow(reynolds, -0.125)  
        inlet = self.api_root.setup.boundary_conditions.velocity_inlet['velocityinlet']
        inlet.turb_intensity = turbulence_intensity
        inlet.vmag.constant = self.inlet_velocity
        #inlet.turb_hydraulic_diam = self.hydraulic_diameter
             
        outlet = self.api_root.setup.boundary_conditions.pressure_outlet['pressureoutlet']
        outlet.turb_intensity = turbulence_intensity
        #outlet.turb_hydraulic_diam = self.hydraulic_diameter

    def set_up_materials(self):
        self.solver.define.materials.change_create("air", "air", "yes", "constant", self.density)
          
    def report_value(self):
        def parameter_table_str_to_dict(table: str) -> dict:
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
        parameter_dict = parameter_table_str_to_dict(
           self.solver.define.parameters.list_parameters.output_parameters().result()
           )
        lift = parameter_dict["drag_unit-op"]
        print("Inlet velocity =", self.inlet_velocity, " Lift =", lift)
        

    def run(self):
        i = 0
        print(i); i = i + 1
        self.set_up_materials(); print(i); i = i + 1
        self.set_up_turbulence_model(); print(i); i = i + 1
        self.set_up_boundary_conditions(); print(i); i = i + 1
        self.set_up_reference_values(); print(i); i = i + 1
        self.set_discretization_scheme(); print(i); i = i + 1
        self.create_report_definitions(); print(i); i = i + 1
        self.initialize(); print(i); i = i + 1
        self.calculate(); print(i); i = i + 1
        self.report_value(); print(i); i = i + 1

