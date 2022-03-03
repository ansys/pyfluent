
import os

def run(read_mesh, input_object=None):
    import ansys.fluent as pyfluent
    session = pyfluent.launch_fluent()
    read_mesh(session)
    workflow = SolverWorkflow(session, input_object=input_object or InputObject())
    workflow.run()
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
    def __init__(self, session, input_object):
        self.solver = session.tui.solver
        self.api_root = session.get_settings_root()
        self.scheme_str_eval = session._Session__scheme_eval.string_eval
        self.hydraulic_diameter = input_object.hydraulic_diameter
        self.density = input_object.density
        self.inlet_velocity = input_object.inlet_velocity
        self.unit_length = input_object.unit_length
        self.unit_width = input_object.unit_width
        self.turbulence_model_name = input_object.turbulence_model_name
        self.iteration_for_average_report = input_object.iteration_for_average_report
        self.iterations_number = input_object.iterations_number     
       
    def calculation(self):
        self.solver.solve.iterate(self.iterations_number)
       
    def initialization(self):
        self.solver.solve.initialize.hyb_initialization()
       
    def report(self):

        reportCmd = """

        (ti-menu-load-string (format #f "solve/report-definition/add drag_unit lift average-over ~a scaled? no thread-names wallunit:1 () q" (rpgetvar 'iteration-for-average-report)))

        (ti-menu-load-string (format #f "solve/report-definition/add c_d_unit lift average-over ~a scaled? yes thread-names wallunit:1 () q" (rpgetvar 'iteration-for-average-report)))

        (ti-menu-load-string (format #f "solve/report-definition/add sideforce_unit drag average-over ~a scaled? no thread-names wallunit:1 () q" (rpgetvar 'iteration-for-average-report)))

        (ti-menu-load-string (format #f "solve/report-definition/add c_s_unit drag average-over ~a scaled? yes thread-names wallunit:1 () q" (rpgetvar 'iteration-for-average-report)))

        """
        reportCmd = """

        (ti-menu-load-string (format #f "solve/report-definition/add drag_unit lift average-over 1 scaled? no thread-names wallunit () q"))

        (ti-menu-load-string (format #f "solve/report-definition/add c_d_unit lift average-over 1 scaled? yes thread-names wallunit () q"))

        (ti-menu-load-string (format #f "solve/report-definition/add sideforce_unit drag average-over 1 scaled? no thread-names wallunit () q"))

        (ti-menu-load-string (format #f "solve/report-definition/add c_s_unit drag average-over 1 scaled? yes thread-names wallunit () q"))

        """
        self.scheme_str_eval(reportCmd)

        '''
        iteration_for_average_report = 1
        solution=self.solver.get_case().get_solution()
        solution.add_report_definition(name='%lift_unit%', oneof_type="LIFT")
        drag_unit=solution.get_report_definition('lift_unit')
        drag_unit.oneof_type = "LIFT"
        drag_unit=drag_unit.get_lift()
        drag_unit.average_over=iteration_for_average_report
        drag_unit.scaled=False
        drag_unit.thread_names=['wallunit']
    
        solution.add_report_definition(name="%c_d_unit%", oneof_type="LIFT")
        c_d_unit=solution.get_report_definition("c_d_unit")
        c_d_unit.oneof_type = "LIFT"
        c_d_unit=c_d_unit.get_lift()
        c_d_unit.average_over=iteration_for_average_report
        c_d_unit.scaled=True
        c_d_unit.thread_names=['wallunit']
                
    
        solution.add_report_definition(name="%drag_unit%", oneof_type="DRAG")
        sideforce_unit=solution.get_report_definition("drag_unit")
        sideforce_unit.oneof_type = "DRAG"
        sideforce_unit=sideforce_unit.get_drag()
        sideforce_unit.average_over=iteration_for_average_report
        sideforce_unit.scaled=False
        sideforce_unit.thread_names=['wallunit']
    
        solution.add_report_definition(name="%c_s_unit%", oneof_type="DRAG")
        c_s_unit=solution.get_report_definition("c_s_unit")
        c_s_unit.oneof_type = "DRAG"
        c_s_unit=c_s_unit.get_drag()
        c_s_unit.average_over=2
        c_s_unit.scaled=True
        c_s_unit.thread_names=['wallunit']
        
        solution.add_report_plot(name='%report-plot-lift%')
        coeff_plots=solution.get_report_plot("report-plot-lift")
        coeff_plots.report_defs = ["lift_unit"] # ["c_s_unit", "c_d_unit"] 
        
        solution.add_report_plot(name='%report-plot-drag%')
        drag_plots=solution.get_report_plot("report-plot-drag")
        drag_plots.report_defs = ["drag_unit"]          
        '''
                  
    def discretization(self):
        self.solver.solve.set.discretization_scheme("k", 1)
        if self.turbulence_model_name == "ke-realizable":
            self.solver.solve.set.discretization_scheme("epsilon", 1)
        else:
            self.solver.solve.set.discretization_scheme("omega", 1)
        
    def reference_value(self):
        self.solver.report.reference_values.area(self.unit_length * self.unit_width)
        self.solver.report.reference_values.density(self.density)
        self.solver.report.reference_values.velocity(self.inlet_velocity)
        self.solver.report.reference_values.zone("farfield")
        
    def turbulence_model(self):
        if self.turbulence_model_name == "ke-realizable":
            self.solver.define.models.viscous.ke_realizable("yes")
            self.solver.define.models.viscous.near_wall_treatment.enhanced_wall_treatment("yes")
        if self.turbulence_model_name == "kw-sst":
            self.solver.define.models.viscous.kw_sst("yes")
        
    def boundary_condition(self):
        reynolds = (self.density * self.inlet_velocity * self.hydraulic_diameter)/1.7894e-5
        turbulence_intensity = 0.16*pow(reynolds, -0.125)  
        inlet = self.api_root.setup.boundary_conditions.velocity_inlet['velocityinlet']
        inlet.turb_intensity = turbulence_intensity
        inlet.vmag.constant = self.inlet_velocity
        #inlet.turb_hydraulic_diam = self.hydraulic_diameter
             
        outlet = self.api_root.setup.boundary_conditions.pressure_outlet['pressureoutlet']
        outlet.turb_intensity = turbulence_intensity
        #outlet.turb_hydraulic_diam = self.hydraulic_diameter

    def material(self):
        self.solver.define.materials.change_create("air", "air", "yes", "constant", self.density)
           
    def run(self):
        self.material()
        self.turbulence_model()
        self.boundary_condition()
        self.reference_value()
        self.discretization()
        self.report()
        self.initialization()
        self.calculation()

