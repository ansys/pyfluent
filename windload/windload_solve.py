
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
        self.inletVelocity = 41.67
        self.unitLength = 0.001
        self.unitWidth = 0.001
        self.turbulenceModel = "ke-realizable"
        self.iterationForAverageReport = 1
        self.iterationsNumber = 10
    

class SolverWorkflow:
    def __init__(self, session, input_object):
        self.solver = session.tui.solver
        self.api_root = session.get_settings_root()
        self.hydraulic_diameter = input_object.hydraulic_diameter
        self.density = input_object.density
        self.inletVelocity = input_object.inletVelocity
        self.unitLength = input_object.unitLength
        self.unitWidth = input_object.unitWidth
        self.turbulenceModel = input_object.turbulenceModel
        self.iterationForAverageReport = input_object.iterationForAverageReport
        self.iterationsNumber = input_object.iterationsNumber     
       
    def calculation(self):
        calculation=self.solver.get_case().get_solution().get_calculation()
        if calculation.oneof_analysis_type=="STEADY_ANALYSIS":
            steady_analysis=calculation.get_steady_analysis()      
            number_of_iterations = self.iterationsNumber
            steady_analysis.number_of_iterations=number_of_iterations
            calculation.calculate()
       
    def initialization(self):
        initialization=self.solver.get_case().get_solution().get_initialization()
        initialization.hybrid_initialization()
       
    def report(self):
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
                  
        
    def discretization(self):
        tke= self.solver.get_case().get_solution().get_methods().get_discretization_schemes("Turbulent Kinetic Energy")                 
        tke.value='Second Order Upwind'
        epsilon=self.solver.get_case().get_solution().get_methods().get_discretization_schemes("Turbulent Dissipation Rate")
        epsilon.value="Second Order Upwind"                            
        
    def reference_value(self):
        reference_values= self.solver.get_case().get_results().get_report().get_reference_values()
        w.solver_workflow.solver.report.reference_values.area(self.unitLength * self.unitWidth)
        w.solver_workflow.solver.report.reference_values.density(self.density)
        w.solver_workflow.solver.report.reference_values.velocity(self.self.inletVelocity)
        w.solver_workflow.solver.report.reference_values.zone("farfield")
        reference_values.density=1.25
        reference_values.velocity=self.inletVelocity
        reference_values.zone= "farfield"
        
        
    def turbulence_model(self):
        if self.turbulenceModel == "ke-realizable":
            self.solver_workflow.solver.define.models.viscous.ke_realizable("yes")
            self.solver_workflow.solver.define.models.viscous.near_wall_treatment.enhanced_wall_treatment("yes")
        if self.turbulenceModel == "kw-sst":
            self.solver_workflow.solver.define.models.viscous.kw_sst("yes")
        
    def boundary_condition(self):
        reynolds = (self.density * self.inlet_velocity * self.hydraulic_diameter)/1.7894e-5
        turbulence_intensity=0.16*pow(reynolds, -0.125)  
        '''
        setup=self.solver.get_case().get_setup()
        bc=setup.get_boundary_condition("velocityinlet").get_velocity_inlet()
        bc.oneof_velocity_spec = 'MAGNITUDE_NORMAL_TO_BOUNDARY'
        
        bc.get_magnitude_normal_to_boundary().magnitude= self.inletVelocity        
        k_e_realizable = bc.get_ke_realizable()
        k_e_realizable.oneof_ke_spec='INTENSITY_AND_HYDRAULIC_DIAMETER'
        i_hd=k_e_realizable.get_intensity_and_hydraulic_diameter()        
        i_hd.hydraulic_diameter=self.hydraulic_diameter
        i_hd.intensity=turbulence_intensity
        '''
        inlet = self.api_root.setup.boundary_conditions.velocity_inlet['velocityinlet']
        inlet.turb_intensity = turbulence_intensity
        inlet.turb_hydraulic_diam = self.hydraulic_diameter
             
        outlet = self.api_root.setup.boundary_conditions.pressure_outlet['pressureoutlet']
        outlet.turb_intensity = turbulence_intensity
        outlet.turb_hydraulic_diam = self.hydraulic_diameter
        '''
        bc=setup.get_boundary_condition("pressureoutlet").get_pressure_outlet()
        k_e_realizable = bc.get_ke_realizable_outlet()
        k_e_realizable.oneof_ke_spec_outlet='INTENSITY_AND_HYDRAULIC_DIAMETER_OUTLET'
        i_hd=k_e_realizable.get_intensity_and_hydraulic_diameter_outlet()
        i_hd.hydraulic_diameter= self.hydraulic_diameter
        i_hd.intensity= turbulence_intensity 
        '''
      
        
    def material(self):
        self.solver.define.materials.change_create("air", "air", "yes", "constant", self.density)
           
    def run(self):
        self.material()
        self.turbulence_model()
        self.boundary_condition()
        self.reference_value()
        '''
        self.discretization()
        self.report()
        self.initialization()
        self.calculation()
        '''
