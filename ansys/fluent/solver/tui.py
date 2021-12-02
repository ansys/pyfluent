# This is an auto-generated file.  DO NOT EDIT!

from ansys.fluent.solver.meta import PyMenuMeta


doc_by_method = {
    'close_fluent' : 'Exit program.',
    'exit' : 'Exit program.',
    'switch_to_meshing_mode' : 'Switch to meshing mode.',
    'print_license_usage' : 'Print license usage information',
}
class adjoint(metaclass=PyMenuMeta):
    """Adjoint."""
    doc_by_method = {
        'observable' : 'Observable menu.',
        'methods' : 'Methods menu.',
        'controls' : 'Controls menu.',
        'monitors' : 'Monitors menu.',
        'expert' : 'Expert menu.',
        'run' : 'Run menu.',
        'reporting' : 'Reporting.',
        'morphing' : 'Morphing menu.',
        'multi_objective' : 'Multi-Objective menu.',
        'design_tool' : 'Design tool menu.',
        'optimizer' : 'Optimizer menu.',
    }
class file(metaclass=PyMenuMeta):
    """Enter the file menu."""
    doc_by_method = {
        'single_precision_coordinates' : 'Indicate whether to write nodal coordinates in single precision.',
        'binary_legacy_files' : 'Indicate whether to write binary or text format case and data files.',
        'cff_files' : 'Indicate whether to write ANSYS common fluids format (CFF) files or legacy case and data files.',
        'async_optimize' : 'Choose whether to optimize file IO using scratch disks and asynchronous operations.',
        'write_pdat' : 'Indicate whether to attempt to save pdat files.',
        'confirm_overwrite' : 'Indicate whether or not to confirm attempts to overwrite existing files.',
        'define_macro' : 'Save input to a named macro.',
        'export_to_cfd_post' : 'Export to CFD-Post compabitble data file',
        'execute_macro' : 'Run a previously defined macro.',
        'read_settings' : 'Read and set boundary conditions from specified file.',
        'read_case' : 'Read a case file.
Arguments:
  case_file_name: str
',
        'read_case_data' : 'Read a case and a data file.',
        'read_data' : 'Read a data file.',
        'read_field_functions' : 'Read custom field-function definitions from a file.',
        'read_injections' : 'Read all DPM injections from a file.',
        'read_journal' : 'Read a journal file.',
        'read_macros' : 'Read macro definitions from a file.',
        'read_profile' : 'Read boundary profile data (*.prof, *.csv). Default is *.prof',
        'read_transient_table' : 'Read a table of transient boundary profile data.',
        'read_pdf' : 'Read a PDF file.',
        'read_rays' : 'Read a DTRM rays file.',
        'read_surface_clusters' : 'Read an S2S file.',
        'read_viewfactors' : 'Read an S2S file.',
        'read_isat_table' : 'Read an ISAT table.',
        'replace_mesh' : 'Replace the mesh with a new one while preserving settings.',
        'reload_setup' : 'Reload case and settings from last saved state',
        'close_without_save' : 'Exit without save',
        'sync_workbench' : 'Sync Fluent changes with WorkBench',
        'set_batch_options' : 'Set the batch options.',
        'set_idle_timeout' : 'Set the idle timeout',
        'show_configuration' : 'Display current release and version information.',
        'start_journal' : 'Start recording all input in a file.',
        'stop_journal' : 'Stop recording input and close the journal file.',
        'stop_macro' : 'Stop recording input to a macro.',
        'start_transcript' : 'Start recording input and output in a file.',
        'stop_transcript' : 'Stop recording input and output and close the transcript file.',
        'write_settings' : 'Write out current boundary conditions in use.',
        'write_boundary_mesh' : 'Write the boundary mesh to a file.',
        'write_case' : 'Write a case file.',
        'data_file_options' : 'Set derived quantities to be written in data file',
        'write_case_data' : 'Write a case and a data file.',
        'write_data' : 'Write a data file.',
        'write_fan_profile' : 'Compute radial profiles for a fan zone and write them to a profile file.',
        'write_field_functions' : 'Write the currently defined custom field functions to a file.',
        'write_profile' : 'Write surface data as a boundary profile file. To use *.csv format specify filename with .csv suffix',
        'write_currently_defined_profiles' : 'Write currently defined profiles. To use *.csv format specify filename with .csv suffix',
        'write_merge_profiles' : 'Write multiple zones surface data as a single boundary profile file. To use *.csv format specify filename with .csv suffix',
        'write_pdf' : 'Write a pdf file.',
        'write_flamelet' : 'Write a flamelet file.',
        'write_injections' : 'Write out selected DPM injections to a file.',
        'write_macros' : 'Write the currently defined macros to a file.',
        'write_isat_table' : 'Write an ISAT table.',
        'write_cleanup_script' : 'Write the cleanup-script-file for Fluent.',
        'load_act_tool' : 'Load ACT Start Page.',
        'set_tui_version' : 'Set the version of the TUI commands.',
    }
    class auto_save(metaclass=PyMenuMeta):
        """Enter the auto save menu."""
        doc_by_method = {
            'case_frequency' : 'Set the preference for saving case files.',
            'data_frequency' : 'Set the iteration or time step increment for saving data files.',
            'root_name' : 'Set the root name for auto-saved files. The number of iterations or time steps will be appended to this root name.',
            'retain_most_recent_files' : 'After the maximum (as in max-files) is reached, a file will be deleted for each file saved.',
            'max_files' : 'Set the maximum number of data files to save. After the maximum is reached, a file will be deleted for each file saved.',
            'append_file_name_with' : 'Set the suffix for auto-saved files. The file name can be appended by flow-time, time-step value or by user specified flags in file name.',
            'save_data_file_every' : 'Set the auto save frequency type to either time-step or crank-angle and set the corresponding frequency.',
        }
    class cffio_options(metaclass=PyMenuMeta):
        """CFF I/O options"""
        doc_by_method = {
            'io_mode' : 'Set CFF I/O mode.',
            'compression_level' : 'Set CFF file compression level.',
            'single_precision_data' : 'Specify whether the double-precision solver saves single-precision data when writing CFF data files.',
        }
    class export(metaclass=PyMenuMeta):
        """Enter the export menu."""
        doc_by_method = {
            'abaqus' : 'Write an ABAQUS file.',
            'mechanical_apdl' : 'Write an Mechanical APDL file.',
            'mechanical_apdl_input' : 'Write an Mechanical APDL Input file.',
            'ascii' : 'Write an ASCII file.',
            'common_fluids_format_post' : 'Write an CFF Post-Only file.',
            'avs' : 'Write an AVS UCD file.',
            'cdat_for_cfd_post__and__ensight' : 'Write a CDAT for CFD-Post & EnSight file.',
            'cgns' : 'Write a CGNS file.',
            'custom_heat_flux' : 'Write a generic file for heat transfer.',
            'dx' : 'Write an IBM Data Explorer format file.',
            'ensight' : 'Write EnSight 6 geometry, velocity, and scalar files.',
            'ensight_gold' : 'Write EnSight Gold geometry, velocity, and scalar files.',
            'ensight_gold_parallel_surfaces' : 'Write EnSight Gold geometry, velocity and scalar files for surfaces. Fluent will write files suitable for EnSight Parallel.',
            'ensight_gold_parallel_volume' : 'Write EnSight Gold geometry, velocity and scalar files for cell zones and boundaries attached to them. Fluent will write files suitable for EnSight Parallel.',
            'ensight_dvs_surfaces' : 'Write post-processing data(geometry, velocity and scalars) for surfaces using EnSight Dynamic Visualization Store Interface.',
            'ensight_dvs_volume' : 'Write post-processing data(geometry, velocity and scalars) for cell zones and boundaries attached to them using EnSight Dynamic Visualization Store Interface.',
            'icemcfd_for_icepak' : 'Write a binary ICEMCFD domain file.',
            'fast_mesh' : 'Write a FAST/Plot3D unstructured mesh file.',
            'fast_scalar' : 'Write a FAST/Plot3D unstructured scalar function file.',
            'fast_solution' : 'Write a FAST/Plot3D unstructured solution file.',
            'fast_velocity' : 'Write a FAST/Plot3D unstructured vector function file.',
            'fieldview' : 'Write Fieldview case and data files.',
            'fieldview_data' : 'Write Fieldview case and data files.',
            'fieldview_unstruct' : 'Write a Fieldview unstructured combined file.',
            'fieldview_unstruct_mesh' : 'Write a Fieldview unstructured mesh only file.',
            'fieldview_unstruct_data' : 'Write a Fieldview unstructured results only file.',
            'fieldview_unstruct_surfaces' : 'Write a Fieldview unstructured surface mesh, data',
            'fieldview_xdb' : 'Write a FieldView XDB format file.',
            'gambit' : 'Write a Gambit neutral file.',
            'ideas' : 'Write an IDEAS universal file.',
            'nastran' : 'Write a NASTRAN file.',
            'patran_neutral' : 'Write a PATRAN neutral file.',
            'patran_nodal' : 'Write a PATRAN nodal results file.',
            'taitherm' : 'Write a TAITherm file.',
            'tecplot' : 'Write a Tecplot+3DV format file.',
            'particle_history_data' : 'Export particle-history data.',
        }
        class system_coupling_definition_file_settings(metaclass=PyMenuMeta):
            """file menu"""
            doc_by_method = {
                'enable_automatic_creation_of_scp_file' : 'Enable/disable automatic creation of scp file during case write',
                'write_system_coupling_file' : 'Write a Fluent Input File for System Coupling',
            }
        class settings(metaclass=PyMenuMeta):
            """Enter the export settings menu"""
            doc_by_method = {
                'set_cgns_export_filetype' : 'Select HDF5 or ADF as file format for CGNS',
            }
    class transient_export(metaclass=PyMenuMeta):
        """Enter the export menu."""
        doc_by_method = {
            'abaqus' : 'Write an ABAQUS file.',
            'mechanical_apdl_input' : 'Write an Mechanical APDL Input file.',
            'ascii' : 'Write an ASCII file.',
            'avs' : 'Write an AVS UCD file.',
            'cdat_for_cfd_post__and__ensight' : 'Write a CDAT for CFD-Post & EnSight file.',
            'common_fluids_format_post' : 'Write an CFF Post-Only file.',
            'cgns' : 'Write a CGNS file.',
            'dx' : 'Write an IBM Data Explorer format file.',
            'ensight_gold_transient' : 'Write EnSight Gold geometry, velocity, and scalar files.',
            'ensight_gold_parallel_surfaces' : 'Write EnSight Gold geometry, velocity and scalar files for surfaces. Fluent will write files suitable for EnSight Parallel.',
            'ensight_gold_parallel_volume' : 'Write EnSight Gold geometry, velocity and scalar files for cell zones and boundaries attached to them. Fluent will write files suitable for EnSight Parallel.',
            'ensight_dvs_surfaces' : 'Write post-processing data(geometry, velocity and scalars) for surfaces using EnSight Dynamic Visualization Store Interface.',
            'ensight_dvs_volume' : 'Write post-processing data(geometry, velocity and scalars) for cell zones and boundaries attached to them using EnSight Dynamic Visualization Store Interface.',
            'ensight_gold_from_existing_files' : 'Write EnSight Gold files using Fluent case files.',
            'fast' : 'Write a FAST/Plot3D unstructured mesh velocity scalar file.',
            'fast_solution' : 'Write a FAST/Plot3D unstructured solution file.',
            'fieldview_unstruct' : 'Write a Fieldview unstructured combined file.',
            'fieldview_unstruct_mesh' : 'Write a Fieldview unstructured mesh only file.',
            'fieldview_unstruct_data' : 'Write a Fieldview unstructured results only file.',
            'fieldview_unstruct_surfaces' : 'Write a Fieldview unstructured combined file for surfaces.',
            'fieldview_xdb' : 'Write a FieldView XDB format file.',
            'ideas' : 'Write an IDEAS universal file.',
            'nastran' : 'Write a NASTRAN file.',
            'patran_neutral' : 'Write a PATRAN neutral file.',
            'taitherm' : 'Write a TAITherm file.',
            'tecplot' : 'Write a Tecplot+3DV format file.',
            'particle_history_data' : 'Setup an automatic particle-history data export.',
            'edit' : 'Edit transient exports',
            'delete' : 'Delete transient exports',
        }
        class settings(metaclass=PyMenuMeta):
            """Enter the automatic export settings menu"""
            doc_by_method = {
                'cfd_post_compatible' : 'Set settings for CFD-Post compatible file export',
            }
    class em_mapping(metaclass=PyMenuMeta):
        """Assign electro-magnetic losses provided by specified product."""
        doc_by_method = {
            'volumetric_energy_source' : 'Loss data provided by Ansoft will be assigned to Fluent for selected cell zones',
            'surface_energy_source' : 'Loss data provided by Ansoft will be assigned to Fluent for selected wall zones',
            'remove_loss_only' : 'Remove the loss data provided by Ansoft and keep all other solution data.',
            'maintain_loss_on_initialization' : 'Maintain the loss data provided by Ansoft even if solution is initialized',
        }
    class import(metaclass=PyMenuMeta):
        """Enter the import menu."""
        doc_by_method = {
            'chemkin_mechanism' : 'Read a CHEMKIN mechanism file.',
            'chemkin_report_each_line' : 'Enable/disable reporting after reading each line.',
            'fidap' : 'Read a FIDAP neutral file as a case file.',
            'fluent4_case' : 'Read a formatted Fluent 4 case file.',
            'gambit' : 'Read a GAMBIT neutral file as a case file.',
            'hypermesh' : 'Read a HYPERMESH file as a case file.',
            'ensight' : 'Read an Ensight file as a case file.',
            'ideas_universal' : 'Read an IDEAS Universal file as a case file.',
            'marc_post' : 'Read a MARC POST file as a case file.',
            'ptc_mechanica' : 'Read a PTC Mechanica file as a case file.',
            'prebfc_structured' : 'Read a formatted preBFC structured mesh (grid) file.',
        }
        class mechanical_apdl(metaclass=PyMenuMeta):
            """Enter the Mechanical APDL menu."""
            doc_by_method = {
                'input' : 'Read an Mechanical APDL file as a case file.',
                'result' : 'Read an Mechanical APDL result file as a case file.',
            }
        class abaqus(metaclass=PyMenuMeta):
            """Enter the Abaqus menu."""
            doc_by_method = {
                'fil' : 'Read an Abaqus .fil result file as a case file.',
                'input' : 'Read an Abaqus Input file as a case file.',
                'odb' : 'Read an Abaqus odb file as a case file.',
            }
        class cfx(metaclass=PyMenuMeta):
            """Enter the CFX menu."""
            doc_by_method = {
                'definition' : 'Read a CFX definition file as a case file.',
                'result' : 'Read a CFX result file as a case file.',
            }
        class cgns(metaclass=PyMenuMeta):
            """Enter the CGNS menu."""
            doc_by_method = {
                'mesh' : 'Read a CGNS file as a case file.',
                'data' : 'Read data from CGNS file.',
                'mesh_data' : 'Read a CGNS file as a case file.',
            }
        class fmu_file(metaclass=PyMenuMeta):
            """Read a FMU file."""
            doc_by_method = {
                'import_fmu' : 'Import a FMU file.',
                'define_fmu' : 'Link the FMU variables with Fluent parameters.',
                'select_fmu_local' : 'Select the FMU local variables to monitor.',
                'set_fmu_parameter' : 'Change the values of FMU parameter variables.',
            }
        class flamelet(metaclass=PyMenuMeta):
            """Import a flamelet file."""
            doc_by_method = {
                'standard' : 'Read a standard format flamelet file.',
                'cfx_rif' : 'Read a CFX-RIF format flamelet file.',
            }
        class lstc(metaclass=PyMenuMeta):
            """Enter the LSTC menu."""
            doc_by_method = {
                'input' : 'Read an LSTC input file as a case file.',
                'state' : 'Read an LSTC result file as a case file.',
            }
        class nastran(metaclass=PyMenuMeta):
            """Enter the NASTRAN menu."""
            doc_by_method = {
                'bulkdata' : 'Read a NASTRAN file as a case file.',
                'output2' : 'Read a NASTRAN op2 file as a case file.',
            }
        class partition(metaclass=PyMenuMeta):
            """Enter the partition menu."""
            doc_by_method = {
                'metis' : 'Read and partition a Fluent 5 case file.',
                'metis_zone' : 'Read and partition a Fluent 5 case file.',
            }
        class patran(metaclass=PyMenuMeta):
            """Enter the PATRAN menu."""
            doc_by_method = {
                'neutral' : 'Read a PATRAN Neutral file (zones defined by named components) as a case file.',
            }
        class plot3d(metaclass=PyMenuMeta):
            """Enter the PLOT3D menu."""
            doc_by_method = {
                'mesh' : 'Read a PLOT3D file as a case file.',
            }
        class tecplot(metaclass=PyMenuMeta):
            """Enter the Tecplot menu."""
            doc_by_method = {
                'mesh' : 'Read a Tecplot binary file as a case file.',
            }
    class interpolate(metaclass=PyMenuMeta):
        """Enter the interpolate menu."""
        doc_by_method = {
            'write_data' : 'Write data for interpolation.',
            'read_data' : 'Read and interpolate data.',
            'zone_selection' : 'Define a list of cell zone IDs. If specified, interpolation data will be
                read/written for these cell zones only.',
        }
    class fsi(metaclass=PyMenuMeta):
        """Enter the fsi menu."""
        doc_by_method = {
            'read_fsi_mesh' : 'Read an FEA mesh for one-way FSI.',
            'display_fsi_mesh' : 'Display the FEA mesh that has been read.',
            'write_fsi_mesh' : 'Write an FEA mesh file with Fluent data.',
            'conserve_force' : 'Conserve the forces for linear line, tri and tet elements',
        }
    class parametric_project(metaclass=PyMenuMeta):
        """Enter to create new project, read project, and save project"""
        doc_by_method = {
            'new' : 'Create New Project',
            'open' : 'Open project',
            'save' : 'Save Project',
            'save_as' : 'Save As Project',
            'save_as_copy' : 'Save As Copy',
            'archive' : 'Archive Project',
        }
    class table_manager(metaclass=PyMenuMeta):
        """Enter the table manager menu."""
        doc_by_method = {
            'delete' : 'Delete a table.',
            'list_matrix_data' : 'List matrix table data',
            'list_properties' : 'List the properties for a table.',
            'list_tables' : 'List the available tables.',
            'read_matrix_data_file' : 'Read matrix data file.',
            'read_rgp_file' : 'Read material from real gas property (RGP) file.',
            'rename' : 'Rename a table.',
            'store_in_case_file' : 'Set persistence mode for tables (in case or separate file).',
        }
    class solution_files(metaclass=PyMenuMeta):
        """enter the solution files menu"""
        doc_by_method = {
            'print_solution_files' : 'Print list of available solution files.',
            'load_solution' : 'Load a solution file.',
            'delete_solution' : 'Delete solution files.',
        }
class icing(metaclass=PyMenuMeta):
    """FENSAP-ICE options"""
    doc_by_method = {
        'file' : 'File menu.',
        'flow' : 'Flow solver menu.',
        'drop' : 'Droplet impingement menu.',
        'ice' : 'Ice accretion menu.',
        'multishot' : 'Multi-shot accretion menu.',
        'settings' : 'Global settings menu.',
    }
class mesh(metaclass=PyMenuMeta):
    """Enter the mesh menu."""
    doc_by_method = {
        'adjacency' : 'View and rename face zones adjacent to selected cell zones.',
        'check' : 'Perform various mesh consistency checks.',
        'check_before_solve' : 'Perform various mesh consistency checks before solve.',
        'check_verbosity' : 'Set verbosity output of mesh check and mesh quality. Higher verbosity corresponds to more detailed information.',
        'enhanced_orthogonal_quality' : 'Enable enhanced orthogonal quality method.',
        'mesh_info' : 'Print zone information size.',
        'memory_usage' : 'Report solver memory use.',
        'quality' : 'Perform analysis of mesh quality.',
        'redistribute_boundary_layer' : 'Enforce growth rate in boundary layer.',
        'replace' : 'Replace mesh and interpolate data.',
        'rotate' : 'Rotate the mesh',
        'scale' : 'Scale the mesh',
        'size_info' : 'Print mesh size.',
        'smooth_mesh' : 'Smooth the mesh using quality-based, Laplace or skewness methods.',
        'swap_mesh_faces' : 'Swap mesh faces.',
        'translate' : 'Translate the mesh.',
        'set_unit_system' : 'To apply standard set of units to all quantities.',
        'units' : 'Set unit conversion factors.',
    }
    class adapt(metaclass=PyMenuMeta):
        """Enter the adaption menu."""
        doc_by_method = {
            'refinement_criteria' : 'Set expression for refinement criterion.',
            'coarsening_criteria' : 'Set expression for coarsening criterion.',
            'adapt_mesh' : 'Adapt the mesh based on set refinement/coarsening criterion.',
            'display_adaption_cells' : 'Display cells marked for refinement/coarsening.',
            'list_adaption_cells' : 'List the number of cells marked for refinement/coarsening.',
            'free_hierarchy' : 'Delete the adaption hierarchy',
            'anisotropic_adaption' : 'Anisotropically refine boundary layers.',
        }
        class set(metaclass=PyMenuMeta):
            """Enter the adaption set menu."""
            doc_by_method = {
                'method' : 'Set the adaption method.',
                'cell_zones' : 'Set cell zones to be used for marking adaption. An empty list implies that all zones are considered for adaption.',
                'verbosity' : 'Set the adaption verbosity.',
                'encapsulate_children' : 'Encapsulate all children of parent cells on the same partition',
                'maximum_refinement_level' : 'Set maximum level of refinement in the mesh.',
                'minimum_edge_length' : 'Set limit on the minimum effective edge-length of cells in the mesh.',
                'minimum_cell_quality' : 'Set limit on the minimum cell orthogonal quality during adaption.',
                'maximum_cell_count' : 'Set limit on the maximum number of cells during adaption.',
                'additional_refinement_layers' : 'Set the number of additional cell layers for refinement.',
                'anisotropic_adaption' : 'Enable/Disable anisotropic adaption for prismatic cells.',
                'anisotropic_boundary_zones' : 'Set the boundary zones to specify directions for anisotropic refinement.',
                'anisotropic_split_ratio' : 'Set the split ratio for anisotropic refinement of prismatic cells.',
                'display_settings' : 'Set the graphics display options for cells marked for adaption.',
                'overset_adapt_dead_cells' : 'Enables adaption of dead cells in overset meshes.',
            }
        class profile(metaclass=PyMenuMeta):
            """Enter the adaption profile menu."""
            doc_by_method = {
                'enable' : 'Enable adaption profiling.',
                'disable' : 'Disable adaption profiling.',
                'print' : 'Print adaption profiling results.',
                'clear' : 'Clear adaption profiling counters.',
            }
        class cell_registers(metaclass=PyMenuMeta):
            """Manage Cell Registers"""
            doc_by_method = {
                'adapt' : 'Adapt cell register objects.',
                'add' : 'Add a new object',
                'apply_poor_mesh_numerics' : 'Apply poor mesh numerics to cell register objects.',
                'coarsen' : 'Coarsen cell register objects.',
                'display' : 'Display cell register objects.',
                'edit' : 'Edit an object',
                'delete' : 'Delete an object',
                'list' : 'List objects',
                'list_properties' : 'List properties of an object',
                'refine' : 'Refine cell register objects.',
            }
        class manage_criteria(metaclass=PyMenuMeta):
            """Manage Adaption Criteria"""
            doc_by_method = {
                'add' : 'Add a new object',
                'edit' : 'Edit an object',
                'delete' : 'Delete an object',
                'list' : 'List objects',
                'list_properties' : 'List properties of an object',
            }
        class multi_layer_refinement(metaclass=PyMenuMeta):
            """Enter the multiple boundary layer refinement menu."""
            doc_by_method = {
                'refine_mesh' : 'Refine the mesh for multiple boundary layers.',
                'boundary_zones' : 'Specify boundary zones for refinement.',
                'layer_count' : 'Specify the layer count for refinement.',
                'parameters' : 'Specify parameters for multiple boundary layer refinement.',
            }
        class geometry(metaclass=PyMenuMeta):
            """Enter the adaption geometry menu."""
            doc_by_method = {
                'reconstruct_geometry' : 'Enable/Disable geometry based adaption.',
                'set_geometry_controls' : 'Set geometry controls for wall zones.',
            }
    class modify_zones(metaclass=PyMenuMeta):
        """Enter the modify zones menu."""
        doc_by_method = {
            'activate_cell_zone' : 'Activate a cell thread.',
            'append_mesh' : 'Append new mesh.',
            'append_mesh_data' : 'Append new mesh with data.',
            'copy_move_cell_zone' : 'Copy and translate or rotate a cell zone.',
            'create_all_shell_threads' : 'Mark all finite thickness wall for shell creation. Shell zones will be created at the start of iterations.',
            'deactivate_cell_zone' : 'Deactivate cell thread.',
            'recreate_all_shells' : 'Create shell on all the walls where which were deleted using the command delete-all-shells',
            'delete_all_shells' : 'Delete all shell zones and switch off shell conduction on all the walls. These zones can be recreated using the command recreate-all-shells',
            'delete_cell_zone' : 'Delete a cell thread.',
            'extrude_face_zone_delta' : 'Extrude a face thread a specified distance based on a list of deltas.',
            'extrude_face_zone_para' : 'Extrude a face thread a specified distance based on a distance and a list of parametric locations between 0 and 1 (eg. 0 0.2 0.4 0.8 1.0).',
            'fuse_face_zones' : 'Attempt to fuse zones by removing duplicate faces and nodes.',
            'list_zones' : 'List zone IDs, types, kinds, and names.',
            'make_periodic' : 'Attempt to establish periodic/shadow face zone connectivity.',
            'create_periodic_interface' : 'Create a conformal or non-conformal periodic interface.',
            'scale_zone' : 'Scale nodal coordinates of input cell zones.',
            'rotate_zone' : 'Rotate nodal coordinates of input cell zones.',
            'translate_zone' : 'Translate nodal coordinates of input cell zones.',
            'matching_tolerance' : 'Set the normalized tolerance used for finding coincident nodes.',
            'merge_zones' : 'Merge zones of the same type and condition into one.',
            'mrf_to_sliding_mesh' : 'Change motion specification from MRF to moving mesh',
            'convert_all_solid_mrf_to_solid_motion' : 'Change all solid zones motion specification from MRF to solid motion',
            'orient_face_zone' : 'Orient the face zone.',
            'replace_zone' : 'Replace a cell zone.',
            'sep_cell_zone_mark' : 'Separate a cell zone based on cell marking.',
            'sep_cell_zone_region' : 'Separate a cell zone based on contiguous regions.',
            'sep_face_zone_angle' : 'Separate a face zone based on significant angle.',
            'sep_face_zone_face' : 'Separate each face in a zone into unique zone.',
            'sep_face_zone_mark' : 'Separate a face zone based on cell marking.',
            'sep_face_zone_region' : 'Separate a face zone based on contiguous regions.',
            'slit_periodic' : 'Slit a periodic zone into two symmetry zones.',
            'slit_face_zone' : 'Slit a two-sided wall into two connected wall zones.',
            'slit_interior_between_diff_solids' : 'Slit interior created between different solids into coupled walls',
            'zone_name' : 'Give a zone a new name.',
            'zone_type' : 'Set a zone's type.',
            'copy_mrf_to_mesh_motion' : 'Copy motion variable values for origin, axis and velocities from Frame Motion to Mesh Motion.',
            'copy_mesh_to_mrf_motion' : 'Copy motion variable values for origin, axis and velocities from Mesh Motion to Frame Motion.',
            'change_zone_state' : 'Change the realgas material state for a zone.',
            'change_zone_phase' : 'Change the realgas phase for a zone.',
        }
    class polyhedra(metaclass=PyMenuMeta):
        """Enter the polyhedra menu."""
        doc_by_method = {
            'convert_domain' : 'Convert entire domain to polyhedra cells.',
            'convert_hanging_nodes' : 'Convert cells with hanging nodes and faces to polyhedra.',
            'convert_hanging_nodes_zones' : 'Convert selected cell zones with hanging nodes and faces to polyhedra. 
The selected cell zones cannot be connected to other zones.',
            'convert_skewed_cells' : 'Convert skewed cells to polyhedra.',
        }
        class options(metaclass=PyMenuMeta):
            """Enter options menu."""
            doc_by_method = {
                'migrate_and_reorder' : 'Perform migration and reordering at the end of the polyhedra conversion.',
                'preserve_boundary_layer' : '0 = Decide at runtime.
1 = Never preserve.
2 = Always preserve.',
                'preserve_interior_zones' : 'Interior zones with matching name pattern are preserved during polyhedra conversion.',
            }
    class reorder(metaclass=PyMenuMeta):
        """Enter the reorder domain menu."""
        doc_by_method = {
            'band_width' : 'Print cell bandwidth.',
            'reorder_domain' : 'Reorder cells and faces by reverse Cuthill-McKee.',
            'reorder_zones' : 'Reorder zones by partition, type, and id.',
        }
    class repair_improve(metaclass=PyMenuMeta):
        """Enter the repair and improve quality menu."""
        doc_by_method = {
            'report_poor_elements' : 'Report invalid and poor quality elements.',
            'improve_quality' : 'Tries to improve the mesh quality.',
            'repair' : 'Tries to repair mesh problems identified by mesh check.',
            'repair_face_handedness' : 'Correct face handedness at left handed faces if possible.',
            'repair_face_node_order' : 'Reverse order of face nodes if needed.',
            'repair_periodic' : 'Modify mesh to enforce specified periodic rotation angle.',
            'repair_wall_distance' : 'Correct wall distance at very high aspect ratio hexahedral/polyhedral cells',
            'allow_repair_at_boundaries' : 'Enable/disable adjustment of boundary nodes during mesh repair.',
            'include_local_polyhedra_conversion_in_repair' : 'Enable/disable local conversion to polyhedra during mesh repair.',
        }
    class surface_mesh(metaclass=PyMenuMeta):
        """Enter the surface mesh menu."""
        doc_by_method = {
            'delete' : 'Delete surface mesh.',
            'display' : 'Display surface meshes.',
            'read' : 'Read surface meshes.',
        }
class parameters__and__customization(metaclass=PyMenuMeta):
    """Enter Parameters and custom menu."""
    class parameters(metaclass=PyMenuMeta):
        """Enter the parameters menu."""
        doc_by_method = {
            'enable_in_TUI' : 'Enable/disable parameters in the text user interface.',
        }
        class input_parameters(metaclass=PyMenuMeta):
            """Enter the input-parameters menu."""
            doc_by_method = {
                'edit' : 'Edit an input parameter.',
                'delete' : 'Delete an input parameter',
                'advance' : 'define custom variable to use input parameter',
            }
        class output_parameters(metaclass=PyMenuMeta):
            """Enter the output-parameters menu."""
            doc_by_method = {
                'create' : 'Create an output parameter.',
                'edit' : 'Edit an output parameter.',
                'rename' : 'Rename an output parameter.',
                'delete' : 'Delete an output parameter.',
                'print_to_console' : 'Print parameter value to console',
                'print_all_to_console' : 'Print all parameter values to console',
                'write_to_file' : 'Write parameter value to file',
                'write_all_to_file' : 'Write all parameter values to file',
            }
    class user_defined(metaclass=PyMenuMeta):
        """Enter the user-defined functions and scalars menu."""
        doc_by_method = {
            'auto_compile_compiled_udfs' : 'For this Fluent session, specify whether to allow auto-compilation of compiled UDF when a case file (or settings file) is read.',
            'compiled_functions' : 'Open user-defined function library.',
            'use_built_in_compiler' : 'Enable/disable the use of the built-in compiler.',
            'interpreted_functions' : 'Load interpreted user-defined functions.',
            'function_hooks' : 'Hook up user-defined functions.',
            'execute_on_demand' : 'Execute UDFs on demand.',
            'user_defined_memory' : 'Allocate user-defined memory.',
            'user_defined_node_memory' : 'Allocate user-defined node memory.',
            'use_contributed_cpp' : 'Enable/disable use of cpp from the Fluent.Inc/contrib directory.',
            'fan_model' : 'Configure user-defined fan model.',
            'one_D_coupling' : 'Load 1D library.',
            'user_defined_scalars' : 'Define user-defined scalars.',
            'enable_udf_on_gpu' : 'Compile UDFs with OpenCL support.',
        }
        class real_gas_models(metaclass=PyMenuMeta):
            """Enable/configure real gas model."""
            doc_by_method = {
                'nist_real_gas_model' : 'Load NIST real gas library.',
                'nist_multispecies_real_gas_model' : 'Load NIST real gas library.',
                'set_state' : 'Select state for NIST real gas model.',
                'nist_settings' : 'Select refprop library.',
                'user_defined_real_gas_model' : 'Load user-defined real gas library.',
                'user_defined_multispecies_real_gas_model' : 'Load user-defined multispecies real gas library.',
            }
class parallel(metaclass=PyMenuMeta):
    """Enter the parallel processing menu."""
    doc_by_method = {
        'check' : 'Parallel check.',
        'check_verbosity' : 'Set verbosity output of parallel check. Higher verbosity corresponds to more detailed information.',
        'show_connectivity' : 'Show machine connectivity.',
        'latency' : 'Show network latency.',
        'bandwidth' : 'Show network bandwidth.',
        'thread_number_control' : 'thread number control',
    }
    class network(metaclass=PyMenuMeta):
        """Enter the network configuration menu."""
        doc_by_method = {
            'kill_all_nodes' : 'Delete all compute nodes from virtual machine.',
            'kill_node' : 'Kill a compute node process specified by ID.',
            'load_hosts' : 'Read a hosts file.',
            'path' : 'Set the Fluent shell script path.',
            'save_hosts' : 'Write a hosts file.',
            'spawn_node' : 'Spawn a compute node process on a specified machine.',
        }
    class partition(metaclass=PyMenuMeta):
        """Enter the partition domain menu."""
        doc_by_method = {
            'combine_partition' : 'Merge every N partitions.',
            'merge_clusters' : 'Merge partition clusters.',
            'method' : 'Partition the domain.',
            'print_partitions' : 'Print partition information.',
            'print_active_partitions' : 'Print active partition information.',
            'print_stored_partitions' : 'Print stored partition information.',
            'reorder_partitions' : 'Reorder partitions.',
            'reorder_partitions_to_architecture' : 'Reorder partitions to architecture.',
            'smooth_partition' : 'Smooth partition interface.',
            'use_stored_partitions' : 'Use stored partitioning.',
        }
        class automatic(metaclass=PyMenuMeta):
            """Enter the menu to set auto partition parameters."""
            doc_by_method = {
                'across_zones' : 'Enable auto partitioning by zone or by domain.',
                'method' : 'Set the method for auto partitioning the domain.',
                'load_vector' : 'Set auto the partition load vector.',
                'pre_test' : 'Set auto partition pre-testing optimization.',
                'use_case_file_method' : 'Enable the use-case-file method for auto partitioning.',
            }
        class set(metaclass=PyMenuMeta):
            """Enter the menu to set partition parameters."""
            doc_by_method = {
                'across_zones' : 'Enable partitioning by zone or by domain.',
                'all_off' : 'Disable all optimization.',
                'all_on' : 'Enable all optimization.',
                'cell_function' : 'Set cell function.',
                'load_distribution' : 'Set partition load vector.',
                'merge' : 'Set partition merging optimization.',
                'origin' : 'Set coordinates of origin.',
                'pre_test' : 'Set partition pre-testing optimization.',
                'smooth' : 'Set partition smoothing optimization.',
                'laplace_smoothing' : 'Laplace smoothing for mesh with stretched cells.',
                'verbosity' : 'Set partition print verbosity.',
                'nfaces_as_weights' : 'Use number of faces as weights.',
                'face_area_as_weights' : 'Use face area as connection weights.',
                'stretched_mesh_enhancement' : 'Enhancement for mesh with stretched cells.',
                'layering' : 'Use layering for partitioning.',
                'solid_thread_weight' : 'Use solid thread weights.',
                'particle_weight' : 'Set DPM particle weight.',
                'vof_free_surface_weight' : 'Set VOF free surface weight.',
                'isat_weight' : 'Set ISAT weight.',
                'model_weighted_partition' : 'Set model weighted partition',
                'fluid_solid_rebalance_after_read_case' : 'Use optimal repartitioning after reading case file with significant solid and fluid zones',
                'dpm_load_balancing' : 'Enable automatic load balancing for DPM',
            }
    class set(metaclass=PyMenuMeta):
        """Enter the set parallel parameters menu."""
        doc_by_method = {
            'partition_mask' : 'Set partition mask.',
            'verbosity' : 'Set the parallel verbosity.',
            'time_out' : 'Set spawn timeout seconds.',
            'fast_i' : 'Use fast I/O option.',
        }
    class load_balance(metaclass=PyMenuMeta):
        """Enter the load balancing parameters menu."""
        doc_by_method = {
            'physical_models' : 'Use physical-models load balancing?',
            'dynamic_mesh' : 'Use load balancing for dynamic mesh?',
            'mesh_adaption' : 'Use load balancing for mesh adaption?',
        }
    class gpgpu(metaclass=PyMenuMeta):
        """Select and show gpgpu."""
        doc_by_method = {
            'show' : 'Show gpgpu.',
            'select' : 'Select gpgpu.',
        }
    class timer(metaclass=PyMenuMeta):
        """Enter the timer menu."""
        doc_by_method = {
            'usage' : 'Print solver timer.',
            'reset' : 'Reset domain timers.',
        }
    class multidomain(metaclass=PyMenuMeta):
        """Enter the multidomain architecture menu."""
        class conjugate_heat_transfer(metaclass=PyMenuMeta):
            """Enter the conjugate heat transfer menu for multidomain simulation."""
            doc_by_method = {
                'enable' : 'Enable/disable loosely coupled conjugate heat transfer.',
                'set' : 'Enter the set menu for loosely coupled conjugate heat transfer.',
            }
        class solve(metaclass=PyMenuMeta):
            """Enter the multi-domain simulation solver menu."""
            doc_by_method = {
                'iterate' : 'Iteration the multidomain conjugate heat transfer.',
                'dual_time_iterate' : 'Dual-time iterate the multidomain conjugate heat transfer.',
            }
class preferences(metaclass=PyMenuMeta):
    """Set preferences"""
    class appearance(metaclass=PyMenuMeta):
        """"""
        doc_by_method = {
            'axis_triad' : '',
            'color_theme' : '',
            'completer' : '',
            'custom_title_bar' : '',
            'default_view' : '',
            'graphics_background_color1' : '',
            'graphics_background_color2' : '',
            'graphics_background_style' : '',
            'graphics_color_theme' : '',
            'graphics_default_manual_face_color' : '',
            'graphics_default_manual_node_color' : '',
            'graphics_edge_color' : '',
            'graphics_foreground_color' : '',
            'graphics_partition_boundary_color' : '',
            'graphics_surface_color' : '',
            'graphics_title_window_framecolor' : '',
            'graphics_view' : '',
            'graphics_wall_face_color' : '',
            'group_by_tree_view' : '',
            'model_color_scheme' : '',
            'number_of_files_recently_used' : '',
            'number_of_pastel_colors' : '',
            'pastel_color_saturation' : '',
            'pastel_color_value' : '',
            'quick_property_view' : '',
            'ruler' : '',
            'show_enabled_models' : '',
            'show_interface_children_zone' : '',
            'show_model_edges' : '',
            'show_periodic_shadow_zones' : '',
            'solution_mode_edge_color_in_meshing_mode' : '',
            'startup_page' : '',
            'surface_emissivity' : '',
            'surface_specularity' : '',
            'surface_specularity_for_contours' : '',
            'titles' : '',
            'titles_border_offset' : '',
        }
        class ansys_logo(metaclass=PyMenuMeta):
            """"""
            doc_by_method = {
                'color' : '',
                'visible' : '',
            }
        class charts(metaclass=PyMenuMeta):
            """"""
            doc_by_method = {
                'curve_colors' : '',
                'enable_open_glfor_modern_plots' : '',
                'font' : '',
                'legend_alignment' : '',
                'legend_visibility' : '',
                'modern_plots_enabled' : '',
                'modern_plots_points_threshold' : '',
                'plots_behavior' : '',
                'print_plot_data' : '',
                'text_color' : '',
                'threshold' : '',
            }
        class selections(metaclass=PyMenuMeta):
            """"""
            doc_by_method = {
                'general_displacement' : '',
                'highlight_edge_color' : '',
                'highlight_edge_weight' : '',
                'highlight_face_color' : '',
                'highlight_gloss' : '',
                'highlight_specular_component' : '',
                'highlight_transparency' : '',
                'mouse_hover_probe_values_enabled' : '',
                'mouse_over_highlight_enabled' : '',
                'probe_tooltip_hide_delay_timer' : '',
                'probe_tooltip_show_delay_timer' : '',
            }
    class general(metaclass=PyMenuMeta):
        """"""
        doc_by_method = {
            'advanced_partition' : '',
            'automatic_transcript' : '',
            'default_ioformat' : '',
            'enable_parametric_study' : '',
            'enable_project_file' : '',
            'flow_model' : '',
            'idle_timeout' : '',
            'key_behavioral_changes_message' : '',
            'qaservice_message' : '',
            'utlcreate_physics_on_mode_change' : '',
        }
    class gpuapp(metaclass=PyMenuMeta):
        """"""
        doc_by_method = {
            'alpha_features' : '',
        }
    class graphics(metaclass=PyMenuMeta):
        """"""
        doc_by_method = {
            'animation_option' : '',
            'double_buffering' : '',
            'enable_non_object_based_workflow' : '',
            'event_poll_interval' : '',
            'event_poll_timeout' : '',
            'force_key_frame_animation_markers_to_off' : '',
            'graphics_window_line_width' : '',
            'graphics_window_point_symbol' : '',
            'hidden_surface_removal_method' : '',
            'higher_resolution_graphics_window_line_width' : '',
            'lower_resolution_graphics_window_line_width' : '',
            'marker_drawing_mode' : '',
            'max_graphics_text_size' : '',
            'min_graphics_text_size' : '',
            'plot_legend_margin' : '',
            'point_tool_size' : '',
            'remove_partition_lines' : '',
            'remove_partition_lines_tolerance' : '',
            'rotation_centerpoint_visible' : '',
            'scroll_wheel_event_end_timer' : '',
            'set_camera_normal_to_surface_increments' : '',
            'show_hidden_lines' : '',
            'show_hidden_surfaces' : '',
            'switch_to_open_glfor_remote_visualization' : '',
            'test_use_external_function' : '',
            'text_window_line_width' : '',
        }
        class boundary_markers(metaclass=PyMenuMeta):
            """"""
            doc_by_method = {
                'color_option' : '',
                'enabled' : '',
                'exclude_from_bounding' : '',
                'inlet_color' : '',
                'marker_fraction' : '',
                'marker_size_limiting_scale_multiplier' : '',
                'markers_limit' : '',
                'outlet_color' : '',
                'scale_marker' : '',
                'show_inlet_markers' : '',
                'show_outlet_markers' : '',
            }
        class colormap_settings(metaclass=PyMenuMeta):
            """"""
            doc_by_method = {
                'alignment' : '',
                'aspect_ratio_when_horizontal' : '',
                'aspect_ratio_when_vertical' : '',
                'auto_refit_on_resize' : '',
                'automatic_resize' : '',
                'border_style' : '',
                'colormap' : '',
                'isolines_position_offset' : '',
                'labels' : '',
                'levels' : '',
                'log_scale' : '',
                'major_length_to_screen_ratio_when_horizontal' : '',
                'major_length_to_screen_ratio_when_vertical' : '',
                'margin_from_edge_to_screen_ratio' : '',
                'max_size_scale_factor' : '',
                'min_size_scale_factor' : '',
                'number_format_precision' : '',
                'number_format_type' : '',
                'show_colormap' : '',
                'skip_value' : '',
                'text_behavior' : '',
                'text_font_automatic_horizontal_size' : '',
                'text_font_automatic_size' : '',
                'text_font_automatic_units' : '',
                'text_font_automatic_vertical_size' : '',
                'text_font_fixed_horizontal_size' : '',
                'text_font_fixed_size' : '',
                'text_font_fixed_units' : '',
                'text_font_fixed_vertical_size' : '',
                'text_font_name' : '',
                'text_truncation_limit_for_horizontal_colormaps' : '',
                'text_truncation_limit_for_vertical_colormaps' : '',
                'type' : '',
                'use_no_sub_windows' : '',
            }
        class embedded_windows(metaclass=PyMenuMeta):
            """"""
            doc_by_method = {
                'default_embedded_mesh_windows_view' : '',
                'default_embedded_windows_view' : '',
                'save_embedded_window_layout' : '',
                'show_border_for_embedded_window' : '',
            }
        class export_video_settings(metaclass=PyMenuMeta):
            """"""
            doc_by_method = {
                'advanced_video_quality_options' : '',
                'video_format' : '',
                'video_fps' : '',
                'video_quality' : '',
                'video_resoution_x' : '',
                'video_resoution_y' : '',
                'video_scale' : '',
                'video_smooth_scaling' : '',
                'video_use_frame_resolution' : '',
            }
        class graphics_effects(metaclass=PyMenuMeta):
            """"""
            doc_by_method = {
                'ambient_occlusion_enabled' : '',
                'ambient_occlusion_quality' : '',
                'ambient_occlusion_strength' : '',
                'anti_aliasing' : '',
                'bloom_blur' : '',
                'bloom_enabled' : '',
                'bloom_strength' : '',
                'grid_color' : '',
                'grid_plane_count' : '',
                'grid_plane_enabled' : '',
                'grid_plane_offset' : '',
                'grid_plane_size_factor' : '',
                'plane_direction' : '',
                'reflections_enabled' : '',
                'shadow_map_enabled' : '',
                'show_edge_reflections' : '',
                'show_marker_reflections' : '',
                'simple_shadows_enabled' : '',
                'update_after_mouse_release' : '',
            }
        class hardcopy_settings(metaclass=PyMenuMeta):
            """"""
            doc_by_method = {
                'export_edges_for_avz' : '',
                'hardcopy_driver' : '',
                'hardcopy_line_width' : '',
                'hardware_image_accel' : '',
                'post_script_permission_override' : '',
                'save_embedded_hardcopies_separately' : '',
                'save_embedded_windows_in_hardcopy' : '',
                'transparent_embedded_windows' : '',
            }
        class lighting(metaclass=PyMenuMeta):
            """"""
            doc_by_method = {
                'ambient_light_intensity' : '',
                'headlight' : '',
                'headlight_intensity' : '',
                'lighting_method' : '',
            }
        class manage_hoops_memory(metaclass=PyMenuMeta):
            """"""
            doc_by_method = {
                'enabled' : '',
                'hsfimport_limit' : '',
            }
        class material_effects(metaclass=PyMenuMeta):
            """"""
            doc_by_method = {
                'decimation_filter' : '',
                'parameterization_source' : '',
                'tiling_style' : '',
            }
        class meshing_mode(metaclass=PyMenuMeta):
            """"""
            doc_by_method = {
                'graphics_window_display_timeout' : '',
                'graphics_window_display_timeout_value' : '',
            }
        class performance(metaclass=PyMenuMeta):
            """"""
            doc_by_method = {
                'fast_display_mode' : '',
                'minimum_frame_rate' : '',
                'optimize_for' : '',
                'ratio_of_target_frame_rate_to_classify_heavy_geometry' : '',
                'ratio_of_target_frame_rate_to_declassify_heavy_geometry' : '',
            }
        class transparency(metaclass=PyMenuMeta):
            """"""
            doc_by_method = {
                'algorithm_for_modern_drivers' : '',
                'depth_peeling_layers' : '',
                'depth_peeling_preference' : '',
                'quick_moves' : '',
                'zsort_options' : '',
            }
        class vector_settings(metaclass=PyMenuMeta):
            """"""
            doc_by_method = {
                'arrow3_dradius1_factor' : '',
                'arrow3_dradius2_factor' : '',
                'arrowhead3_dradius1_factor' : '',
                'line_arrow3_dperpendicular_radius' : '',
            }
    class mat_pro_app(metaclass=PyMenuMeta):
        """"""
        doc_by_method = {
            'beta_features' : '',
            'console' : '',
            'focus' : '',
            'warning' : '',
        }
    class meshing_workflow(metaclass=PyMenuMeta):
        """"""
        doc_by_method = {
            'checkpointing_option' : '',
            'dock_editor' : '',
            'save_checkpoint_files' : '',
            'temp_folder' : '',
            'templates_folder' : '',
            'verbosity' : '',
        }
        class draw_settings(metaclass=PyMenuMeta):
            """"""
            doc_by_method = {
                'auto_draw' : '',
                'face_zone_limit' : '',
                'facet_limit' : '',
            }
    class navigation(metaclass=PyMenuMeta):
        """"""
        class mouse_mapping(metaclass=PyMenuMeta):
            """"""
            doc_by_method = {
                'additional' : '',
                'basic' : '',
                'mousemaptheme' : '',
            }
    class prj_app(metaclass=PyMenuMeta):
        """"""
        doc_by_method = {
            'advanced_flag' : '',
            'beta_flag' : '',
            'cffoutput' : '',
            'default_folder' : '',
            'display_mesh_after_case_load' : '',
            'ncpu' : '',
            'show_fluent_window' : '',
            'uilayout' : '',
            'use_default_folder' : '',
            'use_fluent_graphics' : '',
            'use_launcher' : '',
        }
    class simulation(metaclass=PyMenuMeta):
        """"""
        doc_by_method = {
            'flow_model' : '',
            'local_residual_scaling' : '',
        }
        class report_definitions(metaclass=PyMenuMeta):
            """"""
            doc_by_method = {
                'automatic_plot_file' : '',
                'report_plot_history_data_size' : '',
            }
    class turbo_workflow(metaclass=PyMenuMeta):
        """"""
        class cell_zone_settings(metaclass=PyMenuMeta):
            """"""
            doc_by_method = {
                'czsearch_order' : '',
                'rotating' : '',
                'stationary' : '',
            }
        class face_zone_settings(metaclass=PyMenuMeta):
            """"""
            doc_by_method = {
                'blade_region' : '',
                'fzsearch_order' : '',
                'hub_region' : '',
                'inlet_region' : '',
                'interior_region' : '',
                'outlet_region' : '',
                'periodic1_region' : '',
                'periodic2_region' : '',
                'shroud_region' : '',
                'symmetry_region' : '',
                'tip1_region' : '',
                'tip2_region' : '',
            }
        class graphics_settings(metaclass=PyMenuMeta):
            """"""
            doc_by_method = {
                'auto_draw' : '',
            }
class results(metaclass=PyMenuMeta):
    """Enter results menu."""
    class animate(metaclass=PyMenuMeta):
        """Enter the animation menu."""
        class playback(metaclass=PyMenuMeta):
            """Enter animation playback menu."""
            doc_by_method = {
                'read' : 'Read new animation from file or already-defined animations.',
                'play' : 'Play the selected animation.',
                'write' : 'Write animation sequence to the file.',
                'delete' : 'Delete animation sequence.',
                'stored_view' : 'Play the 3D animation sequence using the view stored in the sequence.',
                'video' : 'Set options for exporting video file menu.',
                'set_custom_frames' : 'Set custom frames start, end, skip frames for video export',
            }
    class graphics(metaclass=PyMenuMeta):
        """Enter graphics menu."""
        doc_by_method = {
            'annotate' : 'Add a text annotation string to the active graphics window.',
            'clear_annotations' : 'Delete all annotation text.',
            'color_map' : 'Enter the color-map menu.',
            'hsf_file' : 'Display hoops stream file data to active graphics window.',
        }
        class expert(metaclass=PyMenuMeta):
            """Enter expert menu."""
            doc_by_method = {
                'add_custom_vector' : 'Add new custom vector definition.',
                'contour' : 'Display contours of a flow variable.',
                'display_custom_vector' : 'Display custom vector.',
                'flamelet_data' : 'Display flamelet data.',
                'graphics_window_layout' : 'Arrange the graphics window layout.',
                'mesh' : 'Display the mesh.',
                'mesh_outline' : 'Display the mesh boundaries.',
                'mesh_partition_boundary' : 'Display mesh partition boundaries.',
                'multigrid_coarsening' : 'Display a coarse mesh level from the last multigrid coarsening.',
                'particle_tracks' : 'Enter the particle tracks menu.',
                'path_lines' : 'Enter the pathlines menu.',
                'pdf_data' : 'Enter the PDF data menu.',
                'profile' : 'Display profiles of a flow variable.',
                'reacting_channel_curves' : 'Plot/Report the reacting channel variables.',
                're_render' : 'Re-render the last contour, profile, or velocity vector plot
     with updated surfaces, meshes, lights, colormap, rendering options, etc.,
     without recalculating the contour data.',
                're_scale' : 'Re-render the last contour, profile, or velocity vector plot
     with updated scale, surfaces, meshes, lights, colormap, rendering options, etc.,
     without recalculating the field data.',
                'set' : 'Enter the set menu to set display parameters.',
                'set_list_tree_separator' : 'Set the separator character for list tree.',
                'surface_cells' : 'Draw the cells on the specified surfaces.',
                'surface_mesh' : 'Draw the mesh defined by the specified surfaces.',
                'vector' : 'Display space vectors.',
                'velocity_vector' : 'Display velocity vectors.',
                'zone_mesh' : 'Draw the mesh defined by specified face zones.',
            }
        class lights(metaclass=PyMenuMeta):
            """Enter the lights menu."""
            doc_by_method = {
                'lights_on' : 'Turn all active lighting on/off.',
                'lighting_interpolation' : 'Set lighting interpolation method.',
                'set_ambient_color' : 'Set the ambient light color for the scene.',
                'set_light' : 'Add or modify a directional, colored light.',
                'headlight_on' : 'Turn the light that moves with the camera on or off.',
            }
        class objects(metaclass=PyMenuMeta):
            """Enter to add, edit, delete or display graphics objects"""
            doc_by_method = {
                'create' : 'Create new graphics object.',
                'edit' : 'Edit graphics object.',
                'copy' : 'Copy graphics object.',
                'delete' : 'Delete graphics object.',
                'display' : 'Display graphics object.',
                'add_to_graphics' : 'Add graphics object to existing graphics.',
                'mesh_objects' : '',
                'contour_objects' : '',
                'vector_objects' : '',
            }
        class rendering_options(metaclass=PyMenuMeta):
            """Enter the rendering options menu."""
            doc_by_method = {
                'auto_spin' : 'Enable/disable mouse view rotations to continue to spin the display after the button is released.',
                'device_info' : 'List information for the graphics device.',
                'double_buffering' : 'Enable/disable double-buffering.',
                'driver' : 'Change the current graphics driver.',
                'hidden_surfaces' : 'Enable/disable hidden surface removal.',
                'hidden_surface_method' : 'Specify the method to perform hidden line and hidden surface rendering.',
                'outer_face_cull' : 'Enable/disable discarding outer faces during display.',
                'surface_edge_visibility' : 'Set edge visibility flags for surfaces.',
                'animation_option' : 'Using Wireframe / All option during animation',
                'color_map_alignment' : 'Set the color bar alignment.',
                'help_text_color' : 'Set the color of screen help text.',
                'face_displacement' : 'Set face displacement value in Z-buffer units along the Camera Z-axis.',
                'set_rendering_options' : 'Set the rendering options.',
                'show_colormap' : 'Enable/Disable colormap.',
            }
        class update_scene(metaclass=PyMenuMeta):
            """Enter the scene options menu."""
            doc_by_method = {
                'select_geometry' : 'Select geometry to be updated.',
                'overlays' : 'Enable/disable the overlays option.',
                'draw_frame' : 'Enable/disable drawing of the bounding frame.',
                'delete' : 'Delete selected geometries.',
                'display' : 'Display selected geometries.',
                'transform' : 'Apply transformation matrix on selected geometries.',
                'pathline' : 'Change pathline attributes.',
                'iso_sweep' : 'Change iso-sweep values.',
                'time' : 'Change time-step value.',
                'set_frame' : 'Change frame options.',
            }
    class plot(metaclass=PyMenuMeta):
        """Enter the XY plot menu."""
        doc_by_method = {
            'circum_avg_axial' : 'Compute iso-axial band surfaces and plot data vs axial coordinate on them.',
            'circum_avg_radial' : 'Compute iso-radial band surfaces and plot data vs radius on them.',
            'change_fft_ref_pressure' : 'Change acoustic reference pressure.',
            'fft' : 'Plot FFT of file data.',
            'fft_set' : 'Enter the menu to set histogram plot parameters.',
            'file' : 'Plot data from file.',
            'datasources' : 'Enter the menu to set data sources.',
            'display_profile_data' : 'Plot profile data.',
            'file_list' : 'Plot data from multiple files.',
            'file_set' : 'Enter the menu to set file plot parameters.',
            'histogram' : 'Plot a histogram of a specified scalar quantity.',
            'histogram_set' : 'Enter the menu to set histogram plot parameters.',
            'plot' : 'Plot solution on surfaces.',
            'plot_direction' : 'Set plot direction for xy plot.',
            'residuals' : 'Plot equation residual history.',
            'residuals_set' : 'Enter the menu to set residual plot parameters.',
            'solution' : 'Plot solution on surfaces and/or zones.',
            'solution_set' : 'Enter the menu to set solution plot parameters.',
            'set_boundary_val_off' : 'Set boundary value off when node values off for XY/Solution Plot.
       
 Note: This setting is valid for current Fluent session only.',
            'label_alignment' : 'Set the alignment of xy plot label to horizontal or axis aligned.',
        }
        class ansys_sound_analysis(metaclass=PyMenuMeta):
            """Ansys Sound analysis and specification."""
            doc_by_method = {
                'write_files' : 'write Ansys Sound out files',
                'print_indicators' : 'print Ansys Sound indicators',
            }
        class cumulative_plot(metaclass=PyMenuMeta):
            """Plot Cumulative Force and Moments"""
            doc_by_method = {
                'add' : 'Add a new object',
                'axes' : 'Set axes options of an object.',
                'curves' : 'Set curves options of an object.',
                'edit' : 'Edit an object',
                'delete' : 'Delete an object',
                'list' : 'List objects',
                'list_properties' : 'List properties of an object',
                'plot' : 'Plot the Cumulative Forces/Moments',
                'print' : 'Print the Cumulative Forces/Moments',
                'write' : 'Write the Cumulative Forces/Moments',
            }
        class flamelet_curves(metaclass=PyMenuMeta):
            """Plot flamelet curves."""
            doc_by_method = {
                'write_to_file' : 'Write curve to a file instead of plot.',
                'plot_curves' : 'Plot of a property.',
            }
    class report(metaclass=PyMenuMeta):
        """Enter the report menu."""
        doc_by_method = {
            'dpm_summary' : 'Print discrete phase summary report of particle fates.',
            'dpm_extended_summary' : 'Print extended discrete phase summary report of particle fates, with options',
            'dpm_zone_summaries_per_injection' : 'Enable per-injection zone DPM summaries',
            'dpm_sample' : 'Sample trajectories at boundaries and lines/planes.',
            'dpm_sample_output_udf' : 'Set the DPM sampling output UDF',
            'dpm_sample_sort_file' : 'Enable writing of sorted DPM sample files.',
            'particle_summary' : 'Print summary report for all current particles',
            'path_line_summary' : 'Print path-line-summary report.',
            'print_histogram' : 'Print a histogram of a scalar quantity.',
            'write_histogram' : '',
            'projected_surface_area' : 'Print total area of the projection of a group of surfaces to a plane.',
            'species_mass_flow' : 'Print list of species mass flow rates at boundaries.',
            'element_mass_flow' : 'Print list of element mass flow rates at boundaries.',
            'summary' : 'Print report summary.',
            'uds_flow' : 'Print list of UDS flow rate at boundaries.',
            'mphase_summary' : 'Multiphase Summary and Recommendations',
        }
        class dpm_histogram(metaclass=PyMenuMeta):
            """Enter the DPM histogram menu."""
            doc_by_method = {
                'compute_sample' : 'Compute minimum/maximum of a sample variable.',
                'delete_sample' : 'Delete a sample from loaded sample list.',
                'list_samples' : 'Show all samples in loaded sample list.',
                'plot_sample' : 'Plot a histogram of a loaded sample.',
                'read_sample' : 'Read a sample file and add it to the sample list.',
                'set' : 'Enter the settings menu for the histogram.',
                'write_sample' : 'Write a histogram of a loaded sample into a file.',
                'pick_sample_to_reduce' : 'Pick a sample for which to first set-up and then perform the data reduction.',
                'reduce_picked_sample' : 'Reduce a sample after first picking it and setting up all data-reduction options and parameters.',
                'setup_reduction' : 'Set up the sample data reduction by specifying all relevant options and setting parameters as desired.',
            }
        class fluxes(metaclass=PyMenuMeta):
            """Flux report menu."""
            doc_by_method = {
                'mass_flow' : 'Print mass flow rate at inlets and outlets.',
                'heat_transfer' : 'Print heat transfer rate at boundaries.',
                'heat_transfer_sensible' : 'Print sensible heat transfer rate at boundaries.',
                'rad_heat_trans' : 'Print radiation heat transfer rate at boundaries.',
                'film_mass_flow' : 'Print film mass flow rate at boundaries.',
                'film_heat_transfer' : 'Print film heat transfer rate at boundaries.',
                'pressure_work' : 'Print pressure work rate at moving boundaries.',
                'viscous_work' : 'Print viscous work rate at boundaries.',
            }
        class forces(metaclass=PyMenuMeta):
            """Force report menu."""
            doc_by_method = {
                'wall_forces' : 'Print integrated pressure and viscous forces on wall zones.',
                'wall_moments' : 'Print integrated pressure and viscous moments on wall zones.',
                'pressure_center' : 'Print center of pressure on wall zones.',
            }
        class reference_values(metaclass=PyMenuMeta):
            """Reference value menu."""
            doc_by_method = {
                'area' : 'Set reference area for normalization.',
                'compute' : 'Enter the compute menu.',
                'depth' : 'Set reference depth for volume calculation.',
                'density' : 'Set reference density for normalization.',
                'enthalpy' : 'Set reference enthalpy for enthalpy damping and normalization.',
                'length' : 'Set reference length for normalization.',
                'pressure' : 'Set reference pressure for normalization.',
                'temperature' : 'Set reference temperature for normalization.',
                'yplus' : 'Set reference yplus for normalization.',
                'velocity' : 'Set reference velocity for normalization.',
                'viscosity' : 'Set reference viscosity for normalization.',
                'zone' : 'Set reference zone.',
                'list' : 'List current reference values.',
            }
        class surface_integrals(metaclass=PyMenuMeta):
            """Surface Integral menu."""
            doc_by_method = {
                'area' : 'Print total area of surfaces.',
                'area_weighted_avg' : 'Print area-weighted average of scalar on surfaces.',
                'facet_avg' : 'Print average of scalar at facet centroids of the surfaces.',
                'facet_max' : 'Print maximum of scalar at facet centroids of the surfaces.',
                'facet_min' : 'Print minimum of scalar at facet centroids of the surfaces.',
                'flow_rate' : 'Print flow rate of scalar through surfaces.',
                'integral' : 'Print integral of scalar over surfaces.',
                'mass_flow_rate' : 'Print mass flow rate through surfaces.',
                'mass_weighted_avg' : 'Print mass-average of scalar over surfaces.',
                'standard_deviation' : 'Print standard deviation of scalar',
                'sum' : 'Print sum of scalar at facet centroids of the surfaces.',
                'uniformity_index_area_weighted' : 'Print uniformity index of scalar over surfaces.',
                'uniformity_index_mass_weighted' : 'Print uniformity index of scalar over surfaces.',
                'vector_based_flux' : 'Print custom vector based flux',
                'vector_flux' : 'Print custom vector flux',
                'vector_weighted_average' : 'Print custom vector weighted average',
                'vertex_avg' : 'Print average of scalar at vertices of the surfaces.',
                'vertex_max' : 'Print maximkum of scalar at vertices of the surfaces.',
                'vertex_min' : 'Print minimum of scalar at vertices of the surfaces.',
                'volume_flow_rate' : 'Print volume flow rate through surfaces.',
            }
        class volume_integrals(metaclass=PyMenuMeta):
            """Volume Integral menu."""
            doc_by_method = {
                'mass' : 'Print total mass of specified cell zones.',
                'mass_avg' : 'Print mass-average of scalar over cell zones.',
                'mass_integral' : 'Print mass-weighted integral of scalar over cell zones.',
                'maximum' : 'Print maximum of scalar over all cell zones.',
                'minimum' : 'Print minimum of scalar over all cell zones.',
                'sum' : 'Print sum of scalar over all cell zones.',
                'twopisum' : 'Print sum of scalar over all cell zones multiplied by 2*Pi.',
                'volume' : 'Print total volume of specified cell zones.',
                'volume_avg' : 'Print volume-weighted average of scalar over cell zones.',
                'volume_integral' : 'Print integral of scalar over cell zones.',
            }
        class modified_setting(metaclass=PyMenuMeta):
            """Enter the menu for setting up the Modified Settings Summary table."""
            doc_by_method = {
                'modified_setting' : 'Specify which settings will be checked for non-default status for generating the Modified Settings Summary table.',
                'write_user_setting' : 'Write the contents of the Modified Settings Summary table to a file.',
            }
        class population_balance(metaclass=PyMenuMeta):
            """Population Balance menu."""
            doc_by_method = {
                'moments' : 'Set moments for population balance.',
                'number_density' : 'Set number density functions.',
            }
        class heat_exchanger(metaclass=PyMenuMeta):
            """Enter the heat exchanger menu."""
            doc_by_method = {
                'computed_heat_rejection' : 'Print total heat rejection.',
                'inlet_temperature' : 'Print inlet temperature.',
                'outlet_temperature' : 'Print outlet temperature.',
                'mass_flow_rate' : 'Print mass flow rate.',
                'specific_heat' : 'Print fluid's specific heat.',
            }
        class system(metaclass=PyMenuMeta):
            """Sytem menu."""
            doc_by_method = {
                'proc_stats' : 'Fluent process information.',
                'sys_stats' : 'System information.',
                'gpgpu_stats' : 'GPGPU information.',
                'time_stats' : 'Time usage information.',
            }
        class simulation_reports(metaclass=PyMenuMeta):
            """Enter the simulation reports menu."""
            doc_by_method = {
                'list_simulation_reports' : 'List all report names.',
                'generate_simulation_report' : 'Generate a new simulation report or regenerate an existing simulation report with the provided name.',
                'view_simulation_report' : 'View a simulation report that has already been generated. In batch mode this will print the report's URL.',
                'export_simulation_report_as_pdf' : 'Export the provided simulation report as a PDF file.',
                'export_simulation_report_as_html' : 'Export the provided simulation report as HTML.',
                'write_report_names_to_file' : 'Write the list of currently generated report names to a txt file.',
                'rename_simulation_report' : 'Rename a report which has already been generated.',
                'duplicate_simulation_report' : 'Duplicate a report and all of its settings to a new report.',
                'reset_report_to_defaults' : 'Reset all report settings to default for the provided simulation report.',
                'delete_simulation_report' : 'Delete the provided simulation report.',
                'write_simulation_report_template_file' : 'Write a JSON template file with this case's Simulation Report settings.',
                'read_simulation_report_template_file' : 'Read a JSON template file with existing Simulation Report settings.',
            }
    class surface(metaclass=PyMenuMeta):
        """Enter the data surface manipulation menu."""
        doc_by_method = {
            'circle_slice' : 'Extract a circular slice.',
            'delete_surface' : 'Remove a defined data surface.',
            'group_surfaces' : 'Group a set of surfaces',
            'ungroup_surface' : 'Ungroup the surface(if grouped)',
            'iso_clip' : 'Clip a data surface (surface, curve, or point) between two iso-values.',
            'iso_surface' : 'Extract an iso-surface (surface, curve, or point) from the curent data field.',
            'expression_volume' : 'Create volume with boolean expression',
            'multiple_iso_surfaces' : 'Create multiple iso-surfaces from the data field at specified spacing.',
            'line_slice' : 'Extract a linear slice.',
            'line_surface' : 'Define a "line" surface by specifying the two endpoint coordinates.',
            'list_surfaces' : 'List the number of facets in the defined surfaces.',
            'mouse_line' : 'Define a line surface using the mouse to select two points.',
            'mouse_plane' : 'Define a plane surface using the mouse to select three points.',
            'mouse_rake' : 'Define a "rake" surface using the mouse to select the end points.',
            'partition_surface' : 'Define a data surface on mesh faces on the partition boundary.',
            'plane' : 'Create a plane given 3 points bounded by the domain.',
            'plane_surface' : 'Create a plane from a coordinate plane, point and normal, or three points.',
            'multiple_plane_surfaces' : 'Create multiple plane surfaces at specified spacing.',
            'plane_slice' : 'Extract a planar slice.',
            'point_array' : 'Extract a rectangular array of data points.',
            'point_surface' : 'Define a "point" surface by specifying the coordinates.',
            'structural_point_surface' : 'Define a "structural point" surface by specifying the coordinates.',
            'quadric_slice' : 'Extract a quadric slice.',
            'rake_surface' : 'Define a "rake" surface by specifying the end points.',
            'rename_surface' : 'Rename a defined data surface.',
            'sphere_slice' : 'Extract a spherical slice.',
            'ellipsoid_slice' : 'Extract a ellipsoid slice.',
            'cone_slice' : 'Extract a cone slice.',
            'surface_cells' : 'Extract all cells intersected by a data surface.',
            'transform_surface' : 'Transform surface.',
            'create_imprint_surface' : 'Imprint surface.',
            'zone_surface' : 'Define a data surface on a mesh zone.',
            'reset_zone_surfaces' : 'Reset case surface list',
            'multiple_zone_surfaces' : 'Create multiple data surfaces at a time.',
            'edit_surface' : 'Edit a defined data surface.',
        }
        class query(metaclass=PyMenuMeta):
            """Enter surface query menu."""
            doc_by_method = {
                'delete_query' : 'Delete saved query.',
                'list_surfaces' : 'List surfaces.',
                'named_surface_list' : 'Create named list of surfaces.',
                'list_named_selection' : 'List named selection of surface type',
                'list_queries' : 'List all saved queries',
            }
    class graphics_window(metaclass=PyMenuMeta):
        """Enter graphics window menu"""
        doc_by_method = {
            'close_window' : 'Close a user graphics window.',
            'close_window_by_name' : 'Close a reserved graphics window by its name.',
            'open_window' : 'Open a user graphics window.',
            'save_picture' : 'Generate a "hardcopy" of the active window.',
            'set_window' : 'Set a user graphics window to be the active window.',
            'set_window_by_name' : 'Set a reserved graphics window to be the active window by its name.',
            'update_layout' : 'update the fluent layout',
        }
        class embedded_windows(metaclass=PyMenuMeta):
            """Enter to embed, close, move-out embedded windows"""
            doc_by_method = {
                'close' : 'Close an embedded window.',
                'close_all' : 'Close all embedded windows for given parent window.',
                'embed_in' : 'Embed Window into another window',
                'move_out' : 'Move out an embedded window',
                'move_out_all' : 'Move out all embedded windows for given parent window.',
            }
        class picture(metaclass=PyMenuMeta):
            """Enter the hardcopy/save-picture options menu."""
            doc_by_method = {
                'color_mode' : 'Enter the hardcopy color mode menu.',
                'driver' : 'Enter the set hardcopy driver menu.',
                'invert_background' : 'Exchange foreground/background colors for hardcopy.',
                'landscape' : 'Plot hardcopies in landscape or portrait orientation.',
                'preview' : 'Display a preview image of a hardcopy.',
                'x_resolution' : 'Set the width of raster-formatted images in pixels (0 implies current window size).',
                'y_resolution' : 'Set the height of raster-formatted images in pixels (0 implies current window size).',
                'dpi' : 'Set the DPI for EPS and Postscript files, specifies the resolution in dots per inch (DPI) instead of setting the width and height',
                'use_window_resolution' : 'Use the currently active window's resolution for hardcopy (ignores the x-resolution and y-resolution in this case).',
                'set_standard_resolution' : 'Select from pre-defined resolution list.',
                'jpeg_hardcopy_quality' : 'To set jpeg hardcopy quality.',
            }
        class windows(metaclass=PyMenuMeta):
            """Enter the window options menu."""
            doc_by_method = {
                'aspect_ratio' : 'Set the aspect ratio of the active window.',
                'axes' : 'Enter the axes window options menu.',
                'main' : 'Enter the main view window options menu.',
                'scale' : 'Enter the color scale window options menu.',
                'text' : 'Enter the text window options menu.',
                'video' : 'Enter the video window options menu.',
                'xy' : 'Enter the X-Y plot window options menu.',
                'logo' : 'Enable/disable visibility of the logo in graphics window.',
                'ruler' : 'Enable/disable ruler visibility.',
                'logo_color' : 'Set logo color to white/black.',
            }
        class titles(metaclass=PyMenuMeta):
            """Set problem title."""
            doc_by_method = {
                'left_top' : 'Set the title text for left top in title segment',
                'left_bottom' : 'Set the title text for left bottom in title segment',
                'right_top' : 'Set the title text for right top in title segment',
                'right_middle' : 'Set the title text for right middle in title segment',
                'right_bottom' : 'Set the title text for right bottom in title segment',
            }
        class views(metaclass=PyMenuMeta):
            """Enter the view manipulation menu."""
            doc_by_method = {
                'auto_scale' : 'Scale and center the current scene.',
                'camera' : 'Enter the camera menu to modify the current viewing parameters.',
                'default_view' : 'Reset view to front and center.',
                'delete_view' : 'Remove a view from the list.',
                'last_view' : 'Return to the camera position before the last manipulation.',
                'next_view' : 'Return to the camera position after the current position in the stack.',
                'list_views' : 'List predefined and saved views.',
                'restore_view' : 'Use a saved view.',
                'read_views' : 'Read views from a view file.',
                'save_view' : 'Save the current view to the view list.',
                'write_views' : 'Write selected views to a view file.',
            }
        class display_states(metaclass=PyMenuMeta):
            """Enter the display state manipulation menu."""
            doc_by_method = {
                'list' : 'Print the names of the available display states to the console.',
                'apply' : 'Apply a display state to the active window.',
                'delete' : 'Delete a display state.',
                'use_active' : 'Update an existing display state's settings to match those of the active graphics window.',
                'copy' : 'Create a new display state with settings copied from an existing display state.',
                'read' : 'Read display states from a file.',
                'write' : 'Write display states to a file.',
                'edit' : 'Edit a particular display state setting.',
                'create' : 'Create a new display state.',
            }
        class view_sync(metaclass=PyMenuMeta):
            """Enter the display state manipulation menu."""
            doc_by_method = {
                'list' : 'Print window ids of open windows.',
                'start' : 'Start view synchronization',
                'stop' : 'Stop view synchronization',
                'remove_all' : 'Unsynchronize all windows.',
                'add_all' : 'Synchronize all windows.',
                'add' : 'Add list of window ids for synchronization.',
                'remove' : 'Remove list of window ids from synchronization.',
            }
class solution(metaclass=PyMenuMeta):
    """Enter solution menu."""
    class calculation_activities(metaclass=PyMenuMeta):
        """Enter calculation activities menu"""
        class animate(metaclass=PyMenuMeta):
            """Enter the animation menu."""
            doc_by_method = {
                'define' : 'Enter the animation definition menu.',
                'objects' : 'Enter to define, edit, delete solution animation objects',
            }
        class auto_save(metaclass=PyMenuMeta):
            """Enter the auto save menu."""
            doc_by_method = {
                'case_frequency' : 'Set the preference for saving case files.',
                'data_frequency' : 'Set the iteration or time step increment for saving data files.',
                'root_name' : 'Set the root name for auto-saved files. The number of iterations or time steps will be appended to this root name.',
                'retain_most_recent_files' : 'After the maximum (as in max-files) is reached, a file will be deleted for each file saved.',
                'max_files' : 'Set the maximum number of data files to save. After the maximum is reached, a file will be deleted for each file saved.',
                'append_file_name_with' : 'Set the suffix for auto-saved files. The file name can be appended by flow-time, time-step value or by user specified flags in file name.',
                'save_data_file_every' : 'Set the auto save frequency type to either time-step or crank-angle and set the corresponding frequency.',
            }
        class cell_register_operations(metaclass=PyMenuMeta):
            """Manage Cell Register Operations"""
            doc_by_method = {
                'add' : 'Add a new object',
                'edit' : 'Edit an object',
                'delete' : 'Delete an object',
                'list' : 'List objects',
                'list_properties' : 'List properties of an object',
            }
        class execute_commands(metaclass=PyMenuMeta):
            """Enter the execute-monitor-commands menu."""
            doc_by_method = {
                'add_edit' : 'Add or edit execute-commands.',
                'enable' : 'Enable an execute-command.',
                'disable' : 'Disable an execute-command.',
            }
        class solution_strategy(metaclass=PyMenuMeta):
            """Enter the automatic initialization and case modification strategy menu"""
            doc_by_method = {
                'enable_strategy' : 'Specify whether automatic initialization and case modification should be enabled',
                'execute_strategy' : 'Execute the automatic initialization and case modification strategy defined at present',
                'continue_strategy_execution' : 'Continue execution of the automatic initialization and case modification strategy defined at present',
                'automatic_initialization' : 'Define how the case is to be initialized automatically.',
                'automatic_case_modification' : 'Define how the case is to be modified as the solution progresses.',
            }
    class cell_registers(metaclass=PyMenuMeta):
        """Manage Cell Registers"""
        doc_by_method = {
            'adapt' : 'Adapt cell register objects.',
            'add' : 'Add a new object',
            'apply_poor_mesh_numerics' : 'Apply poor mesh numerics to cell register objects.',
            'coarsen' : 'Coarsen cell register objects.',
            'display' : 'Display cell register objects.',
            'edit' : 'Edit an object',
            'delete' : 'Delete an object',
            'list' : 'List objects',
            'list_properties' : 'List properties of an object',
            'refine' : 'Refine cell register objects.',
        }
    class controls(metaclass=PyMenuMeta):
        """Enter the controls menu."""
        doc_by_method = {
            'courant_number' : 'Set the fine mesh Courant number (time step factor).',
            'equations' : 'Enter the equations menu.',
            'limits' : 'Set solver limits for the values of various solution variables.',
            'p_v_controls' : 'Set P-V-Controls.',
            'relaxation_factor' : 'Enter the relaxation-factor menu.',
            'set_controls_to_default' : 'Set controls to default values.',
            'under_relaxation' : 'Enter the under-relaxation menu.',
        }
        class acoustics_wave_equation_controls(metaclass=PyMenuMeta):
            """Enter menu for acoustics wave equation solver controls."""
            doc_by_method = {
                'expert' : 'Enter menu for expert controls.',
                'relative_convergence_criterion' : 'Specify convergence tolerance for the timestep iterations
as the target residual reduction factor.',
                'max_iterations_per_timestep' : 'Specify maximum number of iterations per timestep.',
            }
        class advanced(metaclass=PyMenuMeta):
            """Controls advanced options"""
            doc_by_method = {
                'amg_options' : 'Enter AMG options menu.',
                'correction_tolerance' : 'Enter the correction tolerance menu.',
                'fast_transient_settings' : 'Enter the fast transient settings menu.',
                'multi_grid_amg' : 'Set the parameters that govern the algebraic multigrid procedure.',
                'multi_grid_controls' : 'Enter the multi-grid-controls menu.',
                'multi_grid_fas' : 'Set the coefficients that govern the FAS multigrid procedure.',
                'multi_stage' : 'Set the multiple-stage time stepping scheme coefficients.',
                'relaxation_method' : 'Set the solver relaxation method.',
                'slope_limiter_set' : 'Enter the slope limiter set menu.',
            }
        class contact_solution_controls(metaclass=PyMenuMeta):
            """solver controls for contact marks method"""
            doc_by_method = {
                'solution_stabilization' : 'Automatic solver settings adjustment for solution stabilization during contact process',
                'set_settings_to_default' : 'set contact solution stabilization to default',
                'verbosity' : 'specify verbosity level for contact solution controls',
                'parameters' : 'parameters used in stabilization strategy',
                'spatial' : 'spatial discretization control options',
                'transient' : 'transient discretization control options ',
                'amg' : 'AMG control options',
                'models' : 'model control options',
                'methods' : 'methods control options',
                'miscellaneous' : 'miscellaneous',
            }
        class query(metaclass=PyMenuMeta):
            """Enter controls query menu."""
            doc_by_method = {
                'acoustics_wave_equation_controls' : 'Enter menu for acoustics wave equation solver controls.',
                'advanced' : 'Controls advanced options',
                'courant_number' : 'Get the fine mesh Courant number (time step factor).',
                'equations' : 'Enter the equations menu.',
                'limits' : 'Get solver limits for the values of various solution variables.',
                'p_v_controls' : 'Get P-V-Controls.',
                'relaxation_factor' : 'Enter the relaxation-factor menu.',
                'under_relaxation' : 'Enter under relaxation menu.',
            }
    class expert(metaclass=PyMenuMeta):
        """Enter expert options for solution"""
        doc_by_method = {
            'alternate_wall_temp_formulation' : 'Alternate formulation for wall temperatures?',
            'bc_pressure_extrapolations' : 'Setting pressure extrapolations schemes on boundaries.',
            'bcd_boundedness' : 'BCD scheme boundedness strength, constant or expression (0 to 1)',
            'bcd_weights_freeze' : 'At each timestep, freeze BCD scheme weights after specified iteration
in order to improve timestep convergence.',
            'correction_form' : 'Discretize momentum equations in correction form for the pressure-based solver.',
            'disable_reconstruction' : 'Enable/Disable reconstruction. When disabled, accuracy will be first-order.',
            'energy_numerical_noise_filter' : 'The energy equation numerical noise filter can be enabled to eliminate non-physical numerical noise in the energy field.
     The numerical noise can appear in solution fields where large variations in specific heat or combustion with phase change are present.
     Using the energy equation numerical noise filter increases robustness, but may make the solution slightly more diffusive.',
            'explicit_under_relaxation_value' : 'Explicit under-relaxation value.',
            'equation_ordering' : 'Set the equation order',
            'flow_warnings' : 'Control the display of warning diagnostics for boundaries with reversed flow, etc.',
            'limiter_warnings' : 'Control the display of limiter warning diagnostics.',
            'linearized_mass_transfer_udf' : 'Use linearized mass transfer UDFs?',
            'lock_solid_temperature' : 'Lock the temperature for all solid and shell cell zones in the domain.',
            'material_property_warnings' : 'Control the display of material property warning diagnostics:
 0 - off (no messages)
 1 - messages per material
 2 - messages per material and per property',
            'mp_mfluid_aniso_drag' : 'Set anisotropic drag parameters for Eulerian multiphase.',
            'mp_reference_density' : 'Set reference density option for Eulerian multiphase.',
            'numerical_beach_controls' : 'Set damping function in flow direction',
            'open_channel_controls' : '
Set additional open channel controls',
            'retain_cell_residuals' : 'Retain cell residuals for postprocessing?',
            'retain_temporary_solver_mem' : 'Retain temporary solver memory?',
            'set_all_species_together' : 'Set all species discretizations and URFs together.',
            'show_all_discretization_schemes' : 'Allow selection of all applicable discretization schemes?',
            'singhal_et_al_cavitation_model' : 'Use Singhal-et-al cavitation model?',
            'surface_tension' : 'Set surface-tension calculation options.',
            'surface_tension_expert' : 'Set surface-tension expert options.',
            'vof_explicit_controls' : 'Set Explicit VOF controls.',
        }
        class divergence_prevention(metaclass=PyMenuMeta):
            """Enter the divergence prevention menu."""
            doc_by_method = {
                'enable' : 'Enable divergence prevention.',
            }
        class high_speed_numerics(metaclass=PyMenuMeta):
            """Enter high-speed-numerics menu"""
            doc_by_method = {
                'enable' : 'Enable/disable high-speed-numerics.',
                'expert' : 'expert high-speed-numerics.',
                'visualize_pressure_discontinuity_sensor' : 'Enable/disable pressure-discontinuity-sensor visualization.',
            }
        class poor_mesh_numerics(metaclass=PyMenuMeta):
            """Enter Poor Mesh Numerics Menu."""
            doc_by_method = {
                'enable' : 'Solution correction on meshes of poor quality.',
                'cell_quality_based' : 'Enable/disable poor mesh numerics on cells with low quality.',
                'set_quality_threshold' : 'Set quality threshold.',
                'solution_and_quality_based' : 'Enable/disable poor mesh numerics based on solution and cell quality.',
                'gradient_quality_based' : 'Enable/disable poor mesh numerics based on cell gradient quality.',
                'orthogonality_enhancing_cell_centroids' : 'Relocate select cell centroids, to improve orthogonality metrics and solution stability.',
                'solution_based_pmn' : 'Solution based poor-mesh numerics menu',
                'user_defined_on_register' : 'Include cells in register in poor mesh numerics.',
                'reset_poor_elements' : 'Reset marking of poor cell elements.',
                'print_poor_elements_count' : 'Print poor cells count.',
                'enhanced_pmn' : 'This option is available with the density-based solver. When enabled, it will apply quality-based poor-mesh-numerics order=1 on any cells with a quality-measure below 0.2. In addition, their CFL number is limited to 1.0.',
            }
        class previous_defaults(metaclass=PyMenuMeta):
            """Enter previous defaults menu."""
            doc_by_method = {
                'undo_r19_point_0_default_changes' : 'Undo default changes introduced in R19.0.',
                'undo_2019r1_default_changes' : 'Undo default changes introduced in 2019R1.',
                'undo_2019r3_default_changes' : 'Undo default changes introduced in 2019R3.',
                'undo_2021r1_default_changes' : 'Undo default changes introduced in 2021R1.',
                'undo_2021r2_default_changes' : 'Undo default changes introduced in 2021R2.',
                'undo_2022r1_default_changes' : 'Undo default changes introduced in 2022R1.',
            }
        class non_reflecting_boundary_treatment(metaclass=PyMenuMeta):
            """Enter non reflecting boundary treatment using minimal pressure reflection approach menu."""
            doc_by_method = {
                'pressure_inlet' : 'Enabling the use of minimal pressure reflection treatment. This treatment will minimize pressure wave reflections from the boundaries on which this option is active, but not necessarily fully eliminating them. The reflections would be of an acceptable limit in order to not contaminate the solution, the simulation will gain from the robustness of the new algorithm compared to traditional non-reflecting boundary condition treatment.',
                'pressure_outlet' : 'Enabling the use of minimal pressure reflection treatment. This treatment will minimize pressure wave reflections from the boundaries on which this option is active, but not necessarily fully eliminating them. The reflections would be of an acceptable limit in order to not contaminate the solution, the simulation will gain from the robustness of the new algorithm compared to traditional non-reflecting boundary condition treatment.',
                'velocity_inlet' : 'Enabling the use of minimal pressure reflection treatment. This treatment will minimize pressure wave reflections from the boundaries on which this option is active, but not necessarily fully eliminating them. The reflections would be of an acceptable limit in order to not contaminate the solution, the simulation will gain from the robustness of the new algorithm compared to traditional non-reflecting boundary condition treatment.',
            }
        class open_channel_wave_options(metaclass=PyMenuMeta):
            """Enter the open-channel-wave-options menu"""
            doc_by_method = {
                'set_verbosity' : 'set open channel wave verbosity',
                'stokes_wave_variants' : 'set stokes wave theory variants',
                'set_buffer_layer_ht' : 'set bufer layer height between phases for segregated velocity inputs',
            }
        class secondary_gradient_limiting(metaclass=PyMenuMeta):
            """Enter the Secondary Gradient Limiting Menu."""
            doc_by_method = {
                'energy' : 'Enable/disable secondary gradient limiting at coupled walls for energy equation.',
                'uds' : 'Enable/disable secondary gradient limiting at coupled walls for user-defined scalars.',
                'mesh_quality_limits' : 'Specify minimum and maximum mesh quality limits.',
            }
    class initialize(metaclass=PyMenuMeta):
        """Enter the flow initialization menu."""
        doc_by_method = {
            'open_channel_auto_init' : 'Open channel automatic initialization.',
            'levelset_auto_init' : 'Levelset function automatic initialization.',
            'dpm_reset' : 'Reset discrete phase source terms to zero.',
            'lwf_initialization' : 'Delete wall film particles and initialize wall film variables to zero.',
            'initialize_flow' : 'Initialize the flow field with the current default values.',
            'init_acoustics_options' : 'Specify number of timesteps for ramping of sources
and initialize acoustics model variables.
During ramping the sound sources are multiplied by a factor smoothly growing from 0 to 1.',
            'hyb_initialization' : 'Initialize using the hybrid initialization method.',
            'init_flow_statistics' : 'Initialize statistics.',
            'patch' : 'Patch a value for a flow variable in the domain.',
            'show_time_sampled' : 'Display the amount of simulated time covered by the data sampled for unsteady statistics.',
            'show_iterations_sampled' : 'Display the amount of simulated iterations covered by the data sampled for steady statistics.',
            'init_turb_vel_fluctuations' : 'Initialize turbulent velocity fluctuations.',
            'fmg_initialization' : 'Initialize using the full-multigrid initialization (FMG).',
            'repair_wall_distance' : 'Correct wall distance at very high aspect ratio hexahedral/polyhedral cells',
            'set_defaults' : 'Enter the set defaults menu.',
            'set_fmg_initialization' : 'Enter the set full-multigrid for initialization menu.',
            'list_defaults' : 'List default values.',
            'reference_frame' : 'Set reference frame absolute or relative',
        }
        class compute_defaults(metaclass=PyMenuMeta):
            """Enter the compute defaults menu."""
            doc_by_method = {
                'axis' : 'Compute flow-initialization defaults from a zone of this type.',
                'degassing' : 'Compute flow-initialization defaults from a zone of this type.',
                'dummy_entry' : '',
                'all_zones' : 'Initialize the flow field with the default values.',
                'exhaust_fan' : 'Compute flow-initialization defaults from a zone of this type.',
                'fan' : 'Compute flow-initialization defaults from a zone of this type.',
                'fluid' : 'Compute flow-initialization defaults from a zone of this type.',
                'inlet_vent' : 'Compute flow-initialization defaults from a zone of this type.',
                'intake_fan' : 'Compute flow-initialization defaults from a zone of this type.',
                'interface' : 'Compute flow-initialization defaults from a zone of this type.',
                'interior' : 'Compute flow-initialization defaults from a zone of this type.',
                'mass_flow_inlet' : 'Compute flow-initialization defaults from a zone of this type.',
                'mass_flow_outlet' : 'Compute flow-initialization defaults from a zone of this type.',
                'network' : 'Compute flow-initialization defaults from a zone of this type.',
                'network_end' : 'Compute flow-initialization defaults from a zone of this type.',
                'outflow' : 'Compute flow-initialization defaults from a zone of this type.',
                'outlet_vent' : 'Compute flow-initialization defaults from a zone of this type.',
                'overset' : 'Compute flow-initialization defaults from a zone of this type.',
                'periodic' : 'Compute flow-initialization defaults from a zone of this type.',
                'porous_jump' : 'Compute flow-initialization defaults from a zone of this type.',
                'pressure_far_field' : 'Compute flow-initialization defaults from a zone of this type.',
                'pressure_inlet' : 'Compute flow-initialization defaults from a zone of this type.',
                'pressure_outlet' : 'Compute flow-initialization defaults from a zone of this type.',
                'radiator' : 'Compute flow-initialization defaults from a zone of this type.',
                'rans_les_interface' : 'Compute flow-initialization defaults from a zone of this type.',
                'recirculation_inlet' : 'Compute flow-initialization defaults from a zone of this type.',
                'recirculation_outlet' : 'Compute flow-initialization defaults from a zone of this type.',
                'shadow' : 'Compute flow-initialization defaults from a zone of this type.',
                'solid' : 'Compute flow-initialization defaults from a zone of this type.',
                'symmetry' : 'Compute flow-initialization defaults from a zone of this type.',
                'velocity_inlet' : 'Compute flow-initialization defaults from a zone of this type.',
                'wall' : 'Compute flow-initialization defaults from a zone of this type.',
            }
        class mp_localized_turb_init(metaclass=PyMenuMeta):
            """Localized initialization of turbulent flow variables for VOF/Mixture multiphase flow models"""
            doc_by_method = {
                'enable' : 'localized initialization of turbulent flow variables for VOF/Mixture multiphase flow models',
                'turb_init_parameters' : 'turbulent flow parameters for localized initialization',
            }
        class vof_patch_smooth_options(metaclass=PyMenuMeta):
            """Enter the vof patch/smooth options menu"""
            doc_by_method = {
                'set_options' : 'Patch and smoothing options for volume fraction',
                'execute_smoothing' : 'Execute volumetric smoothing for volume fraction',
            }
        class set_fmg_options(metaclass=PyMenuMeta):
            """Enter the full-multigrid option menu."""
            doc_by_method = {
                'enable_viscous_terms' : 'Enable viscous terms during FMG initialization',
                'set_turbulent_viscosity_ratio' : 'Set turbulent viscosity ratio used during FMG initialization',
            }
        class set_hyb_initialization(metaclass=PyMenuMeta):
            """Enter the settings for hybrid initialization method."""
            doc_by_method = {
                'general_settings' : 'Enter the general settings menu.',
                'turbulent_settings' : 'Enter the turbulent settings menu.',
                'species_settings' : 'Enter the species settings menu.',
            }
    class methods(metaclass=PyMenuMeta):
        """Enter the methods menu."""
        doc_by_method = {
            'accelerated_non_iterative_time_marching' : 'Enable/disable accelerated non-iterative time marching',
            'convergence_acceleration_for_stretched_meshes' : 'Enable convergence acceleration for stretched meshes to improve the convergence of the implicit density based solver on meshes with high cell stretching',
            'discretization_scheme' : 'Enter the discretization-scheme menu.',
            'flux_type' : 'Enter the flux type.',
            'frozen_flux' : 'Enable/disable frozen flux formulation for transient flows.',
            'gradient_scheme' : 'Set gradient options.',
            'nb_gradient_boundary_option' : 'Set ggnb options.',
            'noniterative_time_advance' : 'Enable/disable the noniterative time advancement scheme.',
            'p_v_coupling' : 'Select the pressure velocity coupling scheme.',
            'phase_based_vof_discretization' : 'Set phase based slope limiter for VOF compressive scheme.',
            'pseudo_transient' : 'pseudo transient formulation setup',
            'pseudo_relaxation_factor' : 'pseudo relaxation factor menu',
            'pseudo_transient_expert' : 'pseudo transient expert usage control',
            'reduced_rank_extrapolation' : 'Enable Reduced Rank Extrapolation method to accelerate solution time.',
            'reduced_rank_extrapolation_options' : 'Reduced Rank Extrapolation options.',
            'residual_smoothing' : 'Set residual smoothing factor and number of iterations.',
            'set_solution_methods_to_default' : 'Set solution methods to default values.',
            'unsteady_1st_order' : 'Enable/disable first-order unsteady solution model.',
            'unsteady_2nd_order' : 'Enable/disable the second-order unsteady solution model.',
            'unsteady_2nd_order_bounded' : 'Enable/disable bounded second-order unsteady formulation.',
            'unsteady_global_time' : 'Enable/disable the unsteady global-time-step solution model.',
            'vof_numerics' : 'Set VOF numeric options.',
        }
        class expert(metaclass=PyMenuMeta):
            """Enter expert menu."""
            doc_by_method = {
                'reactions' : 'Enable/disable the species reaction sources and set relaxation factor.',
                'numerics' : 'Set numeric options.',
            }
        class high_order_term_relaxation(metaclass=PyMenuMeta):
            """Enter High Order Relaxation Menu"""
            doc_by_method = {
                'enable' : 'Enable/Disable High Order Term Relaxation.',
                'options' : 'High Order Term Relaxation Options',
            }
        class multiphase_numerics(metaclass=PyMenuMeta):
            """Enter the multiphase numerics options menu"""
            doc_by_method = {
                'porous_media' : 'multiphase relative permeability numerics menu',
                'compressible_flow' : 'multiphase compressible numerics options menu',
                'boiling_parameters' : 'multiphase boiling parameters menu',
                'viscous_flow' : 'multiphase viscous flow numerics options menu',
                'heat_mass_transfer' : 'multiphase interphase heat and mass transfer numerics options menu',
                'advanced_stability_controls' : 'Stability controls for multiphase flow',
                'default_controls' : 'Multiphase default controls menu',
                'face_pressure_controls' : 'Enter the face pressure expert controls menu',
                'solution_stabilization' : 'VOF solution stabilization menu',
            }
        class nita_expert_controls(metaclass=PyMenuMeta):
            """Enter the nita expert controls menu"""
            doc_by_method = {
                'set_verbosity' : 'set nita verbosity option',
                'skewness_neighbor_coupling' : 'set skewness neighbor coupling for nita',
                'hybrid_nita_settings' : 'Select a hybrid NITA settings option for faster performance and better robustness.',
            }
        class overset(metaclass=PyMenuMeta):
            """Enter overset solver options menu."""
            doc_by_method = {
                'high_order_pressure' : 'High order pressure extrapolation at overset interface',
                'interpolation_method' : 'Choose the interpolation method for overset interface(s)',
                'orphan_cell_treatment' : 'Enable solver to run with orphans present',
                'expert' : 'Enter overset expert solver options menu',
            }
        class pseudo_time_method(metaclass=PyMenuMeta):
            """Enter the pseudo time method menu."""
            doc_by_method = {
                'formulation' : 'Select the pseudo time step size formulation for the pseudo time method.',
                'local_time_step_settings' : 'Adjust the settings for the local time step formulation.',
                'global_time_step_settings' : 'Adjust the settings for the global time step formulation.',
                'advanced_options' : 'Enter the advanced options menu to define pseudo time settings for equations.',
                'relaxation_factors' : 'Enter the relaxation factors menu to set the pseudo time explicit relaxation factors for equations.',
                'verbosity' : 'Set the verbosity for the pseudo time method.',
            }
        class query(metaclass=PyMenuMeta):
            """Enter methods query menu."""
            doc_by_method = {
                'discretization_scheme' : 'Enter the discretization-scheme menu.',
                'p_v_coupling' : 'Get the pressure velocity coupling scheme.',
            }
        class warped_face_gradient_correction(metaclass=PyMenuMeta):
            """Enter warped-face-gradient-correction menu."""
            doc_by_method = {
                'enable' : 'Enable Warped-Face Gradient Correction.',
                'turbulence_options' : 'Set turbulence Warped Face Gradient Correction',
            }
    class monitors(metaclass=PyMenuMeta):
        """Enter the monitors menu."""
        doc_by_method = {
            'convergence_conditions' : 'Manage convergence report',
            'set_average_over' : 'Set the average over input for monitors.',
        }
        class _(metaclass=PyMenuMeta):
            """Enter the convergence menu to add surface, volume, drag, lift and moment monitors to convergence criteria."""
            doc_by_method = {
                'add_edit' : 'Add or edit convergence criterion for surface, volume, drag, lift and moment monitors.',
                'frequency' : 'To set how often convergence checks are done with respect to iterations or time steps.',
                'list' : 'List defined convergence criteria for monitors.',
                'condition' : 'Option to stop the calculations. All convergence conditions are met or any convergence condition is met.',
                'average_over_last_n_iterations_timesteps' : 'Option to average over previous values for checking convergence.',
                'delete' : 'Delete a monitor from convergence criteria.',
            }
        class __(metaclass=PyMenuMeta):
            """Enter the statistic monitors menu."""
            doc_by_method = {
                'monitors' : 'Choose which statistics to monitor as printed and/or plotted output.',
                'plot' : 'Enable/disable plotting of statistics during iteration.',
                'print' : 'Enable/disable printing of statistics during iteration.',
                'write' : 'Enable/disable writing of statistics during iteration.',
                'window' : 'Specify first window in which statistics will be plotted during iteration.
Multiple statistics are plotted in separate windows, beginning with this one.',
                'file_basename' : 'Specify the file basename and extension. The name of the individual monitor will be insterted automatically.',
                'x_axis' : 'Choose what quantity to use on the abscissa in the plot and in the data written to files.',
            }
        class report_files(metaclass=PyMenuMeta):
            """Manage report files"""
            doc_by_method = {
                'add' : 'Add a new object',
                'clear_data' : 'Delete the report file from the system',
                'delete_all' : 'Delete all report file objects',
                'edit' : 'Edit an object',
                'delete' : 'Delete an object',
                'list' : 'List objects',
                'list_properties' : 'List properties of an object',
            }
        class report_plots(metaclass=PyMenuMeta):
            """Manage report plots"""
            doc_by_method = {
                'add' : 'Add a new object',
                'axes' : 'Set axes options of an object.',
                'clear_data' : 'Clear report plot data.',
                'curves' : 'Set curves options of an object.',
                'delete_all' : 'Delete all plot objects',
                'edit' : 'Edit an object',
                'delete' : 'Delete an object',
                'list' : 'List objects',
                'list_properties' : 'List properties of an object',
                'plot' : 'Plot',
            }
        class residual(metaclass=PyMenuMeta):
            """Enter the residual monitors menu."""
            doc_by_method = {
                'check_convergence' : 'Choose which currently-monitored residuals
should be checked for convergence.',
                'convergence_criteria' : 'Set convergence criteria for residuals which are
currently being both monitored and checked.',
                'criterion_type' : 'Set convergence criterion type',
                'monitor' : 'Choose which residuals to monitor as printed and/or plotted output.',
                'enhanced_continuity_residual' : 'Scale the continuity residuals locally based on the enhanced formulation.',
                'n_display' : 'Set the number of most recent residuals to display in plots.',
                'n_maximize_norms' : 'Set the number of iterations through which normalization
factors will be maximized.',
                'normalization_factors' : 'Set normalization factors for currently-monitored residuals.',
                'normalize' : 'Choose whether or not to normalize residuals in printed and plotted output.',
                'n_save' : 'Set number of residuals to be saved with data.
History is automatically compacted when buffer becomes full.',
                'plot' : 'Choose whether or not residuals will be plotted during iteration.',
                'print' : 'Choose whether or not residuals will be printed during iteration.',
                'relative_conv_criteria' : 'Set relative convergence criteria for residuals which are
currently being both monitored and checked.',
                're_normalize' : 'Renormalize residuals by maximum values.',
                'reset' : 'Delete the residual history and reset iteration counter to unity.',
                'scale_by_coefficient' : 'Enable/disable scaling of residuals by coefficient sum in printed and plotted output.',
            }
    class report_definitions(metaclass=PyMenuMeta):
        """Manage report definitions."""
        doc_by_method = {
            'add' : 'Add a new object',
            'copy' : 'Makes a copy of selected report definition with new name.',
            'delete_all' : 'Delete all report definition objects',
            'edit' : 'Edit an object',
            'delete' : 'Delete an object',
            'list' : 'List objects',
            'list_properties' : 'List properties of an object',
            'rename' : 'Rename selected report definition with new name.',
        }
    class run_calculation(metaclass=PyMenuMeta):
        """Enter run calculation menu"""
        doc_by_method = {
            'adaptive_time_stepping' : 'Set Error-based adaptive time-stepping parameters.',
            'cfl_based_adaptive_time_stepping' : 'Set CFL-based adaptive time-stepping parameters.',
            'data_sampling' : 'Set iteration options.',
            'dual_time_iterate' : 'Perform unsteady iterations.
Arguments:
  number_of_total_periods: int
  number_of_time_steps: int
  total_number_of_time_steps: int
  total_time: float
  incremental_time: float
  maximum_number_of_iterations_per_time_step: int
',
            'iterate' : 'Perform a specified number of iterations.
Arguments:
  number_of_iterations: int
',
            'max_corrections' : 'Enter the max-corrections menu.',
            'mesh_motion' : 'Perform mesh motion.',
            'multistage_time_iterate' : 'Perform unsteady iterations.',
            'number_of_iterations' : 'set number of iterations',
            'reporting_interval' : 'Set number of solver iterations before returning to scheme.',
            'residual_tolerance' : 'Enter the residual tolerance menu.',
            'residual_verbosity' : 'Set the residual report verbosity.',
            'second_order_time_options' : 'Set options for second-order time formulation.',
            'solution_steering' : 'Enable solution steering for density-based solver',
            'set_solution_steering' : 'Set Solution Steering Parameters',
            'summary' : 'Print report summary.',
            'time_step' : 'Set the time step.',
            'update_physical_time' : 'Update the solution to the next physical time level.',
            'variable_time_stepping' : 'Set Multiphase-Specific Adaptive time stepping parameters.',
        }
        class data_sampling_options(metaclass=PyMenuMeta):
            """data sampling options for statistics"""
            doc_by_method = {
                'add_datasets' : 'Add a dataset. After providing the zones for a dataset, press [Enter] to move onto selecting quantities. Enter () to complete the quantity selection for this dataset.',
                'add_rtdft_datasets' : 'Add a dataset. After providing the zones for a dataset, press [Enter] to move onto selecting quantities. Enter () to complete the quantity selection for this dataset.',
                'remove_dataset' : 'remove dataset',
                'list_datasets' : 'list dataset',
            }
        class transient_controls(metaclass=PyMenuMeta):
            """Enter into the transient controls menu."""
            doc_by_method = {
                'specified_time_step' : 'Use specified time step or courant number.',
                'fixed_user_specified' : 'Enable user-specified fixed time stepping method.',
                'fixed_periodic' : 'Set period- or frequency-based fixed time-stepping parameters.',
                'duration_specification_method' : 'Set Duration Specification Method: [0] Incremental Time Steps, [1] Total Time Steps, [2] Total Time, [3] Incremental Time',
                'incremental_time' : 'set Incremental Time.',
                'max_iterations_per_time_step' : 'set Max Iterations/Time step.',
                'number_of_time_steps' : 'set inceremtal number of Time steps.',
                'total_number_of_time_steps' : 'set total number of Time steps.',
                'total_time' : 'set Total Simulation Time.',
                'time_step_size' : 'Set the physical time step size.',
                'solution_status' : 'Activate the simulation status panel.',
                'extrapolate_vars' : 'Applies a predictor algorithm for computing initial condition at time step n+1.',
                'extrapolate_eqn_vars' : 'Enter the extrapolation menu.',
                'max_flow_time' : 'Set maximum flow time.',
                'cfl_based_time_stepping_advanced_options' : 'Set CFL-based adaptive time-stepping advanced parameters.',
                'cfl_based_time_stepping' : 'Set CFL-based adaptive time-stepping parameters.',
                'multiphase_specific_time_stepping' : 'Set Multiphase-specific adaptive time stepping parameters.',
                'multiphase_specific_time_constraints' : 'Set Multiphase-specific time constraints.',
                'udf_based_time_stepping' : 'Set the time-stepping parameters for user-defined time stepping method.',
                'error_based_time_stepping' : 'Set Error-based adaptive time-stepping parameters.',
                'undo_timestep' : 'Undo the previous time step.',
                'predict_next_time' : 'Applies a predictor algorithm for computing initial condition at time step n+1.',
                'rotating_mesh_flow_predictor' : 'Improve prediction of flow field at time step n+1 for rotating mesh.',
                'solid_time_step_size' : 'Specify a different time step size for solid zones.',
                'time_step_size_for_acoustic_export' : 'Set number of time step size for acoustic export.',
            }
class setup(metaclass=PyMenuMeta):
    """Enter setup menu."""
    class boundary_conditions(metaclass=PyMenuMeta):
        """Enter the boudary conditions menu."""
        doc_by_method = {
            'axis' : 'Set boundary conditions for a zone of this type.',
            'copy_bc' : 'Copy boundary conditions to another zone.',
            'degassing' : 'Set boundary conditions for a zone of this type.',
            'exhaust_fan' : 'Set boundary conditions for a zone of this type.',
            'fan' : 'Set boundary conditions for a zone of this type.',
            'fluid' : 'Set boundary conditions for a zone of this type.',
            'inlet_vent' : 'Set boundary conditions for a zone of this type.',
            'intake_fan' : 'Set boundary conditions for a zone of this type.',
            'interface' : 'Set boundary conditions for a zone of this type.',
            'interior' : 'Set boundary conditions for a zone of this type.',
            'list_zones' : 'List zone IDs, types, kinds, and names.',
            'mass_flow_inlet' : 'Set boundary conditions for a zone of this type.',
            'mass_flow_outlet' : 'Set boundary conditions for a zone of this type.',
            'network' : 'Set boundary conditions for a zone of this type.',
            'network_end' : 'Set boundary conditions for a zone of this type.',
            'outflow' : 'Set boundary conditions for a zone of this type.',
            'outlet_vent' : 'Set boundary conditions for a zone of this type.',
            'overset' : 'Set boundary conditions for a zone of this type.',
            'periodic' : 'Set boundary conditions for a zone of this type.',
            'porous_jump' : 'Set boundary conditions for a zone of this type.',
            'pressure_far_field' : 'Set boundary conditions for a zone of this type.',
            'pressure_inlet' : 'Set boundary conditions for a zone of this type.',
            'pressure_outlet' : 'Set boundary conditions for a zone of this type.',
            'radiator' : 'Set boundary conditions for a zone of this type.',
            'rans_les_interface' : 'Set boundary conditions for a zone of this type.',
            'recirculation_inlet' : 'Set boundary conditions for a zone of this type.',
            'recirculation_outlet' : 'Set boundary conditions for a zone of this type.',
            'shadow' : 'Set boundary conditions for a zone of this type.',
            'solid' : 'Set boundary conditions for a zone of this type.',
            'symmetry' : 'Set boundary conditions for a zone of this type.',
            'velocity_inlet' : 'Set boundary conditions for a zone of this type.',
            'wall' : 'Set boundary conditions for a zone of this type.',
            'zone_name' : 'Give a zone a new name.',
            'zone_type' : 'Set a zone's type.',
        }
        class bc_settings(metaclass=PyMenuMeta):
            """"""
            doc_by_method = {
                'mass_flow' : 'Select method for setting the mass flow rate.',
                'pressure_outlet' : 'Select pressure specification method on pressure-outlet boundaries.',
                'pressure_far_field' : 'Select presure-far-field boundary-condition options.',
            }
        class expert(metaclass=PyMenuMeta):
            """Enter expert bc menu."""
            doc_by_method = {
                'impedance_data_fitting' : 'Enter the impedance data fitting menu.',
                'non_overlapping_zone_name' : 'Get non-overlapping zone name from the associated interface zone',
                'non_reflecting_bc' : 'Enter the non-reflecting b.c. menu.',
                'openchannel_threads' : 'List open channel group IDs, names, types, and variables.',
                'open_channel_wave_settings' : 'Open channel wave input analysis',
                'perforated_walls' : 'Enter the perforated walls setting menu.',
                'periodic_conditions' : 'Enter the periodic conditions menu.',
                'target_mass_flow_rate_settings' : 'Enter the targeted mass flow rate setting menu.',
            }
        class modify_zones(metaclass=PyMenuMeta):
            """Enter the modify zones menu."""
            doc_by_method = {
                'activate_cell_zone' : 'Activate a cell thread.',
                'append_mesh' : 'Append new mesh.',
                'append_mesh_data' : 'Append new mesh with data.',
                'copy_move_cell_zone' : 'Copy and translate or rotate a cell zone.',
                'create_all_shell_threads' : 'Mark all finite thickness wall for shell creation. Shell zones will be created at the start of iterations.',
                'deactivate_cell_zone' : 'Deactivate cell thread.',
                'recreate_all_shells' : 'Create shell on all the walls where which were deleted using the command delete-all-shells',
                'delete_all_shells' : 'Delete all shell zones and switch off shell conduction on all the walls. These zones can be recreated using the command recreate-all-shells',
                'delete_cell_zone' : 'Delete a cell thread.',
                'extrude_face_zone_delta' : 'Extrude a face thread a specified distance based on a list of deltas.',
                'extrude_face_zone_para' : 'Extrude a face thread a specified distance based on a distance and a list of parametric locations between 0 and 1 (eg. 0 0.2 0.4 0.8 1.0).',
                'fuse_face_zones' : 'Attempt to fuse zones by removing duplicate faces and nodes.',
                'list_zones' : 'List zone IDs, types, kinds, and names.',
                'make_periodic' : 'Attempt to establish periodic/shadow face zone connectivity.',
                'create_periodic_interface' : 'Create a conformal or non-conformal periodic interface.',
                'scale_zone' : 'Scale nodal coordinates of input cell zones.',
                'rotate_zone' : 'Rotate nodal coordinates of input cell zones.',
                'translate_zone' : 'Translate nodal coordinates of input cell zones.',
                'matching_tolerance' : 'Set the normalized tolerance used for finding coincident nodes.',
                'merge_zones' : 'Merge zones of the same type and condition into one.',
                'mrf_to_sliding_mesh' : 'Change motion specification from MRF to moving mesh',
                'convert_all_solid_mrf_to_solid_motion' : 'Change all solid zones motion specification from MRF to solid motion',
                'orient_face_zone' : 'Orient the face zone.',
                'replace_zone' : 'Replace a cell zone.',
                'sep_cell_zone_mark' : 'Separate a cell zone based on cell marking.',
                'sep_cell_zone_region' : 'Separate a cell zone based on contiguous regions.',
                'sep_face_zone_angle' : 'Separate a face zone based on significant angle.',
                'sep_face_zone_face' : 'Separate each face in a zone into unique zone.',
                'sep_face_zone_mark' : 'Separate a face zone based on cell marking.',
                'sep_face_zone_region' : 'Separate a face zone based on contiguous regions.',
                'slit_periodic' : 'Slit a periodic zone into two symmetry zones.',
                'slit_face_zone' : 'Slit a two-sided wall into two connected wall zones.',
                'slit_interior_between_diff_solids' : 'Slit interior created between different solids into coupled walls',
                'zone_name' : 'Give a zone a new name.',
                'zone_type' : 'Set a zone's type.',
                'copy_mrf_to_mesh_motion' : 'Copy motion variable values for origin, axis and velocities from Frame Motion to Mesh Motion.',
                'copy_mesh_to_mrf_motion' : 'Copy motion variable values for origin, axis and velocities from Mesh Motion to Frame Motion.',
                'change_zone_state' : 'Change the realgas material state for a zone.',
                'change_zone_phase' : 'Change the realgas phase for a zone.',
            }
        class profiles(metaclass=PyMenuMeta):
            """Enter the boundary profiles menu."""
            doc_by_method = {
                'display_profile_surface' : 'Display a profile.',
                'display_profile_point_cloud_data' : 'Display Profile Point Cloud Data.',
                'overlay_profile_surface' : 'Overlay Profile Surface',
                'overlay_profile_point_cloud_data' : 'Overlay Profile Point Cloud Data',
                'set_preference_profile_point_cloud_data' : 'Set Preference Profile Point Cloud Data e.g., Point marker symbol,size,color',
                'list_profile_parameters' : 'List the parameters of a particular profile.',
                'delete' : 'Delete a profile.',
                'delete_all' : 'Delete all boundary-profiles.',
                'list_profiles' : 'List all profiles.',
                'list_profile_fields' : 'List the fields of a particular profile.',
                'interpolation_method' : 'Choose the method for interpolation of profiles.',
                'morphing' : 'Enable/disable profile morphing options in Orient Profile panel.',
                'update_interval' : 'Set interval between updates of dynamic profiles.',
                'link_profile_to_reference_frame' : 'Link profile to a reference frame.',
                'replicate_profile' : 'Replicate Profile.',
                'orient_profile' : 'Orient Profile.',
            }
        class query(metaclass=PyMenuMeta):
            """Enter zone query menu."""
            doc_by_method = {
                'axis' : 'Show boundary conditions for a zone of this type.',
                'degassing' : 'Show boundary conditions for a zone of this type.',
                'delete_query' : 'Delete saved query.',
                'exhaust_fan' : 'Show boundary conditions for a zone of this type.',
                'fan' : 'Show boundary conditions for a zone of this type.',
                'fluid' : 'Show boundary conditions for a zone of this type.',
                'inlet_vent' : 'Show boundary conditions for a zone of this type.',
                'intake_fan' : 'Show boundary conditions for a zone of this type.',
                'interface' : 'Show boundary conditions for a zone of this type.',
                'interior' : 'Show boundary conditions for a zone of this type.',
                'list_boundary_conditions' : 'List boundary conditions.',
                'list_cell_zone_conditions' : 'List cell zone conditions.',
                'mass_flow_inlet' : 'Show boundary conditions for a zone of this type.',
                'mass_flow_outlet' : 'Show boundary conditions for a zone of this type.',
                'named_zone_list' : 'Create named list of zones.',
                'list_named_selection' : 'List named selection of zone type',
                'list_queries' : 'List all saved queries',
                'network' : 'Show boundary conditions for a zone of this type.',
                'network_end' : 'Show boundary conditions for a zone of this type.',
                'outflow' : 'Show boundary conditions for a zone of this type.',
                'outlet_vent' : 'Show boundary conditions for a zone of this type.',
                'overset' : 'Show boundary conditions for a zone of this type.',
                'periodic' : 'Show boundary conditions for a zone of this type.',
                'porous_jump' : 'Show boundary conditions for a zone of this type.',
                'pressure_far_field' : 'Show boundary conditions for a zone of this type.',
                'pressure_inlet' : 'Show boundary conditions for a zone of this type.',
                'pressure_outlet' : 'Show boundary conditions for a zone of this type.',
                'radiator' : 'Show boundary conditions for a zone of this type.',
                'rans_les_interface' : 'Show boundary conditions for a zone of this type.',
                'recirculation_inlet' : 'Show boundary conditions for a zone of this type.',
                'recirculation_outlet' : 'Show boundary conditions for a zone of this type.',
                'shadow' : 'Show boundary conditions for a zone of this type.',
                'solid' : 'Show boundary conditions for a zone of this type.',
                'symmetry' : 'Show boundary conditions for a zone of this type.',
                'velocity_inlet' : 'Show boundary conditions for a zone of this type.',
                'wall' : 'Show boundary conditions for a zone of this type.',
            }
        class rename_zone(metaclass=PyMenuMeta):
            """Enter zone rename menu."""
            doc_by_method = {
                'rename_by_adjacency' : 'Rename zone to adjacent zones.',
                'rename_to_default' : 'Rename zone to default name.',
                'add_suffix_or_prefix' : 'Add suffix or prefix to zone name',
            }
        class set(metaclass=PyMenuMeta):
            """Enter the set boundary conditions menu."""
            doc_by_method = {
                'axis' : 'Set boundary conditions for a zone or multiple zones of this type.',
                'degassing' : 'Set boundary conditions for a zone or multiple zones of this type.',
                'exhaust_fan' : 'Set boundary conditions for a zone or multiple zones of this type.',
                'fan' : 'Set boundary conditions for a zone or multiple zones of this type.',
                'fluid' : 'Set boundary conditions for a zone or multiple zones of this type.',
                'inlet_vent' : 'Set boundary conditions for a zone or multiple zones of this type.',
                'intake_fan' : 'Set boundary conditions for a zone or multiple zones of this type.',
                'interface' : 'Set boundary conditions for a zone or multiple zones of this type.',
                'interior' : 'Set boundary conditions for a zone or multiple zones of this type.',
                'mass_flow_inlet' : 'Set boundary conditions for a zone or multiple zones of this type.',
                'mass_flow_outlet' : 'Set boundary conditions for a zone or multiple zones of this type.',
                'network' : 'Set boundary conditions for a zone or multiple zones of this type.',
                'network_end' : 'Set boundary conditions for a zone or multiple zones of this type.',
                'outflow' : 'Set boundary conditions for a zone or multiple zones of this type.',
                'outlet_vent' : 'Set boundary conditions for a zone or multiple zones of this type.',
                'overset' : 'Set boundary conditions for a zone or multiple zones of this type.',
                'periodic' : 'Set boundary conditions for a zone or multiple zones of this type.',
                'porous_jump' : 'Set boundary conditions for a zone or multiple zones of this type.',
                'pressure_far_field' : 'Set boundary conditions for a zone or multiple zones of this type.',
                'pressure_inlet' : 'Set boundary conditions for a zone or multiple zones of this type.',
                'pressure_outlet' : 'Set boundary conditions for a zone or multiple zones of this type.',
                'radiator' : 'Set boundary conditions for a zone or multiple zones of this type.',
                'rans_les_interface' : 'Set boundary conditions for a zone or multiple zones of this type.',
                'recirculation_inlet' : 'Set boundary conditions for a zone or multiple zones of this type.',
                'recirculation_outlet' : 'Set boundary conditions for a zone or multiple zones of this type.',
                'shadow' : 'Set boundary conditions for a zone or multiple zones of this type.',
                'solid' : 'Set boundary conditions for a zone or multiple zones of this type.',
                'symmetry' : 'Set boundary conditions for a zone or multiple zones of this type.',
                'velocity_inlet' : 'Set boundary conditions for a zone or multiple zones of this type.',
                'wall' : 'Set boundary conditions for a zone or multiple zones of this type.',
            }
        class pressure_far_field_objects(metaclass=PyMenuMeta):
            """"""
            doc_by_method = {
                'pressure_far_field' : '',
            }
        class velocity_inlet_objects(metaclass=PyMenuMeta):
            """"""
            doc_by_method = {
                'velocity_inlet' : '',
            }
        class pressure_inlet_objects(metaclass=PyMenuMeta):
            """"""
            doc_by_method = {
                'pressure_inlet' : '',
            }
        class mass_flow_inlet_objects(metaclass=PyMenuMeta):
            """"""
            doc_by_method = {
                'mass_flow_inlet' : '',
            }
        class wall_objects(metaclass=PyMenuMeta):
            """"""
            doc_by_method = {
                'wall' : '',
            }
        class pressure_outlet_objects(metaclass=PyMenuMeta):
            """"""
            doc_by_method = {
                'pressure_outlet' : '',
            }
        class symmetry_objects(metaclass=PyMenuMeta):
            """"""
            doc_by_method = {
                'symmetry' : '',
            }
        class periodic_objects(metaclass=PyMenuMeta):
            """"""
            doc_by_method = {
                'periodic' : '',
            }
    class dynamic_mesh(metaclass=PyMenuMeta):
        """Enter the dynamic mesh menu."""
        doc_by_method = {
            'dynamic_mesh' : 'Enable/disable the dynamic mesh solver and options.',
        }
        class controls(metaclass=PyMenuMeta):
            """Enter the dynamic mesh control menu."""
            doc_by_method = {
                'in_cylinder_output' : 'Enable/disable in-cylinder output.',
                'smoothing' : 'Enable/disable dynamic mesh smoothing.',
                'smoothing_parameters' : 'Enter the dynamic mesh smoothing menu.',
                'layering' : 'Enable/disable dynamic-layering in quad/hex cell zones.',
                'layering_parameters' : 'Enter the dynamic mesh layering menu.',
                'remeshing' : 'Enable/disable local remeshing in tri/tet and mixed cell zones.',
                'remeshing_parameters' : 'Enter the dynamic mesh remeshing menu.',
                'in_cylinder_parameters' : 'Enter the dynamic mesh in-cylinder menu.',
                'implicit_update_parameters' : 'Enter the dynamic mesh implicit update menu.',
                'six_dof_parameters' : 'Enter the dynamic mesh six-dof menu.',
                'periodic_displacement_parameters' : 'Enter the dynamic mesh periodic displacement menu.',
                'contact_parameters' : 'Enter the dynamic mesh contact detection menu.',
                'steady_pseudo_time_control' : 'Enable/disable pseudo time step control in user interface.',
            }
        class events(metaclass=PyMenuMeta):
            """Enter the dynamic mesh events menu."""
            doc_by_method = {
                'import_event_file' : 'Import dynamic mesh event file.',
                'export_event_file' : 'Export dynamic mesh events to file.',
            }
        class zones(metaclass=PyMenuMeta):
            """Enter the dynamic mesh zones menu."""
            doc_by_method = {
                'create' : 'Create dynamic zone.',
                'delete' : 'Delete dynamic zone.',
                'list' : 'List dynamic zones.',
                'insert_boundary_layer' : 'Insert new cell zone.',
                'remove_boundary_layer' : 'Remove cell zone.',
                'insert_interior_layer' : 'Insert new layer cell zone at specified location.',
                'remove_interior_layer' : 'Remove interior layer cell zone.',
            }
        class actions(metaclass=PyMenuMeta):
            """Enter the dynamic mesh actions menu."""
            doc_by_method = {
                'remesh_cell_zone' : 'Manually remesh cell zone with option to remesh adjacent dynamic face zones.',
            }
        class transient_settings(metaclass=PyMenuMeta):
            """Enter the dynamic mesh transient settings menu."""
            doc_by_method = {
                'verbosity' : 'Enable/disable transient scheme verbosity for dynamic mesh cases',
                'allow_second_order' : 'Enable/disable 2nd order transient scheme for dynamic mesh cases',
            }
    class expert(metaclass=PyMenuMeta):
        """Enter expert setup menu."""
        doc_by_method = {
            'beta_feature_access' : 'Enable access to beta features in the interface.',
            'enable_mesh_morpher_optimizer' : 'Enable use of mesh morpher/optimizer.',
            'heterogeneous_stiff_chemistry' : 'Set heterogeneous stiff-chemistry solver.',
            'stiff_chemistry' : 'Set solver options for stiff-chemistry solutions.',
        }
        class spectral(metaclass=PyMenuMeta):
            """Enter the Spectral menu."""
            doc_by_method = {
                'calculate_fourier_coefficients' : 'Calculates Fourier coefficient data',
                'delete_fourier_coefficients' : 'Deletes Fourier coefficient data',
                'calculate_harmonic_exports' : 'Calculates Harmonic Export data',
                'delete_harmonic_exports' : 'Deletes Harmonic Export data',
            }
    class gap_model(metaclass=PyMenuMeta):
        """Enter the narrow-gaps menu."""
        doc_by_method = {
            'enable' : 'Enable/Disable gap model.',
            'create' : 'Create a gap object.',
            'edit' : 'Edit an exiting gap object.',
            'delete' : 'Delete an exiting gap object.',
            'delete_all' : 'Delete all of the exiting gap objects.',
            'list_gap_regions' : 'List gap regions.',
            'list_gap_face_zones' : 'List name of the gap face zones that can be used for gaps creation.',
            'list_gap_cell_zones' : 'List name of the gap cells zones that can be used as exclided cell zones in gaps creation.',
            'render_gap_regions' : 'Update gap regions for postprocessing.',
        }
        class advanced_options(metaclass=PyMenuMeta):
            """Show options."""
            doc_by_method = {
                'expert' : 'Enable expert options for gap model.',
                'alternative_marking' : 'Mark gap regions using an alternative marking algorithm.',
                'cell_check_distance_factor' : 'Enter value of the cell distance factor.',
                'flow_blocking_stabilization_parameters' : 'Adjust stabilization settings for the sponge layer used for blocked gap regions.',
                'update_gap_regions' : 'Update gap regions and gap model solution information',
                'clear_gap_regions' : 'Clear gap model solution information and marks.',
                'precise_gap_marking' : 'mark cells in gap regions using more accurate search algorithm.',
                'render_flow_modeling_gaps' : 'render solution inside flow modeling gap cells.',
                'reduce_gap_regions' : 'Using a more restrictive algorithm for marking cells in gap regions.',
                'fill_data_in_gap_regions' : 'Interpolate solution data into the whole gap regions.',
                'enhanced_data_interpolation' : 'Use enhanced data interpolation for updating information in gap regions.',
                'sponge_layer' : 'Set advanced settings for gap sponge layer.',
                'solution_stabilization' : 'Set solution stabilization level for gap model.',
                'include_coupled_walls' : 'Include coupled walls in gap face zones',
                'check_cfl_condition' : 'Check time step size for better convergence.',
                'extend_gap_regions' : 'Extend gap regions for better convergence.',
                'revert_controls_to_default' : 'Revert gap stabilization and any related solver settings to default.',
                'verbosity' : 'Set the verbosity for gap model.',
                'render_gap_interface' : 'Render gap interface.',
            }
    class materials(metaclass=PyMenuMeta):
        """Enter the materials menu."""
        doc_by_method = {
            'change_create' : 'Change the properties of a locally-stored material or create a new material.',
            'copy' : 'Copy a material from the database.',
            'copy_by_formula' : 'Copy a material from the database by formula.',
            'delete' : 'Delete a material from local storage.',
            'list_materials' : 'List all locally-stored materials.',
            'list_properties' : 'List the properties of a locally-stored material.',
        }
        class data_base(metaclass=PyMenuMeta):
            """Enter the database menu."""
            doc_by_method = {
                'database_type' : 'Set the database type.',
                'edit' : 'Edit a material.',
                'list_materials' : 'List all materials in the database.',
                'list_properties' : 'List the properties of a material in the database.',
                'new' : 'Define a new material',
                'save' : 'Save user-defined database.',
            }
    class mesh_interfaces(metaclass=PyMenuMeta):
        """Enter the mesh-interfaces menu."""
        doc_by_method = {
            'create' : 'Create a mesh interface.',
            'turbo_create' : 'Create a general turbo interface.',
            'edit' : 'Edit a mesh interface.',
            'delete' : 'Delete a mesh interface.',
            'display' : 'Display specified mesh interface zone.',
            'list' : 'List all mesh-interfaces.',
            'make_periodic' : 'Make interface zones periodic.',
            'make_phaselag_from_boundaries' : 'Make interface zones phase lagged.',
            'make_phaselag_from_periodic' : 'Convert periodic interface to phase lagged.',
            'delete_all' : 'Delete all mesh interfaces.',
            'enforce_continuity_after_bc' : 'Across the interface, enforces continuity over boundary condition',
            'verbosity' : 'Set mesh interface verbosity.',
            'enable_si_with_nodes' : 'Enable sliding interfaces with nodes',
            'enforce_coupled_wall_between_solids' : 'Create coupled wall interface between solids',
            'improve_quality' : 'Improve mesh interface quality',
            'one_to_one_pairing' : 'Use the default one-to-one interface creation method?',
            'auto_pairing' : 'Automatically pair and create mesh interfaces for some or all interface zones',
            'enable_visualization_of_interfaces' : 'Display facets on mesh interfaces',
            'transfer_motion_across_interfaces' : 'Transfer motion from one side of the interface to the other when only one side undergoes user-defined or system-coupling motion',
            'non_overlapping_zone_name' : 'Get non-overlapping zone name from the associated interface zone',
            'remove_left_handed_interface_faces' : 'Remove left-handed faces during mesh interface creation',
        }
        class non_conformal_interface_numerics(metaclass=PyMenuMeta):
            """Setting non-conformal numerics options"""
            doc_by_method = {
                'change_numerics' : 'Enable modified non-conformal interface numerics',
            }
        class mapped_interface_options(metaclass=PyMenuMeta):
            """Enter the mapped-interface-options menu."""
            doc_by_method = {
                'solution_controls' : 'Specification of mapped frequency and under-relaxation factor for mapped interfaces',
                'tolerance' : 'Specification of mapped interface tolerance',
                'convert_to_mapped_interface' : 'Convert non-conformal mesh interface to mapped mesh interfaces',
            }
        class auto_options(metaclass=PyMenuMeta):
            """Enter auto-options menu."""
            doc_by_method = {
                'proximity_tolerance' : 'Specification of auto pairing tolerance',
                'naming_option' : 'Specify whether or not to include an informative suffix to the mesh interface name.',
                'set_default_name_prefix' : 'Specification of auto pairing default name prefix',
                'set_one_to_one_pairing_tolerance' : 'Enable/disable one-to-one auto pairing tolerance',
                'pairing_between_different_cell_zones_only' : 'Pairing between interface zones from different cell zones only',
                'pairing_between_interface_zones_only' : 'Pairing between interface zones only',
                'keep_empty_interface' : 'Keep empty interfaces during one-to-one mesh interface creation',
            }
    class mixing_planes(metaclass=PyMenuMeta):
        """Enter the mixing planes menu."""
        doc_by_method = {
            'create' : 'Create a mixing plane.',
            'delete' : 'Delete a mixing plane.',
            'list' : 'List defined mixing plane(s).',
        }
        class set(metaclass=PyMenuMeta):
            """Enter the mixing plane set menu."""
            doc_by_method = {
                'under_relaxation' : 'Set mixing plane under-relaxation factor.',
                'averaging_method' : 'Set mixing plane profile averaging method',
                'fix_pressure_level' : 'Set fix pressure level using define/reference-pressure-location.',
                'conserve_swirl' : 'Enter the mixing plane conserve-swirl menu.',
                'conserve_total_enthalpy' : 'Enter the menu to set total enthalpy conservation in mixing plane menu.',
            }
    class models(metaclass=PyMenuMeta):
        """Enter the models menu to configure the solver."""
        doc_by_method = {
            'addon_module' : 'Load addon module.',
            'axisymmetric' : 'Enable/disable the axisymmetric model.',
            'solidification_melting' : 'Enable/disable the solidification and melting model.',
            'crevice_model' : 'Enable/disable the crevice model.',
            'crevice_model_controls' : 'Enter the crevice model controls menu.',
            'energy' : 'Enable/disable the energy model.',
            'noniterative_time_advance' : 'Enable/disable the noniterative time advancement scheme.',
            'nox' : 'Enable/disable the NOx model.',
            'soot' : 'Enable/disable the soot model.',
            'steady' : 'Enable/disable the steady solution model.',
            'swirl' : 'Enable/disable axisymmetric swirl velocity.',
            'unsteady_1st_order' : 'Enable/disable first-order unsteady solution model.',
            'frozen_flux' : 'Enable/disable frozen flux formulation for transient flows.',
            'unsteady_2nd_order' : 'Enable/disable the second-order unsteady solution model.',
            'unsteady_2nd_order_bounded' : 'Enable/disable bounded second-order unsteady formulation.',
            'unsteady_global_time' : 'Enable/disable the unsteady global-time-step solution model.',
            'unsteady_structure_newmark' : 'Enable/disable Newmark unsteady solution model.',
            'unsteady_structure_euler' : 'Enable/disable Backward Euler unsteady solution model.',
            'battery_model' : 'Enter battery model menu.',
            'ablation' : 'Enable/disable ablation model.',
            'potential_and_li_ion_battery' : 'Enable/disable the electric-potential model.',
        }
        class acoustics(metaclass=PyMenuMeta):
            """Enter the acoustics model menu."""
            doc_by_method = {
                'off' : 'Enable/disable the acoustics model.',
                'far_field_parameters' : 'Enter the far field parameters menu for the wave equation model.',
                'ffowcs_williams' : 'Enable/disable the Ffowcs-Williams-and-Hawkings model.',
                'broad_band_noise' : 'Enable/disable the broadband noise model.',
                'modal_analysis' : 'Enable/disable the modal analysis model.',
                'wave_equation' : 'Enable/disable the wave equation model.',
                'wave_equation_options' : 'Enter the options menu for the wave equation model.',
                'receivers' : 'Set acoustic receivers.',
                'export_source_data' : 'Enable export acoustic source data in ASD format during the wave equation model run.',
                'export_source_data_cgns' : 'Export acoustic source data in CGNS format.',
                'sources' : 'Set acoustic sources.',
                'read_compute_write' : 'Read acoustic source data files and compute sound pressure.',
                'sources_fft' : 'Enter the acoustic sources FFT menu.',
                'write_acoustic_signals' : 'Write on-the-fly sound pressure.',
                'compute_write' : 'Compute sound pressure.',
                'write_centroid_info' : 'Write centroid info.',
                'acoustic_modal_analysis' : 'Iterate linear acoustic solver to compute the resonance frequencies and the acoustic modes.',
                'export_volumetric_sources' : 'Enable/disable the export of fluid zones.',
                'export_volumetric_sources_cgns' : 'Enable/disable the export of fluid zones.',
                'display_flow_time' : 'Enable/disable the display of flow time during read-and-compute.',
                'cylindrical_export' : 'Enable/disable the export data in cylindrical coordinates.',
                'auto_prune' : 'Enable/disable auto prune of the receiver signal(s) during read-and-compute.',
                'moving_receiver' : 'Enable/disable moving receiver option.',
                'convective_effects' : 'Enable/disable convective effects option.',
                'display_frequencies' : 'Display resonance frequencies.',
                'sponge_layers' : 'Manage sponge layers where density is blended to eliminate reflections from boundary zones.',
            }
        class optics(metaclass=PyMenuMeta):
            """Enter the optics model menu."""
            doc_by_method = {
                'enable' : 'Enable/disable aero-optical model.',
                'add_beam' : 'Add optical beam grid.',
                'set' : 'Enter the set menu for aero-optical model.',
            }
        class eulerian_wallfilm(metaclass=PyMenuMeta):
            """Enter the Eulerian wall film model menu."""
            doc_by_method = {
                'enable_wallfilm_model' : 'Enable Eulerian wall film model',
                'initialize_wallfilm_model' : 'Initialize Eulerian wall film model',
                'solve_wallfilm_equation' : 'Activate Eulerian wall film equations',
                'model_options' : 'Set Eulerian wall film model options',
                'film_material' : 'Set film material and properties',
                'solution_options' : 'Set Eulerian wall film model solution options',
                'coupled_solution' : 'Enter Eulerian wall film coupled solution menu',
                'implicit_options' : 'Enter Implicit Scheme Option (beta)',
            }
        class dpm(metaclass=PyMenuMeta):
            """Enter the dispersed phase model menu."""
            doc_by_method = {
                'clear_particles_from_domain' : 'Remove/keep all particles currently in the domain.',
                'collisions' : 'Enter the DEM collisions menu.',
                'erosion_dynamic_mesh' : 'Enter the erosion-dynamic mesh interactions menu.',
                'fill_injection_material_sources' : 'Initialize the DPM sources corresponding to each material.',
                'injections' : 'Enter the injections menu.',
                'interaction' : 'Enter the interaction menu to set parameters for coupled discrete phase calculations.',
                'numerics' : 'Enter the numerics menu to set numerical solution parameters.',
                'options' : 'Enter the options menu to set optional DPM models.',
                'parallel' : 'Enter the parallel menu.',
                'unsteady_tracking' : 'Enable/disable unsteady particle tracking.',
                'splash_options' : 'Enter the splash options menu to set optional parameters.',
                'stripping_options' : 'Enter the stripping options menu to set optional parameters.',
                'spray_model' : 'Enter the spray model menu.',
                'user_defined' : 'Set DPM user-defined functions.',
            }
        class shell_conduction(metaclass=PyMenuMeta):
            """Enter the shell conduction model menu."""
            doc_by_method = {
                'multi_layer_shell' : 'Enable/disable multi layer shell conduction model.',
                'enhanced_encapsulation' : 'Enable/disable enhanced encapsulation for shell conduction and S2S models. This is not applicable if coupled sliding interface walls exists.',
                'read_csv' : 'Read shell conduction settings from a csv file',
                'write_csv' : 'Write shell conduction settings to a csv file',
                'settings' : 'Enter Multi-layer Shell Conduction data',
                'save_shell_zones' : 'Enable/Disable saving shell zones to case file.',
            }
        class system_coupling_settings(metaclass=PyMenuMeta):
            """Enter the system coupling model menu."""
            doc_by_method = {
                'htc' : 'Enter the heat transfer coeficient menu.',
                'use_face_or_element_based_data_transfer' : 'Enable/disable face based data transfer.',
                'update_rigid_body_mesh_motion_before_mesh_transfer' : 'SC Enable/disable mesh motion.',
                'specify_system_coupling_volumetric_cell_zones' : 'Enable/disable volumetric cell zones',
            }
        class cht(metaclass=PyMenuMeta):
            """Enter the mapped interface model menu."""
            doc_by_method = {
                'read_mi_type_wall' : 'Read mapped interface data settings from a csv file',
                'write_mi_type_wall' : 'Write mapped interface settings to a scv file',
                'implicit_coupling' : 'Enable/disable implicit coupling for mapped interface.',
                'explicit_time_averaged_coupling' : 'Enter the explcit time averaged thermal coupling menu.',
            }
        class two_temperature(metaclass=PyMenuMeta):
            """Define two-temperature model menu"""
            doc_by_method = {
                'enable' : 'Enable/disable the two-temperature model.',
                'robustness_enhancement' : 'Apply robustness enhancements in the two-temperature model.',
                'nasa9_enhancement' : 'Apply nasa9 robustness enhancements in the two-temperature model.',
                'set_verbosity' : 'set two-temperature model verbosity option',
            }
        class multiphase(metaclass=PyMenuMeta):
            """Define multiphase model menu"""
            doc_by_method = {
                'model' : 'Specify multiphase model.',
                'number_of_phases' : 'Specify the number of phases.',
                'phases' : 'Enter the phases menu.',
                'regime_transition_modeling' : 'regime-transition-modeling-options',
                'wet_steam' : 'Enter the wet steam model menu.',
                'eulerian_parameters' : 'Eulerian parameters.',
                'population_balance' : 'Enter the population balance model menu.',
                'volume_fraction_parameters' : 'Volume fraction parameters.',
                'boiling_model_options' : 'Boiling model options.',
                'mixture_parameters' : 'Mixture parameters.',
                'body_force_formulation' : 'Body force formulation.',
                'coupled_level_set' : 'Coupled level set.',
                'vof_sub_models' : 'VOF sub-models.',
                'interface_modeling_options' : 'Interface Modeling Options.',
                'expert_options' : 'Expert Options.',
                'explicit_expert_options' : 'Expert options for explicit formulation.',
            }
        class nox_parameters(metaclass=PyMenuMeta):
            """Enter the NOx parameters menu."""
            doc_by_method = {
                'nox_chemistry' : 'Select NOx chemistry model.',
                'nox_turbulence_interaction' : 'Set NOx-turbulence interaction model.',
                'inlet_diffusion' : 'Enable/disable inclusion of diffusion at inlets.',
                'nox_expert' : 'Select additional nox equations.',
            }
        class soot_parameters(metaclass=PyMenuMeta):
            """Enter the soot parameters menu."""
            doc_by_method = {
                'soot_model_parameters' : 'Enter the soot model parameters menu.',
                'soot_process_parameters' : 'Set soot process parameters.',
                'soot_radiation_interaction' : 'Enable/disable the soot-radiation interaction model.',
                'soot_turbulence_interaction' : 'Set Soot-turbulence interaction model.',
                'modify_schmidt_number' : 'Change Turbulent Schmidt Number for Soot/Nuclei Equations',
                'inlet_diffusion' : 'Enable/disable inclusion of diffusion at inlets.',
                'soot_model_udfs' : 'User defined functions for soot model',
            }
        class radiation(metaclass=PyMenuMeta):
            """Enter the radiation models menu."""
            doc_by_method = {
                'discrete_ordinates' : 'Enable/disable the discrete ordinates radiation model.',
                'do_acceleration' : 'Enable/disable acceleration of computation of DO model',
                'non_gray_model_parameters' : 'Set parameters for non-gray model.',
                'montecarlo' : 'Enable/disable the Monte Carlo radiation model.',
                'target_cells_per_volume_cluster' : 'Enter cells per volume cluster for Monte Carlo radiation model.',
                's2s' : 'Enable/disable the S2S radiation model.',
                's2s_parameters' : 'Enter the S2S parameters menu.',
                'discrete_transfer' : 'Enable/disable discrete the transfer radiation model.',
                'dtrm_parameters' : 'Enter the DTRM parameters menu.',
                'p1' : 'Enable/disable the P1 radiation model.',
                'radiation_model_parameters' : 'Set parameters for radiation models.',
                'radiation_iteration_parameters' : 'Set iteration parameters for radiation models.',
                'mc_model_parameters' : 'Set parameters for montecarlo radiation model.',
                'mc_under_relaxation' : 'Set under-relaxation factor for montecarlo radiation sources used in the energy equation.',
                'rosseland' : 'Enable/disable the Rosseland radiation model.',
                'solar' : 'Enable/disable the solar model.',
                'solar_irradiation' : 'Enable/disable the Solar irradiation model.',
                'solar_calculator' : 'Calculate sun direction and intensity.',
                'apply_full_solar_irradiation' : 'Enable/disable application of solar irradiation to first band with DO model.',
                'solar_parameters' : 'Enter the solar parameters menu.',
                'wsggm_cell_based' : 'Enable/disable WSGGM cell based method.',
                'fast_second_order_discrete_ordinate' : 'Enable/disable the fast-second-order option for Discrete Ordinate Model.',
                'do_coupling' : 'Enabled DO Energy Coupling.',
                'solution_method_for_do_coupling' : 'Enable the solution method for DO/Energy  Coupling.',
                'beta_radiation_features' : 'Enable Radiation Models with Non-Iterative Time Advancement (NITA) as Beta features in FL12.0',
                'method_partially_specular_wall' : 'Set method for partially specular wall with discrete ordinate model.',
                'blending_factor' : 'Set numeric option for Discrete Ordinate model.',
            }
        class solver(metaclass=PyMenuMeta):
            """Enter the menu to select the solver."""
            doc_by_method = {
                'pressure_based' : 'Enable/disable the segregated solver.',
                'density_based_explicit' : 'Enable/disable the coupled-explicit solver.',
                'density_based_implicit' : 'Enable/disable the coupled-implicit solver.',
                'adjust_solver_defaults_based_on_setup' : 'Enable/disable adjustment of solver defaults based on setup.',
            }
        class species(metaclass=PyMenuMeta):
            """Enter the species models menu."""
            doc_by_method = {
                'off' : 'Enable/disable solution of species models.',
                'species_transport' : 'Enable/disable the species transport model.',
                'non_premixed_combustion' : 'Enable/disable the non-premixed combustion model.',
                'premixed_combustion' : 'Enable/disable the premixed combustion model.',
                'partially_premixed_combustion' : 'Enable/disable partially premixed combustion model.',
                'premixed_model' : 'Set premixed combustion model.',
                'pdf_transport' : 'Enable/disable the composition PDF transport combustion model.',
                'save_gradients' : 'Enable/disable storage of species mass fraction gradients.',
                'liquid_energy_diffusion' : 'Enable/disable energy diffusion for liquid regime.',
                'volumetric_reactions' : 'Enable/disable volumetric reactions.',
                'species_transport_expert' : 'Set species transport expert options',
                'coal_calculator' : 'Set up coal modeling inputs.',
                'mixing_model' : 'Set PDF transport mixing model.',
                'stiff_chemistry' : 'Enable/disable stiff chemistry option.',
                'liquid_micro_mixing' : 'Enable/disable liquid micro mixing option.',
                'epdf_energy' : 'Enable/disable EPDF energy  option.',
                'integration_parameters' : 'Set ISAT parameters.',
                'clear_isat_table' : 'Clear the ISAT table.',
                'pdf_transport_expert' : 'Enable/disable PDF transport expert user.',
                'CHEMKIN_CFD_parameters' : 'Enter the expert CHEMKIN-CFD parameters menu.',
                'set_turb_chem_interaction' : 'Set Eddy-Dissipation Concept model constants.',
                'spark_model' : 'Set spark model parameters.',
                'ignition_model' : 'Enable/disable the ignition model.',
                'ignition_model_controls' : 'Set ignition model parameters.',
                'inert_transport_model' : 'Enable/disable the inert transport model.',
                'inert_transport_controls' : 'Set inert transport model parameters.',
                'particle_surface_reactions' : 'Enable/disable particle surface reactions.',
                'wall_surface_reactions' : 'Enable/disable wall surface reactions.',
                'heat_of_surface_reactions' : 'Enable/disable heat of surface reactions.',
                'mass_deposition_source' : 'Enable/disable mass deposition source due to surface reactions.',
                'electro_chemical_surface_reactions' : 'Enable/disable electrochemical surface reactions.',
                'species_migration' : 'Enable/disable ion species migration in electric field.',
                'reaction_diffusion_balance' : 'Enable/disable reaction diffusion balance at reacting surface for surface reactions.',
                'surf_reaction_aggressiveness_factor' : 'Set the surface reaction aggressiveness factor.',
                'surf_reaction_netm_params' : 'Set the surface reaction parameters for the Non-Equilibrium Thermal Model.',
                'inlet_diffusion' : 'Enable/disable inclusion of diffusion at inlets.',
                'diffusion_energy_source' : 'Enable/disable diffusion energy source.',
                'multicomponent_diffusion' : 'Enable/disable multicomponent diffusion.',
                'thermal_diffusion' : 'Enable/disable thermal diffusion.',
                'CHEMKIN_CFD' : 'Enable/disable CHEMKIN-CFD.',
                'non_premixed_combustion_parameters' : 'Set PDF parameters.',
                'partially_premixed_combustion_parameters' : 'Set PDF parameters.',
                'partially_premixed_properties' : 'Set/Change partially premixed mixture properties.',
                're_calc_par_premix_props' : 'Re-calculate partially-premixed properties.',
                'full_tabulation' : 'Enable/disable building of a full 2 mixture fraction table',
                'init_unsteady_flamelet_prob' : 'Initialize Unsteady Flamelet Probability.',
                'import_flamelet_for_restart' : 'Import Flamelet File for Restart.',
                'non_premixed_combustion_expert' : 'Set PDF expert parameters.',
                'partially_premixed_combustion_expert' : 'Set PDF expert parameters.',
                'partially_premixed_combustion_grids' : 'Set user specified grid parameters for PDF and flamelet.',
                'flamelet_expert' : 'Set flamelet expert parameters.',
                'combustion_expert' : 'Set combustion expert parameters.',
                'set_premixed_combustion' : 'Set premixed combustion parameters.',
                'set_multi_regime_fgm' : 'set-multi-regim-fgm-parameters',
                'relax_to_equil' : 'Enable/disable the Relaxation to Chemical Equilibrium model',
                'thickened_flame_model' : 'Enable/disable the Relaxation to Chemical Equilibrium model',
                'decoupled_detailed_chemistry' : 'Enable/disable the Decoupled Detailed Chemistry model',
                'reactor_network_model' : 'Enable/disable the Reactor Network model',
                'reacting_channel_model' : 'Enable/Disable the Reacting Channel Model',
                'reacting_channel_model_options' : 'Set Reacting Channel Model parameters.',
                'combustion_numerics' : 'set combustion numerics options',
            }
        class viscous(metaclass=PyMenuMeta):
            """Enter the viscous model menu."""
            doc_by_method = {
                'inviscid' : 'Enable/disable the inviscid flow model.',
                'laminar' : 'Enable/disable the laminar flow model.',
                'mixing_length' : 'Enable/disable the mixing-length (algebraic) turbulence model.',
                'zero_equation_hvac' : 'Enable/disable the zero-equation HVAC turbulence model.',
                'spalart_allmaras' : 'Enable/disable the Spalart-Allmaras turbulence model.',
                'ke1e' : 'Enable/disable the KE1E turbulence model.',
                'sa_enhanced_wall_treatment' : 'Enable/disable the enhanced wall treatment for the Spalart-Allmaras model.
If disabled, no smooth blending between the viscous sublayer and the
log-law formulation is employed, as was done in versions previous to Fluent14.',
                'sa_alternate_prod' : 'Enable/disable strain/vorticity production in Spalart-Allmaras model.',
                'sa_damping' : 'Enable/disable the full low-Reynolds number form of Spalart-Allmaras model.',
                'ke_standard' : 'Enable/disable the standard k-epsilon turbulence model.',
                'ke_easm' : 'Enable/disable the EASM k-epsilon turbulence model.',
                'ke_realizable' : 'Enable/disable the realizable k-epsilon turbulence model.',
                'ke_rng' : 'Enable/disable the RNG k-epsilon turbulence model.',
                'rng_differential_visc' : 'Enable/disable the differential-viscosity model.',
                'rng_swirl_model' : 'Enable/disable swirl corrections for rng-model.',
                'kw_standard' : 'Enable/disable the standard k-omega turbulence model.',
                'kw_easm' : 'Enable/disable the EASM k-omega turbulence model.',
                'kw_bsl' : 'Enable/disable the BSL k-omega turbulence model.',
                'kw_geko' : 'Enable/disable the GEKO turbulence model.',
                'kw_sst' : 'Enable/disable the SST k-omega turbulence model.',
                'kw_wj_bsl_earsm' : 'Enable/disable the EASM k-omega turbulence model.',
                'kw_low_re_correction' : 'Enable/disable the k-omega low Re option.',
                'kw_shear_correction' : 'Enable/disable the k-omega shear-flow correction option.',
                'turb_compressibility' : 'Enable/disable the compressibility correction option.',
                'k_kl_w' : 'Enable/disable the k-kl-omega turbulence model.',
                'transition_sst' : 'Enable/disable the transition SST turbulence model.',
                'v2f' : 'Enable/disable the V2F turbulence model.',
                'reynolds_stress_model' : 'Enable/disable the RSM turbulence model.',
                'rsm_solve_tke' : 'Enable/disable the solution of T.K.E. in RSM model.',
                'rsm_wall_echo' : 'Enable/disable wall-echo effects in RSM model.',
                'rsm_linear_pressure_strain' : 'Enable/disable the linear pressure-strain model in RSM.',
                'rsm_ssg_pressure_strain' : 'Enable/disable the quadratic pressure-strain model in RSM.',
                'rsm_omega_based' : 'Enable/disable the Stress-omega model.',
                'rsm_bsl_based' : 'Enable/disable the Stress-BSL model.',
                'sas' : 'Enable/disable the SAS turbulence model.',
                'detached_eddy_simulation' : 'Enable/disable detached eddy simulation.',
                'des_limiter_option' : 'Select DES limiter option.',
                'large_eddy_simulation' : 'Enable/disable large eddy simulation.',
                'les_subgrid_smagorinsky' : 'Enable/disable the Smagorinsky-Lilly subgrid-scale model.',
                'les_dynamic_energy_flux' : 'Enable/disable the dynamic sub-grid scale turbulent Prandtl Number.',
                'les_dynamic_scalar_flux' : 'Enable/disable the dynamic sub-grid scale turbulent Schmidt Number.',
                'les_subgrid_dynamic_fvar' : 'Enable/disable the dynamic subgrid-scale mixture fraction variance model.',
                'les_subgrid_rng' : 'Enable/disable the RNG subgrid-scale model.',
                'les_subgrid_wale' : 'Enable/disable the WALE subgrid-scale model.',
                'les_subgrid_wmles' : 'Enable/disable the WMLES subgrid-scale model.',
                'les_subgrid_wmles_s_minus_omega' : 'Enable/disable the WMLES S-Omega subgrid-scale model.',
                'les_subgrid_tke' : 'Enable/disable the kinetic energy transport subgrid-scale model.',
                'turb_buoyancy_effects' : 'Select buoyancy effects on turbulence.',
                'curvature_correction' : 'Enable/disable the curvature correction.',
                'curvature_correction_ccurv' : 'Set the curvature correction coefficient CCURV.',
                'corner_flow_correction' : 'Enable/disable the corner flow correction.',
                'corner_flow_correction_ccorner' : 'Set the corner flow correction coefficient CCORNER.',
                'rsm_or_earsm_geko_option' : 'Enable/disable the GEKO option for RSM or EARSM.',
                'add_transition_model' : 'Enable/disable a transition model to account for transitional effects.',
                'user_defined' : 'Select user-defined functions to define the turbulent viscosity and the turbulent Prandtl and Schmidt numbers.',
                'user_defined_transition' : 'Set user-defined transition correlations.',
                'trans_sst_roughness_correlation' : 'Enable/disable the Transition-SST roughness correlation option.',
                'near_wall_treatment' : 'Enter the near wall treatment menu.',
                'multiphase_turbulence' : 'Enter the multiphase turbulence menu.',
                'turbulence_expert' : 'Enter the turbulence expert menu.',
                'geko_options' : 'Enter the GEKO options menu.',
                'transition_model_options' : 'Enter the transition model options menu.',
            }
        class structure(metaclass=PyMenuMeta):
            """Enter the structure model menu."""
            doc_by_method = {
                'structure_off' : 'Disable the structural model.',
                'linear_elasticity' : 'Enable the linear elasticity model.',
                'nonlinear_elasticity' : 'Enable the nonlinear elasticity model.',
                'thermal_effects' : 'Enable structure thermal effects.',
                'controls' : 'Enter the structure controls menu.',
                'expert' : 'Enter the structure expert menu.',
            }
        class heat_exchanger(metaclass=PyMenuMeta):
            """Enter the heat exchanger menu."""
            doc_by_method = {
                'macro_model' : 'Enter the heat macro-model menu.',
                'dual_cell_model' : 'Enter the dual cell model menu.',
            }
    class named_expressions(metaclass=PyMenuMeta):
        """Manage named expressions"""
        doc_by_method = {
            'add' : 'Add a new object',
            'compute' : 'Compute expression',
            'copy' : 'Copy expression',
            'edit' : 'Edit an object',
            'delete' : 'Delete an object',
            'export_to_tsv' : 'Export expressions',
            'import_from_tsv' : 'Export expressions',
            'list' : 'List objects',
            'list_properties' : 'List properties of an object',
        }
    class operating_conditions(metaclass=PyMenuMeta):
        """Enter the define operating conditions menu."""
        doc_by_method = {
            'gravity' : 'Set gravitational acceleration.',
            'gravity_mrf_rotation' : 'Enable/disable rotation of gravity vector in moving reference frame simulations.',
            'set_state' : 'Select state for real gas EOS subcritical condition.',
            'operating_pressure' : 'Set the operating pressure.',
            'reference_pressure_location' : 'Set coordinates of reference pressure.',
            'reference_pressure_method' : 'Choosing reference pressure type.',
            'used_ref_pressure_location' : 'See the actual coordinates of reference pressure used.',
            'operating_density' : 'Enable/disable use of a specified operating density.',
            'use_inlet_temperature_for_operating_density' : 'Use Inlet Temperature to calculate Opearating Density',
            'operating_temperature' : 'Set the operating temperature for Boussinesq.',
        }
    class overset_interfaces(metaclass=PyMenuMeta):
        """Enter the overset-interfaces menu."""
        doc_by_method = {
            'create' : 'Create an overset interface.',
            'delete' : 'Delete an overset interface.',
            'delete_all' : 'Delete all overset interfaces.',
            'intersect' : 'Intersect an overset interface.',
            'intersect_all' : 'Intersect all overset interfaces.',
            'clear' : 'Clear an overset interface.',
            'clear_all' : 'Clear all overset interfaces.',
            'grid_priorities' : 'Edit grid priorities for an overset interface.',
            'list' : 'List all overset interfaces.',
            'mark_cells' : 'Mark overset interface related cell types.',
            'display_cells' : 'Display the marked overset cells.',
            'mark_cell_change' : 'Mark overset interface related cell type change.',
            'set_mark_bounds' : 'Set bounds (center, radius) for overset cell marking.',
            'check' : 'Check all overset interfaces.',
            'debug_hole_cut' : 'Debugging tool for overset hole cutting.',
            'fill_dci' : 'Fill overset domain connectivity information (DCI).',
            'free_dci' : 'Free overset domain connectivity information (DCI).',
            'update_from_dci' : 'Update all overset intrfaces from stored domain connectivity information (DCI).',
            'write_dci_to_case' : 'Save domain connectivity information (DCI) to case file.',
            'read_dci_from_case' : 'Read domain connectivity information (DCI) from case file.',
            'write_dci' : 'Save domain connectivity information (DCI) to a text file.',
            'write_cell_types' : 'Write overset cell types into file.',
            'find_bounding_cell' : 'Find bounding cell for given cell or search point.',
            'find_all_bounding_cells' : 'Find bounding cells for all cell centroids.',
        }
        class options(metaclass=PyMenuMeta):
            """Enter the overset interface options menu."""
            doc_by_method = {
                'expert' : 'Enable additional overset options and tools.',
                'render_receptor_cells' : 'Set the option to include receptor cells in postprocessing.',
                'partial_cut_faces' : 'Enable enhanced hole cutting where cut faces partially overlap.',
                'auto_create' : 'Enable automatic creation of default overset interface.',
                'minimize_overlap' : 'Enable overlap minimization for overset interfaces.',
                'overlap_boundaries' : 'Enable overset topologies with overlap boundaries.',
                'mesh_interfaces' : 'Allow mesh interfaces inside overset cell zones.',
                'node_connected_donors' : 'Enable node or face connected donor cells.',
                'donor_priority_method' : 'Set method used to evaludate the cell donor priority.',
                'solve_island_removal' : 'Set method used to control the removal of isolated patches of solve cells.',
                'transient_caching' : 'Set options to control caching of entities in transient overset simulations.',
                'modified_donor_search' : 'Enable modified and more extensive donor search.',
                'modified_hole_cutting' : 'Enable modified hole cutting parameters.',
                'dead_cell_update' : 'Enable dead cell update in moving or dynamic mesh simulations.',
                'update_before_case_write' : 'Enable update of overset interfaces before writing case file (CFF format only).',
                'parallel' : 'Set options to control running overset in parallel.',
                'verbosity' : 'Set overset mesh reporting verbosity.',
            }
        class cut_control(metaclass=PyMenuMeta):
            """Enter the overset hole cut control menu."""
            doc_by_method = {
                'add' : 'Add hole cut control for a boundary zone.',
                'delete' : 'Delete hole cut control for a boundary zone.',
                'delete_all' : 'Delete the hole cut controls for all boundary zones.',
                'list' : 'List the defined hole cut controls.',
                'cut_seeds' : 'Enter the overset hole cut seed menu.',
            }
        class adapt(metaclass=PyMenuMeta):
            """Enter the overset adaption menu."""
            doc_by_method = {
                'mark_adaption' : 'Mark cells for overset orphan adaption and donor-receptor size differences.',
                'adapt_mesh' : 'Mark and adapt the mesh to remove orphan cells and large donor-receptor cell size differences.',
                'set' : 'Enter the overset adaption set menu.',
            }
    class reference_frames(metaclass=PyMenuMeta):
        """Manage reference frames"""
        doc_by_method = {
            'add' : 'Add a new object',
            'display' : 'Display Reference Frame',
            'display_edit' : 'display and edit reference frame from graphics',
            'edit' : 'Edit an object',
            'delete' : 'Delete an object',
            'hide' : 'Hide Reference Frame',
            'list' : 'List objects',
            'list_properties' : 'List properties of an object',
        }
    class reference_values(metaclass=PyMenuMeta):
        """Reference value menu."""
        doc_by_method = {
            'area' : 'Set reference area for normalization.',
            'depth' : 'Set reference depth for volume calculation.',
            'density' : 'Set reference density for normalization.',
            'enthalpy' : 'Set reference enthalpy for enthalpy damping and normalization.',
            'length' : 'Set reference length for normalization.',
            'pressure' : 'Set reference pressure for normalization.',
            'temperature' : 'Set reference temperature for normalization.',
            'yplus' : 'Set reference yplus for normalization.',
            'velocity' : 'Set reference velocity for normalization.',
            'viscosity' : 'Set reference viscosity for normalization.',
            'zone' : 'Set reference zone.',
            'list' : 'List current reference values.',
        }
        class compute(metaclass=PyMenuMeta):
            """Enter the compute menu."""
            doc_by_method = {
                'axis' : 'Compute reference values from a zone of this type.',
                'degassing' : 'Compute reference values from a zone of this type.',
                'dummy_entry' : '',
                'exhaust_fan' : 'Compute reference values from a zone of this type.',
                'fan' : 'Compute reference values from a zone of this type.',
                'fluid' : 'Compute reference values from a zone of this type.',
                'inlet_vent' : 'Compute reference values from a zone of this type.',
                'intake_fan' : 'Compute reference values from a zone of this type.',
                'interface' : 'Compute reference values from a zone of this type.',
                'interior' : 'Compute reference values from a zone of this type.',
                'mass_flow_inlet' : 'Compute reference values from a zone of this type.',
                'mass_flow_outlet' : 'Compute reference values from a zone of this type.',
                'network' : 'Compute reference values from a zone of this type.',
                'network_end' : 'Compute reference values from a zone of this type.',
                'outflow' : 'Compute reference values from a zone of this type.',
                'outlet_vent' : 'Compute reference values from a zone of this type.',
                'overset' : 'Compute reference values from a zone of this type.',
                'periodic' : 'Compute reference values from a zone of this type.',
                'porous_jump' : 'Compute reference values from a zone of this type.',
                'pressure_far_field' : 'Compute reference values from a zone of this type.',
                'pressure_inlet' : 'Compute reference values from a zone of this type.',
                'pressure_outlet' : 'Compute reference values from a zone of this type.',
                'radiator' : 'Compute reference values from a zone of this type.',
                'rans_les_interface' : 'Compute reference values from a zone of this type.',
                'recirculation_inlet' : 'Compute reference values from a zone of this type.',
                'recirculation_outlet' : 'Compute reference values from a zone of this type.',
                'shadow' : 'Compute reference values from a zone of this type.',
                'solid' : 'Compute reference values from a zone of this type.',
                'symmetry' : 'Compute reference values from a zone of this type.',
                'velocity_inlet' : 'Compute reference values from a zone of this type.',
                'wall' : 'Compute reference values from a zone of this type.',
            }
    class turbo_model(metaclass=PyMenuMeta):
        """Turbo features menu."""
        doc_by_method = {
            'enable_turbo_model' : 'Enable/disable turbo model menu.',
            'separate_nonoverlapping_interface_boundary' : 'Split a general turbo interface non-overlapping zone',
            'turbo_create' : 'Create a general turbo interface.',
            'number_of_blades_in_row' : 'Define the total number of blades in blade flutter row',
            'define_turbomachine_description' : 'Define turbomachine description',
            'define_phaselag_spectral_content' : 'Define phaselag related spectral content',
            'phaselag_extra_settings' : 'Define phaselag related extra settings',
            'define_post_spectral_content' : 'Define post-processing related spectral content',
            'post_extra_settings' : 'Define phaselag related extra settings',
            'delete_turbomachine_description' : 'Delete turbomachine description',
            'delete_phaselag_spectral_content' : 'Delete phaselag related spectral content',
            'delete_post_spectral_content' : 'Delete post-processing related spectral content',
            'list_turbomachine_description' : 'List turbomachine description',
            'list_post_spectral_content' : 'List post-processing related spectral content',
            'list_phaselag_state' : 'List all phaselag related case settings',
            'make_phaselag_from_boundaries' : 'Make interface zones phase lagged.',
            'make_phaselag_from_periodic' : 'Convert periodic interface to phase lagged.',
        }
        class turbo_topology(metaclass=PyMenuMeta):
            """Define turbo topology."""
            doc_by_method = {
                'define_topology' : 'Define a turbo topology.',
                'mesh_method' : 'Set turbo structured mesh generation method.',
                'search_method' : 'Set search method for a topology.',
                'projection_method' : 'Set 2D projection method.',
                'delete' : 'Delete a turbo topology.',
            }
        class general_turbo_interface_settings(metaclass=PyMenuMeta):
            """Set General Turbo Interface options"""
            doc_by_method = {
                'mixing_plane_model_settings' : 'Set the mixing plane model settings',
                'pitch_scale_model_settings' : 'Set the pitch scale model settings',
                'no_pitch_scale_model_settings' : 'Set the no pitch scale model settings',
                'expert' : 'Set the expert parameters for turbo interfaces',
            }
        class blade_flutter_harmonics(metaclass=PyMenuMeta):
            """Enter the blade flutter harmonics menu."""
            doc_by_method = {
                'enable_harmonic_postprocessing' : 'Calculates/Deletes Postprocessing Fourier coefficients data',
                'enable_harmonic_exports' : 'Calculates/Deletes flutter harmonic export data',
                'write_harmonic_exports' : 'Writes harmonic export data',
            }
class simulation_reports(metaclass=PyMenuMeta):
    """Enter the simulation reports menu."""
    doc_by_method = {
        'list_simulation_reports' : 'List all report names.',
        'generate_simulation_report' : 'Generate a new simulation report or regenerate an existing simulation report with the provided name.',
        'view_simulation_report' : 'View a simulation report that has already been generated. In batch mode this will print the report's URL.',
        'export_simulation_report_as_pdf' : 'Export the provided simulation report as a PDF file.',
        'export_simulation_report_as_html' : 'Export the provided simulation report as HTML.',
        'write_report_names_to_file' : 'Write the list of currently generated report names to a txt file.',
        'rename_simulation_report' : 'Rename a report which has already been generated.',
        'duplicate_simulation_report' : 'Duplicate a report and all of its settings to a new report.',
        'reset_report_to_defaults' : 'Reset all report settings to default for the provided simulation report.',
        'delete_simulation_report' : 'Delete the provided simulation report.',
        'write_simulation_report_template_file' : 'Write a JSON template file with this case's Simulation Report settings.',
        'read_simulation_report_template_file' : 'Read a JSON template file with existing Simulation Report settings.',
    }
class server(metaclass=PyMenuMeta):
    """Enter the server menu."""
    doc_by_method = {
        'start_server' : 'Start server.',
        'start_client' : 'Start client.',
        'print_server_address' : 'Print server address.',
        'write_or_reset_server_info' : 'Write/Reset server info.',
        'print_connected_clients' : 'Print connected clients.',
        'shutdown_server' : 'Shutdown server.',
    }
class turbo_post(metaclass=PyMenuMeta):
    """Enter the turbo menu."""
    doc_by_method = {
        'compute_report' : 'Compute the turbo report.',
        'write_report' : 'Write the turbo report to file.',
        'avg_contours' : 'Display average contours.',
        'two_d_contours' : 'Display 2d contours.',
        'xy_plot_avg' : 'Display average xy plot.',
        'current_topology' : 'Set the current turbo topology for global use.',
    }
class parametric_study(metaclass=PyMenuMeta):
    """Enter the parametric study menu"""
    doc_by_method = {
        'initialize' : 'Start Parametric Study',
        'duplicate_study' : 'Duplicate Parametric Study',
        'export_design_table' : 'Enter the design table menu',
    }
    class design_points(metaclass=PyMenuMeta):
        """Enter the design points menu"""
        doc_by_method = {
            'add_design_point' : 'Add new design point',
            'get_current_design_point' : 'Get Name of Current Design Point',
            'load_case_data_for_current_dp' : 'Loads relevant case/data file for current design point',
            'set_as_current' : 'Set current design point',
            'get_input_parameters_of_dp' : 'Get Input Parameter Values of Current Design Point',
            'set_input_parameters_of_dp' : 'Set Input Parameter Values of Design Point',
            'get_output_parameters_of_dp' : 'Get Output Parameter Values of Design Point',
            'set_write_data' : 'Set WriteData option for Design Point',
            'get_write_data' : 'Get WriteData option for Design Point',
            'set_capture_simulation_report_data' : 'Set Capture Simulation Report Data option for Design Point',
            'get_capture_simulation_report_data' : 'Get Capture Simulation Report Data option for Design Point',
            'delete_design_point' : 'Delete Design Point',
            'duplicate_design_point' : 'Duplicate Design Point',
            'clear_generated_data' : 'Clear Generated Data',
        }
    class update(metaclass=PyMenuMeta):
        """Enter the update menu"""
        doc_by_method = {
            'set_update_method' : 'Set update method',
            'get_update_method' : 'Get update method',
            'update_current' : 'Update Current Design Point',
            'update_all' : 'Update All Design Points',
            'update_selected_design_points' : 'Update Selected Design Points',
            'get_number_of_concurrent_dps' : 'Get Number of Concurrent Design Points',
            'set_number_of_concurrent_dps' : 'Set Number of Concurrent Design Points',
        }
class turbo_workflow(metaclass=PyMenuMeta):
    """Enter the turbo workflow menu"""
    class workflow(metaclass=PyMenuMeta):
        """Enter the workflow menu"""
        doc_by_method = {
            'enable' : 'Enable the workflow',
            'reset' : 'Reset the workflow',
            'disable' : 'Disable the workflow',
        }
