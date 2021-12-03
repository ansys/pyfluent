# This is an auto-generated file.  DO NOT EDIT!

from ansys.fluent.solver.meta import PyMenuMeta, PyNamedObjectMeta


doc_by_method = {
    'close_fluent' : 'Exit program.',
    'exit' : 'Exit program.',
    'switch_to_meshing_mode' : 'Switch to meshing mode.',
    'print_license_usage' : 'Print license usage information',
}

class adjoint(metaclass=PyMenuMeta):
    __doc__ = 'Adjoint.'
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
    __doc__ = 'Enter the file menu.'
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
        'read_case' : 'Read a case file.\nArguments:\n  case_file_name: str\n',
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
        __doc__ = 'Enter the auto save menu.'
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
        __doc__ = 'CFF I/O options'
        doc_by_method = {
            'io_mode' : 'Set CFF I/O mode.',
            'compression_level' : 'Set CFF file compression level.',
            'single_precision_data' : 'Specify whether the double-precision solver saves single-precision data when writing CFF data files.',
        }

    class export(metaclass=PyMenuMeta):
        __doc__ = 'Enter the export menu.'
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
            __doc__ = 'file menu'
            doc_by_method = {
                'enable_automatic_creation_of_scp_file' : 'Enable/disable automatic creation of scp file during case write',
                'write_system_coupling_file' : 'Write a Fluent Input File for System Coupling',
            }

        class settings(metaclass=PyMenuMeta):
            __doc__ = 'Enter the export settings menu'
            doc_by_method = {
                'set_cgns_export_filetype' : 'Select HDF5 or ADF as file format for CGNS',
            }

    class transient_export(metaclass=PyMenuMeta):
        __doc__ = 'Enter the export menu.'
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
            __doc__ = 'Enter the automatic export settings menu'
            doc_by_method = {
                'cfd_post_compatible' : 'Set settings for CFD-Post compatible file export',
            }

    class em_mapping(metaclass=PyMenuMeta):
        __doc__ = 'Assign electro-magnetic losses provided by specified product.'
        doc_by_method = {
            'volumetric_energy_source' : 'Loss data provided by Ansoft will be assigned to Fluent for selected cell zones',
            'surface_energy_source' : 'Loss data provided by Ansoft will be assigned to Fluent for selected wall zones',
            'remove_loss_only' : 'Remove the loss data provided by Ansoft and keep all other solution data.',
            'maintain_loss_on_initialization' : 'Maintain the loss data provided by Ansoft even if solution is initialized',
        }

    class import_(metaclass=PyMenuMeta):
        __doc__ = 'Enter the import menu.'
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
            __doc__ = 'Enter the Mechanical APDL menu.'
            doc_by_method = {
                'input' : 'Read an Mechanical APDL file as a case file.',
                'result' : 'Read an Mechanical APDL result file as a case file.',
            }

        class abaqus(metaclass=PyMenuMeta):
            __doc__ = 'Enter the Abaqus menu.'
            doc_by_method = {
                'fil' : 'Read an Abaqus .fil result file as a case file.',
                'input' : 'Read an Abaqus Input file as a case file.',
                'odb' : 'Read an Abaqus odb file as a case file.',
            }

        class cfx(metaclass=PyMenuMeta):
            __doc__ = 'Enter the CFX menu.'
            doc_by_method = {
                'definition' : 'Read a CFX definition file as a case file.',
                'result' : 'Read a CFX result file as a case file.',
            }

        class cgns(metaclass=PyMenuMeta):
            __doc__ = 'Enter the CGNS menu.'
            doc_by_method = {
                'mesh' : 'Read a CGNS file as a case file.',
                'data' : 'Read data from CGNS file.',
                'mesh_data' : 'Read a CGNS file as a case file.',
            }

        class fmu_file(metaclass=PyMenuMeta):
            __doc__ = 'Read a FMU file.'
            doc_by_method = {
                'import_fmu' : 'Import a FMU file.',
                'define_fmu' : 'Link the FMU variables with Fluent parameters.',
                'select_fmu_local' : 'Select the FMU local variables to monitor.',
                'set_fmu_parameter' : 'Change the values of FMU parameter variables.',
            }

        class flamelet(metaclass=PyMenuMeta):
            __doc__ = 'Import a flamelet file.'
            doc_by_method = {
                'standard' : 'Read a standard format flamelet file.',
                'cfx_rif' : 'Read a CFX-RIF format flamelet file.',
            }

        class lstc(metaclass=PyMenuMeta):
            __doc__ = 'Enter the LSTC menu.'
            doc_by_method = {
                'input' : 'Read an LSTC input file as a case file.',
                'state' : 'Read an LSTC result file as a case file.',
            }

        class nastran(metaclass=PyMenuMeta):
            __doc__ = 'Enter the NASTRAN menu.'
            doc_by_method = {
                'bulkdata' : 'Read a NASTRAN file as a case file.',
                'output2' : 'Read a NASTRAN op2 file as a case file.',
            }

        class partition(metaclass=PyMenuMeta):
            __doc__ = 'Enter the partition menu.'
            doc_by_method = {
                'metis' : 'Read and partition a Fluent 5 case file.',
                'metis_zone' : 'Read and partition a Fluent 5 case file.',
            }

        class patran(metaclass=PyMenuMeta):
            __doc__ = 'Enter the PATRAN menu.'
            doc_by_method = {
                'neutral' : 'Read a PATRAN Neutral file (zones defined by named components) as a case file.',
            }

        class plot3d(metaclass=PyMenuMeta):
            __doc__ = 'Enter the PLOT3D menu.'
            doc_by_method = {
                'mesh' : 'Read a PLOT3D file as a case file.',
            }

        class tecplot(metaclass=PyMenuMeta):
            __doc__ = 'Enter the Tecplot menu.'
            doc_by_method = {
                'mesh' : 'Read a Tecplot binary file as a case file.',
            }

    class interpolate(metaclass=PyMenuMeta):
        __doc__ = 'Enter the interpolate menu.'
        doc_by_method = {
            'write_data' : 'Write data for interpolation.',
            'read_data' : 'Read and interpolate data.',
            'zone_selection' : 'Define a list of cell zone IDs. If specified, interpolation data will be\n                read/written for these cell zones only.',
        }

    class fsi(metaclass=PyMenuMeta):
        __doc__ = 'Enter the fsi menu.'
        doc_by_method = {
            'read_fsi_mesh' : 'Read an FEA mesh for one-way FSI.',
            'display_fsi_mesh' : 'Display the FEA mesh that has been read.',
            'write_fsi_mesh' : 'Write an FEA mesh file with Fluent data.',
            'conserve_force' : 'Conserve the forces for linear line, tri and tet elements',
        }

    class parametric_project(metaclass=PyMenuMeta):
        __doc__ = 'Enter to create new project, read project, and save project'
        doc_by_method = {
            'new' : 'Create New Project',
            'open' : 'Open project',
            'save' : 'Save Project',
            'save_as' : 'Save As Project',
            'save_as_copy' : 'Save As Copy',
            'archive' : 'Archive Project',
        }

    class table_manager(metaclass=PyMenuMeta):
        __doc__ = 'Enter the table manager menu.'
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
        __doc__ = 'enter the solution files menu'
        doc_by_method = {
            'print_solution_files' : 'Print list of available solution files.',
            'load_solution' : 'Load a solution file.',
            'delete_solution' : 'Delete solution files.',
        }

class icing(metaclass=PyMenuMeta):
    __doc__ = 'FENSAP-ICE options'
    doc_by_method = {
        'file' : 'File menu.',
        'flow' : 'Flow solver menu.',
        'drop' : 'Droplet impingement menu.',
        'ice' : 'Ice accretion menu.',
        'multishot' : 'Multi-shot accretion menu.',
        'settings' : 'Global settings menu.',
    }

class mesh(metaclass=PyMenuMeta):
    __doc__ = 'Enter the mesh menu.'
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
        __doc__ = 'Enter the adaption menu.'
        doc_by_method = {
            'refinement_criteria' : 'Set expression for refinement criterion.',
            'coarsening_criteria' : 'Set expression for coarsening criterion.',
            'adapt_mesh' : 'Adapt the mesh based on set refinement/coarsening criterion.',
            'display_adaption_cells' : 'Display cells marked for refinement/coarsening.',
            'list_adaption_cells' : 'List the number of cells marked for refinement/coarsening.',
            'free_hierarchy' : 'Delete the adaption hierarchy',
            'anisotropic_adaption' : 'Anisotropically refine boundary layers.',
        }

        class predefined_criteria(metaclass=PyMenuMeta):
            __doc__ = 'Enter the predefined criteria menu for adaption.'

            class aerodynamics(metaclass=PyMenuMeta):
                __doc__ = 'Enter the aerodynamics menu.'
                doc_by_method = {
                    'shock_indicator' : 'Enter the shock-indicator menu.',
                }

                class error_based(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the error-based menu.'
                    doc_by_method = {
                        'pressure_hessian_indicator' : 'Define cell registers and settings suitable for adaption using the pressure Hessian indicator.',
                    }

            class boundary_layer(metaclass=PyMenuMeta):
                __doc__ = 'Enter the boundary-layer menu.'
                doc_by_method = {
                    'cell_distance' : 'Define cell registers and adaption settings suitable for anisotropic boundary layer adaption based on cell distance.',
                }

            class combustion(metaclass=PyMenuMeta):
                __doc__ = 'Enter the combustion menu.'
                doc_by_method = {
                    'flame_indicator' : 'Define cell registers and adaption settings suitable for a flame adaptive refinement simulation.',
                }

        class set(metaclass=PyMenuMeta):
            __doc__ = 'Enter the adaption set menu.'
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
            __doc__ = 'Enter the adaption profile menu.'
            doc_by_method = {
                'enable' : 'Enable adaption profiling.',
                'disable' : 'Disable adaption profiling.',
                'print' : 'Print adaption profiling results.',
                'clear' : 'Clear adaption profiling counters.',
            }

        class cell_registers(metaclass=PyMenuMeta):
            __doc__ = 'Manage Cell Registers'
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
            __doc__ = 'Manage Adaption Criteria'
            doc_by_method = {
                'add' : 'Add a new object',
                'edit' : 'Edit an object',
                'delete' : 'Delete an object',
                'list' : 'List objects',
                'list_properties' : 'List properties of an object',
            }

        class multi_layer_refinement(metaclass=PyMenuMeta):
            __doc__ = 'Enter the multiple boundary layer refinement menu.'
            doc_by_method = {
                'refine_mesh' : 'Refine the mesh for multiple boundary layers.',
                'boundary_zones' : 'Specify boundary zones for refinement.',
                'layer_count' : 'Specify the layer count for refinement.',
                'parameters' : 'Specify parameters for multiple boundary layer refinement.',
            }

        class geometry(metaclass=PyMenuMeta):
            __doc__ = 'Enter the adaption geometry menu.'
            doc_by_method = {
                'reconstruct_geometry' : 'Enable/Disable geometry based adaption.',
                'set_geometry_controls' : 'Set geometry controls for wall zones.',
            }

    class modify_zones(metaclass=PyMenuMeta):
        __doc__ = 'Enter the modify zones menu.'
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
            'zone_type' : "Set a zone's type.",
            'copy_mrf_to_mesh_motion' : 'Copy motion variable values for origin, axis and velocities from Frame Motion to Mesh Motion.',
            'copy_mesh_to_mrf_motion' : 'Copy motion variable values for origin, axis and velocities from Mesh Motion to Frame Motion.',
            'change_zone_state' : 'Change the realgas material state for a zone.',
            'change_zone_phase' : 'Change the realgas phase for a zone.',
        }

    class polyhedra(metaclass=PyMenuMeta):
        __doc__ = 'Enter the polyhedra menu.'
        doc_by_method = {
            'convert_domain' : 'Convert entire domain to polyhedra cells.',
            'convert_hanging_nodes' : 'Convert cells with hanging nodes and faces to polyhedra.',
            'convert_hanging_nodes_zones' : 'Convert selected cell zones with hanging nodes and faces to polyhedra. \nThe selected cell zones cannot be connected to other zones.',
            'convert_skewed_cells' : 'Convert skewed cells to polyhedra.',
        }

        class options(metaclass=PyMenuMeta):
            __doc__ = 'Enter options menu.'
            doc_by_method = {
                'migrate_and_reorder' : 'Perform migration and reordering at the end of the polyhedra conversion.',
                'preserve_boundary_layer' : '0 = Decide at runtime.\n1 = Never preserve.\n2 = Always preserve.',
                'preserve_interior_zones' : 'Interior zones with matching name pattern are preserved during polyhedra conversion.',
            }

    class reorder(metaclass=PyMenuMeta):
        __doc__ = 'Enter the reorder domain menu.'
        doc_by_method = {
            'band_width' : 'Print cell bandwidth.',
            'reorder_domain' : 'Reorder cells and faces by reverse Cuthill-McKee.',
            'reorder_zones' : 'Reorder zones by partition, type, and id.',
        }

    class repair_improve(metaclass=PyMenuMeta):
        __doc__ = 'Enter the repair and improve quality menu.'
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
        __doc__ = 'Enter the surface mesh menu.'
        doc_by_method = {
            'delete' : 'Delete surface mesh.',
            'display' : 'Display surface meshes.',
            'read' : 'Read surface meshes.',
        }

class parameters__and__customization(metaclass=PyMenuMeta):
    __doc__ = 'Enter Parameters and custom menu.'

    class parameters(metaclass=PyMenuMeta):
        __doc__ = 'Enter the parameters menu.'
        doc_by_method = {
            'enable_in_TUI' : 'Enable/disable parameters in the text user interface.',
        }

        class input_parameters(metaclass=PyMenuMeta):
            __doc__ = 'Enter the input-parameters menu.'
            doc_by_method = {
                'edit' : 'Edit an input parameter.',
                'delete' : 'Delete an input parameter',
            }

            class advance(metaclass=PyMenuMeta):
                __doc__ = 'define custom variable to use input parameter'
                doc_by_method = {
                    'use_in' : 'Use input parameter in solver-udf or in scheme-procedure',
                    'list' : 'List of custom-input-parameters.',
                    'delete' : 'delete selected custom-input-parameters',
                }

        class output_parameters(metaclass=PyMenuMeta):
            __doc__ = 'Enter the output-parameters menu.'
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
        __doc__ = 'Enter the user-defined functions and scalars menu.'
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
            __doc__ = 'Enable/configure real gas model.'
            doc_by_method = {
                'nist_real_gas_model' : 'Load NIST real gas library.',
                'nist_multispecies_real_gas_model' : 'Load NIST real gas library.',
                'set_state' : 'Select state for NIST real gas model.',
                'nist_settings' : 'Select refprop library.',
                'user_defined_real_gas_model' : 'Load user-defined real gas library.',
                'user_defined_multispecies_real_gas_model' : 'Load user-defined multispecies real gas library.',
            }

class parallel(metaclass=PyMenuMeta):
    __doc__ = 'Enter the parallel processing menu.'
    doc_by_method = {
        'check' : 'Parallel check.',
        'check_verbosity' : 'Set verbosity output of parallel check. Higher verbosity corresponds to more detailed information.',
        'show_connectivity' : 'Show machine connectivity.',
        'latency' : 'Show network latency.',
        'bandwidth' : 'Show network bandwidth.',
        'thread_number_control' : 'thread number control',
    }

    class network(metaclass=PyMenuMeta):
        __doc__ = 'Enter the network configuration menu.'
        doc_by_method = {
            'kill_all_nodes' : 'Delete all compute nodes from virtual machine.',
            'kill_node' : 'Kill a compute node process specified by ID.',
            'load_hosts' : 'Read a hosts file.',
            'path' : 'Set the Fluent shell script path.',
            'save_hosts' : 'Write a hosts file.',
            'spawn_node' : 'Spawn a compute node process on a specified machine.',
        }

    class partition(metaclass=PyMenuMeta):
        __doc__ = 'Enter the partition domain menu.'
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
            __doc__ = 'Enter the menu to set auto partition parameters.'
            doc_by_method = {
                'across_zones' : 'Enable auto partitioning by zone or by domain.',
                'method' : 'Set the method for auto partitioning the domain.',
                'load_vector' : 'Set auto the partition load vector.',
                'pre_test' : 'Set auto partition pre-testing optimization.',
                'use_case_file_method' : 'Enable the use-case-file method for auto partitioning.',
            }

        class set(metaclass=PyMenuMeta):
            __doc__ = 'Enter the menu to set partition parameters.'
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
        __doc__ = 'Enter the set parallel parameters menu.'
        doc_by_method = {
            'partition_mask' : 'Set partition mask.',
            'verbosity' : 'Set the parallel verbosity.',
            'time_out' : 'Set spawn timeout seconds.',
            'fast_i' : 'Use fast I/O option.',
        }

    class load_balance(metaclass=PyMenuMeta):
        __doc__ = 'Enter the load balancing parameters menu.'
        doc_by_method = {
            'physical_models' : 'Use physical-models load balancing?',
            'dynamic_mesh' : 'Use load balancing for dynamic mesh?',
            'mesh_adaption' : 'Use load balancing for mesh adaption?',
        }

    class gpgpu(metaclass=PyMenuMeta):
        __doc__ = 'Select and show gpgpu.'
        doc_by_method = {
            'show' : 'Show gpgpu.',
            'select' : 'Select gpgpu.',
        }

    class timer(metaclass=PyMenuMeta):
        __doc__ = 'Enter the timer menu.'
        doc_by_method = {
            'usage' : 'Print solver timer.',
            'reset' : 'Reset domain timers.',
        }

    class multidomain(metaclass=PyMenuMeta):
        __doc__ = 'Enter the multidomain architecture menu.'

        class conjugate_heat_transfer(metaclass=PyMenuMeta):
            __doc__ = 'Enter the conjugate heat transfer menu for multidomain simulation.'
            doc_by_method = {
                'enable' : 'Enable/disable loosely coupled conjugate heat transfer.',
            }

            class set(metaclass=PyMenuMeta):
                __doc__ = 'Enter the set menu for loosely coupled conjugate heat transfer.'
                doc_by_method = {
                    'session_mode' : 'Setup session mode (single/multiple) for multidomain conjugate heat transfer.',
                    'coupling' : 'Specify when the fluid and solid zone calculations are coupled.',
                    'helper_session' : 'Setup helper session for multidomain conjugate heat transfer.',
                }

        class solve(metaclass=PyMenuMeta):
            __doc__ = 'Enter the multi-domain simulation solver menu.'
            doc_by_method = {
                'iterate' : 'Iteration the multidomain conjugate heat transfer.',
                'dual_time_iterate' : 'Dual-time iterate the multidomain conjugate heat transfer.',
            }

class preferences(metaclass=PyMenuMeta):
    __doc__ = 'Set preferences'

    class appearance(metaclass=PyMenuMeta):
        __doc__ = ''
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
            __doc__ = ''
            doc_by_method = {
                'color' : '',
                'visible' : '',
            }

        class charts(metaclass=PyMenuMeta):
            __doc__ = ''
            doc_by_method = {
                'curve_colors' : '',
                'enable_open_glfor_modern_plots' : '',
                'legend_alignment' : '',
                'legend_visibility' : '',
                'modern_plots_enabled' : '',
                'modern_plots_points_threshold' : '',
                'plots_behavior' : '',
                'print_plot_data' : '',
                'threshold' : '',
            }

            class font(metaclass=PyMenuMeta):
                __doc__ = ''
                doc_by_method = {
                    'axes' : '',
                    'axes_titles' : '',
                    'legend' : '',
                    'title' : '',
                }

            class text_color(metaclass=PyMenuMeta):
                __doc__ = ''
                doc_by_method = {
                    'axes' : '',
                    'axes_titles' : '',
                    'legend' : '',
                    'title' : '',
                }

        class selections(metaclass=PyMenuMeta):
            __doc__ = ''
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
        __doc__ = ''
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
        __doc__ = ''
        doc_by_method = {
            'alpha_features' : '',
        }

    class graphics(metaclass=PyMenuMeta):
        __doc__ = ''
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
            __doc__ = ''
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
            __doc__ = ''
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
            __doc__ = ''
            doc_by_method = {
                'default_embedded_mesh_windows_view' : '',
                'default_embedded_windows_view' : '',
                'save_embedded_window_layout' : '',
                'show_border_for_embedded_window' : '',
            }

        class export_video_settings(metaclass=PyMenuMeta):
            __doc__ = ''
            doc_by_method = {
                'video_format' : '',
                'video_fps' : '',
                'video_quality' : '',
                'video_resoution_x' : '',
                'video_resoution_y' : '',
                'video_scale' : '',
                'video_smooth_scaling' : '',
                'video_use_frame_resolution' : '',
            }

            class advanced_video_quality_options(metaclass=PyMenuMeta):
                __doc__ = ''
                doc_by_method = {
                    'bit_rate_quality' : '',
                    'bitrate' : '',
                    'compression_method' : '',
                    'enable_h264' : '',
                    'key_frames' : '',
                }

        class graphics_effects(metaclass=PyMenuMeta):
            __doc__ = ''
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
            __doc__ = ''
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
            __doc__ = ''
            doc_by_method = {
                'ambient_light_intensity' : '',
                'headlight' : '',
                'headlight_intensity' : '',
                'lighting_method' : '',
            }

        class manage_hoops_memory(metaclass=PyMenuMeta):
            __doc__ = ''
            doc_by_method = {
                'enabled' : '',
                'hsfimport_limit' : '',
            }

        class material_effects(metaclass=PyMenuMeta):
            __doc__ = ''
            doc_by_method = {
                'decimation_filter' : '',
                'parameterization_source' : '',
                'tiling_style' : '',
            }

        class meshing_mode(metaclass=PyMenuMeta):
            __doc__ = ''
            doc_by_method = {
                'graphics_window_display_timeout' : '',
                'graphics_window_display_timeout_value' : '',
            }

        class performance(metaclass=PyMenuMeta):
            __doc__ = ''
            doc_by_method = {
                'optimize_for' : '',
                'ratio_of_target_frame_rate_to_classify_heavy_geometry' : '',
                'ratio_of_target_frame_rate_to_declassify_heavy_geometry' : '',
            }

            class fast_display_mode(metaclass=PyMenuMeta):
                __doc__ = ''
                doc_by_method = {
                    'culling' : '',
                    'faces_shown' : '',
                    'markers_decimation' : '',
                    'nodes_shown' : '',
                    'perimeter_edges_shown' : '',
                    'silhouette_shown' : '',
                    'status' : '',
                    'transparency' : '',
                }

            class minimum_frame_rate(metaclass=PyMenuMeta):
                __doc__ = ''
                doc_by_method = {
                    'dynamic_adjustment' : '',
                    'enabled' : '',
                    'fixed_culling_value' : '',
                    'maximum_culling_threshold' : '',
                    'minimum_culling_threshold' : '',
                    'target_fps' : '',
                }

        class transparency(metaclass=PyMenuMeta):
            __doc__ = ''
            doc_by_method = {
                'algorithm_for_modern_drivers' : '',
                'depth_peeling_layers' : '',
                'depth_peeling_preference' : '',
                'quick_moves' : '',
                'zsort_options' : '',
            }

        class vector_settings(metaclass=PyMenuMeta):
            __doc__ = ''
            doc_by_method = {
                'arrow3_dradius1_factor' : '',
                'arrow3_dradius2_factor' : '',
                'arrowhead3_dradius1_factor' : '',
                'line_arrow3_dperpendicular_radius' : '',
            }

    class mat_pro_app(metaclass=PyMenuMeta):
        __doc__ = ''
        doc_by_method = {
            'beta_features' : '',
            'console' : '',
            'focus' : '',
            'warning' : '',
        }

    class meshing_workflow(metaclass=PyMenuMeta):
        __doc__ = ''
        doc_by_method = {
            'checkpointing_option' : '',
            'dock_editor' : '',
            'save_checkpoint_files' : '',
            'temp_folder' : '',
            'templates_folder' : '',
            'verbosity' : '',
        }

        class draw_settings(metaclass=PyMenuMeta):
            __doc__ = ''
            doc_by_method = {
                'auto_draw' : '',
                'face_zone_limit' : '',
                'facet_limit' : '',
            }

    class navigation(metaclass=PyMenuMeta):
        __doc__ = ''

        class mouse_mapping(metaclass=PyMenuMeta):
            __doc__ = ''
            doc_by_method = {
                'mousemaptheme' : '',
            }

            class additional(metaclass=PyMenuMeta):
                __doc__ = ''
                doc_by_method = {
                    'ctrllmbclick' : '',
                    'ctrllmbdrag' : '',
                    'ctrlmmbclick' : '',
                    'ctrlmmbdrag' : '',
                    'ctrlrmbclick' : '',
                    'ctrlrmbdrag' : '',
                    'mouseprobe' : '',
                    'mousewheel' : '',
                    'mousewheelsensitivity' : '',
                    'reversewheeldirection' : '',
                    'shiftlmbclick' : '',
                    'shiftlmbdrag' : '',
                    'shiftmmbclick' : '',
                    'shiftmmbdrag' : '',
                    'shiftrmbclick' : '',
                    'shiftrmbdrag' : '',
                }

            class basic(metaclass=PyMenuMeta):
                __doc__ = ''
                doc_by_method = {
                    'lmb' : '',
                    'lmbclick' : '',
                    'mmb' : '',
                    'mmbclick' : '',
                    'rmb' : '',
                    'rmbclick' : '',
                }

    class prj_app(metaclass=PyMenuMeta):
        __doc__ = ''
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
        __doc__ = ''
        doc_by_method = {
            'flow_model' : '',
            'local_residual_scaling' : '',
        }

        class report_definitions(metaclass=PyMenuMeta):
            __doc__ = ''
            doc_by_method = {
                'automatic_plot_file' : '',
                'report_plot_history_data_size' : '',
            }

    class turbo_workflow(metaclass=PyMenuMeta):
        __doc__ = ''

        class cell_zone_settings(metaclass=PyMenuMeta):
            __doc__ = ''
            doc_by_method = {
                'czsearch_order' : '',
                'rotating' : '',
                'stationary' : '',
            }

        class face_zone_settings(metaclass=PyMenuMeta):
            __doc__ = ''
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
            __doc__ = ''
            doc_by_method = {
                'auto_draw' : '',
            }

class results(metaclass=PyMenuMeta):
    __doc__ = 'Enter results menu.'

    class animate(metaclass=PyMenuMeta):
        __doc__ = 'Enter the animation menu.'

        class playback(metaclass=PyMenuMeta):
            __doc__ = 'Enter animation playback menu.'
            doc_by_method = {
                'read' : 'Read new animation from file or already-defined animations.',
                'play' : 'Play the selected animation.',
                'write' : 'Write animation sequence to the file.',
                'delete' : 'Delete animation sequence.',
                'stored_view' : 'Play the 3D animation sequence using the view stored in the sequence.',
                'set_custom_frames' : 'Set custom frames start, end, skip frames for video export',
            }

            class video(metaclass=PyMenuMeta):
                __doc__ = 'Set options for exporting video file menu.'
                doc_by_method = {
                    'fps' : 'Set the Frame Per Sec(FPS) for exporting video file.',
                    'format' : 'Set format for exporting video file.',
                    'quality' : 'Set quality for exporting video file.',
                    'name' : 'Exporting video file name',
                    'use_original_resolution' : 'enable original resolution',
                    'scale' : 'Set scale by which video resolution will expand.',
                    'set_standard_resolution' : 'Select from pre-defined resolution list.',
                    'width' : 'Set the width for exporting video file.',
                    'height' : 'Set the height for exporting video file.',
                }

                class advance_quality(metaclass=PyMenuMeta):
                    __doc__ = 'Advance Quality setting'
                    doc_by_method = {
                        'bitrate_scale' : 'Mp4 bitrate scale - Best-64000 High-32000 Medium-16000 Low-8000',
                        'enable_h264' : 'H264 encoding flag',
                        'bitrate' : 'Set video bitrate(kbits/sec) for exporting video file.',
                        'compression_method' : 'Compression methode for Microsoft AVI movie',
                        'keyframe' : 'Set video keyframe rate for exporting video file.',
                    }

    class graphics(metaclass=PyMenuMeta):
        __doc__ = 'Enter graphics menu.'
        doc_by_method = {
            'annotate' : 'Add a text annotation string to the active graphics window.',
            'clear_annotations' : 'Delete all annotation text.',
            'color_map' : 'Enter the color-map menu.',
            'hsf_file' : 'Display hoops stream file data to active graphics window.',
        }

        class expert(metaclass=PyMenuMeta):
            __doc__ = 'Enter expert menu.'
            doc_by_method = {
                'add_custom_vector' : 'Add new custom vector definition.',
                'contour' : 'Display contours of a flow variable.',
                'display_custom_vector' : 'Display custom vector.',
                'graphics_window_layout' : 'Arrange the graphics window layout.',
                'mesh' : 'Display the mesh.',
                'mesh_outline' : 'Display the mesh boundaries.',
                'mesh_partition_boundary' : 'Display mesh partition boundaries.',
                'multigrid_coarsening' : 'Display a coarse mesh level from the last multigrid coarsening.',
                'profile' : 'Display profiles of a flow variable.',
                'reacting_channel_curves' : 'Plot/Report the reacting channel variables.',
                're_render' : 'Re-render the last contour, profile, or velocity vector plot\n     with updated surfaces, meshes, lights, colormap, rendering options, etc.,\n     without recalculating the contour data.',
                're_scale' : 'Re-render the last contour, profile, or velocity vector plot\n     with updated scale, surfaces, meshes, lights, colormap, rendering options, etc.,\n     without recalculating the field data.',
                'set_list_tree_separator' : 'Set the separator character for list tree.',
                'surface_cells' : 'Draw the cells on the specified surfaces.',
                'surface_mesh' : 'Draw the mesh defined by the specified surfaces.',
                'vector' : 'Display space vectors.',
                'velocity_vector' : 'Display velocity vectors.',
                'zone_mesh' : 'Draw the mesh defined by specified face zones.',
            }

            class flamelet_data(metaclass=PyMenuMeta):
                __doc__ = 'Display flamelet data.'
                doc_by_method = {
                    'draw_number_box' : 'Enable/disable display of the numbers box.',
                    'plot_1d_slice' : 'Enable/disable plot of the 1D-slice.',
                    'write_to_file' : 'Enable/disable writing the 1D-slice to file instead of plot.',
                    'carpet_plot' : 'Enable/disable display of carpet plot of a property.',
                }

            class particle_tracks(metaclass=PyMenuMeta):
                __doc__ = 'Enter the particle tracks menu.'
                doc_by_method = {
                    'particle_tracks' : 'Calculate and display particle tracks from defined injections.',
                    'plot_write_xy_plot' : 'Plot or write XY plot of particle tracks.',
                }

            class path_lines(metaclass=PyMenuMeta):
                __doc__ = 'Enter the pathlines menu.'
                doc_by_method = {
                    'path_lines' : 'Display pathlines from a surface.',
                    'plot_write_xy_plot' : 'Plot or write XY plot of pathline.',
                    'write_to_files' : 'Write Pathlines to a File.',
                }

            class pdf_data(metaclass=PyMenuMeta):
                __doc__ = 'Enter the PDF data menu.'
                doc_by_method = {
                    'draw_number_box' : 'Enable/disable the display of the numbers box.',
                    'plot_1d_slice' : 'Enable/disable a plot of the 1D-slice.',
                    'write_to_file' : 'Enable/disable writing the 1D-slice to file instead of plot.',
                    'carpet_plot' : 'Enable/disable the display of a carpet plot of a property.',
                }

            class set(metaclass=PyMenuMeta):
                __doc__ = 'Enter the set menu to set display parameters.'
                doc_by_method = {
                    'color_map' : 'Enter the color-map menu.',
                    'element_shrink' : 'Set percentage to shrink elements.',
                    'filled_mesh' : 'Enable/disable the filled mesh option.',
                    'mesh_level' : 'Set coarse mesh level to be drawn.',
                    'mesh_partitions' : 'Enable/disable drawing of the mesh partition boundaries.',
                    'mesh_surfaces' : 'Set surface IDs to be drawn as mesh',
                    'mesh_zones' : 'Set zone IDs to be drawn as mesh',
                    'line_weight' : 'Set the line-weight factor for the window.',
                    'marker_size' : 'Set the size of markers used to represent points.',
                    'marker_symbol' : 'Set the type of markers used to represent points.',
                    'mesh_display_configuration' : 'Set mesh display configuration',
                    'mirror_zones' : 'Set zones to mirror the domain about.',
                    'n_stream_func' : 'Set the number of iterations used in computing stream function.',
                    'nodewt_based_interp' : 'Use more accurate node-weight based interpolation for postprocessing',
                    'overlays' : 'Enable/disable overlays.',
                    'periodic_instancing' : 'Set periodic instancing.',
                    'proximity_zones' : 'Set zones to be used for boundary cell distance and boundary proximity.',
                    'render_mesh' : 'Enable/disable rendering the mesh on top of contours, vectors, etc.',
                    'reset_graphics' : 'Reset the graphics system.',
                    'zero_angle_dir' : 'Set the vector having zero angular coordinates.',
                    'duplicate_node_display' : 'Set flag to remove duplicate nodes in mesh display.',
                }

                class colors(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the color options menu.'
                    doc_by_method = {
                        'background' : 'Set the background (window) color.',
                        'color_by_type' : 'Determine whether to color meshes by type or by surface (ID).',
                        'foreground' : 'Set the foreground (text and window frame) color.',
                        'far_field_faces' : 'Set the color of far field faces.',
                        'inlet_faces' : 'Set the color of inlet faces.',
                        'interior_faces' : 'Set the color of interior faces.',
                        'internal_faces' : 'Set the color of internal interface faces',
                        'outlet_faces' : 'Set the color of outlet faces.',
                        'overset_faces' : 'Set the color of overset faces.',
                        'periodic_faces' : 'Set the color of periodic faces.',
                        'rans_les_interface_faces' : 'Set the color of RANS/LES interface faces.',
                        'reset_user_colors' : 'Reset all user colors',
                        'show_user_colors' : 'List currently defined user colors',
                        'symmetry_faces' : 'Set the color of symmetric faces.',
                        'axis_faces' : 'Set the color of axisymmetric faces.',
                        'free_surface_faces' : 'Set the color of free-surface faces.',
                        'traction_faces' : 'Set the color of traction faces.',
                        'user_color' : 'Explicitly set color of display zone',
                        'wall_faces' : 'Set the color of wall faces.',
                        'interface_faces' : 'Set the color of mesh Interfaces.',
                        'list' : 'List available colors.',
                        'reset_colors' : 'Reset individual mesh surface colors to the defaults.',
                        'surface' : 'Set the color of surfaces.',
                        'skip_label' : 'Set the number of labels to be skipped in the colopmap scale.',
                        'automatic_skip' : 'Determine whether to skip labels in the colopmap scale automatically.',
                        'graphics_color_theme' : 'Enter the graphics color theme menu.',
                    }

                    class by_type(metaclass=PyMenuMeta):
                        __doc__ = 'Enter the zone type color and material assignment menu.'
                        doc_by_method = {
                            'only_list_case_boundaries' : 'Only list the boundary types that are assigned in this case.',
                            'reset' : 'To reset colors and/or materials to the defaults.',
                        }

                        class type_name(metaclass=PyMenuMeta):
                            __doc__ = 'Select the boundary type to specify colors and/or materials.'

                            class axis(metaclass=PyMenuMeta):
                                __doc__ = 'Set the material and/or color for the selected boundary type.'
                                doc_by_method = {
                                    'color' : 'Set a color for the selected boundary type.',
                                    'material' : 'Set a material for the selected boundary type.',
                                }

                            class far_field(metaclass=PyMenuMeta):
                                __doc__ = 'Set the material and/or color for the selected boundary type.'
                                doc_by_method = {
                                    'color' : 'Set a color for the selected boundary type.',
                                    'material' : 'Set a material for the selected boundary type.',
                                }

                            class free_surface(metaclass=PyMenuMeta):
                                __doc__ = 'Set the material and/or color for the selected boundary type.'
                                doc_by_method = {
                                    'color' : 'Set a color for the selected boundary type.',
                                    'material' : 'Set a material for the selected boundary type.',
                                }

                            class inlet(metaclass=PyMenuMeta):
                                __doc__ = 'Set the material and/or color for the selected boundary type.'
                                doc_by_method = {
                                    'color' : 'Set a color for the selected boundary type.',
                                    'material' : 'Set a material for the selected boundary type.',
                                }

                            class interface(metaclass=PyMenuMeta):
                                __doc__ = 'Set the material and/or color for the selected boundary type.'
                                doc_by_method = {
                                    'color' : 'Set a color for the selected boundary type.',
                                    'material' : 'Set a material for the selected boundary type.',
                                }

                            class interior(metaclass=PyMenuMeta):
                                __doc__ = 'Set the material and/or color for the selected boundary type.'
                                doc_by_method = {
                                    'color' : 'Set a color for the selected boundary type.',
                                    'material' : 'Set a material for the selected boundary type.',
                                }

                            class internal(metaclass=PyMenuMeta):
                                __doc__ = 'Set the material and/or color for the selected boundary type.'
                                doc_by_method = {
                                    'color' : 'Set a color for the selected boundary type.',
                                    'material' : 'Set a material for the selected boundary type.',
                                }

                            class outlet(metaclass=PyMenuMeta):
                                __doc__ = 'Set the material and/or color for the selected boundary type.'
                                doc_by_method = {
                                    'color' : 'Set a color for the selected boundary type.',
                                    'material' : 'Set a material for the selected boundary type.',
                                }

                            class overset(metaclass=PyMenuMeta):
                                __doc__ = 'Set the material and/or color for the selected boundary type.'
                                doc_by_method = {
                                    'color' : 'Set a color for the selected boundary type.',
                                    'material' : 'Set a material for the selected boundary type.',
                                }

                            class periodic(metaclass=PyMenuMeta):
                                __doc__ = 'Set the material and/or color for the selected boundary type.'
                                doc_by_method = {
                                    'color' : 'Set a color for the selected boundary type.',
                                    'material' : 'Set a material for the selected boundary type.',
                                }

                            class rans_les_interface(metaclass=PyMenuMeta):
                                __doc__ = 'Set the material and/or color for the selected boundary type.'
                                doc_by_method = {
                                    'color' : 'Set a color for the selected boundary type.',
                                    'material' : 'Set a material for the selected boundary type.',
                                }

                            class surface(metaclass=PyMenuMeta):
                                __doc__ = 'Set the material and/or color for the selected boundary type.'
                                doc_by_method = {
                                    'color' : 'Set a color for the selected boundary type.',
                                    'material' : 'Set a material for the selected boundary type.',
                                }

                            class symmetry(metaclass=PyMenuMeta):
                                __doc__ = 'Set the material and/or color for the selected boundary type.'
                                doc_by_method = {
                                    'color' : 'Set a color for the selected boundary type.',
                                    'material' : 'Set a material for the selected boundary type.',
                                }

                            class traction(metaclass=PyMenuMeta):
                                __doc__ = 'Set the material and/or color for the selected boundary type.'
                                doc_by_method = {
                                    'color' : 'Set a color for the selected boundary type.',
                                    'material' : 'Set a material for the selected boundary type.',
                                }

                            class wall(metaclass=PyMenuMeta):
                                __doc__ = 'Set the material and/or color for the selected boundary type.'
                                doc_by_method = {
                                    'color' : 'Set a color for the selected boundary type.',
                                    'material' : 'Set a material for the selected boundary type.',
                                }

                class contours(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the contour options menu.'
                    doc_by_method = {
                        'auto_range' : 'Enable/disable auto-computation of range for contours.',
                        'clip_to_range' : 'Enable/disable the clip to range option for filled contours.',
                        'surfaces' : 'Set surfaces to be contoured.',
                        'filled_contours' : 'Enable/disable the filled contour option.',
                        'global_range' : 'Enable/disable the global range for contours option.',
                        'line_contours' : 'Enable/disable the filled contour option.',
                        'log_scale' : 'Enable/disable the use of a log scale.',
                        'n_contour' : 'Set the number of contour levels.',
                        'node_values' : 'Enable/disable the plot of node values.',
                        'render_mesh' : 'Determine whether or not to render the mesh on top of contours, vectors, etc.',
                        'coloring' : 'Select coloring option',
                    }

                class picture(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the hardcopy/save-picture options menu.'
                    doc_by_method = {
                        'invert_background' : 'Exchange foreground/background colors for hardcopy.',
                        'landscape' : 'Plot hardcopies in landscape or portrait orientation.',
                        'preview' : 'Display a preview image of a hardcopy.',
                        'x_resolution' : 'Set the width of raster-formatted images in pixels (0 implies current window size).',
                        'y_resolution' : 'Set the height of raster-formatted images in pixels (0 implies current window size).',
                        'dpi' : 'Set the DPI for EPS and Postscript files, specifies the resolution in dots per inch (DPI) instead of setting the width and height',
                        'use_window_resolution' : "Use the currently active window's resolution for hardcopy (ignores the x-resolution and y-resolution in this case).",
                        'set_standard_resolution' : 'Select from pre-defined resolution list.',
                        'jpeg_hardcopy_quality' : 'To set jpeg hardcopy quality.',
                    }

                    class color_mode(metaclass=PyMenuMeta):
                        __doc__ = 'Enter the hardcopy color mode menu.'
                        doc_by_method = {
                            'color' : 'Plot hardcopies in color.',
                            'gray_scale' : 'Convert color to grayscale for hardcopy.',
                            'mono_chrome' : 'Convert color to monochrome (black and white) for hardcopy.',
                            'list' : 'Display the current hardcopy color mode.',
                        }

                    class driver(metaclass=PyMenuMeta):
                        __doc__ = 'Enter the set hardcopy driver menu.'
                        doc_by_method = {
                            'dump_window' : 'Set the command used to dump the graphics window to a file.',
                            'eps' : 'Produce encapsulated PostScript (EPS) output for hardcopies.',
                            'jpeg' : 'Produce JPEG output for hardcopies.',
                            'post_script' : 'Produce PostScript output for hardcopies.',
                            'ppm' : 'Produce PPM output for hardcopies.',
                            'tiff' : 'Use TIFF output for hardcopies.',
                            'png' : 'Use PNG output for hardcopies.',
                            'hsf' : 'Use HSF output for hardcopies.',
                            'avz' : 'Use AVZ output for hardcopies.',
                            'glb' : 'Use GLB output for hardcopies.',
                            'vrml' : 'Use VRML output for hardcopies.',
                            'list' : 'List the current hardcopy driver.',
                            'options' : 'Set the hardcopy options. Available options are:\n\\\\n               \t"no gamma correction", disables gamma correction of colors,\n\\\\n               \t"physical size = (width,height)", where width and height\n          are the actual measurements of the printable area of the page\n          in centimeters.\n\\\\n               \t"subscreen = (left,right,bottom,top)", where left,right,\n          bottom, and top are numbers in [-1,1] describing a subwindow on\n          the page in which to place the hardcopy.\n\n\\\\n          The options may be combined by separating them with commas.',
                        }

                        class post_format(metaclass=PyMenuMeta):
                            __doc__ = 'Enter the PostScript driver format menu.'
                            doc_by_method = {
                                'fast_raster' : 'Use the new raster format.',
                                'raster' : 'Use the original raster format.',
                                'rle_raster' : 'Use the run-length encoded raster format.',
                                'vector' : 'Use vector format.',
                            }

                class lights(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the lights menu.'
                    doc_by_method = {
                        'lights_on' : 'Turn all active lighting on/off.',
                        'set_ambient_color' : 'Set the ambient light color for the scene.',
                        'set_light' : 'Add or modify a directional, colored light.',
                        'headlight_on' : 'Turn the light that moves with the camera on or off.',
                    }

                    class lighting_interpolation(metaclass=PyMenuMeta):
                        __doc__ = 'Set lighting interpolation method.'
                        doc_by_method = {
                            'automatic' : 'Choose Automatic to automatically select the best lighting method for a given graphics object.',
                            'flat' : 'Use flat shading for meshes and polygons.',
                            'gouraud' : 'Use Gouraud shading to calculate the color at each vertex of a polygon and interpolate it in the interior.',
                            'phong' : 'Use Phong shading to interpolate the normals for each pixel of a polygon and compute a color at every pixel.',
                        }

                class particle_tracks(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the particle-tracks menu to set parameters for display of particle tracks.'
                    doc_by_method = {
                        'display' : 'Determine whether particle tracks will be displayed or only tracked.',
                        'history_filename' : 'Specify the name of the particle history file.',
                        'report_to' : 'Specify the destination for the report (console, file, none).',
                        'report_type' : 'Set the report type for particle tracks.',
                        'report_variables' : 'Set the report variables.',
                        'report_default_variables' : 'Set the report variables to default.',
                        'track_single_particle_stream' : 'Specify the stream ID to be tracked.',
                        'arrow_scale' : 'Set the scale factor for arrows drawn on particle tracks.',
                        'arrow_space' : 'Set the spacing factor for arrows drawn on particle tracks.',
                        'coarsen_factor' : 'Set the particle tracks coarsening factor.',
                        'line_width' : 'Set the width for particle track.',
                        'marker_size' : 'Set the marker size for particle drawing.',
                        'radius' : 'Set the radius for particle track (ribbons/cylinder only) cross-section.',
                        'style' : 'Set the display style for particle track (line/ribbon/cylinder/sphere).',
                        'twist_factor' : 'Set the scale factor for twisting (ribbons only).',
                        'sphere_attrib' : 'Specify size and number of slices to be used in drawing spheres.',
                        'particle_skip' : 'Specify how many particle tracks should be displayed.',
                    }

                    class sphere_settings(metaclass=PyMenuMeta):
                        __doc__ = 'Provide sphere specific input.'
                        doc_by_method = {
                            'vary_diameter' : 'Specify whether the spheres can vary with another variable.',
                            'diameter' : 'Diameter of the spheres when vary-diameter? is disabled.',
                            'auto_range' : 'Specify whether displayed spheres should include auto range of variable to size spheres.',
                            'minimum' : 'Set the minimum value of the sphere to be displayed.',
                            'maximum' : 'Set the maximum value of the sphere to be displayed.',
                            'smooth_parameter' : 'Specify number of slices to be used in drawing spheres.',
                            'scale_factor' : 'Specify a scale factor to enlarge/reduce the size of spheres.',
                            'size_variable' : 'Select a particle variable to size the spheres.',
                        }

                    class vector_settings(metaclass=PyMenuMeta):
                        __doc__ = 'Set vector specific input.'
                        doc_by_method = {
                            'style' : 'Enable and set the display style for particle vectors (none/vector/centered-vector/centered-cylinder).',
                            'vector_length' : 'Specify the length of constant vectors.',
                            'vector_length_variable' : 'Select a particle variable to specify the length of vectors.',
                            'scale_factor' : 'Specify a scale factor to enlarge/reduce the length of vectors.',
                            'length_variable' : 'Specify whether the displayed vectors have length varying with another variable.',
                            'length_to_head_ratio' : 'Specify ratio of length to head for vectors and length to diameter for cylinders.',
                            'constant_color' : 'Specify a constant color for the vectors.',
                            'color_variable' : 'Specify whether the vectors should be colored by variable specified in /display/particle-track/particle-track (if false use a constant color).',
                            'vector_variable' : 'Select a particle vector function to specify vector direction.',
                        }

                    class filter_settings(metaclass=PyMenuMeta):
                        __doc__ = 'Set filter for particle display.'
                        doc_by_method = {
                            'enable_filtering' : 'Specify whether particle display is filtered.',
                            'inside' : 'Specify whether filter variable needs to be inside min/max to be displayed (else outside min/max).',
                            'filter_variable' : 'Select a variable used for filtering of particles.',
                            'minimum' : 'Specify the lower bound for the filter variable.',
                            'maximum' : 'Specify the upper bound for the filter variable.',
                        }

                class path_lines(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the path-lines menu to set parameters for the display of pathlines.'
                    doc_by_method = {
                        'arrow_scale' : 'Set the scale factor for arrows drawn on pathlines.',
                        'arrow_space' : 'Set the spacing factor for arrows drawn on pathlines.',
                        'display_steps' : 'Set the display stepping for pathlines.',
                        'error_control' : 'Set error control during pathline computation.',
                        'line_width' : 'Set the width for pathlines.',
                        'marker_size' : 'Set the marker size for particle drawing.',
                        'maximum_steps' : 'Set the maximum number of steps to take for pathlines.',
                        'maximum_error' : 'Set the maximum error allowed while computing the pathlines.',
                        'radius' : 'Set the radius for pathline (ribbons/cylinder only) cross-section.',
                        'relative_pathlines' : 'Enable/disable the tracking of pathlines in a relative coordinate system.',
                        'style' : 'Set display style for pathlines (line/ribbon/cylinder).',
                        'twist_factor' : 'Set the scale factor for twisting (ribbons only).',
                        'step_size' : 'Set the step length between particle positions for path-lines.',
                        'reverse' : 'Enable/disable the direction of path tracking.',
                        'sphere_attrib' : 'Specify size and no. of slices to be used in drawing sphere for sphere-style.',
                        'track_in_phase' : 'Assign phase to display pathlines in.',
                    }

                class rendering_options(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the rendering options menu.'
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

                class titles(metaclass=PyMenuMeta):
                    __doc__ = 'Set problem title.'
                    doc_by_method = {
                        'left_top' : 'Set the title text for left top in title segment',
                        'left_bottom' : 'Set the title text for left bottom in title segment',
                        'right_top' : 'Set the title text for right top in title segment',
                        'right_middle' : 'Set the title text for right middle in title segment',
                        'right_bottom' : 'Set the title text for right bottom in title segment',
                    }

                class velocity_vectors(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the menu to set parameters for display of velocity vectors.'
                    doc_by_method = {
                        'auto_scale' : 'Enable/disable auto-scale of all vectors so that vector overlap is minimal.',
                        'color' : 'Set the color used for all vectors. Set color to the null string to use the color map.',
                        'component_x' : 'Enable/disable use of x-component of vectors.',
                        'component_y' : 'Enable/disable use of y-component of vectors.',
                        'component_z' : 'Enable/disable use of z-component of vectors.',
                        'constant_length' : 'Enable/disable setting all vectors to have the same length.',
                        'color_levels' : 'Set the number of colors used from the color map.',
                        'global_range' : 'Enable/disable the global range for vectors option.',
                        'in_plane' : 'Toggle the display of in-plane velocity vectors.',
                        'log_scale' : 'Enable/disable the use of a log scale.',
                        'node_values' : 'Enable/disable plotting node values. Cell values will be plotted if "no".',
                        'relative' : 'Enable/disable the display of relative velocity vectors.',
                        'render_mesh' : 'Enable/disable rendering the mseh on top of contours, vectors, etc.',
                        'scale' : 'Set the value by which the vector length will be scaled.',
                        'scale_head' : 'Set the value by which the vector head will be scaled.',
                        'style' : 'Set the style with which the vectors will be drawn.',
                        'surfaces' : 'Set surfaces on which vectors are drawn.',
                    }

                class windows(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the window options menu.'
                    doc_by_method = {
                        'aspect_ratio' : 'Set the aspect ratio of the active window.',
                        'logo' : 'Enable/disable visibility of the logo in graphics window.',
                        'ruler' : 'Enable/disable ruler visibility.',
                        'logo_color' : 'Set logo color to white/black.',
                    }

                    class axes(metaclass=PyMenuMeta):
                        __doc__ = 'Enter the axes window options menu.'
                        doc_by_method = {
                            'border' : 'Enable/disable drawing of a border around the axes window.',
                            'bottom' : 'Set the bottom boundary of the axes window.',
                            'clear' : 'Set the transparency of the axes window.',
                            'right' : 'Set the right boundary of the axes window.',
                            'visible' : 'Enable/disable axes visibility.',
                        }

                    class main(metaclass=PyMenuMeta):
                        __doc__ = 'Enter the main view window options menu.'
                        doc_by_method = {
                            'border' : 'Enable/disable drawing of borders around the main viewing window.',
                            'bottom' : 'Set the bottom boundary of the main viewing window.',
                            'left' : 'Set the left boundary of the main viewing window.',
                            'right' : 'Set the right boundary of the main viewing window.',
                            'top' : 'Set the top boundary of the main viewing window.',
                            'visible' : 'Enable/disable visibility of the main viewing window.',
                        }

                    class scale(metaclass=PyMenuMeta):
                        __doc__ = 'Enter the color scale window options menu.'
                        doc_by_method = {
                            'border' : 'Enable/disable drawing of borders around the color scale window.',
                            'bottom' : 'Set the bottom boundary of the color scale window.',
                            'clear' : 'Set the transparency of the scale window.',
                            'format' : 'Set the number format of the color scale window (e.g. %0.2e).',
                            'font_size' : 'Set the font size of the color scale window.',
                            'left' : 'Set the left boundary of the color scale window.',
                            'margin' : 'Set the margin of the color scale window.',
                            'right' : 'Set the right boundary of the color scale window.',
                            'top' : 'Set the top boundary of the color scale window.',
                            'visible' : 'Enable/disable visibility of the color scale window.',
                            'alignment' : 'Set colormap to bottom/left/top/right',
                        }

                    class text(metaclass=PyMenuMeta):
                        __doc__ = 'Enter the text window options menu.'
                        doc_by_method = {
                            'application' : 'Enable/disable the application name in the picture.',
                            'border' : 'Enable/disable drawing of borders around the text window.',
                            'bottom' : 'Set the bottom boundary of the text window.',
                            'clear' : 'Enable/disable text window transparency.',
                            'company' : 'Enable/disable the company name in the picture.',
                            'date' : 'Enable/disable the date in the picture.',
                            'left' : 'Set the left boundary of the text window.',
                            'right' : 'Set the right boundary of the text window.',
                            'top' : 'Set the top boundary of the text window.',
                            'visible' : 'Enable/disable text window transparency.',
                        }

                    class video(metaclass=PyMenuMeta):
                        __doc__ = 'Enter the video window options menu.'
                        doc_by_method = {
                            'background' : 'Set the background color in the video picture.',
                            'color_filter' : 'Set the color filter options for the picture.',
                            'foreground' : 'Set the foreground color in the video picture.',
                            'on' : 'Enable/disable video picture settings.',
                            'pixel_size' : 'Set the window size in pixels.',
                        }

                    class xy(metaclass=PyMenuMeta):
                        __doc__ = 'Enter the X-Y plot window options menu.'
                        doc_by_method = {
                            'border' : 'Enable/disable drawing of a border around the X-Y plotter window.',
                            'bottom' : 'Set the bottom boundary of the X-Y plotter window.',
                            'left' : 'Set the left boundary of the X-Y plotter window.',
                            'right' : 'Set the right boundary of the X-Y plotter window.',
                            'top' : 'Set the top boundary of the X-Y plotter window.',
                            'visible' : 'Enable/disable X-Y plotter window visibility.',
                        }

        class lights(metaclass=PyMenuMeta):
            __doc__ = 'Enter the lights menu.'
            doc_by_method = {
                'lights_on' : 'Turn all active lighting on/off.',
                'set_ambient_color' : 'Set the ambient light color for the scene.',
                'set_light' : 'Add or modify a directional, colored light.',
                'headlight_on' : 'Turn the light that moves with the camera on or off.',
            }

            class lighting_interpolation(metaclass=PyMenuMeta):
                __doc__ = 'Set lighting interpolation method.'
                doc_by_method = {
                    'automatic' : 'Choose Automatic to automatically select the best lighting method for a given graphics object.',
                    'flat' : 'Use flat shading for meshes and polygons.',
                    'gouraud' : 'Use Gouraud shading to calculate the color at each vertex of a polygon and interpolate it in the interior.',
                    'phong' : 'Use Phong shading to interpolate the normals for each pixel of a polygon and compute a color at every pixel.',
                }

        class objects(metaclass=PyMenuMeta):
            __doc__ = 'Enter to add, edit, delete or display graphics objects'
            is_extended_tui = True
            doc_by_method = {
                'create' : 'Create new graphics object.',
                'edit' : 'Edit graphics object.',
                'copy' : 'Copy graphics object.',
                'delete' : 'Delete graphics object.',
                'display' : 'Display graphics object.',
                'add_to_graphics' : 'Add graphics object to existing graphics.',
            }

            class mesh(metaclass=PyNamedObjectMeta):
                __doc__ = ''
                is_extended_tui = True

                class name(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class options(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                    class nodes(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class edges(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class faces(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class partitions(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class overset(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class gap(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                class edge_type(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                    class all(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class feature(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                        class feature_angle(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                    class outline(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                class shrink_factor(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class surfaces_list(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class coloring(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                    class automatic(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                        class type(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                        class id(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                        class normal(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                        class partition(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                    class manual(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                        class faces(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                        class edges(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                        class nodes(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                        class material_color(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                class display_state_name(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

            class contour(metaclass=PyNamedObjectMeta):
                __doc__ = ''
                is_extended_tui = True

                class name(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class field(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class filled(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class boundary_values(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class contour_lines(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class node_values(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class surfaces_list(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class range_option(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                    class auto_range_on(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                        class global_range(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                    class auto_range_off(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                        class clip_to_range(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                        class minimum(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                        class maximum(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                class coloring(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                    class smooth(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class banded(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                class color_map(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                    class visible(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class size(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class color(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class log_scale(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class format(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class user_skip(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class show_all(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class position(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class font_name(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class font_automatic(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class font_size(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class length(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class width(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                class draw_mesh(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class mesh_object(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class display_state_name(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

            class vector(metaclass=PyNamedObjectMeta):
                __doc__ = ''
                is_extended_tui = True

                class name(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class field(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class vector_field(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class surfaces_list(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class scale(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                    class auto_scale(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class scale_f(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                class style(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class skip(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class vector_opt(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                    class in_plane(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class fixed_length(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class x_comp(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class y_comp(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class z_comp(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class scale_head(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class color(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                class range_option(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                    class auto_range_on(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                        class global_range(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                    class auto_range_off(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                        class clip_to_range(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                        class minimum(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                        class maximum(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                class color_map(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                    class visible(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class size(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class color(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class log_scale(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class format(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class user_skip(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class show_all(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class position(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class font_name(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class font_automatic(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class font_size(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class length(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class width(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                class draw_mesh(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class mesh_object(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class display_state_name(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

        class rendering_options(metaclass=PyMenuMeta):
            __doc__ = 'Enter the rendering options menu.'
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
            __doc__ = 'Enter the scene options menu.'
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
        __doc__ = 'Enter the XY plot menu.'
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
            'set_boundary_val_off' : 'Set boundary value off when node values off for XY/Solution Plot.\n       \n Note: This setting is valid for current Fluent session only.',
            'label_alignment' : 'Set the alignment of xy plot label to horizontal or axis aligned.',
        }

        class ansys_sound_analysis(metaclass=PyMenuMeta):
            __doc__ = 'Ansys Sound analysis and specification.'
            doc_by_method = {
                'write_files' : 'write Ansys Sound out files',
                'print_indicators' : 'print Ansys Sound indicators',
            }

        class cumulative_plot(metaclass=PyMenuMeta):
            __doc__ = 'Plot Cumulative Force and Moments'
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
            __doc__ = 'Plot flamelet curves.'
            doc_by_method = {
                'write_to_file' : 'Write curve to a file instead of plot.',
                'plot_curves' : 'Plot of a property.',
            }

    class report(metaclass=PyMenuMeta):
        __doc__ = 'Enter the report menu.'
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
            __doc__ = 'Enter the DPM histogram menu.'
            doc_by_method = {
                'compute_sample' : 'Compute minimum/maximum of a sample variable.',
                'delete_sample' : 'Delete a sample from loaded sample list.',
                'list_samples' : 'Show all samples in loaded sample list.',
                'plot_sample' : 'Plot a histogram of a loaded sample.',
                'read_sample' : 'Read a sample file and add it to the sample list.',
                'write_sample' : 'Write a histogram of a loaded sample into a file.',
                'pick_sample_to_reduce' : 'Pick a sample for which to first set-up and then perform the data reduction.',
                'reduce_picked_sample' : 'Reduce a sample after first picking it and setting up all data-reduction options and parameters.',
            }

            class set(metaclass=PyMenuMeta):
                __doc__ = 'Enter the settings menu for the histogram.'
                doc_by_method = {
                    'auto_range' : 'Automatically compute range of sampling variable for histogram plots.',
                    'correlation' : 'Compute correlation of sampling variable with other variable.',
                    'cumulation_curve' : 'Compute a cumulative curve for sampling variable or correlation variable when correlation? was specified.',
                    'diameter_statistics' : 'Compute Rosin Rammler parameters, Sauter and other mean diameters.\nRequires specification of diameter as sampling variable.',
                    'histogram_mode' : 'Use bars for histogram plot or xy-style.',
                    'minimum' : 'Specify mimimum value of x-axis variable for histogram plots.',
                    'maximum' : 'Specify maximum value of x-axis variable for histogram plots.',
                    'number_of_bins' : 'Specify the number of bins.',
                    'percentage' : 'Use percentages of bins to be computed.',
                    'variable_power_3' : 'Use the cubic of the cumulation variable during computation of the cumulative curve.\nWhen the particle mass was not sampled, the diameter can be used instead.',
                    'logarithmic' : 'Use logarithmic scaling on the abscissa (variable axis)? -- Will not work unless all values are positive.',
                    'weighting' : 'Use weighting with additional variable when sorting data into samples.',
                }

            class setup_reduction(metaclass=PyMenuMeta):
                __doc__ = 'Set up the sample data reduction by specifying all relevant options and setting parameters as desired.'
                doc_by_method = {
                    'use_weighting' : 'Specify whether to use any weighting in the averaging that is done in each bin in the data reduction.',
                    'weighting_variable' : 'Choose the weighting variable for the averaging in each bin in the data reduction.',
                    'make_steady_from_unsteady_file' : 'Specify whether the unsteady sample is to be reduced into a steady-state injection file.',
                    'reset_min_and_max' : 'Reset the min and max values of the range to be considered for a specific variable in the data reduction.',
                    'minimum' : 'Set the minimum value of the range to be considered for a specific variable in the data reduction.',
                    'maximum' : 'Set the maximum value of the range to be considered for a specific variable in the data reduction.',
                    'logarithmic' : 'Switch on or off logarithmic scaling to be used for a specific variable in the data reduction.',
                    'number_of_bins' : 'Set the number of bins to be used for a specific variable in the data reduction.',
                    'all_variables_number_of_bins' : 'Set the number of bins to be used for ALL variables in the data reduction.',
                    'list_settings' : 'List all user inputs for the sample picked for data reduction.',
                }

        class fluxes(metaclass=PyMenuMeta):
            __doc__ = 'Flux report menu.'
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
            __doc__ = 'Force report menu.'
            doc_by_method = {
                'wall_forces' : 'Print integrated pressure and viscous forces on wall zones.',
                'wall_moments' : 'Print integrated pressure and viscous moments on wall zones.',
                'pressure_center' : 'Print center of pressure on wall zones.',
            }

        class reference_values(metaclass=PyMenuMeta):
            __doc__ = 'Reference value menu.'
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
                __doc__ = 'Enter the compute menu.'
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

        class surface_integrals(metaclass=PyMenuMeta):
            __doc__ = 'Surface Integral menu.'
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
            __doc__ = 'Volume Integral menu.'
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
            __doc__ = 'Enter the menu for setting up the Modified Settings Summary table.'
            doc_by_method = {
                'modified_setting' : 'Specify which settings will be checked for non-default status for generating the Modified Settings Summary table.',
                'write_user_setting' : 'Write the contents of the Modified Settings Summary table to a file.',
            }

        class population_balance(metaclass=PyMenuMeta):
            __doc__ = 'Population Balance menu.'
            doc_by_method = {
                'moments' : 'Set moments for population balance.',
                'number_density' : 'Set number density functions.',
            }

        class heat_exchanger(metaclass=PyMenuMeta):
            __doc__ = 'Enter the heat exchanger menu.'
            doc_by_method = {
                'computed_heat_rejection' : 'Print total heat rejection.',
                'inlet_temperature' : 'Print inlet temperature.',
                'outlet_temperature' : 'Print outlet temperature.',
                'mass_flow_rate' : 'Print mass flow rate.',
                'specific_heat' : "Print fluid's specific heat.",
            }

        class system(metaclass=PyMenuMeta):
            __doc__ = 'Sytem menu.'
            doc_by_method = {
                'proc_stats' : 'Fluent process information.',
                'sys_stats' : 'System information.',
                'gpgpu_stats' : 'GPGPU information.',
                'time_stats' : 'Time usage information.',
            }

        class simulation_reports(metaclass=PyMenuMeta):
            __doc__ = 'Enter the simulation reports menu.'
            doc_by_method = {
                'list_simulation_reports' : 'List all report names.',
                'generate_simulation_report' : 'Generate a new simulation report or regenerate an existing simulation report with the provided name.',
                'view_simulation_report' : "View a simulation report that has already been generated. In batch mode this will print the report's URL.",
                'export_simulation_report_as_pdf' : 'Export the provided simulation report as a PDF file.',
                'export_simulation_report_as_html' : 'Export the provided simulation report as HTML.',
                'write_report_names_to_file' : 'Write the list of currently generated report names to a txt file.',
                'rename_simulation_report' : 'Rename a report which has already been generated.',
                'duplicate_simulation_report' : 'Duplicate a report and all of its settings to a new report.',
                'reset_report_to_defaults' : 'Reset all report settings to default for the provided simulation report.',
                'delete_simulation_report' : 'Delete the provided simulation report.',
                'write_simulation_report_template_file' : "Write a JSON template file with this case's Simulation Report settings.",
                'read_simulation_report_template_file' : 'Read a JSON template file with existing Simulation Report settings.',
            }

    class surface(metaclass=PyMenuMeta):
        __doc__ = 'Enter the data surface manipulation menu.'
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
            __doc__ = 'Enter surface query menu.'
            doc_by_method = {
                'delete_query' : 'Delete saved query.',
                'list_surfaces' : 'List surfaces.',
                'named_surface_list' : 'Create named list of surfaces.',
                'list_named_selection' : 'List named selection of surface type',
                'list_queries' : 'List all saved queries',
            }

    class graphics_window(metaclass=PyMenuMeta):
        __doc__ = 'Enter graphics window menu'
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
            __doc__ = 'Enter to embed, close, move-out embedded windows'
            doc_by_method = {
                'close' : 'Close an embedded window.',
                'close_all' : 'Close all embedded windows for given parent window.',
                'embed_in' : 'Embed Window into another window',
                'move_out' : 'Move out an embedded window',
                'move_out_all' : 'Move out all embedded windows for given parent window.',
            }

        class picture(metaclass=PyMenuMeta):
            __doc__ = 'Enter the hardcopy/save-picture options menu.'
            doc_by_method = {
                'invert_background' : 'Exchange foreground/background colors for hardcopy.',
                'landscape' : 'Plot hardcopies in landscape or portrait orientation.',
                'preview' : 'Display a preview image of a hardcopy.',
                'x_resolution' : 'Set the width of raster-formatted images in pixels (0 implies current window size).',
                'y_resolution' : 'Set the height of raster-formatted images in pixels (0 implies current window size).',
                'dpi' : 'Set the DPI for EPS and Postscript files, specifies the resolution in dots per inch (DPI) instead of setting the width and height',
                'use_window_resolution' : "Use the currently active window's resolution for hardcopy (ignores the x-resolution and y-resolution in this case).",
                'set_standard_resolution' : 'Select from pre-defined resolution list.',
                'jpeg_hardcopy_quality' : 'To set jpeg hardcopy quality.',
            }

            class color_mode(metaclass=PyMenuMeta):
                __doc__ = 'Enter the hardcopy color mode menu.'
                doc_by_method = {
                    'color' : 'Plot hardcopies in color.',
                    'gray_scale' : 'Convert color to grayscale for hardcopy.',
                    'mono_chrome' : 'Convert color to monochrome (black and white) for hardcopy.',
                    'list' : 'Display the current hardcopy color mode.',
                }

            class driver(metaclass=PyMenuMeta):
                __doc__ = 'Enter the set hardcopy driver menu.'
                doc_by_method = {
                    'dump_window' : 'Set the command used to dump the graphics window to a file.',
                    'eps' : 'Produce encapsulated PostScript (EPS) output for hardcopies.',
                    'jpeg' : 'Produce JPEG output for hardcopies.',
                    'post_script' : 'Produce PostScript output for hardcopies.',
                    'ppm' : 'Produce PPM output for hardcopies.',
                    'tiff' : 'Use TIFF output for hardcopies.',
                    'png' : 'Use PNG output for hardcopies.',
                    'hsf' : 'Use HSF output for hardcopies.',
                    'avz' : 'Use AVZ output for hardcopies.',
                    'glb' : 'Use GLB output for hardcopies.',
                    'vrml' : 'Use VRML output for hardcopies.',
                    'list' : 'List the current hardcopy driver.',
                    'options' : 'Set the hardcopy options. Available options are:\n\\\\n               \t"no gamma correction", disables gamma correction of colors,\n\\\\n               \t"physical size = (width,height)", where width and height\n          are the actual measurements of the printable area of the page\n          in centimeters.\n\\\\n               \t"subscreen = (left,right,bottom,top)", where left,right,\n          bottom, and top are numbers in [-1,1] describing a subwindow on\n          the page in which to place the hardcopy.\n\n\\\\n          The options may be combined by separating them with commas.',
                }

                class post_format(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the PostScript driver format menu.'
                    doc_by_method = {
                        'fast_raster' : 'Use the new raster format.',
                        'raster' : 'Use the original raster format.',
                        'rle_raster' : 'Use the run-length encoded raster format.',
                        'vector' : 'Use vector format.',
                    }

        class windows(metaclass=PyMenuMeta):
            __doc__ = 'Enter the window options menu.'
            doc_by_method = {
                'aspect_ratio' : 'Set the aspect ratio of the active window.',
                'logo' : 'Enable/disable visibility of the logo in graphics window.',
                'ruler' : 'Enable/disable ruler visibility.',
                'logo_color' : 'Set logo color to white/black.',
            }

            class axes(metaclass=PyMenuMeta):
                __doc__ = 'Enter the axes window options menu.'
                doc_by_method = {
                    'border' : 'Enable/disable drawing of a border around the axes window.',
                    'bottom' : 'Set the bottom boundary of the axes window.',
                    'clear' : 'Set the transparency of the axes window.',
                    'right' : 'Set the right boundary of the axes window.',
                    'visible' : 'Enable/disable axes visibility.',
                }

            class main(metaclass=PyMenuMeta):
                __doc__ = 'Enter the main view window options menu.'
                doc_by_method = {
                    'border' : 'Enable/disable drawing of borders around the main viewing window.',
                    'bottom' : 'Set the bottom boundary of the main viewing window.',
                    'left' : 'Set the left boundary of the main viewing window.',
                    'right' : 'Set the right boundary of the main viewing window.',
                    'top' : 'Set the top boundary of the main viewing window.',
                    'visible' : 'Enable/disable visibility of the main viewing window.',
                }

            class scale(metaclass=PyMenuMeta):
                __doc__ = 'Enter the color scale window options menu.'
                doc_by_method = {
                    'border' : 'Enable/disable drawing of borders around the color scale window.',
                    'bottom' : 'Set the bottom boundary of the color scale window.',
                    'clear' : 'Set the transparency of the scale window.',
                    'format' : 'Set the number format of the color scale window (e.g. %0.2e).',
                    'font_size' : 'Set the font size of the color scale window.',
                    'left' : 'Set the left boundary of the color scale window.',
                    'margin' : 'Set the margin of the color scale window.',
                    'right' : 'Set the right boundary of the color scale window.',
                    'top' : 'Set the top boundary of the color scale window.',
                    'visible' : 'Enable/disable visibility of the color scale window.',
                    'alignment' : 'Set colormap to bottom/left/top/right',
                }

            class text(metaclass=PyMenuMeta):
                __doc__ = 'Enter the text window options menu.'
                doc_by_method = {
                    'application' : 'Enable/disable the application name in the picture.',
                    'border' : 'Enable/disable drawing of borders around the text window.',
                    'bottom' : 'Set the bottom boundary of the text window.',
                    'clear' : 'Enable/disable text window transparency.',
                    'company' : 'Enable/disable the company name in the picture.',
                    'date' : 'Enable/disable the date in the picture.',
                    'left' : 'Set the left boundary of the text window.',
                    'right' : 'Set the right boundary of the text window.',
                    'top' : 'Set the top boundary of the text window.',
                    'visible' : 'Enable/disable text window transparency.',
                }

            class video(metaclass=PyMenuMeta):
                __doc__ = 'Enter the video window options menu.'
                doc_by_method = {
                    'background' : 'Set the background color in the video picture.',
                    'color_filter' : 'Set the color filter options for the picture.',
                    'foreground' : 'Set the foreground color in the video picture.',
                    'on' : 'Enable/disable video picture settings.',
                    'pixel_size' : 'Set the window size in pixels.',
                }

            class xy(metaclass=PyMenuMeta):
                __doc__ = 'Enter the X-Y plot window options menu.'
                doc_by_method = {
                    'border' : 'Enable/disable drawing of a border around the X-Y plotter window.',
                    'bottom' : 'Set the bottom boundary of the X-Y plotter window.',
                    'left' : 'Set the left boundary of the X-Y plotter window.',
                    'right' : 'Set the right boundary of the X-Y plotter window.',
                    'top' : 'Set the top boundary of the X-Y plotter window.',
                    'visible' : 'Enable/disable X-Y plotter window visibility.',
                }

        class titles(metaclass=PyMenuMeta):
            __doc__ = 'Set problem title.'
            doc_by_method = {
                'left_top' : 'Set the title text for left top in title segment',
                'left_bottom' : 'Set the title text for left bottom in title segment',
                'right_top' : 'Set the title text for right top in title segment',
                'right_middle' : 'Set the title text for right middle in title segment',
                'right_bottom' : 'Set the title text for right bottom in title segment',
            }

        class views(metaclass=PyMenuMeta):
            __doc__ = 'Enter the view manipulation menu.'
            doc_by_method = {
                'auto_scale' : 'Scale and center the current scene.',
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

            class camera(metaclass=PyMenuMeta):
                __doc__ = 'Enter the camera menu to modify the current viewing parameters.'
                doc_by_method = {
                    'dolly_camera' : 'Adjust the camera position and target.',
                    'field' : 'Set the field of view (width and height).',
                    'orbit_camera' : 'Adjust the camera position without modifying the target.',
                    'pan_camera' : 'Adjust the camera target without modifying the position.',
                    'position' : 'Set the camera position.',
                    'projection' : 'Set the camera projection type.',
                    'roll_camera' : 'Adjust the camera up-vector.',
                    'target' : 'Set the point to be the center of the camera view.',
                    'up_vector' : 'Set the camera up-vector.',
                    'zoom_camera' : 'Adjust the camera field of view.',
                }

        class display_states(metaclass=PyMenuMeta):
            __doc__ = 'Enter the display state manipulation menu.'
            doc_by_method = {
                'list' : 'Print the names of the available display states to the console.',
                'apply' : 'Apply a display state to the active window.',
                'delete' : 'Delete a display state.',
                'use_active' : "Update an existing display state's settings to match those of the active graphics window.",
                'copy' : 'Create a new display state with settings copied from an existing display state.',
                'read' : 'Read display states from a file.',
                'write' : 'Write display states to a file.',
                'edit' : 'Edit a particular display state setting.',
                'create' : 'Create a new display state.',
            }

        class view_sync(metaclass=PyMenuMeta):
            __doc__ = 'Enter the display state manipulation menu.'
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
    __doc__ = 'Enter solution menu.'

    class calculation_activities(metaclass=PyMenuMeta):
        __doc__ = 'Enter calculation activities menu'

        class animate(metaclass=PyMenuMeta):
            __doc__ = 'Enter the animation menu.'

            class define(metaclass=PyMenuMeta):
                __doc__ = 'Enter the animation definition menu.'
                doc_by_method = {
                    'define_monitor' : 'Define new animation.',
                    'edit_monitor' : 'Change animation monitor attributes.',
                }

            class objects(metaclass=PyMenuMeta):
                __doc__ = 'Enter to define, edit, delete solution animation objects'
                doc_by_method = {
                    'create' : 'Create new graphics object.',
                    'edit' : 'Edit graphics object.',
                    'copy' : 'Copy graphics object.',
                    'delete' : 'Delete graphics object.',
                    'clear_history' : 'Clear object history.',
                }

        class auto_save(metaclass=PyMenuMeta):
            __doc__ = 'Enter the auto save menu.'
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
            __doc__ = 'Manage Cell Register Operations'
            doc_by_method = {
                'add' : 'Add a new object',
                'edit' : 'Edit an object',
                'delete' : 'Delete an object',
                'list' : 'List objects',
                'list_properties' : 'List properties of an object',
            }

        class execute_commands(metaclass=PyMenuMeta):
            __doc__ = 'Enter the execute-monitor-commands menu.'
            doc_by_method = {
                'add_edit' : 'Add or edit execute-commands.',
                'enable' : 'Enable an execute-command.',
                'disable' : 'Disable an execute-command.',
            }

        class solution_strategy(metaclass=PyMenuMeta):
            __doc__ = 'Enter the automatic initialization and case modification strategy menu'
            doc_by_method = {
                'enable_strategy' : 'Specify whether automatic initialization and case modification should be enabled',
                'execute_strategy' : 'Execute the automatic initialization and case modification strategy defined at present',
                'continue_strategy_execution' : 'Continue execution of the automatic initialization and case modification strategy defined at present',
                'automatic_initialization' : 'Define how the case is to be initialized automatically.',
            }

            class automatic_case_modification(metaclass=PyMenuMeta):
                __doc__ = 'Define how the case is to be modified as the solution progresses.'
                doc_by_method = {
                    'before_init_modification' : 'Specify modification to be performed before initialization',
                    'original_settings' : 'Specify modification to be performed after initialization to restore to original settings',
                    'modifications' : 'Specify modifications to be performed during solution',
                }

    class cell_registers(metaclass=PyMenuMeta):
        __doc__ = 'Manage Cell Registers'
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
        __doc__ = 'Enter the controls menu.'
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
            __doc__ = 'Enter menu for acoustics wave equation solver controls.'
            doc_by_method = {
                'relative_convergence_criterion' : 'Specify convergence tolerance for the timestep iterations\nas the target residual reduction factor.',
                'max_iterations_per_timestep' : 'Specify maximum number of iterations per timestep.',
            }

            class expert(metaclass=PyMenuMeta):
                __doc__ = 'Enter menu for expert controls.'
                doc_by_method = {
                    'under_relaxation_factor' : 'Specify under-relaxation factor to be used in \nthe diagonal matrix elements of implicit solver.',
                    'explicit_relaxation_factor' : 'Specify explicit relaxation factor to be applied to\nthe solution correction when updating solution in the timestep iterations.',
                }

        class advanced(metaclass=PyMenuMeta):
            __doc__ = 'Controls advanced options'
            doc_by_method = {
                'correction_tolerance' : 'Enter the correction tolerance menu.',
                'multi_grid_amg' : 'Set the parameters that govern the algebraic multigrid procedure.',
                'multi_grid_controls' : 'Enter the multi-grid-controls menu.',
                'multi_grid_fas' : 'Set the coefficients that govern the FAS multigrid procedure.',
                'multi_stage' : 'Set the multiple-stage time stepping scheme coefficients.',
                'relaxation_method' : 'Set the solver relaxation method.',
                'slope_limiter_set' : 'Enter the slope limiter set menu.',
            }

            class amg_options(metaclass=PyMenuMeta):
                __doc__ = 'Enter AMG options menu.'
                doc_by_method = {
                    'laplace_coarsening' : 'Set AMG laplace coarsening options.',
                    'conservative_amg_coarsening' : 'Use conservative AMG coarsening?',
                    'aggressive_amg_coarsening' : 'Use aggressive AMG coarsening.',
                    'amg_gpgpu_options' : 'Set GPGPU AMG solver options.',
                }

            class fast_transient_settings(metaclass=PyMenuMeta):
                __doc__ = 'Enter the fast transient settings menu.'
                doc_by_method = {
                    'rk2' : 'Enable the use of a two-stage Runge-Kutta scheme for time integration.',
                }

        class contact_solution_controls(metaclass=PyMenuMeta):
            __doc__ = 'solver controls for contact marks method'
            doc_by_method = {
                'solution_stabilization' : 'Automatic solver settings adjustment for solution stabilization during contact process',
                'set_settings_to_default' : 'set contact solution stabilization to default',
                'verbosity' : 'specify verbosity level for contact solution controls',
            }

            class parameters(metaclass=PyMenuMeta):
                __doc__ = 'parameters used in stabilization strategy'
                doc_by_method = {
                    'iterations' : 'specify additional iterations to accomodate contact solution stabilization',
                    'solution_stabilization_persistence' : 'persistence of the solution stabilization based on events [0-contact based, 1-always on]',
                    'persistence_fixed_time_steps' : 'specify fixed time-steps for solution stabilization persistence after trigger',
                    'persistence_fixed_duration' : 'specify fixed time for solution stabilization persistence after trigger',
                    'extrapolation_method' : 'solution extrapolation method for cells changing status from contact to non-contact [0-none, 1-local extrapolation]',
                }

            class spatial(metaclass=PyMenuMeta):
                __doc__ = 'spatial discretization control options'
                doc_by_method = {
                    'first_to_second_order_blending' : 'Set factor to control first order to second order blending',
                    'first_to_second_order_blending_list' : 'list set factor to control first order to second order blending',
                    'scheme' : 'Set advection scheme for contact event stability',
                    'flow_skew_diffusion_exclude' : 'Exclude skew diffusion discretization contribution for momentum',
                    'scalars_skew_diffusion_exclude' : 'Exclude skew diffusion discretization contribution for scalars',
                    'rhie_chow_flux_specify' : 'Allow specification of the the rhie-chow flux method',
                    'rhie_chow_method' : 'Enter the rhie-chow flux method',
                }

            class transient(metaclass=PyMenuMeta):
                __doc__ = 'transient discretization control options '
                doc_by_method = {
                    'transient_parameters_specify' : 'Allow transient parameter specification',
                    'transient_scheme' : 'Specify temporal scheme to be used',
                    'time_scale_modification_method' : 'Enter time scale modification method',
                    'time_scale_modification_factor' : 'Specify time-scale modification factor',
                }

            class amg(metaclass=PyMenuMeta):
                __doc__ = 'AMG control options'
                doc_by_method = {
                    'enforce_laplace_coarsening' : 'enforce the use of laplace coarsening in AMG',
                    'increase_pre_sweeps' : 'allow increase in AMG pre-sweep',
                    'pre_sweeps' : 'specify the number of AMG pre-sweeps',
                    'specify_coarsening_rate' : 'modify AMG coarsening rate',
                    'coarsen_rate' : 'specify AMG coarsening rate',
                }

            class models(metaclass=PyMenuMeta):
                __doc__ = 'model control options'
                doc_by_method = {
                    'model_ramping' : 'Activate model ramping for solver stability and accuracy',
                    'ramp_flow' : 'ramp flow for solver stability and accuracy',
                    'ramp_turbulence' : 'ramp turbulence for solver stability and accuracy',
                    'ramp_scalars' : 'ramp all scalar transport equations for solver stability and accuracy',
                }

            class methods(metaclass=PyMenuMeta):
                __doc__ = 'methods control options'
                doc_by_method = {
                    'pressure_velocity_coupling_controls' : 'enable pressure-velocity coupling method change for solver stability and accuracy',
                    'pressure_velocity_coupling_method' : 'specify pressure-velocity coupling method change for solver stability and accuracy',
                    'gradient_controls' : 'modify gradient method for solver stability and accuracy',
                    'specify_gradient_method' : 'specify gradient method for solver stability and accuracy',
                }

            class miscellaneous(metaclass=PyMenuMeta):
                __doc__ = 'miscellaneous'
                doc_by_method = {
                    'compute_statistics' : 'compute solution statistics for contact updates',
                    'statistics_level' : 'solution statistics level for contact updates',
                }

        class query(metaclass=PyMenuMeta):
            __doc__ = 'Enter controls query menu.'
            doc_by_method = {
                'courant_number' : 'Get the fine mesh Courant number (time step factor).',
                'equations' : 'Enter the equations menu.',
                'limits' : 'Get solver limits for the values of various solution variables.',
                'p_v_controls' : 'Get P-V-Controls.',
                'relaxation_factor' : 'Enter the relaxation-factor menu.',
                'under_relaxation' : 'Enter under relaxation menu.',
            }

            class acoustics_wave_equation_controls(metaclass=PyMenuMeta):
                __doc__ = 'Enter menu for acoustics wave equation solver controls.'
                doc_by_method = {
                    'relative_convergence_criterion' : 'Specify convergence tolerance for the timestep iterations\nas the target residual reduction factor.',
                    'max_iterations_per_timestep' : 'Specify maximum number of iterations per timestep.',
                }

                class expert(metaclass=PyMenuMeta):
                    __doc__ = 'Enter menu for expert controls.'
                    doc_by_method = {
                        'under_relaxation_factor' : 'Specify under-relaxation factor to be used in \nthe diagonal matrix elements of implicit solver.',
                        'explicit_relaxation_factor' : 'Specify explicit relaxation factor to be applied to\nthe solution correction when updating solution in the timestep iterations.',
                    }

            class advanced(metaclass=PyMenuMeta):
                __doc__ = 'Controls advanced options'
                doc_by_method = {
                    'correction_tolerance' : 'Enter the correction tolerance menu.',
                    'multi_grid_amg' : 'Get the parameters that govern the algebraic multigrid procedure.',
                    'multi_grid_controls' : 'Enter the multi-grid-controls menu.',
                    'multi_grid_fas' : 'Get the coefficients that govern the FAS multigrid procedure.',
                    'multi_stage' : 'Set the multiple-stage time stepping scheme coefficients.',
                    'relaxation_method' : 'Set the solver relaxation method.',
                }

                class amg_options(metaclass=PyMenuMeta):
                    __doc__ = 'Enter AMG options menu.'
                    doc_by_method = {
                        'laplace_coarsening' : 'Get AMG laplace coarsening options.',
                        'conservative_amg_coarsening' : 'Use conservative AMG coarsening?',
                        'aggressive_amg_coarsening' : 'Use aggressive AMG coarsening.',
                        'amg_gpgpu_options' : 'amg gpu options',
                    }

    class expert(metaclass=PyMenuMeta):
        __doc__ = 'Enter expert options for solution'
        doc_by_method = {
            'alternate_wall_temp_formulation' : 'Alternate formulation for wall temperatures?',
            'bc_pressure_extrapolations' : 'Setting pressure extrapolations schemes on boundaries.',
            'bcd_boundedness' : 'BCD scheme boundedness strength, constant or expression (0 to 1)',
            'bcd_weights_freeze' : 'At each timestep, freeze BCD scheme weights after specified iteration\nin order to improve timestep convergence.',
            'correction_form' : 'Discretize momentum equations in correction form for the pressure-based solver.',
            'disable_reconstruction' : 'Enable/Disable reconstruction. When disabled, accuracy will be first-order.',
            'energy_numerical_noise_filter' : 'The energy equation numerical noise filter can be enabled to eliminate non-physical numerical noise in the energy field.\n     The numerical noise can appear in solution fields where large variations in specific heat or combustion with phase change are present.\n     Using the energy equation numerical noise filter increases robustness, but may make the solution slightly more diffusive.',
            'explicit_under_relaxation_value' : 'Explicit under-relaxation value.',
            'equation_ordering' : 'Set the equation order',
            'flow_warnings' : 'Control the display of warning diagnostics for boundaries with reversed flow, etc.',
            'limiter_warnings' : 'Control the display of limiter warning diagnostics.',
            'linearized_mass_transfer_udf' : 'Use linearized mass transfer UDFs?',
            'lock_solid_temperature' : 'Lock the temperature for all solid and shell cell zones in the domain.',
            'material_property_warnings' : 'Control the display of material property warning diagnostics:\n 0 - off (no messages)\n 1 - messages per material\n 2 - messages per material and per property',
            'mp_mfluid_aniso_drag' : 'Set anisotropic drag parameters for Eulerian multiphase.',
            'mp_reference_density' : 'Set reference density option for Eulerian multiphase.',
            'numerical_beach_controls' : 'Set damping function in flow direction',
            'open_channel_controls' : '\nSet additional open channel controls',
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
            __doc__ = 'Enter the divergence prevention menu.'
            doc_by_method = {
                'enable' : 'Enable divergence prevention.',
            }

        class high_speed_numerics(metaclass=PyMenuMeta):
            __doc__ = 'Enter high-speed-numerics menu'
            doc_by_method = {
                'enable' : 'Enable/disable high-speed-numerics.',
                'expert' : 'expert high-speed-numerics.',
                'visualize_pressure_discontinuity_sensor' : 'Enable/disable pressure-discontinuity-sensor visualization.',
            }

        class poor_mesh_numerics(metaclass=PyMenuMeta):
            __doc__ = 'Enter Poor Mesh Numerics Menu.'
            doc_by_method = {
                'enable' : 'Solution correction on meshes of poor quality.',
                'cell_quality_based' : 'Enable/disable poor mesh numerics on cells with low quality.',
                'set_quality_threshold' : 'Set quality threshold.',
                'solution_and_quality_based' : 'Enable/disable poor mesh numerics based on solution and cell quality.',
                'gradient_quality_based' : 'Enable/disable poor mesh numerics based on cell gradient quality.',
                'orthogonality_enhancing_cell_centroids' : 'Relocate select cell centroids, to improve orthogonality metrics and solution stability.',
                'user_defined_on_register' : 'Include cells in register in poor mesh numerics.',
                'reset_poor_elements' : 'Reset marking of poor cell elements.',
                'print_poor_elements_count' : 'Print poor cells count.',
                'enhanced_pmn' : 'This option is available with the density-based solver. When enabled, it will apply quality-based poor-mesh-numerics order=1 on any cells with a quality-measure below 0.2. In addition, their CFL number is limited to 1.0.',
            }

            class solution_based_pmn(metaclass=PyMenuMeta):
                __doc__ = 'Solution based poor-mesh numerics menu'
                doc_by_method = {
                    'enable' : 'Enable solution based treatment',
                    'mark_primary_solution_limits' : 'Mark cells violating solution limits',
                    'mark_velocity_limit' : 'Mark cells exceeding velocity limit',
                    'mark_cfl_limit' : 'Mark cells exceeding cfl limit',
                    'mark_cfl_jump' : 'Mark cells exceeding cfl jump in neighborhood',
                }

        class previous_defaults(metaclass=PyMenuMeta):
            __doc__ = 'Enter previous defaults menu.'
            doc_by_method = {
                'undo_r19_point_0_default_changes' : 'Undo default changes introduced in R19.0.',
                'undo_2019r1_default_changes' : 'Undo default changes introduced in 2019R1.',
                'undo_2019r3_default_changes' : 'Undo default changes introduced in 2019R3.',
                'undo_2021r1_default_changes' : 'Undo default changes introduced in 2021R1.',
                'undo_2021r2_default_changes' : 'Undo default changes introduced in 2021R2.',
                'undo_2022r1_default_changes' : 'Undo default changes introduced in 2022R1.',
            }

        class non_reflecting_boundary_treatment(metaclass=PyMenuMeta):
            __doc__ = 'Enter non reflecting boundary treatment using minimal pressure reflection approach menu.'
            doc_by_method = {
                'pressure_inlet' : 'Enabling the use of minimal pressure reflection treatment. This treatment will minimize pressure wave reflections from the boundaries on which this option is active, but not necessarily fully eliminating them. The reflections would be of an acceptable limit in order to not contaminate the solution, the simulation will gain from the robustness of the new algorithm compared to traditional non-reflecting boundary condition treatment.',
                'pressure_outlet' : 'Enabling the use of minimal pressure reflection treatment. This treatment will minimize pressure wave reflections from the boundaries on which this option is active, but not necessarily fully eliminating them. The reflections would be of an acceptable limit in order to not contaminate the solution, the simulation will gain from the robustness of the new algorithm compared to traditional non-reflecting boundary condition treatment.',
                'velocity_inlet' : 'Enabling the use of minimal pressure reflection treatment. This treatment will minimize pressure wave reflections from the boundaries on which this option is active, but not necessarily fully eliminating them. The reflections would be of an acceptable limit in order to not contaminate the solution, the simulation will gain from the robustness of the new algorithm compared to traditional non-reflecting boundary condition treatment.',
            }

        class open_channel_wave_options(metaclass=PyMenuMeta):
            __doc__ = 'Enter the open-channel-wave-options menu'
            doc_by_method = {
                'set_verbosity' : 'set open channel wave verbosity',
                'stokes_wave_variants' : 'set stokes wave theory variants',
                'set_buffer_layer_ht' : 'set bufer layer height between phases for segregated velocity inputs',
            }

        class secondary_gradient_limiting(metaclass=PyMenuMeta):
            __doc__ = 'Enter the Secondary Gradient Limiting Menu.'
            doc_by_method = {
                'energy' : 'Enable/disable secondary gradient limiting at coupled walls for energy equation.',
                'uds' : 'Enable/disable secondary gradient limiting at coupled walls for user-defined scalars.',
                'mesh_quality_limits' : 'Specify minimum and maximum mesh quality limits.',
            }

    class initialize(metaclass=PyMenuMeta):
        __doc__ = 'Enter the flow initialization menu.'
        doc_by_method = {
            'open_channel_auto_init' : 'Open channel automatic initialization.',
            'levelset_auto_init' : 'Levelset function automatic initialization.',
            'dpm_reset' : 'Reset discrete phase source terms to zero.',
            'lwf_initialization' : 'Delete wall film particles and initialize wall film variables to zero.',
            'initialize_flow' : 'Initialize the flow field with the current default values.',
            'init_acoustics_options' : 'Specify number of timesteps for ramping of sources\nand initialize acoustics model variables.\nDuring ramping the sound sources are multiplied by a factor smoothly growing from 0 to 1.',
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
            __doc__ = 'Enter the compute defaults menu.'
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
            __doc__ = 'Localized initialization of turbulent flow variables for VOF/Mixture multiphase flow models'
            doc_by_method = {
                'enable' : 'localized initialization of turbulent flow variables for VOF/Mixture multiphase flow models',
                'turb_init_parameters' : 'turbulent flow parameters for localized initialization',
            }

        class vof_patch_smooth_options(metaclass=PyMenuMeta):
            __doc__ = 'Enter the vof patch/smooth options menu'
            doc_by_method = {
                'set_options' : 'Patch and smoothing options for volume fraction',
                'execute_smoothing' : 'Execute volumetric smoothing for volume fraction',
            }

        class set_fmg_options(metaclass=PyMenuMeta):
            __doc__ = 'Enter the full-multigrid option menu.'
            doc_by_method = {
                'enable_viscous_terms' : 'Enable viscous terms during FMG initialization',
                'set_turbulent_viscosity_ratio' : 'Set turbulent viscosity ratio used during FMG initialization',
            }

        class set_hyb_initialization(metaclass=PyMenuMeta):
            __doc__ = 'Enter the settings for hybrid initialization method.'
            doc_by_method = {
                'general_settings' : 'Enter the general settings menu.',
                'turbulent_settings' : 'Enter the turbulent settings menu.',
                'species_settings' : 'Enter the species settings menu.',
            }

    class methods(metaclass=PyMenuMeta):
        __doc__ = 'Enter the methods menu.'
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
            __doc__ = 'Enter expert menu.'
            doc_by_method = {
                'reactions' : 'Enable/disable the species reaction sources and set relaxation factor.',
                'numerics' : 'Set numeric options.',
            }

        class high_order_term_relaxation(metaclass=PyMenuMeta):
            __doc__ = 'Enter High Order Relaxation Menu'
            doc_by_method = {
                'enable' : 'Enable/Disable High Order Term Relaxation.',
            }

            class options(metaclass=PyMenuMeta):
                __doc__ = 'High Order Term Relaxation Options'
                doc_by_method = {
                    'relaxation_factor' : 'sets relaxation factor',
                }

                class variables(metaclass=PyMenuMeta):
                    __doc__ = 'Select Variables'
                    doc_by_method = {
                        'select' : 'select variables for high order term relaxation',
                    }

        class multiphase_numerics(metaclass=PyMenuMeta):
            __doc__ = 'Enter the multiphase numerics options menu'

            class porous_media(metaclass=PyMenuMeta):
                __doc__ = 'multiphase relative permeability numerics menu'
                doc_by_method = {
                    'relative_permeability' : 'multiphase relative permeability fix option',
                }

            class compressible_flow(metaclass=PyMenuMeta):
                __doc__ = 'multiphase compressible numerics options menu'
                doc_by_method = {
                    'enhanced_numerics' : 'multiphase enhanced compressible flow numerics options',
                    'alternate_bc_formulation' : 'multiphase compressible flow BC alternate method',
                }

            class boiling_parameters(metaclass=PyMenuMeta):
                __doc__ = 'multiphase boiling parameters menu'
                doc_by_method = {
                    'thin_film' : 'multiphase boiling thin film effects',
                    'liquid_vof_factor' : 'multiphase boiling liquid volume fraction effects',
                }

            class viscous_flow(metaclass=PyMenuMeta):
                __doc__ = 'multiphase viscous flow numerics options menu'
                doc_by_method = {
                    'viscosity_averaging' : 'multiphase options for viscosity averaging',
                    'turb_visc_based_damping' : 'turbulence viscosity based damping controls',
                    'interfacial_artificial_viscosity' : 'interfacial artifical viscosity controls',
                }

            class heat_mass_transfer(metaclass=PyMenuMeta):
                __doc__ = 'multiphase interphase heat and mass transfer numerics options menu'
                doc_by_method = {
                    'alternative_energy_treatment' : 'Alternative treatment of latent heat source due to mass transfer.',
                }

                class cavitation(metaclass=PyMenuMeta):
                    __doc__ = 'cavitation numerics options menu'
                    doc_by_method = {
                        'schnerr_evap_coeff' : 'evaporation coefficient for Schnerr-Sauer model',
                        'schnerr_cond_coeff' : 'condensation coefficient for Schnerr-Sauer model',
                        'max_vapor_pressure_ratio' : 'Maximum limit on vapor pressure after turbulence and thermal correction',
                        'min_vapor_pressure' : 'minimum vapor pressure limit for cavitation model',
                        'display_clipped_pressure' : 'Clipped pressure is just used for the properties evaluation. Mass Transfer Rate uses unclipped pressure.',
                        'turbulent_diffusion' : 'Enable/disable turbulent diffusion treatment between phases participating in cavitation.\nThis treatment is generally recommended for better solution stability.\nHowever, in case of numerical difficulties, it can be disabled.',
                    }

                class evaporation_condensation(metaclass=PyMenuMeta):
                    __doc__ = 'evaporation-condensation advanced options menu'
                    doc_by_method = {
                        'vof_from_min_limit' : 'minimum volume fraction below which mass transfer rate is set to zero',
                        'vof_from_max_limit' : 'maximum volume fraction above which mass transfer rate is set to zero',
                        'vof_to_min_limit' : 'minimum volume fraction below which mass transfer rate is set to zero',
                        'vof_to_max_limit' : 'maximum volume fraction above which mass transfer rate is set to zero',
                        'ia_norm_min_limit' : 'minimum normalized area density below which mass transfer rate is set to zero',
                        'max_rel_humidity' : 'maximum value of relative humidity to limit condensation rate',
                    }

                class boiling(metaclass=PyMenuMeta):
                    __doc__ = 'boiling advanced options menu'
                    doc_by_method = {
                        'heat_flux_relaxation_factor' : 'under-relaxation factor for boiling heat flux',
                        'show_expert_options' : 'exposes expert options of min/max superheat along with wetting fraction controls',
                        'two_resistance_boiling_framework' : 'Allow generalized two-resistance framework for boiling model',
                    }

                class area_density(metaclass=PyMenuMeta):
                    __doc__ = 'interfacial area density menu'
                    doc_by_method = {
                        'vof_min_seeding' : 'minimum vof seeding for non-zero area density in heat and mass transfer',
                        'ia_grad_sym' : 'Interfacial area density gradient-symmetric mechanism',
                    }

            class advanced_stability_controls(metaclass=PyMenuMeta):
                __doc__ = 'Stability controls for multiphase flow'

                class pseudo_transient(metaclass=PyMenuMeta):
                    __doc__ = 'Pseudo-Transient stability controls for multiphase flow'
                    doc_by_method = {
                        'smoothed_density_stabilization_method' : 'Set smoothed density stabilization method',
                        'false_time_step_linearization' : 'Set false time-step linearization for added stability',
                    }

                class p_v_coupling(metaclass=PyMenuMeta):
                    __doc__ = 'Pressure velocity coupling controls for multiphase flow'

                    class coupled_vof(metaclass=PyMenuMeta):
                        __doc__ = 'Set Coupled VOF stability controls'
                        doc_by_method = {
                            'buoyancy_force_linearization' : 'Set buoynacy force linerization options in coupled vof',
                        }

                    class rhie_chow_flux(metaclass=PyMenuMeta):
                        __doc__ = 'Set Rhie-Chow related stability controls'
                        doc_by_method = {
                            'low_order_rhie_chow' : 'Use low order velocity interpolation in flux calculation',
                        }

                    class skewness_correction(metaclass=PyMenuMeta):
                        __doc__ = 'Skewness correction related stabiity controls for multiphase flow'
                        doc_by_method = {
                            'limit_pressure_correction_gradient' : 'Use limited pressure correction gradient in skewness corrections for better stability',
                        }

                class hybrid_nita(metaclass=PyMenuMeta):
                    __doc__ = 'Hybrid NITA stability controls for multiphase flow'
                    doc_by_method = {
                        'outer_iterations' : 'Set number of outer iterations in hybrid nita',
                        'initial_outer_iterations' : 'Set hybrid nita start-up controls',
                    }

                    class instability_detector(metaclass=PyMenuMeta):
                        __doc__ = 'Set Hybrid NITA instability detector controls'
                        doc_by_method = {
                            'enable_instability_detector' : 'Enable instability detector for better stability',
                            'set_cfl_limit' : 'Set Courant Number limit for detection of unstable event',
                            'set_cfl_type' : 'Set Courant Number type for detection of unstable event',
                            'set_velocity_limit' : 'Set velocity limit for detection of unstable event',
                            'unstable_event_outer_iterations' : 'Set number of outer iterations for unstable event',
                        }

                class equation_order(metaclass=PyMenuMeta):
                    __doc__ = 'Equation Order Menu for Homogeneous Multiphase Flow Models'
                    doc_by_method = {
                        'solve_flow_last' : 'Solve flow equation at the end of iteration as an alternative',
                        'solve_exp_vof_at_end' : 'Solve Explicit VOF at the end of time-step as an alternative',
                    }

                class anti_diffusion(metaclass=PyMenuMeta):
                    __doc__ = 'Anti Diffusion Menu for VOF/Multi-Fluid VOF Models'
                    doc_by_method = {
                        'enable_dynamic_strength' : 'Enable dynamic strength to reduce compression in the tangential direction to the interface',
                        'set_dynamic_strength_exponent' : 'Set cosine exponent in dynamic strength treatment',
                        'set_maximum_dynamic_strength' : 'Set maximum value of dynamic anti-diffusion strength',
                    }

            class default_controls(metaclass=PyMenuMeta):
                __doc__ = 'Multiphase default controls menu'
                doc_by_method = {
                    'recommended_defaults_for_existing_cases' : 'Activate multiphase defaults for loaded case',
                    'revert_to_pre_r20_point_1_default_settings' : 'Revert to pre-R20.1 multiphase flow default settings',
                }

            class face_pressure_controls(metaclass=PyMenuMeta):
                __doc__ = 'Enter the face pressure expert controls menu'
                doc_by_method = {
                    'face_pressure_options' : 'set face pressure options',
                }

            class solution_stabilization(metaclass=PyMenuMeta):
                __doc__ = 'VOF solution stabilization menu'
                doc_by_method = {
                    'execute_settings_optimization' : 'Execute optimized settings for VOF',
                    'execute_advanced_stabilization' : 'Execute advanced stabilization for VOF',
                    'execute_additional_stability_controls' : 'Execute additional stability controls for VOF',
                }

                class additional_stabilization_controls(metaclass=PyMenuMeta):
                    __doc__ = 'Additional advanced stability controls for VOF'
                    doc_by_method = {
                        'blended_compressive_scheme' : 'Blended Compressive discretization scheme for VOF',
                        'pseudo_transient_stabilization' : 'Pseudo-Transient Momentum stabilization and False Time Step Linearization methods for VOF',
                    }

                class velocity_limiting_treatment(metaclass=PyMenuMeta):
                    __doc__ = 'Velocity limiting related stabiity controls for VOF'
                    doc_by_method = {
                        'enable_velocity_limiting' : 'Enable velocity limiting treatment',
                        'set_velocity_and_vof_cutoffs' : 'Set phase based velocity limiting controls.',
                        'set_damping_strengths' : 'Set phase based damping strength.',
                        'set_velocity_cutoff' : 'Enter max velocity magnitude.',
                        'set_damping_strength' : 'Enter damping strength.',
                        'verbosity' : 'Enable verbosity to print number of velocity limited cells during iterations.',
                    }

        class nita_expert_controls(metaclass=PyMenuMeta):
            __doc__ = 'Enter the nita expert controls menu'
            doc_by_method = {
                'set_verbosity' : 'set nita verbosity option',
                'skewness_neighbor_coupling' : 'set skewness neighbor coupling for nita',
                'hybrid_nita_settings' : 'Select a hybrid NITA settings option for faster performance and better robustness.',
            }

        class overset(metaclass=PyMenuMeta):
            __doc__ = 'Enter overset solver options menu.'
            doc_by_method = {
                'high_order_pressure' : 'High order pressure extrapolation at overset interface',
                'interpolation_method' : 'Choose the interpolation method for overset interface(s)',
                'orphan_cell_treatment' : 'Enable solver to run with orphans present',
            }

            class expert(metaclass=PyMenuMeta):
                __doc__ = 'Enter overset expert solver options menu'
                doc_by_method = {
                    'mass_flux_correction_method' : 'Enter mass flux correction option at overset interfaces.',
                    'hybrid_mode_selection' : 'mode for hybrid interpolation',
                }

        class pseudo_time_method(metaclass=PyMenuMeta):
            __doc__ = 'Enter the pseudo time method menu.'
            doc_by_method = {
                'formulation' : 'Select the pseudo time step size formulation for the pseudo time method.',
                'local_time_step_settings' : 'Adjust the settings for the local time step formulation.',
                'global_time_step_settings' : 'Adjust the settings for the global time step formulation.',
                'advanced_options' : 'Enter the advanced options menu to define pseudo time settings for equations.',
                'relaxation_factors' : 'Enter the relaxation factors menu to set the pseudo time explicit relaxation factors for equations.',
                'verbosity' : 'Set the verbosity for the pseudo time method.',
            }

        class query(metaclass=PyMenuMeta):
            __doc__ = 'Enter methods query menu.'
            doc_by_method = {
                'discretization_scheme' : 'Enter the discretization-scheme menu.',
                'p_v_coupling' : 'Get the pressure velocity coupling scheme.',
            }

        class warped_face_gradient_correction(metaclass=PyMenuMeta):
            __doc__ = 'Enter warped-face-gradient-correction menu.'
            doc_by_method = {
                'enable' : 'Enable Warped-Face Gradient Correction.',
                'turbulence_options' : 'Set turbulence Warped Face Gradient Correction',
            }

    class monitors(metaclass=PyMenuMeta):
        __doc__ = 'Enter the monitors menu.'
        doc_by_method = {
            'convergence_conditions' : 'Manage convergence report',
            'set_average_over' : 'Set the average over input for monitors.',
        }

        class _(metaclass=PyMenuMeta):
            __doc__ = 'Enter the convergence menu to add surface, volume, drag, lift and moment monitors to convergence criteria.'
            doc_by_method = {
                'add_edit' : 'Add or edit convergence criterion for surface, volume, drag, lift and moment monitors.',
                'frequency' : 'To set how often convergence checks are done with respect to iterations or time steps.',
                'list' : 'List defined convergence criteria for monitors.',
                'condition' : 'Option to stop the calculations. All convergence conditions are met or any convergence condition is met.',
                'average_over_last_n_iterations_timesteps' : 'Option to average over previous values for checking convergence.',
                'delete' : 'Delete a monitor from convergence criteria.',
            }

        class __(metaclass=PyMenuMeta):
            __doc__ = 'Enter the statistic monitors menu.'
            doc_by_method = {
                'monitors' : 'Choose which statistics to monitor as printed and/or plotted output.',
                'plot' : 'Enable/disable plotting of statistics during iteration.',
                'print' : 'Enable/disable printing of statistics during iteration.',
                'write' : 'Enable/disable writing of statistics during iteration.',
                'window' : 'Specify first window in which statistics will be plotted during iteration.\nMultiple statistics are plotted in separate windows, beginning with this one.',
                'file_basename' : 'Specify the file basename and extension. The name of the individual monitor will be insterted automatically.',
                'x_axis' : 'Choose what quantity to use on the abscissa in the plot and in the data written to files.',
            }

        class report_files(metaclass=PyMenuMeta):
            __doc__ = 'Manage report files'
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
            __doc__ = 'Manage report plots'
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
            __doc__ = 'Enter the residual monitors menu.'
            doc_by_method = {
                'check_convergence' : 'Choose which currently-monitored residuals\nshould be checked for convergence.',
                'convergence_criteria' : 'Set convergence criteria for residuals which are\ncurrently being both monitored and checked.',
                'criterion_type' : 'Set convergence criterion type',
                'monitor' : 'Choose which residuals to monitor as printed and/or plotted output.',
                'enhanced_continuity_residual' : 'Scale the continuity residuals locally based on the enhanced formulation.',
                'n_display' : 'Set the number of most recent residuals to display in plots.',
                'n_maximize_norms' : 'Set the number of iterations through which normalization\nfactors will be maximized.',
                'normalization_factors' : 'Set normalization factors for currently-monitored residuals.',
                'normalize' : 'Choose whether or not to normalize residuals in printed and plotted output.',
                'n_save' : 'Set number of residuals to be saved with data.\nHistory is automatically compacted when buffer becomes full.',
                'plot' : 'Choose whether or not residuals will be plotted during iteration.',
                'print' : 'Choose whether or not residuals will be printed during iteration.',
                'relative_conv_criteria' : 'Set relative convergence criteria for residuals which are\ncurrently being both monitored and checked.',
                're_normalize' : 'Renormalize residuals by maximum values.',
                'reset' : 'Delete the residual history and reset iteration counter to unity.',
                'scale_by_coefficient' : 'Enable/disable scaling of residuals by coefficient sum in printed and plotted output.',
            }

    class report_definitions(metaclass=PyMenuMeta):
        __doc__ = 'Manage report definitions.'
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
        __doc__ = 'Enter run calculation menu'
        doc_by_method = {
            'adaptive_time_stepping' : 'Set Error-based adaptive time-stepping parameters.',
            'cfl_based_adaptive_time_stepping' : 'Set CFL-based adaptive time-stepping parameters.',
            'data_sampling' : 'Set iteration options.',
            'dual_time_iterate' : 'Perform unsteady iterations.\nArguments:\n  number_of_total_periods: int\n  number_of_time_steps: int\n  total_number_of_time_steps: int\n  total_time: float\n  incremental_time: float\n  maximum_number_of_iterations_per_time_step: int\n',
            'iterate' : 'Perform a specified number of iterations.\nArguments:\n  number_of_iterations: int\n',
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
            __doc__ = 'data sampling options for statistics'
            doc_by_method = {
                'add_datasets' : 'Add a dataset. After providing the zones for a dataset, press [Enter] to move onto selecting quantities. Enter () to complete the quantity selection for this dataset.',
                'add_rtdft_datasets' : 'Add a dataset. After providing the zones for a dataset, press [Enter] to move onto selecting quantities. Enter () to complete the quantity selection for this dataset.',
                'remove_dataset' : 'remove dataset',
                'list_datasets' : 'list dataset',
            }

        class transient_controls(metaclass=PyMenuMeta):
            __doc__ = 'Enter into the transient controls menu.'
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
                'udf_based_time_stepping' : 'Set the time-stepping parameters for user-defined time stepping method.',
                'error_based_time_stepping' : 'Set Error-based adaptive time-stepping parameters.',
                'undo_timestep' : 'Undo the previous time step.',
                'predict_next_time' : 'Applies a predictor algorithm for computing initial condition at time step n+1.',
                'rotating_mesh_flow_predictor' : 'Improve prediction of flow field at time step n+1 for rotating mesh.',
                'solid_time_step_size' : 'Specify a different time step size for solid zones.',
                'time_step_size_for_acoustic_export' : 'Set number of time step size for acoustic export.',
            }

            class multiphase_specific_time_constraints(metaclass=PyMenuMeta):
                __doc__ = 'Set Multiphase-specific time constraints.'
                doc_by_method = {
                    'moving_mesh_cfl_constraint' : 'Enable time step size constraints based on moving mesh courant number',
                    'physics_based_constraint' : 'Include physics driven time-step constraints',
                    'verbosity' : 'Set verbosity to print multiphase specific time scales.',
                }

                class time_scale_options(metaclass=PyMenuMeta):
                    __doc__ = 'Set physics based time scale options'
                    doc_by_method = {
                        'viscous_scale' : 'Include viscous time scale',
                        'gravity_scale' : 'Include gravity based time scale',
                        'surface_tension_scale' : 'Include surface tension based time scale',
                        'acoustic_scale' : 'Include acoustic time scale',
                    }

class setup(metaclass=PyMenuMeta):
    __doc__ = 'Enter setup menu.'

    class boundary_conditions(metaclass=PyMenuMeta):
        __doc__ = 'Enter the boudary conditions menu.'
        is_extended_tui = True
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
            'mass_flow_outlet' : 'Set boundary conditions for a zone of this type.',
            'network' : 'Set boundary conditions for a zone of this type.',
            'network_end' : 'Set boundary conditions for a zone of this type.',
            'outflow' : 'Set boundary conditions for a zone of this type.',
            'outlet_vent' : 'Set boundary conditions for a zone of this type.',
            'overset' : 'Set boundary conditions for a zone of this type.',
            'porous_jump' : 'Set boundary conditions for a zone of this type.',
            'radiator' : 'Set boundary conditions for a zone of this type.',
            'rans_les_interface' : 'Set boundary conditions for a zone of this type.',
            'recirculation_inlet' : 'Set boundary conditions for a zone of this type.',
            'recirculation_outlet' : 'Set boundary conditions for a zone of this type.',
            'shadow' : 'Set boundary conditions for a zone of this type.',
            'solid' : 'Set boundary conditions for a zone of this type.',
            'zone_name' : 'Give a zone a new name.',
            'zone_type' : "Set a zone's type.",
        }

        class bc_settings(metaclass=PyMenuMeta):
            __doc__ = ''
            doc_by_method = {
                'mass_flow' : 'Select method for setting the mass flow rate.',
                'pressure_outlet' : 'Select pressure specification method on pressure-outlet boundaries.',
            }

            class pressure_far_field(metaclass=PyMenuMeta):
                __doc__ = 'Select presure-far-field boundary-condition options.'
                doc_by_method = {
                    'riemann_invariants_tangency_correction' : 'Apply a local correction where the flow is tangential to the boundary.',
                    'type?' : 'Choose pressure-far-field boundary-condition type',
                }

        class expert(metaclass=PyMenuMeta):
            __doc__ = 'Enter expert bc menu.'
            doc_by_method = {
                'non_overlapping_zone_name' : 'Get non-overlapping zone name from the associated interface zone',
                'openchannel_threads' : 'List open channel group IDs, names, types, and variables.',
                'open_channel_wave_settings' : 'Open channel wave input analysis',
                'target_mass_flow_rate_settings' : 'Enter the targeted mass flow rate setting menu.',
            }

            class impedance_data_fitting(metaclass=PyMenuMeta):
                __doc__ = 'Enter the impedance data fitting menu.'
                doc_by_method = {
                    'impedance_data' : 'Read experimental impedance data and output impedance parameters for a boundary condition.',
                    'reflection_data' : 'Read experimental reflection coefficient data and output impedance parameters for a boundary condition.',
                    'absorption_data' : 'Read experimental absorption coefficient data and output impedance parameters for a boundary condition.',
                    'iterations' : 'Set the number of iterations for the fitting algorithm.',
                    'convergence_tolerance' : 'Set the convergence tolerance for the fitting algorithm.',
                    'residue_tolerance' : 'Set the residue tolerance for the fitting algorithm.',
                    'verbosity' : 'Set verbosity level [0, 1] for fitting algorithm.',
                    'import_parameters' : 'Import impedance parameters into boundary condition.',
                }

            class non_reflecting_bc(metaclass=PyMenuMeta):
                __doc__ = 'Enter the non-reflecting b.c. menu.'

                class general_nrbc(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the menu for setting general non-reflecting boundary conditions.'

                    class set(metaclass=PyMenuMeta):
                        __doc__ = 'Enter the general non-reflecting b.c. menu.'
                        doc_by_method = {
                            'sigma' : 'Set nrbc sigma factor (default value 0.15).',
                            'sigma2' : 'Set nrbc sigma2 factor (default value 5.0).',
                            'relax' : 'Set NRBC relaxation factor (default value 0.5).',
                            'tangential_source' : 'Include or not NRBC tangential source (default value #t).',
                            'verbosity' : 'Print boundary equations convergence info',
                        }

                class turbo_specific_nrbc(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the turbo-specific n.r.b.c. menu'
                    doc_by_method = {
                        'enable' : "Enable/disable turbo-specific non-reflecting b.c.'s.",
                        'initialize' : "Initialize turbo-specific non-reflecting b.c.'s.",
                        'show_status' : "Show current status of turbo-specific non-reflecting b.c.'s.",
                    }

                    class set(metaclass=PyMenuMeta):
                        __doc__ = 'Enter the set menu for turbo-specific non-reflecting b.c. parameters.'
                        doc_by_method = {
                            'discretization' : 'Enable use of higher-order reconstruction at boundaries if available.',
                            'under_relaxation' : 'Set turbo-specific non-reflecting b.c. under-relaxation factor.\n specify < 0 => use P/a_ave\n specify = 0 => use 1/N    \n specify > 0 => use specified',
                            'verbosity' : 'Set turbo-specific non-reflecting b.c. verbosity level.\n 0 : silent\n 1 : basic info. default \n 2 : detailed info. for debugging \n',
                        }

            class perforated_walls(metaclass=PyMenuMeta):
                __doc__ = 'Enter the perforated walls setting menu.'
                doc_by_method = {
                    'read_input_file' : 'Read an input file.',
                    'model_setup' : 'Set up perforated walls.',
                }

            class periodic_conditions(metaclass=PyMenuMeta):
                __doc__ = 'Enter the periodic conditions menu.'
                doc_by_method = {
                    'massflow_rate_specification' : 'Enable/disable specification of mass flow rate at the periodic boundary.',
                    'pressure_gradient_specification' : 'Enable/disable specification of pressure gradient at the periodic boundary.',
                }

        class mass_flow_inlet(metaclass=PyNamedObjectMeta):
            __doc__ = ''
            is_extended_tui = True

            class flow_spec(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class mass_flow(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ec_mass_flow(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class mass_flux(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class mass_flux_ave(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class tref(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class pref(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class p(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class direction_spec(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class impedance_0(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class frame_of_reference(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class coordinate_system(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ni(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class nj(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class nk(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ni2(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class nj2(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class nk2(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ai(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class aj(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ak(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class x_origin(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class y_origin(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class z_origin(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ke_spec(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class nut(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class kl(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class intermit(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class k(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class e(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class o(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class v2(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class turb_intensity(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class turb_length_scale(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class turb_hydraulic_diam(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class turb_viscosity_ratio(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class turb_viscosity_ratio_profile(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class rst_spec(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class uu(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class vv(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ww(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class uv(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class vw(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class uw(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ksgs_spec(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ksgs(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class sgs_turb_intensity(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class swirl_model(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class swirl_factor(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class x_fan_origin(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class y_fan_origin(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class z_fan_origin(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class wsf(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class wsb(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class wsn(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class slip_velocity(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class velocity_ratio(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class volume_frac(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class granular_temperature(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ac_options(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ac_wave(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class t0(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

        class modify_zones(metaclass=PyMenuMeta):
            __doc__ = 'Enter the modify zones menu.'
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
                'zone_type' : "Set a zone's type.",
                'copy_mrf_to_mesh_motion' : 'Copy motion variable values for origin, axis and velocities from Frame Motion to Mesh Motion.',
                'copy_mesh_to_mrf_motion' : 'Copy motion variable values for origin, axis and velocities from Mesh Motion to Frame Motion.',
                'change_zone_state' : 'Change the realgas material state for a zone.',
                'change_zone_phase' : 'Change the realgas phase for a zone.',
            }

        class periodic(metaclass=PyNamedObjectMeta):
            __doc__ = ''
            is_extended_tui = True

        class pressure_far_field(metaclass=PyNamedObjectMeta):
            __doc__ = ''
            is_extended_tui = True

            class p(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class m(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class coordinate_system(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ni(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class nj(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class nk(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ai(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class aj(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ak(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class x_origin(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class y_origin(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class z_origin(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ke_spec(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class nut(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class kl(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class intermit(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class k(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class e(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class o(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class v2(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class turb_intensity(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class turb_length_scale(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class turb_hydraulic_diam(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class turb_viscosity_ratio(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class turb_viscosity_ratio_profile(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class rst_spec(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class uu(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class vv(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ww(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class uv(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class vw(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class uw(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ksgs_spec(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ksgs(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class sgs_turb_intensity(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class geom_disable(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class geom_dir_spec(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class geom_dir_x(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class geom_dir_y(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class geom_dir_z(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class geom_levels(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class geom_bgthread(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class t(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class non_equil_boundary(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class tve(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

        class pressure_inlet(metaclass=PyNamedObjectMeta):
            __doc__ = ''
            is_extended_tui = True

            class frame_of_reference(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class p0(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class p(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class direction_spec(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class coordinate_system(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ni(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class nj(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class nk(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ni2(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class nj2(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class nk2(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ai(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class aj(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ak(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class x_origin(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class y_origin(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class z_origin(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class vm_number_of_vortices(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class vm_streamwise_fluct(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class vm_mass_conservation(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class volumetric_synthetic_turbulence_generator(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class volumetric_synthetic_turbulence_generator_option(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class volumetric_synthetic_turbulence_generator_option_thickness(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class prevent_reverse_flow(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ke_spec(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class nut(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class kl(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class intermit(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class k(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class e(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class o(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class v2(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class turb_intensity(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class turb_length_scale(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class turb_hydraulic_diam(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class turb_viscosity_ratio(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class turb_viscosity_ratio_profile(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class rst_spec(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class uu(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class vv(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ww(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class uv(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class vw(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class uw(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ksgs_spec(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ksgs(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class sgs_turb_intensity(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class les_spec_name(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class wsf(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class wsb(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class wsn(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ac_options(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ac_wave(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class impedance_0(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class t0(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

        class pressure_outlet(metaclass=PyNamedObjectMeta):
            __doc__ = ''
            is_extended_tui = True

            class prevent_reverse_flow(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class radial(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class gen_nrbc_spec(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class avg_press_spec(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class avg_option(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class targeted_mf_boundary(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class targeted_mf(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class targeted_mf_pmax(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class targeted_mf_pmin(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class press_spec_gen(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class p_backflow_spec(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class p_backflow_spec_gen(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ac_options(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ac_wave(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class impedance_0(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class p(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class p_profile_multiplier(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class direction_spec(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class frame_of_reference(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class coordinate_system(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ni(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class nj(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class nk(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ai(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class aj(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ak(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class x_origin(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class y_origin(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class z_origin(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ke_spec(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class nut(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class kl(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class intermit(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class k(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class e(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class o(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class v2(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class turb_intensity(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class turb_length_scale(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class turb_hydraulic_diam(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class turb_viscosity_ratio(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class turb_viscosity_ratio_profile(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class rst_spec(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class uu(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class vv(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ww(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class uv(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class vw(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class uw(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ksgs_spec(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ksgs(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class sgs_turb_intensity(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class wsf(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class wsb(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class wsn(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class t0(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

        class profiles(metaclass=PyMenuMeta):
            __doc__ = 'Enter the boundary profiles menu.'
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
            __doc__ = 'Enter zone query menu.'
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
            __doc__ = 'Enter zone rename menu.'
            doc_by_method = {
                'rename_by_adjacency' : 'Rename zone to adjacent zones.',
                'rename_to_default' : 'Rename zone to default name.',
                'add_suffix_or_prefix' : 'Add suffix or prefix to zone name',
            }

        class set(metaclass=PyMenuMeta):
            __doc__ = 'Enter the set boundary conditions menu.'
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

        class symmetry(metaclass=PyNamedObjectMeta):
            __doc__ = ''
            is_extended_tui = True

        class velocity_inlet(metaclass=PyNamedObjectMeta):
            __doc__ = ''
            is_extended_tui = True

            class vmag(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class p_sup(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class velocity_spec(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class wave_velocity_spec(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class wave_vmag(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class wave_u(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class wave_v(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class wave_w(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ocw_ship_vel_spec(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ocw_ship_vmag(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ocw_ship_ni(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ocw_ship_nj(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ocw_ship_nk(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ocw_sp_vel_spec(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ocw_sp_vmag(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ocw_sp_ni(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ocw_sp_nj(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ocw_sp_nk(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ocw_pp_vel_spec(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ocw_pp_vmag(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ocw_pp_vmag_ref(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ocw_pp_ref_ht(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ocw_pp_power_coeff(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ocw_pp_ni(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ocw_pp_nj(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ocw_pp_nk(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class p(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class omega_swirl(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class turb_intensity(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class turb_length_scale(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class turb_hydraulic_diam(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class turb_viscosity_ratio(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class turb_viscosity_ratio_profile(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class frame_of_reference(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class coordinate_system(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ni(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class nj(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class nk(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class u(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class v(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class w(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ai(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class aj(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ak(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class x_origin(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class y_origin(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class z_origin(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class vm_number_of_vortices(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class vm_streamwise_fluct(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class vm_mass_conservation(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class volumetric_synthetic_turbulence_generator(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class volumetric_synthetic_turbulence_generator_option(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class volumetric_synthetic_turbulence_generator_option_thickness(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ke_spec(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class nut(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class kl(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class intermit(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class k(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class e(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class o(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class v2(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class rst_spec(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class uu(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class vv(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ww(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class uv(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class vw(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class uw(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ksgs_spec(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ksgs(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class sgs_turb_intensity(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class les_spec_name(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class granular_temperature(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ac_options(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class ac_wave(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class impedance_0(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class t(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class non_equil_boundary(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class tve(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

        class wall(metaclass=PyNamedObjectMeta):
            __doc__ = ''
            is_extended_tui = True

    class dynamic_mesh(metaclass=PyMenuMeta):
        __doc__ = 'Enter the dynamic mesh menu.'
        doc_by_method = {
            'dynamic_mesh' : 'Enable/disable the dynamic mesh solver and options.',
        }

        class controls(metaclass=PyMenuMeta):
            __doc__ = 'Enter the dynamic mesh control menu.'
            doc_by_method = {
                'in_cylinder_output' : 'Enable/disable in-cylinder output.',
                'smoothing' : 'Enable/disable dynamic mesh smoothing.',
                'layering' : 'Enable/disable dynamic-layering in quad/hex cell zones.',
                'remeshing' : 'Enable/disable local remeshing in tri/tet and mixed cell zones.',
                'steady_pseudo_time_control' : 'Enable/disable pseudo time step control in user interface.',
            }

            class smoothing_parameters(metaclass=PyMenuMeta):
                __doc__ = 'Enter the dynamic mesh smoothing menu.'
                doc_by_method = {
                    'smoothing_method' : 'Specify the smoothing method used by the dynamic mesh model.',
                    'constant_factor' : 'Set the spring constant relaxation factor.',
                    'bnd_node_relaxation' : 'Set the spring boundary node relaxation factor.',
                    'bnd_stiffness_factor' : 'Set the stiffness factor for springs connected to boundary nodes.',
                    'convergence_tolerance' : 'Set the convergence tolerance for spring-based solver.',
                    'max_iter' : 'Set the maximum number of iterations for spring-based solver.',
                    'spring_on_all_elements' : 'Enable/disable spring-based smoothing for all cell shapes.',
                    'spring_on_simplex_elements' : 'Enable/disable spring-based smoothing for tri/tet elements in mixed element zones.',
                    'skew_smooth_niter' : 'Set the number of skewness-based smoothing cycles.',
                    'skew_smooth_cell_skew_max' : 'Set the cell skewness threshold above which cells will be smoothed \nusing the skewness method.',
                    'skew_smooth_face_skew_max' : 'Set the face skewness threshold above which deforming boundary faces \nwill be smoothed using the skewness method.',
                    'skew_smooth_all_deforming_boundaries' : 'Enable/disable skewness smoothing for all deforming \ndynamic boundary zones. If disabled, only the deforming dynamic boundary zones are \nsmoothed which have smoothing explicitly enabled or use local face remeshing.',
                    'laplace_node_relaxation' : 'Set the Laplace boundary node relaxation factor.',
                    'diffusion_coeff_function' : 'Specify whether the diffusion coefficient is based on the \nboundary distance or the cell volume.',
                    'diffusion_coeff_parameter' : 'Set the diffusion coefficient parameter used for diffusion-based smoothing.',
                    'diffusion_fvm' : 'Set the numerical method used for diffusion-based smoothing.',
                    'poisson_ratio' : "Set the Poisson's ratio used by the linearly elastic solid model.",
                    'smooth_from_reference_position' : 'Enable smoothing from reference position.',
                    'relative_convergence_tolerance' : 'Set the relative residual convergence tolerance for diffusion-based (FVM) smoothing.',
                    'amg_stabilization' : 'Set the AMG stabilization method for mesh smoothing (FEM).',
                    'verbosity' : 'Set the verbosity for spring smoothing.',
                    'boundary_distance_method' : 'Set the method used to evaluate the boundary distance for the \ndiffusion coefficient calculation.',
                }

            class layering_parameters(metaclass=PyMenuMeta):
                __doc__ = 'Enter the dynamic mesh layering menu.'
                doc_by_method = {
                    'split_factor' : 'Set the factor determining when to split dynamic layers.',
                    'collapse_factor' : 'Set the factor determining when to collapse dynamic layers.',
                    'constant_height' : 'Enable/disable layering based on constant height, else layering based on constant ratio.',
                }

            class remeshing_parameters(metaclass=PyMenuMeta):
                __doc__ = 'Enter the dynamic mesh remeshing menu.'
                doc_by_method = {
                    'unified_remeshing' : 'Enable/disable unified remeshing.',
                    'retain_size_distribution' : 'Enable/disable retaining of size distribution.',
                    'poly_remeshing' : 'Enable/disable poly remeshing.',
                    'remeshing_methods' : 'Enable/disable remeshing methods.',
                    'zone_remeshing' : 'Enable/disable cell zone remeshing method.',
                    'length_min' : 'Set the length threshold below which cells will be remeshed.',
                    'length_max' : 'Set the length threshold above which cells will be remeshed.',
                    'cell_skew_max' : 'Set the cell skewness threshold above which cells will be remeshed.',
                    'face_skew_max' : 'Set the face skewness threshold above which faces will be remeshed.',
                    'size_remesh_interval' : 'Set the interval (in time steps) when remeshing based on size is done.',
                    'sizing_function' : 'Enable/disable sizing function to control size based remeshing.',
                    'sizing_funct_defaults' : 'Set sizing function defaults.',
                    'sizing_funct_resolution' : 'Set the sizing function resolution with respect to shortest boundary.',
                    'sizing_funct_variation' : 'Set the maximum sizing function increase/decrease in the interior.',
                    'sizing_funct_rate' : 'Determine how far from the boundary the increase/decrease happens.',
                    'parallel_remeshing' : 'Enable/disable parallel remeshing for zone remeshing.',
                    'remeshing_after_moving' : 'Enable/disable optional remeshing after mesh motion to meet skewness threshold.\nSteady state dynamic mesh only.',
                }

                class prism_controls(metaclass=PyMenuMeta):
                    __doc__ = 'Specify optional prism controls'
                    doc_by_method = {
                        'add' : 'Add a new object',
                        'edit' : 'Edit an object',
                        'delete' : 'Delete an object',
                        'list' : 'List objects',
                        'list_properties' : 'List properties of an object',
                    }

                class sizing_controls(metaclass=PyMenuMeta):
                    __doc__ = 'Specify optional sizing controls'
                    doc_by_method = {
                        'add' : 'Add a new object',
                        'edit' : 'Edit an object',
                        'delete' : 'Delete an object',
                        'list' : 'List objects',
                        'list_properties' : 'List properties of an object',
                    }

                class prism_layer_parameters(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the dynamic mesh prism remeshing menu.'
                    doc_by_method = {
                        'first_height' : 'Set first cell height in the prism layer.',
                        'growth_rate' : 'Set the geometric growth rate of the prism layer.',
                        'number_of_layers' : 'Set the number of elements in the prism layer.',
                    }

            class in_cylinder_parameters(metaclass=PyMenuMeta):
                __doc__ = 'Enter the dynamic mesh in-cylinder menu.'
                doc_by_method = {
                    'starting_crank_angle' : 'Specify the starting crank angle.',
                    'crank_angle_step' : 'Specify the crank angle step size.',
                    'crank_period' : 'Specify the crank period.',
                    'max_crank_angle_step' : 'Specify the maximum crank angle step size.',
                    'piston_data' : 'Specify the crank radius, connecting rod length, and piston pin offset.',
                    'piston_stroke_cutoff' : 'Specify the cut off point for in-cylinder piston.',
                    'minimum_lift' : 'Specify the minimum lift for in-cylinder valves.',
                    'print_plot_lift' : 'Print or plot valve lift curve.',
                    'modify_lift' : 'Modify the lift curve (shift or scale).',
                    'position_starting_mesh' : 'Move mesh from top dead center to starting crank angle.',
                }

            class implicit_update_parameters(metaclass=PyMenuMeta):
                __doc__ = 'Enter the dynamic mesh implicit update menu.'
                doc_by_method = {
                    'update_interval' : 'Specify update interval of implicit update.',
                    'motion_relaxation' : 'Specify motion relaxation of implicit update.',
                    'residual_criteria' : 'Specify residual criteria of implicit update.',
                }

            class six_dof_parameters(metaclass=PyMenuMeta):
                __doc__ = 'Enter the dynamic mesh six-dof menu.'
                doc_by_method = {
                    'create_properties' : 'Create a set of Six DOF Properties.',
                    'delete_properties' : 'Delete a set of Six DOF Properties.',
                    'list_properties' : 'List Six DOF Properties.',
                    'x_component_of_gravity' : 'Specify x-component-of-gravity.',
                    'y_component_of_gravity' : 'Specify y-component-of-gravity.',
                    'z_component_of_gravity' : 'Specify z-component-of-gravity.',
                    'second_order' : 'Enable/disable second order six DOF solver.',
                    'motion_history' : 'Enable/disable writing position/orientation of six DOF zones to file.',
                    'motion_history_file_name' : 'Location of six DOF motion history file.',
                }

            class periodic_displacement_parameters(metaclass=PyMenuMeta):
                __doc__ = 'Enter the dynamic mesh periodic displacement menu.'
                doc_by_method = {
                    'list_displacements' : 'List Periodic Displacements.',
                    'create_displacement' : 'Create Periodic Displacement.',
                    'edit_displacement' : 'Edit Periodic Displacement.',
                    'copy_displacement' : 'Copy Periodic Displacement.',
                    'delete_displacement' : 'Delete Periodic Displacement.',
                    'delete_all_displacements' : 'Delete All Periodic Displacements.',
                    'create_group' : 'Create Periodic Displacement Group.',
                    'list_groups' : 'List Periodic Displacement Groups.',
                    'edit_group' : 'Edit Periodic Displacement Group.',
                    'delete_group' : 'Delete Periodic Displacement Group.',
                    'delete_all_groups' : 'Delete All Periodic Displacement Groups.',
                    'set_active_displacement' : 'Set Active Periodic Displacement in Group.',
                }

            class contact_parameters(metaclass=PyMenuMeta):
                __doc__ = 'Enter the dynamic mesh contact detection menu.'
                doc_by_method = {
                    'contact_face_zones' : 'Select face zones involved in contact detection.',
                    'contact_udf' : 'Select UDF to be invoked when contact is detected.',
                    'contact_threshold' : 'Specify threshold distance for contact detection.',
                    'update_contact_marks' : 'Update which cells are marked in order to block flow in the contact region.',
                    'flow_control' : 'Enable/disable flow control.',
                    'contact_method' : 'Select the method used for flow control in the contact region.',
                    'render_contact_cells' : 'Set the option to include contact-cells in post-processing.',
                    'verbosity' : 'Set the verbosity for contact-detection.',
                }

                class flow_control_parameters(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the flow control menu.'
                    doc_by_method = {
                        'solution_stabilization' : 'Enable/disable the performance of additional iterations per time step and \n    the application of solution controls to improve the stability of the solver.',
                        'create_flow_control_zone' : 'Create a flow control zone.',
                        'delete_flow_control_zone' : 'Delete a flow control zone.',
                    }

        class events(metaclass=PyMenuMeta):
            __doc__ = 'Enter the dynamic mesh events menu.'
            doc_by_method = {
                'import_event_file' : 'Import dynamic mesh event file.',
                'export_event_file' : 'Export dynamic mesh events to file.',
            }

        class zones(metaclass=PyMenuMeta):
            __doc__ = 'Enter the dynamic mesh zones menu.'
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
            __doc__ = 'Enter the dynamic mesh actions menu.'
            doc_by_method = {
                'remesh_cell_zone' : 'Manually remesh cell zone with option to remesh adjacent dynamic face zones.',
            }

        class transient_settings(metaclass=PyMenuMeta):
            __doc__ = 'Enter the dynamic mesh transient settings menu.'
            doc_by_method = {
                'verbosity' : 'Enable/disable transient scheme verbosity for dynamic mesh cases',
                'allow_second_order' : 'Enable/disable 2nd order transient scheme for dynamic mesh cases',
            }

    class expert(metaclass=PyMenuMeta):
        __doc__ = 'Enter expert setup menu.'
        doc_by_method = {
            'beta_feature_access' : 'Enable access to beta features in the interface.',
            'enable_mesh_morpher_optimizer' : 'Enable use of mesh morpher/optimizer.',
            'heterogeneous_stiff_chemistry' : 'Set heterogeneous stiff-chemistry solver.',
            'stiff_chemistry' : 'Set solver options for stiff-chemistry solutions.',
        }

        class spectral(metaclass=PyMenuMeta):
            __doc__ = 'Enter the Spectral menu.'
            doc_by_method = {
                'calculate_fourier_coefficients' : 'Calculates Fourier coefficient data',
                'delete_fourier_coefficients' : 'Deletes Fourier coefficient data',
                'calculate_harmonic_exports' : 'Calculates Harmonic Export data',
                'delete_harmonic_exports' : 'Deletes Harmonic Export data',
            }

    class gap_model(metaclass=PyMenuMeta):
        __doc__ = 'Enter the narrow-gaps menu.'
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
            __doc__ = 'Show options.'
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
        __doc__ = 'Enter the materials menu.'
        doc_by_method = {
            'change_create' : 'Change the properties of a locally-stored material or create a new material.',
            'copy' : 'Copy a material from the database.',
            'copy_by_formula' : 'Copy a material from the database by formula.',
            'delete' : 'Delete a material from local storage.',
            'list_materials' : 'List all locally-stored materials.',
            'list_properties' : 'List the properties of a locally-stored material.',
        }

        class data_base(metaclass=PyMenuMeta):
            __doc__ = 'Enter the database menu.'
            doc_by_method = {
                'database_type' : 'Set the database type.',
                'edit' : 'Edit a material.',
                'list_materials' : 'List all materials in the database.',
                'list_properties' : 'List the properties of a material in the database.',
                'new' : 'Define a new material',
                'save' : 'Save user-defined database.',
            }

    class mesh_interfaces(metaclass=PyMenuMeta):
        __doc__ = 'Enter the mesh-interfaces menu.'
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
            __doc__ = 'Setting non-conformal numerics options'
            doc_by_method = {
                'change_numerics' : 'Enable modified non-conformal interface numerics',
            }

        class mapped_interface_options(metaclass=PyMenuMeta):
            __doc__ = 'Enter the mapped-interface-options menu.'
            doc_by_method = {
                'solution_controls' : 'Specification of mapped frequency and under-relaxation factor for mapped interfaces',
                'tolerance' : 'Specification of mapped interface tolerance',
                'convert_to_mapped_interface' : 'Convert non-conformal mesh interface to mapped mesh interfaces',
            }

        class auto_options(metaclass=PyMenuMeta):
            __doc__ = 'Enter auto-options menu.'
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
        __doc__ = 'Enter the mixing planes menu.'
        doc_by_method = {
            'create' : 'Create a mixing plane.',
            'delete' : 'Delete a mixing plane.',
            'list' : 'List defined mixing plane(s).',
        }

        class set(metaclass=PyMenuMeta):
            __doc__ = 'Enter the mixing plane set menu.'
            doc_by_method = {
                'under_relaxation' : 'Set mixing plane under-relaxation factor.',
                'averaging_method' : 'Set mixing plane profile averaging method',
                'fix_pressure_level' : 'Set fix pressure level using define/reference-pressure-location.',
            }

            class conserve_swirl(metaclass=PyMenuMeta):
                __doc__ = 'Enter the mixing plane conserve-swirl menu.'
                doc_by_method = {
                    'enable' : 'Enable/disable swirl conservation in mixing plane.',
                    'verbosity' : 'Enable/disable verbosity in swirl conservation calculations.',
                    'report_swirl_integration' : 'Report swirl integration (torque) on inflow and outflow zones.',
                }

            class conserve_total_enthalpy(metaclass=PyMenuMeta):
                __doc__ = 'Enter the menu to set total enthalpy conservation in mixing plane menu.'
                doc_by_method = {
                    'enable' : 'Enable/disable total enthalpy conservation in mixing plane.',
                    'verbosity' : 'Enable/disable verbosity in total-enthalpy conservation calculations.',
                }

    class models(metaclass=PyMenuMeta):
        __doc__ = 'Enter the models menu to configure the solver.'
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
            __doc__ = 'Enter the acoustics model menu.'
            doc_by_method = {
                'off' : 'Enable/disable the acoustics model.',
                'ffowcs_williams' : 'Enable/disable the Ffowcs-Williams-and-Hawkings model.',
                'broad_band_noise' : 'Enable/disable the broadband noise model.',
                'modal_analysis' : 'Enable/disable the modal analysis model.',
                'wave_equation' : 'Enable/disable the wave equation model.',
                'receivers' : 'Set acoustic receivers.',
                'export_source_data' : 'Enable export acoustic source data in ASD format during the wave equation model run.',
                'export_source_data_cgns' : 'Export acoustic source data in CGNS format.',
                'sources' : 'Set acoustic sources.',
                'read_compute_write' : 'Read acoustic source data files and compute sound pressure.',
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
            }

            class far_field_parameters(metaclass=PyMenuMeta):
                __doc__ = 'Enter the far field parameters menu for the wave equation model.'
                doc_by_method = {
                    'far_field_density' : 'Specify far field density.',
                    'far_field_sound_speed' : 'Specify far field speed of sound.',
                }

            class wave_equation_options(metaclass=PyMenuMeta):
                __doc__ = 'Enter the options menu for the wave equation model.'
                doc_by_method = {
                    'time_filter_source' : 'Activate time-filtering of sound sources.',
                    'sponge_layer_factor' : 'Specify artificial viscosity factor for sponge layer.',
                    'sponge_layer_base_level' : 'Specify artificial viscosity base level applied everywhere.',
                    'source_mask_udf' : 'Select user-defined function for sound source masking.',
                    'sponge_layer_udf' : 'Select user-defined function for sponge layer.',
                    'remote_receivers' : "Activate the Kirchhoff's integral method for remote receivers.",
                }

                class basic_shapes(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the basic shapes menu to build source mask and sponge layer\ngeometry shapes using cell registers.'
                    doc_by_method = {
                        'list_region_registers' : 'List all available region registers (hex/cylinder/sphere)',
                        'list_source_mask_shapes' : 'List all active source mask registers',
                        'list_sponge_layer_shapes' : 'List all active sponge layer registers',
                        'add_source_mask_shape' : 'Add a region register for the source mask',
                        'add_sponge_layer_shape' : 'Add a region register for the sponge layer',
                        'remove_source_mask_shape' : 'Remove a region register from the source mask',
                        'remove_sponge_layer_shape' : 'Remove a region register from the sponge layer',
                    }

                class remote_receivers_options(metaclass=PyMenuMeta):
                    __doc__ = "Enter the menu to set up the Kirchhoff's integral method and output its results."
                    doc_by_method = {
                        'integration_surface' : "Select Kirchhoff's integration surface.",
                        'write_signals' : 'Write signals calculated at receiver locations.',
                    }

            class sources_fft(metaclass=PyMenuMeta):
                __doc__ = 'Enter the acoustic sources FFT menu.'
                doc_by_method = {
                    'read_asd_files' : 'Read ASD files.',
                    'compute_fft_fields' : 'Compute FFT fields.',
                    'write_cgns_files' : 'Write CGNS files.',
                    'clean_up_storage_area' : 'Clean up storage area.',
                }

                class fft_surface_variables(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the FFT surface variables menu.'
                    doc_by_method = {
                        'create_octave_bands' : 'Create octave bands.',
                        'create_third_bands' : 'Create third bands.',
                        'create_constant_width_bands' : 'Create constant-width bands.',
                        'create_set_of_modes' : 'Create set of modes.',
                        'remove_variables' : 'Remove variables.',
                    }

            class sponge_layers(metaclass=PyMenuMeta):
                __doc__ = 'Manage sponge layers where density is blended to eliminate reflections from boundary zones.'
                doc_by_method = {
                    'activate' : 'Activate a sponge object.',
                    'add' : 'Add a new sponge layer definition.',
                    'deactivate' : 'Deactivate the sponge object.',
                    'edit' : 'Edit a sponge layer definition.',
                    'delete' : 'Delete a sponge layer definition.',
                    'list' : 'List the names of the sponge layer definitions.',
                    'list_properties' : 'List the properties of a sponge layer definition.',
                }

        class optics(metaclass=PyMenuMeta):
            __doc__ = 'Enter the optics model menu.'
            doc_by_method = {
                'enable' : 'Enable/disable aero-optical model.',
                'add_beam' : 'Add optical beam grid.',
            }

            class set(metaclass=PyMenuMeta):
                __doc__ = 'Enter the set menu for aero-optical model.'
                doc_by_method = {
                    'sampling' : 'Specify when the fluid density field is sampled.',
                    'index_of_refraction' : 'Specify the model parameters of index of refraction.',
                    'running_average' : 'Setup the running average of the collected density field.',
                }

        class eulerian_wallfilm(metaclass=PyMenuMeta):
            __doc__ = 'Enter the Eulerian wall film model menu.'
            doc_by_method = {
                'enable_wallfilm_model' : 'Enable Eulerian wall film model',
                'initialize_wallfilm_model' : 'Initialize Eulerian wall film model',
                'solve_wallfilm_equation' : 'Activate Eulerian wall film equations',
                'model_options' : 'Set Eulerian wall film model options',
                'film_material' : 'Set film material and properties',
                'solution_options' : 'Set Eulerian wall film model solution options',
            }

            class coupled_solution(metaclass=PyMenuMeta):
                __doc__ = 'Enter Eulerian wall film coupled solution menu'
                doc_by_method = {
                    'enable_coupled_solution' : 'Enable Eulerian wall film coupled solution',
                    'enable_curvature_smoothing' : 'Enable Eulerian wall film curvature smoothing',
                }

            class implicit_options(metaclass=PyMenuMeta):
                __doc__ = 'Enter Implicit Scheme Option (beta)'
                doc_by_method = {
                    'new_implicit_scheme' : 'Enable alternative implicit scheme',
                    'relative_error_residual' : 'Enable relative error residual',
                }

        class dpm(metaclass=PyMenuMeta):
            __doc__ = 'Enter the dispersed phase model menu.'
            doc_by_method = {
                'clear_particles_from_domain' : 'Remove/keep all particles currently in the domain.',
                'fill_injection_material_sources' : 'Initialize the DPM sources corresponding to each material.',
                'injections' : 'Enter the injections menu.',
                'unsteady_tracking' : 'Enable/disable unsteady particle tracking.',
                'spray_model' : 'Enter the spray model menu.',
                'user_defined' : 'Set DPM user-defined functions.',
            }

            class collisions(metaclass=PyMenuMeta):
                __doc__ = 'Enter the DEM collisions menu.'
                doc_by_method = {
                    'collision_pair_settings' : 'Supply settings for collisions to a pair of collision partners.',
                    'list_all_pair_settings' : 'For each pair of collision partners, lists the collision laws and their parameters.',
                    'dem_collisions' : 'Enable/disable the DEM collision model.',
                    'collision_mesh' : 'Input for the collision mesh.',
                    'max_particle_velocity' : 'Set the maximum particle velocity that may arise from collisions.',
                }

                class collision_partners(metaclass=PyMenuMeta):
                    __doc__ = 'Manage collision partners.'
                    doc_by_method = {
                        'create' : 'Create a collision partner.',
                        'delete' : 'Delete a collision partner.',
                        'copy' : 'Copy a collision partner.',
                        'rename' : 'Rename a collision partner.',
                        'list' : 'Lists all known collision partners.',
                    }

            class erosion_dynamic_mesh(metaclass=PyMenuMeta):
                __doc__ = 'Enter the erosion-dynamic mesh interactions menu.'
                doc_by_method = {
                    'enable_erosion_dynamic_mesh_coupling' : 'enable mesh deformation due to wall erosion',
                    'run_simulation' : 'Perform coupled erosion-dynamic mesh simulation.',
                }

                class general_parameters(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the erosion-dynamic mesh setup menu.'
                    doc_by_method = {
                        'erosion_settings' : 'Set erosion modelling specific settings.',
                        'dynamic_mesh_settings' : 'Perform dynamic mesh related setup.',
                        'participating_walls' : 'Specify all participating walls.',
                    }

                class run_parameters(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the erosion-dynamic mesh run menu.'
                    doc_by_method = {
                        'mesh_motion_time_step' : 'Set the mesh motion time stepping parameters and method.',
                        'simulation_termination' : 'Set total time of erosion.',
                        'flow_simulation_control' : 'Set number of iterations per flow simulation step.',
                        'autosave_files' : 'Set the iteration increment to save data files.',
                        'autosave_graphics' : 'Set the iteration increment to save graphics files.',
                    }

            class interaction(metaclass=PyMenuMeta):
                __doc__ = 'Enter the interaction menu to set parameters for coupled discrete phase calculations.'
                doc_by_method = {
                    'choice_of_eulerian_phase_for_interaction' : 'Enable/disable the option to choose for every injection the Eulerian phase for the DPM continuous phase interaction.',
                    'coupled_calculations' : 'Enable/disable coupling of continuous and discrete phase calculations.',
                    'dpm_iteration_interval' : 'Set the number of continuous phase iterations per DPM iteration.',
                    'underrelaxation_factor' : 'Set the under-relaxation factor.',
                    'implicit_momentum_coupling' : 'Enable/disable implicit treatment for the DPM momentum source terms.',
                    'implicit_source_term_coupling' : 'Enable/disable implicit treatment for all DPM source terms.',
                    'linearized_dpm_source_terms' : 'Perform a linearization of all DPM source terms to increase numerical robustness',
                    'replace_dpm_mass_source_by_mixture_fraction' : 'Recalculate the mixture fraction source terms as function of the primary mixture fraction?',
                    'linearized_dpm_mixture_fraction_source_terms' : 'Perform a linearization of mixture fraction source terms.',
                    'keep_linearized_dpm_source_terms_constant' : 'Keep linearized DPM source terms constant until the next DPM Update.',
                    'linearized_dpm_source_terms_limiter' : 'Relative limit for DPM source linear coefficient with respect to fluid linear Ap coefficient.',
                    'update_dpm_sources_every_flow_iteration' : 'Enable/disable the update of DPM source terms every flow iteration. \n\n      (if not, the terms will be updated every DPM iteration).',
                    'linear_growth_of_dpm_source_term' : 'Enable/disable the linear growth of DPM source terms every DPM iteration. \n',
                    'reset_sources_at_timestep?' : 'Enable/disable flush of DPM source terms at beginning of every time step.',
                    'enable_flow_blocking_by_particles?' : 'Enable/disable inclusion of DPM volume fraction in continuous flow.',
                    'enable_source_scaling_due_to_flow_blocking?' : 'Enable/disable scaling of DPM source terms due to inclusion of DPM volume fraction in continuous flow.',
                    'enable_drag_scaling_due_to_flow_blocking?' : 'Enable/disable scaling of DPM drag coefficient due to inclusion of DPM volume fraction in continuous flow.',
                    'max_vf_allowed_for_blocking' : 'Maximum DPM volume fraction used in continuous flow.',
                    'min_vf_threshold_for_dpm_src_scaling' : 'Minimum DPM volume fraction below which no DPM source scaling is applied.',
                    'ddpm_iad_particle' : 'Enable/disable the non-default interfacial area method IA-particle.',
                }

            class numerics(metaclass=PyMenuMeta):
                __doc__ = 'Enter the numerics menu to set numerical solution parameters.'
                doc_by_method = {
                    'coupled_heat_mass_update' : 'Enable/disable coupled heat and mass update.',
                    'minimum_liquid_fraction' : 'Evaporate droplet completely when the remaining mass is below this fraction of initial mass.',
                    'underrelax_film_height' : 'Define underrelaxation factor for film height.',
                    'vaporization_limiting_factors' : 'Set Vaporization Fractional Change Limits.',
                    'tracking_parameters' : 'Set parameters for the (initial) tracking step length.',
                    'tracking_scheme' : 'Specify a tracking scheme.',
                    'tracking_statistics' : 'Control the format of the one-line tracking statistics printed after every DPM tracking pass.',
                    'verbosity' : "Adjust the DPM tracker's verbosity level",
                    'error_control' : 'set the adapt integration step length based on a maximum error',
                    'automated_scheme_selection' : 'Enable/disable the adaptation of integration step length based on a maximum error.',
                    'drag_law' : 'Set the drag law.',
                    'enable_node_based_averaging' : 'Enable node based averaging of DPM variables.',
                    'average_source_terms' : 'Average DPM source terms on nodes.',
                    'average_DDPM_variables' : 'Average DDPM specific variables like volume fractions and velocities on nodes.',
                    'average_each_step' : 'Do the averaging after each integration step for higher accuracy at a higher cost.',
                    'average_kernel' : 'Specify a kernel for the averaging.',
                    'gaussian_factor' : 'Set a factor for the gaussian kernel for node-based averaging.~%Large values give small size, small values give large size of kernel.',
                    'mppic_settings' : 'Enable PIC and MPPIC to compute DPM and DDPM source terms.',
                    'enhanced_packing_limit_numerics' : 'Enable enhanced packing limit numerics to avoid exceeding of packing limit for granular phases',
                }

                class high_resolution_tracking(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the high resolution tracking menu.'
                    doc_by_method = {
                        'enable_high_resolution_tracking' : 'Enable high resolution tracking',
                        'enable_barycentric_intersections' : 'Use barycentric coordinates for intersection calculations',
                        'use_barycentric_sampling' : 'Use barycentric coordinates when sampling at planes',
                        'use_velocity_based_error_control' : 'Use adaptive time stepping based upon the particle velocity',
                        'use_quad_face_centroid' : 'Use quad face centroids when creating subtets',
                        'check_subtet_validity' : 'Test for inverted subtets due to warped cells',
                        'always_use_face_centroid_with_periodics' : 'Use quad face centroids when creating subtets if the case contains periodic boundaries',
                        'boundary_layer_tracking' : 'Adjust the particle timestep to account for high aspect ratio cells',
                        'sliding_interface_crossover_fraction' : 'Move the particle a fraction of the distance to the subtet center when crossing a sliding interface',
                        'wallfilm_relocation_tolerance' : 'Set the relocation tolerance for wallfilm particles after remeshing',
                        'project_wall_film_particles_to_film' : 'Project existing particles to film to track using high resolution tracking?',
                        'use_particle_timestep_for_intersection_tolerance' : 'Use the particle timestep for the axisymmetric subtet intersection tolerance',
                        'enable_automatic_intersection_tolerance' : 'Enable automatic scaling of subtet intersection tolerance',
                        'use_legacy_particle_location_method' : 'Enable legacy method of locating particles in cells',
                        'load_legacy_particles' : 'Load particles that were tracked without high-resolution tracking enabled',
                        'enhanced_wallfilm_location_method' : 'Enable enhanced method of locating film particles on faces',
                        'set_film_spreading_parameter' : 'Set the spreading parameter for Lagrangian wallfilm particles',
                        'set_subtet_intersection_tolerance' : 'Set the tolerance for subtet intersection calculations',
                    }

                    class barycentric_interpolation(metaclass=PyMenuMeta):
                        __doc__ = 'Enter the barycentric interpolation menu.'
                        doc_by_method = {
                            'interpolate_flow_solution_gradients' : 'Enable interpolation of flow solution gradients',
                            'interpolate_temperature' : 'Enable interpolation of temperature to the particle position',
                            'interpolate_flow_density' : 'Enable interpolation of flow density to the particle position',
                            'interpolate_flow_cp' : 'Enable interpolation of flow specific heat to the particle position',
                            'interpolate_flow_viscosity' : 'Enable interpolation of flow viscosity to the particle position',
                            'interpolate_wallfilm_properties' : 'Enable interpolation of wallfilm properties to the particle position',
                            'precompute_pdf_species' : 'Precompute cell values of PDF species mass fractions prior to particle tracking',
                            'zero_nodal_velocity_on_walls' : 'Set the nodal velocity on all walls to zero',
                            'enable_transient_variable_interpolation' : 'Enable transient variable interpolation',
                            'nodal_reconstruction_frequency' : "Update nodal reconstruction every N'th DPM iteration",
                            'user_interpolation_function' : 'Enter user interpolation function',
                        }

            class options(metaclass=PyMenuMeta):
                __doc__ = 'Enter the options menu to set optional DPM models.'
                doc_by_method = {
                    'enable_contour_plots' : 'Enable contour and vector plots of particle data.',
                    'ensemble_average' : 'Set ensemble average cloud properties.',
                    'particle_radiation' : 'Enable/disable particle radiation.',
                    'track_in_absolute_frame' : 'Enable/disable tracking in absolute frame.',
                    'thermophoretic_force' : 'Enable/disable thermophoretic force.',
                    'saffman_lift_force' : 'Enable/disable Saffman lift force.',
                    'pressure_gradient_force' : 'Enable/disable pressure gradient force.',
                    'virtual_mass_force' : 'Enable/disable virtual mass force.',
                    'two_way_coupling' : 'Enable/disable calculation of DPM sources in TKE equation.',
                    'remove_wall_film_temperature_limiter' : 'Remove the wall film temperature limiter.',
                    'maximum_udf_species' : 'Maximum number of species that can interact with particles in the DPM UDFs.',
                    'brownian_motion' : 'Enable/disable Brownian motion of particles.',
                    'stagger_spatially_standard_injections' : 'Spatially stagger non-atomizer injections?',
                    'stagger_spatially_atomizer_injections' : 'Spatially stagger atomizer injections?',
                    'stagger_temporally' : 'Stagger transient parcels for their first time step?',
                    'staggering_factor' : 'Set the staggering factor between 0 and 1 to control the amount of staggering.',
                    'stagger_radius' : 'Provide a stagger radius for non atomizer injections.',
                    'uniform_mass_distribution_for_injections' : 'A uniform mass distribution will be enabled for all solid cone and atomizer injections.',
                    'use_absolute_pressure_for_vaporization' : 'Enable/disable using Absolute Pressure for Vaporization.',
                    'vaporization_options' : 'Set Vaporization options.',
                    'vaporization_heat_transfer_averaging' : 'Enable/disable correction for Vaporization heat transfer.',
                    'allow_supercritical_pressure_vaporization' : 'Skip the pressure dependent boiling point calculation to allow supercritical pressure conditions for vaporization.',
                    'treat_multicomponent_saturation_temperature_failure' : 'Dump multicomponent particle mass if the saturation temperature cannot be determined.',
                    'set_thermolysis_limit' : 'Set the thermolysis limit.',
                    'lowest_volatiles_mass_fraction' : 'Set the lowest volatiles mass fraction.',
                    'erosion_accretion' : 'Enable/disable erosion/accretion.',
                    'init_erosion_accretion_rate' : 'Initialize erosion/accretion rates with Zero.',
                    'step_report_sig_figures' : 'Set significant figures in the step-by-step report.',
                    'current_positions_in_sample_file_format' : 'Write the current positions (step-by-step history report for unsteady tracking) in the sampling file format.',
                    'scr_urea_deposition_risk_analysis' : 'Options to activate and configure the SCR urea deposition risk analysis.',
                }

            class parallel(metaclass=PyMenuMeta):
                __doc__ = 'Enter the parallel menu.'
                doc_by_method = {
                    'enable_workpile' : 'Enable/disable the particle workpile algorithm.',
                    'n_threads' : 'Set the number of processors to use for DPM.',
                    'report' : 'Print particle workpile statistics.',
                    'use_shared_memory' : 'Set DPM parallel-mode to shared memory.',
                    'use_message_passing' : 'Set DPM parallel-mode to message passing.',
                    'use_hybrid' : 'Set DPM parallel-mode to hybrid.',
                    'fix_source_term_accumulation_order' : 'Enforce deterministic order of source term accumulation.',
                    'hybrid_2domain' : 'Use DPM domain to simulate particles.',
                    'hybrid_workpile' : 'Optimize multi-thread load balancing within each partition in hybrid-parallel DPM tracking.',
                    'hybrid_collision_model' : "An EXPERIMENTAL feature to allow 'hybrid' DPM parallel tracking with the collision / coalescence model.",
                    'hybrid_collision_unidirectional' : "A faster, yet potentially somewhat less accurate, modification to the beta feature\nthat allows 'hybrid' DPM parallel tracking with the collision / coalescence model.",
                    'hybrid_collision_variant' : "Further reduce the residual risk of dead-locks in the experimental feature that\nallows 'hybrid' DPM parallel tracking with the collision / coalescence model.",
                }

                class expert(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the menu to set expert DPM parallel options.'
                    doc_by_method = {
                        'partition_method_hybrid_2domain' : 'Set DPM Domain partition method',
                    }

            class splash_options(metaclass=PyMenuMeta):
                __doc__ = 'Enter the splash options menu to set optional parameters.'
                doc_by_method = {
                    'orourke_splash_fraction' : 'Select splash fraction method',
                    'splash_pdf_limiting' : 'Select splash pdf limiting method',
                }

            class stripping_options(metaclass=PyMenuMeta):
                __doc__ = 'Enter the stripping options menu to set optional parameters.'
                doc_by_method = {
                    'mass_coefficient' : 'Set the stripping mass coefficient.',
                    'diameter_coefficient' : 'Set the stripping diameter coefficient.',
                }

        class shell_conduction(metaclass=PyMenuMeta):
            __doc__ = 'Enter the shell conduction model menu.'
            doc_by_method = {
                'multi_layer_shell' : 'Enable/disable multi layer shell conduction model.',
                'enhanced_encapsulation' : 'Enable/disable enhanced encapsulation for shell conduction and S2S models. This is not applicable if coupled sliding interface walls exists.',
                'read_csv' : 'Read shell conduction settings from a csv file',
                'write_csv' : 'Write shell conduction settings to a csv file',
                'settings' : 'Enter Multi-layer Shell Conduction data',
                'save_shell_zones' : 'Enable/Disable saving shell zones to case file.',
            }

        class system_coupling_settings(metaclass=PyMenuMeta):
            __doc__ = 'Enter the system coupling model menu.'
            doc_by_method = {
                'use_face_or_element_based_data_transfer' : 'Enable/disable face based data transfer.',
                'update_rigid_body_mesh_motion_before_mesh_transfer' : 'SC Enable/disable mesh motion.',
                'specify_system_coupling_volumetric_cell_zones' : 'Enable/disable volumetric cell zones',
            }

            class htc(metaclass=PyMenuMeta):
                __doc__ = 'Enter the heat transfer coeficient menu.'

                class unsteady_statistics(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the unsteady statistics menu.'
                    doc_by_method = {
                        'sc_enable_sub_stepping_option_per_coupling_step' : 'Enable/disable sub stepping option per coupling step.',
                    }

                class htc_calculation_method(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the htc calculation menu'
                    doc_by_method = {
                        'use_tref_in_htc_calculation' : 'Enable/disable tref in htc computation.',
                        'use_yplus_based_htc_calculation' : 'Enable/disable yplus in htc computation.',
                        'use_wall_function_based_htc' : 'Enable/disable wall function based htc computation.',
                    }

        class cht(metaclass=PyMenuMeta):
            __doc__ = 'Enter the mapped interface model menu.'
            doc_by_method = {
                'read_mi_type_wall' : 'Read mapped interface data settings from a csv file',
                'write_mi_type_wall' : 'Write mapped interface settings to a scv file',
                'implicit_coupling' : 'Enable/disable implicit coupling for mapped interface.',
            }

            class explicit_time_averaged_coupling(metaclass=PyMenuMeta):
                __doc__ = 'Enter the explcit time averaged thermal coupling menu.'
                doc_by_method = {
                    'conformal_coupled_walls' : 'Select fluid-solid coupled walls (without shell) for explicit coupling using time averaged thermal variables.',
                    'mapped_interfaces' : 'Select fluid-solid mapped interfaces for explicit coupling using time averaged thermal variables.',
                    'coupling_controls' : 'Specify explcit coupling controls.',
                    'fuse_explicit_cht_zones' : 'fuse slitted conformal coupled walls marked for transient explicit thermal coupling.',
                }

        class two_temperature(metaclass=PyMenuMeta):
            __doc__ = 'Define two-temperature model menu'
            doc_by_method = {
                'enable' : 'Enable/disable the two-temperature model.',
                'robustness_enhancement' : 'Apply robustness enhancements in the two-temperature model.',
                'nasa9_enhancement' : 'Apply nasa9 robustness enhancements in the two-temperature model.',
                'set_verbosity' : 'set two-temperature model verbosity option',
            }

        class multiphase(metaclass=PyMenuMeta):
            __doc__ = 'Define multiphase model menu'
            doc_by_method = {
                'model' : 'Specify multiphase model.',
                'number_of_phases' : 'Specify the number of phases.',
                'regime_transition_modeling' : 'regime-transition-modeling-options',
                'eulerian_parameters' : 'Eulerian parameters.',
                'volume_fraction_parameters' : 'Volume fraction parameters.',
                'boiling_model_options' : 'Boiling model options.',
                'mixture_parameters' : 'Mixture parameters.',
                'body_force_formulation' : 'Body force formulation.',
                'coupled_level_set' : 'Coupled level set.',
                'vof_sub_models' : 'VOF sub-models.',
                'interface_modeling_options' : 'Interface Modeling Options.',
                'expert_options' : 'Expert Options.',
            }

            class phases(metaclass=PyMenuMeta):
                __doc__ = 'Enter the phases menu.'

                class set_domain_properties(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the menu to set domain properties.'
                    doc_by_method = {
                        'change_phases_names' : 'Change names for all defined phases?',
                        'phase_domains' : 'Enter the menu to select a specific phase domain.',
                    }

                    class interaction_domain(metaclass=PyMenuMeta):
                        __doc__ = 'Enter the menu to set the interaction domain properties.'

                        class forces(metaclass=PyMenuMeta):
                            __doc__ = 'Enter the menu to set interfacial forces related models.'
                            doc_by_method = {
                                'drag' : 'Specify the drag function for each pair of phases. It also enables drag modification and allow specifying the drag factor.',
                                'heat_coeff' : 'Specify the heat transfer coefficient function between each pair of phases.',
                                'interfacial_area' : 'Set the interfacial area parameters for each pair of phases.',
                                'mass_transfer' : 'Specify the mass transfer mechanisms.',
                                'model_transition' : 'Set the model transition mechanism.',
                                'reactions' : 'Define multiple heterogeneous reactions and stoichiometry.',
                                'restitution' : 'Specify the restitution coefficient for collisions between each pair of granular phases and for collisions between particles of the same granular phase.',
                                'slip_velocity' : 'Specify the slip velocity function for each secondary phase with respect to the primary phase.',
                                'turbulence_interaction' : 'Specify the turbulence interaction model for each primary-secondary phase pair.',
                                'turbulent_dispersion' : 'Specify the turbulent dispersion model for each primary-secondary phase pair.',
                                'wall_lubrication' : 'Specify the wall lubrication model for each primary-secondary phase pair.',
                            }

                            class cavitation(metaclass=PyMenuMeta):
                                __doc__ = 'Enter the menu to set cavitation models.'
                                doc_by_method = {
                                    'cavitation' : 'Set the vaporization pressure, the surface tension coefficient, and the non-condensable gas mass fraction.',
                                    'interphase_discr' : 'Enable the phase localized compressive discretization scheme where the degree of diffusion/sharpness is controlled through the value of the slope limiters?',
                                    'interphase_visc_disp' : 'Enable the interfacial viscous dissipation method, which introduces an artificial viscous damping term in the momentum equation?',
                                    'jump_adhesion' : 'Enable the treatment of the contact angle specification at the porous jump boundary?',
                                    'lift' : '',
                                    'lift_montoya' : 'Include the Montoya correction for Lift',
                                    'lift_shaver_podowski' : 'Include the Shaver-Podowski correction for Lift',
                                    'sfc_model_type' : 'Select the surface tension model.',
                                    'sfc_modeling' : 'Include the effects of surface tension along the fluid-fluid interface?',
                                    'sfc_tension_coeff' : 'Specify the surface tension coefficient for each pair of phases.',
                                    'slope_limiter' : 'Specify the slope limiter to set a specific discretization scheme. 0: first order upwind, 1: second order reconstruction bounded by the global minimum/maximum of the volume fraction, 2: compressive. Value between 0 and 2: blended scheme.',
                                    'virtual_mass' : 'Include the virtual mass force that is present when a secondary phase accelerates relative to the primary phase?',
                                    'visc_disp_factor' : 'Set the dissipation intensity.',
                                    'vmass_coeff' : 'Specify the virtual mass coefficient for each pair of phases.',
                                    'vmass_implicit_options' : 'Select the virtual mass implicit option.',
                                    'vmass_implicit' : 'Enable the implicit method for the virtual mass force?',
                                    'wall_adhesion' : 'Enable the specification for a wall adhesion angle?',
                                }

                            class interphase_discretization(metaclass=PyMenuMeta):
                                __doc__ = 'Enter the menu to set interphase discretization models.'
                                doc_by_method = {
                                    'cavitation' : 'Set the vaporization pressure, the surface tension coefficient, and the non-condensable gas mass fraction.',
                                    'interphase_discr' : 'Enable the phase localized compressive discretization scheme where the degree of diffusion/sharpness is controlled through the value of the slope limiters?',
                                    'interphase_visc_disp' : 'Enable the interfacial viscous dissipation method, which introduces an artificial viscous damping term in the momentum equation?',
                                    'jump_adhesion' : 'Enable the treatment of the contact angle specification at the porous jump boundary?',
                                    'lift' : '',
                                    'lift_montoya' : 'Include the Montoya correction for Lift',
                                    'lift_shaver_podowski' : 'Include the Shaver-Podowski correction for Lift',
                                    'sfc_model_type' : 'Select the surface tension model.',
                                    'sfc_modeling' : 'Include the effects of surface tension along the fluid-fluid interface?',
                                    'sfc_tension_coeff' : 'Specify the surface tension coefficient for each pair of phases.',
                                    'slope_limiter' : 'Specify the slope limiter to set a specific discretization scheme. 0: first order upwind, 1: second order reconstruction bounded by the global minimum/maximum of the volume fraction, 2: compressive. Value between 0 and 2: blended scheme.',
                                    'virtual_mass' : 'Include the virtual mass force that is present when a secondary phase accelerates relative to the primary phase?',
                                    'visc_disp_factor' : 'Set the dissipation intensity.',
                                    'vmass_coeff' : 'Specify the virtual mass coefficient for each pair of phases.',
                                    'vmass_implicit_options' : 'Select the virtual mass implicit option.',
                                    'vmass_implicit' : 'Enable the implicit method for the virtual mass force?',
                                    'wall_adhesion' : 'Enable the specification for a wall adhesion angle?',
                                }

                            class interphase_viscous_dissipation(metaclass=PyMenuMeta):
                                __doc__ = 'Enter the menu to set interphase viscous dissipation related models.'
                                doc_by_method = {
                                    'cavitation' : 'Set the vaporization pressure, the surface tension coefficient, and the non-condensable gas mass fraction.',
                                    'interphase_discr' : 'Enable the phase localized compressive discretization scheme where the degree of diffusion/sharpness is controlled through the value of the slope limiters?',
                                    'interphase_visc_disp' : 'Enable the interfacial viscous dissipation method, which introduces an artificial viscous damping term in the momentum equation?',
                                    'jump_adhesion' : 'Enable the treatment of the contact angle specification at the porous jump boundary?',
                                    'lift' : '',
                                    'lift_montoya' : 'Include the Montoya correction for Lift',
                                    'lift_shaver_podowski' : 'Include the Shaver-Podowski correction for Lift',
                                    'sfc_model_type' : 'Select the surface tension model.',
                                    'sfc_modeling' : 'Include the effects of surface tension along the fluid-fluid interface?',
                                    'sfc_tension_coeff' : 'Specify the surface tension coefficient for each pair of phases.',
                                    'slope_limiter' : 'Specify the slope limiter to set a specific discretization scheme. 0: first order upwind, 1: second order reconstruction bounded by the global minimum/maximum of the volume fraction, 2: compressive. Value between 0 and 2: blended scheme.',
                                    'virtual_mass' : 'Include the virtual mass force that is present when a secondary phase accelerates relative to the primary phase?',
                                    'visc_disp_factor' : 'Set the dissipation intensity.',
                                    'vmass_coeff' : 'Specify the virtual mass coefficient for each pair of phases.',
                                    'vmass_implicit_options' : 'Select the virtual mass implicit option.',
                                    'vmass_implicit' : 'Enable the implicit method for the virtual mass force?',
                                    'wall_adhesion' : 'Enable the specification for a wall adhesion angle?',
                                }

                            class lift(metaclass=PyMenuMeta):
                                __doc__ = 'Enter the menu to set lift models.'
                                doc_by_method = {
                                    'cavitation' : 'Set the vaporization pressure, the surface tension coefficient, and the non-condensable gas mass fraction.',
                                    'interphase_discr' : 'Enable the phase localized compressive discretization scheme where the degree of diffusion/sharpness is controlled through the value of the slope limiters?',
                                    'interphase_visc_disp' : 'Enable the interfacial viscous dissipation method, which introduces an artificial viscous damping term in the momentum equation?',
                                    'jump_adhesion' : 'Enable the treatment of the contact angle specification at the porous jump boundary?',
                                    'lift' : '',
                                    'lift_montoya' : 'Include the Montoya correction for Lift',
                                    'lift_shaver_podowski' : 'Include the Shaver-Podowski correction for Lift',
                                    'sfc_model_type' : 'Select the surface tension model.',
                                    'sfc_modeling' : 'Include the effects of surface tension along the fluid-fluid interface?',
                                    'sfc_tension_coeff' : 'Specify the surface tension coefficient for each pair of phases.',
                                    'slope_limiter' : 'Specify the slope limiter to set a specific discretization scheme. 0: first order upwind, 1: second order reconstruction bounded by the global minimum/maximum of the volume fraction, 2: compressive. Value between 0 and 2: blended scheme.',
                                    'virtual_mass' : 'Include the virtual mass force that is present when a secondary phase accelerates relative to the primary phase?',
                                    'visc_disp_factor' : 'Set the dissipation intensity.',
                                    'vmass_coeff' : 'Specify the virtual mass coefficient for each pair of phases.',
                                    'vmass_implicit_options' : 'Select the virtual mass implicit option.',
                                    'vmass_implicit' : 'Enable the implicit method for the virtual mass force?',
                                    'wall_adhesion' : 'Enable the specification for a wall adhesion angle?',
                                }

                            class surface_tension(metaclass=PyMenuMeta):
                                __doc__ = 'Enter the menu to set surface tension models.'
                                doc_by_method = {
                                    'cavitation' : 'Set the vaporization pressure, the surface tension coefficient, and the non-condensable gas mass fraction.',
                                    'interphase_discr' : 'Enable the phase localized compressive discretization scheme where the degree of diffusion/sharpness is controlled through the value of the slope limiters?',
                                    'interphase_visc_disp' : 'Enable the interfacial viscous dissipation method, which introduces an artificial viscous damping term in the momentum equation?',
                                    'jump_adhesion' : 'Enable the treatment of the contact angle specification at the porous jump boundary?',
                                    'lift' : '',
                                    'lift_montoya' : 'Include the Montoya correction for Lift',
                                    'lift_shaver_podowski' : 'Include the Shaver-Podowski correction for Lift',
                                    'sfc_model_type' : 'Select the surface tension model.',
                                    'sfc_modeling' : 'Include the effects of surface tension along the fluid-fluid interface?',
                                    'sfc_tension_coeff' : 'Specify the surface tension coefficient for each pair of phases.',
                                    'slope_limiter' : 'Specify the slope limiter to set a specific discretization scheme. 0: first order upwind, 1: second order reconstruction bounded by the global minimum/maximum of the volume fraction, 2: compressive. Value between 0 and 2: blended scheme.',
                                    'virtual_mass' : 'Include the virtual mass force that is present when a secondary phase accelerates relative to the primary phase?',
                                    'visc_disp_factor' : 'Set the dissipation intensity.',
                                    'vmass_coeff' : 'Specify the virtual mass coefficient for each pair of phases.',
                                    'vmass_implicit_options' : 'Select the virtual mass implicit option.',
                                    'vmass_implicit' : 'Enable the implicit method for the virtual mass force?',
                                    'wall_adhesion' : 'Enable the specification for a wall adhesion angle?',
                                }

                            class virtual_mass(metaclass=PyMenuMeta):
                                __doc__ = 'Enter the menu to set virtual mass models.'
                                doc_by_method = {
                                    'cavitation' : 'Set the vaporization pressure, the surface tension coefficient, and the non-condensable gas mass fraction.',
                                    'interphase_discr' : 'Enable the phase localized compressive discretization scheme where the degree of diffusion/sharpness is controlled through the value of the slope limiters?',
                                    'interphase_visc_disp' : 'Enable the interfacial viscous dissipation method, which introduces an artificial viscous damping term in the momentum equation?',
                                    'jump_adhesion' : 'Enable the treatment of the contact angle specification at the porous jump boundary?',
                                    'lift' : '',
                                    'lift_montoya' : 'Include the Montoya correction for Lift',
                                    'lift_shaver_podowski' : 'Include the Shaver-Podowski correction for Lift',
                                    'sfc_model_type' : 'Select the surface tension model.',
                                    'sfc_modeling' : 'Include the effects of surface tension along the fluid-fluid interface?',
                                    'sfc_tension_coeff' : 'Specify the surface tension coefficient for each pair of phases.',
                                    'slope_limiter' : 'Specify the slope limiter to set a specific discretization scheme. 0: first order upwind, 1: second order reconstruction bounded by the global minimum/maximum of the volume fraction, 2: compressive. Value between 0 and 2: blended scheme.',
                                    'virtual_mass' : 'Include the virtual mass force that is present when a secondary phase accelerates relative to the primary phase?',
                                    'visc_disp_factor' : 'Set the dissipation intensity.',
                                    'vmass_coeff' : 'Specify the virtual mass coefficient for each pair of phases.',
                                    'vmass_implicit_options' : 'Select the virtual mass implicit option.',
                                    'vmass_implicit' : 'Enable the implicit method for the virtual mass force?',
                                    'wall_adhesion' : 'Enable the specification for a wall adhesion angle?',
                                }

                        class heat_mass_reactions(metaclass=PyMenuMeta):
                            __doc__ = 'Enter the menu to set heat, mass-transfer, or reaction related models.'
                            doc_by_method = {
                                'drag' : 'Specify the drag function for each pair of phases. It also enables drag modification and allow specifying the drag factor.',
                                'heat_coeff' : 'Specify the heat transfer coefficient function between each pair of phases.',
                                'interfacial_area' : 'Set the interfacial area parameters for each pair of phases.',
                                'mass_transfer' : 'Specify the mass transfer mechanisms.',
                                'model_transition' : 'Set the model transition mechanism.',
                                'reactions' : 'Define multiple heterogeneous reactions and stoichiometry.',
                                'restitution' : 'Specify the restitution coefficient for collisions between each pair of granular phases and for collisions between particles of the same granular phase.',
                                'slip_velocity' : 'Specify the slip velocity function for each secondary phase with respect to the primary phase.',
                                'turbulence_interaction' : 'Specify the turbulence interaction model for each primary-secondary phase pair.',
                                'turbulent_dispersion' : 'Specify the turbulent dispersion model for each primary-secondary phase pair.',
                                'wall_lubrication' : 'Specify the wall lubrication model for each primary-secondary phase pair.',
                            }

                            class cavitation(metaclass=PyMenuMeta):
                                __doc__ = 'Enter the menu to set cavitation models.'
                                doc_by_method = {
                                    'cavitation' : 'Set the vaporization pressure, the surface tension coefficient, and the non-condensable gas mass fraction.',
                                    'interphase_discr' : 'Enable the phase localized compressive discretization scheme where the degree of diffusion/sharpness is controlled through the value of the slope limiters?',
                                    'interphase_visc_disp' : 'Enable the interfacial viscous dissipation method, which introduces an artificial viscous damping term in the momentum equation?',
                                    'jump_adhesion' : 'Enable the treatment of the contact angle specification at the porous jump boundary?',
                                    'lift' : '',
                                    'lift_montoya' : 'Include the Montoya correction for Lift',
                                    'lift_shaver_podowski' : 'Include the Shaver-Podowski correction for Lift',
                                    'sfc_model_type' : 'Select the surface tension model.',
                                    'sfc_modeling' : 'Include the effects of surface tension along the fluid-fluid interface?',
                                    'sfc_tension_coeff' : 'Specify the surface tension coefficient for each pair of phases.',
                                    'slope_limiter' : 'Specify the slope limiter to set a specific discretization scheme. 0: first order upwind, 1: second order reconstruction bounded by the global minimum/maximum of the volume fraction, 2: compressive. Value between 0 and 2: blended scheme.',
                                    'virtual_mass' : 'Include the virtual mass force that is present when a secondary phase accelerates relative to the primary phase?',
                                    'visc_disp_factor' : 'Set the dissipation intensity.',
                                    'vmass_coeff' : 'Specify the virtual mass coefficient for each pair of phases.',
                                    'vmass_implicit_options' : 'Select the virtual mass implicit option.',
                                    'vmass_implicit' : 'Enable the implicit method for the virtual mass force?',
                                    'wall_adhesion' : 'Enable the specification for a wall adhesion angle?',
                                }

                            class interphase_discretization(metaclass=PyMenuMeta):
                                __doc__ = 'Enter the menu to set interphase discretization models.'
                                doc_by_method = {
                                    'cavitation' : 'Set the vaporization pressure, the surface tension coefficient, and the non-condensable gas mass fraction.',
                                    'interphase_discr' : 'Enable the phase localized compressive discretization scheme where the degree of diffusion/sharpness is controlled through the value of the slope limiters?',
                                    'interphase_visc_disp' : 'Enable the interfacial viscous dissipation method, which introduces an artificial viscous damping term in the momentum equation?',
                                    'jump_adhesion' : 'Enable the treatment of the contact angle specification at the porous jump boundary?',
                                    'lift' : '',
                                    'lift_montoya' : 'Include the Montoya correction for Lift',
                                    'lift_shaver_podowski' : 'Include the Shaver-Podowski correction for Lift',
                                    'sfc_model_type' : 'Select the surface tension model.',
                                    'sfc_modeling' : 'Include the effects of surface tension along the fluid-fluid interface?',
                                    'sfc_tension_coeff' : 'Specify the surface tension coefficient for each pair of phases.',
                                    'slope_limiter' : 'Specify the slope limiter to set a specific discretization scheme. 0: first order upwind, 1: second order reconstruction bounded by the global minimum/maximum of the volume fraction, 2: compressive. Value between 0 and 2: blended scheme.',
                                    'virtual_mass' : 'Include the virtual mass force that is present when a secondary phase accelerates relative to the primary phase?',
                                    'visc_disp_factor' : 'Set the dissipation intensity.',
                                    'vmass_coeff' : 'Specify the virtual mass coefficient for each pair of phases.',
                                    'vmass_implicit_options' : 'Select the virtual mass implicit option.',
                                    'vmass_implicit' : 'Enable the implicit method for the virtual mass force?',
                                    'wall_adhesion' : 'Enable the specification for a wall adhesion angle?',
                                }

                            class interphase_viscous_dissipation(metaclass=PyMenuMeta):
                                __doc__ = 'Enter the menu to set interphase viscous dissipation related models.'
                                doc_by_method = {
                                    'cavitation' : 'Set the vaporization pressure, the surface tension coefficient, and the non-condensable gas mass fraction.',
                                    'interphase_discr' : 'Enable the phase localized compressive discretization scheme where the degree of diffusion/sharpness is controlled through the value of the slope limiters?',
                                    'interphase_visc_disp' : 'Enable the interfacial viscous dissipation method, which introduces an artificial viscous damping term in the momentum equation?',
                                    'jump_adhesion' : 'Enable the treatment of the contact angle specification at the porous jump boundary?',
                                    'lift' : '',
                                    'lift_montoya' : 'Include the Montoya correction for Lift',
                                    'lift_shaver_podowski' : 'Include the Shaver-Podowski correction for Lift',
                                    'sfc_model_type' : 'Select the surface tension model.',
                                    'sfc_modeling' : 'Include the effects of surface tension along the fluid-fluid interface?',
                                    'sfc_tension_coeff' : 'Specify the surface tension coefficient for each pair of phases.',
                                    'slope_limiter' : 'Specify the slope limiter to set a specific discretization scheme. 0: first order upwind, 1: second order reconstruction bounded by the global minimum/maximum of the volume fraction, 2: compressive. Value between 0 and 2: blended scheme.',
                                    'virtual_mass' : 'Include the virtual mass force that is present when a secondary phase accelerates relative to the primary phase?',
                                    'visc_disp_factor' : 'Set the dissipation intensity.',
                                    'vmass_coeff' : 'Specify the virtual mass coefficient for each pair of phases.',
                                    'vmass_implicit_options' : 'Select the virtual mass implicit option.',
                                    'vmass_implicit' : 'Enable the implicit method for the virtual mass force?',
                                    'wall_adhesion' : 'Enable the specification for a wall adhesion angle?',
                                }

                            class lift(metaclass=PyMenuMeta):
                                __doc__ = 'Enter the menu to set lift models.'
                                doc_by_method = {
                                    'cavitation' : 'Set the vaporization pressure, the surface tension coefficient, and the non-condensable gas mass fraction.',
                                    'interphase_discr' : 'Enable the phase localized compressive discretization scheme where the degree of diffusion/sharpness is controlled through the value of the slope limiters?',
                                    'interphase_visc_disp' : 'Enable the interfacial viscous dissipation method, which introduces an artificial viscous damping term in the momentum equation?',
                                    'jump_adhesion' : 'Enable the treatment of the contact angle specification at the porous jump boundary?',
                                    'lift' : '',
                                    'lift_montoya' : 'Include the Montoya correction for Lift',
                                    'lift_shaver_podowski' : 'Include the Shaver-Podowski correction for Lift',
                                    'sfc_model_type' : 'Select the surface tension model.',
                                    'sfc_modeling' : 'Include the effects of surface tension along the fluid-fluid interface?',
                                    'sfc_tension_coeff' : 'Specify the surface tension coefficient for each pair of phases.',
                                    'slope_limiter' : 'Specify the slope limiter to set a specific discretization scheme. 0: first order upwind, 1: second order reconstruction bounded by the global minimum/maximum of the volume fraction, 2: compressive. Value between 0 and 2: blended scheme.',
                                    'virtual_mass' : 'Include the virtual mass force that is present when a secondary phase accelerates relative to the primary phase?',
                                    'visc_disp_factor' : 'Set the dissipation intensity.',
                                    'vmass_coeff' : 'Specify the virtual mass coefficient for each pair of phases.',
                                    'vmass_implicit_options' : 'Select the virtual mass implicit option.',
                                    'vmass_implicit' : 'Enable the implicit method for the virtual mass force?',
                                    'wall_adhesion' : 'Enable the specification for a wall adhesion angle?',
                                }

                            class surface_tension(metaclass=PyMenuMeta):
                                __doc__ = 'Enter the menu to set surface tension models.'
                                doc_by_method = {
                                    'cavitation' : 'Set the vaporization pressure, the surface tension coefficient, and the non-condensable gas mass fraction.',
                                    'interphase_discr' : 'Enable the phase localized compressive discretization scheme where the degree of diffusion/sharpness is controlled through the value of the slope limiters?',
                                    'interphase_visc_disp' : 'Enable the interfacial viscous dissipation method, which introduces an artificial viscous damping term in the momentum equation?',
                                    'jump_adhesion' : 'Enable the treatment of the contact angle specification at the porous jump boundary?',
                                    'lift' : '',
                                    'lift_montoya' : 'Include the Montoya correction for Lift',
                                    'lift_shaver_podowski' : 'Include the Shaver-Podowski correction for Lift',
                                    'sfc_model_type' : 'Select the surface tension model.',
                                    'sfc_modeling' : 'Include the effects of surface tension along the fluid-fluid interface?',
                                    'sfc_tension_coeff' : 'Specify the surface tension coefficient for each pair of phases.',
                                    'slope_limiter' : 'Specify the slope limiter to set a specific discretization scheme. 0: first order upwind, 1: second order reconstruction bounded by the global minimum/maximum of the volume fraction, 2: compressive. Value between 0 and 2: blended scheme.',
                                    'virtual_mass' : 'Include the virtual mass force that is present when a secondary phase accelerates relative to the primary phase?',
                                    'visc_disp_factor' : 'Set the dissipation intensity.',
                                    'vmass_coeff' : 'Specify the virtual mass coefficient for each pair of phases.',
                                    'vmass_implicit_options' : 'Select the virtual mass implicit option.',
                                    'vmass_implicit' : 'Enable the implicit method for the virtual mass force?',
                                    'wall_adhesion' : 'Enable the specification for a wall adhesion angle?',
                                }

                            class virtual_mass(metaclass=PyMenuMeta):
                                __doc__ = 'Enter the menu to set virtual mass models.'
                                doc_by_method = {
                                    'cavitation' : 'Set the vaporization pressure, the surface tension coefficient, and the non-condensable gas mass fraction.',
                                    'interphase_discr' : 'Enable the phase localized compressive discretization scheme where the degree of diffusion/sharpness is controlled through the value of the slope limiters?',
                                    'interphase_visc_disp' : 'Enable the interfacial viscous dissipation method, which introduces an artificial viscous damping term in the momentum equation?',
                                    'jump_adhesion' : 'Enable the treatment of the contact angle specification at the porous jump boundary?',
                                    'lift' : '',
                                    'lift_montoya' : 'Include the Montoya correction for Lift',
                                    'lift_shaver_podowski' : 'Include the Shaver-Podowski correction for Lift',
                                    'sfc_model_type' : 'Select the surface tension model.',
                                    'sfc_modeling' : 'Include the effects of surface tension along the fluid-fluid interface?',
                                    'sfc_tension_coeff' : 'Specify the surface tension coefficient for each pair of phases.',
                                    'slope_limiter' : 'Specify the slope limiter to set a specific discretization scheme. 0: first order upwind, 1: second order reconstruction bounded by the global minimum/maximum of the volume fraction, 2: compressive. Value between 0 and 2: blended scheme.',
                                    'virtual_mass' : 'Include the virtual mass force that is present when a secondary phase accelerates relative to the primary phase?',
                                    'visc_disp_factor' : 'Set the dissipation intensity.',
                                    'vmass_coeff' : 'Specify the virtual mass coefficient for each pair of phases.',
                                    'vmass_implicit_options' : 'Select the virtual mass implicit option.',
                                    'vmass_implicit' : 'Enable the implicit method for the virtual mass force?',
                                    'wall_adhesion' : 'Enable the specification for a wall adhesion angle?',
                                }

                        class interfacial_area(metaclass=PyMenuMeta):
                            __doc__ = 'Enter the menu to set interfacial area models.'
                            doc_by_method = {
                                'drag' : 'Specify the drag function for each pair of phases. It also enables drag modification and allow specifying the drag factor.',
                                'heat_coeff' : 'Specify the heat transfer coefficient function between each pair of phases.',
                                'interfacial_area' : 'Set the interfacial area parameters for each pair of phases.',
                                'mass_transfer' : 'Specify the mass transfer mechanisms.',
                                'model_transition' : 'Set the model transition mechanism.',
                                'reactions' : 'Define multiple heterogeneous reactions and stoichiometry.',
                                'restitution' : 'Specify the restitution coefficient for collisions between each pair of granular phases and for collisions between particles of the same granular phase.',
                                'slip_velocity' : 'Specify the slip velocity function for each secondary phase with respect to the primary phase.',
                                'turbulence_interaction' : 'Specify the turbulence interaction model for each primary-secondary phase pair.',
                                'turbulent_dispersion' : 'Specify the turbulent dispersion model for each primary-secondary phase pair.',
                                'wall_lubrication' : 'Specify the wall lubrication model for each primary-secondary phase pair.',
                            }

                            class cavitation(metaclass=PyMenuMeta):
                                __doc__ = 'Enter the menu to set cavitation models.'
                                doc_by_method = {
                                    'cavitation' : 'Set the vaporization pressure, the surface tension coefficient, and the non-condensable gas mass fraction.',
                                    'interphase_discr' : 'Enable the phase localized compressive discretization scheme where the degree of diffusion/sharpness is controlled through the value of the slope limiters?',
                                    'interphase_visc_disp' : 'Enable the interfacial viscous dissipation method, which introduces an artificial viscous damping term in the momentum equation?',
                                    'jump_adhesion' : 'Enable the treatment of the contact angle specification at the porous jump boundary?',
                                    'lift' : '',
                                    'lift_montoya' : 'Include the Montoya correction for Lift',
                                    'lift_shaver_podowski' : 'Include the Shaver-Podowski correction for Lift',
                                    'sfc_model_type' : 'Select the surface tension model.',
                                    'sfc_modeling' : 'Include the effects of surface tension along the fluid-fluid interface?',
                                    'sfc_tension_coeff' : 'Specify the surface tension coefficient for each pair of phases.',
                                    'slope_limiter' : 'Specify the slope limiter to set a specific discretization scheme. 0: first order upwind, 1: second order reconstruction bounded by the global minimum/maximum of the volume fraction, 2: compressive. Value between 0 and 2: blended scheme.',
                                    'virtual_mass' : 'Include the virtual mass force that is present when a secondary phase accelerates relative to the primary phase?',
                                    'visc_disp_factor' : 'Set the dissipation intensity.',
                                    'vmass_coeff' : 'Specify the virtual mass coefficient for each pair of phases.',
                                    'vmass_implicit_options' : 'Select the virtual mass implicit option.',
                                    'vmass_implicit' : 'Enable the implicit method for the virtual mass force?',
                                    'wall_adhesion' : 'Enable the specification for a wall adhesion angle?',
                                }

                            class interphase_discretization(metaclass=PyMenuMeta):
                                __doc__ = 'Enter the menu to set interphase discretization models.'
                                doc_by_method = {
                                    'cavitation' : 'Set the vaporization pressure, the surface tension coefficient, and the non-condensable gas mass fraction.',
                                    'interphase_discr' : 'Enable the phase localized compressive discretization scheme where the degree of diffusion/sharpness is controlled through the value of the slope limiters?',
                                    'interphase_visc_disp' : 'Enable the interfacial viscous dissipation method, which introduces an artificial viscous damping term in the momentum equation?',
                                    'jump_adhesion' : 'Enable the treatment of the contact angle specification at the porous jump boundary?',
                                    'lift' : '',
                                    'lift_montoya' : 'Include the Montoya correction for Lift',
                                    'lift_shaver_podowski' : 'Include the Shaver-Podowski correction for Lift',
                                    'sfc_model_type' : 'Select the surface tension model.',
                                    'sfc_modeling' : 'Include the effects of surface tension along the fluid-fluid interface?',
                                    'sfc_tension_coeff' : 'Specify the surface tension coefficient for each pair of phases.',
                                    'slope_limiter' : 'Specify the slope limiter to set a specific discretization scheme. 0: first order upwind, 1: second order reconstruction bounded by the global minimum/maximum of the volume fraction, 2: compressive. Value between 0 and 2: blended scheme.',
                                    'virtual_mass' : 'Include the virtual mass force that is present when a secondary phase accelerates relative to the primary phase?',
                                    'visc_disp_factor' : 'Set the dissipation intensity.',
                                    'vmass_coeff' : 'Specify the virtual mass coefficient for each pair of phases.',
                                    'vmass_implicit_options' : 'Select the virtual mass implicit option.',
                                    'vmass_implicit' : 'Enable the implicit method for the virtual mass force?',
                                    'wall_adhesion' : 'Enable the specification for a wall adhesion angle?',
                                }

                            class interphase_viscous_dissipation(metaclass=PyMenuMeta):
                                __doc__ = 'Enter the menu to set interphase viscous dissipation related models.'
                                doc_by_method = {
                                    'cavitation' : 'Set the vaporization pressure, the surface tension coefficient, and the non-condensable gas mass fraction.',
                                    'interphase_discr' : 'Enable the phase localized compressive discretization scheme where the degree of diffusion/sharpness is controlled through the value of the slope limiters?',
                                    'interphase_visc_disp' : 'Enable the interfacial viscous dissipation method, which introduces an artificial viscous damping term in the momentum equation?',
                                    'jump_adhesion' : 'Enable the treatment of the contact angle specification at the porous jump boundary?',
                                    'lift' : '',
                                    'lift_montoya' : 'Include the Montoya correction for Lift',
                                    'lift_shaver_podowski' : 'Include the Shaver-Podowski correction for Lift',
                                    'sfc_model_type' : 'Select the surface tension model.',
                                    'sfc_modeling' : 'Include the effects of surface tension along the fluid-fluid interface?',
                                    'sfc_tension_coeff' : 'Specify the surface tension coefficient for each pair of phases.',
                                    'slope_limiter' : 'Specify the slope limiter to set a specific discretization scheme. 0: first order upwind, 1: second order reconstruction bounded by the global minimum/maximum of the volume fraction, 2: compressive. Value between 0 and 2: blended scheme.',
                                    'virtual_mass' : 'Include the virtual mass force that is present when a secondary phase accelerates relative to the primary phase?',
                                    'visc_disp_factor' : 'Set the dissipation intensity.',
                                    'vmass_coeff' : 'Specify the virtual mass coefficient for each pair of phases.',
                                    'vmass_implicit_options' : 'Select the virtual mass implicit option.',
                                    'vmass_implicit' : 'Enable the implicit method for the virtual mass force?',
                                    'wall_adhesion' : 'Enable the specification for a wall adhesion angle?',
                                }

                            class lift(metaclass=PyMenuMeta):
                                __doc__ = 'Enter the menu to set lift models.'
                                doc_by_method = {
                                    'cavitation' : 'Set the vaporization pressure, the surface tension coefficient, and the non-condensable gas mass fraction.',
                                    'interphase_discr' : 'Enable the phase localized compressive discretization scheme where the degree of diffusion/sharpness is controlled through the value of the slope limiters?',
                                    'interphase_visc_disp' : 'Enable the interfacial viscous dissipation method, which introduces an artificial viscous damping term in the momentum equation?',
                                    'jump_adhesion' : 'Enable the treatment of the contact angle specification at the porous jump boundary?',
                                    'lift' : '',
                                    'lift_montoya' : 'Include the Montoya correction for Lift',
                                    'lift_shaver_podowski' : 'Include the Shaver-Podowski correction for Lift',
                                    'sfc_model_type' : 'Select the surface tension model.',
                                    'sfc_modeling' : 'Include the effects of surface tension along the fluid-fluid interface?',
                                    'sfc_tension_coeff' : 'Specify the surface tension coefficient for each pair of phases.',
                                    'slope_limiter' : 'Specify the slope limiter to set a specific discretization scheme. 0: first order upwind, 1: second order reconstruction bounded by the global minimum/maximum of the volume fraction, 2: compressive. Value between 0 and 2: blended scheme.',
                                    'virtual_mass' : 'Include the virtual mass force that is present when a secondary phase accelerates relative to the primary phase?',
                                    'visc_disp_factor' : 'Set the dissipation intensity.',
                                    'vmass_coeff' : 'Specify the virtual mass coefficient for each pair of phases.',
                                    'vmass_implicit_options' : 'Select the virtual mass implicit option.',
                                    'vmass_implicit' : 'Enable the implicit method for the virtual mass force?',
                                    'wall_adhesion' : 'Enable the specification for a wall adhesion angle?',
                                }

                            class surface_tension(metaclass=PyMenuMeta):
                                __doc__ = 'Enter the menu to set surface tension models.'
                                doc_by_method = {
                                    'cavitation' : 'Set the vaporization pressure, the surface tension coefficient, and the non-condensable gas mass fraction.',
                                    'interphase_discr' : 'Enable the phase localized compressive discretization scheme where the degree of diffusion/sharpness is controlled through the value of the slope limiters?',
                                    'interphase_visc_disp' : 'Enable the interfacial viscous dissipation method, which introduces an artificial viscous damping term in the momentum equation?',
                                    'jump_adhesion' : 'Enable the treatment of the contact angle specification at the porous jump boundary?',
                                    'lift' : '',
                                    'lift_montoya' : 'Include the Montoya correction for Lift',
                                    'lift_shaver_podowski' : 'Include the Shaver-Podowski correction for Lift',
                                    'sfc_model_type' : 'Select the surface tension model.',
                                    'sfc_modeling' : 'Include the effects of surface tension along the fluid-fluid interface?',
                                    'sfc_tension_coeff' : 'Specify the surface tension coefficient for each pair of phases.',
                                    'slope_limiter' : 'Specify the slope limiter to set a specific discretization scheme. 0: first order upwind, 1: second order reconstruction bounded by the global minimum/maximum of the volume fraction, 2: compressive. Value between 0 and 2: blended scheme.',
                                    'virtual_mass' : 'Include the virtual mass force that is present when a secondary phase accelerates relative to the primary phase?',
                                    'visc_disp_factor' : 'Set the dissipation intensity.',
                                    'vmass_coeff' : 'Specify the virtual mass coefficient for each pair of phases.',
                                    'vmass_implicit_options' : 'Select the virtual mass implicit option.',
                                    'vmass_implicit' : 'Enable the implicit method for the virtual mass force?',
                                    'wall_adhesion' : 'Enable the specification for a wall adhesion angle?',
                                }

                            class virtual_mass(metaclass=PyMenuMeta):
                                __doc__ = 'Enter the menu to set virtual mass models.'
                                doc_by_method = {
                                    'cavitation' : 'Set the vaporization pressure, the surface tension coefficient, and the non-condensable gas mass fraction.',
                                    'interphase_discr' : 'Enable the phase localized compressive discretization scheme where the degree of diffusion/sharpness is controlled through the value of the slope limiters?',
                                    'interphase_visc_disp' : 'Enable the interfacial viscous dissipation method, which introduces an artificial viscous damping term in the momentum equation?',
                                    'jump_adhesion' : 'Enable the treatment of the contact angle specification at the porous jump boundary?',
                                    'lift' : '',
                                    'lift_montoya' : 'Include the Montoya correction for Lift',
                                    'lift_shaver_podowski' : 'Include the Shaver-Podowski correction for Lift',
                                    'sfc_model_type' : 'Select the surface tension model.',
                                    'sfc_modeling' : 'Include the effects of surface tension along the fluid-fluid interface?',
                                    'sfc_tension_coeff' : 'Specify the surface tension coefficient for each pair of phases.',
                                    'slope_limiter' : 'Specify the slope limiter to set a specific discretization scheme. 0: first order upwind, 1: second order reconstruction bounded by the global minimum/maximum of the volume fraction, 2: compressive. Value between 0 and 2: blended scheme.',
                                    'virtual_mass' : 'Include the virtual mass force that is present when a secondary phase accelerates relative to the primary phase?',
                                    'visc_disp_factor' : 'Set the dissipation intensity.',
                                    'vmass_coeff' : 'Specify the virtual mass coefficient for each pair of phases.',
                                    'vmass_implicit_options' : 'Select the virtual mass implicit option.',
                                    'vmass_implicit' : 'Enable the implicit method for the virtual mass force?',
                                    'wall_adhesion' : 'Enable the specification for a wall adhesion angle?',
                                }

                        class model_transition(metaclass=PyMenuMeta):
                            __doc__ = 'Enter the menu to set model transition mechanisms.'
                            doc_by_method = {
                                'drag' : 'Specify the drag function for each pair of phases. It also enables drag modification and allow specifying the drag factor.',
                                'heat_coeff' : 'Specify the heat transfer coefficient function between each pair of phases.',
                                'interfacial_area' : 'Set the interfacial area parameters for each pair of phases.',
                                'mass_transfer' : 'Specify the mass transfer mechanisms.',
                                'model_transition' : 'Set the model transition mechanism.',
                                'reactions' : 'Define multiple heterogeneous reactions and stoichiometry.',
                                'restitution' : 'Specify the restitution coefficient for collisions between each pair of granular phases and for collisions between particles of the same granular phase.',
                                'slip_velocity' : 'Specify the slip velocity function for each secondary phase with respect to the primary phase.',
                                'turbulence_interaction' : 'Specify the turbulence interaction model for each primary-secondary phase pair.',
                                'turbulent_dispersion' : 'Specify the turbulent dispersion model for each primary-secondary phase pair.',
                                'wall_lubrication' : 'Specify the wall lubrication model for each primary-secondary phase pair.',
                            }

                            class cavitation(metaclass=PyMenuMeta):
                                __doc__ = 'Enter the menu to set cavitation models.'
                                doc_by_method = {
                                    'cavitation' : 'Set the vaporization pressure, the surface tension coefficient, and the non-condensable gas mass fraction.',
                                    'interphase_discr' : 'Enable the phase localized compressive discretization scheme where the degree of diffusion/sharpness is controlled through the value of the slope limiters?',
                                    'interphase_visc_disp' : 'Enable the interfacial viscous dissipation method, which introduces an artificial viscous damping term in the momentum equation?',
                                    'jump_adhesion' : 'Enable the treatment of the contact angle specification at the porous jump boundary?',
                                    'lift' : '',
                                    'lift_montoya' : 'Include the Montoya correction for Lift',
                                    'lift_shaver_podowski' : 'Include the Shaver-Podowski correction for Lift',
                                    'sfc_model_type' : 'Select the surface tension model.',
                                    'sfc_modeling' : 'Include the effects of surface tension along the fluid-fluid interface?',
                                    'sfc_tension_coeff' : 'Specify the surface tension coefficient for each pair of phases.',
                                    'slope_limiter' : 'Specify the slope limiter to set a specific discretization scheme. 0: first order upwind, 1: second order reconstruction bounded by the global minimum/maximum of the volume fraction, 2: compressive. Value between 0 and 2: blended scheme.',
                                    'virtual_mass' : 'Include the virtual mass force that is present when a secondary phase accelerates relative to the primary phase?',
                                    'visc_disp_factor' : 'Set the dissipation intensity.',
                                    'vmass_coeff' : 'Specify the virtual mass coefficient for each pair of phases.',
                                    'vmass_implicit_options' : 'Select the virtual mass implicit option.',
                                    'vmass_implicit' : 'Enable the implicit method for the virtual mass force?',
                                    'wall_adhesion' : 'Enable the specification for a wall adhesion angle?',
                                }

                            class interphase_discretization(metaclass=PyMenuMeta):
                                __doc__ = 'Enter the menu to set interphase discretization models.'
                                doc_by_method = {
                                    'cavitation' : 'Set the vaporization pressure, the surface tension coefficient, and the non-condensable gas mass fraction.',
                                    'interphase_discr' : 'Enable the phase localized compressive discretization scheme where the degree of diffusion/sharpness is controlled through the value of the slope limiters?',
                                    'interphase_visc_disp' : 'Enable the interfacial viscous dissipation method, which introduces an artificial viscous damping term in the momentum equation?',
                                    'jump_adhesion' : 'Enable the treatment of the contact angle specification at the porous jump boundary?',
                                    'lift' : '',
                                    'lift_montoya' : 'Include the Montoya correction for Lift',
                                    'lift_shaver_podowski' : 'Include the Shaver-Podowski correction for Lift',
                                    'sfc_model_type' : 'Select the surface tension model.',
                                    'sfc_modeling' : 'Include the effects of surface tension along the fluid-fluid interface?',
                                    'sfc_tension_coeff' : 'Specify the surface tension coefficient for each pair of phases.',
                                    'slope_limiter' : 'Specify the slope limiter to set a specific discretization scheme. 0: first order upwind, 1: second order reconstruction bounded by the global minimum/maximum of the volume fraction, 2: compressive. Value between 0 and 2: blended scheme.',
                                    'virtual_mass' : 'Include the virtual mass force that is present when a secondary phase accelerates relative to the primary phase?',
                                    'visc_disp_factor' : 'Set the dissipation intensity.',
                                    'vmass_coeff' : 'Specify the virtual mass coefficient for each pair of phases.',
                                    'vmass_implicit_options' : 'Select the virtual mass implicit option.',
                                    'vmass_implicit' : 'Enable the implicit method for the virtual mass force?',
                                    'wall_adhesion' : 'Enable the specification for a wall adhesion angle?',
                                }

                            class interphase_viscous_dissipation(metaclass=PyMenuMeta):
                                __doc__ = 'Enter the menu to set interphase viscous dissipation related models.'
                                doc_by_method = {
                                    'cavitation' : 'Set the vaporization pressure, the surface tension coefficient, and the non-condensable gas mass fraction.',
                                    'interphase_discr' : 'Enable the phase localized compressive discretization scheme where the degree of diffusion/sharpness is controlled through the value of the slope limiters?',
                                    'interphase_visc_disp' : 'Enable the interfacial viscous dissipation method, which introduces an artificial viscous damping term in the momentum equation?',
                                    'jump_adhesion' : 'Enable the treatment of the contact angle specification at the porous jump boundary?',
                                    'lift' : '',
                                    'lift_montoya' : 'Include the Montoya correction for Lift',
                                    'lift_shaver_podowski' : 'Include the Shaver-Podowski correction for Lift',
                                    'sfc_model_type' : 'Select the surface tension model.',
                                    'sfc_modeling' : 'Include the effects of surface tension along the fluid-fluid interface?',
                                    'sfc_tension_coeff' : 'Specify the surface tension coefficient for each pair of phases.',
                                    'slope_limiter' : 'Specify the slope limiter to set a specific discretization scheme. 0: first order upwind, 1: second order reconstruction bounded by the global minimum/maximum of the volume fraction, 2: compressive. Value between 0 and 2: blended scheme.',
                                    'virtual_mass' : 'Include the virtual mass force that is present when a secondary phase accelerates relative to the primary phase?',
                                    'visc_disp_factor' : 'Set the dissipation intensity.',
                                    'vmass_coeff' : 'Specify the virtual mass coefficient for each pair of phases.',
                                    'vmass_implicit_options' : 'Select the virtual mass implicit option.',
                                    'vmass_implicit' : 'Enable the implicit method for the virtual mass force?',
                                    'wall_adhesion' : 'Enable the specification for a wall adhesion angle?',
                                }

                            class lift(metaclass=PyMenuMeta):
                                __doc__ = 'Enter the menu to set lift models.'
                                doc_by_method = {
                                    'cavitation' : 'Set the vaporization pressure, the surface tension coefficient, and the non-condensable gas mass fraction.',
                                    'interphase_discr' : 'Enable the phase localized compressive discretization scheme where the degree of diffusion/sharpness is controlled through the value of the slope limiters?',
                                    'interphase_visc_disp' : 'Enable the interfacial viscous dissipation method, which introduces an artificial viscous damping term in the momentum equation?',
                                    'jump_adhesion' : 'Enable the treatment of the contact angle specification at the porous jump boundary?',
                                    'lift' : '',
                                    'lift_montoya' : 'Include the Montoya correction for Lift',
                                    'lift_shaver_podowski' : 'Include the Shaver-Podowski correction for Lift',
                                    'sfc_model_type' : 'Select the surface tension model.',
                                    'sfc_modeling' : 'Include the effects of surface tension along the fluid-fluid interface?',
                                    'sfc_tension_coeff' : 'Specify the surface tension coefficient for each pair of phases.',
                                    'slope_limiter' : 'Specify the slope limiter to set a specific discretization scheme. 0: first order upwind, 1: second order reconstruction bounded by the global minimum/maximum of the volume fraction, 2: compressive. Value between 0 and 2: blended scheme.',
                                    'virtual_mass' : 'Include the virtual mass force that is present when a secondary phase accelerates relative to the primary phase?',
                                    'visc_disp_factor' : 'Set the dissipation intensity.',
                                    'vmass_coeff' : 'Specify the virtual mass coefficient for each pair of phases.',
                                    'vmass_implicit_options' : 'Select the virtual mass implicit option.',
                                    'vmass_implicit' : 'Enable the implicit method for the virtual mass force?',
                                    'wall_adhesion' : 'Enable the specification for a wall adhesion angle?',
                                }

                            class surface_tension(metaclass=PyMenuMeta):
                                __doc__ = 'Enter the menu to set surface tension models.'
                                doc_by_method = {
                                    'cavitation' : 'Set the vaporization pressure, the surface tension coefficient, and the non-condensable gas mass fraction.',
                                    'interphase_discr' : 'Enable the phase localized compressive discretization scheme where the degree of diffusion/sharpness is controlled through the value of the slope limiters?',
                                    'interphase_visc_disp' : 'Enable the interfacial viscous dissipation method, which introduces an artificial viscous damping term in the momentum equation?',
                                    'jump_adhesion' : 'Enable the treatment of the contact angle specification at the porous jump boundary?',
                                    'lift' : '',
                                    'lift_montoya' : 'Include the Montoya correction for Lift',
                                    'lift_shaver_podowski' : 'Include the Shaver-Podowski correction for Lift',
                                    'sfc_model_type' : 'Select the surface tension model.',
                                    'sfc_modeling' : 'Include the effects of surface tension along the fluid-fluid interface?',
                                    'sfc_tension_coeff' : 'Specify the surface tension coefficient for each pair of phases.',
                                    'slope_limiter' : 'Specify the slope limiter to set a specific discretization scheme. 0: first order upwind, 1: second order reconstruction bounded by the global minimum/maximum of the volume fraction, 2: compressive. Value between 0 and 2: blended scheme.',
                                    'virtual_mass' : 'Include the virtual mass force that is present when a secondary phase accelerates relative to the primary phase?',
                                    'visc_disp_factor' : 'Set the dissipation intensity.',
                                    'vmass_coeff' : 'Specify the virtual mass coefficient for each pair of phases.',
                                    'vmass_implicit_options' : 'Select the virtual mass implicit option.',
                                    'vmass_implicit' : 'Enable the implicit method for the virtual mass force?',
                                    'wall_adhesion' : 'Enable the specification for a wall adhesion angle?',
                                }

                            class virtual_mass(metaclass=PyMenuMeta):
                                __doc__ = 'Enter the menu to set virtual mass models.'
                                doc_by_method = {
                                    'cavitation' : 'Set the vaporization pressure, the surface tension coefficient, and the non-condensable gas mass fraction.',
                                    'interphase_discr' : 'Enable the phase localized compressive discretization scheme where the degree of diffusion/sharpness is controlled through the value of the slope limiters?',
                                    'interphase_visc_disp' : 'Enable the interfacial viscous dissipation method, which introduces an artificial viscous damping term in the momentum equation?',
                                    'jump_adhesion' : 'Enable the treatment of the contact angle specification at the porous jump boundary?',
                                    'lift' : '',
                                    'lift_montoya' : 'Include the Montoya correction for Lift',
                                    'lift_shaver_podowski' : 'Include the Shaver-Podowski correction for Lift',
                                    'sfc_model_type' : 'Select the surface tension model.',
                                    'sfc_modeling' : 'Include the effects of surface tension along the fluid-fluid interface?',
                                    'sfc_tension_coeff' : 'Specify the surface tension coefficient for each pair of phases.',
                                    'slope_limiter' : 'Specify the slope limiter to set a specific discretization scheme. 0: first order upwind, 1: second order reconstruction bounded by the global minimum/maximum of the volume fraction, 2: compressive. Value between 0 and 2: blended scheme.',
                                    'virtual_mass' : 'Include the virtual mass force that is present when a secondary phase accelerates relative to the primary phase?',
                                    'visc_disp_factor' : 'Set the dissipation intensity.',
                                    'vmass_coeff' : 'Specify the virtual mass coefficient for each pair of phases.',
                                    'vmass_implicit_options' : 'Select the virtual mass implicit option.',
                                    'vmass_implicit' : 'Enable the implicit method for the virtual mass force?',
                                    'wall_adhesion' : 'Enable the specification for a wall adhesion angle?',
                                }

                        class numerics(metaclass=PyMenuMeta):
                            __doc__ = 'Enter the menu to set numerics models.'
                            doc_by_method = {
                                'drag' : 'Specify the drag function for each pair of phases. It also enables drag modification and allow specifying the drag factor.',
                                'heat_coeff' : 'Specify the heat transfer coefficient function between each pair of phases.',
                                'interfacial_area' : 'Set the interfacial area parameters for each pair of phases.',
                                'mass_transfer' : 'Specify the mass transfer mechanisms.',
                                'model_transition' : 'Set the model transition mechanism.',
                                'reactions' : 'Define multiple heterogeneous reactions and stoichiometry.',
                                'restitution' : 'Specify the restitution coefficient for collisions between each pair of granular phases and for collisions between particles of the same granular phase.',
                                'slip_velocity' : 'Specify the slip velocity function for each secondary phase with respect to the primary phase.',
                                'turbulence_interaction' : 'Specify the turbulence interaction model for each primary-secondary phase pair.',
                                'turbulent_dispersion' : 'Specify the turbulent dispersion model for each primary-secondary phase pair.',
                                'wall_lubrication' : 'Specify the wall lubrication model for each primary-secondary phase pair.',
                            }

                            class cavitation(metaclass=PyMenuMeta):
                                __doc__ = 'Enter the menu to set cavitation models.'
                                doc_by_method = {
                                    'cavitation' : 'Set the vaporization pressure, the surface tension coefficient, and the non-condensable gas mass fraction.',
                                    'interphase_discr' : 'Enable the phase localized compressive discretization scheme where the degree of diffusion/sharpness is controlled through the value of the slope limiters?',
                                    'interphase_visc_disp' : 'Enable the interfacial viscous dissipation method, which introduces an artificial viscous damping term in the momentum equation?',
                                    'jump_adhesion' : 'Enable the treatment of the contact angle specification at the porous jump boundary?',
                                    'lift' : '',
                                    'lift_montoya' : 'Include the Montoya correction for Lift',
                                    'lift_shaver_podowski' : 'Include the Shaver-Podowski correction for Lift',
                                    'sfc_model_type' : 'Select the surface tension model.',
                                    'sfc_modeling' : 'Include the effects of surface tension along the fluid-fluid interface?',
                                    'sfc_tension_coeff' : 'Specify the surface tension coefficient for each pair of phases.',
                                    'slope_limiter' : 'Specify the slope limiter to set a specific discretization scheme. 0: first order upwind, 1: second order reconstruction bounded by the global minimum/maximum of the volume fraction, 2: compressive. Value between 0 and 2: blended scheme.',
                                    'virtual_mass' : 'Include the virtual mass force that is present when a secondary phase accelerates relative to the primary phase?',
                                    'visc_disp_factor' : 'Set the dissipation intensity.',
                                    'vmass_coeff' : 'Specify the virtual mass coefficient for each pair of phases.',
                                    'vmass_implicit_options' : 'Select the virtual mass implicit option.',
                                    'vmass_implicit' : 'Enable the implicit method for the virtual mass force?',
                                    'wall_adhesion' : 'Enable the specification for a wall adhesion angle?',
                                }

                            class interphase_discretization(metaclass=PyMenuMeta):
                                __doc__ = 'Enter the menu to set interphase discretization models.'
                                doc_by_method = {
                                    'cavitation' : 'Set the vaporization pressure, the surface tension coefficient, and the non-condensable gas mass fraction.',
                                    'interphase_discr' : 'Enable the phase localized compressive discretization scheme where the degree of diffusion/sharpness is controlled through the value of the slope limiters?',
                                    'interphase_visc_disp' : 'Enable the interfacial viscous dissipation method, which introduces an artificial viscous damping term in the momentum equation?',
                                    'jump_adhesion' : 'Enable the treatment of the contact angle specification at the porous jump boundary?',
                                    'lift' : '',
                                    'lift_montoya' : 'Include the Montoya correction for Lift',
                                    'lift_shaver_podowski' : 'Include the Shaver-Podowski correction for Lift',
                                    'sfc_model_type' : 'Select the surface tension model.',
                                    'sfc_modeling' : 'Include the effects of surface tension along the fluid-fluid interface?',
                                    'sfc_tension_coeff' : 'Specify the surface tension coefficient for each pair of phases.',
                                    'slope_limiter' : 'Specify the slope limiter to set a specific discretization scheme. 0: first order upwind, 1: second order reconstruction bounded by the global minimum/maximum of the volume fraction, 2: compressive. Value between 0 and 2: blended scheme.',
                                    'virtual_mass' : 'Include the virtual mass force that is present when a secondary phase accelerates relative to the primary phase?',
                                    'visc_disp_factor' : 'Set the dissipation intensity.',
                                    'vmass_coeff' : 'Specify the virtual mass coefficient for each pair of phases.',
                                    'vmass_implicit_options' : 'Select the virtual mass implicit option.',
                                    'vmass_implicit' : 'Enable the implicit method for the virtual mass force?',
                                    'wall_adhesion' : 'Enable the specification for a wall adhesion angle?',
                                }

                            class interphase_viscous_dissipation(metaclass=PyMenuMeta):
                                __doc__ = 'Enter the menu to set interphase viscous dissipation related models.'
                                doc_by_method = {
                                    'cavitation' : 'Set the vaporization pressure, the surface tension coefficient, and the non-condensable gas mass fraction.',
                                    'interphase_discr' : 'Enable the phase localized compressive discretization scheme where the degree of diffusion/sharpness is controlled through the value of the slope limiters?',
                                    'interphase_visc_disp' : 'Enable the interfacial viscous dissipation method, which introduces an artificial viscous damping term in the momentum equation?',
                                    'jump_adhesion' : 'Enable the treatment of the contact angle specification at the porous jump boundary?',
                                    'lift' : '',
                                    'lift_montoya' : 'Include the Montoya correction for Lift',
                                    'lift_shaver_podowski' : 'Include the Shaver-Podowski correction for Lift',
                                    'sfc_model_type' : 'Select the surface tension model.',
                                    'sfc_modeling' : 'Include the effects of surface tension along the fluid-fluid interface?',
                                    'sfc_tension_coeff' : 'Specify the surface tension coefficient for each pair of phases.',
                                    'slope_limiter' : 'Specify the slope limiter to set a specific discretization scheme. 0: first order upwind, 1: second order reconstruction bounded by the global minimum/maximum of the volume fraction, 2: compressive. Value between 0 and 2: blended scheme.',
                                    'virtual_mass' : 'Include the virtual mass force that is present when a secondary phase accelerates relative to the primary phase?',
                                    'visc_disp_factor' : 'Set the dissipation intensity.',
                                    'vmass_coeff' : 'Specify the virtual mass coefficient for each pair of phases.',
                                    'vmass_implicit_options' : 'Select the virtual mass implicit option.',
                                    'vmass_implicit' : 'Enable the implicit method for the virtual mass force?',
                                    'wall_adhesion' : 'Enable the specification for a wall adhesion angle?',
                                }

                            class lift(metaclass=PyMenuMeta):
                                __doc__ = 'Enter the menu to set lift models.'
                                doc_by_method = {
                                    'cavitation' : 'Set the vaporization pressure, the surface tension coefficient, and the non-condensable gas mass fraction.',
                                    'interphase_discr' : 'Enable the phase localized compressive discretization scheme where the degree of diffusion/sharpness is controlled through the value of the slope limiters?',
                                    'interphase_visc_disp' : 'Enable the interfacial viscous dissipation method, which introduces an artificial viscous damping term in the momentum equation?',
                                    'jump_adhesion' : 'Enable the treatment of the contact angle specification at the porous jump boundary?',
                                    'lift' : '',
                                    'lift_montoya' : 'Include the Montoya correction for Lift',
                                    'lift_shaver_podowski' : 'Include the Shaver-Podowski correction for Lift',
                                    'sfc_model_type' : 'Select the surface tension model.',
                                    'sfc_modeling' : 'Include the effects of surface tension along the fluid-fluid interface?',
                                    'sfc_tension_coeff' : 'Specify the surface tension coefficient for each pair of phases.',
                                    'slope_limiter' : 'Specify the slope limiter to set a specific discretization scheme. 0: first order upwind, 1: second order reconstruction bounded by the global minimum/maximum of the volume fraction, 2: compressive. Value between 0 and 2: blended scheme.',
                                    'virtual_mass' : 'Include the virtual mass force that is present when a secondary phase accelerates relative to the primary phase?',
                                    'visc_disp_factor' : 'Set the dissipation intensity.',
                                    'vmass_coeff' : 'Specify the virtual mass coefficient for each pair of phases.',
                                    'vmass_implicit_options' : 'Select the virtual mass implicit option.',
                                    'vmass_implicit' : 'Enable the implicit method for the virtual mass force?',
                                    'wall_adhesion' : 'Enable the specification for a wall adhesion angle?',
                                }

                            class surface_tension(metaclass=PyMenuMeta):
                                __doc__ = 'Enter the menu to set surface tension models.'
                                doc_by_method = {
                                    'cavitation' : 'Set the vaporization pressure, the surface tension coefficient, and the non-condensable gas mass fraction.',
                                    'interphase_discr' : 'Enable the phase localized compressive discretization scheme where the degree of diffusion/sharpness is controlled through the value of the slope limiters?',
                                    'interphase_visc_disp' : 'Enable the interfacial viscous dissipation method, which introduces an artificial viscous damping term in the momentum equation?',
                                    'jump_adhesion' : 'Enable the treatment of the contact angle specification at the porous jump boundary?',
                                    'lift' : '',
                                    'lift_montoya' : 'Include the Montoya correction for Lift',
                                    'lift_shaver_podowski' : 'Include the Shaver-Podowski correction for Lift',
                                    'sfc_model_type' : 'Select the surface tension model.',
                                    'sfc_modeling' : 'Include the effects of surface tension along the fluid-fluid interface?',
                                    'sfc_tension_coeff' : 'Specify the surface tension coefficient for each pair of phases.',
                                    'slope_limiter' : 'Specify the slope limiter to set a specific discretization scheme. 0: first order upwind, 1: second order reconstruction bounded by the global minimum/maximum of the volume fraction, 2: compressive. Value between 0 and 2: blended scheme.',
                                    'virtual_mass' : 'Include the virtual mass force that is present when a secondary phase accelerates relative to the primary phase?',
                                    'visc_disp_factor' : 'Set the dissipation intensity.',
                                    'vmass_coeff' : 'Specify the virtual mass coefficient for each pair of phases.',
                                    'vmass_implicit_options' : 'Select the virtual mass implicit option.',
                                    'vmass_implicit' : 'Enable the implicit method for the virtual mass force?',
                                    'wall_adhesion' : 'Enable the specification for a wall adhesion angle?',
                                }

                            class virtual_mass(metaclass=PyMenuMeta):
                                __doc__ = 'Enter the menu to set virtual mass models.'
                                doc_by_method = {
                                    'cavitation' : 'Set the vaporization pressure, the surface tension coefficient, and the non-condensable gas mass fraction.',
                                    'interphase_discr' : 'Enable the phase localized compressive discretization scheme where the degree of diffusion/sharpness is controlled through the value of the slope limiters?',
                                    'interphase_visc_disp' : 'Enable the interfacial viscous dissipation method, which introduces an artificial viscous damping term in the momentum equation?',
                                    'jump_adhesion' : 'Enable the treatment of the contact angle specification at the porous jump boundary?',
                                    'lift' : '',
                                    'lift_montoya' : 'Include the Montoya correction for Lift',
                                    'lift_shaver_podowski' : 'Include the Shaver-Podowski correction for Lift',
                                    'sfc_model_type' : 'Select the surface tension model.',
                                    'sfc_modeling' : 'Include the effects of surface tension along the fluid-fluid interface?',
                                    'sfc_tension_coeff' : 'Specify the surface tension coefficient for each pair of phases.',
                                    'slope_limiter' : 'Specify the slope limiter to set a specific discretization scheme. 0: first order upwind, 1: second order reconstruction bounded by the global minimum/maximum of the volume fraction, 2: compressive. Value between 0 and 2: blended scheme.',
                                    'virtual_mass' : 'Include the virtual mass force that is present when a secondary phase accelerates relative to the primary phase?',
                                    'visc_disp_factor' : 'Set the dissipation intensity.',
                                    'vmass_coeff' : 'Specify the virtual mass coefficient for each pair of phases.',
                                    'vmass_implicit_options' : 'Select the virtual mass implicit option.',
                                    'vmass_implicit' : 'Enable the implicit method for the virtual mass force?',
                                    'wall_adhesion' : 'Enable the specification for a wall adhesion angle?',
                                }

                class iac_expert(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the IAC expert setting menu'
                    doc_by_method = {
                        'ishii_kim_model' : 'set ik model coefficients',
                        'hibiki_ishii_model' : 'set hi model coefficients',
                        'yao_morel_model' : 'set ym model coefficients',
                        'iac_pseudo_time_step' : 'set iac pseudo-time',
                    }

            class wet_steam(metaclass=PyMenuMeta):
                __doc__ = 'Enter the wet steam model menu.'
                doc_by_method = {
                    'enable' : 'Enable/disable the wet steam model.',
                    'compile_user_defined_wetsteam_functions' : 'Compile user-defined wet steam library.',
                    'load_unload_user_defined_wetsteam_library' : 'Load or unload user-defined wet steam library.',
                }

                class set(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the set menu for setting wet steam model options.'
                    doc_by_method = {
                        'max_liquid_mass_fraction' : 'Set the maximum limit on the condensed liquid-phase mass-fraction to prevent divergence.',
                        'droplet_growth_rate' : 'Select the formula to model the droplet growth rate.',
                        'virial_equation' : 'Select the formulation of the virial equation of state and associated equations for thermodynamic properties of steam.',
                        'rgp_tables' : 'Select which properties to use: build-in or from RGP tables.',
                        'stagnation_conditions' : 'If the gas phase is selected, zero wetness is assumed when evaluating total or static values of pressure and temperature.',
                    }

            class population_balance(metaclass=PyMenuMeta):
                __doc__ = 'Enter the population balance model menu.'
                doc_by_method = {
                    'model' : 'Select the population balance model.',
                    'include_expansion' : 'set expansion',
                    'size_calculator' : 'calculate fluid particle diameters using different methods',
                }

                class phenomena(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the phenomena menu for population balance.'
                    doc_by_method = {
                        'nucleation' : 'Set the nucleantion rate.',
                        'growth' : 'Set the growth rate.',
                        'aggregation' : 'Set the aggregation kernel.',
                        'breakage' : 'Set the breakage kernel.',
                        'aggregation_factor' : 'Set a factor which controls the intensity of the selected aggregation kernel.',
                        'breakage_factor' : 'Set a factor which controls the intensity of the selected breakage kernel.',
                        'breakage_aggregation_vof_cutoff' : 'control vof cut-off for breakage and aggregation',
                    }

                class expert(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the expert menu for quadrature-based population balance method.'

                    class qmom(metaclass=PyMenuMeta):
                        __doc__ = ''
                        doc_by_method = {
                            'realizable_moments' : 'Set the population balance model.',
                            'print_realizable_moment_warning' : 'Print the information for realizable moments in the population balance model.',
                            'inversion_algorithm' : 'Select the inversion algorithm for quadrature-based population balance method.',
                        }

            class explicit_expert_options(metaclass=PyMenuMeta):
                __doc__ = 'Expert options for explicit formulation.'
                doc_by_method = {
                    'sub_time_step_method' : 'Select sub-time step method for the time integration in explicit formulation',
                    'solve_vof_every_iter' : 'Solve volume fraction equation every iteration for explicit formulation',
                }

                class volume_fraction_filtering(metaclass=PyMenuMeta):
                    __doc__ = 'Advanced volume fraction filtering controls for explicit formulation'
                    doc_by_method = {
                        'enable' : 'enable volume fraction filtering treatment',
                        'filtering_options' : 'select volume fraction filtering method',
                        'vol_frac_cutoff' : 'Enter node-averaged volume fraction cutoff.',
                    }

        class nox_parameters(metaclass=PyMenuMeta):
            __doc__ = 'Enter the NOx parameters menu.'
            doc_by_method = {
                'nox_chemistry' : 'Select NOx chemistry model.',
                'nox_turbulence_interaction' : 'Set NOx-turbulence interaction model.',
                'inlet_diffusion' : 'Enable/disable inclusion of diffusion at inlets.',
                'nox_expert' : 'Select additional nox equations.',
            }

        class soot_parameters(metaclass=PyMenuMeta):
            __doc__ = 'Enter the soot parameters menu.'
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
            __doc__ = 'Enter the radiation models menu.'
            doc_by_method = {
                'discrete_ordinates' : 'Enable/disable the discrete ordinates radiation model.',
                'do_acceleration' : 'Enable/disable acceleration of computation of DO model',
                'non_gray_model_parameters' : 'Set parameters for non-gray model.',
                'montecarlo' : 'Enable/disable the Monte Carlo radiation model.',
                'target_cells_per_volume_cluster' : 'Enter cells per volume cluster for Monte Carlo radiation model.',
                's2s' : 'Enable/disable the S2S radiation model.',
                'discrete_transfer' : 'Enable/disable discrete the transfer radiation model.',
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
                'wsggm_cell_based' : 'Enable/disable WSGGM cell based method.',
                'fast_second_order_discrete_ordinate' : 'Enable/disable the fast-second-order option for Discrete Ordinate Model.',
                'do_coupling' : 'Enabled DO Energy Coupling.',
                'solution_method_for_do_coupling' : 'Enable the solution method for DO/Energy  Coupling.',
                'beta_radiation_features' : 'Enable Radiation Models with Non-Iterative Time Advancement (NITA) as Beta features in FL12.0',
                'method_partially_specular_wall' : 'Set method for partially specular wall with discrete ordinate model.',
                'blending_factor' : 'Set numeric option for Discrete Ordinate model.',
            }

            class s2s_parameters(metaclass=PyMenuMeta):
                __doc__ = 'Enter the S2S parameters menu.'
                doc_by_method = {
                    'compute_vf_only' : 'Compute/write view factors only.',
                    'compute_write_vf' : 'Compute/write surface clusters and view factors for S2S radiation model.',
                    'compute_vf_accelerated' : 'Compute/Write view factors from existing surface clusters.',
                    'compute_clusters_and_vf_accelerated' : 'Compute/Write surface cluster first and then view factors.',
                    'non_participating_boundary_zones_temperature' : 'Set temperature for the non-participating boundary zones.',
                    'read_vf_file' : 'Read an S2S file.',
                    'set_vf_parameters' : 'Set the parameters needed for the view factor calculations.',
                    'split_angle' : 'Set the split angle for the clustering algorithm.',
                    'set_global_faces_per_surface_cluster' : 'Set global value of faces per surface cluster for all boundary zones.',
                    'print_thread_clusters' : 'Prints the following for all boundary threads: thread-id, number of faces, faces per surface cluster, and the number of surface clusters.',
                    'print_zonewise_radiation' : 'Prints the zonewise incoming radiation, viewfactors, and average temperature.',
                    'use_old_cluster_algorithm' : 'Use the old surface clustering algorithm.',
                    'use_new_cluster_algorithm' : 'Use the new surface clustering algorithm.',
                    'compute_fpsc_values' : 'Compute only fpsc values based on current settings',
                    'enable_mesh_interface_clustering' : 'Enable clustering on mesh interfaces?',
                }

            class dtrm_parameters(metaclass=PyMenuMeta):
                __doc__ = 'Enter the DTRM parameters menu.'
                doc_by_method = {
                    'controls' : 'Set DTRM solution controls.',
                    'make_globs' : 'Make globs (coarser mesh) for radiation.',
                    'ray_trace' : 'Create DTRM rays for radiation.',
                    'check_ray_file' : 'Read DTRM rays file.',
                }

            class solar_parameters(metaclass=PyMenuMeta):
                __doc__ = 'Enter the solar parameters menu.'
                doc_by_method = {
                    'autosave_solar_data' : 'Set autosave solar data parameters.',
                    'autoread_solar_data' : 'Set autoread solar data parameters.',
                    'sun_direction_vector' : 'Set sun direction vector.',
                    'illumination_parameters' : 'Set illumination parameters.',
                    'iteration_parameters' : 'Set update parameters.',
                    'quad_tree_parameters' : 'Set quad-tree refinement parameters.',
                    'ground_reflectivity' : 'Set ground reflectivity parameters.',
                    'scattering_fraction' : 'Set scattering fraction parameters.',
                    'sol_on_demand' : 'Enable  solar load on demand.',
                    'sol_camera_pos' : 'Set camera position based on sun direction vector.',
                    'sol_adjacent_fluidcells' : 'Enable solar load for adjacent fluid cells.',
                    'use_direction_from_sol_calc' : 'Set direction computed from solar calculator.',
                    'solar_thread_control' : 'Solar thread control',
                }

        class solver(metaclass=PyMenuMeta):
            __doc__ = 'Enter the menu to select the solver.'
            doc_by_method = {
                'pressure_based' : 'Enable/disable the segregated solver.',
                'density_based_explicit' : 'Enable/disable the coupled-explicit solver.',
                'density_based_implicit' : 'Enable/disable the coupled-implicit solver.',
                'adjust_solver_defaults_based_on_setup' : 'Enable/disable adjustment of solver defaults based on setup.',
            }

        class species(metaclass=PyMenuMeta):
            __doc__ = 'Enter the species models menu.'
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

            class CHEMKIN_CFD_parameters(metaclass=PyMenuMeta):
                __doc__ = 'Enter the expert CHEMKIN-CFD parameters menu.'
                doc_by_method = {
                    'basic_options' : 'Set basic parameter options.',
                    'advanced_options' : 'Set advanced parameter options.',
                    'add_cell_monitor' : 'Add a monitor cell for debug output.',
                    'list_cell_monitors' : 'List cell monitors.',
                    'delete_cell_monitors' : 'Delete cell monitors.',
                }

        class viscous(metaclass=PyMenuMeta):
            __doc__ = 'Enter the viscous model menu.'
            doc_by_method = {
                'inviscid' : 'Enable/disable the inviscid flow model.',
                'laminar' : 'Enable/disable the laminar flow model.',
                'mixing_length' : 'Enable/disable the mixing-length (algebraic) turbulence model.',
                'zero_equation_hvac' : 'Enable/disable the zero-equation HVAC turbulence model.',
                'spalart_allmaras' : 'Enable/disable the Spalart-Allmaras turbulence model.',
                'ke1e' : 'Enable/disable the KE1E turbulence model.',
                'sa_enhanced_wall_treatment' : 'Enable/disable the enhanced wall treatment for the Spalart-Allmaras model.\nIf disabled, no smooth blending between the viscous sublayer and the\nlog-law formulation is employed, as was done in versions previous to Fluent14.',
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
            }

            class near_wall_treatment(metaclass=PyMenuMeta):
                __doc__ = 'Enter the near wall treatment menu.'
                doc_by_method = {
                    'non_equilibrium_wall_fn' : 'Enable/disable non-equilibrium wall functions.',
                    'enhanced_wall_treatment' : 'Enable/disable enhanced wall functions.',
                    'menter_lechner' : 'Enable/disable near wall treatment Menter-Lechner.',
                    'scalable_wall_functions' : 'Enable/disable scalable wall functions.',
                    'user_defined_wall_functions' : 'Enable user defined wall functions.',
                    'werner_wengle_wall_fn' : 'Enable/disable Werner-Wengle wall functions.',
                    'wf_pressure_gradient_effects' : 'Enable/disable wall function pressure-gradient effects.',
                    'wf_thermal_effects' : 'Enable/disable wall function thermal effects.',
                }

            class multiphase_turbulence(metaclass=PyMenuMeta):
                __doc__ = 'Enter the multiphase turbulence menu.'
                doc_by_method = {
                    'multiphase_options' : 'Enable/disable multiphase options.',
                    'turbulence_multiphase_models' : 'Select the k-epsilon multiphase model.',
                    'rsm_multiphase_models' : 'Enable/disable the Reynolds Stress multiphase model.',
                    'subgrid_turbulence_contribution_aiad' : 'Enable/disable the Subgrid Turbulence Contribution for the AIAD model.',
                }

            class turbulence_expert(metaclass=PyMenuMeta):
                __doc__ = 'Enter the turbulence expert menu.'
                doc_by_method = {
                    'low_re_ke' : 'Enable/disable the low-Re k-epsilon turbulence model.',
                    'low_re_ke_index' : 'Enable/disable the low-Re k-epsilon model version.',
                    'kato_launder_model' : 'Enable/disable Kato-Launder modification for production.',
                    'production_limiter' : 'Enable/disable the Production Limiter.',
                    'kw_vorticity_based_production' : 'Enable/disable vorticity based production.',
                    'kw_add_sas' : 'Enable/disable the SAS-mode with the current turbulence model.',
                    'kw_add_des' : 'Enable/disable DES-mode with the current turbulence model.',
                    'turb_add_sbes_sdes' : 'Enable/disable SBES / SDES with the current turbulence model.',
                    'sbes_sdes_hybrid_model' : 'Select the SBES / SDES hybrid model.',
                    'sbes_update_interval_k_omega' : 'Set an integer value how often the k and omega equations are updated in a transient SBES run.',
                    'sbes_sgs_option' : 'Select SBES subgrid-scale model.',
                    'sbes_les_subgrid_dynamic_fvar' : 'Enable/disable the dynamic subgrid-scale mixture fraction variance model.',
                    'turbulence_damping' : 'Enable/disable turbulence damping and set turbulence damping parameters.',
                    'rke_cmu_rotation_term' : 'Enable/disable inclusion of omega in the Cmu definition.',
                    'turb_non_newtonian' : 'Enable/disable turbulence for non-Newtonian fluids.',
                    'non_newtonian_modification' : 'Enable/disable non-Newtonian modification for Lam-Bremhorst model.',
                    'turb_pk_compressible' : 'Enable/disable turbulent production due to compressible divergence.',
                    'thermal_p_function' : 'Enable/disable the Jayatilleke P function.',
                    'restore_sst_v61' : 'Enable/disable SST formulation of v6.1.',
                }

            class geko_options(metaclass=PyMenuMeta):
                __doc__ = 'Enter the GEKO options menu.'
                doc_by_method = {
                    'wall_distance_free' : 'Enable/disable wall-distance-free version of GEKO model.',
                    'csep' : 'Set the GEKO model coefficient CSEP.',
                    'cnw' : 'Set the GEKO model coefficient CNW.',
                    'cmix' : 'Set the GEKO model coefficient CMIX.',
                    'cjet' : 'Set the GEKO model coefficient CJET.',
                    'blending_function' : 'Set the GEKO model blending function.',
                    'creal' : 'Set the GEKO model coefficient CREAL.',
                    'cnw_sub' : 'Set the GEKO model coefficient CNW_SUB.',
                    'cjet_aux' : 'Set the GEKO model coefficient CJET_AUX.',
                    'cbf_lam' : 'Set the GEKO model coefficient CBF_LAM.',
                    'cbf_tur' : 'Set the GEKO model coefficient CBF_TUR.',
                    'geko_defaults' : 'Set GEKO options to default.',
                }

            class transition_model_options(metaclass=PyMenuMeta):
                __doc__ = 'Enter the transition model options menu.'
                doc_by_method = {
                    'crossflow_transition' : 'Enable/disable crossflow transition for the intermittency transition model.',
                    'critical_reynolds_number_correlation' : 'Set the critical Reynolds number correlation.',
                    'clambda_scale' : 'Set the algebraic transition model coefficient CLAMBDA_SCALE.',
                    'capg_hightu' : 'Set the algebraic transition model coefficient CAPG_HIGHTU.',
                    'cfpg_hightu' : 'Set the algebraic transition model coefficient CFPG_HIGHTU.',
                    'capg_lowtu' : 'Set the algebraic transition model coefficient CAPG_LOWTU.',
                    'cfpg_lowtu' : 'Set the algebraic transition model coefficient CFPG_LOWTU.',
                    'ctu_hightu' : 'Set the algebraic transition model coefficient CTU_HIGHTU.',
                    'ctu_lowtu' : 'Set the algebraic transition model coefficient CTU_LOWTU.',
                    'rec_max' : 'Set the algebraic transition model coefficient REC_MAX.',
                    'rec_c1' : 'Set the algebraic transition model coefficient REC_C1.',
                    'rec_c2' : 'Set the algebraic transition model coefficient REC_C2.',
                    'cbubble_c1' : 'Set the algebraic transition model coefficient CBUBBLE_C1.',
                    'cbubble_c2' : 'Set the algebraic transition model coefficient CBUBBLE_C2.',
                    'rv1_switch' : 'Set the algebraic transition model coefficient RV1_SWITCH.',
                }

        class structure(metaclass=PyMenuMeta):
            __doc__ = 'Enter the structure model menu.'
            doc_by_method = {
                'structure_off' : 'Disable the structural model.',
                'linear_elasticity' : 'Enable the linear elasticity model.',
                'nonlinear_elasticity' : 'Enable the nonlinear elasticity model.',
                'thermal_effects' : 'Enable structure thermal effects.',
            }

            class controls(metaclass=PyMenuMeta):
                __doc__ = 'Enter the structure controls menu.'
                doc_by_method = {
                    'numerical_damping_factor' : 'Set structure damping parameters.',
                    'enhanced_strain' : 'Enable enhanced strain element.',
                    'unsteady_damping_rayleigh' : 'Enable/disable Newmark unsteady solution model.',
                    'amg_stabilization' : 'Set the AMG stabilization method for structural solver.',
                    'max_iter' : 'Set the maximum number of iterations for structural solver.',
                }

            class expert(metaclass=PyMenuMeta):
                __doc__ = 'Enter the structure expert menu.'
                doc_by_method = {
                    'include_pop_in_fsi_force' : 'Enable inclusion of operating p into fsi force.',
                    'include_viscous_fsi_force' : 'Enable inclusion of viscous fsi force.',
                    'explicit_fsi_force' : 'Enable explicit fsi force.',
                }

        class heat_exchanger(metaclass=PyMenuMeta):
            __doc__ = 'Enter the heat exchanger menu.'

            class macro_model(metaclass=PyMenuMeta):
                __doc__ = 'Enter the heat macro-model menu.'
                doc_by_method = {
                    'heat_exchanger' : 'Enable/disable heat-exchanger model.',
                    'heat_exchanger_model' : 'Define heat-exchanger core model.',
                    'heat_exchanger_zone' : 'Define heat-exchanger zone.',
                    'heat_exchanger_group' : 'Define heat-exchanger group.',
                    'delete_heat_exchanger_group' : 'Delete heat-exchanger group.',
                    'heat_exchanger_report' : 'Report heat-exchanger information.',
                    'heat_exchanger_macro_report' : 'Report heat-exchanger information for all the macros.',
                    'plot_NTU' : 'Plot NTU vs primary mass flow rate for each auxiliary mass flow rate.',
                    'write_NTU' : 'Write NTU vs primary mass flow rate for each auxiliary mass flow rate.',
                }

            class dual_cell_model(metaclass=PyMenuMeta):
                __doc__ = 'Enter the dual cell model menu.'
                doc_by_method = {
                    'heat_exchanger' : 'Enable/disable the dual cell heat-exchanger model.',
                    'add_heat_exchanger' : 'Add heat-exchanger.',
                    'modify_heat_exchanger' : 'Modify heat-exchanger.',
                    'delete_heat_exchanger' : 'Delete heat-exchanger.',
                    'plot_NTU' : 'Plot NTU vs primary mass flow rate for each auxiliary mass flow rate.',
                    'write_NTU' : 'Write NTU vs primary mass flow rate for each auxiliary mass flow rate.',
                    'alternative_formulation' : 'Enable/disable alternative formulation for heat transfer calculations.',
                }

    class named_expressions(metaclass=PyMenuMeta):
        __doc__ = 'Manage named expressions'
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
        __doc__ = 'Enter the define operating conditions menu.'
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
        __doc__ = 'Enter the overset-interfaces menu.'
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
            __doc__ = 'Enter the overset interface options menu.'
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
            __doc__ = 'Enter the overset hole cut control menu.'
            doc_by_method = {
                'add' : 'Add hole cut control for a boundary zone.',
                'delete' : 'Delete hole cut control for a boundary zone.',
                'delete_all' : 'Delete the hole cut controls for all boundary zones.',
                'list' : 'List the defined hole cut controls.',
            }

            class cut_seeds(metaclass=PyMenuMeta):
                __doc__ = 'Enter the overset hole cut seed menu.'
                doc_by_method = {
                    'add' : 'Add a hole cut seed.',
                    'delete' : 'Delete a hole cut seed.',
                    'delete_all' : 'Delete all hole cut seeds.',
                    'list' : 'List the defined hole cut seeds.',
                    'cut_seeds_for_all_component_zones' : 'Enable that all component zones get a cut seed.',
                }

        class adapt(metaclass=PyMenuMeta):
            __doc__ = 'Enter the overset adaption menu.'
            doc_by_method = {
                'mark_adaption' : 'Mark cells for overset orphan adaption and donor-receptor size differences.',
                'adapt_mesh' : 'Mark and adapt the mesh to remove orphan cells and large donor-receptor cell size differences.',
            }

            class set(metaclass=PyMenuMeta):
                __doc__ = 'Enter the overset adaption set menu.'
                doc_by_method = {
                    'mark_orphans' : 'Enable the option to adapt for orphan reduction.',
                    'mark_fixed_orphans' : 'Enable the option to adapt for orphans which were removed by accepting neighbor donors.',
                    'mark_size' : 'Enable the option to adapt for donor-receptor cell size differences.',
                    'mark_gaps' : 'Enable the option to adapt underresolved gaps.',
                    'mark_coarsening' : 'Enable the option to coarsen the mesh during overset adaption.',
                    'anisotropic' : 'Enable the option to use anisotropic adaption in prismatic cells.',
                    'automatic' : 'Enable the option to automatically adapt overset meshes during solution update.',
                    'length_ratio_max' : 'Set the length scale ratio threshold used to determine which cells are marked for adaption based on donor-receptor cell size differences.',
                    'buffer_layers' : 'Set the number of cell layers marked in addition to the cells marked for orphan adaption.',
                    'adaption_sweeps' : 'Set the number of adaption sweeps per overset adaption.',
                    'maximum_refinement_level' : 'Set the maximum level of refinement in overset adaption.',
                }

    class reference_frames(metaclass=PyMenuMeta):
        __doc__ = 'Manage reference frames'
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
        __doc__ = 'Reference value menu.'
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
            __doc__ = 'Enter the compute menu.'
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
        __doc__ = 'Turbo features menu.'
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
            __doc__ = 'Define turbo topology.'
            doc_by_method = {
                'define_topology' : 'Define a turbo topology.',
                'mesh_method' : 'Set turbo structured mesh generation method.',
                'search_method' : 'Set search method for a topology.',
                'projection_method' : 'Set 2D projection method.',
                'delete' : 'Delete a turbo topology.',
            }

        class general_turbo_interface_settings(metaclass=PyMenuMeta):
            __doc__ = 'Set General Turbo Interface options'

            class mixing_plane_model_settings(metaclass=PyMenuMeta):
                __doc__ = 'Set the mixing plane model settings'
                doc_by_method = {
                    'averaging_method' : 'Set the averaging method for the mixing.',
                    'mixing_set_constraint' : 'To set the mixing of primitive or total variable approach',
                    'bands_type' : 'To set the mixing plane bands type',
                    'number_of_inner_iterations' : 'To set the number of iteration used for the scaling',
                    'list_mixing_planes' : 'List the settings of mixing planes in the case.',
                }

                class number_of_bands(metaclass=PyMenuMeta):
                    __doc__ = 'Set the maximum number of bands to be used for mixing'
                    doc_by_method = {
                        'set_specific_interface' : 'Set number of band to be used for mixing',
                        'set_all_interfaces' : 'Set number of band to be used for mixing',
                    }

            class pitch_scale_model_settings(metaclass=PyMenuMeta):
                __doc__ = 'Set the pitch scale model settings'
                doc_by_method = {
                    'scale_mflux' : 'Scale mass flux to improve the conservation',
                }

            class no_pitch_scale_model_settings(metaclass=PyMenuMeta):
                __doc__ = 'Set the no pitch scale model settings'
                doc_by_method = {
                    'scale_mflux' : 'Scale mass flux to improve the conservation',
                }

            class expert(metaclass=PyMenuMeta):
                __doc__ = 'Set the expert parameters for turbo interfaces'
                doc_by_method = {
                    'enforce_flux_scaling' : 'Enforce flux scaling ON/OFF at the turbo interfaces.',
                    'list_settings' : 'List the flux scale settings at the turbo interfaces',
                }

        class blade_flutter_harmonics(metaclass=PyMenuMeta):
            __doc__ = 'Enter the blade flutter harmonics menu.'
            doc_by_method = {
                'enable_harmonic_postprocessing' : 'Calculates/Deletes Postprocessing Fourier coefficients data',
                'enable_harmonic_exports' : 'Calculates/Deletes flutter harmonic export data',
                'write_harmonic_exports' : 'Writes harmonic export data',
            }

class simulation_reports(metaclass=PyMenuMeta):
    __doc__ = 'Enter the simulation reports menu.'
    doc_by_method = {
        'list_simulation_reports' : 'List all report names.',
        'generate_simulation_report' : 'Generate a new simulation report or regenerate an existing simulation report with the provided name.',
        'view_simulation_report' : "View a simulation report that has already been generated. In batch mode this will print the report's URL.",
        'export_simulation_report_as_pdf' : 'Export the provided simulation report as a PDF file.',
        'export_simulation_report_as_html' : 'Export the provided simulation report as HTML.',
        'write_report_names_to_file' : 'Write the list of currently generated report names to a txt file.',
        'rename_simulation_report' : 'Rename a report which has already been generated.',
        'duplicate_simulation_report' : 'Duplicate a report and all of its settings to a new report.',
        'reset_report_to_defaults' : 'Reset all report settings to default for the provided simulation report.',
        'delete_simulation_report' : 'Delete the provided simulation report.',
        'write_simulation_report_template_file' : "Write a JSON template file with this case's Simulation Report settings.",
        'read_simulation_report_template_file' : 'Read a JSON template file with existing Simulation Report settings.',
    }

class server(metaclass=PyMenuMeta):
    __doc__ = 'Enter the server menu.'
    doc_by_method = {
        'start_server' : 'Start server.',
        'start_client' : 'Start client.',
        'print_server_address' : 'Print server address.',
        'write_or_reset_server_info' : 'Write/Reset server info.',
        'print_connected_clients' : 'Print connected clients.',
        'shutdown_server' : 'Shutdown server.',
    }

class turbo_post(metaclass=PyMenuMeta):
    __doc__ = 'Enter the turbo menu.'
    doc_by_method = {
        'compute_report' : 'Compute the turbo report.',
        'write_report' : 'Write the turbo report to file.',
        'avg_contours' : 'Display average contours.',
        'two_d_contours' : 'Display 2d contours.',
        'xy_plot_avg' : 'Display average xy plot.',
        'current_topology' : 'Set the current turbo topology for global use.',
    }

class parametric_study(metaclass=PyMenuMeta):
    __doc__ = 'Enter the parametric study menu'
    doc_by_method = {
        'initialize' : 'Start Parametric Study',
        'duplicate_study' : 'Duplicate Parametric Study',
        'export_design_table' : 'Enter the design table menu',
    }

    class design_points(metaclass=PyMenuMeta):
        __doc__ = 'Enter the design points menu'
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
        __doc__ = 'Enter the update menu'
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
    __doc__ = 'Enter the turbo workflow menu'

    class workflow(metaclass=PyMenuMeta):
        __doc__ = 'Enter the workflow menu'
        doc_by_method = {
            'enable' : 'Enable the workflow',
            'reset' : 'Reset the workflow',
            'disable' : 'Disable the workflow',
        }
