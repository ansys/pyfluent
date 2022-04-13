"""Fluent Meshing TUI Commands"""
#
# This is an auto-generated file.  DO NOT EDIT!
#
# pylint: disable=line-too-long

from ansys.fluent.core.meta import PyMenuMeta, PyNamedObjectMeta
from ansys.fluent.core.services.datamodel_tui import PyMenu


class main_menu(metaclass=PyMenuMeta):
    """
    Fluent meshing main menu.
    """
    def __init__(self, path, service):
        self.path = path
        self.service = service
        self.file = self.__class__.file(path + [("file", None)], service)
        self.boundary = self.__class__.boundary(path + [("boundary", None)], service)
        self.cad_assemblies = self.__class__.cad_assemblies(path + [("cad_assemblies", None)], service)
        self.preferences = self.__class__.preferences(path + [("preferences", None)], service)
        self.size_functions = self.__class__.size_functions(path + [("size_functions", None)], service)
        self.scoped_sizing = self.__class__.scoped_sizing(path + [("scoped_sizing", None)], service)
        self.objects = self.__class__.objects(path + [("objects", None)], service)
        self.diagnostics = self.__class__.diagnostics(path + [("diagnostics", None)], service)
        self.material_point = self.__class__.material_point(path + [("material_point", None)], service)
        self.mesh = self.__class__.mesh(path + [("mesh", None)], service)
        self.display = self.__class__.display(path + [("display", None)], service)
        self.report = self.__class__.report(path + [("report", None)], service)
        self.parallel = self.__class__.parallel(path + [("parallel", None)], service)
        self.openmp_controls = self.__class__.openmp_controls(path + [("openmp_controls", None)], service)
        self.reference_frames = self.__class__.reference_frames(path + [("reference_frames", None)], service)
    def beta_feature_access(self, *args, **kwargs):
        """
        Enable access to beta features in the interface.
        """
        return PyMenu(self.service, "/beta_feature_access").execute(*args, **kwargs)
    def close_fluent(self, *args, **kwargs):
        """
        (ANSYS Fluent in Workbench only) Exits program.
        """
        return PyMenu(self.service, "/close_fluent").execute(*args, **kwargs)
    def exit(self, *args, **kwargs):
        """
        Exits the program.
        """
        return PyMenu(self.service, "/exit").execute(*args, **kwargs)
    def switch_to_solution_mode(self, *args, **kwargs):
        """
        Enables you to transfer the mesh data from meshing mode to solution mode in ANSYS Fluent. When you use the switch-to-solution-mode command, you will be asked to confirm that you want to switch to solution mode.
        """
        return PyMenu(self.service, "/switch_to_solution_mode").execute(*args, **kwargs)
    def print_license_usage(self, *args, **kwargs):
        """
        Print license usage information.
        """
        return PyMenu(self.service, "/print_license_usage").execute(*args, **kwargs)

    class file(metaclass=PyMenuMeta):
        """
        Enter the file menu.
        """
        def __init__(self, path, service):
            self.path = path
            self.service = service
            self.export = self.__class__.export(path + [("export", None)], service)
            self.import_ = self.__class__.import_(path + [("import", None)], service)
            self.checkpoint = self.__class__.checkpoint(path + [("checkpoint", None)], service)
            self.project = self.__class__.project(path + [("project[beta]", None)], service)
        def append_mesh(self, *args, **kwargs):
            """
            Enables you to append the mesh files. This command is available only after a mesh file has been read in.
            """
            return PyMenu(self.service, "/file/append_mesh").execute(*args, **kwargs)
        def append_meshes_by_tmerge(self, *args, **kwargs):
            """
            Enables you to append the mesh files using the tmerge utility. This command is available only after a mesh file has been read in.
            """
            return PyMenu(self.service, "/file/append_meshes_by_tmerge").execute(*args, **kwargs)
        def file_format(self, *args, **kwargs):
            """
            Enables/disables the writing of binary files. 
            """
            return PyMenu(self.service, "/file/file_format").execute(*args, **kwargs)
        def filter_list(self, *args, **kwargs):
            """
            Lists the names of the converters that are used to change foreign mesh (while importing mesh files from third-party packages) files. 
            """
            return PyMenu(self.service, "/file/filter_list").execute(*args, **kwargs)
        def filter_options(self, *args, **kwargs):
            """
            Enables you to change the extension (such as .cas, .msh, .neu) and arguments used with a specified filter.   For example, if you saved the PATRAN files with a .NEU extension instead of .neu, you can substitute or add .NEU to the extension list. For some filters, one of the arguments will be the dimensionality of the grid.   When you use the filter-options command for such a filter, you will see a default dimensionality argument of -d a. The dimension will automatically be determined, so you need not substitute 2 or 3 for a. 
            """
            return PyMenu(self.service, "/file/filter_options").execute(*args, **kwargs)
        def hdf_files(self, *args, **kwargs):
            """
            Indicate whether to write Ansys common fluids format (CFF) files or legacy case files.
            """
            return PyMenu(self.service, "/file/hdf_files").execute(*args, **kwargs)
        def cff_files(self, *args, **kwargs):
            """
            Answering yes will set the Common Fluids Format (CFF) as the default file format for reading and writing case/data files.
            """
            return PyMenu(self.service, "/file/cff_files").execute(*args, **kwargs)
        def read_boundary_mesh(self, *args, **kwargs):
            """
            Enables you to read a boundary mesh. If the boundary mesh is contained in two or more separate files, you can read them in together and assemble the complete boundary mesh.   This option is also convenient if you want to reuse the boundary mesh from a file containing a large volume mesh.   The naming of face zones can be controlled by Named Selections defined in Ansys Workbench. For details on exporting faceted geometry from Ansys Workbench, refer to the Ansys Workbench Help. 
            """
            return PyMenu(self.service, "/file/read_boundary_mesh").execute(*args, **kwargs)
        def read_mesh(self, *args, **kwargs):
            """
            Enables you to read a mesh file. You can also use this command to read a Fluent mesh file created with GAMBIT, or to read the mesh available in a Fluent case file.   Reading a case file as a mesh file will result in loss of boundary condition data as the mesh file does not contain any information on boundary conditions.  Case files containing polyhedral cells can also be read in the meshing mode of Fluent. You can display the polyhedral mesh, perform certain mesh manipulation operations, check the mesh quality, and so on. Important:  You cannot read meshes from solvers that have been adapted using hanging nodes. To read one of these meshes in the meshing mode in Fluent, coarsen the mesh within the solver until you have recovered the original unadapted grid.   The naming of face zones can be controlled by Named Selections defined in Ansys Workbench. For details on exporting faceted geometry from Ansys Workbench, refer to the Ansys Workbench Help. 
            """
            return PyMenu(self.service, "/file/read_mesh").execute(*args, **kwargs)
        def read_meshes_by_tmerge(self, *args, **kwargs):
            """
            Uses the tmerge utility to read the mesh contained in two or more separate files. It enables you to read the mesh files together and helps assemble the complete mesh. 
            """
            return PyMenu(self.service, "/file/read_meshes_by_tmerge").execute(*args, **kwargs)
        def read_multi_bound_mesh(self, *args, **kwargs):
            """
            Enables you to read multiple boundary mesh files into the meshing mode. 
            """
            return PyMenu(self.service, "/file/read_multi_bound_mesh").execute(*args, **kwargs)
        def read_case(self, *args, **kwargs):
            """
            Enables you to read the mesh contained in a case file.   Cell hierarchy in case files adapted in the solution mode will be lost when they are read in the meshing mode.  Case files containing polyhedral cells can also be read in the meshing mode of Fluent. You can display the polyhedral mesh, perform certain mesh manipulation operations, check the mesh quality, and so on.
            """
            return PyMenu(self.service, "/file/read_case").execute(*args, **kwargs)
        def read_domains(self, *args, **kwargs):
            """
            Enables you to read domain files.   Each mesh file written by Fluent has a domain section. A domain file is the domain section of the mesh file and is written as a separate file. It contains a list of node, face, and cell zone IDs that make up each domain in the mesh.   If a domain that is being read already exists in the mesh, a warning message is displayed. Fluent verifies if the zones defining the domains exist in the mesh. If not, it will display a warning message. 
            """
            return PyMenu(self.service, "/file/read_domains").execute(*args, **kwargs)
        def read_size_field(self, *args, **kwargs):
            """
            Enables you to read in a size field file.  If you read a size-field file after scaling the model, ensure that the size-field file is appropriate for the scaled model (size-field vertices should match the scaled model).
            """
            return PyMenu(self.service, "/file/read_size_field").execute(*args, **kwargs)
        def write_size_field(self, *args, **kwargs):
            """
            Enables you to write a size field file.
            """
            return PyMenu(self.service, "/file/write_size_field").execute(*args, **kwargs)
        def read_journal(self, *args, **kwargs):
            """
            Enables you to read a journal file into the program.   The read-journal command always loads the file in the main (that is, top-level) menu, regardless of where you are in the menu hierarchy when you invoke it. 
            """
            return PyMenu(self.service, "/file/read_journal").execute(*args, **kwargs)
        def read_mesh_vars(self, *args, **kwargs):
            """
            Reads mesh varaibles from a mesh file.
            """
            return PyMenu(self.service, "/file/read_mesh_vars").execute(*args, **kwargs)
        def read_multiple_mesh(self, *args, **kwargs):
            """
            Enables you to read in two or more files together and have the complete mesh assembled for you, if the mesh files are contained in two or more separate files.   For example, if you are going to create a hybrid mesh by reading in a triangular boundary mesh and a volume mesh consisting of hexahedral cells, you can read both files at the same time using this command. 
            """
            return PyMenu(self.service, "/file/read_multiple_mesh").execute(*args, **kwargs)
        def read_options(self, *args, **kwargs):
            """
            Enables you to set the following options for reading mesh files: 
            """
            return PyMenu(self.service, "/file/read_options").execute(*args, **kwargs)
        def show_configuration(self, *args, **kwargs):
            """
            Displays the current release and version information. 
            """
            return PyMenu(self.service, "/file/show_configuration").execute(*args, **kwargs)
        def start_journal(self, *args, **kwargs):
            """
            Starts recording all input and writes it to a file. The current Fluent version is automatically recorded in the journal file. Note that commands entered using paths from older versions of Fluent will be upgraded to their current path in the journal file. See .
            """
            return PyMenu(self.service, "/file/start_journal").execute(*args, **kwargs)
        def start_transcript(self, *args, **kwargs):
            """
            Starts recording input and output in a file.   A transcript file contains a complete record of all standard input to and output from Fluent (usually all keyboard and user interface input and all screen output).Start the transcription process with the file/start-transcript command, and end it with the file/stop-
                           transcript command (or by exiting the program). 
                              file/start-transcript
                           
                           
                              file/stop-transcript
                           
                        
            """
            return PyMenu(self.service, "/file/start_transcript").execute(*args, **kwargs)
        def stop_journal(self, *args, **kwargs):
            """
            Stops recording input and closes the journal file. 
            """
            return PyMenu(self.service, "/file/stop_journal").execute(*args, **kwargs)
        def stop_transcript(self, *args, **kwargs):
            """
            Stops recording input and output, and closes the transcript file. 
            """
            return PyMenu(self.service, "/file/stop_transcript").execute(*args, **kwargs)
        def confirm_overwrite(self, *args, **kwargs):
            """
            Controls whether attempts to overwrite existing files require confirmation.  If you do not want ANSYS Fluent to ask you for confirmation before it overwrites existing files, you can enter the file/confirm-overwrite? text command and answer no.
            """
            return PyMenu(self.service, "/file/confirm_overwrite").execute(*args, **kwargs)
        def write_boundaries(self, *args, **kwargs):
            """
            Enables you to write the specified boundaries into a mesh file.   This is useful for large cases where you may want to mesh different parts of the mesh separately and then merge them together. This enables you to avoid frequent switching between domains for such cases. You can write out selected boundaries to a mesh file and then create the volume mesh for the part in a separate session. You can then read the saved mesh into the previous session and merge the part with the rest of the mesh. 
            """
            return PyMenu(self.service, "/file/write_boundaries").execute(*args, **kwargs)
        def write_case(self, *args, **kwargs):
            """
            Enables you to write a case file that can be read by Fluent.   You should delete dead zones in the mesh before writing the mesh or case file for Fluent.
            """
            return PyMenu(self.service, "/file/write_case").execute(*args, **kwargs)
        def write_domains(self, *args, **kwargs):
            """
            Enables you to write all the mesh domains (except global) into a file that can be read. 
            """
            return PyMenu(self.service, "/file/write_domains").execute(*args, **kwargs)
        def write_mesh(self, *args, **kwargs):
            """
            Enables you to write a mesh file.   You should delete dead zones in the mesh before writing the mesh or case file for Fluent.
            """
            return PyMenu(self.service, "/file/write_mesh").execute(*args, **kwargs)
        def write_mesh_vars(self, *args, **kwargs):
            """
            Writes mesh varaibles to a file.
            """
            return PyMenu(self.service, "/file/write_mesh_vars").execute(*args, **kwargs)
        def write_options(self, *args, **kwargs):
            """
            Allows you to enable or disable the enforce mesh topology option for writing mesh/case files.   This option is enabled by default; where it will orient the face zones consistently when the mesh file is written. If necessary, the zones will be separated, such that each boundary face zone has at most two cell zones as neighbors, one on either side. Also, internal face zones will be inserted between neighboring cell zones that are connected by interior faces. 
            """
            return PyMenu(self.service, "/file/write_options").execute(*args, **kwargs)
        def set_idle_timeout(self, *args, **kwargs):
            """
            Allows you to set an idle timeout so that an idle ANSYS Fluent session will automatically save and close after the specified time.
            """
            return PyMenu(self.service, "/file/set_idle_timeout").execute(*args, **kwargs)
        def load_act_tool(self, *args, **kwargs):
            """
            Loads the Ansys ACT tool.
            """
            return PyMenu(self.service, "/file/load_act_tool").execute(*args, **kwargs)
        def set_tui_version(self, *args, **kwargs):
            """
            Allows you to improve backwards compatibility for journal files. This command hides any new TUI prompts that are added at a future release of ANSYS Fluent and reverts to the arguments of the release that you specify using the command (within two full releases of the current release). The command is automatically added to a journal file as soon as you start the recording. See  for details.
            """
            return PyMenu(self.service, "/file/set_tui_version").execute(*args, **kwargs)

        class export(metaclass=PyMenuMeta):
            """
            Exports case and data information.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def ansys(self, *args, **kwargs):
                """
                Write a Ansys mesh file.
                """
                return PyMenu(self.service, "/file/export/ansys").execute(*args, **kwargs)
            def hypermesh(self, *args, **kwargs):
                """
                Write a HYPERMESH ascii file.
                """
                return PyMenu(self.service, "/file/export/hypermesh").execute(*args, **kwargs)
            def nastran(self, *args, **kwargs):
                """
                Writes a NASTRAN file.
                """
                return PyMenu(self.service, "/file/export/nastran").execute(*args, **kwargs)
            def patran(self, *args, **kwargs):
                """
                Write a PATRAN mesh file.
                """
                return PyMenu(self.service, "/file/export/patran").execute(*args, **kwargs)
            def stl(self, *args, **kwargs):
                """
                Write a STL boundary mesh file.
                """
                return PyMenu(self.service, "/file/export/stl").execute(*args, **kwargs)

        class import_(metaclass=PyMenuMeta):
            """
            Enables you to import mesh information generated by some CAD packages (Ansys, I-deas, NASTRAN, PATRAN, and HYPERMESH), as well as mesh information in the CGNS (CFD general notation system) format. 
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
                self.cad_options = self.__class__.cad_options(path + [("cad_options", None)], service)
            def ansys_surf_mesh(self, *args, **kwargs):
                """
                Enables you to read a Ansys surface mesh file. 
                """
                return PyMenu(self.service, "/file/import/ansys_surf_mesh").execute(*args, **kwargs)
            def ansys_vol_mesh(self, *args, **kwargs):
                """
                Enables you to read a Ansys volume mesh file. 
                """
                return PyMenu(self.service, "/file/import/ansys_vol_mesh").execute(*args, **kwargs)
            def cgns_vol_mesh(self, *args, **kwargs):
                """
                Enables you to read a CGNS volume mesh file. 
                """
                return PyMenu(self.service, "/file/import/cgns_vol_mesh").execute(*args, **kwargs)
            def cgns_surf_mesh(self, *args, **kwargs):
                """
                Enables you to read a CGNS surface mesh file. 
                """
                return PyMenu(self.service, "/file/import/cgns_surf_mesh").execute(*args, **kwargs)
            def fidap_surf_mesh(self, *args, **kwargs):
                """
                Enables you to read a FIDAP surface mesh file. 
                """
                return PyMenu(self.service, "/file/import/fidap_surf_mesh").execute(*args, **kwargs)
            def fidap_vol_mesh(self, *args, **kwargs):
                """
                Enables you to read a FIDAP volume mesh file. 
                """
                return PyMenu(self.service, "/file/import/fidap_vol_mesh").execute(*args, **kwargs)
            def fl_uns2_mesh(self, *args, **kwargs):
                """
                Enables you to read a Fluent UNS V2 case file. 
                """
                return PyMenu(self.service, "/file/import/fl_uns2_mesh").execute(*args, **kwargs)
            def fluent_2d_mesh(self, *args, **kwargs):
                """
                Enables you to read a 2D mesh into the 3D version. 
                """
                return PyMenu(self.service, "/file/import/fluent_2d_mesh").execute(*args, **kwargs)
            def fluent_3d_mesh(self, *args, **kwargs):
                """
                Read a 3D mesh.
                """
                return PyMenu(self.service, "/file/import/fluent_3d_mesh").execute(*args, **kwargs)
            def gambit_surf_mesh(self, *args, **kwargs):
                """
                Enables you to read a GAMBIT surface mesh file. 
                """
                return PyMenu(self.service, "/file/import/gambit_surf_mesh").execute(*args, **kwargs)
            def gambit_vol_mesh(self, *args, **kwargs):
                """
                Enables you to read a GAMBIT volume mesh file. 
                """
                return PyMenu(self.service, "/file/import/gambit_vol_mesh").execute(*args, **kwargs)
            def hypermesh_surf_mesh(self, *args, **kwargs):
                """
                Enables you to read a HYPERMESH surface mesh file. 
                """
                return PyMenu(self.service, "/file/import/hypermesh_surf_mesh").execute(*args, **kwargs)
            def hypermesh_vol_mesh(self, *args, **kwargs):
                """
                Enables you to read a HYPERMESH volume mesh file. 
                """
                return PyMenu(self.service, "/file/import/hypermesh_vol_mesh").execute(*args, **kwargs)
            def ideas_surf_mesh(self, *args, **kwargs):
                """
                Enables you to read an I-deas surface mesh file. 
                """
                return PyMenu(self.service, "/file/import/ideas_surf_mesh").execute(*args, **kwargs)
            def ideas_vol_mesh(self, *args, **kwargs):
                """
                Enables you to read an I-deas volume mesh file. 
                """
                return PyMenu(self.service, "/file/import/ideas_vol_mesh").execute(*args, **kwargs)
            def nastran_surf_mesh(self, *args, **kwargs):
                """
                Enables you to read a NASTRAN surface mesh file. 
                """
                return PyMenu(self.service, "/file/import/nastran_surf_mesh").execute(*args, **kwargs)
            def nastran_vol_mesh(self, *args, **kwargs):
                """
                Enables you to read a NASTRAN volume mesh file. 
                """
                return PyMenu(self.service, "/file/import/nastran_vol_mesh").execute(*args, **kwargs)
            def patran_surf_mesh(self, *args, **kwargs):
                """
                Enables you to read a PATRAN surface mesh file. 
                """
                return PyMenu(self.service, "/file/import/patran_surf_mesh").execute(*args, **kwargs)
            def patran_vol_mesh(self, *args, **kwargs):
                """
                Enables you to read a PATRAN volume mesh file. 
                """
                return PyMenu(self.service, "/file/import/patran_vol_mesh").execute(*args, **kwargs)
            def cad(self, *args, **kwargs):
                """
                Enables you to import CAD files based on the options set.
                """
                return PyMenu(self.service, "/file/import/cad").execute(*args, **kwargs)
            def cad_geometry(self, *args, **kwargs):
                """
                Enables you to import CAD files based on the options set.
                """
                return PyMenu(self.service, "/file/import/cad_geometry").execute(*args, **kwargs)
            def stl(self, *args, **kwargs):
                """
                Read a surface mesh from a stereolithography (STL) file.
                """
                return PyMenu(self.service, "/file/import/stl").execute(*args, **kwargs)
            def reimport_last_with_cfd_surface_mesh(self, *args, **kwargs):
                """
                Reimport CAD using the size field.
                """
                return PyMenu(self.service, "/file/import/reimport_last_with_cfd_surface_mesh").execute(*args, **kwargs)

            class cad_options(metaclass=PyMenuMeta):
                """
                Contains additional options for importing CAD files.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def read_all_cad_in_subdirectories(self, *args, **kwargs):
                    """
                    When enabled, all files in the specified directory as well as in its subdirectories will be imported. This option is disabled by default.
                    """
                    return PyMenu(self.service, "/file/import/cad_options/read_all_cad_in_subdirectories").execute(*args, **kwargs)
                def continue_on_error(self, *args, **kwargs):
                    """
                    Enables you to continue the import of the CAD file(s), despite errors or problems creating the faceting on certain surfaces, or other issues. This option is disabled by default.
                    """
                    return PyMenu(self.service, "/file/import/cad_options/continue_on_error").execute(*args, **kwargs)
                def save_PMDB(self, *args, **kwargs):
                    """
                    Saves a PMDB (*.pmdb) file in the directory containing the CAD files imported. You can use this file to import the same CAD file(s) again with different options set, for a quicker import than the full import. This option is disabled by default.  Some options will not be available any more once the model is imported from a PMDB file (for example, enclosure-symm-processing?), since they are processed before the PMDB file is created.
                    """
                    return PyMenu(self.service, "/file/import/cad_options/save_PMDB").execute(*args, **kwargs)
                def tessellation(self, *args, **kwargs):
                    """
                    Enables you to control the tessellation (faceting) during file import. You can select either cad-faceting or cfd-surface-mesh.   CAD faceting enables you to control the tessellation based on the CAD faceting tolerance and maximum facet size specified.   CFD Surface Mesh enables you to use a size field file, (Use size field file?). If you enter yes, specify the size field file to be read. If you do not want to use a size field file, you can obtain conformal faceting based on the underlying curve and surface curvature (using the minimum and maximum facet sizes, and the facet curvature normal angle specified) and edge proximity (using the cells per gap specified). You can also save a size field in a file (size field is computed based on the specified parameters; that is, Min Size, Max Size, Curvature Normal Angle, Cells Per Gap).
                    """
                    return PyMenu(self.service, "/file/import/cad_options/tessellation").execute(*args, **kwargs)
                def named_selections(self, *args, **kwargs):
                    """
                    Enables you to import Named Selections from the CAD file(s), including Named Selections from Ansys DesignModeler, publications from CATIA, and so on. You can additionally choose to ignore import of certain Named Selections based on the pattern specified (for example, Layer* to ignore layer Named Selections from CATIA), or by specifying multiple wild cards (for example, ^(Color|Layer|Material).* to remove color, layer, and material Named Selections from CATIA).
                    """
                    return PyMenu(self.service, "/file/import/cad_options/named_selections").execute(*args, **kwargs)
                def enclosure_symm_processing(self, *args, **kwargs):
                    """
                    Enables processing of enclosure and symmetry named selections during import. This option is disabled by default. This option is applicable only to Ansys DesignModeler (*.agdb) files.
                    """
                    return PyMenu(self.service, "/file/import/cad_options/enclosure_symm_processing").execute(*args, **kwargs)
                def reconstruct_topology(self, *args, **kwargs):
                    """
                    Reconstruct topology for STL files.
                    """
                    return PyMenu(self.service, "/file/import/cad_options/reconstruct_topology").execute(*args, **kwargs)
                def import_part_names(self, *args, **kwargs):
                    """
                    Enables import of Part names from the CAD file(s). This option is enabled by default.  Any renaming of Part names in Ansys Mechanical/Ansys Meshing prior to the export of the mechdat/meshdat files is ignored during import. Only original Part names will be imported.
                    """
                    return PyMenu(self.service, "/file/import/cad_options/import_part_names").execute(*args, **kwargs)
                def import_body_names(self, *args, **kwargs):
                    """
                    Enables import of Body names from the CAD files. This option is enabled by default.  Any renaming of Body names in Ansys Mechanical/Ansys Meshing prior to the export of the mechdat/meshdat files is ignored during import. Only original Body names will be imported.
                    """
                    return PyMenu(self.service, "/file/import/cad_options/import_body_names").execute(*args, **kwargs)
                def separate_features_by_type(self, *args, **kwargs):
                    """
                    Enables separation of feature edges based on angle, connectivity, and named selections on import. Edge zone names will have suitable suffixes depending on separation criteria, order of zones, existing zone names and other import options selected.
                    """
                    return PyMenu(self.service, "/file/import/cad_options/separate_features_by_type").execute(*args, **kwargs)
                def single_connected_edge_label(self, *args, **kwargs):
                    """
                    Adds the specified label to the name of single-connected edge zones (edge zones referenced by a single face).
                    """
                    return PyMenu(self.service, "/file/import/cad_options/single_connected_edge_label").execute(*args, **kwargs)
                def double_connected_face_label(self, *args, **kwargs):
                    """
                    Adds the specified label to the name of double-connected face zones (face zones shared by two bodies).
                    """
                    return PyMenu(self.service, "/file/import/cad_options/double_connected_face_label").execute(*args, **kwargs)
                def use_collection_names(self, *args, **kwargs):
                    """
                    Enables you to use the Named Selections for the object/zone names on import. Select auto, no, or yes. The default selection is auto where the Named Selection will be used as the object/zone name, except when the object creation granularity is set to one object per file.
                    """
                    return PyMenu(self.service, "/file/import/cad_options/use_collection_names").execute(*args, **kwargs)
                def use_component_names(self, *args, **kwargs):
                    """
                    Enables you to add the component (part or assembly) names to the object/zone names on import. Select auto, no, or yes. The default selection is auto where the component name will be added to the object/zone name.
                    """
                    return PyMenu(self.service, "/file/import/cad_options/use_component_names").execute(*args, **kwargs)
                def name_separator_character(self, *args, **kwargs):
                    """
                    :
                    """
                    return PyMenu(self.service, "/file/import/cad_options/name_separator_character").execute(*args, **kwargs)
                def object_type(self, *args, **kwargs):
                    """
                    Enables the setting of object type on import. The options available are auto, geometry, and mesh. The default setting is auto based on the tessellation method selected: geometry objects will be created when the cad-faceting  method is used, while mesh objects will be created when the cfd-surface-mesh method is used.
                    """
                    return PyMenu(self.service, "/file/import/cad_options/object_type").execute(*args, **kwargs)
                def one_object_per(self, *args, **kwargs):
                    """
                    Enables you to create one object per body/part/file/selection to be imported. The default program-controlled option allows the software to make the appropriate choice. This option makes a choice between per body and per part based on whether shared topology is off or on, respectively.  For Ansys ICEM CFD files (*.tin), set the object granularity to one object per selection.
                    """
                    return PyMenu(self.service, "/file/import/cad_options/one_object_per").execute(*args, **kwargs)
                def one_face_zone_per(self, *args, **kwargs):
                    """
                    Enables you to create one face zone per body/face/object to be imported.
                    """
                    return PyMenu(self.service, "/file/import/cad_options/one_face_zone_per").execute(*args, **kwargs)
                def named_selection_tessellation_failure(self, *args, **kwargs):
                    """
                    Set named selection for CFD surface mesh failures.
                    """
                    return PyMenu(self.service, "/file/import/cad_options/named_selection_tessellation_failure").execute(*args, **kwargs)
                def use_body_names(self, *args, **kwargs):
                    """
                    Use body names for CAD files.
                    """
                    return PyMenu(self.service, "/file/import/cad_options/use_body_names").execute(*args, **kwargs)
                def use_part_names(self, *args, **kwargs):
                    """
                    Enables you to choose whether to add the part names from the CAD file to the object and zone names on import. The default setting is auto which adds the part names to both object and zone names when object creation granularity is set to body. When the object creation granularity is set to part or file, the part names are not added to the zone names, face zone labels, or the region names, by default. You can also explicitly select yes or no.
                    """
                    return PyMenu(self.service, "/file/import/cad_options/use_part_names").execute(*args, **kwargs)
                def replacement_character(self, *args, **kwargs):
                    """
                    Name replacement character.
                    """
                    return PyMenu(self.service, "/file/import/cad_options/replacement_character").execute(*args, **kwargs)
                def derive_zone_name_from_object_scope(self, *args, **kwargs):
                    """
                    Enables zones without Named Selections to inherit the object name on import. This option is disabled by default.
                    """
                    return PyMenu(self.service, "/file/import/cad_options/derive_zone_name_from_object_scope").execute(*args, **kwargs)
                def merge_nodes(self, *args, **kwargs):
                    """
                    Enables the merging of geometry object nodes during CAD import. This option is enabled by default.  This option can be optionally enabled/disabled only when geometry objects are imported using the CAD Faceting option for CAD import. Mesh object nodes will always be merged when the CFD Surface Mesh is selected for CAD import.
                    """
                    return PyMenu(self.service, "/file/import/cad_options/merge_nodes").execute(*args, **kwargs)
                def create_cad_assemblies(self, *args, **kwargs):
                    """
                    Enables creating the CAD Assemblies tree on CAD import. The CAD Assemblies tree represents the CAD tree as it is presented in the CAD package in which it was created. All sub-assembly levels from the CAD are maintained on import in Fluent Meshing.  For commands specific to the CAD assemblies, refer to cad-assemblies/
                                
                    """
                    return PyMenu(self.service, "/file/import/cad_options/create_cad_assemblies").execute(*args, **kwargs)
                def modify_all_duplicate_names(self, *args, **kwargs):
                    """
                    Enables you to modify all duplicate object/zone names by adding incremental integers as suffix. This option is disabled by default.
                    """
                    return PyMenu(self.service, "/file/import/cad_options/modify_all_duplicate_names").execute(*args, **kwargs)
                def use_part_or_body_names_as_suffix_to_named_selections(self, *args, **kwargs):
                    """
                    Part or Body names are used as suffix for named selections spanning over multiple parts or bodies.
                    """
                    return PyMenu(self.service, "/file/import/cad_options/use_part_or_body_names_as_suffix_to_named_selections").execute(*args, **kwargs)
                def strip_file_name_extension_from_naming(self, *args, **kwargs):
                    """
                    Removes the extension of the CAD files from the object/face zone names on import. This option is disabled by default.
                    """
                    return PyMenu(self.service, "/file/import/cad_options/strip_file_name_extension_from_naming").execute(*args, **kwargs)
                def import_label_for_body_named_selection(self, *args, **kwargs):
                    """
                    Import face zone labels for body named selections.
                    """
                    return PyMenu(self.service, "/file/import/cad_options/import_label_for_body_named_selection").execute(*args, **kwargs)
                def strip_path_prefix_from_names(self, *args, **kwargs):
                    """
                    Enables you to remove the path prefix from the object/face zone names on import. The default setting is auto which removes the path prefix from object/face zone names when the object creation granularity is set to one object per file. You can also explicitly select yes or no.
                    """
                    return PyMenu(self.service, "/file/import/cad_options/strip_path_prefix_from_names").execute(*args, **kwargs)
                def merge_objects_per_body_named_selection(self, *args, **kwargs):
                    """
                    Merge Objects per body named selection.
                    """
                    return PyMenu(self.service, "/file/import/cad_options/merge_objects_per_body_named_selection").execute(*args, **kwargs)
                def extract_features(self, *args, **kwargs):
                    """
                    Enables feature extraction from the CAD model on import. You can choose to disable this, if desired. Specify an appropriate value for feature angle. The default value is 40.
                    """
                    return PyMenu(self.service, "/file/import/cad_options/extract_features").execute(*args, **kwargs)
                def import_curvature_data_from_CAD(self, *args, **kwargs):
                    """
                    Enables importing of the curvature data from the nodes of the CAD facets. You can choose to disable this, if desired.
                    """
                    return PyMenu(self.service, "/file/import/cad_options/import_curvature_data_from_CAD").execute(*args, **kwargs)
                def create_label_per_body_during_cad_faceting(self, *args, **kwargs):
                    """
                    Create label Per Body during cad faceting.
                    """
                    return PyMenu(self.service, "/file/import/cad_options/create_label_per_body_during_cad_faceting").execute(*args, **kwargs)

        class checkpoint(metaclass=PyMenuMeta):
            """
            Checkpoint stores the mesh in the memory instead of writing it to a file.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def write_checkpoint(self, *args, **kwargs):
                """
                Write checkpoint.
                """
                return PyMenu(self.service, "/file/checkpoint/write_checkpoint").execute(*args, **kwargs)
            def restore_checkpoint(self, *args, **kwargs):
                """
                Restore to checkpoint.
                """
                return PyMenu(self.service, "/file/checkpoint/restore_checkpoint").execute(*args, **kwargs)
            def list_checkpoint_names(self, *args, **kwargs):
                """
                Get all checkpoint names.
                """
                return PyMenu(self.service, "/file/checkpoint/list_checkpoint_names").execute(*args, **kwargs)
            def delete_checkpoint(self, *args, **kwargs):
                """
                Delete checkpoint.
                """
                return PyMenu(self.service, "/file/checkpoint/delete_checkpoint").execute(*args, **kwargs)

        class project(metaclass=PyMenuMeta):
            """
            Enter to create new project, open project, save and archive project.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def new(self, *args, **kwargs):
                """
                Create New Project.
                """
                return PyMenu(self.service, "/file/project[beta]/new").execute(*args, **kwargs)
            def open(self, *args, **kwargs):
                """
                Open project.
                """
                return PyMenu(self.service, "/file/project[beta]/open").execute(*args, **kwargs)
            def save(self, *args, **kwargs):
                """
                Save Project.
                """
                return PyMenu(self.service, "/file/project[beta]/save").execute(*args, **kwargs)
            def save_as(self, *args, **kwargs):
                """
                Save As Project.
                """
                return PyMenu(self.service, "/file/project[beta]/save_as").execute(*args, **kwargs)
            def save_as_copy(self, *args, **kwargs):
                """
                Save As Copy.
                """
                return PyMenu(self.service, "/file/project[beta]/save_as_copy").execute(*args, **kwargs)
            def archive(self, *args, **kwargs):
                """
                Archive Project.
                """
                return PyMenu(self.service, "/file/project[beta]/archive").execute(*args, **kwargs)

    class boundary(metaclass=PyMenuMeta):
        """
        Enter the boundary menu.
        """
        def __init__(self, path, service):
            self.path = path
            self.service = service
            self.feature = self.__class__.feature(path + [("feature", None)], service)
            self.modify = self.__class__.modify(path + [("modify", None)], service)
            self.refine = self.__class__.refine(path + [("refine", None)], service)
            self.remesh = self.__class__.remesh(path + [("remesh", None)], service)
            self.improve = self.__class__.improve(path + [("improve", None)], service)
            self.separate = self.__class__.separate(path + [("separate", None)], service)
            self.manage = self.__class__.manage(path + [("manage", None)], service)
            self.shell_boundary_layer = self.__class__.shell_boundary_layer(path + [("shell_boundary_layer", None)], service)
            self.boundary_conditions = self.__class__.boundary_conditions(path + [("boundary_conditions", None)], service)
        def auto_slit_faces(self, *args, **kwargs):
            """
            Slits all boundary faces with cells on both sides (these cells must be in the same cell zone). A displacement can be specified to provide thickness to the boundary. 
            """
            return PyMenu(self.service, "/boundary/auto_slit_faces").execute(*args, **kwargs)
        def orient_faces_by_point(self, *args, **kwargs):
            """
            Orients the normals based on the specified material point. 
            """
            return PyMenu(self.service, "/boundary/orient_faces_by_point").execute(*args, **kwargs)
        def check_boundary_mesh(self, *args, **kwargs):
            """
            Reports the number of Delaunay violations on the triangular surface mesh and the number of isolated nodes. 
            """
            return PyMenu(self.service, "/boundary/check_boundary_mesh").execute(*args, **kwargs)
        def check_duplicate_geom(self, *args, **kwargs):
            """
            Displays the names of the duplicate surfaces and prints maximum and average distance between them. 
            """
            return PyMenu(self.service, "/boundary/check_duplicate_geom").execute(*args, **kwargs)
        def clear_marked_faces(self, *args, **kwargs):
            """
            Clears marked faces. 
            """
            return PyMenu(self.service, "/boundary/clear_marked_faces").execute(*args, **kwargs)
        def clear_marked_nodes(self, *args, **kwargs):
            """
            Clears nodes that were marked using the mark-duplicate-nodes command. 
            """
            return PyMenu(self.service, "/boundary/clear_marked_nodes").execute(*args, **kwargs)
        def coarsen_boundary_faces(self, *args, **kwargs):
            """
            Coarsen boundary face zones.
            """
            return PyMenu(self.service, "/boundary/coarsen_boundary_faces").execute(*args, **kwargs)
        def count_marked_faces(self, *args, **kwargs):
            """
            Reports the number of marked faces. 
            """
            return PyMenu(self.service, "/boundary/count_marked_faces").execute(*args, **kwargs)
        def count_free_nodes(self, *args, **kwargs):
            """
            Reports the number of boundary nodes associated with edges having only one attached face. 
            """
            return PyMenu(self.service, "/boundary/count_free_nodes").execute(*args, **kwargs)
        def count_unused_nodes(self, *args, **kwargs):
            """
            Lists the number of boundary nodes that are not used by any cell. 
            """
            return PyMenu(self.service, "/boundary/count_unused_nodes").execute(*args, **kwargs)
        def count_unused_bound_node(self, *args, **kwargs):
            """
            Counts the unused boundary nodes in the domain. 
            """
            return PyMenu(self.service, "/boundary/count_unused_bound_node").execute(*args, **kwargs)
        def count_unused_faces(self, *args, **kwargs):
            """
            Lists the number of boundary faces that are not used by any cell. 
            """
            return PyMenu(self.service, "/boundary/count_unused_faces").execute(*args, **kwargs)
        def compute_bounding_box(self, *args, **kwargs):
            """
            Computes the bounding box for the zones specified. 
            """
            return PyMenu(self.service, "/boundary/compute_bounding_box").execute(*args, **kwargs)
        def create_bounding_box(self, *args, **kwargs):
            """
            Creates the bounding box for the specified zones. You can specify the zone type, name, edge length, and the extents of the box, as required. You can also optionally create a geometry object from the bounding box created.
            """
            return PyMenu(self.service, "/boundary/create_bounding_box").execute(*args, **kwargs)
        def create_cylinder(self, *args, **kwargs):
            """
            Creates a cylinder by specifying the axis, radius, and edge length or three arc nodes, the axial delta, the radial gap, and the edge length. You can also specify the prefix for the zone being created, as required. You can also optionally create a geometry object from the cylinder created.
            """
            return PyMenu(self.service, "/boundary/create_cylinder").execute(*args, **kwargs)
        def create_plane_surface(self, *args, **kwargs):
            """
            Creates a plane surface by specifying either the axis direction, axial location, and the extents of the surface or three points defining the plane. You can also optionally create a geometry object from the plane surface created.
            """
            return PyMenu(self.service, "/boundary/create_plane_surface").execute(*args, **kwargs)
        def create_swept_surface(self, *args, **kwargs):
            """
            Creates a surface by sweeping the specified edge in the direction specified. You need to specify the distance to sweep through and the number of offsets, as required. You can also optionally create a geometry object from the swept surface created.
            """
            return PyMenu(self.service, "/boundary/create_swept_surface").execute(*args, **kwargs)
        def create_revolved_surface(self, *args, **kwargs):
            """
            Creates a revolved surface by rotating the specified edge through the angle specified. Specify the number of segments, scale factor, and the pivot point and axis of rotation. You can also optionally create a geometry object from the revolved surface created.
            """
            return PyMenu(self.service, "/boundary/create_revolved_surface").execute(*args, **kwargs)
        def delete_duplicate_faces(self, *args, **kwargs):
            """
            Searches for faces on a specified zone that have the same nodes and deletes the duplicates.   Duplicate faces may be present if you generated the boundary mesh using a third-party grid generator, or if you have used the slit-boundary-face command to modify the boundary mesh and then merged the nodes. 
            """
            return PyMenu(self.service, "/boundary/delete_duplicate_faces").execute(*args, **kwargs)
        def delete_all_dup_faces(self, *args, **kwargs):
            """
            Searches for faces on all boundary zones that have the same nodes and deletes the duplicates. 
            """
            return PyMenu(self.service, "/boundary/delete_all_dup_faces").execute(*args, **kwargs)
        def delete_island_faces(self, *args, **kwargs):
            """
            Enables you to delete faces in a non-contiguous region of a face zone. 
            """
            return PyMenu(self.service, "/boundary/delete_island_faces").execute(*args, **kwargs)
        def delete_unused_nodes(self, *args, **kwargs):
            """
            Deletes the boundary nodes that are not used by any boundary faces. 
            """
            return PyMenu(self.service, "/boundary/delete_unused_nodes").execute(*args, **kwargs)
        def delete_unused_faces(self, *args, **kwargs):
            """
            Deletes all the boundary faces that are not used by any cell. 
            """
            return PyMenu(self.service, "/boundary/delete_unused_faces").execute(*args, **kwargs)
        def delete_unconnected_faces(self, *args, **kwargs):
            """
            Enables you to delete the unconnected face-zones. 
            """
            return PyMenu(self.service, "/boundary/delete_unconnected_faces").execute(*args, **kwargs)
        def edge_limits(self, *args, **kwargs):
            """
            Prints the length of the shortest and longest edges on the boundary. This information is useful for setting initial mesh parameters and refinement controls. 
            """
            return PyMenu(self.service, "/boundary/edge_limits").execute(*args, **kwargs)
        def expand_marked_faces_by_rings(self, *args, **kwargs):
            """
            Mark rings of faces around marked faces.
            """
            return PyMenu(self.service, "/boundary/expand_marked_faces_by_rings").execute(*args, **kwargs)
        def face_distribution(self, *args, **kwargs):
            """
            Reports the distribution of face quality in the text window. 
            """
            return PyMenu(self.service, "/boundary/face_distribution").execute(*args, **kwargs)
        def face_skewness(self, *args, **kwargs):
            """
            Lists the worst face skewness. 
            """
            return PyMenu(self.service, "/boundary/face_skewness").execute(*args, **kwargs)
        def jiggle_boundary_nodes(self, *args, **kwargs):
            """
            Randomly perturbs all boundary nodes based on an input tolerance. Some nodes will be perturbed less than the tolerance value, while others will be perturbed by half of the tolerance value in all three coordinate directions. 
            """
            return PyMenu(self.service, "/boundary/jiggle_boundary_nodes").execute(*args, **kwargs)
        def improve_surface_mesh(self, *args, **kwargs):
            """
            Improve surface mesh by swapping face edges
            where Delaunay violations occur.
            """
            return PyMenu(self.service, "/boundary/improve_surface_mesh").execute(*args, **kwargs)
        def make_periodic(self, *args, **kwargs):
            """
            Enables you to make the specified boundaries periodic. You can specify the type of periodicity (rotational or translational), the angle, pivot, and axis of rotation, for rotational periodicity or the translational shift for translational periodicity.   For each of the zones specified, a corresponding periodic shadow boundary zone will be created. 
            """
            return PyMenu(self.service, "/boundary/make_periodic").execute(*args, **kwargs)
        def recover_periodic_surfaces(self, *args, **kwargs):
            """
            Restores the periodic relationship between face zones. You will be prompted for the type (rotational or translational), method (semi-automatic, automatic, or manual, depending on the periodicity type) and for face zones. Periodicity information (angle, pivot point, axis of rotation, or translational shift) are read in with the mesh file. 
            """
            return PyMenu(self.service, "/boundary/recover_periodic_surfaces").execute(*args, **kwargs)
        def set_periodicity(self, *args, **kwargs):
            """
            Defines the periodicity parameters. You will be prompted for the type of periodicity (rotational or translational). For rotational periodicity, you will be prompted for the angle and axis of rotation parameters. For translational periodicity, you will be prompted for the shift vector components.
            """
            return PyMenu(self.service, "/boundary/set_periodicity").execute(*args, **kwargs)
        def mark_bad_quality_faces(self, *args, **kwargs):
            """
            Mark Bad Quality Faces.
            """
            return PyMenu(self.service, "/boundary/mark_bad_quality_faces").execute(*args, **kwargs)
        def mark_faces_in_region(self, *args, **kwargs):
            """
            Marks the faces that are contained in a specified local refinement region. 
            """
            return PyMenu(self.service, "/boundary/mark_faces_in_region").execute(*args, **kwargs)
        def mark_face_intersection(self, *args, **kwargs):
            """
            Marks intersecting faces. Intersection is detected if the line defined by any two consecutive nodes on a face intersects any face in the current domain. The marked faces will appear in the grid display when faces are displayed. For a list of intersecting faces, set the /report/verbosity level to 2 before using the mark-face-intersection command. 
            """
            return PyMenu(self.service, "/boundary/mark_face_intersection").execute(*args, **kwargs)
        def resolve_face_intersection(self, *args, **kwargs):
            """
            Resolves self intersection on manifold surface meshes.
            """
            return PyMenu(self.service, "/boundary/resolve_face_intersection").execute(*args, **kwargs)
        def mark_face_proximity(self, *args, **kwargs):
            """
            Marks faces that are in proximity to each other.   Face A is considered to be in proximity to face B if any of the nodes on face A are within the calculated proximity distance from face B. The proximity distance is calculated based on the specified relative distance and the sphere radius. The sphere radius is determined by the maximum distance from the centroid of the face to its nodes. The marked faces will appear in the grid display when faces are displayed.   For a list of faces in proximity to each other, set the /report/verbosity level to 2 before using the mark-face-proximity command. 
            """
            return PyMenu(self.service, "/boundary/mark_face_proximity").execute(*args, **kwargs)
        def mark_duplicate_nodes(self, *args, **kwargs):
            """
            Marks duplicate nodes. The marked nodes will appear in the grid display when nodes are displayed. For a list of duplicate nodes, set the /report/verbosity level to 2 before using the mark-duplicate-nodes command. 
            """
            return PyMenu(self.service, "/boundary/mark_duplicate_nodes").execute(*args, **kwargs)
        def merge_nodes(self, *args, **kwargs):
            """
            Merges duplicate nodes. 
            """
            return PyMenu(self.service, "/boundary/merge_nodes").execute(*args, **kwargs)
        def merge_small_face_zones(self, *args, **kwargs):
            """
            Merges the face zones having area less than the minimum area. 
            """
            return PyMenu(self.service, "/boundary/merge_small_face_zones").execute(*args, **kwargs)
        def print_info(self, *args, **kwargs):
            """
            Prints information about the grid in the text window. 
            """
            return PyMenu(self.service, "/boundary/print_info").execute(*args, **kwargs)
        def project_face_zone(self, *args, **kwargs):
            """
            Projects nodes on a selected face zone onto a target face zone. Projection can be performed based on normal direction, closest point, or specified direction. 
            """
            return PyMenu(self.service, "/boundary/project_face_zone").execute(*args, **kwargs)
        def reset_element_type(self, *args, **kwargs):
            """
            Resets the element type (mixed, tri, or quad) of a boundary zone. If you have separated a mixed (tri and quad) face zone into one tri face zone and one quad face zone, for example, each of these will be identified as a “mixed" zone. Resetting the element type for each of these new zones will identify them as, respectively, a triangular zone and a quadrilateral zone. 
            """
            return PyMenu(self.service, "/boundary/reset_element_type").execute(*args, **kwargs)
        def scale_nodes(self, *args, **kwargs):
            """
            Applies a scaling factor to all node coordinates. You can use this command to change the units of the grid. 
            """
            return PyMenu(self.service, "/boundary/scale_nodes").execute(*args, **kwargs)
        def slit_boundary_face(self, *args, **kwargs):
            """
            Slits a boundary face zone by duplicating all faces and nodes, except those nodes that are located at the edges of the boundary zone. A displacement can be specified to provide thickness to the boundary. The slit command only works when it is possible to move from face to face using the connectivity provided by the cells.   You should slit the boundary face after you generate the volume mesh so that cells will not be placed inside the gap. There may be some inaccuracies when you graphically display solution data for a mesh with a slit boundary in ANSYS Fluent. 
            """
            return PyMenu(self.service, "/boundary/slit_boundary_face").execute(*args, **kwargs)
        def unmark_selected_faces(self, *args, **kwargs):
            """
            Unmarks the marked selected faces. 
            """
            return PyMenu(self.service, "/boundary/unmark_selected_faces").execute(*args, **kwargs)
        def smooth_marked_faces(self, *args, **kwargs):
            """
            Smooths the marked faces. 
            """
            return PyMenu(self.service, "/boundary/smooth_marked_faces").execute(*args, **kwargs)
        def wrapper(self, *args, **kwargs):
            """
            Enters the surface wrapper menu.  This menu is no longer supported, and will be removed in a future release.
            """
            return PyMenu(self.service, "/boundary/wrapper").execute(*args, **kwargs)
        def unmark_faces_in_zones(self, *args, **kwargs):
            """
            Unmark faces in zones.
            """
            return PyMenu(self.service, "/boundary/unmark_faces_in_zones").execute(*args, **kwargs)
        def delete_free_edge_faces(self, *args, **kwargs):
            """
            Enables you to remove faces with the specified number of free edges from the specified boundary zones. 
            """
            return PyMenu(self.service, "/boundary/delete_free_edge_faces").execute(*args, **kwargs)
        def fix_mconnected_edges(self, *args, **kwargs):
            """
            Resolves multi-connected edges/non-manifold configurations in the boundary mesh by deleting fringes and overlaps based on threshold values specified.
            """
            return PyMenu(self.service, "/boundary/fix_mconnected_edges").execute(*args, **kwargs)

        class feature(metaclass=PyMenuMeta):
            """
            Enables you to create and modify features. 
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def copy_edge_zones(self, *args, **kwargs):
                """
                Copies the specified edge zone(s) to new edge zone(s). 
                """
                return PyMenu(self.service, "/boundary/feature/copy_edge_zones").execute(*args, **kwargs)
            def create_edge_zones(self, *args, **kwargs):
                """
                Extracts edge loops for the specified face zone(s) based on the feature method specified. You also need to specify an appropriate value for feature angle when using the fixed-angle method.   The Face Seed approach cannot be used when creating edge loops using text commands.
                """
                return PyMenu(self.service, "/boundary/feature/create_edge_zones").execute(*args, **kwargs)
            def delete_edge_zones(self, *args, **kwargs):
                """
                Deletes the specified edge zone(s) 
                """
                return PyMenu(self.service, "/boundary/feature/delete_edge_zones").execute(*args, **kwargs)
            def delete_degenerated_edges(self, *args, **kwargs):
                """
                Deletes degenerated edges (edges where the two end nodes are the same) for the edge zone(s) specified.
                """
                return PyMenu(self.service, "/boundary/feature/delete_degenerated_edges").execute(*args, **kwargs)
            def edge_size_limits(self, *args, **kwargs):
                """
                Reports the minimum, maximum, and average edge length for the specified edge zone(s) in the console. 
                """
                return PyMenu(self.service, "/boundary/feature/edge_size_limits").execute(*args, **kwargs)
            def intersect_edge_zones(self, *args, **kwargs):
                """
                Intersects the specified edge loops to create a new edge loop comprising the common edges. You can enable automatic deleting of overlapped edges and specify an appropriate intersection tolerance. 
                """
                return PyMenu(self.service, "/boundary/feature/intersect_edge_zones").execute(*args, **kwargs)
            def group(self, *args, **kwargs):
                """
                Associates the specified edge zone(s) with the specified face zone. 
                """
                return PyMenu(self.service, "/boundary/feature/group").execute(*args, **kwargs)
            def list_edge_zones(self, *args, **kwargs):
                """
                Lists the name, ID, type, and count for the specified edge zone(s). 
                """
                return PyMenu(self.service, "/boundary/feature/list_edge_zones").execute(*args, **kwargs)
            def merge_edge_zones(self, *args, **kwargs):
                """
                Merges multiple edge loops of the same type into a single loop. 
                """
                return PyMenu(self.service, "/boundary/feature/merge_edge_zones").execute(*args, **kwargs)
            def orient_edge_direction(self, *args, **kwargs):
                """
                Orients the edges on the loop to point in the same direction. 
                """
                return PyMenu(self.service, "/boundary/feature/orient_edge_direction").execute(*args, **kwargs)
            def project_edge_zones(self, *args, **kwargs):
                """
                Projects the edges of the specified loop onto the specified face zone using the specified projection method. 
                """
                return PyMenu(self.service, "/boundary/feature/project_edge_zones").execute(*args, **kwargs)
            def remesh_edge_zones(self, *args, **kwargs):
                """
                Remeshes the specified edge loop(s), modifying the node distribution according to the specified remeshing method, spacing values, and feature angle. You can also enable quadratic reconstruction, if required. 
                """
                return PyMenu(self.service, "/boundary/feature/remesh_edge_zones").execute(*args, **kwargs)
            def reverse_edge_direction(self, *args, **kwargs):
                """
                Reverses the direction of the edge loop. 
                """
                return PyMenu(self.service, "/boundary/feature/reverse_edge_direction").execute(*args, **kwargs)
            def separate_edge_zones(self, *args, **kwargs):
                """
                Separates the specified edge loop based on connectivity and the specified feature angle. 
                """
                return PyMenu(self.service, "/boundary/feature/separate_edge_zones").execute(*args, **kwargs)
            def separate_edge_zones_by_seed(self, *args, **kwargs):
                """
                Separates the edge loop based on the seed edge specified. The edge zone separation angle is used to separate the edge zone (default 40).
                """
                return PyMenu(self.service, "/boundary/feature/separate_edge_zones_by_seed").execute(*args, **kwargs)
            def toggle_edge_type(self, *args, **kwargs):
                """
                Toggles the edge type between boundary and interior. 
                """
                return PyMenu(self.service, "/boundary/feature/toggle_edge_type").execute(*args, **kwargs)
            def ungroup(self, *args, **kwargs):
                """
                Ungroups previously grouped edge zones. 
                """
                return PyMenu(self.service, "/boundary/feature/ungroup").execute(*args, **kwargs)
            def separate_delete_small_edges(self, *args, **kwargs):
                """
                Separates the edge zones based on the feature angle specified, and then deletes the edges having a count smaller than the minimum count specified.
                """
                return PyMenu(self.service, "/boundary/feature/separate_delete_small_edges").execute(*args, **kwargs)

        class modify(metaclass=PyMenuMeta):
            """
            Contains commands used to modify the boundary mesh. 
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
                self.patch_options = self.__class__.patch_options(path + [("patch_options", None)], service)
            def analyze_bnd_connectvty(self, *args, **kwargs):
                """
                Finds and marks free edges and nodes and multiply-connected edges and nodes. This process is necessary if the boundary mesh has been changed with Scheme functions. 
                """
                return PyMenu(self.service, "/boundary/modify/analyze_bnd_connectvty").execute(*args, **kwargs)
            def clear_selections(self, *args, **kwargs):
                """
                Clears all selections. 
                """
                return PyMenu(self.service, "/boundary/modify/clear_selections").execute(*args, **kwargs)
            def create(self, *args, **kwargs):
                """
                Creates a boundary face if the selection list contains 3 nodes and an optional zone. If the selection list contains positions, then nodes are created. 
                """
                return PyMenu(self.service, "/boundary/modify/create").execute(*args, **kwargs)
            def auto_patch_holes(self, *args, **kwargs):
                """
                Patch zone(s) by filling holes.
                """
                return PyMenu(self.service, "/boundary/modify/auto_patch_holes").execute(*args, **kwargs)
            def create_mid_node(self, *args, **kwargs):
                """
                Creates a node at the midpoint between two selected nodes. 
                """
                return PyMenu(self.service, "/boundary/modify/create_mid_node").execute(*args, **kwargs)
            def collapse(self, *args, **kwargs):
                """
                Collapses pairs of nodes, edge(s), or face(s). If a pair of nodes is selected, both the nodes are deleted and a new node is created at the midpoint of the two nodes. If a triangular face is selected, the complete face is collapsed into a single node at the centroid of the face. 
                """
                return PyMenu(self.service, "/boundary/modify/collapse").execute(*args, **kwargs)
            def delete(self, *args, **kwargs):
                """
                Deletes all selected faces and nodes. 
                """
                return PyMenu(self.service, "/boundary/modify/delete").execute(*args, **kwargs)
            def deselect_last(self, *args, **kwargs):
                """
                Removes the last selection from the selection list. 
                """
                return PyMenu(self.service, "/boundary/modify/deselect_last").execute(*args, **kwargs)
            def clear_skew_faces(self, *args, **kwargs):
                """
                Clears faces that were marked using the mark-skew-face command. 
                """
                return PyMenu(self.service, "/boundary/modify/clear_skew_faces").execute(*args, **kwargs)
            def list_selections(self, *args, **kwargs):
                """
                Lists all of the selected objects. 
                """
                return PyMenu(self.service, "/boundary/modify/list_selections").execute(*args, **kwargs)
            def mark_skew_face(self, *args, **kwargs):
                """
                Marks faces that should be skipped when the worst skewed face is reported using the Modify Boundary dialog box. This enables you to search for the next skewed face. 
                """
                return PyMenu(self.service, "/boundary/modify/mark_skew_face").execute(*args, **kwargs)
            def merge(self, *args, **kwargs):
                """
                Merges pairs of nodes. The first node selected is retained, and the second is the duplicate that is merged. 
                """
                return PyMenu(self.service, "/boundary/modify/merge").execute(*args, **kwargs)
            def move(self, *args, **kwargs):
                """
                Moves the selected node to the selected position if the selection list contains a node and a position. 
                """
                return PyMenu(self.service, "/boundary/modify/move").execute(*args, **kwargs)
            def delta_move(self, *args, **kwargs):
                """
                Moves the selected node by specified magnitude. 
                """
                return PyMenu(self.service, "/boundary/modify/delta_move").execute(*args, **kwargs)
            def rezone(self, *args, **kwargs):
                """
                Moves the selected faces from their current zone into the selected zone, if the selection list contains a zone and one or more faces. 
                """
                return PyMenu(self.service, "/boundary/modify/rezone").execute(*args, **kwargs)
            def select_entity(self, *args, **kwargs):
                """
                Adds a cell, face, or node to the selection list by entering the name of the entity. 
                """
                return PyMenu(self.service, "/boundary/modify/select_entity").execute(*args, **kwargs)
            def select_filter(self, *args, **kwargs):
                """
                Selects a filter. The possible filters are off, cell, face, edge, node, zone, position, object, and size. If off is chosen, then when a selection is made, it is first checked to see if it is a cell, then a face, an edge, and so on. When the node filter is used, and if a cell or face is selected, the node closest to the selection point is picked. Thus, the nodes do not have to be displayed, to be picked. 
                """
                return PyMenu(self.service, "/boundary/modify/select_filter").execute(*args, **kwargs)
            def select_probe(self, *args, **kwargs):
                """
                Selects the probe function. The possible functions are: 
                """
                return PyMenu(self.service, "/boundary/modify/select_probe").execute(*args, **kwargs)
            def select_position(self, *args, **kwargs):
                """
                Adds a position to the selection list by entering the coordinates of the position. 
                """
                return PyMenu(self.service, "/boundary/modify/select_position").execute(*args, **kwargs)
            def select_zone(self, *args, **kwargs):
                """
                Adds a zone to the selection list by entering the zone name or ID. 
                """
                return PyMenu(self.service, "/boundary/modify/select_zone").execute(*args, **kwargs)
            def show_filter(self, *args, **kwargs):
                """
                Shows the current filter. 
                """
                return PyMenu(self.service, "/boundary/modify/show_filter").execute(*args, **kwargs)
            def show_probe(self, *args, **kwargs):
                """
                Shows the current probe function. 
                """
                return PyMenu(self.service, "/boundary/modify/show_probe").execute(*args, **kwargs)
            def skew(self, *args, **kwargs):
                """
                Finds the face with the highest (worst) skewness, selects it in the graphics window, and reports its skewness and zone ID in the console window. 
                """
                return PyMenu(self.service, "/boundary/modify/skew").execute(*args, **kwargs)
            def smooth(self, *args, **kwargs):
                """
                Uses Laplace smoothing to modify the position of the nodes in the selection list. It moves the selected node to a position computed from an average of its node neighbors. The new position is an average of the neighboring node coordinates and is not reprojected to the discrete surface. 
                """
                return PyMenu(self.service, "/boundary/modify/smooth").execute(*args, **kwargs)
            def split_face(self, *args, **kwargs):
                """
                Splits two selected faces into four faces. 
                """
                return PyMenu(self.service, "/boundary/modify/split_face").execute(*args, **kwargs)
            def swap(self, *args, **kwargs):
                """
                Swaps boundary edges (of triangular faces) if the selection list contains edges. 
                """
                return PyMenu(self.service, "/boundary/modify/swap").execute(*args, **kwargs)
            def hole_feature_angle(self, *args, **kwargs):
                """
                Specifies the feature angle for consideration of holes in the geometry. 
                """
                return PyMenu(self.service, "/boundary/modify/hole_feature_angle").execute(*args, **kwargs)
            def undo(self, *args, **kwargs):
                """
                Undoes the previous operation. When an operation is performed, the reverse operation is stored on the undo stack. For example, a create operation places a delete on the stack, and a delete adds a create operation.   The undo operation requires that the name of the object exist when the action is undone. If the name does not exist, then the undo will fail. You can undo the last few operations, but if many operations are being performed it is recommended that you also save the mesh periodically. 
                """
                return PyMenu(self.service, "/boundary/modify/undo").execute(*args, **kwargs)
            def next_skew(self, *args, **kwargs):
                """
                Finds the triangular face of nearest lower skewness value than that of the worst skewed face. The face ID, its skewness, the longest edge ID, and the node ID opposite to the longest edge are displayed in the console. 
                """
                return PyMenu(self.service, "/boundary/modify/next_skew").execute(*args, **kwargs)
            def skew_report_zone(self, *args, **kwargs):
                """
                Enables you to select the zone for which you want to report the skewness. You can either specify zone name or zone ID. 
                """
                return PyMenu(self.service, "/boundary/modify/skew_report_zone").execute(*args, **kwargs)
            def local_remesh(self, *args, **kwargs):
                """
                Remeshes marked faces or faces based on selections in the graphics window. Select the faces to be remeshed and specify the sizing source (constant-size, geometry, or size-field), the number of radial layers of faces to be remeshed (rings), the feature angle to be preserved while remeshing the selected faces, and the size for constant size remeshing (if applicable).
                """
                return PyMenu(self.service, "/boundary/modify/local_remesh").execute(*args, **kwargs)
            def select_visible_entities(self, *args, **kwargs):
                """
                Enables you to select only visible entities (nodes, edges, faces, zones, objects) when the box select or polygon select options are used. Ensure that the model is zoomed to an appropriate level for correct selection.
                """
                return PyMenu(self.service, "/boundary/modify/select_visible_entities").execute(*args, **kwargs)

            class patch_options(metaclass=PyMenuMeta):
                """
                Settings for Patching zone(s) by filling holes.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def remesh(self, *args, **kwargs):
                    """
                    Remeshes newly added patches.
                    """
                    return PyMenu(self.service, "/boundary/modify/patch_options/remesh").execute(*args, **kwargs)
                def separate(self, *args, **kwargs):
                    """
                    Separates newly added patches.
                    """
                    return PyMenu(self.service, "/boundary/modify/patch_options/separate").execute(*args, **kwargs)

        class refine(metaclass=PyMenuMeta):
            """
            Discusses the commands used to refine the boundary mesh. 
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
                self.local_regions = self.__class__.local_regions(path + [("local_regions", None)], service)
            def auto_refine(self, *args, **kwargs):
                """
                Automatically refines a face zone based on proximity. The original face zone is treated as a background mesh. Faces are refined by multiple face splitting passes, so that no face is in close proximity to any face in the current domain. 
                """
                return PyMenu(self.service, "/boundary/refine/auto_refine").execute(*args, **kwargs)
            def clear(self, *args, **kwargs):
                """
                Clears all refinement marks from all boundary faces. 
                """
                return PyMenu(self.service, "/boundary/refine/clear").execute(*args, **kwargs)
            def count(self, *args, **kwargs):
                """
                Counts the number of faces marked on each boundary zone. 
                """
                return PyMenu(self.service, "/boundary/refine/count").execute(*args, **kwargs)
            def mark(self, *args, **kwargs):
                """
                Marks the faces for refinement. 
                """
                return PyMenu(self.service, "/boundary/refine/mark").execute(*args, **kwargs)
            def limits(self, *args, **kwargs):
                """
                Prints a report of the minimum and maximum size of each specified zone. This report will also tell you how many faces on each zone have been marked for refinement. 
                """
                return PyMenu(self.service, "/boundary/refine/limits").execute(*args, **kwargs)
            def refine(self, *args, **kwargs):
                """
                Refines the marked faces. 
                """
                return PyMenu(self.service, "/boundary/refine/refine").execute(*args, **kwargs)

            class local_regions(metaclass=PyMenuMeta):
                """
                Enters the local refinement menu. 
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def define(self, *args, **kwargs):
                    """
                    Defines the refinement region according to the specified parameters. 
                    """
                    return PyMenu(self.service, "/boundary/refine/local_regions/define").execute(*args, **kwargs)
                def delete(self, *args, **kwargs):
                    """
                    Deletes the specified region. 
                    """
                    return PyMenu(self.service, "/boundary/refine/local_regions/delete").execute(*args, **kwargs)
                def init(self, *args, **kwargs):
                    """
                    Creates a region encompassing the entire geometry. 
                    """
                    return PyMenu(self.service, "/boundary/refine/local_regions/init").execute(*args, **kwargs)
                def list_all_regions(self, *args, **kwargs):
                    """
                    Lists all the refinement regions in the console. 
                    """
                    return PyMenu(self.service, "/boundary/refine/local_regions/list_all_regions").execute(*args, **kwargs)

        class remesh(metaclass=PyMenuMeta):
            """
            Has a set of commands for remeshing the face zones. 
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
                self.controls = self.__class__.controls(path + [("controls", None)], service)
                self.size_functions = self.__class__.size_functions(path + [("size_functions", None)], service)
            def create_edge_loops(self, *args, **kwargs):
                """
                Creates edge loops for a specified face zone, based on feature angle. 
                """
                return PyMenu(self.service, "/boundary/remesh/create_edge_loops").execute(*args, **kwargs)
            def create_intersect_loop(self, *args, **kwargs):
                """
                Creates an interior edge loop at the intersection between two adjacent face zones. Edges created in this way will not be remeshed by default. 
                """
                return PyMenu(self.service, "/boundary/remesh/create_intersect_loop").execute(*args, **kwargs)
            def create_all_intrst_loops(self, *args, **kwargs):
                """
                Creates edge loop of intersection for all boundary zones in current domain. 
                """
                return PyMenu(self.service, "/boundary/remesh/create_all_intrst_loops").execute(*args, **kwargs)
            def create_join_loop(self, *args, **kwargs):
                """
                Creates edge loop on boundary of the region of overlap of two surfaces. 
                """
                return PyMenu(self.service, "/boundary/remesh/create_join_loop").execute(*args, **kwargs)
            def create_stitch_loop(self, *args, **kwargs):
                """
                Creates edge loops for connecting two surfaces along their free edges. 
                """
                return PyMenu(self.service, "/boundary/remesh/create_stitch_loop").execute(*args, **kwargs)
            def delete_overlapped_edges(self, *args, **kwargs):
                """
                Deletes edges that overlap selected edge loops. 
                """
                return PyMenu(self.service, "/boundary/remesh/delete_overlapped_edges").execute(*args, **kwargs)
            def intersect_face_zones(self, *args, **kwargs):
                """
                Remeshes two intersecting face zones so that they become conformal.   After the intersect operation, remesh is called automatically. To disable the post-remesh operation, use the text command:  /boundary/remesh/controls/intersect/remesh-post-intersection?
                               no
                            
                """
                return PyMenu(self.service, "/boundary/remesh/intersect_face_zones").execute(*args, **kwargs)
            def intersect_all_face_zones(self, *args, **kwargs):
                """
                Remeshes all the intersecting face zones.   After the intersect operation, remesh is called automatically. To disable the post-remesh operation, use the text command:  /boundary/remesh/controls/intersect/remesh-post-intersection?
                               no
                            
                """
                return PyMenu(self.service, "/boundary/remesh/intersect_all_face_zones").execute(*args, **kwargs)
            def remesh_face_zone(self, *args, **kwargs):
                """
                Remeshes a specified face zone by automatically extracting edge loops. If edge loops are present in the current domain (for example, if they were created using the create-edge-loops command), they are used to remesh the specified face zone. 
                """
                return PyMenu(self.service, "/boundary/remesh/remesh_face_zone").execute(*args, **kwargs)
            def remesh_marked_faces(self, *args, **kwargs):
                """
                Locally remesh marked faces.
                """
                return PyMenu(self.service, "/boundary/remesh/remesh_marked_faces").execute(*args, **kwargs)
            def mark_intersecting_faces(self, *args, **kwargs):
                """
                Highlights the triangles in the neighborhood of the line of intersection. 
                """
                return PyMenu(self.service, "/boundary/remesh/mark_intersecting_faces").execute(*args, **kwargs)
            def remesh_face_zones_conformally(self, *args, **kwargs):
                """
                Remeshes face zones using the current size function and keeping a conformal interface between them. If no size function is defined, an error message will be generated.  This command will prompt for:
                                  
                                     
                                        
                                           Boundary Face Zones
                                        
                                     
                                     
                                        
                                           Boundary Edge Zones
                                        
                                     
                                     
                                        
                                           feature angle – used to determine the minimum angle between features that will be preserved during remeshing 
                                     
                                     
                                        
                                           corner angle – used to specify the minimum angle between feature edges that will be preserved 
                                     
                                     
                                        
                                           Replace Face Zone? – (default is Yes) the remeshed face zone(s) will take the name and -id of the original zones, and the original face zone(s) will have “orig” appended to their name. If No, the remeshed face zone(s) will have “retri” added postfix. 
                                     
                                  
                                 Periodic face zones cannot be remeshed using this command.
                """
                return PyMenu(self.service, "/boundary/remesh/remesh_face_zones_conformally").execute(*args, **kwargs)
            def remesh_constant_size(self, *args, **kwargs):
                """
                Remeshes the specified face zones to a constant triangle size while maintaining conformity with adjacent zones. Specify the boundary face zones to be remeshed, the boundary edge zones, feature angle, corner angle, and the constant size. Additionally, specify whether the current boundary face zones should be replaced by the remeshed face zones after the operation is complete.
                """
                return PyMenu(self.service, "/boundary/remesh/remesh_constant_size").execute(*args, **kwargs)
            def coarsen_and_refine(self, *args, **kwargs):
                """
                Remeshes (coarsens/refines) the boundary face zones based on the computed size field. Specify the boundary face zones to be remeshed, the boundary edge zones, feature angle, and corner angle. Additionally, specify whether the current boundary face zones should be replaced by the remeshed face zones after the operation is complete.
                """
                return PyMenu(self.service, "/boundary/remesh/coarsen_and_refine").execute(*args, **kwargs)
            def remesh_overlapping_zones(self, *args, **kwargs):
                """
                Remeshes overlapping face zones. The non-overlapping region is remeshed using the edge loops created from the overlapping face zones. 
                """
                return PyMenu(self.service, "/boundary/remesh/remesh_overlapping_zones").execute(*args, **kwargs)
            def join_face_zones(self, *args, **kwargs):
                """
                Connects two overlapping faces.   After the join operation, remesh is called automatically. To disable the post-remesh operation, use the text command:  /boundary/remesh/controls/intersect/remesh-post-intersection?
                               no
                            
                """
                return PyMenu(self.service, "/boundary/remesh/join_face_zones").execute(*args, **kwargs)
            def join_all_face_zones(self, *args, **kwargs):
                """
                Connects all overlapping face zones using the join operation.   After the join operation, remesh is called automatically. To disable the post-remesh operation, use the text command:  /boundary/remesh/controls/intersect/remesh-post-intersection?
                               no
                            
                """
                return PyMenu(self.service, "/boundary/remesh/join_all_face_zones").execute(*args, **kwargs)
            def mark_join_faces(self, *args, **kwargs):
                """
                Highlights the triangles in the neighborhood of the join edge loop. 
                """
                return PyMenu(self.service, "/boundary/remesh/mark_join_faces").execute(*args, **kwargs)
            def stitch_face_zones(self, *args, **kwargs):
                """
                Connects two surfaces along their free edges.   After the stitch operation, remesh is called automatically. To disable the post-remesh operation, use the text command:  /boundary/remesh/controls/intersect/remesh-post-intersection?
                               no
                            
                """
                return PyMenu(self.service, "/boundary/remesh/stitch_face_zones").execute(*args, **kwargs)
            def stitch_all_face_zones(self, *args, **kwargs):
                """
                Connects (stitches) all the face zones along the free edges.   After the stitch operation, remesh is called automatically. To disable the post-remesh operation, use the text command:  /boundary/remesh/controls/intersect/remesh-post-intersection?
                               no
                            
                """
                return PyMenu(self.service, "/boundary/remesh/stitch_all_face_zones").execute(*args, **kwargs)
            def triangulate(self, *args, **kwargs):
                """
                Triangulates quad zones. 
                """
                return PyMenu(self.service, "/boundary/remesh/triangulate").execute(*args, **kwargs)
            def mark_stitch_faces(self, *args, **kwargs):
                """
                Highlights the triangles in the neighborhood of the stitch edge loop. 
                """
                return PyMenu(self.service, "/boundary/remesh/mark_stitch_faces").execute(*args, **kwargs)
            def faceted_stitch_zones(self, *args, **kwargs):
                """
                Performs the faceted stitching of zones. 
                """
                return PyMenu(self.service, "/boundary/remesh/faceted_stitch_zones").execute(*args, **kwargs)
            def insert_edge_zone(self, *args, **kwargs):
                """
                Inserts an edge zone into a triangulated boundary face zone. 
                """
                return PyMenu(self.service, "/boundary/remesh/insert_edge_zone").execute(*args, **kwargs)
            def clear_marked_faces(self, *args, **kwargs):
                """
                Clears the highlighting of the triangles that are marked. 
                """
                return PyMenu(self.service, "/boundary/remesh/clear_marked_faces").execute(*args, **kwargs)
            def stitch_with_preserve_boundary(self, *args, **kwargs):
                """
                Connects (stitches) a zone to another which is connected to an existing volume mesh, while preserving the boundary of the zones connected to the volume mesh. Specify a list of boundary zones to be preserved, a list of the boundary zones to be connected to each of these zones, and the tolerance value.   After the stitch operation, remesh is called automatically. To disable the post-remesh operation, use the text command:  /boundary/remesh/controls/intersect/remesh-post-intersection?
                               no  This command will not work for overlapping or partially overlapping face zones.
                """
                return PyMenu(self.service, "/boundary/remesh/stitch_with_preserve_boundary").execute(*args, **kwargs)

            class controls(metaclass=PyMenuMeta):
                """
                Enters the edge loop tools text menu. 
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                    self.intersect = self.__class__.intersect(path + [("intersect", None)], service)
                def remesh_method(self, *args, **kwargs):
                    """
                    Specifies the method to be used for the node distribution on the edge loop. 
                    """
                    return PyMenu(self.service, "/boundary/remesh/controls/remesh_method").execute(*args, **kwargs)
                def quadratic_recon(self, *args, **kwargs):
                    """
                    Enables/disables quadratic reconstruction of edge loops. 
                    """
                    return PyMenu(self.service, "/boundary/remesh/controls/quadratic_recon").execute(*args, **kwargs)
                def spacing(self, *args, **kwargs):
                    """
                    Sets the node spacing for the edge loop. 
                    """
                    return PyMenu(self.service, "/boundary/remesh/controls/spacing").execute(*args, **kwargs)
                def delete_overlapped(self, *args, **kwargs):
                    """
                    Toggles the deletion of region of overlap of the two surfaces. 
                    """
                    return PyMenu(self.service, "/boundary/remesh/controls/delete_overlapped").execute(*args, **kwargs)
                def tolerance(self, *args, **kwargs):
                    """
                    Sets the tolerance for determining if two edges intersect. 
                    """
                    return PyMenu(self.service, "/boundary/remesh/controls/tolerance").execute(*args, **kwargs)
                def project_method(self, *args, **kwargs):
                    """
                    Specifies the method for projecting edge loops. 
                    """
                    return PyMenu(self.service, "/boundary/remesh/controls/project_method").execute(*args, **kwargs)
                def direction(self, *args, **kwargs):
                    """
                    Specifies the direction of the edge loop projection. 
                    """
                    return PyMenu(self.service, "/boundary/remesh/controls/direction").execute(*args, **kwargs)
                def proximity_local_search(self, *args, **kwargs):
                    """
                    Includes the selected face for proximity calculation. 
                    """
                    return PyMenu(self.service, "/boundary/remesh/controls/proximity_local_search").execute(*args, **kwargs)

                class intersect(metaclass=PyMenuMeta):
                    """
                    Enters the intersect control menu. 
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                    def within_tolerance(self, *args, **kwargs):
                        """
                        Performs the intersection operation only within the specified tolerance value. It is useful only for the Intersect option. 
                        """
                        return PyMenu(self.service, "/boundary/remesh/controls/intersect/within_tolerance").execute(*args, **kwargs)
                    def delete_overlap(self, *args, **kwargs):
                        """
                        Enables/disables the deletion of overlapped edges. It toggles the automatic deletion of region of overlap of the two surfaces. This option is used by while remeshing overlapping zones and retriangulating prisms. By default, this option is enabled. 
                        """
                        return PyMenu(self.service, "/boundary/remesh/controls/intersect/delete_overlap").execute(*args, **kwargs)
                    def ignore_parallel_faces(self, *args, **kwargs):
                        """
                        Default is yes. If there are close-to-parallel faces, set to no to separate the zones and avoid creating an intersection loop.
                        """
                        return PyMenu(self.service, "/boundary/remesh/controls/intersect/ignore_parallel_faces").execute(*args, **kwargs)
                    def refine_region(self, *args, **kwargs):
                        """
                        Enables you to refine the regions that are modified during the intersect operations. It toggles the refinement of the intersecting regions after performing any of the intersection operation.   This operation improves the quality of the resulting mesh, however, this option is disabled by default. 
                        """
                        return PyMenu(self.service, "/boundary/remesh/controls/intersect/refine_region").execute(*args, **kwargs)
                    def separate(self, *args, **kwargs):
                        """
                        Enables the automatic separation of intersected zones. 
                        """
                        return PyMenu(self.service, "/boundary/remesh/controls/intersect/separate").execute(*args, **kwargs)
                    def absolute_tolerance(self, *args, **kwargs):
                        """
                        Enables you to switch between the use of absolute and relative tolerance. By default, the relative tolerance value is used. 
                        """
                        return PyMenu(self.service, "/boundary/remesh/controls/intersect/absolute_tolerance").execute(*args, **kwargs)
                    def retri_improve(self, *args, **kwargs):
                        """
                        Enables you to improve the mesh. After performing any intersection operation, the slivers are removed along the curve of intersection, Laplace smoothing is performed, and followed by the edge swapping. Laplace smoothing is also performed for insert-edge-zone, remesh-overlapped-zones, and prism-retriangulation options. Smoothing is performed again. The smooth-swap operations can be controlled by changing the various defaults such as swapping iterations, smoothing iterations, etc. 
                        """
                        return PyMenu(self.service, "/boundary/remesh/controls/intersect/retri_improve").execute(*args, **kwargs)
                    def stitch_preserve(self, *args, **kwargs):
                        """
                        Indicates that shape of the first zone specified is to be preserved. This option is enabled by default. 
                        """
                        return PyMenu(self.service, "/boundary/remesh/controls/intersect/stitch_preserve").execute(*args, **kwargs)
                    def tolerance(self, *args, **kwargs):
                        """
                        Specifies the tolerance value for the intersect operations. 
                        """
                        return PyMenu(self.service, "/boundary/remesh/controls/intersect/tolerance").execute(*args, **kwargs)
                    def join_match_angle(self, *args, **kwargs):
                        """
                        Specifies the allowed maximum angle between the normals of the two overlapping surfaces to be joined. This parameter is used to control the size of the join region. 
                        """
                        return PyMenu(self.service, "/boundary/remesh/controls/intersect/join_match_angle").execute(*args, **kwargs)
                    def feature_angle(self, *args, **kwargs):
                        """
                        Specifies the minimum feature angle that should be considered while retriangulating the boundary zones. All the edges in the zone having feature angle greater than the specified feature angle are retained. This option is useful for preserving the shape of the intersecting boundary zones. The default value of feature angle is 40, however, a value in the range of 10–50 degrees is recommended. A large value may distort the shape of the intersecting boundary zones.
                        """
                        return PyMenu(self.service, "/boundary/remesh/controls/intersect/feature_angle").execute(*args, **kwargs)
                    def join_project_angle(self, *args, **kwargs):
                        """
                        Specifies the allowed maximum angle between the face normal and the project direction for the overlapping surfaces to be joined. This parameter is used to control the size of the join region. 
                        """
                        return PyMenu(self.service, "/boundary/remesh/controls/intersect/join_project_angle").execute(*args, **kwargs)
                    def remesh_post_intersection(self, *args, **kwargs):
                        """
                        Used to enable or disable automatic post-remesh operation after any connect operation (join, intersect, or stitch).
                        """
                        return PyMenu(self.service, "/boundary/remesh/controls/intersect/remesh_post_intersection").execute(*args, **kwargs)

            class size_functions(metaclass=PyMenuMeta):
                """
                Enters the size functions menu where you can define size functions for controlling mesh size distribution. 
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                    self.contours = self.__class__.contours(path + [("contours", None)], service)
                    self.controls = self.__class__.controls(path + [("controls", None)], service)
                def create(self, *args, **kwargs):
                    """
                    Defines the size function based on the specified parameters. 
                    """
                    return PyMenu(self.service, "/boundary/remesh/size_functions/create").execute(*args, **kwargs)
                def delete(self, *args, **kwargs):
                    """
                    Deletes the specified size function or the current size field. 
                    """
                    return PyMenu(self.service, "/boundary/remesh/size_functions/delete").execute(*args, **kwargs)
                def delete_all(self, *args, **kwargs):
                    """
                    Deletes all the defined size functions. 
                    """
                    return PyMenu(self.service, "/boundary/remesh/size_functions/delete_all").execute(*args, **kwargs)
                def compute(self, *args, **kwargs):
                    """
                    Computes the size field based on the defined parameters.
                    """
                    return PyMenu(self.service, "/boundary/remesh/size_functions/compute").execute(*args, **kwargs)
                def list(self, *args, **kwargs):
                    """
                    Lists all the defined size functions and the parameter values defined. 
                    """
                    return PyMenu(self.service, "/boundary/remesh/size_functions/list").execute(*args, **kwargs)
                def create_defaults(self, *args, **kwargs):
                    """
                    Creates default size functions based on face and edge curvature and proximity.
                    """
                    return PyMenu(self.service, "/boundary/remesh/size_functions/create_defaults").execute(*args, **kwargs)
                def set_global_controls(self, *args, **kwargs):
                    """
                    Sets the values for the global minimum and maximum size, and the growth rate. 
                    """
                    return PyMenu(self.service, "/boundary/remesh/size_functions/set_global_controls").execute(*args, **kwargs)
                def enable_periodicity_filter(self, *args, **kwargs):
                    """
                    Enable size field periodicity.
                    """
                    return PyMenu(self.service, "/boundary/remesh/size_functions/enable_periodicity_filter").execute(*args, **kwargs)
                def disable_periodicity_filter(self, *args, **kwargs):
                    """
                    Removes periodicity from the size field.
                    """
                    return PyMenu(self.service, "/boundary/remesh/size_functions/disable_periodicity_filter").execute(*args, **kwargs)
                def list_periodicity_filter(self, *args, **kwargs):
                    """
                    List periodic in size field.
                    """
                    return PyMenu(self.service, "/boundary/remesh/size_functions/list_periodicity_filter").execute(*args, **kwargs)
                def set_scaling_filter(self, *args, **kwargs):
                    """
                    Specifies the scale factor, and minimum and maximum size values to filter the size output from the size field. 
                    """
                    return PyMenu(self.service, "/boundary/remesh/size_functions/set_scaling_filter").execute(*args, **kwargs)
                def reset_global_controls(self, *args, **kwargs):
                    """
                    Resets the global controls to their default values. 
                    """
                    return PyMenu(self.service, "/boundary/remesh/size_functions/reset_global_controls").execute(*args, **kwargs)
                def set_prox_gap_tolerance(self, *args, **kwargs):
                    """
                    Sets the tolerance relative to minimum size to take gaps into account. Gaps whose thickness is less than the global minimum size multiplied by this factor will not be regarded as a proximity gap.
                    """
                    return PyMenu(self.service, "/boundary/remesh/size_functions/set_prox_gap_tolerance").execute(*args, **kwargs)
                def triangulate_quad_faces(self, *args, **kwargs):
                    """
                    Identifies the zones comprising non-triangular elements and uses a triangulated copy of these zones for computing the size functions.
                    """
                    return PyMenu(self.service, "/boundary/remesh/size_functions/triangulate_quad_faces").execute(*args, **kwargs)
                def use_cad_imported_curvature(self, *args, **kwargs):
                    """
                    Enables/disables curvature data from the nodes of the CAD facets.
                    """
                    return PyMenu(self.service, "/boundary/remesh/size_functions/use_cad_imported_curvature").execute(*args, **kwargs)

                class contours(metaclass=PyMenuMeta):
                    """
                    Contains options for displaying contours of size functions.
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                        self.set = self.__class__.set(path + [("set", None)], service)
                    def draw(self, *args, **kwargs):
                        """
                        Displays contours in the graphics window. Compute the size field using /size-functions/compute or read in a size field file prior to displaying the contours of size.
                        """
                        return PyMenu(self.service, "/boundary/remesh/size_functions/contours/draw").execute(*args, **kwargs)

                    class set(metaclass=PyMenuMeta):
                        """
                        Set contour options.
                        """
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service
                        def refine_facets(self, *args, **kwargs):
                            """
                            Enables you to specify smaller facets if the original are too large. Default is no.
                            """
                            return PyMenu(self.service, "/boundary/remesh/size_functions/contours/set/refine_facets").execute(*args, **kwargs)

                class controls(metaclass=PyMenuMeta):
                    """
                    Menu to control different behavior of sf.
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                    def meshed_sf_behavior(self, *args, **kwargs):
                        """
                        Set meshed size function processing to hard.
                        """
                        return PyMenu(self.service, "/boundary/remesh/size_functions/controls/meshed_sf_behavior").execute(*args, **kwargs)
                    def curvature_method(self, *args, **kwargs):
                        """
                        Option to get facet curvature.
                        """
                        return PyMenu(self.service, "/boundary/remesh/size_functions/controls/curvature_method").execute(*args, **kwargs)

        class improve(metaclass=PyMenuMeta):
            """
            Enables you to improve boundary surfaces. 
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def collapse_bad_faces(self, *args, **kwargs):
                """
                Enables you to collapse the short edge of faces having a high aspect ratio or skewness in the specified face zone(s). 
                """
                return PyMenu(self.service, "/boundary/improve/collapse_bad_faces").execute(*args, **kwargs)
            def improve(self, *args, **kwargs):
                """
                Enables you to improve the boundary surface quality using skewness, size change, aspect ratio, or area as the quality measure. 
                """
                return PyMenu(self.service, "/boundary/improve/improve").execute(*args, **kwargs)
            def smooth(self, *args, **kwargs):
                """
                Enables you to improve the boundary surface using smoothing. 
                """
                return PyMenu(self.service, "/boundary/improve/smooth").execute(*args, **kwargs)
            def swap(self, *args, **kwargs):
                """
                Enables you to improve the boundary surface using edge swapping. 
                """
                return PyMenu(self.service, "/boundary/improve/swap").execute(*args, **kwargs)
            def degree_swap(self, *args, **kwargs):
                """
                Enables you to improve the boundary mesh by swapping edges based on a node degree value other than 6. The node degree is defined as the number of edges connected to the node.
                """
                return PyMenu(self.service, "/boundary/improve/degree_swap").execute(*args, **kwargs)

        class separate(metaclass=PyMenuMeta):
            """
            Contains options for separating face zones. 
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
                self.local_regions = self.__class__.local_regions(path + [("local_regions", None)], service)
            def mark_faces_in_region(self, *args, **kwargs):
                """
                Marks the faces that are contained in a specified local refinement region. 
                """
                return PyMenu(self.service, "/boundary/separate/mark_faces_in_region").execute(*args, **kwargs)
            def sep_face_zone_by_angle(self, *args, **kwargs):
                """
                Separates a boundary face zone based on significant angle. 
                """
                return PyMenu(self.service, "/boundary/separate/sep_face_zone_by_angle").execute(*args, **kwargs)
            def sep_face_zone_by_cnbor(self, *args, **kwargs):
                """
                Separates a boundary/interior face zone based on its cell neighbors. 
                """
                return PyMenu(self.service, "/boundary/separate/sep_face_zone_by_cnbor").execute(*args, **kwargs)
            def sep_face_zone_by_mark(self, *args, **kwargs):
                """
                Separates a boundary face zone by moving marked faces to a new zone. 
                """
                return PyMenu(self.service, "/boundary/separate/sep_face_zone_by_mark").execute(*args, **kwargs)
            def sep_face_zone_by_region(self, *args, **kwargs):
                """
                Separates a boundary face zone based on contiguous regions. 
                """
                return PyMenu(self.service, "/boundary/separate/sep_face_zone_by_region").execute(*args, **kwargs)
            def sep_face_zone_by_seed(self, *args, **kwargs):
                """
                Separates a boundary face zone by defining a seed face on the surface. 
                """
                return PyMenu(self.service, "/boundary/separate/sep_face_zone_by_seed").execute(*args, **kwargs)
            def sep_face_zone_by_seed_angle(self, *args, **kwargs):
                """
                Separates faces connected to the seed face, whose normal fall within the specified cone. 
                """
                return PyMenu(self.service, "/boundary/separate/sep_face_zone_by_seed_angle").execute(*args, **kwargs)
            def sep_face_zone_by_shape(self, *args, **kwargs):
                """
                Separates a boundary face zone based on the shape of the faces (triangular or quadrilateral). 
                """
                return PyMenu(self.service, "/boundary/separate/sep_face_zone_by_shape").execute(*args, **kwargs)

            class local_regions(metaclass=PyMenuMeta):
                """
                Enters the local refinement menu. 
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def define(self, *args, **kwargs):
                    """
                    Enables you to define the local region. 
                    """
                    return PyMenu(self.service, "/boundary/separate/local_regions/define").execute(*args, **kwargs)
                def delete(self, *args, **kwargs):
                    """
                    Deletes the specified local region. 
                    """
                    return PyMenu(self.service, "/boundary/separate/local_regions/delete").execute(*args, **kwargs)
                def init(self, *args, **kwargs):
                    """
                    Creates a region encompassing the entire geometry. 
                    """
                    return PyMenu(self.service, "/boundary/separate/local_regions/init").execute(*args, **kwargs)
                def list_all_regions(self, *args, **kwargs):
                    """
                    Lists all the local regions defined. 
                    """
                    return PyMenu(self.service, "/boundary/separate/local_regions/list_all_regions").execute(*args, **kwargs)

        class manage(metaclass=PyMenuMeta):
            """
            Contains options for manipulating the boundary zones.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
                self.user_defined_groups = self.__class__.user_defined_groups(path + [("user_defined_groups", None)], service)
            def auto_delete_nodes(self, *args, **kwargs):
                """
                Specifies whether or not unused nodes should be deleted when their face zone is deleted. 
                """
                return PyMenu(self.service, "/boundary/manage/auto_delete_nodes").execute(*args, **kwargs)
            def copy(self, *args, **kwargs):
                """
                Copies all nodes and faces of the specified face zone(s). 
                """
                return PyMenu(self.service, "/boundary/manage/copy").execute(*args, **kwargs)
            def change_prefix(self, *args, **kwargs):
                """
                Enables you to change the prefix for the specified face zones. 
                """
                return PyMenu(self.service, "/boundary/manage/change_prefix").execute(*args, **kwargs)
            def change_suffix(self, *args, **kwargs):
                """
                Change the suffix for specified face zones.
                """
                return PyMenu(self.service, "/boundary/manage/change_suffix").execute(*args, **kwargs)
            def create(self, *args, **kwargs):
                """
                Creates a new face zone. 
                """
                return PyMenu(self.service, "/boundary/manage/create").execute(*args, **kwargs)
            def delete(self, *args, **kwargs):
                """
                Deletes the face zone. 
                """
                return PyMenu(self.service, "/boundary/manage/delete").execute(*args, **kwargs)
            def flip(self, *args, **kwargs):
                """
                Reverses the normal direction of the specified boundary zone(s). 
                """
                return PyMenu(self.service, "/boundary/manage/flip").execute(*args, **kwargs)
            def id(self, *args, **kwargs):
                """
                Specifies a new boundary zone ID. If there is a conflict, the change will be ignored. 
                """
                return PyMenu(self.service, "/boundary/manage/id").execute(*args, **kwargs)
            def list(self, *args, **kwargs):
                """
                Prints information about all boundary zones. 
                """
                return PyMenu(self.service, "/boundary/manage/list").execute(*args, **kwargs)
            def merge(self, *args, **kwargs):
                """
                Merges face zones. 
                """
                return PyMenu(self.service, "/boundary/manage/merge").execute(*args, **kwargs)
            def name(self, *args, **kwargs):
                """
                Gives a face zone a new name. 
                """
                return PyMenu(self.service, "/boundary/manage/name").execute(*args, **kwargs)
            def remove_suffix(self, *args, **kwargs):
                """
                Removes the suffix (characters including and after the leftmost ":") in the face zone names.
                """
                return PyMenu(self.service, "/boundary/manage/remove_suffix").execute(*args, **kwargs)
            def orient(self, *args, **kwargs):
                """
                Consistently orients the faces in the specified zones. 
                """
                return PyMenu(self.service, "/boundary/manage/orient").execute(*args, **kwargs)
            def origin(self, *args, **kwargs):
                """
                Specifies a new origin for the mesh, to be used for face zone rotation and for periodic zone creation. The default origin is (0,0,0). 
                """
                return PyMenu(self.service, "/boundary/manage/origin").execute(*args, **kwargs)
            def rotate(self, *args, **kwargs):
                """
                Rotates all nodes of the specified face zone(s). 
                """
                return PyMenu(self.service, "/boundary/manage/rotate").execute(*args, **kwargs)
            def rotate_model(self, *args, **kwargs):
                """
                Rotates all nodes of the model through the specified angle, based on the specified point and axis of rotation.
                """
                return PyMenu(self.service, "/boundary/manage/rotate_model").execute(*args, **kwargs)
            def scale(self, *args, **kwargs):
                """
                Scales all nodes of the specified face zone(s). 
                """
                return PyMenu(self.service, "/boundary/manage/scale").execute(*args, **kwargs)
            def scale_model(self, *args, **kwargs):
                """
                Scales all nodes of the model by multiplying the node coordinates by the specified scale factors (x, y, z). 
                """
                return PyMenu(self.service, "/boundary/manage/scale_model").execute(*args, **kwargs)
            def translate(self, *args, **kwargs):
                """
                Translates all nodes of the specified face zone(s). 
                """
                return PyMenu(self.service, "/boundary/manage/translate").execute(*args, **kwargs)
            def translate_model(self, *args, **kwargs):
                """
                Translates all nodes of the model by the specified translation offsets (x, y, z).   The translation offsets are interpreted as absolute numbers in meshing mode. In solution mode, however, the translation offsets are assumed to be distances in the length unit set. This may lead to differences in domain extents reported after translating the mesh in the respective modes.
                """
                return PyMenu(self.service, "/boundary/manage/translate_model").execute(*args, **kwargs)
            def type(self, *args, **kwargs):
                """
                Changes the boundary type of the face zone.   When changing the boundary type of any zone to type interior, ensure that there is a single cell zone across the interior boundary. Retaining multiple cell zones across an interior boundary can cause undesirable results with further tet meshing or smoothing operations.  Also, face zones having no/one neighboring cell zone should not be changed to type interior.  The mesh check will issue a warning if multiple cell zones are maintained across an interior boundary. The boundary type in such cases should be set to internal instead.
                """
                return PyMenu(self.service, "/boundary/manage/type").execute(*args, **kwargs)

            class user_defined_groups(metaclass=PyMenuMeta):
                """
                Enables you to manipulate user-defined groups. 
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def create(self, *args, **kwargs):
                    """
                    Creates the user-defined group comprising the specified zones. 
                    """
                    return PyMenu(self.service, "/boundary/manage/user_defined_groups/create").execute(*args, **kwargs)
                def activate(self, *args, **kwargs):
                    """
                    Activates the specified user-defined groups. 
                    """
                    return PyMenu(self.service, "/boundary/manage/user_defined_groups/activate").execute(*args, **kwargs)
                def update(self, *args, **kwargs):
                    """
                    Enables you to modify an existing group. 
                    """
                    return PyMenu(self.service, "/boundary/manage/user_defined_groups/update").execute(*args, **kwargs)
                def delete(self, *args, **kwargs):
                    """
                    Deletes the specified user-defined group. 
                    """
                    return PyMenu(self.service, "/boundary/manage/user_defined_groups/delete").execute(*args, **kwargs)
                def list(self, *args, **kwargs):
                    """
                    Lists the groups in the console. 
                    """
                    return PyMenu(self.service, "/boundary/manage/user_defined_groups/list").execute(*args, **kwargs)

        class shell_boundary_layer(metaclass=PyMenuMeta):
            """
            Enter the shell boundary layer menu.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
                self.controls = self.__class__.controls(path + [("controls", None)], service)
            def create(self, *args, **kwargs):
                """
                Create shell boundary layers from one or more face zones.
                """
                return PyMenu(self.service, "/boundary/shell_boundary_layer/create").execute(*args, **kwargs)

            class controls(metaclass=PyMenuMeta):
                """
                Shell Boundary Layer Controls.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                    self.zone_specific_growth = self.__class__.zone_specific_growth(path + [("zone_specific_growth", None)], service)

                class zone_specific_growth(metaclass=PyMenuMeta):
                    """
                    Shell boundary Layer Growth Controls.
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                    def apply_growth(self, *args, **kwargs):
                        """
                        Apply  shell boundary la growth on individual edge zones.
                        """
                        return PyMenu(self.service, "/boundary/shell_boundary_layer/controls/zone_specific_growth/apply_growth").execute(*args, **kwargs)
                    def clear_growth(self, *args, **kwargs):
                        """
                        Clear shell boundary layer specific growth on individual edge zones.
                        """
                        return PyMenu(self.service, "/boundary/shell_boundary_layer/controls/zone_specific_growth/clear_growth").execute(*args, **kwargs)

        class boundary_conditions(metaclass=PyMenuMeta):
            """
            Contains options for copying or clearing boundary conditions when a case file is read.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def copy(self, *args, **kwargs):
                """
                Enables you to copy the boundary conditions from the face zone selected to the face zones specified.
                """
                return PyMenu(self.service, "/boundary/boundary_conditions/copy").execute(*args, **kwargs)
            def clear(self, *args, **kwargs):
                """
                Clears the boundary conditions assigned to the specified face zones.
                """
                return PyMenu(self.service, "/boundary/boundary_conditions/clear").execute(*args, **kwargs)
            def clear_all(self, *args, **kwargs):
                """
                Clears the boundary conditions assigned to all the face zones.
                """
                return PyMenu(self.service, "/boundary/boundary_conditions/clear_all").execute(*args, **kwargs)

    class cad_assemblies(metaclass=PyMenuMeta):
        """
        Menu for cad assemblies.
        """
        def __init__(self, path, service):
            self.path = path
            self.service = service
            self.draw_options = self.__class__.draw_options(path + [("draw_options", None)], service)
            self.manage_state = self.__class__.manage_state(path + [("manage_state", None)], service)
            self.labels = self.__class__.labels(path + [("labels", None)], service)
            self.update_options = self.__class__.update_options(path + [("update_options", None)], service)
        def draw(self, *args, **kwargs):
            """
            Displays the selected CAD entities.
            """
            return PyMenu(self.service, "/cad_assemblies/draw").execute(*args, **kwargs)
        def create_objects(self, *args, **kwargs):
            """
            Enables you to create new geometry/mesh objects for the selected entities. Specify the path for the entities and if required, choose to create one object per CAD entity selected and/or retain the CAD zone granularity for object creation. By default, a single object will be created for all entities selected and the CAD zone granularity will not be retained. Specify the object name (if applicable), object type (geom or mesh), and cell zone type (dead, fluid, or solid).
            """
            return PyMenu(self.service, "/cad_assemblies/create_objects").execute(*args, **kwargs)
        def add_to_object(self, *args, **kwargs):
            """
            Enables you to add the selected CAD entities to an existing object. Specify the path for the entities to be added and select the object to be modified.
            """
            return PyMenu(self.service, "/cad_assemblies/add_to_object").execute(*args, **kwargs)
        def replace_object(self, *args, **kwargs):
            """
            Enables you to replace an object with the selected CAD entities. Specify the path for the entities to be added and select the object to be modified.
            """
            return PyMenu(self.service, "/cad_assemblies/replace_object").execute(*args, **kwargs)
        def extract_edges_zones(self, *args, **kwargs):
            """
            Extract feature edges for CAD assemblies.
            """
            return PyMenu(self.service, "/cad_assemblies/extract_edges_zones").execute(*args, **kwargs)
        def update_cad_assemblies(self, *args, **kwargs):
            """
            Reimports the selected CAD entities using new parameters specified in the update-options/ menu. 
            """
            return PyMenu(self.service, "/cad_assemblies/update_cad_assemblies").execute(*args, **kwargs)
        def rename(self, *args, **kwargs):
            """
            Enables you to rename the selected entities. Specify the path for the entities and the new name. For multiple entities, the specified name will be used, with a suitable index as suffix. For example, specifying a new name wall will result in entities wall.1, wall.2, etc.
            """
            return PyMenu(self.service, "/cad_assemblies/rename").execute(*args, **kwargs)
        def add_prefix(self, *args, **kwargs):
            """
            Enables you to add a prefix to the selected entities. Specify the path for the entities and the prefix to be added.
            """
            return PyMenu(self.service, "/cad_assemblies/add_prefix").execute(*args, **kwargs)
        def delete_cad_assemblies(self, *args, **kwargs):
            """
            Deletes all the CAD assemblies data.
            """
            return PyMenu(self.service, "/cad_assemblies/delete_cad_assemblies").execute(*args, **kwargs)

        class draw_options(metaclass=PyMenuMeta):
            """
            Contains additional options for displaying CAD entities.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def add_to_graphics(self, *args, **kwargs):
                """
                Adds the selected entities to the display in the graphics window.
                """
                return PyMenu(self.service, "/cad_assemblies/draw_options/add_to_graphics").execute(*args, **kwargs)
            def remove_from_graphics(self, *args, **kwargs):
                """
                Removes the selected entities from the display in the graphics window.
                """
                return PyMenu(self.service, "/cad_assemblies/draw_options/remove_from_graphics").execute(*args, **kwargs)
            def draw_unlabelled_zones(self, *args, **kwargs):
                """
                Displays the unlabeled zones for the selected entities in the graphics window.
                """
                return PyMenu(self.service, "/cad_assemblies/draw_options/draw_unlabelled_zones").execute(*args, **kwargs)

        class manage_state(metaclass=PyMenuMeta):
            """
            Contains options for setting the CAD entity state.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def unlock(self, *args, **kwargs):
                """
                Unlocks the selected CAD entities.
                """
                return PyMenu(self.service, "/cad_assemblies/manage_state/unlock").execute(*args, **kwargs)
            def suppress(self, *args, **kwargs):
                """
                Suppresses the selected CAD entities.
                """
                return PyMenu(self.service, "/cad_assemblies/manage_state/suppress").execute(*args, **kwargs)
            def unsuppress(self, *args, **kwargs):
                """
                Unsuppresses the selected CAD entities.
                """
                return PyMenu(self.service, "/cad_assemblies/manage_state/unsuppress").execute(*args, **kwargs)

        class labels(metaclass=PyMenuMeta):
            """
            Contains options for displaying and managing labels.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def draw(self, *args, **kwargs):
                """
                Displays the selected labels.
                """
                return PyMenu(self.service, "/cad_assemblies/labels/draw").execute(*args, **kwargs)
            def add_to_graphics(self, *args, **kwargs):
                """
                Adds the selected labels to the display in the graphics window.
                """
                return PyMenu(self.service, "/cad_assemblies/labels/add_to_graphics").execute(*args, **kwargs)
            def remove_from_graphics(self, *args, **kwargs):
                """
                Removes the selected labels from the display in the graphics window.
                """
                return PyMenu(self.service, "/cad_assemblies/labels/remove_from_graphics").execute(*args, **kwargs)
            def delete(self, *args, **kwargs):
                """
                Deletes the selected labels.
                """
                return PyMenu(self.service, "/cad_assemblies/labels/delete").execute(*args, **kwargs)
            def rename(self, *args, **kwargs):
                """
                Enables you to rename the selected labels. Specify the path for the labels and the new name. For multiple selections, the specified name will be used, with a suitable index as suffix. For example, specifying a new label name wall will result in entities wall.1, wall.2, etc.
                """
                return PyMenu(self.service, "/cad_assemblies/labels/rename").execute(*args, **kwargs)

        class update_options(metaclass=PyMenuMeta):
            """
            Contains options for updating the CAD entities on reimport.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def tessellation(self, *args, **kwargs):
                """
                Enables you to control the tessellation (faceting) during reimport. You can select either cad-faceting or cfd-surface-mesh.   CAD faceting enables you to control the tessellation based on the CAD faceting tolerance and maximum facet size specified.   CFD Surface Mesh enables you to use a size field file during reimport. If you enter yes, specify the size field file to be read. If you do not want to use a size field file, you can obtain conformal faceting based on the underlying curve and surface curvature (using the minimum and maximum facet sizes, and the facet curvature normal angle specified) and edge proximity (using the cells per gap specified). You can also save the size field in a file (size field is computed based on the specified parameters; that is, Min Size, Max Size, Curvature Normal Angle, Cells Per Gap).
                """
                return PyMenu(self.service, "/cad_assemblies/update_options/tessellation").execute(*args, **kwargs)
            def one_zone_per(self, *args, **kwargs):
                """
                Enables you to change the CAD zone granularity on reimport.
                """
                return PyMenu(self.service, "/cad_assemblies/update_options/one_zone_per").execute(*args, **kwargs)
            def one_object_per(self, *args, **kwargs):
                """
                Enables you to change the CAD object granularity on reimport.
                """
                return PyMenu(self.service, "/cad_assemblies/update_options/one_object_per").execute(*args, **kwargs)
            def import_edge_zones(self, *args, **kwargs):
                """
                Enables you to import edge zones from the CAD entities on reimport. Specify an appropriate value for feature angle.
                """
                return PyMenu(self.service, "/cad_assemblies/update_options/import_edge_zones").execute(*args, **kwargs)

    class preferences(metaclass=PyMenuMeta):
        """
        Set preferences.
        """
        def __init__(self, path, service):
            self.path = path
            self.service = service
            self.appearance = self.__class__.appearance(path + [("appearance", None)], service)
            self.general = self.__class__.general(path + [("general", None)], service)
            self.gpuapp = self.__class__.gpuapp(path + [("gpuapp", None)], service)
            self.graphics = self.__class__.graphics(path + [("graphics", None)], service)
            self.mat_pro_app = self.__class__.mat_pro_app(path + [("mat_pro_app", None)], service)
            self.meshing_workflow = self.__class__.meshing_workflow(path + [("meshing_workflow", None)], service)
            self.navigation = self.__class__.navigation(path + [("navigation", None)], service)
            self.prj_app = self.__class__.prj_app(path + [("prj_app", None)], service)
            self.simulation = self.__class__.simulation(path + [("simulation", None)], service)
            self.turbo_workflow = self.__class__.turbo_workflow(path + [("turbo_workflow", None)], service)

        class appearance(metaclass=PyMenuMeta):
            """
            Enter the menu for preferences covering appearance.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
                self.ansys_logo = self.__class__.ansys_logo(path + [("ansys_logo", None)], service)
                self.charts = self.__class__.charts(path + [("charts", None)], service)
                self.selections = self.__class__.selections(path + [("selections", None)], service)
            def application_font_size(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/appearance/application_font_size").execute(*args, **kwargs)
            def axis_triad(self, *args, **kwargs):
                """
                Enable or disable the visibility of the axis triad in the graphics window.
                """
                return PyMenu(self.service, "/preferences/appearance/axis_triad").execute(*args, **kwargs)
            def color_theme(self, *args, **kwargs):
                """
                Specify a color theme for the appearance of ANSYS Fluent.
                """
                return PyMenu(self.service, "/preferences/appearance/color_theme").execute(*args, **kwargs)
            def completer(self, *args, **kwargs):
                """
                Enable/disable the console automatic-completer, which suggests available commands as you type in the console.
                """
                return PyMenu(self.service, "/preferences/appearance/completer").execute(*args, **kwargs)
            def custom_title_bar(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/appearance/custom_title_bar").execute(*args, **kwargs)
            def default_view(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/appearance/default_view").execute(*args, **kwargs)
            def graphics_background_color1(self, *args, **kwargs):
                """
                Controls the primary background color of the graphics window.
                """
                return PyMenu(self.service, "/preferences/appearance/graphics_background_color1").execute(*args, **kwargs)
            def graphics_background_color2(self, *args, **kwargs):
                """
                Controls the secondary background color when the style is set as a gradient.
                """
                return PyMenu(self.service, "/preferences/appearance/graphics_background_color2").execute(*args, **kwargs)
            def graphics_background_style(self, *args, **kwargs):
                """
                Specify whether the background color is uniform or if there is a gradient.
                """
                return PyMenu(self.service, "/preferences/appearance/graphics_background_style").execute(*args, **kwargs)
            def graphics_color_theme(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/appearance/graphics_color_theme").execute(*args, **kwargs)
            def graphics_default_manual_face_color(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/appearance/graphics_default_manual_face_color").execute(*args, **kwargs)
            def graphics_default_manual_node_color(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/appearance/graphics_default_manual_node_color").execute(*args, **kwargs)
            def graphics_edge_color(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/appearance/graphics_edge_color").execute(*args, **kwargs)
            def graphics_foreground_color(self, *args, **kwargs):
                """
                Specify the color of graphics window text.
                """
                return PyMenu(self.service, "/preferences/appearance/graphics_foreground_color").execute(*args, **kwargs)
            def graphics_partition_boundary_color(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/appearance/graphics_partition_boundary_color").execute(*args, **kwargs)
            def graphics_surface_color(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/appearance/graphics_surface_color").execute(*args, **kwargs)
            def graphics_title_window_framecolor(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/appearance/graphics_title_window_framecolor").execute(*args, **kwargs)
            def graphics_view(self, *args, **kwargs):
                """
                Specify whether the default view is orthographic or perspective.
                """
                return PyMenu(self.service, "/preferences/appearance/graphics_view").execute(*args, **kwargs)
            def graphics_wall_face_color(self, *args, **kwargs):
                """
                Set the default face color for when the mesh is displayed.
                """
                return PyMenu(self.service, "/preferences/appearance/graphics_wall_face_color").execute(*args, **kwargs)
            def group_by_tree_view(self, *args, **kwargs):
                """
                Specify how boundary conditions are grouped in the tree.
                """
                return PyMenu(self.service, "/preferences/appearance/group_by_tree_view").execute(*args, **kwargs)
            def model_color_scheme(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/appearance/model_color_scheme").execute(*args, **kwargs)
            def number_of_files_recently_used(self, *args, **kwargs):
                """
                Controls how many recently-used files are listed in the File ribbon tab and the Fluent Launcher.
                """
                return PyMenu(self.service, "/preferences/appearance/number_of_files_recently_used").execute(*args, **kwargs)
            def number_of_pastel_colors(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/appearance/number_of_pastel_colors").execute(*args, **kwargs)
            def pastel_color_saturation(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/appearance/pastel_color_saturation").execute(*args, **kwargs)
            def pastel_color_value(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/appearance/pastel_color_value").execute(*args, **kwargs)
            def quick_property_view(self, *args, **kwargs):
                """
                Enables/Disables the "quick-edit" properties panels that appear when you select a boundary in the graphics windows.
                """
                return PyMenu(self.service, "/preferences/appearance/quick_property_view").execute(*args, **kwargs)
            def ruler(self, *args, **kwargs):
                """
                Adds or removes the ruler from the graphics window. Note that you must be in orthographic view for the ruler to be visible in the graphics  window.
                            
                """
                return PyMenu(self.service, "/preferences/appearance/ruler").execute(*args, **kwargs)
            def show_enabled_models(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/appearance/show_enabled_models").execute(*args, **kwargs)
            def show_interface_children_zone(self, *args, **kwargs):
                """
                Enable/disable the showing of the non-overlapping zones and interior zones associated with one-to-one mesh interfaces under Setup / Boundary Conditions (under their zone types) in the outline view tree.
                """
                return PyMenu(self.service, "/preferences/appearance/show_interface_children_zone").execute(*args, **kwargs)
            def show_model_edges(self, *args, **kwargs):
                """
                Enable/disable whether mesh edges are shown in a mesh display.
                """
                return PyMenu(self.service, "/preferences/appearance/show_model_edges").execute(*args, **kwargs)
            def solution_mode_edge_color_in_meshing_mode(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/appearance/solution_mode_edge_color_in_meshing_mode").execute(*args, **kwargs)
            def startup_page(self, *args, **kwargs):
                """
                Enable/disable the display of the startup page when ANSYS Fluent is started without loading a mesh or case file.
                """
                return PyMenu(self.service, "/preferences/appearance/startup_page").execute(*args, **kwargs)
            def surface_emissivity(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/appearance/surface_emissivity").execute(*args, **kwargs)
            def surface_specularity(self, *args, **kwargs):
                """
                Specify the specularity of all surfaces except those included in contour plots. Sepecularity is the reflectiveness of a surface; higher values (closer to 1) equate to a more reflective surface.
                """
                return PyMenu(self.service, "/preferences/appearance/surface_specularity").execute(*args, **kwargs)
            def surface_specularity_for_contours(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/appearance/surface_specularity_for_contours").execute(*args, **kwargs)
            def titles(self, *args, **kwargs):
                """
                Enable/disable the display of solver information in the graphics window.
                """
                return PyMenu(self.service, "/preferences/appearance/titles").execute(*args, **kwargs)
            def titles_border_offset(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/appearance/titles_border_offset").execute(*args, **kwargs)

            class ansys_logo(metaclass=PyMenuMeta):
                """
                Enter the menu for controlling Ansys logo visibility.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def color(self, *args, **kwargs):
                    """
                    Specify whether the Ansys logo is white or black.
                    """
                    return PyMenu(self.service, "/preferences/appearance/ansys_logo/color").execute(*args, **kwargs)
                def visible(self, *args, **kwargs):
                    """
                    Enable or disable the visibility of the Ansys logo in the graphics window.
                    """
                    return PyMenu(self.service, "/preferences/appearance/ansys_logo/visible").execute(*args, **kwargs)

            class charts(metaclass=PyMenuMeta):
                """
                Enter the menu for controlling the display of 2D charts/plots.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                    self.font = self.__class__.font(path + [("font", None)], service)
                    self.text_color = self.__class__.text_color(path + [("text_color", None)], service)
                def curve_colors(self, *args, **kwargs):
                    """
                    Specify the initial set of default colors for the rendering of curves. Note that changing this setting requires any plots to be replotted before you see the effect of the new setting.
                                
                    """
                    return PyMenu(self.service, "/preferences/appearance/charts/curve_colors").execute(*args, **kwargs)
                def enable_open_glfor_modern_plots(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/appearance/charts/enable_open_glfor_modern_plots").execute(*args, **kwargs)
                def legend_alignment(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/appearance/charts/legend_alignment").execute(*args, **kwargs)
                def legend_visibility(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/appearance/charts/legend_visibility").execute(*args, **kwargs)
                def modern_plots_enabled(self, *args, **kwargs):
                    """
                    Enables enhanced plots, which is a beta feature. Enabling this feature exposes new fields (all beta functionality).
                    """
                    return PyMenu(self.service, "/preferences/appearance/charts/modern_plots_enabled").execute(*args, **kwargs)
                def modern_plots_points_threshold(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/appearance/charts/modern_plots_points_threshold").execute(*args, **kwargs)
                def plots_behavior(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/appearance/charts/plots_behavior").execute(*args, **kwargs)
                def print_plot_data(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/appearance/charts/print_plot_data").execute(*args, **kwargs)
                def print_residuals_data(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/appearance/charts/print_residuals_data").execute(*args, **kwargs)
                def threshold(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/appearance/charts/threshold").execute(*args, **kwargs)

                class font(metaclass=PyMenuMeta):
                    """
                    .
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                    def axes(self, *args, **kwargs):
                        """
                        .
                        """
                        return PyMenu(self.service, "/preferences/appearance/charts/font/axes").execute(*args, **kwargs)
                    def axes_titles(self, *args, **kwargs):
                        """
                        .
                        """
                        return PyMenu(self.service, "/preferences/appearance/charts/font/axes_titles").execute(*args, **kwargs)
                    def legend(self, *args, **kwargs):
                        """
                        .
                        """
                        return PyMenu(self.service, "/preferences/appearance/charts/font/legend").execute(*args, **kwargs)
                    def title(self, *args, **kwargs):
                        """
                        .
                        """
                        return PyMenu(self.service, "/preferences/appearance/charts/font/title").execute(*args, **kwargs)

                class text_color(metaclass=PyMenuMeta):
                    """
                    .
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                    def axes(self, *args, **kwargs):
                        """
                        .
                        """
                        return PyMenu(self.service, "/preferences/appearance/charts/text_color/axes").execute(*args, **kwargs)
                    def axes_titles(self, *args, **kwargs):
                        """
                        .
                        """
                        return PyMenu(self.service, "/preferences/appearance/charts/text_color/axes_titles").execute(*args, **kwargs)
                    def legend(self, *args, **kwargs):
                        """
                        .
                        """
                        return PyMenu(self.service, "/preferences/appearance/charts/text_color/legend").execute(*args, **kwargs)
                    def title(self, *args, **kwargs):
                        """
                        .
                        """
                        return PyMenu(self.service, "/preferences/appearance/charts/text_color/title").execute(*args, **kwargs)

            class selections(metaclass=PyMenuMeta):
                """
                Enters the menu for controlling selections in the graphics window.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def general_displacement(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/appearance/selections/general_displacement").execute(*args, **kwargs)
                def highlight_edge_color(self, *args, **kwargs):
                    """
                    Specifies the color used to highlight edges when the Hover-Over Highlight feature is enabled (mouse-over-highlight-enabled).
                    """
                    return PyMenu(self.service, "/preferences/appearance/selections/highlight_edge_color").execute(*args, **kwargs)
                def highlight_edge_weight(self, *args, **kwargs):
                    """
                    Specifies the thickness of the edge highlights when the Hover-Over Highlight feature is enabled (mouse-over-highlight-enabled).
                    """
                    return PyMenu(self.service, "/preferences/appearance/selections/highlight_edge_weight").execute(*args, **kwargs)
                def highlight_face_color(self, *args, **kwargs):
                    """
                    Specify which color indicates that a face is selected.
                    """
                    return PyMenu(self.service, "/preferences/appearance/selections/highlight_face_color").execute(*args, **kwargs)
                def highlight_gloss(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/appearance/selections/highlight_gloss").execute(*args, **kwargs)
                def highlight_specular_component(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/appearance/selections/highlight_specular_component").execute(*args, **kwargs)
                def highlight_transparency(self, *args, **kwargs):
                    """
                    Specify the transparency of the coloring on a selected surface. 0.1 is fully opaque and 1 is fully transparent.
                    """
                    return PyMenu(self.service, "/preferences/appearance/selections/highlight_transparency").execute(*args, **kwargs)
                def mouse_hover_probe_values_enabled(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/appearance/selections/mouse_hover_probe_values_enabled").execute(*args, **kwargs)
                def mouse_over_highlight_enabled(self, *args, **kwargs):
                    """
                    Enable/disable the highlighted outline of a surface when hovered-over. Note that objects must be redisplayed after changing this setting before the new setting is visible.
                    """
                    return PyMenu(self.service, "/preferences/appearance/selections/mouse_over_highlight_enabled").execute(*args, **kwargs)
                def probe_tooltip_hide_delay_timer(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/appearance/selections/probe_tooltip_hide_delay_timer").execute(*args, **kwargs)
                def probe_tooltip_show_delay_timer(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/appearance/selections/probe_tooltip_show_delay_timer").execute(*args, **kwargs)

        class general(metaclass=PyMenuMeta):
            """
            Enter the menu for general preferences.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def advanced_partition(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/general/advanced_partition").execute(*args, **kwargs)
            def automatic_transcript(self, *args, **kwargs):
                """
                Enable/disable the automatic creation of a transcript file for each ANSYS Fluent session.
                """
                return PyMenu(self.service, "/preferences/general/automatic_transcript").execute(*args, **kwargs)
            def default_ioformat(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/general/default_ioformat").execute(*args, **kwargs)
            def dock_editor(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/general/dock_editor").execute(*args, **kwargs)
            def enable_parametric_study(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/general/enable_parametric_study").execute(*args, **kwargs)
            def flow_model(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/general/flow_model").execute(*args, **kwargs)
            def idle_timeout(self, *args, **kwargs):
                """
                Specify the default file format for saving case and data files.
                """
                return PyMenu(self.service, "/preferences/general/idle_timeout").execute(*args, **kwargs)
            def key_behavioral_changes_message(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/general/key_behavioral_changes_message").execute(*args, **kwargs)
            def qaservice_message(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/general/qaservice_message").execute(*args, **kwargs)
            def utlcreate_physics_on_mode_change(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/general/utlcreate_physics_on_mode_change").execute(*args, **kwargs)
            def utlmode(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/general/utlmode").execute(*args, **kwargs)

        class gpuapp(metaclass=PyMenuMeta):
            """
            .
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def alpha_features(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/gpuapp/alpha_features").execute(*args, **kwargs)

        class graphics(metaclass=PyMenuMeta):
            """
            Enter the menu for preferences covering appearance.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
                self.boundary_markers = self.__class__.boundary_markers(path + [("boundary_markers", None)], service)
                self.colormap_settings = self.__class__.colormap_settings(path + [("colormap_settings", None)], service)
                self.embedded_windows = self.__class__.embedded_windows(path + [("embedded_windows", None)], service)
                self.export_video_settings = self.__class__.export_video_settings(path + [("export_video_settings", None)], service)
                self.graphics_effects = self.__class__.graphics_effects(path + [("graphics_effects", None)], service)
                self.hardcopy_settings = self.__class__.hardcopy_settings(path + [("hardcopy_settings", None)], service)
                self.lighting = self.__class__.lighting(path + [("lighting", None)], service)
                self.manage_hoops_memory = self.__class__.manage_hoops_memory(path + [("manage_hoops_memory", None)], service)
                self.material_effects = self.__class__.material_effects(path + [("material_effects", None)], service)
                self.meshing_mode = self.__class__.meshing_mode(path + [("meshing_mode", None)], service)
                self.performance = self.__class__.performance(path + [("performance", None)], service)
                self.transparency = self.__class__.transparency(path + [("transparency", None)], service)
                self.vector_settings = self.__class__.vector_settings(path + [("vector_settings", None)], service)
            def animation_option(self, *args, **kwargs):
                """
                Specify whether the entire model or just a wireframe is shown during manipulations in the graphics window.
                """
                return PyMenu(self.service, "/preferences/graphics/animation_option").execute(*args, **kwargs)
            def double_buffering(self, *args, **kwargs):
                """
                Enable/disable double-buffering, which reduces screen flicker, but may use more memory on some machines.
                """
                return PyMenu(self.service, "/preferences/graphics/double_buffering").execute(*args, **kwargs)
            def enable_non_object_based_workflow(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/enable_non_object_based_workflow").execute(*args, **kwargs)
            def event_poll_interval(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/event_poll_interval").execute(*args, **kwargs)
            def event_poll_timeout(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/event_poll_timeout").execute(*args, **kwargs)
            def force_key_frame_animation_markers_to_off(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/force_key_frame_animation_markers_to_off").execute(*args, **kwargs)
            def graphics_window_line_width(self, *args, **kwargs):
                """
                Specify the thickness of lines that appear in the graphics window.
                """
                return PyMenu(self.service, "/preferences/graphics/graphics_window_line_width").execute(*args, **kwargs)
            def graphics_window_point_symbol(self, *args, **kwargs):
                """
                Specify the symbol used for indicating points in the graphics window (like the points in an XY plot).
                """
                return PyMenu(self.service, "/preferences/graphics/graphics_window_point_symbol").execute(*args, **kwargs)
            def hidden_surface_removal_method(self, *args, **kwargs):
                """
                Specify the method for removing hidden surfaces. These methods vary in speed and quality, depending on your machine.
                """
                return PyMenu(self.service, "/preferences/graphics/hidden_surface_removal_method").execute(*args, **kwargs)
            def higher_resolution_graphics_window_line_width(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/higher_resolution_graphics_window_line_width").execute(*args, **kwargs)
            def lower_resolution_graphics_window_line_width(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/lower_resolution_graphics_window_line_width").execute(*args, **kwargs)
            def marker_drawing_mode(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/marker_drawing_mode").execute(*args, **kwargs)
            def max_graphics_text_size(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/max_graphics_text_size").execute(*args, **kwargs)
            def min_graphics_text_size(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/min_graphics_text_size").execute(*args, **kwargs)
            def new_material_infra(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/new_material_infra").execute(*args, **kwargs)
            def plot_legend_margin(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/plot_legend_margin").execute(*args, **kwargs)
            def point_tool_size(self, *args, **kwargs):
                """
                Specify the size of the point tool (10-100).
                """
                return PyMenu(self.service, "/preferences/graphics/point_tool_size").execute(*args, **kwargs)
            def remove_partition_lines(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/remove_partition_lines").execute(*args, **kwargs)
            def remove_partition_lines_tolerance(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/remove_partition_lines_tolerance").execute(*args, **kwargs)
            def rotation_centerpoint_visible(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/rotation_centerpoint_visible").execute(*args, **kwargs)
            def scroll_wheel_event_end_timer(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/scroll_wheel_event_end_timer").execute(*args, **kwargs)
            def set_camera_normal_to_surface_increments(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/set_camera_normal_to_surface_increments").execute(*args, **kwargs)
            def show_hidden_lines(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/show_hidden_lines").execute(*args, **kwargs)
            def show_hidden_surfaces(self, *args, **kwargs):
                """
                Enable/disable the display of hidden surfaces.
                """
                return PyMenu(self.service, "/preferences/graphics/show_hidden_surfaces").execute(*args, **kwargs)
            def switch_to_open_glfor_remote_visualization(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/switch_to_open_glfor_remote_visualization").execute(*args, **kwargs)
            def test_use_external_function(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/test_use_external_function").execute(*args, **kwargs)
            def text_window_line_width(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/text_window_line_width").execute(*args, **kwargs)

            class boundary_markers(metaclass=PyMenuMeta):
                """
                Enter the boundary markers menu.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def color_option(self, *args, **kwargs):
                    """
                    Specify whether boundary markers are a fixed color or if they match the color of the surface they are identifying.
                    """
                    return PyMenu(self.service, "/preferences/graphics/boundary_markers/color_option").execute(*args, **kwargs)
                def enabled(self, *args, **kwargs):
                    """
                    Enable/disable boundary marker display.
                    """
                    return PyMenu(self.service, "/preferences/graphics/boundary_markers/enabled").execute(*args, **kwargs)
                def exclude_from_bounding(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/boundary_markers/exclude_from_bounding").execute(*args, **kwargs)
                def inlet_color(self, *args, **kwargs):
                    """
                    Specify the color of the inlet boundary markers.
                    """
                    return PyMenu(self.service, "/preferences/graphics/boundary_markers/inlet_color").execute(*args, **kwargs)
                def marker_fraction(self, *args, **kwargs):
                    """
                    Specify marker density factor (0.1-1).
                    """
                    return PyMenu(self.service, "/preferences/graphics/boundary_markers/marker_fraction").execute(*args, **kwargs)
                def marker_size_limiting_scale_multiplier(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/boundary_markers/marker_size_limiting_scale_multiplier").execute(*args, **kwargs)
                def markers_limit(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/boundary_markers/markers_limit").execute(*args, **kwargs)
                def outlet_color(self, *args, **kwargs):
                    """
                    Specify the color of the outlet boundary markers.
                    """
                    return PyMenu(self.service, "/preferences/graphics/boundary_markers/outlet_color").execute(*args, **kwargs)
                def scale_marker(self, *args, **kwargs):
                    """
                    Specify the scale factor for the boundary markers (0.1-10), which controls the overall size of the markers.
                    """
                    return PyMenu(self.service, "/preferences/graphics/boundary_markers/scale_marker").execute(*args, **kwargs)
                def show_inlet_markers(self, *args, **kwargs):
                    """
                    Enable/disable the display of boundary markers for inlets.
                    """
                    return PyMenu(self.service, "/preferences/graphics/boundary_markers/show_inlet_markers").execute(*args, **kwargs)
                def show_outlet_markers(self, *args, **kwargs):
                    """
                    Enable/disable the display of boundary markers for outlets.
                    """
                    return PyMenu(self.service, "/preferences/graphics/boundary_markers/show_outlet_markers").execute(*args, **kwargs)

            class colormap_settings(metaclass=PyMenuMeta):
                """
                Enter the colormap settings menu.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def alignment(self, *args, **kwargs):
                    """
                    Specify the default colormap location.
                    """
                    return PyMenu(self.service, "/preferences/graphics/colormap_settings/alignment").execute(*args, **kwargs)
                def aspect_ratio_when_horizontal(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/colormap_settings/aspect_ratio_when_horizontal").execute(*args, **kwargs)
                def aspect_ratio_when_vertical(self, *args, **kwargs):
                    """
                    Specify the length vs. width ratio for a vertical colormap, which controls the thickness of the colormap; smaller values mean a thicker colormap.
                    """
                    return PyMenu(self.service, "/preferences/graphics/colormap_settings/aspect_ratio_when_vertical").execute(*args, **kwargs)
                def auto_refit_on_resize(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/colormap_settings/auto_refit_on_resize").execute(*args, **kwargs)
                def automatic_resize(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/colormap_settings/automatic_resize").execute(*args, **kwargs)
                def border_style(self, *args, **kwargs):
                    """
                    Specify how/when the colormap border appears.
                    """
                    return PyMenu(self.service, "/preferences/graphics/colormap_settings/border_style").execute(*args, **kwargs)
                def colormap(self, *args, **kwargs):
                    """
                    Choose the default colormap.
                    """
                    return PyMenu(self.service, "/preferences/graphics/colormap_settings/colormap").execute(*args, **kwargs)
                def isolines_position_offset(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/colormap_settings/isolines_position_offset").execute(*args, **kwargs)
                def labels(self, *args, **kwargs):
                    """
                    Specify whether there is a label for every colormap value or if some are skipped.
                    """
                    return PyMenu(self.service, "/preferences/graphics/colormap_settings/labels").execute(*args, **kwargs)
                def levels(self, *args, **kwargs):
                    """
                    Specify the default colormap size.
                    """
                    return PyMenu(self.service, "/preferences/graphics/colormap_settings/levels").execute(*args, **kwargs)
                def log_scale(self, *args, **kwargs):
                    """
                    Enable/disable the use of a logarithmic scale for the colormap.
                    """
                    return PyMenu(self.service, "/preferences/graphics/colormap_settings/log_scale").execute(*args, **kwargs)
                def major_length_to_screen_ratio_when_horizontal(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/colormap_settings/major_length_to_screen_ratio_when_horizontal").execute(*args, **kwargs)
                def major_length_to_screen_ratio_when_vertical(self, *args, **kwargs):
                    """
                    Choose the length of the colormap as a fraction of graphics window height, when the colormap is vertical.
                    """
                    return PyMenu(self.service, "/preferences/graphics/colormap_settings/major_length_to_screen_ratio_when_vertical").execute(*args, **kwargs)
                def margin_from_edge_to_screen_ratio(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/colormap_settings/margin_from_edge_to_screen_ratio").execute(*args, **kwargs)
                def max_size_scale_factor(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/colormap_settings/max_size_scale_factor").execute(*args, **kwargs)
                def min_size_scale_factor(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/colormap_settings/min_size_scale_factor").execute(*args, **kwargs)
                def number_format_precision(self, *args, **kwargs):
                    """
                    Specify the colormap number label precision.
                    """
                    return PyMenu(self.service, "/preferences/graphics/colormap_settings/number_format_precision").execute(*args, **kwargs)
                def number_format_type(self, *args, **kwargs):
                    """
                    Specify how colormap numbers are displayed.
                    """
                    return PyMenu(self.service, "/preferences/graphics/colormap_settings/number_format_type").execute(*args, **kwargs)
                def show_colormap(self, *args, **kwargs):
                    """
                    Enable/disable the display of colormaps.
                    """
                    return PyMenu(self.service, "/preferences/graphics/colormap_settings/show_colormap").execute(*args, **kwargs)
                def skip_value(self, *args, **kwargs):
                    """
                    Specify how many number labels are skipped in the colormap.
                    """
                    return PyMenu(self.service, "/preferences/graphics/colormap_settings/skip_value").execute(*args, **kwargs)
                def text_behavior(self, *args, **kwargs):
                    """
                    Specify whether colormap label text automatically scales with the colormap size.
                    """
                    return PyMenu(self.service, "/preferences/graphics/colormap_settings/text_behavior").execute(*args, **kwargs)
                def text_font_automatic_horizontal_size(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/colormap_settings/text_font_automatic_horizontal_size").execute(*args, **kwargs)
                def text_font_automatic_size(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/colormap_settings/text_font_automatic_size").execute(*args, **kwargs)
                def text_font_automatic_units(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/colormap_settings/text_font_automatic_units").execute(*args, **kwargs)
                def text_font_automatic_vertical_size(self, *args, **kwargs):
                    """
                    Specify the initial font size as a ratio of the colormap overall size, for vertically aligned colormaps.
                    """
                    return PyMenu(self.service, "/preferences/graphics/colormap_settings/text_font_automatic_vertical_size").execute(*args, **kwargs)
                def text_font_fixed_horizontal_size(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/colormap_settings/text_font_fixed_horizontal_size").execute(*args, **kwargs)
                def text_font_fixed_size(self, *args, **kwargs):
                    """
                    Set the font size for colormap labels.
                    """
                    return PyMenu(self.service, "/preferences/graphics/colormap_settings/text_font_fixed_size").execute(*args, **kwargs)
                def text_font_fixed_units(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/colormap_settings/text_font_fixed_units").execute(*args, **kwargs)
                def text_font_fixed_vertical_size(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/colormap_settings/text_font_fixed_vertical_size").execute(*args, **kwargs)
                def text_font_name(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/colormap_settings/text_font_name").execute(*args, **kwargs)
                def text_truncation_limit_for_horizontal_colormaps(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/colormap_settings/text_truncation_limit_for_horizontal_colormaps").execute(*args, **kwargs)
                def text_truncation_limit_for_vertical_colormaps(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/colormap_settings/text_truncation_limit_for_vertical_colormaps").execute(*args, **kwargs)
                def type(self, *args, **kwargs):
                    """
                    Specify whether the colormap appearance is smooth or banded.
                    """
                    return PyMenu(self.service, "/preferences/graphics/colormap_settings/type").execute(*args, **kwargs)
                def use_no_sub_windows(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/colormap_settings/use_no_sub_windows").execute(*args, **kwargs)

            class embedded_windows(metaclass=PyMenuMeta):
                """
                .
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def default_embedded_mesh_windows_view(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/embedded_windows/default_embedded_mesh_windows_view").execute(*args, **kwargs)
                def default_embedded_windows_view(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/embedded_windows/default_embedded_windows_view").execute(*args, **kwargs)
                def save_embedded_window_layout(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/embedded_windows/save_embedded_window_layout").execute(*args, **kwargs)
                def show_border_for_embedded_window(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/embedded_windows/show_border_for_embedded_window").execute(*args, **kwargs)

            class export_video_settings(metaclass=PyMenuMeta):
                """
                .
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                    self.advanced_video_quality_options = self.__class__.advanced_video_quality_options(path + [("advanced_video_quality_options", None)], service)
                def video_format(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/export_video_settings/video_format").execute(*args, **kwargs)
                def video_fps(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/export_video_settings/video_fps").execute(*args, **kwargs)
                def video_quality(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/export_video_settings/video_quality").execute(*args, **kwargs)
                def video_resoution_x(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/export_video_settings/video_resoution_x").execute(*args, **kwargs)
                def video_resoution_y(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/export_video_settings/video_resoution_y").execute(*args, **kwargs)
                def video_scale(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/export_video_settings/video_scale").execute(*args, **kwargs)
                def video_smooth_scaling(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/export_video_settings/video_smooth_scaling").execute(*args, **kwargs)
                def video_use_frame_resolution(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/export_video_settings/video_use_frame_resolution").execute(*args, **kwargs)

                class advanced_video_quality_options(metaclass=PyMenuMeta):
                    """
                    .
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                    def bit_rate_quality(self, *args, **kwargs):
                        """
                        .
                        """
                        return PyMenu(self.service, "/preferences/graphics/export_video_settings/advanced_video_quality_options/bit_rate_quality").execute(*args, **kwargs)
                    def bitrate(self, *args, **kwargs):
                        """
                        .
                        """
                        return PyMenu(self.service, "/preferences/graphics/export_video_settings/advanced_video_quality_options/bitrate").execute(*args, **kwargs)
                    def compression_method(self, *args, **kwargs):
                        """
                        .
                        """
                        return PyMenu(self.service, "/preferences/graphics/export_video_settings/advanced_video_quality_options/compression_method").execute(*args, **kwargs)
                    def enable_h264(self, *args, **kwargs):
                        """
                        .
                        """
                        return PyMenu(self.service, "/preferences/graphics/export_video_settings/advanced_video_quality_options/enable_h264").execute(*args, **kwargs)
                    def key_frames(self, *args, **kwargs):
                        """
                        .
                        """
                        return PyMenu(self.service, "/preferences/graphics/export_video_settings/advanced_video_quality_options/key_frames").execute(*args, **kwargs)

            class graphics_effects(metaclass=PyMenuMeta):
                """
                Enter the graphics effects menu.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def ambient_occlusion_enabled(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/graphics_effects/ambient_occlusion_enabled").execute(*args, **kwargs)
                def ambient_occlusion_quality(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/graphics_effects/ambient_occlusion_quality").execute(*args, **kwargs)
                def ambient_occlusion_strength(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/graphics_effects/ambient_occlusion_strength").execute(*args, **kwargs)
                def anti_aliasing(self, *args, **kwargs):
                    """
                    Enable/disable the smoothing of lines and text.
                    """
                    return PyMenu(self.service, "/preferences/graphics/graphics_effects/anti_aliasing").execute(*args, **kwargs)
                def bloom_blur(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/graphics_effects/bloom_blur").execute(*args, **kwargs)
                def bloom_enabled(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/graphics_effects/bloom_enabled").execute(*args, **kwargs)
                def bloom_strength(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/graphics_effects/bloom_strength").execute(*args, **kwargs)
                def grid_color(self, *args, **kwargs):
                    """
                    Specify the color of the grid lines when the ground plane grid is shown.
                    """
                    return PyMenu(self.service, "/preferences/graphics/graphics_effects/grid_color").execute(*args, **kwargs)
                def grid_plane_count(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/graphics_effects/grid_plane_count").execute(*args, **kwargs)
                def grid_plane_enabled(self, *args, **kwargs):
                    """
                    Enable/disable the display of the ground plane grid.
                    """
                    return PyMenu(self.service, "/preferences/graphics/graphics_effects/grid_plane_enabled").execute(*args, **kwargs)
                def grid_plane_offset(self, *args, **kwargs):
                    """
                    Set the grid plane offset from the model as a percentage of the model size.
                    """
                    return PyMenu(self.service, "/preferences/graphics/graphics_effects/grid_plane_offset").execute(*args, **kwargs)
                def grid_plane_size_factor(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/graphics_effects/grid_plane_size_factor").execute(*args, **kwargs)
                def plane_direction(self, *args, **kwargs):
                    """
                    Specify the direction of the plane for the ground plane grid and reflections.
                    """
                    return PyMenu(self.service, "/preferences/graphics/graphics_effects/plane_direction").execute(*args, **kwargs)
                def reflections_enabled(self, *args, **kwargs):
                    """
                    Enable/disable model reflections (mirror-type reflections).
                    """
                    return PyMenu(self.service, "/preferences/graphics/graphics_effects/reflections_enabled").execute(*args, **kwargs)
                def shadow_map_enabled(self, *args, **kwargs):
                    """
                    Enable/disable dynamic shadows, which show shadows of geometric entities on other objects based on lighting and object orientation.
                    """
                    return PyMenu(self.service, "/preferences/graphics/graphics_effects/shadow_map_enabled").execute(*args, **kwargs)
                def show_edge_reflections(self, *args, **kwargs):
                    """
                    Enable/disable the display of model edges in reflections. Note that this can negatively affect performance.
                    """
                    return PyMenu(self.service, "/preferences/graphics/graphics_effects/show_edge_reflections").execute(*args, **kwargs)
                def show_marker_reflections(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/graphics_effects/show_marker_reflections").execute(*args, **kwargs)
                def simple_shadows_enabled(self, *args, **kwargs):
                    """
                    Enable/disable the display of static shadows on the ground plane.
                    """
                    return PyMenu(self.service, "/preferences/graphics/graphics_effects/simple_shadows_enabled").execute(*args, **kwargs)
                def update_after_mouse_release(self, *args, **kwargs):
                    """
                    Enable/disable the updating of graphics effects as a model is being manipulated in the graphics window.
                    """
                    return PyMenu(self.service, "/preferences/graphics/graphics_effects/update_after_mouse_release").execute(*args, **kwargs)

            class hardcopy_settings(metaclass=PyMenuMeta):
                """
                Enter the menu for saving picture settings.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def export_edges_for_avz(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/hardcopy_settings/export_edges_for_avz").execute(*args, **kwargs)
                def hardcopy_driver(self, *args, **kwargs):
                    """
                    Specify the default format for saving pictures.
                    """
                    return PyMenu(self.service, "/preferences/graphics/hardcopy_settings/hardcopy_driver").execute(*args, **kwargs)
                def hardcopy_line_width(self, *args, **kwargs):
                    """
                    Specify the thinkness of lines for saved pictures.
                    """
                    return PyMenu(self.service, "/preferences/graphics/hardcopy_settings/hardcopy_line_width").execute(*args, **kwargs)
                def hardware_image_accel(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/hardcopy_settings/hardware_image_accel").execute(*args, **kwargs)
                def post_script_permission_override(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/hardcopy_settings/post_script_permission_override").execute(*args, **kwargs)
                def save_embedded_hardcopies_separately(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/hardcopy_settings/save_embedded_hardcopies_separately").execute(*args, **kwargs)
                def save_embedded_windows_in_hardcopy(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/hardcopy_settings/save_embedded_windows_in_hardcopy").execute(*args, **kwargs)
                def transparent_embedded_windows(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/hardcopy_settings/transparent_embedded_windows").execute(*args, **kwargs)

            class lighting(metaclass=PyMenuMeta):
                """
                Enter the lighting menu.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def ambient_light_intensity(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/lighting/ambient_light_intensity").execute(*args, **kwargs)
                def headlight(self, *args, **kwargs):
                    """
                    Turn the headlight on or off or set it as automatic.
                    """
                    return PyMenu(self.service, "/preferences/graphics/lighting/headlight").execute(*args, **kwargs)
                def headlight_intensity(self, *args, **kwargs):
                    """
                    Specify the intensity of the headlight.
                    """
                    return PyMenu(self.service, "/preferences/graphics/lighting/headlight_intensity").execute(*args, **kwargs)
                def lighting_method(self, *args, **kwargs):
                    """
                    Specify the default lighting method.
                    """
                    return PyMenu(self.service, "/preferences/graphics/lighting/lighting_method").execute(*args, **kwargs)

            class manage_hoops_memory(metaclass=PyMenuMeta):
                """
                .
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def enabled(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/manage_hoops_memory/enabled").execute(*args, **kwargs)
                def hsfimport_limit(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/manage_hoops_memory/hsfimport_limit").execute(*args, **kwargs)

            class material_effects(metaclass=PyMenuMeta):
                """
                .
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def decimation_filter(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/material_effects/decimation_filter").execute(*args, **kwargs)
                def parameterization_source(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/material_effects/parameterization_source").execute(*args, **kwargs)
                def tiling_style(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/material_effects/tiling_style").execute(*args, **kwargs)

            class meshing_mode(metaclass=PyMenuMeta):
                """
                Enter the menu for meshing-specific graphics settings.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def graphics_window_display_timeout(self, *args, **kwargs):
                    """
                    Enable/disable graphics window display timeout.
                    """
                    return PyMenu(self.service, "/preferences/graphics/meshing_mode/graphics_window_display_timeout").execute(*args, **kwargs)
                def graphics_window_display_timeout_value(self, *args, **kwargs):
                    """
                    Specify the graphics window display timeout value.
                    """
                    return PyMenu(self.service, "/preferences/graphics/meshing_mode/graphics_window_display_timeout_value").execute(*args, **kwargs)

            class performance(metaclass=PyMenuMeta):
                """
                Enter the menu for selecting the predefined graphics effects settings.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                    self.fast_display_mode = self.__class__.fast_display_mode(path + [("fast_display_mode", None)], service)
                    self.minimum_frame_rate = self.__class__.minimum_frame_rate(path + [("minimum_frame_rate", None)], service)
                def optimize_for(self, *args, **kwargs):
                    """
                    Choose a preset selection for how graphics are displayed.
                    """
                    return PyMenu(self.service, "/preferences/graphics/performance/optimize_for").execute(*args, **kwargs)
                def ratio_of_target_frame_rate_to_classify_heavy_geometry(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/performance/ratio_of_target_frame_rate_to_classify_heavy_geometry").execute(*args, **kwargs)
                def ratio_of_target_frame_rate_to_declassify_heavy_geometry(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/performance/ratio_of_target_frame_rate_to_declassify_heavy_geometry").execute(*args, **kwargs)

                class fast_display_mode(metaclass=PyMenuMeta):
                    """
                    .
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                    def culling(self, *args, **kwargs):
                        """
                        .
                        """
                        return PyMenu(self.service, "/preferences/graphics/performance/fast_display_mode/culling").execute(*args, **kwargs)
                    def faces_shown(self, *args, **kwargs):
                        """
                        .
                        """
                        return PyMenu(self.service, "/preferences/graphics/performance/fast_display_mode/faces_shown").execute(*args, **kwargs)
                    def markers_decimation(self, *args, **kwargs):
                        """
                        .
                        """
                        return PyMenu(self.service, "/preferences/graphics/performance/fast_display_mode/markers_decimation").execute(*args, **kwargs)
                    def nodes_shown(self, *args, **kwargs):
                        """
                        .
                        """
                        return PyMenu(self.service, "/preferences/graphics/performance/fast_display_mode/nodes_shown").execute(*args, **kwargs)
                    def perimeter_edges_shown(self, *args, **kwargs):
                        """
                        .
                        """
                        return PyMenu(self.service, "/preferences/graphics/performance/fast_display_mode/perimeter_edges_shown").execute(*args, **kwargs)
                    def silhouette_shown(self, *args, **kwargs):
                        """
                        .
                        """
                        return PyMenu(self.service, "/preferences/graphics/performance/fast_display_mode/silhouette_shown").execute(*args, **kwargs)
                    def status(self, *args, **kwargs):
                        """
                        .
                        """
                        return PyMenu(self.service, "/preferences/graphics/performance/fast_display_mode/status").execute(*args, **kwargs)
                    def transparency(self, *args, **kwargs):
                        """
                        .
                        """
                        return PyMenu(self.service, "/preferences/graphics/performance/fast_display_mode/transparency").execute(*args, **kwargs)

                class minimum_frame_rate(metaclass=PyMenuMeta):
                    """
                    Enter the menu for minimum frame-rate settings.
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                    def dynamic_adjustment(self, *args, **kwargs):
                        """
                        Enable/disable dynamic adjustment of quality loss per frame to get to the desired frame rate.
                        """
                        return PyMenu(self.service, "/preferences/graphics/performance/minimum_frame_rate/dynamic_adjustment").execute(*args, **kwargs)
                    def enabled(self, *args, **kwargs):
                        """
                        Enable/disable minimum frame rate.
                        """
                        return PyMenu(self.service, "/preferences/graphics/performance/minimum_frame_rate/enabled").execute(*args, **kwargs)
                    def fixed_culling_value(self, *args, **kwargs):
                        """
                        .
                        """
                        return PyMenu(self.service, "/preferences/graphics/performance/minimum_frame_rate/fixed_culling_value").execute(*args, **kwargs)
                    def maximum_culling_threshold(self, *args, **kwargs):
                        """
                        With minimum frame rate enabled, Fluent will not cull beyond this number of pixels.
                        """
                        return PyMenu(self.service, "/preferences/graphics/performance/minimum_frame_rate/maximum_culling_threshold").execute(*args, **kwargs)
                    def minimum_culling_threshold(self, *args, **kwargs):
                        """
                        With minimum frame rate enabled, Fluent will cull at least this number of pixels.
                        """
                        return PyMenu(self.service, "/preferences/graphics/performance/minimum_frame_rate/minimum_culling_threshold").execute(*args, **kwargs)
                    def target_fps(self, *args, **kwargs):
                        """
                        Specify the target frames-per-second.
                        """
                        return PyMenu(self.service, "/preferences/graphics/performance/minimum_frame_rate/target_fps").execute(*args, **kwargs)

            class transparency(metaclass=PyMenuMeta):
                """
                .
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def algorithm_for_modern_drivers(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/transparency/algorithm_for_modern_drivers").execute(*args, **kwargs)
                def depth_peeling_layers(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/transparency/depth_peeling_layers").execute(*args, **kwargs)
                def depth_peeling_preference(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/transparency/depth_peeling_preference").execute(*args, **kwargs)
                def quick_moves(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/transparency/quick_moves").execute(*args, **kwargs)
                def zsort_options(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/transparency/zsort_options").execute(*args, **kwargs)

            class vector_settings(metaclass=PyMenuMeta):
                """
                .
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def arrow3_dradius1_factor(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/vector_settings/arrow3_dradius1_factor").execute(*args, **kwargs)
                def arrow3_dradius2_factor(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/vector_settings/arrow3_dradius2_factor").execute(*args, **kwargs)
                def arrowhead3_dradius1_factor(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/vector_settings/arrowhead3_dradius1_factor").execute(*args, **kwargs)
                def line_arrow3_dperpendicular_radius(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/vector_settings/line_arrow3_dperpendicular_radius").execute(*args, **kwargs)

        class mat_pro_app(metaclass=PyMenuMeta):
            """
            .
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def beta_features(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/mat_pro_app/beta_features").execute(*args, **kwargs)
            def focus(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/mat_pro_app/focus").execute(*args, **kwargs)
            def warning(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/mat_pro_app/warning").execute(*args, **kwargs)

        class meshing_workflow(metaclass=PyMenuMeta):
            """
            Enter the menu for preferences covering the Fluent Meshing workflows.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
                self.draw_settings = self.__class__.draw_settings(path + [("draw_settings", None)], service)
            def checkpointing_option(self, *args, **kwargs):
                """
                Specify how Fluent Meshing will save data when you edit a task.
                """
                return PyMenu(self.service, "/preferences/meshing_workflow/checkpointing_option").execute(*args, **kwargs)
            def save_checkpoint_files(self, *args, **kwargs):
                """
                Enable/disable the saving of task editing data when writing a mesh file.
                """
                return PyMenu(self.service, "/preferences/meshing_workflow/save_checkpoint_files").execute(*args, **kwargs)
            def temp_folder(self, *args, **kwargs):
                """
                Specify a temporary location to hold generated mesh files. If nothing is specified, Fluent Meshing will write to percentageTEMPpercentage on Windows and to  /tmp on Linux.
                """
                return PyMenu(self.service, "/preferences/meshing_workflow/temp_folder").execute(*args, **kwargs)
            def templates_folder(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/meshing_workflow/templates_folder").execute(*args, **kwargs)
            def verbosity(self, *args, **kwargs):
                """
                Enable/disable the printing of additional information and messages in the Console.
                """
                return PyMenu(self.service, "/preferences/meshing_workflow/verbosity").execute(*args, **kwargs)

            class draw_settings(metaclass=PyMenuMeta):
                """
                Enter the menu for specifying drawing settings.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def auto_draw(self, *args, **kwargs):
                    """
                    Enable/disable the automatic display of changes in the graphics window based on the current task.
                    """
                    return PyMenu(self.service, "/preferences/meshing_workflow/draw_settings/auto_draw").execute(*args, **kwargs)
                def face_zone_limit(self, *args, **kwargs):
                    """
                    Specify the cutoff number of face zones, beyond which, Fluent Meshing will not automatically display changes.
                    """
                    return PyMenu(self.service, "/preferences/meshing_workflow/draw_settings/face_zone_limit").execute(*args, **kwargs)
                def facet_limit(self, *args, **kwargs):
                    """
                    Specify the cutoff number facets, beyond which, Fluent Meshing will not automatically display changes.
                    """
                    return PyMenu(self.service, "/preferences/meshing_workflow/draw_settings/facet_limit").execute(*args, **kwargs)

        class navigation(metaclass=PyMenuMeta):
            """
            Enter the menu for controlling navigation in ANSYS Fluent.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
                self.mouse_mapping = self.__class__.mouse_mapping(path + [("mouse_mapping", None)], service)

            class mouse_mapping(metaclass=PyMenuMeta):
                """
                Enable/disable the printing of additional information and messages in the Console.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                    self.additional = self.__class__.additional(path + [("additional", None)], service)
                    self.basic = self.__class__.basic(path + [("basic", None)], service)
                def mousemaptheme(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/navigation/mouse_mapping/mousemaptheme").execute(*args, **kwargs)

                class additional(metaclass=PyMenuMeta):
                    """
                    Enter the menu for controlling mouse mappings that include a modifier button such as Ctrl and Shift.
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                    def ctrllmbclick(self, *args, **kwargs):
                        """
                        Specify the action/behavoir for Ctrl + left-mouse-button + click.
                        """
                        return PyMenu(self.service, "/preferences/navigation/mouse_mapping/additional/ctrllmbclick").execute(*args, **kwargs)
                    def ctrllmbdrag(self, *args, **kwargs):
                        """
                        Specify the action/behavior for Ctrl + left-mouse-button + drag.
                        """
                        return PyMenu(self.service, "/preferences/navigation/mouse_mapping/additional/ctrllmbdrag").execute(*args, **kwargs)
                    def ctrlmmbclick(self, *args, **kwargs):
                        """
                        Specify the action/behavior for Ctrl + middle-mouse-button + click.
                        """
                        return PyMenu(self.service, "/preferences/navigation/mouse_mapping/additional/ctrlmmbclick").execute(*args, **kwargs)
                    def ctrlmmbdrag(self, *args, **kwargs):
                        """
                        Specify the action/behavior for Ctrl + middle-mouse-button + drag.
                        """
                        return PyMenu(self.service, "/preferences/navigation/mouse_mapping/additional/ctrlmmbdrag").execute(*args, **kwargs)
                    def ctrlrmbclick(self, *args, **kwargs):
                        """
                        Specify the action/behavior for Ctrl + right-mouse-button + click.
                        """
                        return PyMenu(self.service, "/preferences/navigation/mouse_mapping/additional/ctrlrmbclick").execute(*args, **kwargs)
                    def ctrlrmbdrag(self, *args, **kwargs):
                        """
                        Specify the action/behavior for Ctrl + right-mouse-button + drag.
                        """
                        return PyMenu(self.service, "/preferences/navigation/mouse_mapping/additional/ctrlrmbdrag").execute(*args, **kwargs)
                    def mouseprobe(self, *args, **kwargs):
                        """
                        Specify whether the probe action provides a long description or a short description.
                        """
                        return PyMenu(self.service, "/preferences/navigation/mouse_mapping/additional/mouseprobe").execute(*args, **kwargs)
                    def mousewheel(self, *args, **kwargs):
                        """
                        Specify the action/behavior of the mouse-wheel.
                        """
                        return PyMenu(self.service, "/preferences/navigation/mouse_mapping/additional/mousewheel").execute(*args, **kwargs)
                    def mousewheelsensitivity(self, *args, **kwargs):
                        """
                        Specify the sensitivity of the mouse-wheel (0 is least sensitive, 1 is most sensitive).
                        """
                        return PyMenu(self.service, "/preferences/navigation/mouse_mapping/additional/mousewheelsensitivity").execute(*args, **kwargs)
                    def reversewheeldirection(self, *args, **kwargs):
                        """
                        Reverse the behavior of the mouse-wheel.
                        """
                        return PyMenu(self.service, "/preferences/navigation/mouse_mapping/additional/reversewheeldirection").execute(*args, **kwargs)
                    def shiftlmbclick(self, *args, **kwargs):
                        """
                        Specify the action/behavior for Shift + left-mouse-button + click.
                        """
                        return PyMenu(self.service, "/preferences/navigation/mouse_mapping/additional/shiftlmbclick").execute(*args, **kwargs)
                    def shiftlmbdrag(self, *args, **kwargs):
                        """
                        Specify the action/behavior for Shift + left-mouse-button + drag.
                        """
                        return PyMenu(self.service, "/preferences/navigation/mouse_mapping/additional/shiftlmbdrag").execute(*args, **kwargs)
                    def shiftmmbclick(self, *args, **kwargs):
                        """
                        Specify the action/behavior for Shift + middle-mouse-button + click.
                        """
                        return PyMenu(self.service, "/preferences/navigation/mouse_mapping/additional/shiftmmbclick").execute(*args, **kwargs)
                    def shiftmmbdrag(self, *args, **kwargs):
                        """
                        Specify the action/behavior for Shift + middle-mouse-button + drag.
                        """
                        return PyMenu(self.service, "/preferences/navigation/mouse_mapping/additional/shiftmmbdrag").execute(*args, **kwargs)
                    def shiftrmbclick(self, *args, **kwargs):
                        """
                        Specify the action/behavior for Shift + right-mouse-button + click.
                        """
                        return PyMenu(self.service, "/preferences/navigation/mouse_mapping/additional/shiftrmbclick").execute(*args, **kwargs)
                    def shiftrmbdrag(self, *args, **kwargs):
                        """
                        Specify the action/behavior for Shift + right-mouse-button + drag.
                        """
                        return PyMenu(self.service, "/preferences/navigation/mouse_mapping/additional/shiftrmbdrag").execute(*args, **kwargs)

                class basic(metaclass=PyMenuMeta):
                    """
                    .
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                    def lmb(self, *args, **kwargs):
                        """
                        .
                        """
                        return PyMenu(self.service, "/preferences/navigation/mouse_mapping/basic/lmb").execute(*args, **kwargs)
                    def lmbclick(self, *args, **kwargs):
                        """
                        .
                        """
                        return PyMenu(self.service, "/preferences/navigation/mouse_mapping/basic/lmbclick").execute(*args, **kwargs)
                    def mmb(self, *args, **kwargs):
                        """
                        .
                        """
                        return PyMenu(self.service, "/preferences/navigation/mouse_mapping/basic/mmb").execute(*args, **kwargs)
                    def mmbclick(self, *args, **kwargs):
                        """
                        .
                        """
                        return PyMenu(self.service, "/preferences/navigation/mouse_mapping/basic/mmbclick").execute(*args, **kwargs)
                    def rmb(self, *args, **kwargs):
                        """
                        .
                        """
                        return PyMenu(self.service, "/preferences/navigation/mouse_mapping/basic/rmb").execute(*args, **kwargs)
                    def rmbclick(self, *args, **kwargs):
                        """
                        .
                        """
                        return PyMenu(self.service, "/preferences/navigation/mouse_mapping/basic/rmbclick").execute(*args, **kwargs)

        class prj_app(metaclass=PyMenuMeta):
            """
            .
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def advanced_flag(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/prj_app/advanced_flag").execute(*args, **kwargs)
            def beta_flag(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/prj_app/beta_flag").execute(*args, **kwargs)
            def cffoutput(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/prj_app/cffoutput").execute(*args, **kwargs)
            def default_folder(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/prj_app/default_folder").execute(*args, **kwargs)
            def display_mesh_after_case_load(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/prj_app/display_mesh_after_case_load").execute(*args, **kwargs)
            def multi_console(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/prj_app/multi_console").execute(*args, **kwargs)
            def ncpu(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/prj_app/ncpu").execute(*args, **kwargs)
            def session_color(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/prj_app/session_color").execute(*args, **kwargs)
            def show_fluent_window(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/prj_app/show_fluent_window").execute(*args, **kwargs)
            def use_default_folder(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/prj_app/use_default_folder").execute(*args, **kwargs)
            def use_fluent_graphics(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/prj_app/use_fluent_graphics").execute(*args, **kwargs)
            def use_launcher(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/prj_app/use_launcher").execute(*args, **kwargs)

        class simulation(metaclass=PyMenuMeta):
            """
            .
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
                self.report_definitions = self.__class__.report_definitions(path + [("report_definitions", None)], service)
            def flow_model(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/simulation/flow_model").execute(*args, **kwargs)
            def local_residual_scaling(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/simulation/local_residual_scaling").execute(*args, **kwargs)

            class report_definitions(metaclass=PyMenuMeta):
                """
                Enter the menu for report definition preferences.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def automatic_plot_file(self, *args, **kwargs):
                    """
                    New report definitions will automatically create associated report files and plots.
                    """
                    return PyMenu(self.service, "/preferences/simulation/report_definitions/automatic_plot_file").execute(*args, **kwargs)
                def report_plot_history_data_size(self, *args, **kwargs):
                    """
                    Specify how many data points are read from the associated report file and plotted in the graphics window. If the case/data files are already open, read the case and data again, after changing this setting, and re-plot to see the updated report plot.
                    """
                    return PyMenu(self.service, "/preferences/simulation/report_definitions/report_plot_history_data_size").execute(*args, **kwargs)

        class turbo_workflow(metaclass=PyMenuMeta):
            """
            .
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
                self.cell_zone_settings = self.__class__.cell_zone_settings(path + [("cell_zone_settings", None)], service)
                self.face_zone_settings = self.__class__.face_zone_settings(path + [("face_zone_settings", None)], service)
                self.graphics_settings = self.__class__.graphics_settings(path + [("graphics_settings", None)], service)
            def checkpointing_option(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/turbo_workflow/checkpointing_option").execute(*args, **kwargs)
            def save_checkpoint_files(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/turbo_workflow/save_checkpoint_files").execute(*args, **kwargs)

            class cell_zone_settings(metaclass=PyMenuMeta):
                """
                .
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def czsearch_order(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/turbo_workflow/cell_zone_settings/czsearch_order").execute(*args, **kwargs)
                def rotating(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/turbo_workflow/cell_zone_settings/rotating").execute(*args, **kwargs)
                def stationary(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/turbo_workflow/cell_zone_settings/stationary").execute(*args, **kwargs)

            class face_zone_settings(metaclass=PyMenuMeta):
                """
                .
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def blade_region(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/turbo_workflow/face_zone_settings/blade_region").execute(*args, **kwargs)
                def fzsearch_order(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/turbo_workflow/face_zone_settings/fzsearch_order").execute(*args, **kwargs)
                def hub_region(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/turbo_workflow/face_zone_settings/hub_region").execute(*args, **kwargs)
                def inlet_region(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/turbo_workflow/face_zone_settings/inlet_region").execute(*args, **kwargs)
                def interior_region(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/turbo_workflow/face_zone_settings/interior_region").execute(*args, **kwargs)
                def outlet_region(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/turbo_workflow/face_zone_settings/outlet_region").execute(*args, **kwargs)
                def periodic1_region(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/turbo_workflow/face_zone_settings/periodic1_region").execute(*args, **kwargs)
                def periodic2_region(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/turbo_workflow/face_zone_settings/periodic2_region").execute(*args, **kwargs)
                def shroud_region(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/turbo_workflow/face_zone_settings/shroud_region").execute(*args, **kwargs)
                def symmetry_region(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/turbo_workflow/face_zone_settings/symmetry_region").execute(*args, **kwargs)
                def tip1_region(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/turbo_workflow/face_zone_settings/tip1_region").execute(*args, **kwargs)
                def tip2_region(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/turbo_workflow/face_zone_settings/tip2_region").execute(*args, **kwargs)

            class graphics_settings(metaclass=PyMenuMeta):
                """
                .
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def auto_draw(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/turbo_workflow/graphics_settings/auto_draw").execute(*args, **kwargs)

    class size_functions(metaclass=PyMenuMeta):
        """
        Manage advanced size functions.
        """
        def __init__(self, path, service):
            self.path = path
            self.service = service
            self.contours = self.__class__.contours(path + [("contours", None)], service)
            self.controls = self.__class__.controls(path + [("controls", None)], service)
        def create(self, *args, **kwargs):
            """
            Defines the size function based on the specified parameters. 
            """
            return PyMenu(self.service, "/size_functions/create").execute(*args, **kwargs)
        def delete(self, *args, **kwargs):
            """
            Deletes the specified size function or the current size field. 
            """
            return PyMenu(self.service, "/size_functions/delete").execute(*args, **kwargs)
        def delete_all(self, *args, **kwargs):
            """
            Deletes all the defined size functions. 
            """
            return PyMenu(self.service, "/size_functions/delete_all").execute(*args, **kwargs)
        def compute(self, *args, **kwargs):
            """
            Computes the size function based on the defined parameters.
            """
            return PyMenu(self.service, "/size_functions/compute").execute(*args, **kwargs)
        def list(self, *args, **kwargs):
            """
            Lists all the defined size functions and the corresponding parameter values defined. 
            """
            return PyMenu(self.service, "/size_functions/list").execute(*args, **kwargs)
        def create_defaults(self, *args, **kwargs):
            """
            Creates default size functions based on face and edge curvature and proximity.
            """
            return PyMenu(self.service, "/size_functions/create_defaults").execute(*args, **kwargs)
        def set_global_controls(self, *args, **kwargs):
            """
            Sets the values for the global minimum and maximum size, and the growth rate.   If you set the global minimum size to a value greater than the local minimum size defined for existing proximity, curvature, or hard size functions, a warning will appear, indicating that the global minimum size cannot be greater than the specified local minimum size. 
            """
            return PyMenu(self.service, "/size_functions/set_global_controls").execute(*args, **kwargs)
        def enable_periodicity_filter(self, *args, **kwargs):
            """
            Applies periodicity to the size field.  Specify the angle, pivot, and axis of rotation to set up periodicity.  If periodicity has been previously defined, the existing settings will be applied.  Only rotational periodicity is supported, translational periodicity is not supported currently.
            """
            return PyMenu(self.service, "/size_functions/enable_periodicity_filter").execute(*args, **kwargs)
        def disable_periodicity_filter(self, *args, **kwargs):
            """
            Removes periodicity from the size field.
            """
            return PyMenu(self.service, "/size_functions/disable_periodicity_filter").execute(*args, **kwargs)
        def list_periodicity_filter(self, *args, **kwargs):
            """
            List periodic in size field.
            """
            return PyMenu(self.service, "/size_functions/list_periodicity_filter").execute(*args, **kwargs)
        def set_scaling_filter(self, *args, **kwargs):
            """
            Allows you specify the scale factor, and minimum and maximum size values to filter the size output from the size field. 
            """
            return PyMenu(self.service, "/size_functions/set_scaling_filter").execute(*args, **kwargs)
        def reset_global_controls(self, *args, **kwargs):
            """
            Resets the global controls to their default values. 
            """
            return PyMenu(self.service, "/size_functions/reset_global_controls").execute(*args, **kwargs)
        def set_prox_gap_tolerance(self, *args, **kwargs):
            """
            Sets the tolerance relative to minimum size to take gaps into account. Gaps whose thickness is less than the global minimum size multiplied by this factor will not be regarded as a proximity gap.
            """
            return PyMenu(self.service, "/size_functions/set_prox_gap_tolerance").execute(*args, **kwargs)
        def triangulate_quad_faces(self, *args, **kwargs):
            """
            Identifies the zones comprising non-triangular elements and uses a triangulated copy of these zones for computing the size functions.
            """
            return PyMenu(self.service, "/size_functions/triangulate_quad_faces").execute(*args, **kwargs)
        def use_cad_imported_curvature(self, *args, **kwargs):
            """
            Allows you to disable curvature data from the nodes of the CAD facets.
            """
            return PyMenu(self.service, "/size_functions/use_cad_imported_curvature").execute(*args, **kwargs)

        class contours(metaclass=PyMenuMeta):
            """
            Contains options for managing contours.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
                self.set = self.__class__.set(path + [("set", None)], service)
            def draw(self, *args, **kwargs):
                """
                Displays contours in the graphics window. Run compute prior to contours/draw.
                """
                return PyMenu(self.service, "/size_functions/contours/draw").execute(*args, **kwargs)

            class set(metaclass=PyMenuMeta):
                """
                Contains options to manage the contour size.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def refine_facets(self, *args, **kwargs):
                    """
                    Allows you to specify smaller facets if the original are too large. Default is no.
                    """
                    return PyMenu(self.service, "/size_functions/contours/set/refine_facets").execute(*args, **kwargs)

        class controls(metaclass=PyMenuMeta):
            """
            Menu to control different behavior of sf.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def meshed_sf_behavior(self, *args, **kwargs):
                """
                Set meshed size function processing to hard.
                """
                return PyMenu(self.service, "/size_functions/controls/meshed_sf_behavior").execute(*args, **kwargs)
            def curvature_method(self, *args, **kwargs):
                """
                Option to get facet curvature.
                """
                return PyMenu(self.service, "/size_functions/controls/curvature_method").execute(*args, **kwargs)

    class scoped_sizing(metaclass=PyMenuMeta):
        """
        Manage scoped sizing.
        """
        def __init__(self, path, service):
            self.path = path
            self.service = service
        def create(self, *args, **kwargs):
            """
            Defines the scoped size based on the specified parameters.
            """
            return PyMenu(self.service, "/scoped_sizing/create").execute(*args, **kwargs)
        def modify(self, *args, **kwargs):
            """
            Modifies the scoped size control definition.
            """
            return PyMenu(self.service, "/scoped_sizing/modify").execute(*args, **kwargs)
        def delete(self, *args, **kwargs):
            """
            Deletes the specified scoped size controls.
            """
            return PyMenu(self.service, "/scoped_sizing/delete").execute(*args, **kwargs)
        def delete_all(self, *args, **kwargs):
            """
            Deletes all the defined scoped size controls.
            """
            return PyMenu(self.service, "/scoped_sizing/delete_all").execute(*args, **kwargs)
        def compute(self, *args, **kwargs):
            """
            Computes the size field based on the defined size functions and/or scoped size controls.
            """
            return PyMenu(self.service, "/scoped_sizing/compute").execute(*args, **kwargs)
        def list(self, *args, **kwargs):
            """
            Lists all the defined scoped size controls and the corresponding parameter values defined.
            """
            return PyMenu(self.service, "/scoped_sizing/list").execute(*args, **kwargs)
        def list_zones_uncovered_by_controls(self, *args, **kwargs):
            """
            Lists the zones for which no scoped sizing controls have been defined.
            """
            return PyMenu(self.service, "/scoped_sizing/list_zones_uncovered_by_controls").execute(*args, **kwargs)
        def delete_size_field(self, *args, **kwargs):
            """
            Deletes the current size field.
            """
            return PyMenu(self.service, "/scoped_sizing/delete_size_field").execute(*args, **kwargs)
        def read(self, *args, **kwargs):
            """
            Enables you to read in a scoped sizing file (*.szcontrol).
            """
            return PyMenu(self.service, "/scoped_sizing/read").execute(*args, **kwargs)
        def write(self, *args, **kwargs):
            """
            Enables you to write a scoped sizing file (*.szcontrol).
            """
            return PyMenu(self.service, "/scoped_sizing/write").execute(*args, **kwargs)
        def validate(self, *args, **kwargs):
            """
            Validates the scoped sizing controls defined. An error will be reported if the scoped sizing controls do not exist or the scope for one (or more) controls is invalid.
            """
            return PyMenu(self.service, "/scoped_sizing/validate").execute(*args, **kwargs)

    class objects(metaclass=PyMenuMeta):
        """
        Manage objects.
        """
        def __init__(self, path, service):
            self.path = path
            self.service = service
            self.cad_association = self.__class__.cad_association(path + [("cad_association", None)], service)
            self.set = self.__class__.set(path + [("set", None)], service)
            self.deprecated = self.__class__.deprecated(path + [("deprecated", None)], service)
            self.wrap = self.__class__.wrap(path + [("wrap", None)], service)
            self.remove_gaps = self.__class__.remove_gaps(path + [("remove_gaps", None)], service)
            self.join_intersect = self.__class__.join_intersect(path + [("join_intersect", None)], service)
            self.fix_holes = self.__class__.fix_holes(path + [("fix_holes", None)], service)
            self.create_new_mesh_object = self.__class__.create_new_mesh_object(path + [("create_new_mesh_object", None)], service)
            self.labels = self.__class__.labels(path + [("labels", None)], service)
            self.volumetric_regions = self.__class__.volumetric_regions(path + [("volumetric_regions", None)], service)
        def create(self, *args, **kwargs):
            """
            Creates the object based on the priority, cell zone type, face zone(s), edge zone(s), and object type specified. You can specify the object name or retain the default blank entry to have the object name generated automatically. 
            """
            return PyMenu(self.service, "/objects/create").execute(*args, **kwargs)
        def create_multiple(self, *args, **kwargs):
            """
            Creates multiple objects by creating an object per face zone specified. The objects will be named automatically based on the prefix and priority specified. 
            """
            return PyMenu(self.service, "/objects/create_multiple").execute(*args, **kwargs)
        def delete(self, *args, **kwargs):
            """
            Deletes the specified object(s). 
            """
            return PyMenu(self.service, "/objects/delete").execute(*args, **kwargs)
        def delete_all(self, *args, **kwargs):
            """
            Deletes all the defined objects. 
            """
            return PyMenu(self.service, "/objects/delete_all").execute(*args, **kwargs)
        def delete_all_geom(self, *args, **kwargs):
            """
            Deletes all the defined geom objects. 
            """
            return PyMenu(self.service, "/objects/delete_all_geom").execute(*args, **kwargs)
        def merge(self, *args, **kwargs):
            """
            Merges the specified objects into a single object. 
            """
            return PyMenu(self.service, "/objects/merge").execute(*args, **kwargs)
        def list(self, *args, **kwargs):
            """
            Lists details such as cell zone type, priority, object type, comprising face and edge zones, and object reference point for all the defined objects.
            """
            return PyMenu(self.service, "/objects/list").execute(*args, **kwargs)
        def extract_edges(self, *args, **kwargs):
            """
            Extracts the edge zone(s) from the face zone(s) included in the specified object(s), based on the edge-feature-angle value specified (/objects/set/set-edge-feature-angle).
            """
            return PyMenu(self.service, "/objects/extract_edges").execute(*args, **kwargs)
        def update(self, *args, **kwargs):
            """
            Allows you to update the objects defined when the face and/or edge zone(s) comprising the object have been deleted. 
            """
            return PyMenu(self.service, "/objects/update").execute(*args, **kwargs)
        def merge_walls(self, *args, **kwargs):
            """
            Merges all the face zones of type wall in an object into a single face zone.
            """
            return PyMenu(self.service, "/objects/merge_walls").execute(*args, **kwargs)
        def merge_edges(self, *args, **kwargs):
            """
            Merges all the edge zones in an object into a single edge zone.  If the object is composed of edge zones of different types (boundary and interior), the edge zones of the same type (boundary or interior) will be merged into a single edge zone.
            """
            return PyMenu(self.service, "/objects/merge_edges").execute(*args, **kwargs)
        def separate_faces_by_angle(self, *args, **kwargs):
            """
            Separates the face zone(s) comprising the object based on the angle specified.
            """
            return PyMenu(self.service, "/objects/separate_faces_by_angle").execute(*args, **kwargs)
        def separate_faces_by_seed(self, *args, **kwargs):
            """
            Separates the face zone(s) comprising the object based on the seed face specified.
            """
            return PyMenu(self.service, "/objects/separate_faces_by_seed").execute(*args, **kwargs)
        def create_and_activate_domain(self, *args, **kwargs):
            """
            Creates and activates the domain comprising the face zone(s) from the object(s) specified.
            """
            return PyMenu(self.service, "/objects/create_and_activate_domain").execute(*args, **kwargs)
        def create_groups(self, *args, **kwargs):
            """
            Creates a face group and an edge group comprising the face zone(s) and edge zone(s) included in the specified object(s), respectively.
            """
            return PyMenu(self.service, "/objects/create_groups").execute(*args, **kwargs)
        def delete_unreferenced_faces_and_edges(self, *args, **kwargs):
            """
            Deletes all the faces and edges that are not included in any defined objects. 
            """
            return PyMenu(self.service, "/objects/delete_unreferenced_faces_and_edges").execute(*args, **kwargs)
        def improve_object_quality(self, *args, **kwargs):
            """
            Enables you to improve the surface mesh quality for mesh objects. Select the mesh objects and the method for improving the surface mesh. The smooth-and-improve method improves the mesh by a combination of smoothing, swapping, and surface mesh improvement operations. Object normals are correctly oriented and island faces are also deleted. You can optionally coarsen the surface mesh by specifying a suitable coarsening factor. Additional imprinting operations can be done to improve feature capture on the surface mesh. The surface-remesh method improves the mesh by remeshing based on the current size field. Object normals are correctly oriented and island faces are also deleted.
            """
            return PyMenu(self.service, "/objects/improve_object_quality").execute(*args, **kwargs)
        def merge_voids(self, *args, **kwargs):
            """
            Allows you to merge voids in the mesh object after the sewing operation.
            """
            return PyMenu(self.service, "/objects/merge_voids").execute(*args, **kwargs)
        def create_intersection_loops(self, *args, **kwargs):
            """
            Allows you to create intersection loops for objects.
            """
            return PyMenu(self.service, "/objects/create_intersection_loops").execute(*args, **kwargs)
        def change_object_type(self, *args, **kwargs):
            """
            Allows you to change the object type (geom, or mesh).
            """
            return PyMenu(self.service, "/objects/change_object_type").execute(*args, **kwargs)
        def improve_feature_capture(self, *args, **kwargs):
            """
            Enables you to imprint the edges comprising the object on to the object face zones to improve feature capture for mesh objects. You can specify the number of imprinting iterations to be performed.  The geometry objects used to create the mesh objects should be available when the improve-feature-capture command is invoked. Additionally, the face zones comprising the objects should be of type other than geometry.
            """
            return PyMenu(self.service, "/objects/improve_feature_capture").execute(*args, **kwargs)
        def sew(self, *args, **kwargs):
            """
            Contains options related to the object sewing operation. This menu is no longer supported, and will be removed in a future release.
            """
            return PyMenu(self.service, "/objects/sew").execute(*args, **kwargs)
        def merge_nodes(self, *args, **kwargs):
            """
            Merges the free nodes at the object level based on the specified tolerance or using a tolerance that is a specified percentage of shortest connected edge length.
            """
            return PyMenu(self.service, "/objects/merge_nodes").execute(*args, **kwargs)
        def translate(self, *args, **kwargs):
            """
            Translates the object(s) based on the translation offsets specified.
            """
            return PyMenu(self.service, "/objects/translate").execute(*args, **kwargs)
        def rotate(self, *args, **kwargs):
            """
            Rotates the object(s) based on the angle of rotation, pivot point, and axis of rotation specified.
            """
            return PyMenu(self.service, "/objects/rotate").execute(*args, **kwargs)
        def scale(self, *args, **kwargs):
            """
            Scales the object(s) based on the scale factors specified.
            """
            return PyMenu(self.service, "/objects/scale").execute(*args, **kwargs)
        def rename_object_zones(self, *args, **kwargs):
            """
            Renames the face and edge zones comprising the object based on the object name. You can also specify the separator to be used.
            """
            return PyMenu(self.service, "/objects/rename_object_zones").execute(*args, **kwargs)
        def rename_object(self, *args, **kwargs):
            """
            Allows you to rename a specified geometry or mesh object with another specified name.
            """
            return PyMenu(self.service, "/objects/rename_object").execute(*args, **kwargs)
        def check_mesh(self, *args, **kwargs):
            """
            Checks the mesh on the specified objects for connectivity and orientation of faces. The domain extents, volume statistics, and face area statistics will be reported along with the results of other checks on the mesh.
            """
            return PyMenu(self.service, "/objects/check_mesh").execute(*args, **kwargs)
        def rename_cell_zone_boundaries_using_labels(self, *args, **kwargs):
            """
            Renames the boundaries of the cell zones based on the existing face zone labels. This allows for the cell zone boundaries in solution mode to have names corresponding to the face zone labels in meshing mode.   This command will not work if you read in a volume mesh generated in a version prior to release 16.2. In such cases, regenerate the volume mesh before using the command.
            """
            return PyMenu(self.service, "/objects/rename_cell_zone_boundaries_using_labels").execute(*args, **kwargs)
        def summary(self, *args, **kwargs):
            """
            Allows you to obtain a summary of a specified geometry or mesh object, or obtain a summary of all geometry or mesh objects.
            """
            return PyMenu(self.service, "/objects/summary").execute(*args, **kwargs)
        def restore_faces(self, *args, **kwargs):
            """
            Restores the mesh object surface mesh from the backup created. The current mesh object face zones and cell zones will be deleted.  If the object backup is disabled (/mesh/auto-mesh-controls/backup-object no), you will not be able to restore the surface mesh using this command.  There may be a difference in the initial volume mesh generated for an object and that generated after restoring the object surface mesh due to differences in the order of zones/entities processed during volume meshing. 
            """
            return PyMenu(self.service, "/objects/restore_faces").execute(*args, **kwargs)
        def clear_backup(self, *args, **kwargs):
            """
            Clear backup data of objects.
            """
            return PyMenu(self.service, "/objects/clear_backup").execute(*args, **kwargs)
        def change_prefix(self, *args, **kwargs):
            """
            Change the prefix for specified objects.
            """
            return PyMenu(self.service, "/objects/change_prefix").execute(*args, **kwargs)
        def change_suffix(self, *args, **kwargs):
            """
            Change the suffix for specified objects.
            """
            return PyMenu(self.service, "/objects/change_suffix").execute(*args, **kwargs)

        class cad_association(metaclass=PyMenuMeta):
            """
            Contains options for modifying the selected objects based on the associated CAD entities and attaching/detaching the CAD entities from the objects. This menu is available when the CAD Assemblies tree is created during CAD import.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def attach_cad(self, *args, **kwargs):
                """
                Attaches CAD entities to the selected geometry/mesh objects. Select the geometry/mesh objects and specify the path for the CAD entities to be associated with the objects. The selected geometry/mesh objects will be associated with the CAD entities which will then be locked.
                """
                return PyMenu(self.service, "/objects/cad_association/attach_cad").execute(*args, **kwargs)
            def update_all_objects(self, *args, **kwargs):
                """
                Updates all geometry/mesh objects based on changes to the associated CAD objects. Specify the type of objects (geom or mesh) to be updated.
                """
                return PyMenu(self.service, "/objects/cad_association/update_all_objects").execute(*args, **kwargs)
            def detach_all_objects(self, *args, **kwargs):
                """
                Detaches all the CAD objects associated with the geometry/mesh objects. Specify the type of objects (geom or mesh) to be detached. All association will be removed and the geometry/mesh objects will be independent of changes to the CAD entities.
                """
                return PyMenu(self.service, "/objects/cad_association/detach_all_objects").execute(*args, **kwargs)
            def update_objects(self, *args, **kwargs):
                """
                Updates the specified geometry/mesh objects based on changes to the associated CAD objects.
                """
                return PyMenu(self.service, "/objects/cad_association/update_objects").execute(*args, **kwargs)
            def detach_objects(self, *args, **kwargs):
                """
                Detaches the CAD objects associated with the specified geometry/mesh objects. All association will be removed and the selected geometry/mesh objects will be independent of changes to the CAD entities.
                """
                return PyMenu(self.service, "/objects/cad_association/detach_objects").execute(*args, **kwargs)
            def query_object_association(self, *args, **kwargs):
                """
                Returns a list of the CAD entities associated with the objects selected.
                """
                return PyMenu(self.service, "/objects/cad_association/query_object_association").execute(*args, **kwargs)
            def unlock_cad(self, *args, **kwargs):
                """
                Unlocks the CAD objects associated with the selected geometry/mesh objects.
                """
                return PyMenu(self.service, "/objects/cad_association/unlock_cad").execute(*args, **kwargs)
            def restore_cad(self, *args, **kwargs):
                """
                Restores the geometry/mesh objects from the associated CAD objects.
                """
                return PyMenu(self.service, "/objects/cad_association/restore_cad").execute(*args, **kwargs)

        class set(metaclass=PyMenuMeta):
            """
            Contains options for setting additional object-related settings.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def set_edge_feature_angle(self, *args, **kwargs):
                """
                Sets the edge feature angle to be used for extracting edge zone(s) from the face zone(s) included in the object(s).
                """
                return PyMenu(self.service, "/objects/set/set_edge_feature_angle").execute(*args, **kwargs)
            def show_face_zones(self, *args, **kwargs):
                """
                Displays the face zone(s) comprising the object(s) drawn in the graphics window.
                """
                return PyMenu(self.service, "/objects/set/show_face_zones").execute(*args, **kwargs)
            def show_edge_zones(self, *args, **kwargs):
                """
                Displays the edge zone(s) comprising the object(s) drawn in the graphics window.
                """
                return PyMenu(self.service, "/objects/set/show_edge_zones").execute(*args, **kwargs)

        class deprecated(metaclass=PyMenuMeta):
            """
            Deprecated features.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def create_mesh_object_from_wrap(self, *args, **kwargs):
                """
                Create mesh object from a wrap object.
                """
                return PyMenu(self.service, "/objects/deprecated/create_mesh_object_from_wrap").execute(*args, **kwargs)

        class wrap(metaclass=PyMenuMeta):
            """
            Contains options related to the object wrapping operation.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
                self.set = self.__class__.set(path + [("set", None)], service)
            def wrap(self, *args, **kwargs):
                """
                Creates the mesh objects based on the geometry objects selected and other object wrapping parameters specified. 
                """
                return PyMenu(self.service, "/objects/wrap/wrap").execute(*args, **kwargs)
            def check_holes(self, *args, **kwargs):
                """
                Allows you to check for holes in the objects. The number of hole faces marked will be reported.
                """
                return PyMenu(self.service, "/objects/wrap/check_holes").execute(*args, **kwargs)
            def object_zone_separate(self, *args, **kwargs):
                """
                Separate Object Face Zones.
                """
                return PyMenu(self.service, "/objects/wrap/object_zone_separate").execute(*args, **kwargs)
            def debug(self, *args, **kwargs):
                """
                Debug from intermediate objects.
                """
                return PyMenu(self.service, "/objects/wrap/debug").execute(*args, **kwargs)

            class set(metaclass=PyMenuMeta):
                """
                Contains additional options related to the object wrapping operation.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def use_ray_tracing(self, *args, **kwargs):
                    """
                    Use ray tracing.
                    """
                    return PyMenu(self.service, "/objects/wrap/set/use_ray_tracing").execute(*args, **kwargs)
                def delete_far_edges(self, *args, **kwargs):
                    """
                    Delete-far-edges-after-wrap.
                    """
                    return PyMenu(self.service, "/objects/wrap/set/delete_far_edges").execute(*args, **kwargs)
                def use_smooth_folded_faces(self, *args, **kwargs):
                    """
                    Use smooth folded faces.
                    """
                    return PyMenu(self.service, "/objects/wrap/set/use_smooth_folded_faces").execute(*args, **kwargs)
                def include_thin_cut_edges_and_faces(self, *args, **kwargs):
                    """
                    Allows better recovery of thin region configurations during the object wrapping operation.
                    """
                    return PyMenu(self.service, "/objects/wrap/set/include_thin_cut_edges_and_faces").execute(*args, **kwargs)
                def shrink_wrap_rezone_parameters(self, *args, **kwargs):
                    """
                    Allows you to set the parameters for improving the mesh object surface quality using rezoning. The geometry object zones will be separated based on the separation angle specified to improve the feature imprinting on the mesh object.
                    """
                    return PyMenu(self.service, "/objects/wrap/set/shrink_wrap_rezone_parameters").execute(*args, **kwargs)
                def zone_name_prefix(self, *args, **kwargs):
                    """
                    Allows you to specify a prefix for the zones included in the mesh object created using the object wrapping operation.
                    """
                    return PyMenu(self.service, "/objects/wrap/set/zone_name_prefix").execute(*args, **kwargs)
                def relative_feature_tolerance(self, *args, **kwargs):
                    """
                    Specifies the relative feature tolerance for shrink wrapping.
                    """
                    return PyMenu(self.service, "/objects/wrap/set/relative_feature_tolerance").execute(*args, **kwargs)
                def minimum_topo_area(self, *args, **kwargs):
                    """
                    Specifies the minimum topological area for shrink wrapping.
                    """
                    return PyMenu(self.service, "/objects/wrap/set/minimum_topo_area").execute(*args, **kwargs)
                def minimum_relative_topo_area(self, *args, **kwargs):
                    """
                    Specifies the minimum relative topological area for shrink wrapping.
                    """
                    return PyMenu(self.service, "/objects/wrap/set/minimum_relative_topo_area").execute(*args, **kwargs)
                def minimum_topo_count(self, *args, **kwargs):
                    """
                    Specifies the minimum topological count for shrink wrapping.
                    """
                    return PyMenu(self.service, "/objects/wrap/set/minimum_topo_count").execute(*args, **kwargs)
                def minimum_relative_topo_count(self, *args, **kwargs):
                    """
                    Specifies the minimum relative topological count for shrink wrapping.
                    """
                    return PyMenu(self.service, "/objects/wrap/set/minimum_relative_topo_count").execute(*args, **kwargs)
                def resolution_factor(self, *args, **kwargs):
                    """
                    Sets the resolution factor for shrink wrapping. This option can be used to set sampling coarser or finer than the final surface mesh.
                    """
                    return PyMenu(self.service, "/objects/wrap/set/resolution_factor").execute(*args, **kwargs)
                def report_holes(self, *args, **kwargs):
                    """
                    Allows you to check for holes in the mesh object created. Holes, if any will be reported at the end of the object wrapping operation.
                    """
                    return PyMenu(self.service, "/objects/wrap/set/report_holes").execute(*args, **kwargs)
                def max_free_edges_for_hole_patching(self, *args, **kwargs):
                    """
                    Allows you to set the maximum number of free edges in a loop to fill the holes.
                    """
                    return PyMenu(self.service, "/objects/wrap/set/max_free_edges_for_hole_patching").execute(*args, **kwargs)
                def add_geometry_recovery_level_to_zones(self, *args, **kwargs):
                    """
                    Enables you to set the geometry recovery level (high or low) for the specified face zones.
                    """
                    return PyMenu(self.service, "/objects/wrap/set/add_geometry_recovery_level_to_zones").execute(*args, **kwargs)
                def list_zones_geometry_recovery_levels(self, *args, **kwargs):
                    """
                    Lists the zones based on geometry recovery level specified.
                    """
                    return PyMenu(self.service, "/objects/wrap/set/list_zones_geometry_recovery_levels").execute(*args, **kwargs)

        class remove_gaps(metaclass=PyMenuMeta):
            """
            Contains options for removing gaps between the mesh objects specified or removing the thickness in the mesh objects specified. 
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def remove_gaps(self, *args, **kwargs):
                """
                Allows you to remove gaps between the mesh objects specified or remove the thickness in the mesh objects specified. Select the appropriate repair option and specify the other parameters required.
                """
                return PyMenu(self.service, "/objects/remove_gaps/remove_gaps").execute(*args, **kwargs)
            def show_gaps(self, *args, **kwargs):
                """
                Marks the faces at the gap between mesh objects based on the gap distance and percentage margin specified.
                """
                return PyMenu(self.service, "/objects/remove_gaps/show_gaps").execute(*args, **kwargs)
            def ignore_orientation(self, *args, **kwargs):
                """
                Allows you to set whether the orientation of the normals should be taken into account while identifying the gap to be removed.
                """
                return PyMenu(self.service, "/objects/remove_gaps/ignore_orientation").execute(*args, **kwargs)

        class join_intersect(metaclass=PyMenuMeta):
            """
            Contains options for connecting overlapping and intersecting face zones.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
                self.controls = self.__class__.controls(path + [("controls", None)], service)
            def create_mesh_object(self, *args, **kwargs):
                """
                Allows you to specify one or more mesh objects to be connected in one mesh object.
                """
                return PyMenu(self.service, "/objects/join_intersect/create_mesh_object").execute(*args, **kwargs)
            def add_objects_to_mesh_object(self, *args, **kwargs):
                """
                Allows you to specify one or more mesh objects to be added to an existing mesh object.
                """
                return PyMenu(self.service, "/objects/join_intersect/add_objects_to_mesh_object").execute(*args, **kwargs)
            def join(self, *args, **kwargs):
                """
                Connects two overlapping face zones within specified angle and tolerance.
                """
                return PyMenu(self.service, "/objects/join_intersect/join").execute(*args, **kwargs)
            def intersect(self, *args, **kwargs):
                """
                Connects two intersecting face zones within specified angle and tolerance.
                """
                return PyMenu(self.service, "/objects/join_intersect/intersect").execute(*args, **kwargs)
            def compute_regions(self, *args, **kwargs):
                """
                Closed cell zone regions are computed from the specified mesh object. You may include a material point, if desired.
                """
                return PyMenu(self.service, "/objects/join_intersect/compute_regions").execute(*args, **kwargs)
            def rename_region(self, *args, **kwargs):
                """
                Enables you to specify a new name for a specified region.
                """
                return PyMenu(self.service, "/objects/join_intersect/rename_region").execute(*args, **kwargs)
            def delete_region(self, *args, **kwargs):
                """
                Removes a closed cell zone region and all of its face zones, except those which are shared by other regions, from the specified mesh object.
                """
                return PyMenu(self.service, "/objects/join_intersect/delete_region").execute(*args, **kwargs)
            def merge_regions(self, *args, **kwargs):
                """
                Specified regions are joined into a single region.
                """
                return PyMenu(self.service, "/objects/join_intersect/merge_regions").execute(*args, **kwargs)
            def change_region_type(self, *args, **kwargs):
                """
                Allows you to select a cell zone type (solid, fluid or dead) for a specific region.
                """
                return PyMenu(self.service, "/objects/join_intersect/change_region_type").execute(*args, **kwargs)
            def list_regions(self, *args, **kwargs):
                """
                Lists details of region type, volume, material point, and comprising face zones for the topological regions computed for the specified mesh object.
                """
                return PyMenu(self.service, "/objects/join_intersect/list_regions").execute(*args, **kwargs)

            class controls(metaclass=PyMenuMeta):
                """
                Build topology controls.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def remesh_post_intersection(self, *args, **kwargs):
                    """
                    Used to enable or disable automatic post-remesh operation after join or intersect.
                    """
                    return PyMenu(self.service, "/objects/join_intersect/controls/remesh_post_intersection").execute(*args, **kwargs)

        class fix_holes(metaclass=PyMenuMeta):
            """
            Fix holes in surface mesh using octree.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
                self.advanced = self.__class__.advanced(path + [("advanced", None)], service)
            def find_holes(self, *args, **kwargs):
                """
                Find holes in objects using octree.
                """
                return PyMenu(self.service, "/objects/fix_holes/find_holes").execute(*args, **kwargs)
            def reset_material_point(self, *args, **kwargs):
                """
                Reset material point of of region of interest.
                """
                return PyMenu(self.service, "/objects/fix_holes/reset_material_point").execute(*args, **kwargs)
            def patch_all_holes(self, *args, **kwargs):
                """
                Patch all wetted holes of the material point.
                """
                return PyMenu(self.service, "/objects/fix_holes/patch_all_holes").execute(*args, **kwargs)
            def open_all_holes(self, *args, **kwargs):
                """
                Open all wetted holes of the material point.
                """
                return PyMenu(self.service, "/objects/fix_holes/open_all_holes").execute(*args, **kwargs)
            def patch_holes(self, *args, **kwargs):
                """
                Patch holes even not connected by material point.
                """
                return PyMenu(self.service, "/objects/fix_holes/patch_holes").execute(*args, **kwargs)
            def open_holes(self, *args, **kwargs):
                """
                Open holes even not connected by material point.
                """
                return PyMenu(self.service, "/objects/fix_holes/open_holes").execute(*args, **kwargs)
            def shrink_wrap(self, *args, **kwargs):
                """
                Shrink wrap wetted region of material point.
                """
                return PyMenu(self.service, "/objects/fix_holes/shrink_wrap").execute(*args, **kwargs)

            class advanced(metaclass=PyMenuMeta):
                """
                Advanced fix holes options.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def patch_holes_between_material_points(self, *args, **kwargs):
                    """
                    Patch holes separating the material points.
                    """
                    return PyMenu(self.service, "/objects/fix_holes/advanced/patch_holes_between_material_points").execute(*args, **kwargs)
                def open_holes_between_material_points(self, *args, **kwargs):
                    """
                    Open holes separating the material points to merge them.
                    """
                    return PyMenu(self.service, "/objects/fix_holes/advanced/open_holes_between_material_points").execute(*args, **kwargs)
                def open_traced_holes_between_material_points(self, *args, **kwargs):
                    """
                    Trace a path between material points and open holes part of the traced path.
                    """
                    return PyMenu(self.service, "/objects/fix_holes/advanced/open_traced_holes_between_material_points").execute(*args, **kwargs)
                def patch_holes_connected_to_material_points(self, *args, **kwargs):
                    """
                    Patch all holes wetted by material points.
                    """
                    return PyMenu(self.service, "/objects/fix_holes/advanced/patch_holes_connected_to_material_points").execute(*args, **kwargs)
                def open_holes_connected_to_material_points(self, *args, **kwargs):
                    """
                    Open all holes wetted by material points.
                    """
                    return PyMenu(self.service, "/objects/fix_holes/advanced/open_holes_connected_to_material_points").execute(*args, **kwargs)
                def patch_holes_not_connected_to_material_points(self, *args, **kwargs):
                    """
                    Patch all holes other than holes wetted by material points.
                    """
                    return PyMenu(self.service, "/objects/fix_holes/advanced/patch_holes_not_connected_to_material_points").execute(*args, **kwargs)
                def open_holes_not_connected_to_material_points(self, *args, **kwargs):
                    """
                    Open all holes other than holes wetted by material points.
                    """
                    return PyMenu(self.service, "/objects/fix_holes/advanced/open_holes_not_connected_to_material_points").execute(*args, **kwargs)

        class create_new_mesh_object(metaclass=PyMenuMeta):
            """
            Contains options for creating a new mesh object by wrapping or remeshing existing objects.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def wrap(self, *args, **kwargs):
                """
                Creates a new mesh object by wrapping the specified objects individually or collectively.
                """
                return PyMenu(self.service, "/objects/create_new_mesh_object/wrap").execute(*args, **kwargs)
            def remesh(self, *args, **kwargs):
                """
                Creates a new mesh object by remeshing geometry objects individually or collectively.
                """
                return PyMenu(self.service, "/objects/create_new_mesh_object/remesh").execute(*args, **kwargs)

        class labels(metaclass=PyMenuMeta):
            """
            Contains options for creating and managing face zone labels.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
                self.cavity = self.__class__.cavity(path + [("cavity", None)], service)
            def create(self, *args, **kwargs):
                """
                Creates a new face zone label for the specified face zones.
                """
                return PyMenu(self.service, "/objects/labels/create").execute(*args, **kwargs)
            def create_label_per_object(self, *args, **kwargs):
                """
                Creates a new face zone label for all the face zones in every object.
                """
                return PyMenu(self.service, "/objects/labels/create_label_per_object").execute(*args, **kwargs)
            def rename(self, *args, **kwargs):
                """
                Renames the specified face zone label.
                """
                return PyMenu(self.service, "/objects/labels/rename").execute(*args, **kwargs)
            def merge(self, *args, **kwargs):
                """
                Merges the specified face zone labels to a single label with the name specified.
                """
                return PyMenu(self.service, "/objects/labels/merge").execute(*args, **kwargs)
            def delete(self, *args, **kwargs):
                """
                Deletes the specified face zone labels.
                """
                return PyMenu(self.service, "/objects/labels/delete").execute(*args, **kwargs)
            def add_zones(self, *args, **kwargs):
                """
                Adds the specified face zones to the existing face zone label for an object.
                """
                return PyMenu(self.service, "/objects/labels/add_zones").execute(*args, **kwargs)
            def label_unlabeled_zones(self, *args, **kwargs):
                """
                Creates labels for unlabeled face zones within the specified object. You can either use the object name as the label or provide your own label.
                """
                return PyMenu(self.service, "/objects/labels/label_unlabeled_zones").execute(*args, **kwargs)
            def remove_zones(self, *args, **kwargs):
                """
                Removes the specified face zones from the existing face zone label for an object.
                """
                return PyMenu(self.service, "/objects/labels/remove_zones").execute(*args, **kwargs)
            def remove_all_labels_on_zones(self, *args, **kwargs):
                """
                Removes all the face zone labels for the specified face zones. This command is applicable to geometry objects only.
                """
                return PyMenu(self.service, "/objects/labels/remove_all_labels_on_zones").execute(*args, **kwargs)
            def create_label_per_zone(self, *args, **kwargs):
                """
                Creates a new face zone label for each face zone in the object.
                """
                return PyMenu(self.service, "/objects/labels/create_label_per_zone").execute(*args, **kwargs)

            class cavity(metaclass=PyMenuMeta):
                """
                Enter menu to create cavity using labels.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def replace(self, *args, **kwargs):
                    """
                    Create cavity by replacing labels from another mesh object.
                    """
                    return PyMenu(self.service, "/objects/labels/cavity/replace").execute(*args, **kwargs)
                def remove(self, *args, **kwargs):
                    """
                    Create cavity by removing labels.
                    """
                    return PyMenu(self.service, "/objects/labels/cavity/remove").execute(*args, **kwargs)
                def add(self, *args, **kwargs):
                    """
                    Create cavity by adding labels from another mesh object.
                    """
                    return PyMenu(self.service, "/objects/labels/cavity/add").execute(*args, **kwargs)

        class volumetric_regions(metaclass=PyMenuMeta):
            """
            Manage volumetric regions of an object.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
                self.scoped_prism = self.__class__.scoped_prism(path + [("scoped_prism", None)], service)
                self.tet = self.__class__.tet(path + [("tet", None)], service)
                self.hexcore = self.__class__.hexcore(path + [("hexcore", None)], service)
            def compute(self, *args, **kwargs):
                """
                Computes the volumetric regions based on the face zone labels. You can choose to use existing material points for computing the regions.  When regions are computed, region names and types will be based on the face zone labels of the mesh object selected. If regions are recomputed, all previous region names and types will be over written.
                """
                return PyMenu(self.service, "/objects/volumetric_regions/compute").execute(*args, **kwargs)
            def update(self, *args, **kwargs):
                """
                Recomputes the selected volumetric region(s) while preserving the region name(s) and type(s).
                """
                return PyMenu(self.service, "/objects/volumetric_regions/update").execute(*args, **kwargs)
            def rename(self, *args, **kwargs):
                """
                Renames the region.
                """
                return PyMenu(self.service, "/objects/volumetric_regions/rename").execute(*args, **kwargs)
            def delete(self, *args, **kwargs):
                """
                Deletes the specified volumetric regions.
                """
                return PyMenu(self.service, "/objects/volumetric_regions/delete").execute(*args, **kwargs)
            def merge(self, *args, **kwargs):
                """
                Merges specified regions in to a single region.  If there are shared face zones, merging regions will delete the shared face zones. However, if there are cell zones associated with the regions, then merging the regions will not delete the shared face zones. In this case, the shared face zones will be deleted when the cell zones are deleted.
                """
                return PyMenu(self.service, "/objects/volumetric_regions/merge").execute(*args, **kwargs)
            def change_type(self, *args, **kwargs):
                """
                Enables you to change the region type.
                """
                return PyMenu(self.service, "/objects/volumetric_regions/change_type").execute(*args, **kwargs)
            def list(self, *args, **kwargs):
                """
                Prints region information to the console, including type, volume, material point and face zones.
                """
                return PyMenu(self.service, "/objects/volumetric_regions/list").execute(*args, **kwargs)
            def auto_fill_volume(self, *args, **kwargs):
                """
                Creates the volume mesh for the selected volumetric regions based on the meshing parameters set.
                """
                return PyMenu(self.service, "/objects/volumetric_regions/auto_fill_volume").execute(*args, **kwargs)
            def fill_empty_volume(self, *args, **kwargs):
                """
                Fill empty volume of selected regions.
                """
                return PyMenu(self.service, "/objects/volumetric_regions/fill_empty_volume").execute(*args, **kwargs)
            def merge_cells(self, *args, **kwargs):
                """
                Merge all cell zones assocaited to a region.
                """
                return PyMenu(self.service, "/objects/volumetric_regions/merge_cells").execute(*args, **kwargs)
            def delete_cells(self, *args, **kwargs):
                """
                Deletes the cell zones of the specified regions.
                """
                return PyMenu(self.service, "/objects/volumetric_regions/delete_cells").execute(*args, **kwargs)

            class scoped_prism(metaclass=PyMenuMeta):
                """
                Contains options for setting scoped prism controls.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                    self.set = self.__class__.set(path + [("set", None)], service)
                def generate(self, *args, **kwargs):
                    """
                    Grow prism into selected region using scoped prism controls.
                    """
                    return PyMenu(self.service, "/objects/volumetric_regions/scoped_prism/generate").execute(*args, **kwargs)

                class set(metaclass=PyMenuMeta):
                    """
                    Enter scoped prism settings.
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                    def create(self, *args, **kwargs):
                        """
                        Create new scoped prism.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/scoped_prism/set/create").execute(*args, **kwargs)
                    def modify(self, *args, **kwargs):
                        """
                        Modify scoped prisms.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/scoped_prism/set/modify").execute(*args, **kwargs)
                    def delete(self, *args, **kwargs):
                        """
                        Delete scoped prisms.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/scoped_prism/set/delete").execute(*args, **kwargs)
                    def list(self, *args, **kwargs):
                        """
                        List all scoped prisms parameters.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/scoped_prism/set/list").execute(*args, **kwargs)
                    def read(self, *args, **kwargs):
                        """
                        Read scoped prisms from a file.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/scoped_prism/set/read").execute(*args, **kwargs)
                    def set_no_imprint_zones(self, *args, **kwargs):
                        """
                        Set zones which should not be imprinted during prism generation.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/scoped_prism/set/set_no_imprint_zones").execute(*args, **kwargs)
                    def write(self, *args, **kwargs):
                        """
                        Write scoped prisms to a file.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/scoped_prism/set/write").execute(*args, **kwargs)
                    def growth_options(self, *args, **kwargs):
                        """
                        Set scoped prisms growth options.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/scoped_prism/set/growth_options").execute(*args, **kwargs)
                    def set_overset_prism_controls(self, *args, **kwargs):
                        """
                        Set boundary layer controls for overset mesh generation.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/scoped_prism/set/set_overset_prism_controls").execute(*args, **kwargs)
                    def set_advanced_controls(self, *args, **kwargs):
                        """
                        Set scoped boundary layer controls.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/scoped_prism/set/set_advanced_controls").execute(*args, **kwargs)

            class tet(metaclass=PyMenuMeta):
                """
                Contains options for setting tetrahedral mesh controls. See mesh/
                            
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                    self.set = self.__class__.set(path + [("set", None)], service)
                def generate(self, *args, **kwargs):
                    """
                    Fill empty volume of selected regions with tets.
                    """
                    return PyMenu(self.service, "/objects/volumetric_regions/tet/generate").execute(*args, **kwargs)

                class set(metaclass=PyMenuMeta):
                    """
                    Enter tet settings.
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                        self.improve_mesh = self.__class__.improve_mesh(path + [("improve_mesh", None)], service)
                        self.adv_front_method = self.__class__.adv_front_method(path + [("adv_front_method", None)], service)
                        self.remove_slivers = self.__class__.remove_slivers(path + [("remove_slivers", None)], service)
                        self.tet_improve = self.__class__.tet_improve(path + [("tet_improve", None)], service)
                    def cell_sizing(self, *args, **kwargs):
                        """
                        Allow cell volume distribution to be determined based on boundary.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/tet/set/cell_sizing").execute(*args, **kwargs)
                    def set_zone_growth_rate(self, *args, **kwargs):
                        """
                        Set zone specific geometric growth rates.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/tet/set/set_zone_growth_rate").execute(*args, **kwargs)
                    def clear_zone_growth_rate(self, *args, **kwargs):
                        """
                        Clear zone specific geometric growth rates.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/tet/set/clear_zone_growth_rate").execute(*args, **kwargs)
                    def compute_max_cell_volume(self, *args, **kwargs):
                        """
                        Computes max cell size.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/tet/set/compute_max_cell_volume").execute(*args, **kwargs)
                    def delete_dead_zones(self, *args, **kwargs):
                        """
                        Automatically delete dead face and cell zones?.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/tet/set/delete_dead_zones").execute(*args, **kwargs)
                    def max_cell_length(self, *args, **kwargs):
                        """
                        Set max-cell-length.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/tet/set/max_cell_length").execute(*args, **kwargs)
                    def max_cell_volume(self, *args, **kwargs):
                        """
                        Set max-cell-volume.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/tet/set/max_cell_volume").execute(*args, **kwargs)
                    def use_max_cell_size(self, *args, **kwargs):
                        """
                        Use max cell size for objects in auto-mesh and do not recompute it based on the object being meshed.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/tet/set/use_max_cell_size").execute(*args, **kwargs)
                    def non_fluid_type(self, *args, **kwargs):
                        """
                        Select the default non-fluid cell zone type.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/tet/set/non_fluid_type").execute(*args, **kwargs)
                    def refine_method(self, *args, **kwargs):
                        """
                        Define refinement method.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/tet/set/refine_method").execute(*args, **kwargs)
                    def set_region_based_sizing(self, *args, **kwargs):
                        """
                        Set region based sizings.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/tet/set/set_region_based_sizing").execute(*args, **kwargs)
                    def print_region_based_sizing(self, *args, **kwargs):
                        """
                        Print region based sizings.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/tet/set/print_region_based_sizing").execute(*args, **kwargs)
                    def skewness_method(self, *args, **kwargs):
                        """
                        Skewness refinement controls.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/tet/set/skewness_method").execute(*args, **kwargs)

                    class improve_mesh(metaclass=PyMenuMeta):
                        """
                        Improve mesh controls.
                        """
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service
                        def improve(self, *args, **kwargs):
                            """
                            Automatically improve mesh.
                            """
                            return PyMenu(self.service, "/objects/volumetric_regions/tet/set/improve_mesh/improve").execute(*args, **kwargs)
                        def swap(self, *args, **kwargs):
                            """
                            Face swap parameters.
                            """
                            return PyMenu(self.service, "/objects/volumetric_regions/tet/set/improve_mesh/swap").execute(*args, **kwargs)
                        def skewness_smooth(self, *args, **kwargs):
                            """
                            Skewness smooth parametersx.
                            """
                            return PyMenu(self.service, "/objects/volumetric_regions/tet/set/improve_mesh/skewness_smooth").execute(*args, **kwargs)
                        def laplace_smooth(self, *args, **kwargs):
                            """
                            Laplace smooth parameters.
                            """
                            return PyMenu(self.service, "/objects/volumetric_regions/tet/set/improve_mesh/laplace_smooth").execute(*args, **kwargs)

                    class adv_front_method(metaclass=PyMenuMeta):
                        """
                        Advancing front refinement controls.
                        """
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service
                            self.skew_improve = self.__class__.skew_improve(path + [("skew_improve", None)], service)
                        def refine_parameters(self, *args, **kwargs):
                            """
                            Define refine parameters.
                            """
                            return PyMenu(self.service, "/objects/volumetric_regions/tet/set/adv_front_method/refine_parameters").execute(*args, **kwargs)
                        def first_improve_params(self, *args, **kwargs):
                            """
                            Define refine front improve parameters.
                            """
                            return PyMenu(self.service, "/objects/volumetric_regions/tet/set/adv_front_method/first_improve_params").execute(*args, **kwargs)
                        def second_improve_params(self, *args, **kwargs):
                            """
                            Define cell zone improve parameters.
                            """
                            return PyMenu(self.service, "/objects/volumetric_regions/tet/set/adv_front_method/second_improve_params").execute(*args, **kwargs)

                        class skew_improve(metaclass=PyMenuMeta):
                            """
                            Refine improve controls.
                            """
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service
                            def boundary_sliver_skew(self, *args, **kwargs):
                                """
                                Refine improve boundary sliver skew.
                                """
                                return PyMenu(self.service, "/objects/volumetric_regions/tet/set/adv_front_method/skew_improve/boundary_sliver_skew").execute(*args, **kwargs)
                            def sliver_skew(self, *args, **kwargs):
                                """
                                Refine improve sliver skew.
                                """
                                return PyMenu(self.service, "/objects/volumetric_regions/tet/set/adv_front_method/skew_improve/sliver_skew").execute(*args, **kwargs)
                            def target(self, *args, **kwargs):
                                """
                                Activate target skew refinement.
                                """
                                return PyMenu(self.service, "/objects/volumetric_regions/tet/set/adv_front_method/skew_improve/target").execute(*args, **kwargs)
                            def target_skew(self, *args, **kwargs):
                                """
                                Refine improve target skew.
                                """
                                return PyMenu(self.service, "/objects/volumetric_regions/tet/set/adv_front_method/skew_improve/target_skew").execute(*args, **kwargs)
                            def target_low_skew(self, *args, **kwargs):
                                """
                                Refine improve target low skew.
                                """
                                return PyMenu(self.service, "/objects/volumetric_regions/tet/set/adv_front_method/skew_improve/target_low_skew").execute(*args, **kwargs)
                            def attempts(self, *args, **kwargs):
                                """
                                Refine improve attempts.
                                """
                                return PyMenu(self.service, "/objects/volumetric_regions/tet/set/adv_front_method/skew_improve/attempts").execute(*args, **kwargs)
                            def iterations(self, *args, **kwargs):
                                """
                                Refine improve iterations.
                                """
                                return PyMenu(self.service, "/objects/volumetric_regions/tet/set/adv_front_method/skew_improve/iterations").execute(*args, **kwargs)

                    class remove_slivers(metaclass=PyMenuMeta):
                        """
                        Sliver remove controls.
                        """
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service
                        def remove(self, *args, **kwargs):
                            """
                            Automatically remove slivers.
                            """
                            return PyMenu(self.service, "/objects/volumetric_regions/tet/set/remove_slivers/remove").execute(*args, **kwargs)
                        def skew(self, *args, **kwargs):
                            """
                            Remove sliver skew.
                            """
                            return PyMenu(self.service, "/objects/volumetric_regions/tet/set/remove_slivers/skew").execute(*args, **kwargs)
                        def low_skew(self, *args, **kwargs):
                            """
                            Remove sliver low skew.
                            """
                            return PyMenu(self.service, "/objects/volumetric_regions/tet/set/remove_slivers/low_skew").execute(*args, **kwargs)
                        def angle(self, *args, **kwargs):
                            """
                            Max dihedral angle defining a valid boundary sliver.
                            """
                            return PyMenu(self.service, "/objects/volumetric_regions/tet/set/remove_slivers/angle").execute(*args, **kwargs)
                        def attempts(self, *args, **kwargs):
                            """
                            Sliver remove attempts.
                            """
                            return PyMenu(self.service, "/objects/volumetric_regions/tet/set/remove_slivers/attempts").execute(*args, **kwargs)
                        def iterations(self, *args, **kwargs):
                            """
                            Sliver remove iterations.
                            """
                            return PyMenu(self.service, "/objects/volumetric_regions/tet/set/remove_slivers/iterations").execute(*args, **kwargs)
                        def method(self, *args, **kwargs):
                            """
                            Sliver remove method.
                            """
                            return PyMenu(self.service, "/objects/volumetric_regions/tet/set/remove_slivers/method").execute(*args, **kwargs)

                    class tet_improve(metaclass=PyMenuMeta):
                        """
                        Improve cells controls.
                        """
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service
                        def skew(self, *args, **kwargs):
                            """
                            Remove skew.
                            """
                            return PyMenu(self.service, "/objects/volumetric_regions/tet/set/tet_improve/skew").execute(*args, **kwargs)
                        def angle(self, *args, **kwargs):
                            """
                            Max dihedral angle defining a valid boundary cell.
                            """
                            return PyMenu(self.service, "/objects/volumetric_regions/tet/set/tet_improve/angle").execute(*args, **kwargs)
                        def attempts(self, *args, **kwargs):
                            """
                            Improve attempts.
                            """
                            return PyMenu(self.service, "/objects/volumetric_regions/tet/set/tet_improve/attempts").execute(*args, **kwargs)
                        def iterations(self, *args, **kwargs):
                            """
                            Improve iterations.
                            """
                            return PyMenu(self.service, "/objects/volumetric_regions/tet/set/tet_improve/iterations").execute(*args, **kwargs)

            class hexcore(metaclass=PyMenuMeta):
                """
                Contains options for setting hexcore mesh controls. See mesh/
                            
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                    self.set = self.__class__.set(path + [("set", None)], service)
                def generate(self, *args, **kwargs):
                    """
                    Fill empty volume of selected regions with hexcore.
                    """
                    return PyMenu(self.service, "/objects/volumetric_regions/hexcore/generate").execute(*args, **kwargs)

                class set(metaclass=PyMenuMeta):
                    """
                    Enter hexcore settings.
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                        self.outer_domain_params = self.__class__.outer_domain_params(path + [("outer_domain_params", None)], service)
                    def define_hexcore_extents(self, *args, **kwargs):
                        """
                        Enables sspecificaton of hexcore outer domain parameters.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/hexcore/set/define_hexcore_extents").execute(*args, **kwargs)
                    def buffer_layers(self, *args, **kwargs):
                        """
                        Number of addition cells to mark for subdivision.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/hexcore/set/buffer_layers").execute(*args, **kwargs)
                    def delete_dead_zones(self, *args, **kwargs):
                        """
                        Delete dead zones after hexcore creation.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/hexcore/set/delete_dead_zones").execute(*args, **kwargs)
                    def maximum_cell_length(self, *args, **kwargs):
                        """
                        Maximum cell length.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/hexcore/set/maximum_cell_length").execute(*args, **kwargs)
                    def compute_max_cell_length(self, *args, **kwargs):
                        """
                        Compute maximum cell length.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/hexcore/set/compute_max_cell_length").execute(*args, **kwargs)
                    def maximum_initial_cells(self, *args, **kwargs):
                        """
                        Maximum number of initial Cartesian cells.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/hexcore/set/maximum_initial_cells").execute(*args, **kwargs)
                    def non_fluid_type(self, *args, **kwargs):
                        """
                        Set non fluid type for cell zones.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/hexcore/set/non_fluid_type").execute(*args, **kwargs)
                    def peel_layers(self, *args, **kwargs):
                        """
                        Number of hexcore cells to peel back from boundary.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/hexcore/set/peel_layers").execute(*args, **kwargs)
                    def skip_tet_refinement(self, *args, **kwargs):
                        """
                        Skip tethedral refinement in transition cell generation.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/hexcore/set/skip_tet_refinement").execute(*args, **kwargs)
                    def merge_tets_to_pyramids(self, *args, **kwargs):
                        """
                        Merge tets into pyramids.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/hexcore/set/merge_tets_to_pyramids").execute(*args, **kwargs)
                    def octree_hexcore(self, *args, **kwargs):
                        """
                        Create hexcore using size-function driven octree.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/hexcore/set/octree_hexcore").execute(*args, **kwargs)
                    def avoid_1_by_8_cell_jump_in_hexcore(self, *args, **kwargs):
                        """
                        Avoid-1:8-cell-jump-in-hexcore.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/hexcore/set/avoid_1_by_8_cell_jump_in_hexcore").execute(*args, **kwargs)
                    def set_region_based_sizing(self, *args, **kwargs):
                        """
                        Set region based sizings.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/hexcore/set/set_region_based_sizing").execute(*args, **kwargs)
                    def print_region_based_sizing(self, *args, **kwargs):
                        """
                        Print region based sizings.
                        """
                        return PyMenu(self.service, "/objects/volumetric_regions/hexcore/set/print_region_based_sizing").execute(*args, **kwargs)

                    class outer_domain_params(metaclass=PyMenuMeta):
                        """
                        Define outer domain parameters.
                        """
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service
                        def specify_coordinates(self, *args, **kwargs):
                            """
                            Enables specification of coordinates of hexcore outer box.
                            """
                            return PyMenu(self.service, "/objects/volumetric_regions/hexcore/set/outer_domain_params/specify_coordinates").execute(*args, **kwargs)
                        def coordinates(self, *args, **kwargs):
                            """
                            Secifiy coordinates of outer box.
                            """
                            return PyMenu(self.service, "/objects/volumetric_regions/hexcore/set/outer_domain_params/coordinates").execute(*args, **kwargs)
                        def specify_boundaries(self, *args, **kwargs):
                            """
                            Set parameters to get hex mesh to boundary(s).
                            """
                            return PyMenu(self.service, "/objects/volumetric_regions/hexcore/set/outer_domain_params/specify_boundaries").execute(*args, **kwargs)
                        def boundaries(self, *args, **kwargs):
                            """
                            Set box-aligned zones which  have to be removed from hexcore meshing.
                            """
                            return PyMenu(self.service, "/objects/volumetric_regions/hexcore/set/outer_domain_params/boundaries").execute(*args, **kwargs)
                        def auto_align(self, *args, **kwargs):
                            """
                            Enable auto-align?.
                            """
                            return PyMenu(self.service, "/objects/volumetric_regions/hexcore/set/outer_domain_params/auto_align").execute(*args, **kwargs)
                        def auto_align_tolerance(self, *args, **kwargs):
                            """
                            Set auto-align-tolerance.
                            """
                            return PyMenu(self.service, "/objects/volumetric_regions/hexcore/set/outer_domain_params/auto_align_tolerance").execute(*args, **kwargs)
                        def auto_align_boundaries(self, *args, **kwargs):
                            """
                            Auto-align selected boundaries.
                            """
                            return PyMenu(self.service, "/objects/volumetric_regions/hexcore/set/outer_domain_params/auto_align_boundaries").execute(*args, **kwargs)
                        def delete_old_face_zones(self, *args, **kwargs):
                            """
                            Delete replaced old tri face zones.
                            """
                            return PyMenu(self.service, "/objects/volumetric_regions/hexcore/set/outer_domain_params/delete_old_face_zones").execute(*args, **kwargs)
                        def list(self, *args, **kwargs):
                            """
                            List the face zones selected for hexcore up to boundaries.
                            """
                            return PyMenu(self.service, "/objects/volumetric_regions/hexcore/set/outer_domain_params/list").execute(*args, **kwargs)

    class diagnostics(metaclass=PyMenuMeta):
        """
        Diagnostic tools.
        """
        def __init__(self, path, service):
            self.path = path
            self.service = service
            self.face_connectivity = self.__class__.face_connectivity(path + [("face_connectivity", None)], service)
            self.quality = self.__class__.quality(path + [("quality", None)], service)
        def perform_summary(self, *args, **kwargs):
            """
            Performs diagnostics check and report in console.
            """
            return PyMenu(self.service, "/diagnostics/perform_summary").execute(*args, **kwargs)
        def set_scope(self, *args, **kwargs):
            """
            Set Diagnostics scope.
            """
            return PyMenu(self.service, "/diagnostics/set_scope").execute(*args, **kwargs)
        def manage_summary(self, *args, **kwargs):
            """
            Manage diagnostics summary checks.
            """
            return PyMenu(self.service, "/diagnostics/manage_summary").execute(*args, **kwargs)
        def modify_defaults(self, *args, **kwargs):
            """
            Modify diagnostics defaults.
            """
            return PyMenu(self.service, "/diagnostics/modify_defaults").execute(*args, **kwargs)

        class face_connectivity(metaclass=PyMenuMeta):
            """
            Contains options for fixing problems with face connectivity on the specified object face zones or boundary face zones.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def fix_free_faces(self, *args, **kwargs):
                """
                Removes free faces by the method selected. The methods available are:
                """
                return PyMenu(self.service, "/diagnostics/face_connectivity/fix_free_faces").execute(*args, **kwargs)
            def fix_multi_faces(self, *args, **kwargs):
                """
                Fixes multiply connected faces by a combination of deleting face fringes, overlapping faces, and disconnected faces. Specify the maximum number of fringe faces, overlapping faces, and multiply connected edges, respectively.
                """
                return PyMenu(self.service, "/diagnostics/face_connectivity/fix_multi_faces").execute(*args, **kwargs)
            def fix_self_intersections(self, *args, **kwargs):
                """
                Fixes self intersecting or folded faces. For fixing folded faces by smoothing, specify whether features should be imprinted.
                """
                return PyMenu(self.service, "/diagnostics/face_connectivity/fix_self_intersections").execute(*args, **kwargs)
            def fix_duplicate_faces(self, *args, **kwargs):
                """
                Removes duplicate faces.
                """
                return PyMenu(self.service, "/diagnostics/face_connectivity/fix_duplicate_faces").execute(*args, **kwargs)
            def fix_spikes(self, *args, **kwargs):
                """
                Fixes spiked faces based on the spike angle specified.
                """
                return PyMenu(self.service, "/diagnostics/face_connectivity/fix_spikes").execute(*args, **kwargs)
            def fix_islands(self, *args, **kwargs):
                """
                Deletes groups of island faces based on the absolute face count specified.
                """
                return PyMenu(self.service, "/diagnostics/face_connectivity/fix_islands").execute(*args, **kwargs)
            def fix_steps(self, *args, **kwargs):
                """
                Fixes step configurations by smoothing or collapsing faces based on the angle and step width specified.
                """
                return PyMenu(self.service, "/diagnostics/face_connectivity/fix_steps").execute(*args, **kwargs)
            def fix_slivers(self, *args, **kwargs):
                """
                Fixes faces based on skewness and height criteria. Height is the perpendicular distance between the longest edge of the triangle and the opposite node.
                """
                return PyMenu(self.service, "/diagnostics/face_connectivity/fix_slivers").execute(*args, **kwargs)
            def fix_deviations(self, *args, **kwargs):
                """
                Fixes deviations in the wrapped surface mesh by imprinting edges on the wrapped face zones. Specify the number of imprint iterations and aggressive imprint iterations to be performed.
                """
                return PyMenu(self.service, "/diagnostics/face_connectivity/fix_deviations").execute(*args, **kwargs)
            def fix_point_contacts(self, *args, **kwargs):
                """
                Fixes non-manifold configurations by removing point contacts.
                """
                return PyMenu(self.service, "/diagnostics/face_connectivity/fix_point_contacts").execute(*args, **kwargs)
            def fix_invalid_normals(self, *args, **kwargs):
                """
                Fixes invalid normals by smoothing.  Zone-specific or scoped prism settings should be applied prior to using this command.
                """
                return PyMenu(self.service, "/diagnostics/face_connectivity/fix_invalid_normals").execute(*args, **kwargs)
            def add_label_to_small_neighbors(self, *args, **kwargs):
                """
                Separates island object face zones from all connected neighbors and merges them to the connected neighboring face zone label based on minimum face count specified.
                """
                return PyMenu(self.service, "/diagnostics/face_connectivity/add_label_to_small_neighbors").execute(*args, **kwargs)
            def remove_label_from_small_islands(self, *args, **kwargs):
                """
                Change small disconnected island labels to their connected neighbors.
                """
                return PyMenu(self.service, "/diagnostics/face_connectivity/remove_label_from_small_islands").execute(*args, **kwargs)

        class quality(metaclass=PyMenuMeta):
            """
            Contains options for fixing problems related to surface mesh quality on the specified object face zones or boundary face zones.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def general_improve(self, *args, **kwargs):
                """
                Improves the surface mesh based on aspect ratio, size change, or skewness. Specify the minimum quality value, feature angle, number of iterations, and whether the boundary should be preserved.
                """
                return PyMenu(self.service, "/diagnostics/quality/general_improve").execute(*args, **kwargs)
            def smooth(self, *args, **kwargs):
                """
                Improves the surface mesh by smoothing. Specify the number of smoothing iterations and whether the boundary should be preserved.
                """
                return PyMenu(self.service, "/diagnostics/quality/smooth").execute(*args, **kwargs)
            def collapse(self, *args, **kwargs):
                """
                Collapses bad quality faces based on area or skewness. For collapsing based on face area, specify the maximum face area and relative maximum area. For collapsing based on face skewness, specify the minimum skewness and feature angle. Additionally, specify the number of iterations and whether the boundary should be preserved.
                """
                return PyMenu(self.service, "/diagnostics/quality/collapse").execute(*args, **kwargs)
            def delaunay_swap(self, *args, **kwargs):
                """
                Improves the surface mesh by swapping based on the minimum skewness value and feature angle specified. Additionally, specify the number of iterations and whether the boundary should be preserved.
                """
                return PyMenu(self.service, "/diagnostics/quality/delaunay_swap").execute(*args, **kwargs)

    class material_point(metaclass=PyMenuMeta):
        """
        Manage material points.
        """
        def __init__(self, path, service):
            self.path = path
            self.service = service
        def create_material_point(self, *args, **kwargs):
            """
            Enables the definition of a material point. Specify the fluid zone name and the location to define the material point.
            """
            return PyMenu(self.service, "/material_point/create_material_point").execute(*args, **kwargs)
        def delete_material_point(self, *args, **kwargs):
            """
            Deletes the specified material point.
            """
            return PyMenu(self.service, "/material_point/delete_material_point").execute(*args, **kwargs)
        def delete_all_material_points(self, *args, **kwargs):
            """
            Enables the deletion of all defined material points.
            """
            return PyMenu(self.service, "/material_point/delete_all_material_points").execute(*args, **kwargs)
        def list_material_points(self, *args, **kwargs):
            """
            Lists all the defined material points.
            """
            return PyMenu(self.service, "/material_point/list_material_points").execute(*args, **kwargs)

    class mesh(metaclass=PyMenuMeta):
        """
        Enter the grid menu.
        """
        def __init__(self, path, service):
            self.path = path
            self.service = service
            self.cartesian = self.__class__.cartesian(path + [("cartesian", None)], service)
            self.cavity = self.__class__.cavity(path + [("cavity", None)], service)
            self.domains = self.__class__.domains(path + [("domains", None)], service)
            self.hexcore = self.__class__.hexcore(path + [("hexcore", None)], service)
            self.modify = self.__class__.modify(path + [("modify", None)], service)
            self.non_conformals = self.__class__.non_conformals(path + [("non_conformals", None)], service)
            self.rapid_octree = self.__class__.rapid_octree(path + [("rapid_octree", None)], service)
            self.prism = self.__class__.prism(path + [("prism", None)], service)
            self.pyramid = self.__class__.pyramid(path + [("pyramid", None)], service)
            self.thin_volume_mesh = self.__class__.thin_volume_mesh(path + [("thin_volume_mesh", None)], service)
            self.separate = self.__class__.separate(path + [("separate", None)], service)
            self.tet = self.__class__.tet(path + [("tet", None)], service)
            self.manage = self.__class__.manage(path + [("manage", None)], service)
            self.cell_zone_conditions = self.__class__.cell_zone_conditions(path + [("cell_zone_conditions", None)], service)
            self.poly = self.__class__.poly(path + [("poly", None)], service)
            self.poly_hexcore = self.__class__.poly_hexcore(path + [("poly_hexcore", None)], service)
            self.auto_mesh_controls = self.__class__.auto_mesh_controls(path + [("auto_mesh_controls", None)], service)
            self.scoped_prisms = self.__class__.scoped_prisms(path + [("scoped_prisms", None)], service)
        def activate_lean_datastructures(self, *args, **kwargs):
            """
            Activates Lean data structures to reduce memory.
            """
            return PyMenu(self.service, "/mesh/activate_lean_datastructures").execute(*args, **kwargs)
        def deactivate_lean_datastructures(self, *args, **kwargs):
            """
            Deactivates Lean data structures.
            """
            return PyMenu(self.service, "/mesh/deactivate_lean_datastructures").execute(*args, **kwargs)
        def auto_mesh(self, *args, **kwargs):
            """
            Enables you to generate the volume mesh automatically. Specify a mesh object name for object-based auto mesh; if no name is given, face zone based auto mesh is performed. Specify the mesh elements to be used when prompted. Specify whether to merge the cells into a single zone or keep the cell zones separate. For face zone based meshing, specify whether automatically identify the domain to be meshed based on the topology information.
            """
            return PyMenu(self.service, "/mesh/auto_mesh").execute(*args, **kwargs)
        def auto_mesh_multiple_objects(self, *args, **kwargs):
            """
            Automatically executes initialization and refinement of mesh for multiple objects.
            """
            return PyMenu(self.service, "/mesh/auto_mesh_multiple_objects").execute(*args, **kwargs)
        def check_mesh(self, *args, **kwargs):
            """
            Checks the mesh for topological errors.
            """
            return PyMenu(self.service, "/mesh/check_mesh").execute(*args, **kwargs)
        def selective_mesh_check(self, *args, **kwargs):
            """
            Performs a customized mesh check on specific zones rather than all zones.
            """
            return PyMenu(self.service, "/mesh/selective_mesh_check").execute(*args, **kwargs)
        def check_quality(self, *args, **kwargs):
            """
            Enables you to ensure that the mesh quality is appropriate before transferring the mesh to the solution mode.
            """
            return PyMenu(self.service, "/mesh/check_quality").execute(*args, **kwargs)
        def check_quality_level(self, *args, **kwargs):
            """
            Enables you to report additional quality metrics when set to 1.  In addition to the orthogonal quality and Fluent aspect ratio, additional metrics such as cell squish and skewness will be reported when the check-quality-level is set to 1.
            """
            return PyMenu(self.service, "/mesh/check_quality_level").execute(*args, **kwargs)
        def clear_mesh(self, *args, **kwargs):
            """
            Enables you to generate a new mesh by deleting the internal mesh and leaving only the boundary faces and nodes.
            """
            return PyMenu(self.service, "/mesh/clear_mesh").execute(*args, **kwargs)
        def clear_undo_stack(self, *args, **kwargs):
            """
            Clears undo stack.
            """
            return PyMenu(self.service, "/mesh/clear_undo_stack").execute(*args, **kwargs)
        def create_heat_exchanger(self, *args, **kwargs):
            """
            Creates the heat exchanger mesh. You need to specify the method for selecting the Location coordinates (by Position or Nodes), the location coordinates, the parameters for setting up mesh density (by Interval or Size), and the number of intervals (sizes) between points (nodes) 1–2, 1–3, 1–4. Also specify the object/zone name prefix and enable creating the mesh object, if required. 
            """
            return PyMenu(self.service, "/mesh/create_heat_exchanger").execute(*args, **kwargs)
        def create_frustrum(self, *args, **kwargs):
            """
            Create a cylindrical hex mesh.
            """
            return PyMenu(self.service, "/mesh/create_frustrum").execute(*args, **kwargs)
        def list_mesh_parameter(self, *args, **kwargs):
            """
            Shows all mesh parameters.
            """
            return PyMenu(self.service, "/mesh/list_mesh_parameter").execute(*args, **kwargs)
        def repair_face_handedness(self, *args, **kwargs):
            """
            Reverses face node orientation.
            """
            return PyMenu(self.service, "/mesh/repair_face_handedness").execute(*args, **kwargs)
        def laplace_smooth_nodes(self, *args, **kwargs):
            """
            Applies a Laplacian smoothing operator to the mesh nodes. This command can be used for smoothing of all cell types, including prismatic cells.
            """
            return PyMenu(self.service, "/mesh/laplace_smooth_nodes").execute(*args, **kwargs)
        def reset_mesh(self, *args, **kwargs):
            """
            Clears the entire mesh.
            """
            return PyMenu(self.service, "/mesh/reset_mesh").execute(*args, **kwargs)
        def reset_mesh_parameter(self, *args, **kwargs):
            """
            Resets all parameters to their default value.
            """
            return PyMenu(self.service, "/mesh/reset_mesh_parameter").execute(*args, **kwargs)
        def auto_prefix_cell_zones(self, *args, **kwargs):
            """
            Enables you to specify a prefix for cell zones created during the auto mesh procedure.   The auto-prefix-cell-zones command is not relevant for object-based meshing, where the cell zone names are generated based on the material points and the objects used to generate the mesh object.
            """
            return PyMenu(self.service, "/mesh/auto_prefix_cell_zones").execute(*args, **kwargs)
        def cutcell(self, *args, **kwargs):
            """
            Enters the cutcell menu. This menu is no longer supported, and will be removed in a future release.
            """
            return PyMenu(self.service, "/mesh/cutcell").execute(*args, **kwargs)
        def prepare_for_solve(self, *args, **kwargs):
            """
            Prepares the mesh for solving in solution mode by performing a cleanup operation after the volume mesh has been generated. Operations such as deleting dead zones, deleting geometry objects, deleting edge zones, deleting unused faces and nodes are performed during this operation.
            """
            return PyMenu(self.service, "/mesh/prepare_for_solve").execute(*args, **kwargs)
        def zone_names_clean_up(self, *args, **kwargs):
            """
            S
            """
            return PyMenu(self.service, "/mesh/zone_names_clean_up").execute(*args, **kwargs)

        class cartesian(metaclass=PyMenuMeta):
            """
            Enter Cartesian mesh menu.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def mesh(self, *args, **kwargs):
                """
                Generate Cartesian mesh.
                """
                return PyMenu(self.service, "/mesh/cartesian/mesh").execute(*args, **kwargs)

        class cavity(metaclass=PyMenuMeta):
            """
            Enters the cavity menu.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def replace_zones(self, *args, **kwargs):
                """
                Enables you to create a cavity for removing a set of zones from an existing volume mesh and replacing them with new set of zones.
                """
                return PyMenu(self.service, "/mesh/cavity/replace_zones").execute(*args, **kwargs)
            def add_zones(self, *args, **kwargs):
                """
                Enables you to create a cavity for adding new zones to the existing volume mesh.
                """
                return PyMenu(self.service, "/mesh/cavity/add_zones").execute(*args, **kwargs)
            def remove_zones(self, *args, **kwargs):
                """
                Enables you to create a cavity for removing zones from the existing volume mesh.
                """
                return PyMenu(self.service, "/mesh/cavity/remove_zones").execute(*args, **kwargs)
            def region(self, *args, **kwargs):
                """
                Enables you to create a cavity to modify the existing volume mesh in the specified region.
                """
                return PyMenu(self.service, "/mesh/cavity/region").execute(*args, **kwargs)
            def merge_cavity(self, *args, **kwargs):
                """
                Enables you to merge the specified cavity domain with the parent domain.  During the merging operation, the cavity cell zones merges with the zones in the parent domain. The wall boundaries extracted from the interior zones will be converted to  interior type and merged with the corresponding zones in the parent domain.
                """
                return PyMenu(self.service, "/mesh/cavity/merge_cavity").execute(*args, **kwargs)
            def create_hexcore_cavity_by_region(self, *args, **kwargs):
                """
                Creates the cavity in the hexcore mesh based on the zones and bounding box extents specified. The create-hexcore-cavity-by-region option is no longer supported and will be removed at a future release. 
                """
                return PyMenu(self.service, "/mesh/cavity/create_hexcore_cavity_by_region").execute(*args, **kwargs)
            def create_hexcore_cavity_by_scale(self, *args, **kwargs):
                """
                Creates the cavity in the hexcore mesh based on the zones and scale specified. The create-hexcore-cavity-by-scale option is no longer supported and will be removed at a future release. 
                """
                return PyMenu(self.service, "/mesh/cavity/create_hexcore_cavity_by_scale").execute(*args, **kwargs)
            def remesh_hexcore_cavity(self, *args, **kwargs):
                """
                Remesh a cavity in hexcore mesh.
                """
                return PyMenu(self.service, "/mesh/cavity/remesh_hexcore_cavity").execute(*args, **kwargs)

        class domains(metaclass=PyMenuMeta):
            """
            Enters the domain menu.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def activate(self, *args, **kwargs):
                """
                Activates the specified domain for meshing or reporting operations.
                """
                return PyMenu(self.service, "/mesh/domains/activate").execute(*args, **kwargs)
            def create_by_cell_zone(self, *args, **kwargs):
                """
                Creates a new domain based on the specified cell zone.
                """
                return PyMenu(self.service, "/mesh/domains/create_by_cell_zone").execute(*args, **kwargs)
            def create_by_point(self, *args, **kwargs):
                """
                Creates a new domain based on the specified   The create-by-point option works only for cases with no overlapping face zones.
                """
                return PyMenu(self.service, "/mesh/domains/create_by_point").execute(*args, **kwargs)
            def draw(self, *args, **kwargs):
                """
                Displays the boundary face zones of the specified domain.
                """
                return PyMenu(self.service, "/mesh/domains/draw").execute(*args, **kwargs)
            def create(self, *args, **kwargs):
                """
                Creates a new domain based on the specified boundary face zones. Ensure valid boundary zones are specified; specifying invalid zones will generate an error.
                """
                return PyMenu(self.service, "/mesh/domains/create").execute(*args, **kwargs)
            def delete(self, *args, **kwargs):
                """
                Deletes the specified domain.
                """
                return PyMenu(self.service, "/mesh/domains/delete").execute(*args, **kwargs)
            def print(self, *args, **kwargs):
                """
                Prints the information for the specified domain.
                """
                return PyMenu(self.service, "/mesh/domains/print").execute(*args, **kwargs)

        class hexcore(metaclass=PyMenuMeta):
            """
            Enters the hexcore menu.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
                self.controls = self.__class__.controls(path + [("controls", None)], service)
                self.local_regions = self.__class__.local_regions(path + [("local_regions", None)], service)
            def create(self, *args, **kwargs):
                """
                Enables you to create the hexcore mesh according to the specified parameters.
                """
                return PyMenu(self.service, "/mesh/hexcore/create").execute(*args, **kwargs)
            def merge_tets_to_pyramids(self, *args, **kwargs):
                """
                Enables the merge-tets-to-pyramids command to reduce the total cell count.  If skip-tet-refinement is enabled, pairs of tets will be merged into pyramids. Hexcore count is unaffected.
                """
                return PyMenu(self.service, "/mesh/hexcore/merge_tets_to_pyramids").execute(*args, **kwargs)

            class controls(metaclass=PyMenuMeta):
                """
                Enters the hexcore controls menu.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                    self.outer_domain_params = self.__class__.outer_domain_params(path + [("outer_domain_params", None)], service)
                def define_hexcore_extents(self, *args, **kwargs):
                    """
                    Enables you to extend the hexcore mesh to specified domain extents and/or selected planar boundaries. When enabled, the outer-domain-params sub-menu will be available.
                    """
                    return PyMenu(self.service, "/mesh/hexcore/controls/define_hexcore_extents").execute(*args, **kwargs)
                def buffer_layers(self, *args, **kwargs):
                    """
                    Sets the number of addition cells to mark for subdivision.
                    """
                    return PyMenu(self.service, "/mesh/hexcore/controls/buffer_layers").execute(*args, **kwargs)
                def delete_dead_zones(self, *args, **kwargs):
                    """
                    Toggles the automatic deleting of the dead zones.
                    """
                    return PyMenu(self.service, "/mesh/hexcore/controls/delete_dead_zones").execute(*args, **kwargs)
                def maximum_cell_length(self, *args, **kwargs):
                    """
                    Sets the maximum cell length for the hex cells in the domain.
                    """
                    return PyMenu(self.service, "/mesh/hexcore/controls/maximum_cell_length").execute(*args, **kwargs)
                def compute_max_cell_length(self, *args, **kwargs):
                    """
                    Computes the maximum cell length for the hexcore mesh.
                    """
                    return PyMenu(self.service, "/mesh/hexcore/controls/compute_max_cell_length").execute(*args, **kwargs)
                def maximum_initial_cells(self, *args, **kwargs):
                    """
                    Specifies the maximum number of cells in the initial Cartesian mesh.
                    """
                    return PyMenu(self.service, "/mesh/hexcore/controls/maximum_initial_cells").execute(*args, **kwargs)
                def non_fluid_type(self, *args, **kwargs):
                    """
                    Selects the default non-fluid cell zone type. After the mesh is initialized, any non-fluid zones will be set to this type. If the mesh includes multiple regions (for example, the problem for which you are creating the mesh includes a fluid zone and one or more solid zones), and you plan to refine all of them using the same refinement parameters, modify the Non-Fluid Type
                                   before generating the hexcore mesh.  For zone-based meshing, if any cell zone has at least one boundary zone type as inlet, it will automatically be set to fluid type. For object based meshing, volume region type is used to determine the cell zone type.
                    """
                    return PyMenu(self.service, "/mesh/hexcore/controls/non_fluid_type").execute(*args, **kwargs)
                def peel_layers(self, *args, **kwargs):
                    """
                    Specifies the distance for the hexcore interface to peel-back from the boundary. The default value is 0. The higher the value of peel layer, the bigger the distance between the hexcore interface and the boundary.
                    """
                    return PyMenu(self.service, "/mesh/hexcore/controls/peel_layers").execute(*args, **kwargs)
                def skip_tet_refinement(self, *args, **kwargs):
                    """
                    Enables you to omit the tetrahedral refinement phase for reducing total cell count (default is no). Hex cell count is unaffected.
                    """
                    return PyMenu(self.service, "/mesh/hexcore/controls/skip_tet_refinement").execute(*args, **kwargs)
                def merge_tets_to_pyramids(self, *args, **kwargs):
                    """
                    Merge tets into pyramids.
                    """
                    return PyMenu(self.service, "/mesh/hexcore/controls/merge_tets_to_pyramids").execute(*args, **kwargs)
                def octree_hexcore(self, *args, **kwargs):
                    """
                    Speeds up hexahedral core generation by enabling the octree technique for hexcore mesh generation. This option is disabled by default.   Body-of-influence sizing may be used for refinement.  This option does not support hexcore generation up to boundaries. 
                    """
                    return PyMenu(self.service, "/mesh/hexcore/controls/octree_hexcore").execute(*args, **kwargs)
                def avoid_1_by_8_cell_jump_in_hexcore(self, *args, **kwargs):
                    """
                    Avoid-1:8-cell-jump-in-hexcore.
                    """
                    return PyMenu(self.service, "/mesh/hexcore/controls/avoid_1_by_8_cell_jump_in_hexcore").execute(*args, **kwargs)
                def set_region_based_sizing(self, *args, **kwargs):
                    """
                    Allows you to specify local sizing settings (max cell length and growth rate) for specified region(s).
                    """
                    return PyMenu(self.service, "/mesh/hexcore/controls/set_region_based_sizing").execute(*args, **kwargs)
                def print_region_based_sizing(self, *args, **kwargs):
                    """
                    Displays local sizing settings (max cell length and growth rate) for specified region(s).
                    """
                    return PyMenu(self.service, "/mesh/hexcore/controls/print_region_based_sizing").execute(*args, **kwargs)

                class outer_domain_params(metaclass=PyMenuMeta):
                    """
                    Contains options for defining the outer domain parameters. This sub-menu is available only when define-hexcore-extents? is enabled.
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                    def specify_coordinates(self, *args, **kwargs):
                        """
                        Enables you to specify the extents of the hexcore outer box using the coordinates command.
                        """
                        return PyMenu(self.service, "/mesh/hexcore/controls/outer_domain_params/specify_coordinates").execute(*args, **kwargs)
                    def coordinates(self, *args, **kwargs):
                        """
                        Specifies the extents (min and max coordinates) of the hexcore outer box. This command is available when the specify-coordinates? option is enabled.
                        """
                        return PyMenu(self.service, "/mesh/hexcore/controls/outer_domain_params/coordinates").execute(*args, **kwargs)
                    def specify_boundaries(self, *args, **kwargs):
                        """
                        Enables you to specify selected boundaries to which the hexcore mesh is to be generated using the boundaries command.
                        """
                        return PyMenu(self.service, "/mesh/hexcore/controls/outer_domain_params/specify_boundaries").execute(*args, **kwargs)
                    def boundaries(self, *args, **kwargs):
                        """
                        Specifies the boundaries to which the hexcore mesh is to be generated when the specify-boundaries? option is enabled. After specifying the boundaries, the auto-align?, delete-old-face-zones?, and list options will also be available.
                        """
                        return PyMenu(self.service, "/mesh/hexcore/controls/outer_domain_params/boundaries").execute(*args, **kwargs)
                    def auto_align(self, *args, **kwargs):
                        """
                        Enables you to axis-align non-aligned planar boundaries to which hexcore mesh is to be generated. This option is available only when the specify-boundaries? option is enabled and the boundaries are specified.
                        """
                        return PyMenu(self.service, "/mesh/hexcore/controls/outer_domain_params/auto_align").execute(*args, **kwargs)
                    def auto_align_tolerance(self, *args, **kwargs):
                        """
                        Specifies the tolerance for aligning boundary zones when auto-align? is enabled.
                        """
                        return PyMenu(self.service, "/mesh/hexcore/controls/outer_domain_params/auto_align_tolerance").execute(*args, **kwargs)
                    def auto_align_boundaries(self, *args, **kwargs):
                        """
                        Aligns the boundary zones specified (using the boundaries command) with the tolerance specified \ (using the auto-align-tolerance command) when auto-align? is enabled.
                        """
                        return PyMenu(self.service, "/mesh/hexcore/controls/outer_domain_params/auto_align_boundaries").execute(*args, **kwargs)
                    def delete_old_face_zones(self, *args, **kwargs):
                        """
                        Enables you to delete the original tri face zones that have been replaced during the hexcore meshing process. This option is available only when the specify-boundaries? option is enabled and the boundaries are specified.
                        """
                        return PyMenu(self.service, "/mesh/hexcore/controls/outer_domain_params/delete_old_face_zones").execute(*args, **kwargs)
                    def list(self, *args, **kwargs):
                        """
                        Lists the boundaries to which the hexcore mesh is to be generated. This option is available only when the specify-boundaries? option is enabled and the boundaries are specified.
                        """
                        return PyMenu(self.service, "/mesh/hexcore/controls/outer_domain_params/list").execute(*args, **kwargs)

            class local_regions(metaclass=PyMenuMeta):
                """
                Enters the hexcore local refinement region sub-menu.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def activate(self, *args, **kwargs):
                    """
                    Enables you to activate the specified local regions for refinement.
                    """
                    return PyMenu(self.service, "/mesh/hexcore/local_regions/activate").execute(*args, **kwargs)
                def deactivate(self, *args, **kwargs):
                    """
                    Enables you to deactivate the specified local regions for refinement.
                    """
                    return PyMenu(self.service, "/mesh/hexcore/local_regions/deactivate").execute(*args, **kwargs)
                def define(self, *args, **kwargs):
                    """
                    Defines the local region according to the specified parameters.
                    """
                    return PyMenu(self.service, "/mesh/hexcore/local_regions/define").execute(*args, **kwargs)
                def delete(self, *args, **kwargs):
                    """
                    Deletes the specified refinement region.
                    """
                    return PyMenu(self.service, "/mesh/hexcore/local_regions/delete").execute(*args, **kwargs)
                def init(self, *args, **kwargs):
                    """
                    Creates a default region encompassing the entire geometry.
                    """
                    return PyMenu(self.service, "/mesh/hexcore/local_regions/init").execute(*args, **kwargs)
                def list_all_regions(self, *args, **kwargs):
                    """
                    Lists the defined and active regions in the console.
                    """
                    return PyMenu(self.service, "/mesh/hexcore/local_regions/list_all_regions").execute(*args, **kwargs)
                def ideal_hex_vol(self, *args, **kwargs):
                    """
                    Reports the ideal hex volume for the given edge length.
                    """
                    return PyMenu(self.service, "/mesh/hexcore/local_regions/ideal_hex_vol").execute(*args, **kwargs)
                def ideal_quad_area(self, *args, **kwargs):
                    """
                    Ideal quad area for given edge length.
                    """
                    return PyMenu(self.service, "/mesh/hexcore/local_regions/ideal_quad_area").execute(*args, **kwargs)

        class modify(metaclass=PyMenuMeta):
            """
            Enters the mesh modify menu.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def clear_selections(self, *args, **kwargs):
                """
                Clears all items from the selection list.
                """
                return PyMenu(self.service, "/mesh/modify/clear_selections").execute(*args, **kwargs)
            def extract_unused_nodes(self, *args, **kwargs):
                """
                Places all unused nodes in a separate interior node zone.
                """
                return PyMenu(self.service, "/mesh/modify/extract_unused_nodes").execute(*args, **kwargs)
            def smooth_node(self, *args, **kwargs):
                """
                Applies Laplace smoothing to the nodes in the selection list.
                """
                return PyMenu(self.service, "/mesh/modify/smooth_node").execute(*args, **kwargs)
            def list_selections(self, *args, **kwargs):
                """
                Lists all items in the selection list.
                """
                return PyMenu(self.service, "/mesh/modify/list_selections").execute(*args, **kwargs)
            def list_skewed_cells(self, *args, **kwargs):
                """
                Lists cells with skewness in a specified range.
                """
                return PyMenu(self.service, "/mesh/modify/list_skewed_cells").execute(*args, **kwargs)
            def mesh_node(self, *args, **kwargs):
                """
                Attempts to introduce a new node into the existing mesh.
                """
                return PyMenu(self.service, "/mesh/modify/mesh_node").execute(*args, **kwargs)
            def mesh_nodes_on_zone(self, *args, **kwargs):
                """
                Inserts nodes associated with node or face zone into the volume mesh. 
                """
                return PyMenu(self.service, "/mesh/modify/mesh_nodes_on_zone").execute(*args, **kwargs)
            def neighborhood_skew(self, *args, **kwargs):
                """
                Reports the maximum skewness of cells using the specified node.
                """
                return PyMenu(self.service, "/mesh/modify/neighborhood_skew").execute(*args, **kwargs)
            def refine_cell(self, *args, **kwargs):
                """
                Attempts to refine the cells in the probe list by introducing a node nears its centroid. This technique is useful for removing very flat cells near the boundary when boundary sliver removal is not possible. After refining the cell, you should smooth the mesh.
                """
                return PyMenu(self.service, "/mesh/modify/refine_cell").execute(*args, **kwargs)
            def deselect_last(self, *args, **kwargs):
                """
                Deselects the last item you selected using the select-entity command.
                """
                return PyMenu(self.service, "/mesh/modify/deselect_last").execute(*args, **kwargs)
            def select_entity(self, *args, **kwargs):
                """
                Adds an entity (face, node, cell, etc.) to the selection list.
                """
                return PyMenu(self.service, "/mesh/modify/select_entity").execute(*args, **kwargs)
            def auto_node_move(self, *args, **kwargs):
                """
                Enables you to improve the mesh quality by node movement. Specify the appropriate cell zones and boundary zones, the quality limit based on the quality measure selected, dihedral angle, the number of iterations per node to be moved and the number of iterations of the automatic node movement procedure (default, 1). You can also choose to restrict the movement of boundary nodes along the surface.
                """
                return PyMenu(self.service, "/mesh/modify/auto_node_move").execute(*args, **kwargs)
            def repair_negative_volume_cells(self, *args, **kwargs):
                """
                Repairs negative volume cells by moving nodes. Specify the appropriate boundary zones, the number of iterations per node to be moved, dihedral angle, whether to restrict the movement of boundary nodes along the surface, and the number of iterations of the automatic node movement procedure (default, 1).
                """
                return PyMenu(self.service, "/mesh/modify/repair_negative_volume_cells").execute(*args, **kwargs)
            def auto_improve_warp(self, *args, **kwargs):
                """
                Enables you to improve face warp by node movement. Specify the appropriate cell zones and boundary zones, the maximum warp, the number of iterations per face to be improved, and the number of iterations of the automatic node movement procedure (default, 4).
                """
                return PyMenu(self.service, "/mesh/modify/auto_improve_warp").execute(*args, **kwargs)

        class non_conformals(metaclass=PyMenuMeta):
            """
            Enters the non-conformals menu.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
                self.controls = self.__class__.controls(path + [("controls", None)], service)
            def create(self, *args, **kwargs):
                """
                Creates the non-conformal interface on the specified face zones using the specified retriangulation method.
                """
                return PyMenu(self.service, "/mesh/non_conformals/create").execute(*args, **kwargs)
            def separate(self, *args, **kwargs):
                """
                Enables you to separate the face zones comprising the non-conformal interface between the cell zones specified. Specify the cell zones where the interface is non-conformal, an appropriate gap distance, and the critical angle to be used for separating the face zones. You can also choose to orient the boundary face zones after separation and additionally write a journal file for the separation operation.   If you choose to write a journal file when using the /mesh/non-conformals/separate command to separate the mesh  interface zones, you can read the journal file to create the mesh interface automatically  in solution mode.
                """
                return PyMenu(self.service, "/mesh/non_conformals/separate").execute(*args, **kwargs)

            class controls(metaclass=PyMenuMeta):
                """
                Enters the non-conformals controls menu.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def enable(self, *args, **kwargs):
                    """
                    Toggles the creation of a non-conformal interface.
                    """
                    return PyMenu(self.service, "/mesh/non_conformals/controls/enable").execute(*args, **kwargs)
                def retri_method(self, *args, **kwargs):
                    """
                    Specifies the method to be used for retriangulating the quad faces on the non-conformal zones. 
                    """
                    return PyMenu(self.service, "/mesh/non_conformals/controls/retri_method").execute(*args, **kwargs)

        class rapid_octree(metaclass=PyMenuMeta):
            """
            Enters the rapid octree menu, which provides text commands for using the Rapid Octree mesher.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
                self.refinement_regions = self.__class__.refinement_regions(path + [("refinement_regions", None)], service)
                self.mesh_sizing = self.__class__.mesh_sizing(path + [("mesh_sizing", None)], service)
                self.advanced_meshing_options = self.__class__.advanced_meshing_options(path + [("advanced_meshing_options", None)], service)
            def verbosity(self, *args, **kwargs):
                """
                Sets the verbosity of the messages printed by the Rapid Octree mesher.
                """
                return PyMenu(self.service, "/mesh/rapid_octree/verbosity").execute(*args, **kwargs)
            def estimate_cell_count(self, *args, **kwargs):
                """
                Give a quick estimate about the expected number of cells.
                """
                return PyMenu(self.service, "/mesh/rapid_octree/estimate_cell_count").execute(*args, **kwargs)
            def distribute_geometry(self, *args, **kwargs):
                """
                Enables/disables the distribution of the input geometry across partitions / compute nodes, so that it is not copied to each process. This reduces the memory requirements of the mesh generation significantly, especially for geometries with a high number of triangles. Note that this geometric distribution is enabled by default and is automatically deactivated if the geometry is not fully enclosed by the defined bounding box.
                """
                return PyMenu(self.service, "/mesh/rapid_octree/distribute_geometry").execute(*args, **kwargs)
            def improve_geometry_resolution(self, *args, **kwargs):
                """
                Activate improved geometry resolution, will significantly increase mesh generation time.
                """
                return PyMenu(self.service, "/mesh/rapid_octree/improve_geometry_resolution").execute(*args, **kwargs)
            def dry_run(self, *args, **kwargs):
                """
                If yes: Just print diagnostic information, do not create a mesh.
                """
                return PyMenu(self.service, "/mesh/rapid_octree/dry_run").execute(*args, **kwargs)
            def undo_last_meshing_operation(self, *args, **kwargs):
                """
                Attempts to restore the object state (including its surfaces) as it was prior to the meshing operation performed by the Rapid Octree mesher.
                """
                return PyMenu(self.service, "/mesh/rapid_octree/undo_last_meshing_operation").execute(*args, **kwargs)
            def boundary_treatment(self, *args, **kwargs):
                """
                Selects the boundary treatment option. Enter 0 for the Boundary Projection treatment or 1 for the Cartesian Snapping treatment.
                """
                return PyMenu(self.service, "/mesh/rapid_octree/boundary_treatment").execute(*args, **kwargs)
            def bounding_box(self, *args, **kwargs):
                """
                Defines/modifies the bounding box around the geometry.
                """
                return PyMenu(self.service, "/mesh/rapid_octree/bounding_box").execute(*args, **kwargs)
            def reset_bounding_box(self, *args, **kwargs):
                """
                Redefines the bounding box extents to encompass all of the surfaces of the currently selected geometry, and updates the base length scale used in the mesh generation process.
                """
                return PyMenu(self.service, "/mesh/rapid_octree/reset_bounding_box").execute(*args, **kwargs)
            def geometry(self, *args, **kwargs):
                """
                Allows you to apply the Rapid Octree mesher to a defined mesh object or geometry object rather than all available surface zones. Note that using a mesh object with multiple volumetric regions allows you to generate multiple disconnected cell zones that can be coupled by a non-conformal mesh interface in the solution mode; all other input objects result in the creation of a single volume / cell zone.
                """
                return PyMenu(self.service, "/mesh/rapid_octree/geometry").execute(*args, **kwargs)
            def flow_volume(self, *args, **kwargs):
                """
                Specifies the volume to be filled by the mesh.
                """
                return PyMenu(self.service, "/mesh/rapid_octree/flow_volume").execute(*args, **kwargs)
            def create(self, *args, **kwargs):
                """
                Creates a mesh using the Rapid Octree mesher.
                """
                return PyMenu(self.service, "/mesh/rapid_octree/create").execute(*args, **kwargs)
            def create_stair_step_mesh(self, *args, **kwargs):
                """
                Create rapid octree mesh with a cartesian boundary approximation.
                """
                return PyMenu(self.service, "/mesh/rapid_octree/create_stair_step_mesh").execute(*args, **kwargs)
            def is_manifold_geo(self, *args, **kwargs):
                """
                Set to yes if the geomety is manifold (speed up mesh generation).
                """
                return PyMenu(self.service, "/mesh/rapid_octree/is_manifold_geo").execute(*args, **kwargs)
            def projection_mesh_optimization(self, *args, **kwargs):
                """
                Set optimization for projection mesh. 0 to deactivate.
                """
                return PyMenu(self.service, "/mesh/rapid_octree/projection_mesh_optimization").execute(*args, **kwargs)
            def delete_poor_quality_cells(self, *args, **kwargs):
                """
                Delete all cells with orthogonal-quality less than 0.01.
                """
                return PyMenu(self.service, "/mesh/rapid_octree/delete_poor_quality_cells").execute(*args, **kwargs)

            class refinement_regions(metaclass=PyMenuMeta):
                """
                Enters the rapid octree refinement region menu, which allows you to manage the refinement regions.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def add(self, *args, **kwargs):
                    """
                    Adds a refinement region to the domain.
                    """
                    return PyMenu(self.service, "/mesh/rapid_octree/refinement_regions/add").execute(*args, **kwargs)
                def delete(self, *args, **kwargs):
                    """
                    Deletes a refinement region.
                    """
                    return PyMenu(self.service, "/mesh/rapid_octree/refinement_regions/delete").execute(*args, **kwargs)
                def list(self, *args, **kwargs):
                    """
                    Lists all of the refinement regions.
                    """
                    return PyMenu(self.service, "/mesh/rapid_octree/refinement_regions/list").execute(*args, **kwargs)

            class mesh_sizing(metaclass=PyMenuMeta):
                """
                Enters the mesh sizing menu, which allows you to define the cell sizes.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def max_cell_size(self, *args, **kwargs):
                    """
                    Sets the maximum cell size in the octree mesh.
                    """
                    return PyMenu(self.service, "/mesh/rapid_octree/mesh_sizing/max_cell_size").execute(*args, **kwargs)
                def boundary_cell_size(self, *args, **kwargs):
                    """
                    Sets the default cell size for the geometry.
                    """
                    return PyMenu(self.service, "/mesh/rapid_octree/mesh_sizing/boundary_cell_size").execute(*args, **kwargs)
                def prism_layers(self, *args, **kwargs):
                    """
                    Specify the number of prismatic layers for surface zones.
                    """
                    return PyMenu(self.service, "/mesh/rapid_octree/mesh_sizing/prism_layers").execute(*args, **kwargs)
                def clear_prism_layer_settings(self, *args, **kwargs):
                    """
                    Delete all settings for prismatic layers in the domain.
                    """
                    return PyMenu(self.service, "/mesh/rapid_octree/mesh_sizing/clear_prism_layer_settings").execute(*args, **kwargs)
                def boundary_layers(self, *args, **kwargs):
                    """
                    Set the minimum number of constant-size cells adjacent to the geometry.
                    """
                    return PyMenu(self.service, "/mesh/rapid_octree/mesh_sizing/boundary_layers").execute(*args, **kwargs)
                def buffer_layers(self, *args, **kwargs):
                    """
                    Set the number of buffer layers.
                    """
                    return PyMenu(self.service, "/mesh/rapid_octree/mesh_sizing/buffer_layers").execute(*args, **kwargs)
                def surface_coarsening_layers(self, *args, **kwargs):
                    """
                    Set the minimum number of constant-size cells adjacent to the geometry.
                    """
                    return PyMenu(self.service, "/mesh/rapid_octree/mesh_sizing/surface_coarsening_layers").execute(*args, **kwargs)
                def mesh_coarsening_exponent(self, *args, **kwargs):
                    """
                    Set the exponent for mesh coarsening.
                    """
                    return PyMenu(self.service, "/mesh/rapid_octree/mesh_sizing/mesh_coarsening_exponent").execute(*args, **kwargs)
                def feature_angle_refinement(self, *args, **kwargs):
                    """
                    Defines the angular threshold and number of refinement levels for features. This text command is only available when the Boundary Projection treatment is selected through the /mesh/rapid-octree/boundary-treatment text command.
                    """
                    return PyMenu(self.service, "/mesh/rapid_octree/mesh_sizing/feature_angle_refinement").execute(*args, **kwargs)
                def add_surface_sizing(self, *args, **kwargs):
                    """
                    Add a size function definition.
                    """
                    return PyMenu(self.service, "/mesh/rapid_octree/mesh_sizing/add_surface_sizing").execute(*args, **kwargs)
                def change_surface_sizing(self, *args, **kwargs):
                    """
                    Change a size function definition.
                    """
                    return PyMenu(self.service, "/mesh/rapid_octree/mesh_sizing/change_surface_sizing").execute(*args, **kwargs)
                def clear_all_surface_sizings(self, *args, **kwargs):
                    """
                    Delete all size function definitions.
                    """
                    return PyMenu(self.service, "/mesh/rapid_octree/mesh_sizing/clear_all_surface_sizings").execute(*args, **kwargs)
                def list_surface_sizings(self, *args, **kwargs):
                    """
                    List all size function definitions.
                    """
                    return PyMenu(self.service, "/mesh/rapid_octree/mesh_sizing/list_surface_sizings").execute(*args, **kwargs)
                def delete_surface_sizing(self, *args, **kwargs):
                    """
                    Delete a size function definition.
                    """
                    return PyMenu(self.service, "/mesh/rapid_octree/mesh_sizing/delete_surface_sizing").execute(*args, **kwargs)

            class advanced_meshing_options(metaclass=PyMenuMeta):
                """
                Advanced and experimental options for octree mesh generation.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def pseudo_normal_mode(self, *args, **kwargs):
                    """
                    Sets the mode for cumputing projection front sudo normals.
                    """
                    return PyMenu(self.service, "/mesh/rapid_octree/advanced_meshing_options/pseudo_normal_mode").execute(*args, **kwargs)
                def target_cell_orthoskew(self, *args, **kwargs):
                    """
                    Set target orthoskew in mesh (0.0-1.0). Smaller values are likely to increase pullback.
                    """
                    return PyMenu(self.service, "/mesh/rapid_octree/advanced_meshing_options/target_cell_orthoskew").execute(*args, **kwargs)
                def distance_erosion_factor(self, *args, **kwargs):
                    """
                    Set distance erosion factor as a factor of prism edge length.
                    """
                    return PyMenu(self.service, "/mesh/rapid_octree/advanced_meshing_options/distance_erosion_factor").execute(*args, **kwargs)
                def aspect_ratio_skewness_limit(self, *args, **kwargs):
                    """
                    Ignore cells with higher skew in aspect ratio improvement.
                    """
                    return PyMenu(self.service, "/mesh/rapid_octree/advanced_meshing_options/aspect_ratio_skewness_limit").execute(*args, **kwargs)
                def projection_priority_zones(self, *args, **kwargs):
                    """
                    Prioritize zone association of faces crossing multiple boundary zones.
                    """
                    return PyMenu(self.service, "/mesh/rapid_octree/advanced_meshing_options/projection_priority_zones").execute(*args, **kwargs)
                def rename_bounding_box_zones(self, *args, **kwargs):
                    """
                    Set flag to change naming scheme of bounding box surface zones.
                    """
                    return PyMenu(self.service, "/mesh/rapid_octree/advanced_meshing_options/rename_bounding_box_zones").execute(*args, **kwargs)

        class prism(metaclass=PyMenuMeta):
            """
            Enters the prism menu.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
                self.improve = self.__class__.improve(path + [("improve", None)], service)
                self.post_ignore = self.__class__.post_ignore(path + [("post_ignore", None)], service)
                self.split = self.__class__.split(path + [("split", None)], service)
                self.controls = self.__class__.controls(path + [("controls", None)], service)
            def create(self, *args, **kwargs):
                """
                Creates prism layers on one or more boundary face zones based on the offset method, growth method, number of layers, and rate specified.
                """
                return PyMenu(self.service, "/mesh/prism/create").execute(*args, **kwargs)
            def mark_ignore_faces(self, *args, **kwargs):
                """
                Enables you to mark the faces to be ignored during prism meshing.
                """
                return PyMenu(self.service, "/mesh/prism/mark_ignore_faces").execute(*args, **kwargs)
            def mark_nonmanifold_nodes(self, *args, **kwargs):
                """
                Enables you to mark the non-manifold prism base nodes. A list of the non-manifold nodes will be printed in the console. The faces connected to the non-manifold nodes will also be marked. You can use this command after specifying zone-specific prism settings, prior to generating the prisms to verify that non-manifold configurations do not exist.
                """
                return PyMenu(self.service, "/mesh/prism/mark_nonmanifold_nodes").execute(*args, **kwargs)
            def mark_proximity_faces(self, *args, **kwargs):
                """
                Mark prism base faces with certain gap.
                """
                return PyMenu(self.service, "/mesh/prism/mark_proximity_faces").execute(*args, **kwargs)
            def list_parameters(self, *args, **kwargs):
                """
                Shows all prism mesh parameters.
                """
                return PyMenu(self.service, "/mesh/prism/list_parameters").execute(*args, **kwargs)
            def reset_parameters(self, *args, **kwargs):
                """
                Resets all prism parameters.
                """
                return PyMenu(self.service, "/mesh/prism/reset_parameters").execute(*args, **kwargs)
            def quality_method(self, *args, **kwargs):
                """
                Specifies the quality method used during prism generation.
                """
                return PyMenu(self.service, "/mesh/prism/quality_method").execute(*args, **kwargs)

            class improve(metaclass=PyMenuMeta):
                """
                Enters the prism improve menu.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def smooth_prism_cells(self, *args, **kwargs):
                    """
                    Enables optimization based smoothing of prism cells. The nodes of cells with quality worse than the specified threshold value will be moved to improve quality. The cell aspect ratio will also be maintained based on the value specified for max-aspect-ratio.
                    """
                    return PyMenu(self.service, "/mesh/prism/improve/smooth_prism_cells").execute(*args, **kwargs)
                def improve_prism_cells(self, *args, **kwargs):
                    """
                    Collects and smooths cells in layers around poor quality cells. Cells with quality worse than the specified threshold value will be identified, and the nodes of the cells surrounding the poor quality cells will be moved to improve quality.
                    """
                    return PyMenu(self.service, "/mesh/prism/improve/improve_prism_cells").execute(*args, **kwargs)
                def smooth_improve_prism_cells(self, *args, **kwargs):
                    """
                    Uses a combination of node movement and optimized smoothing to improve the quality. This command is a combination of the smooth-prism-cells and improve-prism-cells commands. The cell aspect ratio will also be maintained based on the value specified for max-aspect-ratio.
                    """
                    return PyMenu(self.service, "/mesh/prism/improve/smooth_improve_prism_cells").execute(*args, **kwargs)
                def smooth_sliver_skew(self, *args, **kwargs):
                    """
                    Specifies the skewness above which prism cells will be smoothed.
                    """
                    return PyMenu(self.service, "/mesh/prism/improve/smooth_sliver_skew").execute(*args, **kwargs)
                def smooth_brute_force(self, *args, **kwargs):
                    """
                    Forcibly smooths cells if cell skewness is still high after regular smoothing.
                    """
                    return PyMenu(self.service, "/mesh/prism/improve/smooth_brute_force").execute(*args, **kwargs)
                def smooth_cell_rings(self, *args, **kwargs):
                    """
                    Specifies the number of cell rings around the skewed cell used by improve-prism-cells.
                    """
                    return PyMenu(self.service, "/mesh/prism/improve/smooth_cell_rings").execute(*args, **kwargs)

            class post_ignore(metaclass=PyMenuMeta):
                """
                Contains the following options for ignoring prism cells:
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def mark_prism_cap(self, *args, **kwargs):
                    """
                    Marks the prism cap faces for ignoring prism cells in regions of poor quality cells and sharp corners. Specify the prism cell zone and the basis for ignoring prism cells and the relevant parameters. The prism cells can be ignored based on quality, intersection, (both enabled by default), warp, and features (both disabled by default). Specify the quality measure and threshold value to be used for ignoring cells based on quality and (if applicable) the feature edges for ignoring cells based on features. Additionally, specify whether cells are to be marked in regions of high aspect ratio and based on feature angle, and the additional number of cell rings based on which prism cells will be removed.
                    """
                    return PyMenu(self.service, "/mesh/prism/post_ignore/mark_prism_cap").execute(*args, **kwargs)
                def post_remove_cells(self, *args, **kwargs):
                    """
                    Enables you to remove prism cells in layers around poor quality cells and sharp corners. Specify the prism cell zone, the basis for ignoring prism cells (quality, intersection, warp, features) and the relevant parameters. Specify the number of cell rings to be removed around the marked cells. Cells will be marked for removal in regions of sharp corners based on quality, intersection, warp, and features (as applicable) and then extended based on the number of cell rings specified. Additional cells will be marked for removal in regions of high aspect ratio and based on feature angle (if applicable) around the exposed prism side. The boundary will be smoothed at feature corners after the prism cells have been removed. The prism-side faces exposed by the removal of the prism cells will be collected in a zone named prism-side-#, while for a zone wall-n, the faces corresponding to the ignored prism cells will be collected in a zone named wall-n:ignore. You can also optionally smooth the prism side nodes from the base node to the cap node to create better triangles for the non-conformal interface.
                    """
                    return PyMenu(self.service, "/mesh/prism/post_ignore/post_remove_cells").execute(*args, **kwargs)
                def create_cavity(self, *args, **kwargs):
                    """
                    Creates a cavity in regions where prism quality is adequate, but the quality of adjacent tetrahedra is poor. The cavity is created based on the tetrahedral cell zone, the quality measure and the corresponding threshold value, and the additional number of cell rings specified. You can create a cavity comprising only tetrahedral cells or optionally include prism cells in the cavity created. When prism cells are also included in the cavity, you can specify whether the non-conformal interface is to be created.
                    """
                    return PyMenu(self.service, "/mesh/prism/post_ignore/create_cavity").execute(*args, **kwargs)
                def mark_cavity_prism_cap(self, *args, **kwargs):
                    """
                    Marks the prism cap faces and tetrahedral cell faces bounding the cavity to be created in regions where prism quality is adequate, but the quality of adjacent tetrahedra is poor. Specify the tetrahedral cell zone, the quality measure and the corresponding threshold value to be used, and the additional number of cell rings based on which the cavity will be created.
                    """
                    return PyMenu(self.service, "/mesh/prism/post_ignore/mark_cavity_prism_cap").execute(*args, **kwargs)

            class split(metaclass=PyMenuMeta):
                """
                Contains options for splitting the prism layers after the initial prism layers are generated, to generate the total number of layers required.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def split(self, *args, **kwargs):
                    """
                    Enables you to split the prism layers after the initial prism layers are generated, to generate the total number of layers required. Specify the prism cell zones to be split and the number of divisions per layer. You can also choose to use the existing growth rate (default) or specify the growth rate to be used while splitting the prism layers.
                    """
                    return PyMenu(self.service, "/mesh/prism/split/split").execute(*args, **kwargs)

            class controls(metaclass=PyMenuMeta):
                """
                Enters the prism controls menu.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                    self.morph = self.__class__.morph(path + [("morph", None)], service)
                    self.offset = self.__class__.offset(path + [("offset", None)], service)
                    self.proximity = self.__class__.proximity(path + [("proximity", None)], service)
                    self.normal = self.__class__.normal(path + [("normal", None)], service)
                    self.improve = self.__class__.improve(path + [("improve", None)], service)
                    self.post_ignore = self.__class__.post_ignore(path + [("post_ignore", None)], service)
                    self.adjacent_zone = self.__class__.adjacent_zone(path + [("adjacent_zone", None)], service)
                    self.zone_specific_growth = self.__class__.zone_specific_growth(path + [("zone_specific_growth", None)], service)
                def merge_ignored_threads(self, *args, **kwargs):
                    """
                    Enables you to automatically merge all ignored zones related to a base thread into a single thread. This option is enabled by default. When this option is disabled, more than one ignored thread will be generated per base thread. However, various zones can be created by ignoring this option. They are: 
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/merge_ignored_threads").execute(*args, **kwargs)
                def check_quality(self, *args, **kwargs):
                    """
                    Enables/disables the checking of volume, skewness, and handedness of each new cell and face.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/check_quality").execute(*args, **kwargs)
                def remove_invalid_layer(self, *args, **kwargs):
                    """
                    Removes the last prism layer if it fails in the quality check.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/remove_invalid_layer").execute(*args, **kwargs)
                def set_post_mesh_controls(self, *args, **kwargs):
                    """
                    Sets controls specific to growing prisms post volume mesh generation.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/set_post_mesh_controls").execute(*args, **kwargs)
                def split(self, *args, **kwargs):
                    """
                    Enables you to set parameters for splitting the prism layers after the initial prism layers are generated, to generate the total number of layers required. Specify the number of divisions per layer.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/split").execute(*args, **kwargs)
                def set_overset_prism_controls(self, *args, **kwargs):
                    """
                    Set boundary layer controls for overset mesh generation.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/set_overset_prism_controls").execute(*args, **kwargs)

                class morph(metaclass=PyMenuMeta):
                    """
                    Enters the prism morphing controls menu.
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                    def improve_threshold(self, *args, **kwargs):
                        """
                        Specifies the quality threshold used for improving the quality during the morphing operation.
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/morph/improve_threshold").execute(*args, **kwargs)
                    def morphing_frequency(self, *args, **kwargs):
                        """
                        Specifies the frequency of the morphing operation. The number specified denotes the number of prism layers after which the morpher is applied to the remainder of the mesh (for example, a value of 5 indicates that the morpher is applied to the mesh after every 5 prism layers grown).
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/morph/morphing_frequency").execute(*args, **kwargs)
                    def morphing_convergence_limit(self, *args, **kwargs):
                        """
                        Specifies the convergence limit for the morphing operation. The morpher uses an iterative solver. It is assumed to have converged when the relative residual is less than this number.
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/morph/morphing_convergence_limit").execute(*args, **kwargs)

                class offset(metaclass=PyMenuMeta):
                    """
                    Enters the prism offset controls menu.
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                    def min_aspect_ratio(self, *args, **kwargs):
                        """
                        Specifies the minimum aspect ratio (ratio of prism base length to prism layer height) for the prism cells.
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/offset/min_aspect_ratio").execute(*args, **kwargs)
                    def first_aspect_ratio_min(self, *args, **kwargs):
                        """
                        Specifies the minimum first aspect ratio (ratio of prism base length to prism layer height) for the prism cells. 
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/offset/first_aspect_ratio_min").execute(*args, **kwargs)

                class proximity(metaclass=PyMenuMeta):
                    """
                    Enters the prism proximity controls menu.
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                    def gap_factor(self, *args, **kwargs):
                        """
                        Controls the gap between the intersecting prisms layers in the proximity region with respect to the cell size of the prisms.
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/proximity/gap_factor").execute(*args, **kwargs)
                    def allow_ignore(self, *args, **kwargs):
                        """
                        Enables you to ignore nodes where the specified maximum shrink factor cannot be maintained.
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/proximity/allow_ignore").execute(*args, **kwargs)
                    def max_shrink_factor(self, *args, **kwargs):
                        """
                        Specifies the shrink factor determining the maximum shrinkage of the prism layers. This option is available only when the allow-ignore? option is enabled.
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/proximity/max_shrink_factor").execute(*args, **kwargs)
                    def max_aspect_ratio(self, *args, **kwargs):
                        """
                        Specifies the maximum allowable cell aspect ratio to determine the limit for the shrinkage of prism layers. This option is available only when the allow-ignore? option is disabled.
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/proximity/max_aspect_ratio").execute(*args, **kwargs)
                    def allow_shrinkage(self, *args, **kwargs):
                        """
                        Enables shrinkage while growing prism layers.
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/proximity/allow_shrinkage").execute(*args, **kwargs)
                    def keep_first_layer_offsets(self, *args, **kwargs):
                        """
                        Enables you to retain first layer offsets while performing proximity detection.
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/proximity/keep_first_layer_offsets").execute(*args, **kwargs)

                class normal(metaclass=PyMenuMeta):
                    """
                    Enters the prism normal controls menu.
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                    def ignore_invalid_normals(self, *args, **kwargs):
                        """
                        Enables you to ignore nodes that have poor normals.
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/normal/ignore_invalid_normals").execute(*args, **kwargs)
                    def direction_method(self, *args, **kwargs):
                        """
                        Specifies whether the prism layers should be grown normal to surfaces or along a specified direction vector.
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/normal/direction_method").execute(*args, **kwargs)
                    def orient_mesh_object_face_normals(self, *args, **kwargs):
                        """
                        Enables you to orient the face normals for mesh object boundary zones. Specify the mesh object, region or material point as appropriate, and specify whether walls, baffles or both comprising the prism base zones are to be separated and oriented.
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/normal/orient_mesh_object_face_normals").execute(*args, **kwargs)
                    def compute_normal(self, *args, **kwargs):
                        """
                        Computes the normal for the specified face zone.
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/normal/compute_normal").execute(*args, **kwargs)
                    def direction_vector(self, *args, **kwargs):
                        """
                        Specifies the direction vector for prism extrusion when the uniform method is selected for direction-method.
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/normal/direction_vector").execute(*args, **kwargs)
                    def bisect_angle(self, *args, **kwargs):
                        """
                        Is required for growing prisms out of sharp interior corners. When the value of this angle is set, the normals are automatically projected onto the plane bisecting the angle between faces having an interior angle less than this angle.
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/normal/bisect_angle").execute(*args, **kwargs)
                    def max_angle_change(self, *args, **kwargs):
                        """
                        Specifies the maximum angle by which the normal direction at a node can change during smoothing.
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/normal/max_angle_change").execute(*args, **kwargs)
                    def orthogonal_layers(self, *args, **kwargs):
                        """
                        Specifies the number of layers to preserve orthogonality. All smoothing is deferred until after these layers.
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/normal/orthogonal_layers").execute(*args, **kwargs)

                class improve(metaclass=PyMenuMeta):
                    """
                    Enters the prism smoothing controls menu.
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                    def edge_swap_base_angle(self, *args, **kwargs):
                        """
                        Specifies the maximum allowable angle between the normals of the base faces for skewness-driven edge swapping.
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/improve/edge_swap_base_angle").execute(*args, **kwargs)
                    def edge_swap_cap_angle(self, *args, **kwargs):
                        """
                        Specifies the maximum allowable angle between the normals of the cap faces for skewness-driven edge swapping.
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/improve/edge_swap_cap_angle").execute(*args, **kwargs)
                    def max_allowable_cap_skew(self, *args, **kwargs):
                        """
                        Specifies the maximum skewness allowed for a prism cap face. If the skewness of a cap face exceeds this value, the meshing process will stop and a warning indicates that the skewness for that layer is too high.
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/improve/max_allowable_cap_skew").execute(*args, **kwargs)
                    def max_allowable_cell_skew(self, *args, **kwargs):
                        """
                        Specifies the cell quality criteria for smoothing and quality checking.
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/improve/max_allowable_cell_skew").execute(*args, **kwargs)
                    def corner_height_weight(self, *args, **kwargs):
                        """
                        When enabled, the offset height at corners with large angles (for example, 270º) is reduced to give a smoother prism cap.
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/improve/corner_height_weight").execute(*args, **kwargs)
                    def improve_warp(self, *args, **kwargs):
                        """
                        Enables or disables improving of face warp during prism generation. This option is disabled by default.
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/improve/improve_warp").execute(*args, **kwargs)
                    def face_smooth_skew(self, *args, **kwargs):
                        """
                        Min. skewness to smooth cap faces.
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/improve/face_smooth_skew").execute(*args, **kwargs)
                    def check_allowable_skew(self, *args, **kwargs):
                        """
                        Enables you to check the skewness of the prism cap for every layer.
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/improve/check_allowable_skew").execute(*args, **kwargs)
                    def left_hand_check(self, *args, **kwargs):
                        """
                        Controls checking for left-handedness of faces. The default setting of 0 implies face handedness will not be checked. A value of 1 implies only cap faces will be checked, while 2 implies faces of all cells in current layer will be checked.
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/improve/left_hand_check").execute(*args, **kwargs)
                    def smooth_improve_prism_cells(self, *args, **kwargs):
                        """
                        Enables you to set the parameters for improving the prism cells after the required prism layers are created. You can select optimized smoothing (smooth), node movement (improve), or a combination of both to improve the quality. Specify the quality measure to be used, the cell quality threshold, the number of improvement iterations, and the minimum improvement required.
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/improve/smooth_improve_prism_cells").execute(*args, **kwargs)

                class post_ignore(metaclass=PyMenuMeta):
                    """
                    Contains options for setting the parameters for removing poor quality prism cells after the required prism layers are created.
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                    def post_remove_cells(self, *args, **kwargs):
                        """
                        Enables you to set the parameters for removing poor quality prism cells after the required prism layers are created. You can remove cells based on quality, intersection, interior warp, and feature edges. Specify options for removing additional cells in regions of high aspect ratio and feature angle, the number of cell rings to be removed around the marked cells, and options for smoothing the prism boundary and prism side height.
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/post_ignore/post_remove_cells").execute(*args, **kwargs)

                class adjacent_zone(metaclass=PyMenuMeta):
                    """
                    Enters the prism adjacent zone controls menu.
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                    def side_feature_angle(self, *args, **kwargs):
                        """
                        Specifies the angle used for computing the feature normals.
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/adjacent_zone/side_feature_angle").execute(*args, **kwargs)
                    def project_adjacent_angle(self, *args, **kwargs):
                        """
                        Determines whether or not to project to an adjacent zone. If a zone shares outer nodes with any of the zones from which the layers are being grown (the “base zones”), its angle with respect to the growth direction is compared with this value. If the angle is less than or equal to this value, then the zone will be projected to. The default value is 75 degrees. See  for details.
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/adjacent_zone/project_adjacent_angle").execute(*args, **kwargs)

                class zone_specific_growth(metaclass=PyMenuMeta):
                    """
                    Enters the prism growth controls menu.
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                    def apply_growth(self, *args, **kwargs):
                        """
                        Applies the zone-specific growth parameters specified.
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/zone_specific_growth/apply_growth").execute(*args, **kwargs)
                    def clear_growth(self, *args, **kwargs):
                        """
                        Clears the zone-specific growth specified.
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/zone_specific_growth/clear_growth").execute(*args, **kwargs)
                    def list_growth(self, *args, **kwargs):
                        """
                        Lists the zone-specific growth parameters specified for individual zones in the console.
                        """
                        return PyMenu(self.service, "/mesh/prism/controls/zone_specific_growth/list_growth").execute(*args, **kwargs)

        class pyramid(metaclass=PyMenuMeta):
            """
            Enters the pyramid menu.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
                self.controls = self.__class__.controls(path + [("controls", None)], service)
            def create(self, *args, **kwargs):
                """
                Creates a layer of pyramids on the quad face zone.
                """
                return PyMenu(self.service, "/mesh/pyramid/create").execute(*args, **kwargs)

            class controls(metaclass=PyMenuMeta):
                """
                Enters the pyramid controls menu.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def neighbor_angle(self, *args, **kwargs):
                    """
                    Sets the threshold dihedral angle used to limit the neighboring faces considered for pyramid creation. For example, if the value is set to 110° and the angle between a given quadrilateral face and a neighboring triangular face is greater than 110°, the resulting pyramid will not include the triangular face.
                    """
                    return PyMenu(self.service, "/mesh/pyramid/controls/neighbor_angle").execute(*args, **kwargs)
                def offset_scaling(self, *args, **kwargs):
                    """
                    Specifies the scaling, to be used to determine the height of the pyramid.
                    """
                    return PyMenu(self.service, "/mesh/pyramid/controls/offset_scaling").execute(*args, **kwargs)
                def vertex_method(self, *args, **kwargs):
                    """
                    Specifies the method by which the location of the new vertex of the pyramid will be determined. The skewness method is used by default.
                    """
                    return PyMenu(self.service, "/mesh/pyramid/controls/vertex_method").execute(*args, **kwargs)
                def offset_factor(self, *args, **kwargs):
                    """
                    Specifies the fraction of the computed pyramid height (offset) by which the pyramid heights will be randomly adjusted. The default value is 0, indicating that all pyramids will have the exact height computed. A value of 0.1, for example, will limit each adjustment to ±10percentage of the computed height.
                    """
                    return PyMenu(self.service, "/mesh/pyramid/controls/offset_factor").execute(*args, **kwargs)

        class thin_volume_mesh(metaclass=PyMenuMeta):
            """
            Creates a sweep-like mesh for a body occupying a thin gap. You define source and target boundary faces zones (the source face normal should point to the target). The source face mesh may be triangles or quads.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def create(self, *args, **kwargs):
                """
                Initiates the dialog box to specify source and target faces and specify the following parameters
                """
                return PyMenu(self.service, "/mesh/thin_volume_mesh/create").execute(*args, **kwargs)

        class separate(metaclass=PyMenuMeta):
            """
            Separates cells by various user-defined methods.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
                self.local_regions = self.__class__.local_regions(path + [("local_regions", None)], service)
            def separate_cell_by_face(self, *args, **kwargs):
                """
                Separates cells that are connected to a specified face zone into another cell zone. This separation method applies only to prism cells.
                """
                return PyMenu(self.service, "/mesh/separate/separate_cell_by_face").execute(*args, **kwargs)
            def separate_cell_by_mark(self, *args, **kwargs):
                """
                Separates cells within a specified local region into another cell zone.
                """
                return PyMenu(self.service, "/mesh/separate/separate_cell_by_mark").execute(*args, **kwargs)
            def separate_prisms_from_poly(self, *args, **kwargs):
                """
                Separates the poly-prism cells from the poly cells within your mesh. Available only when the report/enhanced-orthogonal-quality? flag is set to  yes, and is only supported for the .h5 format.
                """
                return PyMenu(self.service, "/mesh/separate/separate_prisms_from_poly").execute(*args, **kwargs)
            def separate_cell_by_region(self, *args, **kwargs):
                """
                Separates contiguous regions within a cell zone into separate cell zones.
                """
                return PyMenu(self.service, "/mesh/separate/separate_cell_by_region").execute(*args, **kwargs)
            def separate_cell_by_shape(self, *args, **kwargs):
                """
                Separates cells with different shapes (pyramids, tetrahedra, etc.) into separate cell zones.
                """
                return PyMenu(self.service, "/mesh/separate/separate_cell_by_shape").execute(*args, **kwargs)
            def separate_cell_by_skew(self, *args, **kwargs):
                """
                Separates cells based on the specified cell skewness.
                """
                return PyMenu(self.service, "/mesh/separate/separate_cell_by_skew").execute(*args, **kwargs)
            def separate_cell_by_size(self, *args, **kwargs):
                """
                Separates cells based on the specified minimum and maximum cell sizes.
                """
                return PyMenu(self.service, "/mesh/separate/separate_cell_by_size").execute(*args, **kwargs)

            class local_regions(metaclass=PyMenuMeta):
                """
                Enters the local refinement menu.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def define(self, *args, **kwargs):
                    """
                    Enables you to define the parameters for the refinement region.
                    """
                    return PyMenu(self.service, "/mesh/separate/local_regions/define").execute(*args, **kwargs)
                def delete(self, *args, **kwargs):
                    """
                    Enables you to delete a refinement region.
                    """
                    return PyMenu(self.service, "/mesh/separate/local_regions/delete").execute(*args, **kwargs)
                def init(self, *args, **kwargs):
                    """
                    Deletes all current regions and adds the default refinement region.
                    """
                    return PyMenu(self.service, "/mesh/separate/local_regions/init").execute(*args, **kwargs)
                def list_all_regions(self, *args, **kwargs):
                    """
                    Lists all the refinement regions.
                    """
                    return PyMenu(self.service, "/mesh/separate/local_regions/list_all_regions").execute(*args, **kwargs)

        class tet(metaclass=PyMenuMeta):
            """
            Enters the tetrahedral mesh menu.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
                self.controls = self.__class__.controls(path + [("controls", None)], service)
                self.improve = self.__class__.improve(path + [("improve", None)], service)
                self.local_regions = self.__class__.local_regions(path + [("local_regions", None)], service)
            def delete_virtual_cells(self, *args, **kwargs):
                """
                Deletes virtual cells created due to the use of the  keep-virtual-entities? option.
                """
                return PyMenu(self.service, "/mesh/tet/delete_virtual_cells").execute(*args, **kwargs)
            def init(self, *args, **kwargs):
                """
                Generates the initial Delaunay mesh by meshing the boundary nodes.
                """
                return PyMenu(self.service, "/mesh/tet/init").execute(*args, **kwargs)
            def init_refine(self, *args, **kwargs):
                """
                Generates the tetrahedral mesh.
                """
                return PyMenu(self.service, "/mesh/tet/init_refine").execute(*args, **kwargs)
            def mesh_object(self, *args, **kwargs):
                """
                Tet mesh object of type mesh.
                """
                return PyMenu(self.service, "/mesh/tet/mesh_object").execute(*args, **kwargs)
            def preserve_cell_zone(self, *args, **kwargs):
                """
                Allows you to specify the cell zones to be preserved during the meshing process.
                """
                return PyMenu(self.service, "/mesh/tet/preserve_cell_zone").execute(*args, **kwargs)
            def un_preserve_cell_zone(self, *args, **kwargs):
                """
                Un-preserve cell zone.
                """
                return PyMenu(self.service, "/mesh/tet/un_preserve_cell_zone").execute(*args, **kwargs)
            def refine(self, *args, **kwargs):
                """
                Refines the initialized mesh.
                """
                return PyMenu(self.service, "/mesh/tet/refine").execute(*args, **kwargs)
            def trace_path_between_cells(self, *args, **kwargs):
                """
                Detects holes in the geometry by tracing the path between the two specified cells 
                """
                return PyMenu(self.service, "/mesh/tet/trace_path_between_cells").execute(*args, **kwargs)

            class controls(metaclass=PyMenuMeta):
                """
                Enters the tet controls menu.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                    self.improve_mesh = self.__class__.improve_mesh(path + [("improve_mesh", None)], service)
                    self.adv_front_method = self.__class__.adv_front_method(path + [("adv_front_method", None)], service)
                    self.remove_slivers = self.__class__.remove_slivers(path + [("remove_slivers", None)], service)
                    self.tet_improve = self.__class__.tet_improve(path + [("tet_improve", None)], service)
                def cell_sizing(self, *args, **kwargs):
                    """
                    Specifies the cell sizing function for refinement. You can select geometric, linear, none, or size-field as appropriate.
                    """
                    return PyMenu(self.service, "/mesh/tet/controls/cell_sizing").execute(*args, **kwargs)
                def set_zone_growth_rate(self, *args, **kwargs):
                    """
                    Set zone specific geometric growth rates.
                    """
                    return PyMenu(self.service, "/mesh/tet/controls/set_zone_growth_rate").execute(*args, **kwargs)
                def clear_zone_growth_rate(self, *args, **kwargs):
                    """
                    Clear zone specific geometric growth rates.
                    """
                    return PyMenu(self.service, "/mesh/tet/controls/clear_zone_growth_rate").execute(*args, **kwargs)
                def compute_max_cell_volume(self, *args, **kwargs):
                    """
                    Computes the maximum cell volume for the current mesh.
                    """
                    return PyMenu(self.service, "/mesh/tet/controls/compute_max_cell_volume").execute(*args, **kwargs)
                def delete_dead_zones(self, *args, **kwargs):
                    """
                    Specifies the maximum allowable cell volume.
                    """
                    return PyMenu(self.service, "/mesh/tet/controls/delete_dead_zones").execute(*args, **kwargs)
                def max_cell_length(self, *args, **kwargs):
                    """
                    Specifies the maximum allowable cell length.
                    """
                    return PyMenu(self.service, "/mesh/tet/controls/max_cell_length").execute(*args, **kwargs)
                def max_cell_volume(self, *args, **kwargs):
                    """
                    Specifies the maximum allowable cell volume.
                    """
                    return PyMenu(self.service, "/mesh/tet/controls/max_cell_volume").execute(*args, **kwargs)
                def use_max_cell_size(self, *args, **kwargs):
                    """
                    Enables you to use the maximum cell size specified instead of recomputing the value based on the objects, when the volume mesh is generated. This option is disabled by default.
                    """
                    return PyMenu(self.service, "/mesh/tet/controls/use_max_cell_size").execute(*args, **kwargs)
                def non_fluid_type(self, *args, **kwargs):
                    """
                    Selects the non-fluid cell zone type. After the mesh is initialized, any non-fluid zones will be set to this type. If the mesh includes multiple regions (for example, the problem for which you are creating the mesh includes a fluid zone and one or more solid zones), and you plan to refine all of them using the same refinement parameters, modify the non-fluid type before generating the mesh.  For zone-based meshing, if any cell zone has at least one boundary zone type as inlet, it will automatically be set to fluid type. For object based meshing, volume region type is used to determine the cell zone type.
                    """
                    return PyMenu(self.service, "/mesh/tet/controls/non_fluid_type").execute(*args, **kwargs)
                def refine_method(self, *args, **kwargs):
                    """
                    Enables you to select the refinement method. You can select either skewness-based refinement or the advancing front method.  The skewness-based refinement option is no longer supported and will be removed at a future release. 
                    """
                    return PyMenu(self.service, "/mesh/tet/controls/refine_method").execute(*args, **kwargs)
                def set_region_based_sizing(self, *args, **kwargs):
                    """
                    Allows you to specify local sizing settings (max cell length) for specified region(s)
                    """
                    return PyMenu(self.service, "/mesh/tet/controls/set_region_based_sizing").execute(*args, **kwargs)
                def print_region_based_sizing(self, *args, **kwargs):
                    """
                    Displays local sizing settings (max cell length) for specified region(s).
                    """
                    return PyMenu(self.service, "/mesh/tet/controls/print_region_based_sizing").execute(*args, **kwargs)
                def skewness_method(self, *args, **kwargs):
                    """
                    Enters the skewness refinement controls menu.
                    """
                    return PyMenu(self.service, "/mesh/tet/controls/skewness_method").execute(*args, **kwargs)

                class improve_mesh(metaclass=PyMenuMeta):
                    """
                    Enters the improve mesh controls menu.
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                    def improve(self, *args, **kwargs):
                        """
                        Automatically improves the mesh.
                        """
                        return PyMenu(self.service, "/mesh/tet/controls/improve_mesh/improve").execute(*args, **kwargs)
                    def swap(self, *args, **kwargs):
                        """
                        Enables you to specify the face swap parameters.
                        """
                        return PyMenu(self.service, "/mesh/tet/controls/improve_mesh/swap").execute(*args, **kwargs)
                    def skewness_smooth(self, *args, **kwargs):
                        """
                        Enables you to specify the skewness smooth parameters.
                        """
                        return PyMenu(self.service, "/mesh/tet/controls/improve_mesh/skewness_smooth").execute(*args, **kwargs)
                    def laplace_smooth(self, *args, **kwargs):
                        """
                        Enables you to specify the Laplace smoothing parameters.
                        """
                        return PyMenu(self.service, "/mesh/tet/controls/improve_mesh/laplace_smooth").execute(*args, **kwargs)

                class adv_front_method(metaclass=PyMenuMeta):
                    """
                    Enters the advancing front refinement controls menu.
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                        self.skew_improve = self.__class__.skew_improve(path + [("skew_improve", None)], service)
                    def refine_parameters(self, *args, **kwargs):
                        """
                        Defines the cell zone improvement parameters for the advancing front method.
                        """
                        return PyMenu(self.service, "/mesh/tet/controls/adv_front_method/refine_parameters").execute(*args, **kwargs)
                    def first_improve_params(self, *args, **kwargs):
                        """
                        Defines the refining front improvement parameters for the advancing front method.
                        """
                        return PyMenu(self.service, "/mesh/tet/controls/adv_front_method/first_improve_params").execute(*args, **kwargs)
                    def second_improve_params(self, *args, **kwargs):
                        """
                        Defines the cell zone improvement parameters for the advancing front method.
                        """
                        return PyMenu(self.service, "/mesh/tet/controls/adv_front_method/second_improve_params").execute(*args, **kwargs)

                    class skew_improve(metaclass=PyMenuMeta):
                        """
                        Enters the refine improve controls menu.
                        """
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service
                        def boundary_sliver_skew(self, *args, **kwargs):
                            """
                            Specifies the boundary sliver skewness for the advancing front method. This  parameter is used for removing sliver cells along the boundary.
                            """
                            return PyMenu(self.service, "/mesh/tet/controls/adv_front_method/skew_improve/boundary_sliver_skew").execute(*args, **kwargs)
                        def sliver_skew(self, *args, **kwargs):
                            """
                            Specifies the sliver skewness for the advancing front method. This parameter  is used for removing sliver cells in the interior.
                            """
                            return PyMenu(self.service, "/mesh/tet/controls/adv_front_method/skew_improve/sliver_skew").execute(*args, **kwargs)
                        def target(self, *args, **kwargs):
                            """
                            Enables you to enable targeted skewness-based refinement for the advancing  front method. This option enables you to improve the mesh until the targeted  skewness value is achieved.
                            """
                            return PyMenu(self.service, "/mesh/tet/controls/adv_front_method/skew_improve/target").execute(*args, **kwargs)
                        def target_skew(self, *args, **kwargs):
                            """
                            Specifies the targeted skewness during improvement for the advancing front  method.
                            """
                            return PyMenu(self.service, "/mesh/tet/controls/adv_front_method/skew_improve/target_skew").execute(*args, **kwargs)
                        def target_low_skew(self, *args, **kwargs):
                            """
                            Specifies the targeted skewness threshold above which cells will be improved.  The improve operation will attempt to improve cells with skewness above the target-low-skew value specified, but there will be no  attempt to reduce the skewness below the specified value. A limited set of improve  operations will be used as compared to the operations required for the target-skew value-based improvement. The value specified  could be approximately 0.1 lower than the target-skew  value.
                            """
                            return PyMenu(self.service, "/mesh/tet/controls/adv_front_method/skew_improve/target_low_skew").execute(*args, **kwargs)
                        def attempts(self, *args, **kwargs):
                            """
                            Specifies the number of overall improvement attempts for the advancing front  method.
                            """
                            return PyMenu(self.service, "/mesh/tet/controls/adv_front_method/skew_improve/attempts").execute(*args, **kwargs)
                        def iterations(self, *args, **kwargs):
                            """
                            Specifies the number of improvement iterations in each attempt for the  advancing front method.
                            """
                            return PyMenu(self.service, "/mesh/tet/controls/adv_front_method/skew_improve/iterations").execute(*args, **kwargs)

                class remove_slivers(metaclass=PyMenuMeta):
                    """
                    Enters the sliver remove controls menu.
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                    def remove(self, *args, **kwargs):
                        """
                        Enables/disables the automatic removal of slivers.
                        """
                        return PyMenu(self.service, "/mesh/tet/controls/remove_slivers/remove").execute(*args, **kwargs)
                    def skew(self, *args, **kwargs):
                        """
                        Specifies the skewness threshold for sliver removal.
                        """
                        return PyMenu(self.service, "/mesh/tet/controls/remove_slivers/skew").execute(*args, **kwargs)
                    def low_skew(self, *args, **kwargs):
                        """
                        Specifies the targeted skewness threshold above which cells will be improved. The improve operation will attempt to improve cells with skewness above the low-skew value specified, but there will be no attempt to reduce the skewness below the specified value. A limited set of improve operations will be used as compared to the operations required for the skew value-based improvement.
                        """
                        return PyMenu(self.service, "/mesh/tet/controls/remove_slivers/low_skew").execute(*args, **kwargs)
                    def angle(self, *args, **kwargs):
                        """
                        Specifies the maximum dihedral angle for considering the cell to be a sliver 
                        """
                        return PyMenu(self.service, "/mesh/tet/controls/remove_slivers/angle").execute(*args, **kwargs)
                    def attempts(self, *args, **kwargs):
                        """
                        Specifies the number of attempts overall to remove slivers.
                        """
                        return PyMenu(self.service, "/mesh/tet/controls/remove_slivers/attempts").execute(*args, **kwargs)
                    def iterations(self, *args, **kwargs):
                        """
                        Specifies the number of iterations to be performed for the specific sliver removal operation.
                        """
                        return PyMenu(self.service, "/mesh/tet/controls/remove_slivers/iterations").execute(*args, **kwargs)
                    def method(self, *args, **kwargs):
                        """
                        Enables you to select the method for sliver removal. The default method used is the fast method. The fast and the aggressive methods use the same controls and give similar results for good quality surface meshes. In case of poor surface meshes, the aggressive method will typically succeed in improving the mesh to a greater extent, but it may be slower than the fast method.
                        """
                        return PyMenu(self.service, "/mesh/tet/controls/remove_slivers/method").execute(*args, **kwargs)

                class tet_improve(metaclass=PyMenuMeta):
                    """
                    Improve cells controls.
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                    def skew(self, *args, **kwargs):
                        """
                        Remove skew.
                        """
                        return PyMenu(self.service, "/mesh/tet/controls/tet_improve/skew").execute(*args, **kwargs)
                    def angle(self, *args, **kwargs):
                        """
                        Max dihedral angle defining a valid boundary cell.
                        """
                        return PyMenu(self.service, "/mesh/tet/controls/tet_improve/angle").execute(*args, **kwargs)
                    def attempts(self, *args, **kwargs):
                        """
                        Improve attempts.
                        """
                        return PyMenu(self.service, "/mesh/tet/controls/tet_improve/attempts").execute(*args, **kwargs)
                    def iterations(self, *args, **kwargs):
                        """
                        Improve iterations.
                        """
                        return PyMenu(self.service, "/mesh/tet/controls/tet_improve/iterations").execute(*args, **kwargs)

            class improve(metaclass=PyMenuMeta):
                """
                Enters the tet improve menu.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def swap_faces(self, *args, **kwargs):
                    """
                    Performs interior face swapping to improve cell skewness.
                    """
                    return PyMenu(self.service, "/mesh/tet/improve/swap_faces").execute(*args, **kwargs)
                def refine_slivers(self, *args, **kwargs):
                    """
                    Attempts to remove the sliver by placing a node at or near the centroid of the sliver cell. Swapping and smoothing are performed to improve the skewness. You can also specify whether boundary cells are to be refined. Refining the boundary cells may enable you to carry out further improvement options such as smoothing, swapping, and collapsing slivers.
                    """
                    return PyMenu(self.service, "/mesh/tet/improve/refine_slivers").execute(*args, **kwargs)
                def sliver_boundary_swap(self, *args, **kwargs):
                    """
                    Removes boundary slivers by moving the boundary to exclude the cells from the zone.
                    """
                    return PyMenu(self.service, "/mesh/tet/improve/sliver_boundary_swap").execute(*args, **kwargs)
                def refine_boundary_slivers(self, *args, **kwargs):
                    """
                    Attempts to increase the volume of boundary slivers to create a valid tet cell. Tetrahedra having one or two faces on the boundary are identified and then the appropriate edge split. The split node is then smoothed such that the volume of the tetrahedron increases, thereby creating a valid tet cell.
                    """
                    return PyMenu(self.service, "/mesh/tet/improve/refine_boundary_slivers").execute(*args, **kwargs)
                def collapse_slivers(self, *args, **kwargs):
                    """
                    Attempts to collapse the nodes of a skewed sliver cell on any one of its neighbors.
                    """
                    return PyMenu(self.service, "/mesh/tet/improve/collapse_slivers").execute(*args, **kwargs)
                def improve_cells(self, *args, **kwargs):
                    """
                    Improves skewed tetrahedral cells.
                    """
                    return PyMenu(self.service, "/mesh/tet/improve/improve_cells").execute(*args, **kwargs)
                def smooth_boundary_sliver(self, *args, **kwargs):
                    """
                    Smooths nodes on sliver cells having all four nodes on the boundary until the skewness value is less than the specified value. The default values for the skewness threshold, minimum dihedral angle between boundary faces, and feature angle are 0.985, 10, and 30, respectively.
                    """
                    return PyMenu(self.service, "/mesh/tet/improve/smooth_boundary_sliver").execute(*args, **kwargs)
                def smooth_interior_sliver(self, *args, **kwargs):
                    """
                    Smooths non-boundary nodes on sliver cells having skewness greater than the specified threshold value. The default value for the skewness threshold is 0.985.
                    """
                    return PyMenu(self.service, "/mesh/tet/improve/smooth_interior_sliver").execute(*args, **kwargs)
                def smooth_nodes(self, *args, **kwargs):
                    """
                    Enables you to apply either Laplacian or variational smoothing to nodes on the tetrahedral cell zones to improve the mesh quality.
                    """
                    return PyMenu(self.service, "/mesh/tet/improve/smooth_nodes").execute(*args, **kwargs)
                def skew_smooth_nodes(self, *args, **kwargs):
                    """
                    Applies skewness-based smoothing to nodes on the tetrahedral cell zones to improve the mesh quality.
                    """
                    return PyMenu(self.service, "/mesh/tet/improve/skew_smooth_nodes").execute(*args, **kwargs)

            class local_regions(metaclass=PyMenuMeta):
                """
                Enters the local refinement menu.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def activate(self, *args, **kwargs):
                    """
                    Activates the specified regions for refinement.
                    """
                    return PyMenu(self.service, "/mesh/tet/local_regions/activate").execute(*args, **kwargs)
                def deactivate(self, *args, **kwargs):
                    """
                    Deactivates the specified regions for refinement.
                    """
                    return PyMenu(self.service, "/mesh/tet/local_regions/deactivate").execute(*args, **kwargs)
                def define(self, *args, **kwargs):
                    """
                    Defines the refinement region according to the specified parameters.
                    """
                    return PyMenu(self.service, "/mesh/tet/local_regions/define").execute(*args, **kwargs)
                def delete(self, *args, **kwargs):
                    """
                    Deletes the specified refinement region.
                    """
                    return PyMenu(self.service, "/mesh/tet/local_regions/delete").execute(*args, **kwargs)
                def init(self, *args, **kwargs):
                    """
                    Defines the default refinement region encompassing the entire geometry.
                    """
                    return PyMenu(self.service, "/mesh/tet/local_regions/init").execute(*args, **kwargs)
                def list_all_regions(self, *args, **kwargs):
                    """
                    Lists all refinement region parameters and the activated regions in the console.
                    """
                    return PyMenu(self.service, "/mesh/tet/local_regions/list_all_regions").execute(*args, **kwargs)
                def refine(self, *args, **kwargs):
                    """
                    Refines the active cells inside the selected region based on the specified refinement parameters.
                    """
                    return PyMenu(self.service, "/mesh/tet/local_regions/refine").execute(*args, **kwargs)
                def ideal_vol(self, *args, **kwargs):
                    """
                    Reports the volume of an ideal tetrahedron for the edge length specified.
                    """
                    return PyMenu(self.service, "/mesh/tet/local_regions/ideal_vol").execute(*args, **kwargs)
                def ideal_area(self, *args, **kwargs):
                    """
                    Ideal triangle area for given edge length.
                    """
                    return PyMenu(self.service, "/mesh/tet/local_regions/ideal_area").execute(*args, **kwargs)

        class manage(metaclass=PyMenuMeta):
            """
            Enters the manage cell zones menu.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def adjacent_face_zones(self, *args, **kwargs):
                """
                Lists all face zones that refer to the specified cell zone.
                """
                return PyMenu(self.service, "/mesh/manage/adjacent_face_zones").execute(*args, **kwargs)
            def auto_set_active(self, *args, **kwargs):
                """
                Sets the active zones based on points that are defined in an external file. For each zone you want to activate, you need to specify the coordinates of a point in the zone, the zone type (for example, fluid), and (optionally) a new name. A sample file is shown below: 
                """
                return PyMenu(self.service, "/mesh/manage/auto_set_active").execute(*args, **kwargs)
            def active_list(self, *args, **kwargs):
                """
                Lists all active zones.
                """
                return PyMenu(self.service, "/mesh/manage/active_list").execute(*args, **kwargs)
            def copy(self, *args, **kwargs):
                """
                Copies all nodes and faces of specified cell zones.
                """
                return PyMenu(self.service, "/mesh/manage/copy").execute(*args, **kwargs)
            def change_prefix(self, *args, **kwargs):
                """
                Enables you to change the prefix for the cell zone.
                """
                return PyMenu(self.service, "/mesh/manage/change_prefix").execute(*args, **kwargs)
            def change_suffix(self, *args, **kwargs):
                """
                Change the suffix for specified face zones.
                """
                return PyMenu(self.service, "/mesh/manage/change_suffix").execute(*args, **kwargs)
            def delete(self, *args, **kwargs):
                """
                Deletes a cell zone, along with its associated nodes and faces. When deleting cell zones that contain poly cells, you will be warned that the original mesh needs to be deleted and the original faces restored prior to remeshing the volumetric region.
                """
                return PyMenu(self.service, "/mesh/manage/delete").execute(*args, **kwargs)
            def id(self, *args, **kwargs):
                """
                Specifies a new cell zone ID. If a conflict is detected, the change will be ignored.
                """
                return PyMenu(self.service, "/mesh/manage/id").execute(*args, **kwargs)
            def list(self, *args, **kwargs):
                """
                Prints information on all cell zones.
                """
                return PyMenu(self.service, "/mesh/manage/list").execute(*args, **kwargs)
            def merge(self, *args, **kwargs):
                """
                Merges two or more cell zones.  For object-based merge, the selected zones must be in the same volumetric region. If  not, you will have to merge the volumetric regions first using /objects/volumetric-regions/merge. If the volumetric regions  cannot be merged because they are not contiguous, you will have to delete the object(s)  only before merging the cell zones.
                """
                return PyMenu(self.service, "/mesh/manage/merge").execute(*args, **kwargs)
            def name(self, *args, **kwargs):
                """
                Enables you to rename a cell zone.
                """
                return PyMenu(self.service, "/mesh/manage/name").execute(*args, **kwargs)
            def origin(self, *args, **kwargs):
                """
                Specifies a new origin for the mesh, to be used for cell zone rotation. The default origin is (0,0,0).
                """
                return PyMenu(self.service, "/mesh/manage/origin").execute(*args, **kwargs)
            def rotate(self, *args, **kwargs):
                """
                Rotates all nodes of specified cell zones by a specified angle.
                """
                return PyMenu(self.service, "/mesh/manage/rotate").execute(*args, **kwargs)
            def rotate_model(self, *args, **kwargs):
                """
                Rotates all nodes of the model by a specified angle.
                """
                return PyMenu(self.service, "/mesh/manage/rotate_model").execute(*args, **kwargs)
            def revolve_face_zone(self, *args, **kwargs):
                """
                Generates cells by revolving a face thread.
                """
                return PyMenu(self.service, "/mesh/manage/revolve_face_zone").execute(*args, **kwargs)
            def scale(self, *args, **kwargs):
                """
                Scales all nodes of specified cell zones by a specified factor.
                """
                return PyMenu(self.service, "/mesh/manage/scale").execute(*args, **kwargs)
            def scale_model(self, *args, **kwargs):
                """
                Scales all nodes of the model by a specified factor.
                """
                return PyMenu(self.service, "/mesh/manage/scale_model").execute(*args, **kwargs)
            def set_active(self, *args, **kwargs):
                """
                Sets the specified cell zones to be active.
                """
                return PyMenu(self.service, "/mesh/manage/set_active").execute(*args, **kwargs)
            def translate(self, *args, **kwargs):
                """
                Translates all nodes of specified cell zones by a specified vector.
                """
                return PyMenu(self.service, "/mesh/manage/translate").execute(*args, **kwargs)
            def translate_model(self, *args, **kwargs):
                """
                Translates all nodes of the model by a specified vector.
                """
                return PyMenu(self.service, "/mesh/manage/translate_model").execute(*args, **kwargs)
            def type(self, *args, **kwargs):
                """
                Changes the type and name of a cell zone.
                """
                return PyMenu(self.service, "/mesh/manage/type").execute(*args, **kwargs)
            def merge_dead_zones(self, *args, **kwargs):
                """
                Enables you to merge dead zones having a cell count lower than the specified threshold value, with the adjacent cell zone. The result of the merge operation is determined by the type of the adjacent cell zone and the shared face area. The priority for merging with the adjacent cell zone based on type is fluid > solid > dead (that is, merging with an adjacent fluid zone takes priority over merging with an adjacent solid zone, which in turn takes priority over merging with a dead zone). Also, if the adjacent zones are of the same type (for example, fluid), the zone will be merged with the zone having the largest shared face area.
                """
                return PyMenu(self.service, "/mesh/manage/merge_dead_zones").execute(*args, **kwargs)
            def get_material_point(self, *args, **kwargs):
                """
                Prints the coordinates of the material point for the specified cell zone.  If the cell zone is non-contiguous, the get-material-point  command will print a list of material points, one for each contiguous region.
                """
                return PyMenu(self.service, "/mesh/manage/get_material_point").execute(*args, **kwargs)

        class cell_zone_conditions(metaclass=PyMenuMeta):
            """
            Contains options for copying or clearing cell zone conditions when a case file is read.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def copy(self, *args, **kwargs):
                """
                Enables you to copy the cell zone conditions from the zone selected to the zones specified.
                """
                return PyMenu(self.service, "/mesh/cell_zone_conditions/copy").execute(*args, **kwargs)
            def clear(self, *args, **kwargs):
                """
                Clears the cell zone conditions assigned to the specified zones.
                """
                return PyMenu(self.service, "/mesh/cell_zone_conditions/clear").execute(*args, **kwargs)
            def clear_all(self, *args, **kwargs):
                """
                Clears the cell conditions assigned to all the zones.
                """
                return PyMenu(self.service, "/mesh/cell_zone_conditions/clear_all").execute(*args, **kwargs)

        class poly(metaclass=PyMenuMeta):
            """
            Enters the polyhedral mesh generation menu.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
                self.controls = self.__class__.controls(path + [("controls", None)], service)
                self.local_regions = self.__class__.local_regions(path + [("local_regions", None)], service)
            def improve(self, *args, **kwargs):
                """
                Allows you to improve the polyhedral mesh quality based on the  quality-method.
                """
                return PyMenu(self.service, "/mesh/poly/improve").execute(*args, **kwargs)
            def collapse(self, *args, **kwargs):
                """
                Merge nodes to remove short edges and small faces. The decision threshold uses  edge size ratio, face size ratio, and (face)  area fraction.
                            
                """
                return PyMenu(self.service, "/mesh/poly/collapse").execute(*args, **kwargs)
            def remesh(self, *args, **kwargs):
                """
                Improves the quality in a local region based on the minimum skewness threshold.
                """
                return PyMenu(self.service, "/mesh/poly/remesh").execute(*args, **kwargs)
            def quality_method(self, *args, **kwargs):
                """
                Asks you to choose from internal-default,  orthoskew or squish quality measure for mesh improvement.
                """
                return PyMenu(self.service, "/mesh/poly/quality_method").execute(*args, **kwargs)

            class controls(metaclass=PyMenuMeta):
                """
                Enters the controls menu for setting poly parameters.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                    self.smooth_controls = self.__class__.smooth_controls(path + [("smooth_controls", None)], service)
                    self.prism = self.__class__.prism(path + [("prism", None)], service)
                def cell_sizing(self, *args, **kwargs):
                    """
                    Sets cell volume distribution function as geometric, linear, or size-field.
                    """
                    return PyMenu(self.service, "/mesh/poly/controls/cell_sizing").execute(*args, **kwargs)
                def non_fluid_type(self, *args, **kwargs):
                    """
                    Selects the default type for non-fluid zones.
                    """
                    return PyMenu(self.service, "/mesh/poly/controls/non_fluid_type").execute(*args, **kwargs)
                def improve(self, *args, **kwargs):
                    """
                    Enables poly mesh improvement by smoothing based on the smooth-controls.
                    """
                    return PyMenu(self.service, "/mesh/poly/controls/improve").execute(*args, **kwargs)
                def feature_angle(self, *args, **kwargs):
                    """
                    Sets the minimum threshold that should be preserved as a feature.
                    """
                    return PyMenu(self.service, "/mesh/poly/controls/feature_angle").execute(*args, **kwargs)
                def edge_size_ratio(self, *args, **kwargs):
                    """
                    Sets the threshold for the size ratio of two connected edges. Recommended range is 20 to 200.
                    """
                    return PyMenu(self.service, "/mesh/poly/controls/edge_size_ratio").execute(*args, **kwargs)
                def face_size_ratio(self, *args, **kwargs):
                    """
                    Sets the threshold for the size ratio of two faces on one cell. Recommended range is 100 to 300.
                    """
                    return PyMenu(self.service, "/mesh/poly/controls/face_size_ratio").execute(*args, **kwargs)
                def sliver_cell_area_fraction(self, *args, **kwargs):
                    """
                    Sets the threshold for the area of a single face to the cell surface area. Recommended range is 0.00001 to 0.001.
                    """
                    return PyMenu(self.service, "/mesh/poly/controls/sliver_cell_area_fraction").execute(*args, **kwargs)
                def merge_skew(self, *args, **kwargs):
                    """
                    Sets the minimum skewness threshold for cell merge.
                    """
                    return PyMenu(self.service, "/mesh/poly/controls/merge_skew").execute(*args, **kwargs)
                def remesh_skew(self, *args, **kwargs):
                    """
                    Sets the target skewness when remeshing.
                    """
                    return PyMenu(self.service, "/mesh/poly/controls/remesh_skew").execute(*args, **kwargs)

                class smooth_controls(metaclass=PyMenuMeta):
                    """
                    Enters the menu for setting smoothing parameters for poly mesh.
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                    def laplace_smooth_iterations(self, *args, **kwargs):
                        """
                        Sets the number of passes for tet-cell Laplace smoothing during the poly mesh generation phase.
                        """
                        return PyMenu(self.service, "/mesh/poly/controls/smooth_controls/laplace_smooth_iterations").execute(*args, **kwargs)
                    def edge_smooth_iterations(self, *args, **kwargs):
                        """
                        Sets the number of passes for tet-cell edge smoothing during the poly mesh generation phase.
                        """
                        return PyMenu(self.service, "/mesh/poly/controls/smooth_controls/edge_smooth_iterations").execute(*args, **kwargs)
                    def centroid_smooth_iterations(self, *args, **kwargs):
                        """
                        Sets the number of passes for tet-cell centroid smoothing during the poly mesh generation phase.
                        """
                        return PyMenu(self.service, "/mesh/poly/controls/smooth_controls/centroid_smooth_iterations").execute(*args, **kwargs)
                    def smooth_iterations(self, *args, **kwargs):
                        """
                        Sets the number of improvement passes over the full poly mesh.
                        """
                        return PyMenu(self.service, "/mesh/poly/controls/smooth_controls/smooth_iterations").execute(*args, **kwargs)
                    def smooth_attempts(self, *args, **kwargs):
                        """
                        Sets the maximum number of movements for a single node during poly mesh smoothing.
                        """
                        return PyMenu(self.service, "/mesh/poly/controls/smooth_controls/smooth_attempts").execute(*args, **kwargs)
                    def smooth_boundary(self, *args, **kwargs):
                        """
                        Enables boundary smoothing as part of poly cell smoothing. Default is no.
                        """
                        return PyMenu(self.service, "/mesh/poly/controls/smooth_controls/smooth_boundary").execute(*args, **kwargs)
                    def smooth_on_layer(self, *args, **kwargs):
                        """
                        Constrains movement of nodes to maintain layering during poly mesh smoothing.
                        """
                        return PyMenu(self.service, "/mesh/poly/controls/smooth_controls/smooth_on_layer").execute(*args, **kwargs)
                    def smooth_skew(self, *args, **kwargs):
                        """
                        Sets the minimum skewness threshold for poly mesh smoothing.
                        """
                        return PyMenu(self.service, "/mesh/poly/controls/smooth_controls/smooth_skew").execute(*args, **kwargs)

                class prism(metaclass=PyMenuMeta):
                    """
                    Poly prism transition controls.
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                    def apply_growth(self, *args, **kwargs):
                        """
                        Apply growth settings.
                        """
                        return PyMenu(self.service, "/mesh/poly/controls/prism/apply_growth").execute(*args, **kwargs)
                    def clear_growth(self, *args, **kwargs):
                        """
                        Clear growth settings.
                        """
                        return PyMenu(self.service, "/mesh/poly/controls/prism/clear_growth").execute(*args, **kwargs)
                    def list_growth(self, *args, **kwargs):
                        """
                        List growth settings.
                        """
                        return PyMenu(self.service, "/mesh/poly/controls/prism/list_growth").execute(*args, **kwargs)

            class local_regions(metaclass=PyMenuMeta):
                """
                Enters the local refinement menu.  Poly meshing follows tet meshing. These commands behave like the equivalent commands under /mesh/tet/local-regions/.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def activate(self, *args, **kwargs):
                    """
                    Activates the specified regions for refinement.
                    """
                    return PyMenu(self.service, "/mesh/poly/local_regions/activate").execute(*args, **kwargs)
                def deactivate(self, *args, **kwargs):
                    """
                    Deactivates the specified regions for refinement.
                    """
                    return PyMenu(self.service, "/mesh/poly/local_regions/deactivate").execute(*args, **kwargs)
                def define(self, *args, **kwargs):
                    """
                    Defines the refinement region according to the specified parameters.
                    """
                    return PyMenu(self.service, "/mesh/poly/local_regions/define").execute(*args, **kwargs)
                def delete(self, *args, **kwargs):
                    """
                    Deletes the specified refinement region.
                    """
                    return PyMenu(self.service, "/mesh/poly/local_regions/delete").execute(*args, **kwargs)
                def init(self, *args, **kwargs):
                    """
                    Defines the default refinement region encompassing the entire geometry.
                    """
                    return PyMenu(self.service, "/mesh/poly/local_regions/init").execute(*args, **kwargs)
                def list_all_regions(self, *args, **kwargs):
                    """
                    Lists all refinement region parameters and the activated regions in the console.
                    """
                    return PyMenu(self.service, "/mesh/poly/local_regions/list_all_regions").execute(*args, **kwargs)
                def refine(self, *args, **kwargs):
                    """
                    Refines the active cells inside the selected region based on the specified refinement parameters.
                    """
                    return PyMenu(self.service, "/mesh/poly/local_regions/refine").execute(*args, **kwargs)
                def ideal_vol(self, *args, **kwargs):
                    """
                    Reports the volume of an ideal tetrahedron for the edge length specified.
                    """
                    return PyMenu(self.service, "/mesh/poly/local_regions/ideal_vol").execute(*args, **kwargs)
                def ideal_area(self, *args, **kwargs):
                    """
                    Ideal triangle area for given edge length.
                    """
                    return PyMenu(self.service, "/mesh/poly/local_regions/ideal_area").execute(*args, **kwargs)

        class poly_hexcore(metaclass=PyMenuMeta):
            """
            Enters the menu for poly-hexcore mesh.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
                self.controls = self.__class__.controls(path + [("controls", None)], service)

            class controls(metaclass=PyMenuMeta):
                """
                Enters the menu for setting parameters for poly-hexcore mesh.
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def mark_core_region_cell_type_as_hex(self, *args, **kwargs):
                    """
                    Determines whether or not to apply hexahedra cells in the core region of the mesh. The default value is yes. 
                    """
                    return PyMenu(self.service, "/mesh/poly_hexcore/controls/mark_core_region_cell_type_as_hex").execute(*args, **kwargs)
                def avoid_1_by_8_cell_jump_in_hexcore(self, *args, **kwargs):
                    """
                    Avoid-1:8-cell-jump-in-hexcore.
                    """
                    return PyMenu(self.service, "/mesh/poly_hexcore/controls/avoid_1_by_8_cell_jump_in_hexcore").execute(*args, **kwargs)
                def only_polyhedra_for_selected_regions(self, *args, **kwargs):
                    """
                    Determines if polyhedra cells are to be applied to the selected regions. 
                    """
                    return PyMenu(self.service, "/mesh/poly_hexcore/controls/only_polyhedra_for_selected_regions").execute(*args, **kwargs)

        class auto_mesh_controls(metaclass=PyMenuMeta):
            """
            Enters the auto-mesh-controls submenu
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def backup_object(self, *args, **kwargs):
                """
                Enables creation of a backup of the surface mesh before volume meshing starts. This option is enabled by default.
                """
                return PyMenu(self.service, "/mesh/auto_mesh_controls/backup_object").execute(*args, **kwargs)

        class scoped_prisms(metaclass=PyMenuMeta):
            """
            Contains options for creating scoped prism controls for mesh objects.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def create(self, *args, **kwargs):
                """
                Creates a new scoped prism control based on the parameters and scope specified. Specify the name, offset method, first height or aspect ratio, number of layers, and rate or last percent. Select the mesh object and set the scope  (fluid-regions, named-regions, or  solid-regions). Specify the zones to grow prisms  (all-zones, only-walls,  selected-face-zones, or selected-labels, or solid-fluid-interface). When  named-regions and/or selected-face-zones or selected-labels are selected, specify the volume and/or boundary scope. If interior baffle zones are selected, retain the option to grow prisms on both sides of the baffles or disable it to grow prisms on one side.
                """
                return PyMenu(self.service, "/mesh/scoped_prisms/create").execute(*args, **kwargs)
            def modify(self, *args, **kwargs):
                """
                Modifies the specified control based on the parameters specified.
                """
                return PyMenu(self.service, "/mesh/scoped_prisms/modify").execute(*args, **kwargs)
            def delete(self, *args, **kwargs):
                """
                Deletes the specified scoped prism control.
                """
                return PyMenu(self.service, "/mesh/scoped_prisms/delete").execute(*args, **kwargs)
            def list(self, *args, **kwargs):
                """
                Lists all the defined scoped prism controls.
                """
                return PyMenu(self.service, "/mesh/scoped_prisms/list").execute(*args, **kwargs)
            def read(self, *args, **kwargs):
                """
                Reads in the specified scoped prism control file (*.pzmcontrol).
                """
                return PyMenu(self.service, "/mesh/scoped_prisms/read").execute(*args, **kwargs)
            def set_no_imprint_zones(self, *args, **kwargs):
                """
                Used to specify face zones that should not be imprinted during prism generation.
                """
                return PyMenu(self.service, "/mesh/scoped_prisms/set_no_imprint_zones").execute(*args, **kwargs)
            def write(self, *args, **kwargs):
                """
                Writes the scoped prism controls to a prism control file (*.pzmcontrol). Specify the scoped prism file name.
                """
                return PyMenu(self.service, "/mesh/scoped_prisms/write").execute(*args, **kwargs)
            def growth_options(self, *args, **kwargs):
                """
                Enables you to specify scoped prism growth options. Select Fix First  Height if required, and specify the gap factor, maximum aspect ratio, prism quality method, and the threshold quality value for stair stepping.
                """
                return PyMenu(self.service, "/mesh/scoped_prisms/growth_options").execute(*args, **kwargs)
            def set_overset_prism_controls(self, *args, **kwargs):
                """
                Set boundary layer controls for overset mesh generation.
                """
                return PyMenu(self.service, "/mesh/scoped_prisms/set_overset_prism_controls").execute(*args, **kwargs)
            def set_advanced_controls(self, *args, **kwargs):
                """
                Used to specify various controls for scoped prisms. Prompts include setting iterations for normal based prisms, smoothing, prism improvement, automatic node movement, and warp improvement. Prompts also include checks for stair-step interactions, as well as proximity, quality, and the exposure of quad quality. Automatic stair-stepping occurs during prism generation based on the proximity and quality limits. You can intentionally avoid stair-stepping by setting the last three prompts (proximity, quality, and the exposure of quad quality) to no, although you may also retain some poor quality cells.
                """
                return PyMenu(self.service, "/mesh/scoped_prisms/set_advanced_controls").execute(*args, **kwargs)

    class display(metaclass=PyMenuMeta):
        """
        Enter the display menu.
        """
        def __init__(self, path, service):
            self.path = path
            self.service = service
            self.set = self.__class__.set(path + [("set", None)], service)
            self.set_grid = self.__class__.set_grid(path + [("set_grid", None)], service)
            self.views = self.__class__.views(path + [("views", None)], service)
            self.display_states = self.__class__.display_states(path + [("display_states", None)], service)
            self.xy_plot = self.__class__.xy_plot(path + [("xy_plot", None)], service)
            self.update_scene = self.__class__.update_scene(path + [("update_scene", None)], service)
            self.objects = self.__class__.objects(path + [("objects", None)], service)
            self.zones = self.__class__.zones(path + [("zones", None)], service)
            self.advanced_rendering = self.__class__.advanced_rendering(path + [("advanced_rendering", None)], service)
        def annotate(self, *args, **kwargs):
            """
            Adds annotation text to a graphics window. It will prompt you for a string to use as the annotation text, and then a dialog box will prompt you to select a screen location using the mouse-probe button on your mouse. 
            """
            return PyMenu(self.service, "/display/annotate").execute(*args, **kwargs)
        def boundary_cells(self, *args, **kwargs):
            """
            Displays boundary cells attached to the specified face zones. 
            """
            return PyMenu(self.service, "/display/boundary_cells").execute(*args, **kwargs)
        def boundary_grid(self, *args, **kwargs):
            """
            Displays only boundary zones according to the currently set parameters. 
            """
            return PyMenu(self.service, "/display/boundary_grid").execute(*args, **kwargs)
        def center_view_on(self, *args, **kwargs):
            """
            Sets the camera target to be the center (centroid) of an entity. 
            """
            return PyMenu(self.service, "/display/center_view_on").execute(*args, **kwargs)
        def clear(self, *args, **kwargs):
            """
            Clears the active graphics window. This option is useful when you redo an overlay. 
            """
            return PyMenu(self.service, "/display/clear").execute(*args, **kwargs)
        def clear_annotation(self, *args, **kwargs):
            """
            Removes all annotations and attachment lines from the active graphics window. 
            """
            return PyMenu(self.service, "/display/clear_annotation").execute(*args, **kwargs)
        def draw_zones(self, *args, **kwargs):
            """
            Draws the boundary/cell zones using the zone ID specified as input. 
            """
            return PyMenu(self.service, "/display/draw_zones").execute(*args, **kwargs)
        def draw_cells_using_faces(self, *args, **kwargs):
            """
            Draws cells that are neighbors for the selected faces. 
            """
            return PyMenu(self.service, "/display/draw_cells_using_faces").execute(*args, **kwargs)
        def draw_cells_using_nodes(self, *args, **kwargs):
            """
            Draws cells that are connected to the selected nodes. 
            """
            return PyMenu(self.service, "/display/draw_cells_using_nodes").execute(*args, **kwargs)
        def draw_face_zones_using_entities(self, *args, **kwargs):
            """
            Draws cells that are connected to the selected entities. 
            """
            return PyMenu(self.service, "/display/draw_face_zones_using_entities").execute(*args, **kwargs)
        def all_grid(self, *args, **kwargs):
            """
            Displays the grid according to the currently set parameters. 
            """
            return PyMenu(self.service, "/display/all_grid").execute(*args, **kwargs)
        def save_picture(self, *args, **kwargs):
            """
            Saves a picture file of the active graphics window. 
            """
            return PyMenu(self.service, "/display/save_picture").execute(*args, **kwargs)
        def redisplay(self, *args, **kwargs):
            """
            Redraws the grid in the graphics window. 
            """
            return PyMenu(self.service, "/display/redisplay").execute(*args, **kwargs)
        def show_hide_clipping_plane_triad(self, *args, **kwargs):
            """
            S
            """
            return PyMenu(self.service, "/display/show_hide_clipping_plane_triad").execute(*args, **kwargs)
        def set_list_tree_separator(self, *args, **kwargs):
            """
            Sets the separator character to be used to determine the common prefix for items listed in the selection lists, when the tree view is used.
            """
            return PyMenu(self.service, "/display/set_list_tree_separator").execute(*args, **kwargs)
        def update_layout(self, *args, **kwargs):
            """
            Update the fluent layout.
            """
            return PyMenu(self.service, "/display/update_layout").execute(*args, **kwargs)

        class set(metaclass=PyMenuMeta):
            """
            Enables you to enter the set menu to set the display parameters. 
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
                self.colors = self.__class__.colors(path + [("colors", None)], service)
                self.picture = self.__class__.picture(path + [("picture", None)], service)
                self.lights = self.__class__.lights(path + [("lights", None)], service)
                self.rendering_options = self.__class__.rendering_options(path + [("rendering_options", None)], service)
                self.styles = self.__class__.styles(path + [("styles", None)], service)
                self.windows = self.__class__.windows(path + [("windows", None)], service)
            def highlight_tree_selection(self, *args, **kwargs):
                """
                Turn on/off outline display of tree selection in graphics window.
                """
                return PyMenu(self.service, "/display/set/highlight_tree_selection").execute(*args, **kwargs)
            def remote_display_defaults(self, *args, **kwargs):
                """
                Adjusts graphics window parameters to optimal settings for a remote display.   Restore parameters for local display using native-display-defaults.
                """
                return PyMenu(self.service, "/display/set/remote_display_defaults").execute(*args, **kwargs)
            def native_display_defaults(self, *args, **kwargs):
                """
                Resets graphics window parameters to optimal settings for a local display.   Used after setting parameters for a remote display with remote-display-defaults.
                """
                return PyMenu(self.service, "/display/set/native_display_defaults").execute(*args, **kwargs)
            def edges(self, *args, **kwargs):
                """
                Enables/disables the display of face/cell edges. 
                """
                return PyMenu(self.service, "/display/set/edges").execute(*args, **kwargs)
            def filled_grid(self, *args, **kwargs):
                """
                Enables/disables the filled grid option. When a grid is not filled, only its outline is drawn. 
                """
                return PyMenu(self.service, "/display/set/filled_grid").execute(*args, **kwargs)
            def quick_moves_algorithm(self, *args, **kwargs):
                """
                Select quick moves algorithm for icons and helptext overlay.
                """
                return PyMenu(self.service, "/display/set/quick_moves_algorithm").execute(*args, **kwargs)
            def line_weight(self, *args, **kwargs):
                """
                Sets the line width factor for the window. 
                """
                return PyMenu(self.service, "/display/set/line_weight").execute(*args, **kwargs)
            def overlays(self, *args, **kwargs):
                """
                Turns overlays on and off. 
                """
                return PyMenu(self.service, "/display/set/overlays").execute(*args, **kwargs)
            def re_render(self, *args, **kwargs):
                """
                Re-renders the current window after modifying the variables in the set menu. 
                """
                return PyMenu(self.service, "/display/set/re_render").execute(*args, **kwargs)
            def reset_graphics(self, *args, **kwargs):
                """
                Resets the graphics system. 
                """
                return PyMenu(self.service, "/display/set/reset_graphics").execute(*args, **kwargs)
            def shrink_factor(self, *args, **kwargs):
                """
                Sets shrinkage of both faces and cells. A value of zero indicates no shrinkage, while a value of one would shrink the face or cell to a point. 
                """
                return PyMenu(self.service, "/display/set/shrink_factor").execute(*args, **kwargs)
            def title(self, *args, **kwargs):
                """
                Sets the problem title. 
                """
                return PyMenu(self.service, "/display/set/title").execute(*args, **kwargs)

            class colors(metaclass=PyMenuMeta):
                """
                Enables you to enter the colors options menu. 
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                    self.by_type = self.__class__.by_type(path + [("by_type", None)], service)
                    self.by_surface = self.__class__.by_surface(path + [("by_surface", None)], service)
                def background(self, *args, **kwargs):
                    """
                    Sets the background (window) color. 
                    """
                    return PyMenu(self.service, "/display/set/colors/background").execute(*args, **kwargs)
                def color_by_type(self, *args, **kwargs):
                    """
                    Enables you to specify that the entities should be colored by their type or ID. 
                    """
                    return PyMenu(self.service, "/display/set/colors/color_by_type").execute(*args, **kwargs)
                def foreground(self, *args, **kwargs):
                    """
                    Sets the foreground (text and window frame) color. 
                    """
                    return PyMenu(self.service, "/display/set/colors/foreground").execute(*args, **kwargs)
                def far_field_faces(self, *args, **kwargs):
                    """
                    Sets the color of far field faces. 
                    """
                    return PyMenu(self.service, "/display/set/colors/far_field_faces").execute(*args, **kwargs)
                def inlet_faces(self, *args, **kwargs):
                    """
                    Sets the color of the inlet faces. 
                    """
                    return PyMenu(self.service, "/display/set/colors/inlet_faces").execute(*args, **kwargs)
                def interior_faces(self, *args, **kwargs):
                    """
                    Sets the color of the interior faces. 
                    """
                    return PyMenu(self.service, "/display/set/colors/interior_faces").execute(*args, **kwargs)
                def internal_faces(self, *args, **kwargs):
                    """
                    Sets the color of the internal interface faces. 
                    """
                    return PyMenu(self.service, "/display/set/colors/internal_faces").execute(*args, **kwargs)
                def outlet_faces(self, *args, **kwargs):
                    """
                    Sets the color of the outlet faces. 
                    """
                    return PyMenu(self.service, "/display/set/colors/outlet_faces").execute(*args, **kwargs)
                def overset_faces(self, *args, **kwargs):
                    """
                    Sets the color of the overset faces. 
                    """
                    return PyMenu(self.service, "/display/set/colors/overset_faces").execute(*args, **kwargs)
                def periodic_faces(self, *args, **kwargs):
                    """
                    Sets the color of periodic faces. 
                    """
                    return PyMenu(self.service, "/display/set/colors/periodic_faces").execute(*args, **kwargs)
                def rans_les_interface_faces(self, *args, **kwargs):
                    """
                    Sets the color of RANS/LES interface faces. 
                    """
                    return PyMenu(self.service, "/display/set/colors/rans_les_interface_faces").execute(*args, **kwargs)
                def reset_user_colors(self, *args, **kwargs):
                    """
                    Resets individual grid surface colors to the defaults. 
                    """
                    return PyMenu(self.service, "/display/set/colors/reset_user_colors").execute(*args, **kwargs)
                def show_user_colors(self, *args, **kwargs):
                    """
                    Lists the current defined user colors. 
                    """
                    return PyMenu(self.service, "/display/set/colors/show_user_colors").execute(*args, **kwargs)
                def symmetry_faces(self, *args, **kwargs):
                    """
                    Sets the color of symmetric faces. 
                    """
                    return PyMenu(self.service, "/display/set/colors/symmetry_faces").execute(*args, **kwargs)
                def axis_faces(self, *args, **kwargs):
                    """
                    Sets the color of axisymmetric faces. 
                    """
                    return PyMenu(self.service, "/display/set/colors/axis_faces").execute(*args, **kwargs)
                def free_surface_faces(self, *args, **kwargs):
                    """
                    Sets the color of free surface faces. 
                    """
                    return PyMenu(self.service, "/display/set/colors/free_surface_faces").execute(*args, **kwargs)
                def traction_faces(self, *args, **kwargs):
                    """
                    Sets the color for traction faces. 
                    """
                    return PyMenu(self.service, "/display/set/colors/traction_faces").execute(*args, **kwargs)
                def user_color(self, *args, **kwargs):
                    """
                    Enables you to change the color for the specified zone. 
                    """
                    return PyMenu(self.service, "/display/set/colors/user_color").execute(*args, **kwargs)
                def wall_faces(self, *args, **kwargs):
                    """
                    Sets color for wall faces. 
                    """
                    return PyMenu(self.service, "/display/set/colors/wall_faces").execute(*args, **kwargs)
                def interface_faces(self, *args, **kwargs):
                    """
                    Sets the color of grid interface faces. 
                    """
                    return PyMenu(self.service, "/display/set/colors/interface_faces").execute(*args, **kwargs)
                def list(self, *args, **kwargs):
                    """
                    Lists the colors available for the selected zone type. 
                    """
                    return PyMenu(self.service, "/display/set/colors/list").execute(*args, **kwargs)
                def reset_colors(self, *args, **kwargs):
                    """
                    Resets the individual grid surface colors to the defaults. 
                    """
                    return PyMenu(self.service, "/display/set/colors/reset_colors").execute(*args, **kwargs)
                def surface(self, *args, **kwargs):
                    """
                    Sets the color of surfaces. 
                    """
                    return PyMenu(self.service, "/display/set/colors/surface").execute(*args, **kwargs)
                def skip_label(self, *args, **kwargs):
                    """
                    Sets the number of labels to be skipped in the colormap scale. 
                    """
                    return PyMenu(self.service, "/display/set/colors/skip_label").execute(*args, **kwargs)
                def automatic_skip(self, *args, **kwargs):
                    """
                    Specify whether the number of colormap labels is determined automatically. The default is yes.
                    """
                    return PyMenu(self.service, "/display/set/colors/automatic_skip").execute(*args, **kwargs)
                def graphics_color_theme(self, *args, **kwargs):
                    """
                    Sets the color theme for the graphics window. The color options (black, white, gray-gradient, or workbench) are for the background display, but changing the theme also changes the default colors for items that display in the graphics windows, like faces and edges. 
                    """
                    return PyMenu(self.service, "/display/set/colors/graphics_color_theme").execute(*args, **kwargs)

                class by_type(metaclass=PyMenuMeta):
                    """
                    Enter the zone type color and material assignment menu.
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                        self.type_name = self.__class__.type_name(path + [("type_name", None)], service)
                    def only_list_case_boundaries(self, *args, **kwargs):
                        """
                        Only list the boundary types that are assigned in this case.
                        """
                        return PyMenu(self.service, "/display/set/colors/by_type/only_list_case_boundaries").execute(*args, **kwargs)
                    def use_inherent_material_color(self, *args, **kwargs):
                        """
                        Use inherent material color for boundary zones.
                        """
                        return PyMenu(self.service, "/display/set/colors/by_type/use_inherent_material_color").execute(*args, **kwargs)
                    def reset(self, *args, **kwargs):
                        """
                        To reset colors and/or materials to the defaults.
                        """
                        return PyMenu(self.service, "/display/set/colors/by_type/reset").execute(*args, **kwargs)

                    class type_name(metaclass=PyMenuMeta):
                        """
                        Select the boundary type to specify colors and/or materials.
                        """
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service
                            self.axis = self.__class__.axis(path + [("axis", None)], service)
                            self.far_field = self.__class__.far_field(path + [("far_field", None)], service)
                            self.free_surface = self.__class__.free_surface(path + [("free_surface", None)], service)
                            self.inlet = self.__class__.inlet(path + [("inlet", None)], service)
                            self.interface = self.__class__.interface(path + [("interface", None)], service)
                            self.interior = self.__class__.interior(path + [("interior", None)], service)
                            self.internal = self.__class__.internal(path + [("internal", None)], service)
                            self.outlet = self.__class__.outlet(path + [("outlet", None)], service)
                            self.overset = self.__class__.overset(path + [("overset", None)], service)
                            self.periodic = self.__class__.periodic(path + [("periodic", None)], service)
                            self.rans_les_interface = self.__class__.rans_les_interface(path + [("rans_les_interface", None)], service)
                            self.surface = self.__class__.surface(path + [("surface", None)], service)
                            self.symmetry = self.__class__.symmetry(path + [("symmetry", None)], service)
                            self.traction = self.__class__.traction(path + [("traction", None)], service)
                            self.wall = self.__class__.wall(path + [("wall", None)], service)

                        class axis(metaclass=PyMenuMeta):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service
                            def color(self, *args, **kwargs):
                                """
                                Set a color for the selected boundary type.
                                """
                                return PyMenu(self.service, "/display/set/colors/by_type/type_name/axis/color").execute(*args, **kwargs)
                            def material(self, *args, **kwargs):
                                """
                                Set a material for the selected boundary type.
                                """
                                return PyMenu(self.service, "/display/set/colors/by_type/type_name/axis/material").execute(*args, **kwargs)

                        class far_field(metaclass=PyMenuMeta):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service
                            def color(self, *args, **kwargs):
                                """
                                Set a color for the selected boundary type.
                                """
                                return PyMenu(self.service, "/display/set/colors/by_type/type_name/far_field/color").execute(*args, **kwargs)
                            def material(self, *args, **kwargs):
                                """
                                Set a material for the selected boundary type.
                                """
                                return PyMenu(self.service, "/display/set/colors/by_type/type_name/far_field/material").execute(*args, **kwargs)

                        class free_surface(metaclass=PyMenuMeta):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service
                            def color(self, *args, **kwargs):
                                """
                                Set a color for the selected boundary type.
                                """
                                return PyMenu(self.service, "/display/set/colors/by_type/type_name/free_surface/color").execute(*args, **kwargs)
                            def material(self, *args, **kwargs):
                                """
                                Set a material for the selected boundary type.
                                """
                                return PyMenu(self.service, "/display/set/colors/by_type/type_name/free_surface/material").execute(*args, **kwargs)

                        class inlet(metaclass=PyMenuMeta):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service
                            def color(self, *args, **kwargs):
                                """
                                Set a color for the selected boundary type.
                                """
                                return PyMenu(self.service, "/display/set/colors/by_type/type_name/inlet/color").execute(*args, **kwargs)
                            def material(self, *args, **kwargs):
                                """
                                Set a material for the selected boundary type.
                                """
                                return PyMenu(self.service, "/display/set/colors/by_type/type_name/inlet/material").execute(*args, **kwargs)

                        class interface(metaclass=PyMenuMeta):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service
                            def color(self, *args, **kwargs):
                                """
                                Set a color for the selected boundary type.
                                """
                                return PyMenu(self.service, "/display/set/colors/by_type/type_name/interface/color").execute(*args, **kwargs)
                            def material(self, *args, **kwargs):
                                """
                                Set a material for the selected boundary type.
                                """
                                return PyMenu(self.service, "/display/set/colors/by_type/type_name/interface/material").execute(*args, **kwargs)

                        class interior(metaclass=PyMenuMeta):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service
                            def color(self, *args, **kwargs):
                                """
                                Set a color for the selected boundary type.
                                """
                                return PyMenu(self.service, "/display/set/colors/by_type/type_name/interior/color").execute(*args, **kwargs)
                            def material(self, *args, **kwargs):
                                """
                                Set a material for the selected boundary type.
                                """
                                return PyMenu(self.service, "/display/set/colors/by_type/type_name/interior/material").execute(*args, **kwargs)

                        class internal(metaclass=PyMenuMeta):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service
                            def color(self, *args, **kwargs):
                                """
                                Set a color for the selected boundary type.
                                """
                                return PyMenu(self.service, "/display/set/colors/by_type/type_name/internal/color").execute(*args, **kwargs)
                            def material(self, *args, **kwargs):
                                """
                                Set a material for the selected boundary type.
                                """
                                return PyMenu(self.service, "/display/set/colors/by_type/type_name/internal/material").execute(*args, **kwargs)

                        class outlet(metaclass=PyMenuMeta):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service
                            def color(self, *args, **kwargs):
                                """
                                Set a color for the selected boundary type.
                                """
                                return PyMenu(self.service, "/display/set/colors/by_type/type_name/outlet/color").execute(*args, **kwargs)
                            def material(self, *args, **kwargs):
                                """
                                Set a material for the selected boundary type.
                                """
                                return PyMenu(self.service, "/display/set/colors/by_type/type_name/outlet/material").execute(*args, **kwargs)

                        class overset(metaclass=PyMenuMeta):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service
                            def color(self, *args, **kwargs):
                                """
                                Set a color for the selected boundary type.
                                """
                                return PyMenu(self.service, "/display/set/colors/by_type/type_name/overset/color").execute(*args, **kwargs)
                            def material(self, *args, **kwargs):
                                """
                                Set a material for the selected boundary type.
                                """
                                return PyMenu(self.service, "/display/set/colors/by_type/type_name/overset/material").execute(*args, **kwargs)

                        class periodic(metaclass=PyMenuMeta):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service
                            def color(self, *args, **kwargs):
                                """
                                Set a color for the selected boundary type.
                                """
                                return PyMenu(self.service, "/display/set/colors/by_type/type_name/periodic/color").execute(*args, **kwargs)
                            def material(self, *args, **kwargs):
                                """
                                Set a material for the selected boundary type.
                                """
                                return PyMenu(self.service, "/display/set/colors/by_type/type_name/periodic/material").execute(*args, **kwargs)

                        class rans_les_interface(metaclass=PyMenuMeta):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service
                            def color(self, *args, **kwargs):
                                """
                                Set a color for the selected boundary type.
                                """
                                return PyMenu(self.service, "/display/set/colors/by_type/type_name/rans_les_interface/color").execute(*args, **kwargs)
                            def material(self, *args, **kwargs):
                                """
                                Set a material for the selected boundary type.
                                """
                                return PyMenu(self.service, "/display/set/colors/by_type/type_name/rans_les_interface/material").execute(*args, **kwargs)

                        class surface(metaclass=PyMenuMeta):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service
                            def color(self, *args, **kwargs):
                                """
                                Set a color for the selected boundary type.
                                """
                                return PyMenu(self.service, "/display/set/colors/by_type/type_name/surface/color").execute(*args, **kwargs)
                            def material(self, *args, **kwargs):
                                """
                                Set a material for the selected boundary type.
                                """
                                return PyMenu(self.service, "/display/set/colors/by_type/type_name/surface/material").execute(*args, **kwargs)

                        class symmetry(metaclass=PyMenuMeta):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service
                            def color(self, *args, **kwargs):
                                """
                                Set a color for the selected boundary type.
                                """
                                return PyMenu(self.service, "/display/set/colors/by_type/type_name/symmetry/color").execute(*args, **kwargs)
                            def material(self, *args, **kwargs):
                                """
                                Set a material for the selected boundary type.
                                """
                                return PyMenu(self.service, "/display/set/colors/by_type/type_name/symmetry/material").execute(*args, **kwargs)

                        class traction(metaclass=PyMenuMeta):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service
                            def color(self, *args, **kwargs):
                                """
                                Set a color for the selected boundary type.
                                """
                                return PyMenu(self.service, "/display/set/colors/by_type/type_name/traction/color").execute(*args, **kwargs)
                            def material(self, *args, **kwargs):
                                """
                                Set a material for the selected boundary type.
                                """
                                return PyMenu(self.service, "/display/set/colors/by_type/type_name/traction/material").execute(*args, **kwargs)

                        class wall(metaclass=PyMenuMeta):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service
                            def color(self, *args, **kwargs):
                                """
                                Set a color for the selected boundary type.
                                """
                                return PyMenu(self.service, "/display/set/colors/by_type/type_name/wall/color").execute(*args, **kwargs)
                            def material(self, *args, **kwargs):
                                """
                                Set a material for the selected boundary type.
                                """
                                return PyMenu(self.service, "/display/set/colors/by_type/type_name/wall/material").execute(*args, **kwargs)

                class by_surface(metaclass=PyMenuMeta):
                    """
                    Enter the surface(s) color and material assignment menu.
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                    def surfaces(self, *args, **kwargs):
                        """
                        Select the surface(s) to specify colors and/or materials.
                        """
                        return PyMenu(self.service, "/display/set/colors/by_surface/surfaces").execute(*args, **kwargs)
                    def use_inherent_material_color(self, *args, **kwargs):
                        """
                        Use inherent material color for surfaces.
                        """
                        return PyMenu(self.service, "/display/set/colors/by_surface/use_inherent_material_color").execute(*args, **kwargs)
                    def reset(self, *args, **kwargs):
                        """
                        To reset colors and/or materials to the defaults.
                        """
                        return PyMenu(self.service, "/display/set/colors/by_surface/reset").execute(*args, **kwargs)
                    def list_surfaces_by_color(self, *args, **kwargs):
                        """
                        To list the surfaces by its color.
                        """
                        return PyMenu(self.service, "/display/set/colors/by_surface/list_surfaces_by_color").execute(*args, **kwargs)
                    def list_surfaces_by_material(self, *args, **kwargs):
                        """
                        To list the surfaces by its material.
                        """
                        return PyMenu(self.service, "/display/set/colors/by_surface/list_surfaces_by_material").execute(*args, **kwargs)

            class picture(metaclass=PyMenuMeta):
                """
                Saves a hardcopy file of the active graphics window. 
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                    self.color_mode = self.__class__.color_mode(path + [("color_mode", None)], service)
                    self.driver = self.__class__.driver(path + [("driver", None)], service)
                def invert_background(self, *args, **kwargs):
                    """
                    Enables/disables the exchange of foreground/background colors for hardcopy files. 
                    """
                    return PyMenu(self.service, "/display/set/picture/invert_background").execute(*args, **kwargs)
                def landscape(self, *args, **kwargs):
                    """
                    Toggles between landscape or portrait orientation. 
                    """
                    return PyMenu(self.service, "/display/set/picture/landscape").execute(*args, **kwargs)
                def preview(self, *args, **kwargs):
                    """
                    Applies the settings of the color-mode, invert-background, and landscape options to the currently active graphics window to preview the appearance of printed hardcopies. 
                    """
                    return PyMenu(self.service, "/display/set/picture/preview").execute(*args, **kwargs)
                def x_resolution(self, *args, **kwargs):
                    """
                    Sets the width of the raster format images in pixels (0 implies that the hardcopy should use the same resolution as the active graphics window). 
                    """
                    return PyMenu(self.service, "/display/set/picture/x_resolution").execute(*args, **kwargs)
                def y_resolution(self, *args, **kwargs):
                    """
                    Sets the height of the raster format images in pixels (0 implies that the hardcopy should use the same resolution as the active graphics window). 
                    """
                    return PyMenu(self.service, "/display/set/picture/y_resolution").execute(*args, **kwargs)
                def dpi(self, *args, **kwargs):
                    """
                    Specifies the resolution in dots per inch for EPS and PostScript files. 
                    """
                    return PyMenu(self.service, "/display/set/picture/dpi").execute(*args, **kwargs)
                def use_window_resolution(self, *args, **kwargs):
                    """
                    Disables/enables the use of the current graphics window resolution when saving an image of the graphics window. If disabled, the resolution will be as specified for x-resolution and y-resolution.
                    """
                    return PyMenu(self.service, "/display/set/picture/use_window_resolution").execute(*args, **kwargs)
                def set_standard_resolution(self, *args, **kwargs):
                    """
                    Select from pre-defined resolution list.
                    """
                    return PyMenu(self.service, "/display/set/picture/set_standard_resolution").execute(*args, **kwargs)
                def jpeg_hardcopy_quality(self, *args, **kwargs):
                    """
                    Controls the size and quality of how JPEG files are saved based on a scale of 0-100, with zero being low quality small files and 100 being high quality larger files.
                    """
                    return PyMenu(self.service, "/display/set/picture/jpeg_hardcopy_quality").execute(*args, **kwargs)

                class color_mode(metaclass=PyMenuMeta):
                    """
                    Contains the available color modes. 
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                    def color(self, *args, **kwargs):
                        """
                        Selects full color and plots the hardcopy in color. 
                        """
                        return PyMenu(self.service, "/display/set/picture/color_mode/color").execute(*args, **kwargs)
                    def gray_scale(self, *args, **kwargs):
                        """
                        Selects gray scale (that is, various shades of gray) and converts color to gray-scale for hardcopy. 
                        """
                        return PyMenu(self.service, "/display/set/picture/color_mode/gray_scale").execute(*args, **kwargs)
                    def mono_chrome(self, *args, **kwargs):
                        """
                        Selects color to monochrome (black and white) for hardcopy. 
                        """
                        return PyMenu(self.service, "/display/set/picture/color_mode/mono_chrome").execute(*args, **kwargs)
                    def list(self, *args, **kwargs):
                        """
                        Displays the current hardcopy color mode. 
                        """
                        return PyMenu(self.service, "/display/set/picture/color_mode/list").execute(*args, **kwargs)

                class driver(metaclass=PyMenuMeta):
                    """
                    Contains the available hardcopy formats. 
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                        self.post_format = self.__class__.post_format(path + [("post_format", None)], service)
                    def dump_window(self, *args, **kwargs):
                        """
                        Sets the command to dump a graphics window to a file. 
                        """
                        return PyMenu(self.service, "/display/set/picture/driver/dump_window").execute(*args, **kwargs)
                    def eps(self, *args, **kwargs):
                        """
                        Sets the Encapsulated PostScript format. 
                        """
                        return PyMenu(self.service, "/display/set/picture/driver/eps").execute(*args, **kwargs)
                    def jpeg(self, *args, **kwargs):
                        """
                        Sets the JPEG image format. 
                        """
                        return PyMenu(self.service, "/display/set/picture/driver/jpeg").execute(*args, **kwargs)
                    def post_script(self, *args, **kwargs):
                        """
                        Sets the PostScript format. 
                        """
                        return PyMenu(self.service, "/display/set/picture/driver/post_script").execute(*args, **kwargs)
                    def ppm(self, *args, **kwargs):
                        """
                        Sets the PPM format. 
                        """
                        return PyMenu(self.service, "/display/set/picture/driver/ppm").execute(*args, **kwargs)
                    def tiff(self, *args, **kwargs):
                        """
                        Sets the TIFF format. 
                        """
                        return PyMenu(self.service, "/display/set/picture/driver/tiff").execute(*args, **kwargs)
                    def png(self, *args, **kwargs):
                        """
                        Sets the PNG image format. 
                        """
                        return PyMenu(self.service, "/display/set/picture/driver/png").execute(*args, **kwargs)
                    def hsf(self, *args, **kwargs):
                        """
                        Produces HOOPS Visualize Stream Format (HSF) output for  hardcopies.
                        """
                        return PyMenu(self.service, "/display/set/picture/driver/hsf").execute(*args, **kwargs)
                    def avz(self, *args, **kwargs):
                        """
                        Use AVZ output for hardcopies.
                        """
                        return PyMenu(self.service, "/display/set/picture/driver/avz").execute(*args, **kwargs)
                    def glb(self, *args, **kwargs):
                        """
                        Produces GLB output for hardcopies.
                        """
                        return PyMenu(self.service, "/display/set/picture/driver/glb").execute(*args, **kwargs)
                    def vrml(self, *args, **kwargs):
                        """
                        Sets the VRML format. 
                        """
                        return PyMenu(self.service, "/display/set/picture/driver/vrml").execute(*args, **kwargs)
                    def list(self, *args, **kwargs):
                        """
                        Displays the current hardcopy format. 
                        """
                        return PyMenu(self.service, "/display/set/picture/driver/list").execute(*args, **kwargs)
                    def options(self, *args, **kwargs):
                        """
                        Enables you to set hardcopy options, such as landscape orientation, pen speed, and physical size. The options may be entered on one line if you separate them with commas. 
                        """
                        return PyMenu(self.service, "/display/set/picture/driver/options").execute(*args, **kwargs)

                    class post_format(metaclass=PyMenuMeta):
                        """
                        Contains commands for setting the PostScript driver format and save files in PS files that can be printed quickly. 
                        """
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service
                        def fast_raster(self, *args, **kwargs):
                            """
                            Enables a raster file that may be larger than the standard raster file, but will print much more quickly. 
                            """
                            return PyMenu(self.service, "/display/set/picture/driver/post_format/fast_raster").execute(*args, **kwargs)
                        def raster(self, *args, **kwargs):
                            """
                            Enables the standard raster file. 
                            """
                            return PyMenu(self.service, "/display/set/picture/driver/post_format/raster").execute(*args, **kwargs)
                        def rle_raster(self, *args, **kwargs):
                            """
                            Enables a run-length encoded raster file that will be about the same size as the standard raster file, but will print slightly more quickly. This is the default file type. 
                            """
                            return PyMenu(self.service, "/display/set/picture/driver/post_format/rle_raster").execute(*args, **kwargs)
                        def vector(self, *args, **kwargs):
                            """
                            Enables the standard vector file. 
                            """
                            return PyMenu(self.service, "/display/set/picture/driver/post_format/vector").execute(*args, **kwargs)

            class lights(metaclass=PyMenuMeta):
                """
                Enters the lights menu. 
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                    self.lighting_interpolation = self.__class__.lighting_interpolation(path + [("lighting_interpolation", None)], service)
                def lights_on(self, *args, **kwargs):
                    """
                    Enables/disables the display of all lights. 
                    """
                    return PyMenu(self.service, "/display/set/lights/lights_on").execute(*args, **kwargs)
                def set_ambient_color(self, *args, **kwargs):
                    """
                    Sets the ambient color for the scene. The ambient color is the background light color in scene. 
                    """
                    return PyMenu(self.service, "/display/set/lights/set_ambient_color").execute(*args, **kwargs)
                def set_light(self, *args, **kwargs):
                    """
                    Adds or modifies a directional, colored light. 
                    """
                    return PyMenu(self.service, "/display/set/lights/set_light").execute(*args, **kwargs)
                def headlight_on(self, *args, **kwargs):
                    """
                    Turns the light that moves with the camera on or off. This is controlled automatically by default.
                    """
                    return PyMenu(self.service, "/display/set/lights/headlight_on").execute(*args, **kwargs)

                class lighting_interpolation(metaclass=PyMenuMeta):
                    """
                    Sets the lighting interpolation method to be used. You can choose automatic, flat, gouraud, or phong. "Automatic" automatically picks the best lighting method for the display in the graphics window. Flat is the most basic method, and the others are more sophisticated and provide smoother gradations of color. 
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                    def automatic(self, *args, **kwargs):
                        """
                        Fluent automatically picks the best lighting method for the display in the graphics window.
                        """
                        return PyMenu(self.service, "/display/set/lights/lighting_interpolation/automatic").execute(*args, **kwargs)
                    def flat(self, *args, **kwargs):
                        """
                        Uses flat shading for meshes and polygons.
                        """
                        return PyMenu(self.service, "/display/set/lights/lighting_interpolation/flat").execute(*args, **kwargs)
                    def gouraud(self, *args, **kwargs):
                        """
                        Uses Gouraud shading to calculate the color at each vertex of a polygon and interpolates it in the interior.
                        """
                        return PyMenu(self.service, "/display/set/lights/lighting_interpolation/gouraud").execute(*args, **kwargs)
                    def phong(self, *args, **kwargs):
                        """
                        Uses Phong shading to interpolate the normals for each pixel of a polygon and computes a color at every pixel.
                        """
                        return PyMenu(self.service, "/display/set/lights/lighting_interpolation/phong").execute(*args, **kwargs)

            class rendering_options(metaclass=PyMenuMeta):
                """
                Contains the commands that enable you to set options that determine how the scene is rendered. 
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def auto_spin(self, *args, **kwargs):
                    """
                    Enables mouse view rotations to continue to spin the display after the button is released. 
                    """
                    return PyMenu(self.service, "/display/set/rendering_options/auto_spin").execute(*args, **kwargs)
                def device_info(self, *args, **kwargs):
                    """
                    Prints out information about your graphics driver. 
                    """
                    return PyMenu(self.service, "/display/set/rendering_options/device_info").execute(*args, **kwargs)
                def double_buffering(self, *args, **kwargs):
                    """
                    Enables or disables double buffering. Double buffering dramatically reduces screen flicker during graphics updates. If your display hardware does not support double buffering and you turn this option on, double buffering will be done in software. Software double buffering uses extra memory. 
                    """
                    return PyMenu(self.service, "/display/set/rendering_options/double_buffering").execute(*args, **kwargs)
                def driver(self, *args, **kwargs):
                    """
                    Changes the current graphics driver. When enabling graphics display, you have various options: for Linux, the available drivers include opengl and x11; for Windows, the available drivers include opengl, dx11 (for DirectX 11), and msw (for Microsoft Windows). You can also disable the graphics display window by entering null. For a comprehensive list of the drivers available to you, press the Enter key at the driver> prompt.  For any session that displays graphics in a graphics window and/or saves picture files, having the driver set to x11, msw, or null will cause the rendering / saving speed to be significantly slower.
                    """
                    return PyMenu(self.service, "/display/set/rendering_options/driver").execute(*args, **kwargs)
                def hidden_surfaces(self, *args, **kwargs):
                    """
                    Enables/disables the display of hidden surfaces. 
                    """
                    return PyMenu(self.service, "/display/set/rendering_options/hidden_surfaces").execute(*args, **kwargs)
                def hidden_surface_method(self, *args, **kwargs):
                    """
                    Enables you to choose from among the hidden surface removal methods that are supported. These options (listed below) are display hardware dependent. 
                    """
                    return PyMenu(self.service, "/display/set/rendering_options/hidden_surface_method").execute(*args, **kwargs)
                def outer_face_cull(self, *args, **kwargs):
                    """
                    Enables/disables the display of outer faces. 
                    """
                    return PyMenu(self.service, "/display/set/rendering_options/outer_face_cull").execute(*args, **kwargs)
                def surface_edge_visibility(self, *args, **kwargs):
                    """
                    Controls whether or not the mesh edges are drawn. 
                    """
                    return PyMenu(self.service, "/display/set/rendering_options/surface_edge_visibility").execute(*args, **kwargs)
                def animation_option(self, *args, **kwargs):
                    """
                    Enables you to specify the animation option as appropriate. 
                    """
                    return PyMenu(self.service, "/display/set/rendering_options/animation_option").execute(*args, **kwargs)
                def color_map_alignment(self, *args, **kwargs):
                    """
                    Sets the color bar alignment. 
                    """
                    return PyMenu(self.service, "/display/set/rendering_options/color_map_alignment").execute(*args, **kwargs)
                def help_text_color(self, *args, **kwargs):
                    """
                    Sets the color of the help text on the screen. You can select black, default, or white.
                    """
                    return PyMenu(self.service, "/display/set/rendering_options/help_text_color").execute(*args, **kwargs)
                def face_displacement(self, *args, **kwargs):
                    """
                    Sets the face displacement (in Z-buffer units along the camera Z-axis) for the displayed geometry when both faces and edges are displayed simultaneously. 
                    """
                    return PyMenu(self.service, "/display/set/rendering_options/face_displacement").execute(*args, **kwargs)
                def set_rendering_options(self, *args, **kwargs):
                    """
                    Sets the rendering options. 
                    """
                    return PyMenu(self.service, "/display/set/rendering_options/set_rendering_options").execute(*args, **kwargs)
                def show_colormap(self, *args, **kwargs):
                    """
                    Enable/Disable colormap.
                    """
                    return PyMenu(self.service, "/display/set/rendering_options/show_colormap").execute(*args, **kwargs)

            class styles(metaclass=PyMenuMeta):
                """
                Contains commands for setting the display style for the different types of nodes and faces that can be displayed. 
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def cell_quality(self, *args, **kwargs):
                    """
                    Indicates cells within the specified cell quality range. 
                    """
                    return PyMenu(self.service, "/display/set/styles/cell_quality").execute(*args, **kwargs)
                def cell_size(self, *args, **kwargs):
                    """
                    Indicates cells within the specified cell size range. 
                    """
                    return PyMenu(self.service, "/display/set/styles/cell_size").execute(*args, **kwargs)
                def dummy(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/display/set/styles/dummy").execute(*args, **kwargs)
                def face_quality(self, *args, **kwargs):
                    """
                    Indicates faces within the specified face quality range. 
                    """
                    return PyMenu(self.service, "/display/set/styles/face_quality").execute(*args, **kwargs)
                def face_size(self, *args, **kwargs):
                    """
                    Indicates faces within the specified face size range. 
                    """
                    return PyMenu(self.service, "/display/set/styles/face_size").execute(*args, **kwargs)
                def free(self, *args, **kwargs):
                    """
                    Indicates free nodes or faces. 
                    """
                    return PyMenu(self.service, "/display/set/styles/free").execute(*args, **kwargs)
                def left_handed(self, *args, **kwargs):
                    """
                    Indicates faces that do not follow the right-hand rule with respect to their cell neighbors. 
                    """
                    return PyMenu(self.service, "/display/set/styles/left_handed").execute(*args, **kwargs)
                def mark(self, *args, **kwargs):
                    """
                    Indicates marked objects (for expert users). 
                    """
                    return PyMenu(self.service, "/display/set/styles/mark").execute(*args, **kwargs)
                def multi(self, *args, **kwargs):
                    """
                    Indicates multiply-connected nodes or faces. 
                    """
                    return PyMenu(self.service, "/display/set/styles/multi").execute(*args, **kwargs)
                def refine(self, *args, **kwargs):
                    """
                    Indicates boundary faces to be refined. 
                    """
                    return PyMenu(self.service, "/display/set/styles/refine").execute(*args, **kwargs)
                def tag(self, *args, **kwargs):
                    """
                    Indicates tagged objects (for expert users). 
                    """
                    return PyMenu(self.service, "/display/set/styles/tag").execute(*args, **kwargs)
                def unmeshed(self, *args, **kwargs):
                    """
                    Indicates unmeshed nodes or faces. 
                    """
                    return PyMenu(self.service, "/display/set/styles/unmeshed").execute(*args, **kwargs)
                def unused(self, *args, **kwargs):
                    """
                    Indicates unused nodes or faces. 
                    """
                    return PyMenu(self.service, "/display/set/styles/unused").execute(*args, **kwargs)

            class windows(metaclass=PyMenuMeta):
                """
                Enters the windows options menu, which contains commands that enable you to customize the relative positions of sub-windows inside the active graphics window. 
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                    self.axes = self.__class__.axes(path + [("axes", None)], service)
                    self.main = self.__class__.main(path + [("main", None)], service)
                    self.scale = self.__class__.scale(path + [("scale", None)], service)
                    self.text = self.__class__.text(path + [("text", None)], service)
                    self.video = self.__class__.video(path + [("video", None)], service)
                    self.xy = self.__class__.xy(path + [("xy", None)], service)
                def aspect_ratio(self, *args, **kwargs):
                    """
                    Sets the aspect ratio of the active window. 
                    """
                    return PyMenu(self.service, "/display/set/windows/aspect_ratio").execute(*args, **kwargs)
                def logo(self, *args, **kwargs):
                    """
                    Enable/disable visibility of the logo in graphics window.
                    """
                    return PyMenu(self.service, "/display/set/windows/logo").execute(*args, **kwargs)
                def ruler(self, *args, **kwargs):
                    """
                    Turns the ruler on/off. Note that if you are running Fluent in 3D, then the view must be set toorthographic.
                    """
                    return PyMenu(self.service, "/display/set/windows/ruler").execute(*args, **kwargs)
                def logo_color(self, *args, **kwargs):
                    """
                    Set logo color to white/black.
                    """
                    return PyMenu(self.service, "/display/set/windows/logo_color").execute(*args, **kwargs)

                class axes(metaclass=PyMenuMeta):
                    """
                    Enters the axes window options menu.
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                    def border(self, *args, **kwargs):
                        """
                        Sets whether or not to draw a border around the axes window. 
                        """
                        return PyMenu(self.service, "/display/set/windows/axes/border").execute(*args, **kwargs)
                    def bottom(self, *args, **kwargs):
                        """
                        Sets the bottom boundary of the axes window. 
                        """
                        return PyMenu(self.service, "/display/set/windows/axes/bottom").execute(*args, **kwargs)
                    def clear(self, *args, **kwargs):
                        """
                        Sets the transparency of the axes window. 
                        """
                        return PyMenu(self.service, "/display/set/windows/axes/clear").execute(*args, **kwargs)
                    def right(self, *args, **kwargs):
                        """
                        Sets the right boundary of the axes window. 
                        """
                        return PyMenu(self.service, "/display/set/windows/axes/right").execute(*args, **kwargs)
                    def visible(self, *args, **kwargs):
                        """
                        Controls the visibility of the axes window. 
                        """
                        return PyMenu(self.service, "/display/set/windows/axes/visible").execute(*args, **kwargs)

                class main(metaclass=PyMenuMeta):
                    """
                    Enters the main view window options menu. 
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                    def border(self, *args, **kwargs):
                        """
                        Sets whether or not to draw a border around the main viewing window. 
                        """
                        return PyMenu(self.service, "/display/set/windows/main/border").execute(*args, **kwargs)
                    def bottom(self, *args, **kwargs):
                        """
                        Sets the bottom boundary of the main viewing window. 
                        """
                        return PyMenu(self.service, "/display/set/windows/main/bottom").execute(*args, **kwargs)
                    def left(self, *args, **kwargs):
                        """
                        Sets the left boundary of the main viewing window. 
                        """
                        return PyMenu(self.service, "/display/set/windows/main/left").execute(*args, **kwargs)
                    def right(self, *args, **kwargs):
                        """
                        Sets the right boundary of the main viewing window. 
                        """
                        return PyMenu(self.service, "/display/set/windows/main/right").execute(*args, **kwargs)
                    def top(self, *args, **kwargs):
                        """
                        Sets the top boundary of the main viewing window. 
                        """
                        return PyMenu(self.service, "/display/set/windows/main/top").execute(*args, **kwargs)
                    def visible(self, *args, **kwargs):
                        """
                        Controls the visibility of the main viewing window. 
                        """
                        return PyMenu(self.service, "/display/set/windows/main/visible").execute(*args, **kwargs)

                class scale(metaclass=PyMenuMeta):
                    """
                    Enters the color scale window options menu. 
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                    def border(self, *args, **kwargs):
                        """
                        Sets whether or not to draw a border around the color scale window. 
                        """
                        return PyMenu(self.service, "/display/set/windows/scale/border").execute(*args, **kwargs)
                    def bottom(self, *args, **kwargs):
                        """
                        Sets the bottom boundary of the color scale window. 
                        """
                        return PyMenu(self.service, "/display/set/windows/scale/bottom").execute(*args, **kwargs)
                    def clear(self, *args, **kwargs):
                        """
                        Sets the transparency of the color scale window. 
                        """
                        return PyMenu(self.service, "/display/set/windows/scale/clear").execute(*args, **kwargs)
                    def format(self, *args, **kwargs):
                        """
                        Sets the number format of the color scale window (for example, percentage0.2e). 
                        """
                        return PyMenu(self.service, "/display/set/windows/scale/format").execute(*args, **kwargs)
                    def font_size(self, *args, **kwargs):
                        """
                        Sets the font size of the color scale window. 
                        """
                        return PyMenu(self.service, "/display/set/windows/scale/font_size").execute(*args, **kwargs)
                    def left(self, *args, **kwargs):
                        """
                        Sets the left boundary of the color scale window. 
                        """
                        return PyMenu(self.service, "/display/set/windows/scale/left").execute(*args, **kwargs)
                    def margin(self, *args, **kwargs):
                        """
                        Sets the margin of the color scale window. 
                        """
                        return PyMenu(self.service, "/display/set/windows/scale/margin").execute(*args, **kwargs)
                    def right(self, *args, **kwargs):
                        """
                        Sets the right boundary of the color scale window. 
                        """
                        return PyMenu(self.service, "/display/set/windows/scale/right").execute(*args, **kwargs)
                    def top(self, *args, **kwargs):
                        """
                        Sets the top boundary of the color scale window. 
                        """
                        return PyMenu(self.service, "/display/set/windows/scale/top").execute(*args, **kwargs)
                    def visible(self, *args, **kwargs):
                        """
                        Controls the visibility of the color scale window. 
                        """
                        return PyMenu(self.service, "/display/set/windows/scale/visible").execute(*args, **kwargs)
                    def alignment(self, *args, **kwargs):
                        """
                        Sets the colormap position to the bottom, left, top, or right.
                        """
                        return PyMenu(self.service, "/display/set/windows/scale/alignment").execute(*args, **kwargs)

                class text(metaclass=PyMenuMeta):
                    """
                    Enters the text window options menu. 
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                    def application(self, *args, **kwargs):
                        """
                        Shows or hides the application name in the picture. 
                        """
                        return PyMenu(self.service, "/display/set/windows/text/application").execute(*args, **kwargs)
                    def border(self, *args, **kwargs):
                        """
                        Sets whether or not to draw a border around the text window. 
                        """
                        return PyMenu(self.service, "/display/set/windows/text/border").execute(*args, **kwargs)
                    def bottom(self, *args, **kwargs):
                        """
                        Sets the bottom boundary of the text window. 
                        """
                        return PyMenu(self.service, "/display/set/windows/text/bottom").execute(*args, **kwargs)
                    def clear(self, *args, **kwargs):
                        """
                        Enables/disables the transparency of the text window. 
                        """
                        return PyMenu(self.service, "/display/set/windows/text/clear").execute(*args, **kwargs)
                    def company(self, *args, **kwargs):
                        """
                        Shows or hides the company name in the picture. 
                        """
                        return PyMenu(self.service, "/display/set/windows/text/company").execute(*args, **kwargs)
                    def date(self, *args, **kwargs):
                        """
                        Shows or hides the date in the picture. 
                        """
                        return PyMenu(self.service, "/display/set/windows/text/date").execute(*args, **kwargs)
                    def left(self, *args, **kwargs):
                        """
                        Sets the left boundary of the text window. 
                        """
                        return PyMenu(self.service, "/display/set/windows/text/left").execute(*args, **kwargs)
                    def right(self, *args, **kwargs):
                        """
                        Sets the right boundary of the text window. 
                        """
                        return PyMenu(self.service, "/display/set/windows/text/right").execute(*args, **kwargs)
                    def top(self, *args, **kwargs):
                        """
                        Sets the top boundary of the text window. 
                        """
                        return PyMenu(self.service, "/display/set/windows/text/top").execute(*args, **kwargs)
                    def visible(self, *args, **kwargs):
                        """
                        Controls the visibility of the text window. 
                        """
                        return PyMenu(self.service, "/display/set/windows/text/visible").execute(*args, **kwargs)

                class video(metaclass=PyMenuMeta):
                    """
                    Contains options for modifying a video. This menu is not relevant for the meshing mode. 
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                    def background(self, *args, **kwargs):
                        """
                        Sets the background color of the graphics window. The color is specified as a string of three comma-separated numbers between 0 and 1, representing red, green, and blue. For example, to change the background from black (default) to gray, you would enter ".5,.5,.5" after selecting the background command. 
                        """
                        return PyMenu(self.service, "/display/set/windows/video/background").execute(*args, **kwargs)
                    def color_filter(self, *args, **kwargs):
                        """
                        Sets the video color filter. For example, to change the color filter from its default setting  to PAL video with a saturation of 80percentage and a brightness of 90percentage, you would  enter "video=pal,sat=.8,gain=.9" after selecting the color-filter command. 
                        """
                        return PyMenu(self.service, "/display/set/windows/video/color_filter").execute(*args, **kwargs)
                    def foreground(self, *args, **kwargs):
                        """
                        Sets the foreground (text) color of the graphics window. The color is specified as a string of three comma-separated numbers between 0 and 1, representing red, green, and blue. For example, to change the foreground from white (default) to gray, you would enter ".5,.5,.5" after selecting the foreground command. 
                        """
                        return PyMenu(self.service, "/display/set/windows/video/foreground").execute(*args, **kwargs)
                    def on(self, *args, **kwargs):
                        """
                        Enables or disables the video picture settings. 
                        """
                        return PyMenu(self.service, "/display/set/windows/video/on").execute(*args, **kwargs)
                    def pixel_size(self, *args, **kwargs):
                        """
                        Sets the window size in pixels. 
                        """
                        return PyMenu(self.service, "/display/set/windows/video/pixel_size").execute(*args, **kwargs)

                class xy(metaclass=PyMenuMeta):
                    """
                    Enters the XY plot window options menu. 
                    """
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                    def border(self, *args, **kwargs):
                        """
                        Sets whether or not to draw a border around the XY plot window. 
                        """
                        return PyMenu(self.service, "/display/set/windows/xy/border").execute(*args, **kwargs)
                    def bottom(self, *args, **kwargs):
                        """
                        Sets the bottom boundary of the XY plot window. 
                        """
                        return PyMenu(self.service, "/display/set/windows/xy/bottom").execute(*args, **kwargs)
                    def left(self, *args, **kwargs):
                        """
                        Sets the left boundary of the XY plot window. 
                        """
                        return PyMenu(self.service, "/display/set/windows/xy/left").execute(*args, **kwargs)
                    def right(self, *args, **kwargs):
                        """
                        Sets the right boundary of the XY plot window. 
                        """
                        return PyMenu(self.service, "/display/set/windows/xy/right").execute(*args, **kwargs)
                    def top(self, *args, **kwargs):
                        """
                        Sets the top boundary of the XY plot window. 
                        """
                        return PyMenu(self.service, "/display/set/windows/xy/top").execute(*args, **kwargs)
                    def visible(self, *args, **kwargs):
                        """
                        Controls the visibility of the XY plot window. 
                        """
                        return PyMenu(self.service, "/display/set/windows/xy/visible").execute(*args, **kwargs)

        class set_grid(metaclass=PyMenuMeta):
            """
            Contains options controlling the display of the grid. 
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def all_cells(self, *args, **kwargs):
                """
                Enables/disables the display of all cells. 
                """
                return PyMenu(self.service, "/display/set_grid/all_cells").execute(*args, **kwargs)
            def all_faces(self, *args, **kwargs):
                """
                Enables/disables the display of all faces. 
                """
                return PyMenu(self.service, "/display/set_grid/all_faces").execute(*args, **kwargs)
            def all_nodes(self, *args, **kwargs):
                """
                Enables/disables the display of all nodes. 
                """
                return PyMenu(self.service, "/display/set_grid/all_nodes").execute(*args, **kwargs)
            def free(self, *args, **kwargs):
                """
                Enables/disables the drawing of faces/nodes that have no neighboring face on at least one edge. 
                """
                return PyMenu(self.service, "/display/set_grid/free").execute(*args, **kwargs)
            def left_handed(self, *args, **kwargs):
                """
                Enables/disables the display of left-handed faces. 
                """
                return PyMenu(self.service, "/display/set_grid/left_handed").execute(*args, **kwargs)
            def multi(self, *args, **kwargs):
                """
                Enables/disables the display of those faces/nodes that have more than one neighboring face on an edge. 
                """
                return PyMenu(self.service, "/display/set_grid/multi").execute(*args, **kwargs)
            def refine(self, *args, **kwargs):
                """
                Enables/disables the display of those faces that have been marked for refinement. 
                """
                return PyMenu(self.service, "/display/set_grid/refine").execute(*args, **kwargs)
            def unmeshed(self, *args, **kwargs):
                """
                Enables/disables the display of nodes and faces that have not been meshed. 
                """
                return PyMenu(self.service, "/display/set_grid/unmeshed").execute(*args, **kwargs)
            def unused(self, *args, **kwargs):
                """
                Enables/disables the display of unused nodes. 
                """
                return PyMenu(self.service, "/display/set_grid/unused").execute(*args, **kwargs)
            def marked(self, *args, **kwargs):
                """
                Enables/disables the display of marked nodes. 
                """
                return PyMenu(self.service, "/display/set_grid/marked").execute(*args, **kwargs)
            def tagged(self, *args, **kwargs):
                """
                Enables/disables the display of tagged nodes. 
                """
                return PyMenu(self.service, "/display/set_grid/tagged").execute(*args, **kwargs)
            def face_quality(self, *args, **kwargs):
                """
                Sets the lower and upper bounds of quality for faces to be displayed. Only faces with a quality measure value (for example, skewness) within the specified range will be displayed. 
                """
                return PyMenu(self.service, "/display/set_grid/face_quality").execute(*args, **kwargs)
            def cell_quality(self, *args, **kwargs):
                """
                Sets the lower and upper bounds of quality for cells to be displayed. Only cells with a quality measure value (for example, skewness) within the specified range will be displayed. 
                """
                return PyMenu(self.service, "/display/set_grid/cell_quality").execute(*args, **kwargs)
            def neighborhood(self, *args, **kwargs):
                """
                Sets the x, y, and z range to be within a specified neighborhood of a specified grid object. 
                """
                return PyMenu(self.service, "/display/set_grid/neighborhood").execute(*args, **kwargs)
            def x_range(self, *args, **kwargs):
                """
                Limits the display of grid objects to the specified x-range. 
                """
                return PyMenu(self.service, "/display/set_grid/x_range").execute(*args, **kwargs)
            def y_range(self, *args, **kwargs):
                """
                Limits the display of grid objects to the specified y-range. 
                """
                return PyMenu(self.service, "/display/set_grid/y_range").execute(*args, **kwargs)
            def z_range(self, *args, **kwargs):
                """
                Limits the display of grid objects to the specified z-range. 
                """
                return PyMenu(self.service, "/display/set_grid/z_range").execute(*args, **kwargs)
            def normals(self, *args, **kwargs):
                """
                Enables/disables the display of face normals. 
                """
                return PyMenu(self.service, "/display/set_grid/normals").execute(*args, **kwargs)
            def normal_scale(self, *args, **kwargs):
                """
                Sets the scale factor for face normals. 
                """
                return PyMenu(self.service, "/display/set_grid/normal_scale").execute(*args, **kwargs)
            def labels(self, *args, **kwargs):
                """
                Enables/disables the display of labels. 
                """
                return PyMenu(self.service, "/display/set_grid/labels").execute(*args, **kwargs)
            def label_alignment(self, *args, **kwargs):
                """
                Sets the alignment of labels that appear in the graphics window. By default, the label is centered on the node, cell, and so on, to which the label refers. You can specify *,ˆ, v, <, > for center, top, bottom, left, or right. You can also combine symbols—for example, "*v" for bottom center. 
                """
                return PyMenu(self.service, "/display/set_grid/label_alignment").execute(*args, **kwargs)
            def label_font(self, *args, **kwargs):
                """
                Sets the label font. By default, all labels appear in “sans serif" font. Some other choices are roman, typewriter, and stroked. 
                """
                return PyMenu(self.service, "/display/set_grid/label_font").execute(*args, **kwargs)
            def label_scale(self, *args, **kwargs):
                """
                Scales the size of the label. 
                """
                return PyMenu(self.service, "/display/set_grid/label_scale").execute(*args, **kwargs)
            def node_size(self, *args, **kwargs):
                """
                Sets the node symbol scaling factor. 
                """
                return PyMenu(self.service, "/display/set_grid/node_size").execute(*args, **kwargs)
            def node_symbol(self, *args, **kwargs):
                """
                Specifies the node symbol. 
                """
                return PyMenu(self.service, "/display/set_grid/node_symbol").execute(*args, **kwargs)
            def list(self, *args, **kwargs):
                """
                Lists all the grid display settings. 
                """
                return PyMenu(self.service, "/display/set_grid/list").execute(*args, **kwargs)
            def default(self, *args, **kwargs):
                """
                Resets the grid display parameters to their default values. 
                """
                return PyMenu(self.service, "/display/set_grid/default").execute(*args, **kwargs)

        class views(metaclass=PyMenuMeta):
            """
            Enters the view window options menu. 
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
                self.camera = self.__class__.camera(path + [("camera", None)], service)
            def auto_scale(self, *args, **kwargs):
                """
                Scales and centers the current scene without changing its orientation. 
                """
                return PyMenu(self.service, "/display/views/auto_scale").execute(*args, **kwargs)
            def default_view(self, *args, **kwargs):
                """
                Resets the view to front and center. 
                """
                return PyMenu(self.service, "/display/views/default_view").execute(*args, **kwargs)
            def delete_view(self, *args, **kwargs):
                """
                Deletes a particular view from the list of stored views. 
                """
                return PyMenu(self.service, "/display/views/delete_view").execute(*args, **kwargs)
            def last_view(self, *args, **kwargs):
                """
                Returns to the camera position before the last manipulation. 
                """
                return PyMenu(self.service, "/display/views/last_view").execute(*args, **kwargs)
            def next_view(self, *args, **kwargs):
                """
                Return to the camera position after the current position in the stack.
                """
                return PyMenu(self.service, "/display/views/next_view").execute(*args, **kwargs)
            def list_views(self, *args, **kwargs):
                """
                Lists all predefined and saved views. 
                """
                return PyMenu(self.service, "/display/views/list_views").execute(*args, **kwargs)
            def restore_view(self, *args, **kwargs):
                """
                Sets the current view to one of the stored views. 
                """
                return PyMenu(self.service, "/display/views/restore_view").execute(*args, **kwargs)
            def read_views(self, *args, **kwargs):
                """
                Reads views from an external view file. 
                """
                return PyMenu(self.service, "/display/views/read_views").execute(*args, **kwargs)
            def save_view(self, *args, **kwargs):
                """
                Saves the currently displayed view into the list of stored views. 
                """
                return PyMenu(self.service, "/display/views/save_view").execute(*args, **kwargs)
            def write_views(self, *args, **kwargs):
                """
                Writes views to an external view file. 
                """
                return PyMenu(self.service, "/display/views/write_views").execute(*args, **kwargs)

            class camera(metaclass=PyMenuMeta):
                """
                Contains commands to set the camera options. 
                """
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                def dolly_camera(self, *args, **kwargs):
                    """
                    Enables you to move the camera left, right, up, down, in, and out. 
                    """
                    return PyMenu(self.service, "/display/views/camera/dolly_camera").execute(*args, **kwargs)
                def field(self, *args, **kwargs):
                    """
                    Enables you to set the field of view (width and height) of the scene. 
                    """
                    return PyMenu(self.service, "/display/views/camera/field").execute(*args, **kwargs)
                def orbit_camera(self, *args, **kwargs):
                    """
                    Enables you to move the camera around the target. Gives the effect of circling around the target. 
                    """
                    return PyMenu(self.service, "/display/views/camera/orbit_camera").execute(*args, **kwargs)
                def pan_camera(self, *args, **kwargs):
                    """
                    Gives you the effect of sweeping the camera across the scene. The camera remains at its position but its target changes. 
                    """
                    return PyMenu(self.service, "/display/views/camera/pan_camera").execute(*args, **kwargs)
                def position(self, *args, **kwargs):
                    """
                    Sets the camera position. 
                    """
                    return PyMenu(self.service, "/display/views/camera/position").execute(*args, **kwargs)
                def projection(self, *args, **kwargs):
                    """
                    Lets you switch between perspective and orthographic views. 
                    """
                    return PyMenu(self.service, "/display/views/camera/projection").execute(*args, **kwargs)
                def roll_camera(self, *args, **kwargs):
                    """
                    Lets you adjust the camera up-vector. 
                    """
                    return PyMenu(self.service, "/display/views/camera/roll_camera").execute(*args, **kwargs)
                def target(self, *args, **kwargs):
                    """
                    Sets the point the camera will look at. 
                    """
                    return PyMenu(self.service, "/display/views/camera/target").execute(*args, **kwargs)
                def up_vector(self, *args, **kwargs):
                    """
                    Sets the camera up-vector. 
                    """
                    return PyMenu(self.service, "/display/views/camera/up_vector").execute(*args, **kwargs)
                def zoom_camera(self, *args, **kwargs):
                    """
                    Adjusts the camera’s field of view. This operation is similar to dollying the camera in or out of the scene. Dollying causes objects in front to move past you. Zooming changes the perspective effect in the scene (and can be disconcerting). 
                    """
                    return PyMenu(self.service, "/display/views/camera/zoom_camera").execute(*args, **kwargs)

        class display_states(metaclass=PyMenuMeta):
            """
            Enter the display states menu.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def list(self, *args, **kwargs):
                """
                Print the names of the existing display states to the console.
                """
                return PyMenu(self.service, "/display/display_states/list").execute(*args, **kwargs)
            def apply(self, *args, **kwargs):
                """
                Apply a display state to the active graphics window.
                """
                return PyMenu(self.service, "/display/display_states/apply").execute(*args, **kwargs)
            def delete(self, *args, **kwargs):
                """
                Delete a display state.
                """
                return PyMenu(self.service, "/display/display_states/delete").execute(*args, **kwargs)
            def use_active(self, *args, **kwargs):
                """
                Save the display state settings of the active graphics window to an existing display state. This command is not available when the active window is displaying a 2D plot.
                            
                """
                return PyMenu(self.service, "/display/display_states/use_active").execute(*args, **kwargs)
            def copy(self, *args, **kwargs):
                """
                Copy the settings of an existing display state to another existing display state.
                """
                return PyMenu(self.service, "/display/display_states/copy").execute(*args, **kwargs)
            def read(self, *args, **kwargs):
                """
                Read in display states from a file.
                """
                return PyMenu(self.service, "/display/display_states/read").execute(*args, **kwargs)
            def write(self, *args, **kwargs):
                """
                Write one or more of the saved display states to a file.
                """
                return PyMenu(self.service, "/display/display_states/write").execute(*args, **kwargs)
            def edit(self, *args, **kwargs):
                """
                Edit a display state. Enter quit (or a substring, such as q or qui) to exit the editing loop.
                """
                return PyMenu(self.service, "/display/display_states/edit").execute(*args, **kwargs)
            def create(self, *args, **kwargs):
                """
                Create a new display state.
                """
                return PyMenu(self.service, "/display/display_states/create").execute(*args, **kwargs)

        class xy_plot(metaclass=PyMenuMeta):
            """
            Enters the XY plot menu. 
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def file(self, *args, **kwargs):
                """
                Enables you to choose a file from which to create an xy plot. 
                """
                return PyMenu(self.service, "/display/xy_plot/file").execute(*args, **kwargs)
            def cell_distribution(self, *args, **kwargs):
                """
                Plots a histogram of cell quality. 
                """
                return PyMenu(self.service, "/display/xy_plot/cell_distribution").execute(*args, **kwargs)
            def face_distribution(self, *args, **kwargs):
                """
                Plots a histogram of face quality. 
                """
                return PyMenu(self.service, "/display/xy_plot/face_distribution").execute(*args, **kwargs)
            def set(self, *args, **kwargs):
                """
                Enters the set window options menu. 
                """
                return PyMenu(self.service, "/display/xy_plot/set").execute(*args, **kwargs)

        class update_scene(metaclass=PyMenuMeta):
            """
            Contains commands that enable you to update the scene description. 
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def select_geometry(self, *args, **kwargs):
                """
                Enables you to select the geometry to be updated. 
                """
                return PyMenu(self.service, "/display/update_scene/select_geometry").execute(*args, **kwargs)
            def overlays(self, *args, **kwargs):
                """
                Enables/disables the overlays option. 
                """
                return PyMenu(self.service, "/display/update_scene/overlays").execute(*args, **kwargs)
            def draw_frame(self, *args, **kwargs):
                """
                Enables/disables the drawing of the bounding frame. 
                """
                return PyMenu(self.service, "/display/update_scene/draw_frame").execute(*args, **kwargs)
            def delete(self, *args, **kwargs):
                """
                Deletes the geometry selected using the select-geometry command. 
                """
                return PyMenu(self.service, "/display/update_scene/delete").execute(*args, **kwargs)
            def display(self, *args, **kwargs):
                """
                Displays the geometry selected using the select-geometry command. 
                """
                return PyMenu(self.service, "/display/update_scene/display").execute(*args, **kwargs)
            def transform(self, *args, **kwargs):
                """
                Enables you to apply the transformation matrix to the geometry selected using the select-geometry command. 
                """
                return PyMenu(self.service, "/display/update_scene/transform").execute(*args, **kwargs)
            def pathline(self, *args, **kwargs):
                """
                Changes pathline attributes.
                """
                return PyMenu(self.service, "/display/update_scene/pathline").execute(*args, **kwargs)
            def iso_sweep(self, *args, **kwargs):
                """
                Changes iso-sweep values.
                """
                return PyMenu(self.service, "/display/update_scene/iso_sweep").execute(*args, **kwargs)
            def time(self, *args, **kwargs):
                """
                Changes time-step value.
                """
                return PyMenu(self.service, "/display/update_scene/time").execute(*args, **kwargs)
            def set_frame(self, *args, **kwargs):
                """
                Enables you to change the frame options. 
                """
                return PyMenu(self.service, "/display/update_scene/set_frame").execute(*args, **kwargs)

        class objects(metaclass=PyMenuMeta):
            """
            Contains commands for displaying objects.
            """
            is_extended_tui = True
            def __init__(self, path, service):
                self.path = path
                self.service = service
                self.xy_plot = self.__class__.xy_plot(path + [("xy_plot", None)], None, service)
                self.mesh = self.__class__.mesh(path + [("mesh", None)], None, service)
                self.contour = self.__class__.contour(path + [("contour", None)], None, service)
                self.vector = self.__class__.vector(path + [("vector", None)], None, service)
                self.pathlines = self.__class__.pathlines(path + [("pathlines", None)], None, service)
                self.particle_tracks = self.__class__.particle_tracks(path + [("particle_tracks", None)], None, service)
                self.scene = self.__class__.scene(path + [("scene", None)], None, service)
            def show_all(self, *args, **kwargs):
                """
                Unhides all the objects in the geometry and displays them.
                """
                return PyMenu(self.service, "/display/objects/show_all").execute(*args, **kwargs)
            def explode(self, *args, **kwargs):
                """
                Explodes the objects in the geometry. (This command is valid only when the geometry is an assembled mode.)
                """
                return PyMenu(self.service, "/display/objects/explode").execute(*args, **kwargs)
            def toggle_color_palette(self, *args, **kwargs):
                """
                Toggles the color palette of the geometry.
                """
                return PyMenu(self.service, "/display/objects/toggle_color_palette").execute(*args, **kwargs)
            def implode(self, *args, **kwargs):
                """
                Implodes or assembles the objects in the geometry. (This command is available only when the geometry is an exploded mode.)
                """
                return PyMenu(self.service, "/display/objects/implode").execute(*args, **kwargs)
            def display_similar_area(self, *args, **kwargs):
                """
                Displays the objects with similar area to the selected object area.
                """
                return PyMenu(self.service, "/display/objects/display_similar_area").execute(*args, **kwargs)
            def toggle_color_mode(self, *args, **kwargs):
                """
                Toggles the colors of the geometry. In one mode geometry is colored object-wise while in the other mode it is colored zone-wise.
                """
                return PyMenu(self.service, "/display/objects/toggle_color_mode").execute(*args, **kwargs)
            def make_transparent(self, *args, **kwargs):
                """
                Makes the geometry transparent so that internal objects are visible. This command works as a toggle undoing the transparency of the previously selected objects.
                """
                return PyMenu(self.service, "/display/objects/make_transparent").execute(*args, **kwargs)
            def select_all_visible(self, *args, **kwargs):
                """
                Selects all the visible objects in the graphics window.
                """
                return PyMenu(self.service, "/display/objects/select_all_visible").execute(*args, **kwargs)
            def display_neighborhood(self, *args, **kwargs):
                """
                Displays the objects that are in the neighborhood of the selected object. The neighboring objects have to be in contact, or intersecting the selected object.
                """
                return PyMenu(self.service, "/display/objects/display_neighborhood").execute(*args, **kwargs)
            def hide_objects(self, *args, **kwargs):
                """
                Hides the selected objects in the display.
                """
                return PyMenu(self.service, "/display/objects/hide_objects").execute(*args, **kwargs)
            def isolate_objects(self, *args, **kwargs):
                """
                Displays only the selected objects.
                """
                return PyMenu(self.service, "/display/objects/isolate_objects").execute(*args, **kwargs)

            class xy_plot(metaclass=PyNamedObjectMeta):
                """
                """
                is_extended_tui = True
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                    self.name = self.__class__.name(path + [("name", None)], service)
                    self.uid = self.__class__.uid(path + [("uid", None)], service)
                    self.options = self.__class__.options(path + [("options", None)], service)
                    self.plot_direction = self.__class__.plot_direction(path + [("plot_direction", None)], service)
                    self.x_axis_function = self.__class__.x_axis_function(path + [("x_axis_function", None)], service)
                    self.y_axis_function = self.__class__.y_axis_function(path + [("y_axis_function", None)], service)
                    self.surfaces_list = self.__class__.surfaces_list(path + [("surfaces_list", None)], service)
                    self.physics = self.__class__.physics(path + [("physics", None)], service)
                    self.geometry = self.__class__.geometry(path + [("geometry", None)], service)
                    self.surfaces = self.__class__.surfaces(path + [("surfaces", None)], service)

                class name(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class uid(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class options(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                        self.node_values = self.__class__.node_values(path + [("node_values", None)], service)
                        self.position_on_x_axis = self.__class__.position_on_x_axis(path + [("position_on_x_axis", None)], service)
                        self.position_on_y_axis = self.__class__.position_on_y_axis(path + [("position_on_y_axis", None)], service)

                    class node_values(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class position_on_x_axis(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class position_on_y_axis(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                class plot_direction(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                        self.direction_vector = self.__class__.direction_vector(path + [("direction_vector", None)], service)
                        self.curve_length = self.__class__.curve_length(path + [("curve_length", None)], service)

                    class direction_vector(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service
                            self.x_component = self.__class__.x_component(path + [("x_component", None)], service)
                            self.y_component = self.__class__.y_component(path + [("y_component", None)], service)
                            self.z_component = self.__class__.z_component(path + [("z_component", None)], service)

                        class x_component(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                        class y_component(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                        class z_component(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                    class curve_length(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service
                            self.default = self.__class__.default(path + [("default", None)], service)
                            self.reverse = self.__class__.reverse(path + [("reverse", None)], service)

                        class default(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                        class reverse(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                class x_axis_function(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class y_axis_function(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class surfaces_list(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class physics(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class geometry(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class surfaces(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

            class mesh(metaclass=PyNamedObjectMeta):
                """
                """
                is_extended_tui = True
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                    self.name = self.__class__.name(path + [("name", None)], service)
                    self.options = self.__class__.options(path + [("options", None)], service)
                    self.edge_type = self.__class__.edge_type(path + [("edge_type", None)], service)
                    self.shrink_factor = self.__class__.shrink_factor(path + [("shrink_factor", None)], service)
                    self.surfaces_list = self.__class__.surfaces_list(path + [("surfaces_list", None)], service)
                    self.coloring = self.__class__.coloring(path + [("coloring", None)], service)
                    self.display_state_name = self.__class__.display_state_name(path + [("display_state_name", None)], service)
                    self.physics = self.__class__.physics(path + [("physics", None)], service)
                    self.geometry = self.__class__.geometry(path + [("geometry", None)], service)
                    self.surfaces = self.__class__.surfaces(path + [("surfaces", None)], service)

                class name(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class options(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                        self.nodes = self.__class__.nodes(path + [("nodes", None)], service)
                        self.edges = self.__class__.edges(path + [("edges", None)], service)
                        self.faces = self.__class__.faces(path + [("faces", None)], service)
                        self.partitions = self.__class__.partitions(path + [("partitions", None)], service)
                        self.overset = self.__class__.overset(path + [("overset", None)], service)
                        self.gap = self.__class__.gap(path + [("gap", None)], service)

                    class nodes(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class edges(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class faces(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class partitions(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class overset(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class gap(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                class edge_type(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                        self.all = self.__class__.all(path + [("all", None)], service)
                        self.feature = self.__class__.feature(path + [("feature", None)], service)
                        self.outline = self.__class__.outline(path + [("outline", None)], service)

                    class all(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class feature(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service
                            self.feature_angle = self.__class__.feature_angle(path + [("feature_angle", None)], service)

                        class feature_angle(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                    class outline(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                class shrink_factor(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class surfaces_list(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class coloring(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                        self.automatic = self.__class__.automatic(path + [("automatic", None)], service)
                        self.manual = self.__class__.manual(path + [("manual", None)], service)

                    class automatic(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service
                            self.type = self.__class__.type(path + [("type", None)], service)
                            self.id = self.__class__.id(path + [("id", None)], service)
                            self.normal = self.__class__.normal(path + [("normal", None)], service)
                            self.partition = self.__class__.partition(path + [("partition", None)], service)

                        class type(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                        class id(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                        class normal(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                        class partition(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                    class manual(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service
                            self.faces = self.__class__.faces(path + [("faces", None)], service)
                            self.edges = self.__class__.edges(path + [("edges", None)], service)
                            self.nodes = self.__class__.nodes(path + [("nodes", None)], service)
                            self.material_color = self.__class__.material_color(path + [("material_color", None)], service)

                        class faces(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                        class edges(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                        class nodes(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                        class material_color(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                class display_state_name(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class physics(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class geometry(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class surfaces(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

            class contour(metaclass=PyNamedObjectMeta):
                """
                """
                is_extended_tui = True
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                    self.name = self.__class__.name(path + [("name", None)], service)
                    self.field = self.__class__.field(path + [("field", None)], service)
                    self.filled = self.__class__.filled(path + [("filled", None)], service)
                    self.boundary_values = self.__class__.boundary_values(path + [("boundary_values", None)], service)
                    self.contour_lines = self.__class__.contour_lines(path + [("contour_lines", None)], service)
                    self.node_values = self.__class__.node_values(path + [("node_values", None)], service)
                    self.surfaces_list = self.__class__.surfaces_list(path + [("surfaces_list", None)], service)
                    self.range_option = self.__class__.range_option(path + [("range_option", None)], service)
                    self.coloring = self.__class__.coloring(path + [("coloring", None)], service)
                    self.color_map = self.__class__.color_map(path + [("color_map", None)], service)
                    self.draw_mesh = self.__class__.draw_mesh(path + [("draw_mesh", None)], service)
                    self.mesh_object = self.__class__.mesh_object(path + [("mesh_object", None)], service)
                    self.display_state_name = self.__class__.display_state_name(path + [("display_state_name", None)], service)
                    self.physics = self.__class__.physics(path + [("physics", None)], service)
                    self.geometry = self.__class__.geometry(path + [("geometry", None)], service)
                    self.surfaces = self.__class__.surfaces(path + [("surfaces", None)], service)

                class name(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class field(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class filled(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class boundary_values(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class contour_lines(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class node_values(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class surfaces_list(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class range_option(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                        self.auto_range_on = self.__class__.auto_range_on(path + [("auto_range_on", None)], service)
                        self.auto_range_off = self.__class__.auto_range_off(path + [("auto_range_off", None)], service)

                    class auto_range_on(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service
                            self.global_range = self.__class__.global_range(path + [("global_range", None)], service)

                        class global_range(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                    class auto_range_off(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service
                            self.clip_to_range = self.__class__.clip_to_range(path + [("clip_to_range", None)], service)
                            self.minimum = self.__class__.minimum(path + [("minimum", None)], service)
                            self.maximum = self.__class__.maximum(path + [("maximum", None)], service)

                        class clip_to_range(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                        class minimum(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                        class maximum(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                class coloring(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                        self.smooth = self.__class__.smooth(path + [("smooth", None)], service)
                        self.banded = self.__class__.banded(path + [("banded", None)], service)

                    class smooth(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class banded(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                class color_map(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                        self.visible = self.__class__.visible(path + [("visible", None)], service)
                        self.size = self.__class__.size(path + [("size", None)], service)
                        self.color = self.__class__.color(path + [("color", None)], service)
                        self.log_scale = self.__class__.log_scale(path + [("log_scale", None)], service)
                        self.format = self.__class__.format(path + [("format", None)], service)
                        self.user_skip = self.__class__.user_skip(path + [("user_skip", None)], service)
                        self.show_all = self.__class__.show_all(path + [("show_all", None)], service)
                        self.position = self.__class__.position(path + [("position", None)], service)
                        self.font_name = self.__class__.font_name(path + [("font_name", None)], service)
                        self.font_automatic = self.__class__.font_automatic(path + [("font_automatic", None)], service)
                        self.font_size = self.__class__.font_size(path + [("font_size", None)], service)
                        self.length = self.__class__.length(path + [("length", None)], service)
                        self.width = self.__class__.width(path + [("width", None)], service)

                    class visible(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class size(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class color(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class log_scale(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class format(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class user_skip(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class show_all(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class position(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class font_name(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class font_automatic(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class font_size(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class length(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class width(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                class draw_mesh(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class mesh_object(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class display_state_name(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class physics(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class geometry(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class surfaces(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

            class vector(metaclass=PyNamedObjectMeta):
                """
                """
                is_extended_tui = True
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                    self.name = self.__class__.name(path + [("name", None)], service)
                    self.field = self.__class__.field(path + [("field", None)], service)
                    self.vector_field = self.__class__.vector_field(path + [("vector_field", None)], service)
                    self.surfaces_list = self.__class__.surfaces_list(path + [("surfaces_list", None)], service)
                    self.scale = self.__class__.scale(path + [("scale", None)], service)
                    self.style = self.__class__.style(path + [("style", None)], service)
                    self.skip = self.__class__.skip(path + [("skip", None)], service)
                    self.vector_opt = self.__class__.vector_opt(path + [("vector_opt", None)], service)
                    self.range_option = self.__class__.range_option(path + [("range_option", None)], service)
                    self.color_map = self.__class__.color_map(path + [("color_map", None)], service)
                    self.draw_mesh = self.__class__.draw_mesh(path + [("draw_mesh", None)], service)
                    self.mesh_object = self.__class__.mesh_object(path + [("mesh_object", None)], service)
                    self.display_state_name = self.__class__.display_state_name(path + [("display_state_name", None)], service)
                    self.physics = self.__class__.physics(path + [("physics", None)], service)
                    self.geometry = self.__class__.geometry(path + [("geometry", None)], service)
                    self.surfaces = self.__class__.surfaces(path + [("surfaces", None)], service)

                class name(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class field(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class vector_field(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class surfaces_list(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class scale(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                        self.auto_scale = self.__class__.auto_scale(path + [("auto_scale", None)], service)
                        self.scale_f = self.__class__.scale_f(path + [("scale_f", None)], service)

                    class auto_scale(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class scale_f(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                class style(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class skip(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class vector_opt(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                        self.in_plane = self.__class__.in_plane(path + [("in_plane", None)], service)
                        self.fixed_length = self.__class__.fixed_length(path + [("fixed_length", None)], service)
                        self.x_comp = self.__class__.x_comp(path + [("x_comp", None)], service)
                        self.y_comp = self.__class__.y_comp(path + [("y_comp", None)], service)
                        self.z_comp = self.__class__.z_comp(path + [("z_comp", None)], service)
                        self.scale_head = self.__class__.scale_head(path + [("scale_head", None)], service)
                        self.color = self.__class__.color(path + [("color", None)], service)

                    class in_plane(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class fixed_length(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class x_comp(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class y_comp(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class z_comp(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class scale_head(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class color(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                class range_option(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                        self.auto_range_on = self.__class__.auto_range_on(path + [("auto_range_on", None)], service)
                        self.auto_range_off = self.__class__.auto_range_off(path + [("auto_range_off", None)], service)

                    class auto_range_on(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service
                            self.global_range = self.__class__.global_range(path + [("global_range", None)], service)

                        class global_range(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                    class auto_range_off(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service
                            self.clip_to_range = self.__class__.clip_to_range(path + [("clip_to_range", None)], service)
                            self.minimum = self.__class__.minimum(path + [("minimum", None)], service)
                            self.maximum = self.__class__.maximum(path + [("maximum", None)], service)

                        class clip_to_range(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                        class minimum(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                        class maximum(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                class color_map(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                        self.visible = self.__class__.visible(path + [("visible", None)], service)
                        self.size = self.__class__.size(path + [("size", None)], service)
                        self.color = self.__class__.color(path + [("color", None)], service)
                        self.log_scale = self.__class__.log_scale(path + [("log_scale", None)], service)
                        self.format = self.__class__.format(path + [("format", None)], service)
                        self.user_skip = self.__class__.user_skip(path + [("user_skip", None)], service)
                        self.show_all = self.__class__.show_all(path + [("show_all", None)], service)
                        self.position = self.__class__.position(path + [("position", None)], service)
                        self.font_name = self.__class__.font_name(path + [("font_name", None)], service)
                        self.font_automatic = self.__class__.font_automatic(path + [("font_automatic", None)], service)
                        self.font_size = self.__class__.font_size(path + [("font_size", None)], service)
                        self.length = self.__class__.length(path + [("length", None)], service)
                        self.width = self.__class__.width(path + [("width", None)], service)

                    class visible(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class size(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class color(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class log_scale(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class format(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class user_skip(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class show_all(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class position(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class font_name(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class font_automatic(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class font_size(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class length(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class width(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                class draw_mesh(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class mesh_object(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class display_state_name(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class physics(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class geometry(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class surfaces(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

            class pathlines(metaclass=PyNamedObjectMeta):
                """
                """
                is_extended_tui = True
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                    self.name = self.__class__.name(path + [("name", None)], service)
                    self.uid = self.__class__.uid(path + [("uid", None)], service)
                    self.options = self.__class__.options(path + [("options", None)], service)
                    self.range = self.__class__.range(path + [("range", None)], service)
                    self.style_attribute = self.__class__.style_attribute(path + [("style_attribute", None)], service)
                    self.accuracy_control = self.__class__.accuracy_control(path + [("accuracy_control", None)], service)
                    self.plot = self.__class__.plot(path + [("plot", None)], service)
                    self.step = self.__class__.step(path + [("step", None)], service)
                    self.skip = self.__class__.skip(path + [("skip", None)], service)
                    self.coarsen = self.__class__.coarsen(path + [("coarsen", None)], service)
                    self.onzone = self.__class__.onzone(path + [("onzone", None)], service)
                    self.field = self.__class__.field(path + [("field", None)], service)
                    self.surfaces_list = self.__class__.surfaces_list(path + [("surfaces_list", None)], service)
                    self.velocity_domain = self.__class__.velocity_domain(path + [("velocity_domain", None)], service)
                    self.color_map = self.__class__.color_map(path + [("color_map", None)], service)
                    self.draw_mesh = self.__class__.draw_mesh(path + [("draw_mesh", None)], service)
                    self.mesh_object = self.__class__.mesh_object(path + [("mesh_object", None)], service)
                    self.display_state_name = self.__class__.display_state_name(path + [("display_state_name", None)], service)
                    self.physics = self.__class__.physics(path + [("physics", None)], service)
                    self.geometry = self.__class__.geometry(path + [("geometry", None)], service)
                    self.surfaces = self.__class__.surfaces(path + [("surfaces", None)], service)

                class name(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class uid(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class options(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                        self.oil_flow = self.__class__.oil_flow(path + [("oil_flow", None)], service)
                        self.reverse = self.__class__.reverse(path + [("reverse", None)], service)
                        self.node_values = self.__class__.node_values(path + [("node_values", None)], service)
                        self.relative = self.__class__.relative(path + [("relative", None)], service)

                    class oil_flow(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class reverse(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class node_values(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class relative(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                class range(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                        self.auto_range = self.__class__.auto_range(path + [("auto_range", None)], service)
                        self.clip_to_range = self.__class__.clip_to_range(path + [("clip_to_range", None)], service)

                    class auto_range(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class clip_to_range(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service
                            self.min_value = self.__class__.min_value(path + [("min_value", None)], service)
                            self.max_value = self.__class__.max_value(path + [("max_value", None)], service)

                        class min_value(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                        class max_value(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                class style_attribute(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                        self.style = self.__class__.style(path + [("style", None)], service)
                        self.line_width = self.__class__.line_width(path + [("line_width", None)], service)
                        self.arrow_space = self.__class__.arrow_space(path + [("arrow_space", None)], service)
                        self.arrow_scale = self.__class__.arrow_scale(path + [("arrow_scale", None)], service)
                        self.marker_size = self.__class__.marker_size(path + [("marker_size", None)], service)
                        self.sphere_size = self.__class__.sphere_size(path + [("sphere_size", None)], service)
                        self.sphere_lod = self.__class__.sphere_lod(path + [("sphere_lod", None)], service)
                        self.radius = self.__class__.radius(path + [("radius", None)], service)
                        self.ribbon = self.__class__.ribbon(path + [("ribbon", None)], service)

                    class style(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class line_width(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class arrow_space(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class arrow_scale(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class marker_size(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class sphere_size(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class sphere_lod(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class radius(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class ribbon(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service
                            self.field = self.__class__.field(path + [("field", None)], service)
                            self.scalefactor = self.__class__.scalefactor(path + [("scalefactor", None)], service)

                        class field(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                        class scalefactor(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                class accuracy_control(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                        self.step_size = self.__class__.step_size(path + [("step_size", None)], service)
                        self.tolerance = self.__class__.tolerance(path + [("tolerance", None)], service)

                    class step_size(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class tolerance(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                class plot(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                        self.x_axis_function = self.__class__.x_axis_function(path + [("x_axis_function", None)], service)
                        self.enabled = self.__class__.enabled(path + [("enabled", None)], service)

                    class x_axis_function(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class enabled(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                class step(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class skip(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class coarsen(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class onzone(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class field(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class surfaces_list(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class velocity_domain(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class color_map(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                        self.visible = self.__class__.visible(path + [("visible", None)], service)
                        self.size = self.__class__.size(path + [("size", None)], service)
                        self.color = self.__class__.color(path + [("color", None)], service)
                        self.log_scale = self.__class__.log_scale(path + [("log_scale", None)], service)
                        self.format = self.__class__.format(path + [("format", None)], service)
                        self.user_skip = self.__class__.user_skip(path + [("user_skip", None)], service)
                        self.show_all = self.__class__.show_all(path + [("show_all", None)], service)
                        self.position = self.__class__.position(path + [("position", None)], service)
                        self.font_name = self.__class__.font_name(path + [("font_name", None)], service)
                        self.font_automatic = self.__class__.font_automatic(path + [("font_automatic", None)], service)
                        self.font_size = self.__class__.font_size(path + [("font_size", None)], service)
                        self.length = self.__class__.length(path + [("length", None)], service)
                        self.width = self.__class__.width(path + [("width", None)], service)

                    class visible(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class size(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class color(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class log_scale(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class format(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class user_skip(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class show_all(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class position(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class font_name(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class font_automatic(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class font_size(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class length(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class width(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                class draw_mesh(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class mesh_object(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class display_state_name(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class physics(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class geometry(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class surfaces(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

            class particle_tracks(metaclass=PyNamedObjectMeta):
                """
                """
                is_extended_tui = True
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                    self.name = self.__class__.name(path + [("name", None)], service)
                    self.uid = self.__class__.uid(path + [("uid", None)], service)
                    self.options = self.__class__.options(path + [("options", None)], service)
                    self.filter_settings = self.__class__.filter_settings(path + [("filter_settings", None)], service)
                    self.range = self.__class__.range(path + [("range", None)], service)
                    self.style_attribute = self.__class__.style_attribute(path + [("style_attribute", None)], service)
                    self.vector_settings = self.__class__.vector_settings(path + [("vector_settings", None)], service)
                    self.plot = self.__class__.plot(path + [("plot", None)], service)
                    self.track_single_particle_stream = self.__class__.track_single_particle_stream(path + [("track_single_particle_stream", None)], service)
                    self.skip = self.__class__.skip(path + [("skip", None)], service)
                    self.coarsen = self.__class__.coarsen(path + [("coarsen", None)], service)
                    self.field = self.__class__.field(path + [("field", None)], service)
                    self.injections_list = self.__class__.injections_list(path + [("injections_list", None)], service)
                    self.free_stream_particles = self.__class__.free_stream_particles(path + [("free_stream_particles", None)], service)
                    self.wall_film_particles = self.__class__.wall_film_particles(path + [("wall_film_particles", None)], service)
                    self.track_pdf_particles = self.__class__.track_pdf_particles(path + [("track_pdf_particles", None)], service)
                    self.color_map = self.__class__.color_map(path + [("color_map", None)], service)
                    self.draw_mesh = self.__class__.draw_mesh(path + [("draw_mesh", None)], service)
                    self.mesh_object = self.__class__.mesh_object(path + [("mesh_object", None)], service)
                    self.display_state_name = self.__class__.display_state_name(path + [("display_state_name", None)], service)

                class name(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class uid(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class options(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                        self.node_values = self.__class__.node_values(path + [("node_values", None)], service)

                    class node_values(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                class filter_settings(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                        self.field = self.__class__.field(path + [("field", None)], service)
                        self.options = self.__class__.options(path + [("options", None)], service)
                        self.enabled = self.__class__.enabled(path + [("enabled", None)], service)
                        self.filter_minimum = self.__class__.filter_minimum(path + [("filter_minimum", None)], service)
                        self.filter_maximum = self.__class__.filter_maximum(path + [("filter_maximum", None)], service)

                    class field(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class options(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service
                            self.inside = self.__class__.inside(path + [("inside", None)], service)
                            self.outside = self.__class__.outside(path + [("outside", None)], service)

                        class inside(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                        class outside(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                    class enabled(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class filter_minimum(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class filter_maximum(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                class range(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                        self.auto_range = self.__class__.auto_range(path + [("auto_range", None)], service)
                        self.clip_to_range = self.__class__.clip_to_range(path + [("clip_to_range", None)], service)

                    class auto_range(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class clip_to_range(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service
                            self.min_value = self.__class__.min_value(path + [("min_value", None)], service)
                            self.max_value = self.__class__.max_value(path + [("max_value", None)], service)

                        class min_value(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                        class max_value(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                class style_attribute(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                        self.style = self.__class__.style(path + [("style", None)], service)
                        self.line_width = self.__class__.line_width(path + [("line_width", None)], service)
                        self.arrow_space = self.__class__.arrow_space(path + [("arrow_space", None)], service)
                        self.arrow_scale = self.__class__.arrow_scale(path + [("arrow_scale", None)], service)
                        self.marker_size = self.__class__.marker_size(path + [("marker_size", None)], service)
                        self.sphere_size = self.__class__.sphere_size(path + [("sphere_size", None)], service)
                        self.sphere_lod = self.__class__.sphere_lod(path + [("sphere_lod", None)], service)
                        self.radius = self.__class__.radius(path + [("radius", None)], service)
                        self.ribbon_settings = self.__class__.ribbon_settings(path + [("ribbon_settings", None)], service)
                        self.sphere_settings = self.__class__.sphere_settings(path + [("sphere_settings", None)], service)

                    class style(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class line_width(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class arrow_space(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class arrow_scale(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class marker_size(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class sphere_size(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class sphere_lod(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class radius(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class ribbon_settings(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service
                            self.field = self.__class__.field(path + [("field", None)], service)
                            self.scalefactor = self.__class__.scalefactor(path + [("scalefactor", None)], service)

                        class field(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                        class scalefactor(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                    class sphere_settings(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service
                            self.scale = self.__class__.scale(path + [("scale", None)], service)
                            self.sphere_lod = self.__class__.sphere_lod(path + [("sphere_lod", None)], service)
                            self.options = self.__class__.options(path + [("options", None)], service)

                        class scale(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                        class sphere_lod(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                        class options(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service
                                self.constant = self.__class__.constant(path + [("constant", None)], service)
                                self.variable = self.__class__.variable(path + [("variable", None)], service)

                            class constant(metaclass=PyMenuMeta):
                                """
                                """
                                is_extended_tui = True
                                def __init__(self, path, service):
                                    self.path = path
                                    self.service = service
                                    self.diameter = self.__class__.diameter(path + [("diameter", None)], service)

                                class diameter(metaclass=PyMenuMeta):
                                    """
                                    """
                                    is_extended_tui = True
                                    def __init__(self, path, service):
                                        self.path = path
                                        self.service = service

                            class variable(metaclass=PyMenuMeta):
                                """
                                """
                                is_extended_tui = True
                                def __init__(self, path, service):
                                    self.path = path
                                    self.service = service
                                    self.size_by = self.__class__.size_by(path + [("size_by", None)], service)
                                    self.range = self.__class__.range(path + [("range", None)], service)

                                class size_by(metaclass=PyMenuMeta):
                                    """
                                    """
                                    is_extended_tui = True
                                    def __init__(self, path, service):
                                        self.path = path
                                        self.service = service

                                class range(metaclass=PyMenuMeta):
                                    """
                                    """
                                    is_extended_tui = True
                                    def __init__(self, path, service):
                                        self.path = path
                                        self.service = service
                                        self.auto_range = self.__class__.auto_range(path + [("auto_range", None)], service)
                                        self.clip_to_range = self.__class__.clip_to_range(path + [("clip_to_range", None)], service)

                                    class auto_range(metaclass=PyMenuMeta):
                                        """
                                        """
                                        is_extended_tui = True
                                        def __init__(self, path, service):
                                            self.path = path
                                            self.service = service

                                    class clip_to_range(metaclass=PyMenuMeta):
                                        """
                                        """
                                        is_extended_tui = True
                                        def __init__(self, path, service):
                                            self.path = path
                                            self.service = service
                                            self.min_value = self.__class__.min_value(path + [("min_value", None)], service)
                                            self.max_value = self.__class__.max_value(path + [("max_value", None)], service)

                                        class min_value(metaclass=PyMenuMeta):
                                            """
                                            """
                                            is_extended_tui = True
                                            def __init__(self, path, service):
                                                self.path = path
                                                self.service = service

                                        class max_value(metaclass=PyMenuMeta):
                                            """
                                            """
                                            is_extended_tui = True
                                            def __init__(self, path, service):
                                                self.path = path
                                                self.service = service

                class vector_settings(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                        self.style = self.__class__.style(path + [("style", None)], service)
                        self.vector_length = self.__class__.vector_length(path + [("vector_length", None)], service)
                        self.constant_color = self.__class__.constant_color(path + [("constant_color", None)], service)
                        self.vector_of = self.__class__.vector_of(path + [("vector_of", None)], service)
                        self.scale = self.__class__.scale(path + [("scale", None)], service)
                        self.length_to_head_ratio = self.__class__.length_to_head_ratio(path + [("length_to_head_ratio", None)], service)

                    class style(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class vector_length(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service
                            self.constant_length = self.__class__.constant_length(path + [("constant_length", None)], service)
                            self.variable_length = self.__class__.variable_length(path + [("variable_length", None)], service)

                        class constant_length(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                        class variable_length(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                    class constant_color(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service
                            self.enabled = self.__class__.enabled(path + [("enabled", None)], service)
                            self.color = self.__class__.color(path + [("color", None)], service)

                        class enabled(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                        class color(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True
                            def __init__(self, path, service):
                                self.path = path
                                self.service = service

                    class vector_of(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class scale(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class length_to_head_ratio(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                class plot(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                        self.x_axis_function = self.__class__.x_axis_function(path + [("x_axis_function", None)], service)
                        self.enabled = self.__class__.enabled(path + [("enabled", None)], service)

                    class x_axis_function(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class enabled(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                class track_single_particle_stream(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                        self.enabled = self.__class__.enabled(path + [("enabled", None)], service)
                        self.stream_id = self.__class__.stream_id(path + [("stream_id", None)], service)

                    class enabled(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class stream_id(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                class skip(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class coarsen(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class field(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class injections_list(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class free_stream_particles(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class wall_film_particles(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class track_pdf_particles(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class color_map(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service
                        self.visible = self.__class__.visible(path + [("visible", None)], service)
                        self.size = self.__class__.size(path + [("size", None)], service)
                        self.color = self.__class__.color(path + [("color", None)], service)
                        self.log_scale = self.__class__.log_scale(path + [("log_scale", None)], service)
                        self.format = self.__class__.format(path + [("format", None)], service)
                        self.user_skip = self.__class__.user_skip(path + [("user_skip", None)], service)
                        self.show_all = self.__class__.show_all(path + [("show_all", None)], service)
                        self.position = self.__class__.position(path + [("position", None)], service)
                        self.font_name = self.__class__.font_name(path + [("font_name", None)], service)
                        self.font_automatic = self.__class__.font_automatic(path + [("font_automatic", None)], service)
                        self.font_size = self.__class__.font_size(path + [("font_size", None)], service)
                        self.length = self.__class__.length(path + [("length", None)], service)
                        self.width = self.__class__.width(path + [("width", None)], service)

                    class visible(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class size(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class color(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class log_scale(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class format(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class user_skip(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class show_all(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class position(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class font_name(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class font_automatic(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class font_size(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class length(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                    class width(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True
                        def __init__(self, path, service):
                            self.path = path
                            self.service = service

                class draw_mesh(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class mesh_object(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class display_state_name(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

            class scene(metaclass=PyNamedObjectMeta):
                """
                """
                is_extended_tui = True
                def __init__(self, path, service):
                    self.path = path
                    self.service = service
                    self.name = self.__class__.name(path + [("name", None)], service)
                    self.title = self.__class__.title(path + [("title", None)], service)
                    self.temporary = self.__class__.temporary(path + [("temporary", None)], service)
                    self.display_state_name = self.__class__.display_state_name(path + [("display_state_name", None)], service)

                class name(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class title(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class temporary(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

                class display_state_name(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True
                    def __init__(self, path, service):
                        self.path = path
                        self.service = service

        class zones(metaclass=PyMenuMeta):
            """
            Contains commands for displaying zones.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def show_all(self, *args, **kwargs):
                """
                Unhides all the zones in the geometry and displays them.
                """
                return PyMenu(self.service, "/display/zones/show_all").execute(*args, **kwargs)
            def toggle_color_palette(self, *args, **kwargs):
                """
                Toggles the color palette of the geometry.
                """
                return PyMenu(self.service, "/display/zones/toggle_color_palette").execute(*args, **kwargs)
            def display_similar_area(self, *args, **kwargs):
                """
                Displays the zones with similar area to the selected zone area.
                """
                return PyMenu(self.service, "/display/zones/display_similar_area").execute(*args, **kwargs)
            def toggle_color_mode(self, *args, **kwargs):
                """
                Toggles the colors of the geometry. In one mode geometry is colored object-wise while in the other mode it is colored zone-wise.
                """
                return PyMenu(self.service, "/display/zones/toggle_color_mode").execute(*args, **kwargs)
            def make_transparent(self, *args, **kwargs):
                """
                Makes the geometry transparent so that internal zones are visible. This command works as a toggle undoing the transparency of the previously selected zones.
                """
                return PyMenu(self.service, "/display/zones/make_transparent").execute(*args, **kwargs)
            def select_all_visible(self, *args, **kwargs):
                """
                Selects all the visible zones in the graphics window.
                """
                return PyMenu(self.service, "/display/zones/select_all_visible").execute(*args, **kwargs)
            def display_neighborhood(self, *args, **kwargs):
                """
                Displays the zones that are in the neighborhood of the selected zones. The neighboring zones have to be in contact, or intersecting the selected zone.
                """
                return PyMenu(self.service, "/display/zones/display_neighborhood").execute(*args, **kwargs)
            def hide_zones(self, *args, **kwargs):
                """
                Hides the selected zones in the display.
                """
                return PyMenu(self.service, "/display/zones/hide_zones").execute(*args, **kwargs)
            def isolate_zones(self, *args, **kwargs):
                """
                Displays only the selected zones.
                """
                return PyMenu(self.service, "/display/zones/isolate_zones").execute(*args, **kwargs)

        class advanced_rendering(metaclass=PyMenuMeta):
            """
            Enter the advanced rendering menu.
            """
            def __init__(self, path, service):
                self.path = path
                self.service = service
            def max_extent_culling(self, *args, **kwargs):
                """
                Truncates zones smaller that the maximum extent culling pixel value.
                """
                return PyMenu(self.service, "/display/advanced_rendering/max_extent_culling").execute(*args, **kwargs)
            def static_model(self, *args, **kwargs):
                """
                Static model driver setting.
                """
                return PyMenu(self.service, "/display/advanced_rendering/static_model").execute(*args, **kwargs)
            def simple_shadow(self, *args, **kwargs):
                """
                Enhances viewability by adding a simple shadow.
                """
                return PyMenu(self.service, "/display/advanced_rendering/simple_shadow").execute(*args, **kwargs)
            def fast_silhouette_edges(self, *args, **kwargs):
                """
                Enhances viewability by adding fast silhouette edges.
                """
                return PyMenu(self.service, "/display/advanced_rendering/fast_silhouette_edges").execute(*args, **kwargs)
            def edge_color(self, *args, **kwargs):
                """
                Choose between black and body colored edges.
                """
                return PyMenu(self.service, "/display/advanced_rendering/edge_color").execute(*args, **kwargs)

    class report(metaclass=PyMenuMeta):
        """
        Enter the report menu.
        """
        def __init__(self, path, service):
            self.path = path
            self.service = service
        def face_node_degree_distribution(self, *args, **kwargs):
            """
            Reports the distribution of boundary faces based on face node degree. The node degree is the number of faces connected to the node. Specify the list of boundary face zones and the minimum and maximum face node degree to be reported. You can also consider only internal nodes, if required.
            """
            return PyMenu(self.service, "/report/face_node_degree_distribution").execute(*args, **kwargs)
        def boundary_cell_quality(self, *args, **kwargs):
            """
            Reports the number and quality limits of boundary cells containing the specified number of boundary faces. If you specify zero for number of boundary faces, you will be prompted for number of boundary nodes. 
            """
            return PyMenu(self.service, "/report/boundary_cell_quality").execute(*args, **kwargs)
        def cell_distribution(self, *args, **kwargs):
            """
            Reports the distribution of cell quality or size based on the bounding limits and number of partitions specified. 
            """
            return PyMenu(self.service, "/report/cell_distribution").execute(*args, **kwargs)
        def face_distribution(self, *args, **kwargs):
            """
            Reports the distribution of face quality or size based on the bounding limits and number of partitions specified. 
            """
            return PyMenu(self.service, "/report/face_distribution").execute(*args, **kwargs)
        def cell_zone_volume(self, *args, **kwargs):
            """
            Reports the volume of the specified cell zone. 
            """
            return PyMenu(self.service, "/report/cell_zone_volume").execute(*args, **kwargs)
        def cell_zone_at_location(self, *args, **kwargs):
            """
            Returns the cell zone at or closest to the specified location. 
            """
            return PyMenu(self.service, "/report/cell_zone_at_location").execute(*args, **kwargs)
        def face_zone_at_location(self, *args, **kwargs):
            """
            Reports the face zone at the given location. 
            """
            return PyMenu(self.service, "/report/face_zone_at_location").execute(*args, **kwargs)
        def number_meshed(self, *args, **kwargs):
            """
            Reports the number of elements that have been meshed. 
            """
            return PyMenu(self.service, "/report/number_meshed").execute(*args, **kwargs)
        def list_cell_quality(self, *args, **kwargs):
            """
            Reports a list of cells with the specified quality measure within a specified range. The valid prefixes are bn (boundary node), n (node), bf (boundary face), f (face), and c (cell). 
            """
            return PyMenu(self.service, "/report/list_cell_quality").execute(*args, **kwargs)
        def mesh_size(self, *args, **kwargs):
            """
            Reports the number of nodes, faces, and cells in the mesh. 
            """
            return PyMenu(self.service, "/report/mesh_size").execute(*args, **kwargs)
        def mesh_statistics(self, *args, **kwargs):
            """
            Writes mesh statistics (such as zone information, number of cells, faces, and nodes, range of quality and size) to an external file. 
            """
            return PyMenu(self.service, "/report/mesh_statistics").execute(*args, **kwargs)
        def meshing_time(self, *args, **kwargs):
            """
            Report meshing time.
            """
            return PyMenu(self.service, "/report/meshing_time").execute(*args, **kwargs)
        def memory_usage(self, *args, **kwargs):
            """
            Reports the amount of memory used for all nodes, faces, and cells, and the total memory allocated. 
            """
            return PyMenu(self.service, "/report/memory_usage").execute(*args, **kwargs)
        def print_info(self, *args, **kwargs):
            """
            Prints information about individual components of the mesh. This command also appears in the boundary menu. When you use this command, you will be prompted for an “entity” (that is, a node, face, or cell). An entity name consists of a prefix and an index. For a description of the displayed information see 
                        
            """
            return PyMenu(self.service, "/report/print_info").execute(*args, **kwargs)
        def edge_size_limits(self, *args, **kwargs):
            """
            Reports the edge size limits. 
            """
            return PyMenu(self.service, "/report/edge_size_limits").execute(*args, **kwargs)
        def face_size_limits(self, *args, **kwargs):
            """
            Reports the face size limits. 
            """
            return PyMenu(self.service, "/report/face_size_limits").execute(*args, **kwargs)
        def face_quality_limits(self, *args, **kwargs):
            """
            Reports the face quality limits. 
            """
            return PyMenu(self.service, "/report/face_quality_limits").execute(*args, **kwargs)
        def face_zone_area(self, *args, **kwargs):
            """
            Reports the area of the specified face zone. 
            """
            return PyMenu(self.service, "/report/face_zone_area").execute(*args, **kwargs)
        def cell_size_limits(self, *args, **kwargs):
            """
            Reports the cell size limits. 
            """
            return PyMenu(self.service, "/report/cell_size_limits").execute(*args, **kwargs)
        def cell_quality_limits(self, *args, **kwargs):
            """
            Reports the cell quality limits. 
            """
            return PyMenu(self.service, "/report/cell_quality_limits").execute(*args, **kwargs)
        def neighborhood_quality(self, *args, **kwargs):
            """
            Reports the maximum skewness, aspect ratio, or size change of all cells using a specified node. 
            """
            return PyMenu(self.service, "/report/neighborhood_quality").execute(*args, **kwargs)
        def quality_method(self, *args, **kwargs):
            """
            Specifies the method to be used for reporting face and cell quality. 
            """
            return PyMenu(self.service, "/report/quality_method").execute(*args, **kwargs)
        def enhanced_orthogonal_quality(self, *args, **kwargs):
            """
            Employs an enhanced definition of the orthogonal quality measure that combines a variety of quality measures, including: the orthogonality of a face relative to a vector between the face and cell centroids; a metric that detects poor cell shape at a local edge (such as twisting and/or concavity); and the variation of normals between the faces that can be constructed from the cell face. This definition is optimal for evaluating thin prism cells.
            """
            return PyMenu(self.service, "/report/enhanced_orthogonal_quality").execute(*args, **kwargs)
        def unrefined_cells(self, *args, **kwargs):
            """
            Reports the number of cells that have not been refined. 
            """
            return PyMenu(self.service, "/report/unrefined_cells").execute(*args, **kwargs)
        def update_bounding_box(self, *args, **kwargs):
            """
            Updates the bounding box. 
            """
            return PyMenu(self.service, "/report/update_bounding_box").execute(*args, **kwargs)
        def verbosity_level(self, *args, **kwargs):
            """
            Specifies how much information should be displayed during mesh initialization, refinement and other operations. Changing the value to 2 from the default value of 1 will produce more messages, while changing it to 0 will disable all messages. 
            """
            return PyMenu(self.service, "/report/verbosity_level").execute(*args, **kwargs)
        def spy_level(self, *args, **kwargs):
            """
            Spy on meshing process.
            """
            return PyMenu(self.service, "/report/spy_level").execute(*args, **kwargs)

    class parallel(metaclass=PyMenuMeta):
        """
        Enter the parallel menu.
        """
        def __init__(self, path, service):
            self.path = path
            self.service = service
        def spawn_solver_processes(self, *args, **kwargs):
            """
            Specifies the number of solver processes. Additional processes will be spawned as necessary when switching to solution mode in Linux with the default MPI. You will also be prompted for (Linux and mixed Windows/Linux) interconnect type, machine list or host file, and (Linux and mixed Windows/Linux) option to be used.
            """
            return PyMenu(self.service, "/parallel/spawn_solver_processes").execute(*args, **kwargs)
        def auto_partition(self, *args, **kwargs):
            """
            Automatically partitions face-zones for parallel meshing.
            """
            return PyMenu(self.service, "/parallel/auto_partition").execute(*args, **kwargs)
        def agglomerate(self, *args, **kwargs):
            """
            Recombines distributed mesh data into a single partition on compute node 0.
            """
            return PyMenu(self.service, "/parallel/agglomerate").execute(*args, **kwargs)
        def print_partition_info(self, *args, **kwargs):
            """
            Displays computed partition data to the console.
            """
            return PyMenu(self.service, "/parallel/print_partition_info").execute(*args, **kwargs)
        def thread_number_control(self, *args, **kwargs):
            """
            Controls the maximum number of threads on each machine.
            """
            return PyMenu(self.service, "/parallel/thread_number_control").execute(*args, **kwargs)

    class openmp_controls(metaclass=PyMenuMeta):
        """
        Enter the openmp menu.
        """
        def __init__(self, path, service):
            self.path = path
            self.service = service
        def get_max_cores(self, *args, **kwargs):
            """
            Max Number of Cores.
            """
            return PyMenu(self.service, "/openmp_controls/get_max_cores").execute(*args, **kwargs)
        def get_active_cores(self, *args, **kwargs):
            """
            Number of Active Cores.
            """
            return PyMenu(self.service, "/openmp_controls/get_active_cores").execute(*args, **kwargs)
        def set_num_cores(self, *args, **kwargs):
            """
            Enter Number of Cores.
            """
            return PyMenu(self.service, "/openmp_controls/set_num_cores").execute(*args, **kwargs)

    class reference_frames(metaclass=PyMenuMeta):
        """
        Manage reference frames.
        """
        def __init__(self, path, service):
            self.path = path
            self.service = service
        def add(self, *args, **kwargs):
            """
            Add a new object.
            """
            return PyMenu(self.service, "/reference_frames/add").execute(*args, **kwargs)
        def display(self, *args, **kwargs):
            """
            Display Reference Frame.
            """
            return PyMenu(self.service, "/reference_frames/display").execute(*args, **kwargs)
        def display_edit(self, *args, **kwargs):
            """
            Display and edit reference frame from graphics.
            """
            return PyMenu(self.service, "/reference_frames/display_edit").execute(*args, **kwargs)
        def edit(self, *args, **kwargs):
            """
            Edit an object.
            """
            return PyMenu(self.service, "/reference_frames/edit").execute(*args, **kwargs)
        def delete(self, *args, **kwargs):
            """
            Delete an object.
            """
            return PyMenu(self.service, "/reference_frames/delete").execute(*args, **kwargs)
        def hide(self, *args, **kwargs):
            """
            Hide Reference Frame.
            """
            return PyMenu(self.service, "/reference_frames/hide").execute(*args, **kwargs)
        def list(self, *args, **kwargs):
            """
            List objects.
            """
            return PyMenu(self.service, "/reference_frames/list").execute(*args, **kwargs)
        def list_properties(self, *args, **kwargs):
            """
            List properties of an object.
            """
            return PyMenu(self.service, "/reference_frames/list_properties").execute(*args, **kwargs)
