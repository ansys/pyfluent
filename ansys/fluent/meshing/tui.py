"""
This is an auto-generated file.  DO NOT EDIT!
"""
# pylint: disable=line-too-long

from ansys.fluent.solver.meta import PyMenuMeta, PyNamedObjectMeta
from ansys.fluent.services.datamodel_tui import PyMenu


def beta_feature_access(self, *args, **kwargs):
    """
    Enable access to beta features in the interface.
    """
    return PyMenu(self.service).execute('/beta_feature_access', *args, **kwargs)
def close_fluent(self, *args, **kwargs):
    """
    Exit Fluent Meshing
    """
    return PyMenu(self.service).execute('/close_fluent', *args, **kwargs)
def exit(self, *args, **kwargs):
    """
    Exit Fluent Meshing
    """
    return PyMenu(self.service).execute('/exit', *args, **kwargs)
def switch_to_solution_mode(self, *args, **kwargs):
    """
    Switch to solution mode.
    """
    return PyMenu(self.service).execute('/switch_to_solution_mode', *args, **kwargs)
def print_license_usage(self, *args, **kwargs):
    """
    Print license usage information
    """
    return PyMenu(self.service).execute('/print_license_usage', *args, **kwargs)

class file(metaclass=PyMenuMeta):
    __doc__ = 'Enter the file menu'
    def append_mesh(self, *args, **kwargs):
        """
        Append a new mesh to the existing mesh
        """
        return PyMenu(self.service).execute('/file/append_mesh', *args, **kwargs)
    def append_meshes_by_tmerge(self, *args, **kwargs):
        """
        Append mesh files, or the meshes from case files.
        """
        return PyMenu(self.service).execute('/file/append_meshes_by_tmerge', *args, **kwargs)
    def file_format(self, *args, **kwargs):
        """
        Indicate whether to write formatted or unformatted files.
        """
        return PyMenu(self.service).execute('/file/file_format', *args, **kwargs)
    def filter_list(self, *args, **kwargs):
        """
        List all filter names.
        """
        return PyMenu(self.service).execute('/file/filter_list', *args, **kwargs)
    def filter_options(self, *args, **kwargs):
        """
        Change filter extension and/or its arguments.
        """
        return PyMenu(self.service).execute('/file/filter_options', *args, **kwargs)
    def hdf_files(self, *args, **kwargs):
        """
        Indicate whether to write Ansys common fluids format (CFF) files or legacy case files.
        """
        return PyMenu(self.service).execute('/file/hdf_files', *args, **kwargs)
    def cff_files(self, *args, **kwargs):
        """
        Indicate whether to write Ansys common fluids format (CFF) files or legacy case files.
        """
        return PyMenu(self.service).execute('/file/cff_files', *args, **kwargs)
    def read_boundary_mesh(self, *args, **kwargs):
        """
        Read the boundary mesh from either a mesh or case file.
        """
        return PyMenu(self.service).execute('/file/read_boundary_mesh', *args, **kwargs)
    def read_mesh(self, *args, **kwargs):
        """
        Read a mesh file, or the mesh from a case file.
        """
        return PyMenu(self.service).execute('/file/read_mesh', *args, **kwargs)
    def read_meshes_by_tmerge(self, *args, **kwargs):
        """
        Read mesh files, or the meshes from case files.
        """
        return PyMenu(self.service).execute('/file/read_meshes_by_tmerge', *args, **kwargs)
    def read_multi_bound_mesh(self, *args, **kwargs):
        """
        Read multiple boundary meshes.
        """
        return PyMenu(self.service).execute('/file/read_multi_bound_mesh', *args, **kwargs)
    def read_case(self, *args, **kwargs):
        """
        Read a case file.
        Arguments:
          case_file_name: str
        """
        return PyMenu(self.service).execute('/file/read_case', *args, **kwargs)
    def read_domains(self, *args, **kwargs):
        """
        Read TGrid domains from a file.
        """
        return PyMenu(self.service).execute('/file/read_domains', *args, **kwargs)
    def read_size_field(self, *args, **kwargs):
        """
        Read TGrid Size-field from a file.
        """
        return PyMenu(self.service).execute('/file/read_size_field', *args, **kwargs)
    def write_size_field(self, *args, **kwargs):
        """
        Write TGrid Size-field into a file.
        """
        return PyMenu(self.service).execute('/file/write_size_field', *args, **kwargs)
    def read_journal(self, *args, **kwargs):
        """
        Start a main-menu that takes its input from a file.
        """
        return PyMenu(self.service).execute('/file/read_journal', *args, **kwargs)
    def read_mesh_vars(self, *args, **kwargs):
        """
        Reads mesh varaibles from a mesh file.
        """
        return PyMenu(self.service).execute('/file/read_mesh_vars', *args, **kwargs)
    def read_multiple_mesh(self, *args, **kwargs):
        """
        Read multiple mesh files, or the meshes from multiple case files.
        """
        return PyMenu(self.service).execute('/file/read_multiple_mesh', *args, **kwargs)
    def read_options(self, *args, **kwargs):
        """
        Set read options.
        """
        return PyMenu(self.service).execute('/file/read_options', *args, **kwargs)
    def show_configuration(self, *args, **kwargs):
        """
        Display current release and version information.
        """
        return PyMenu(self.service).execute('/file/show_configuration', *args, **kwargs)
    def start_journal(self, *args, **kwargs):
        """
        Start recording all input in a file.
        """
        return PyMenu(self.service).execute('/file/start_journal', *args, **kwargs)
    def start_transcript(self, *args, **kwargs):
        """
        Start recording input and output in a file.
        """
        return PyMenu(self.service).execute('/file/start_transcript', *args, **kwargs)
    def stop_journal(self, *args, **kwargs):
        """
        Stop recording input and close journal file.
        """
        return PyMenu(self.service).execute('/file/stop_journal', *args, **kwargs)
    def stop_transcript(self, *args, **kwargs):
        """
        Stop recording input and output and close transcript file.
        """
        return PyMenu(self.service).execute('/file/stop_transcript', *args, **kwargs)
    def confirm_overwrite(self, *args, **kwargs):
        """
        Indicate whether or not to confirm attempts to overwrite existing files.
        """
        return PyMenu(self.service).execute('/file/confirm_overwrite', *args, **kwargs)
    def write_boundaries(self, *args, **kwargs):
        """
        Write the mesh file of selected boundary face zones.
        """
        return PyMenu(self.service).execute('/file/write_boundaries', *args, **kwargs)
    def write_case(self, *args, **kwargs):
        """
        Write the mesh to a case file.
        """
        return PyMenu(self.service).execute('/file/write_case', *args, **kwargs)
    def write_domains(self, *args, **kwargs):
        """
        Write all (except global) domains of the mesh into a file.
        """
        return PyMenu(self.service).execute('/file/write_domains', *args, **kwargs)
    def write_mesh(self, *args, **kwargs):
        """
        Write a mesh file.
        """
        return PyMenu(self.service).execute('/file/write_mesh', *args, **kwargs)
    def write_mesh_vars(self, *args, **kwargs):
        """
        Writes mesh varaibles to a file.
        """
        return PyMenu(self.service).execute('/file/write_mesh_vars', *args, **kwargs)
    def write_options(self, *args, **kwargs):
        """
        Set write options.
        """
        return PyMenu(self.service).execute('/file/write_options', *args, **kwargs)
    def set_idle_timeout(self, *args, **kwargs):
        """
        Set the idle timeout
        """
        return PyMenu(self.service).execute('/file/set_idle_timeout', *args, **kwargs)
    def load_act_tool(self, *args, **kwargs):
        """
        Load ACT Start Page.
        """
        return PyMenu(self.service).execute('/file/load_act_tool', *args, **kwargs)
    def set_tui_version(self, *args, **kwargs):
        """
        Set the version of the TUI commands.
        """
        return PyMenu(self.service).execute('/file/set_tui_version', *args, **kwargs)

    class export(metaclass=PyMenuMeta):
        __doc__ = 'Export surface and volume meshes to non-native formats.'
        def ansys(self, *args, **kwargs):
            """
            Write a Ansys mesh file.
            """
            return PyMenu(self.service).execute('/file/export/ansys', *args, **kwargs)
        def hypermesh(self, *args, **kwargs):
            """
            Write a HYPERMESH ascii file.
            """
            return PyMenu(self.service).execute('/file/export/hypermesh', *args, **kwargs)
        def nastran(self, *args, **kwargs):
            """
            Write a NASTRAN mesh file.
            """
            return PyMenu(self.service).execute('/file/export/nastran', *args, **kwargs)
        def patran(self, *args, **kwargs):
            """
            Write a PATRAN mesh file.
            """
            return PyMenu(self.service).execute('/file/export/patran', *args, **kwargs)
        def stl(self, *args, **kwargs):
            """
            Write a STL boundary mesh file.
            """
            return PyMenu(self.service).execute('/file/export/stl', *args, **kwargs)

    class import_(metaclass=PyMenuMeta):
        __doc__ = 'Import surface and volume meshes from non-native formats.'
        def ansys_surf_mesh(self, *args, **kwargs):
            """
            Read a surface mesh from an Ansys prep7 or cdb file.
            """
            return PyMenu(self.service).execute('/file/import/ansys_surf_mesh', *args, **kwargs)
        def ansys_vol_mesh(self, *args, **kwargs):
            """
            Read a volume mesh from an Ansys prep7 or cdb file.
            """
            return PyMenu(self.service).execute('/file/import/ansys_vol_mesh', *args, **kwargs)
        def cgns_vol_mesh(self, *args, **kwargs):
            """
            Read a volume mesh from an CGNS format file.
            """
            return PyMenu(self.service).execute('/file/import/cgns_vol_mesh', *args, **kwargs)
        def cgns_surf_mesh(self, *args, **kwargs):
            """
            Read a surface mesh from a CGNS format file.
            """
            return PyMenu(self.service).execute('/file/import/cgns_surf_mesh', *args, **kwargs)
        def fidap_surf_mesh(self, *args, **kwargs):
            """
            Read a surface mesh from a FIDAP neutral file.
            """
            return PyMenu(self.service).execute('/file/import/fidap_surf_mesh', *args, **kwargs)
        def fidap_vol_mesh(self, *args, **kwargs):
            """
            Read a volume mesh from a FIDAP neutral file.
            """
            return PyMenu(self.service).execute('/file/import/fidap_vol_mesh', *args, **kwargs)
        def fl_uns2_mesh(self, *args, **kwargs):
            """
            Read a mesh from a Fluent UNS V2 case file.
            """
            return PyMenu(self.service).execute('/file/import/fl_uns2_mesh', *args, **kwargs)
        def fluent_2d_mesh(self, *args, **kwargs):
            """
            Read a 2D mesh.
            """
            return PyMenu(self.service).execute('/file/import/fluent_2d_mesh', *args, **kwargs)
        def fluent_3d_mesh(self, *args, **kwargs):
            """
            Read a 3D mesh.
            """
            return PyMenu(self.service).execute('/file/import/fluent_3d_mesh', *args, **kwargs)
        def gambit_surf_mesh(self, *args, **kwargs):
            """
            Read a surface mesh from a GAMBIT neutral file.
            """
            return PyMenu(self.service).execute('/file/import/gambit_surf_mesh', *args, **kwargs)
        def gambit_vol_mesh(self, *args, **kwargs):
            """
            Read a volume mesh from a GAMBIT neutral file.
            """
            return PyMenu(self.service).execute('/file/import/gambit_vol_mesh', *args, **kwargs)
        def hypermesh_surf_mesh(self, *args, **kwargs):
            """
            Read a surface mesh from a HYPERMESH ascii file.
            """
            return PyMenu(self.service).execute('/file/import/hypermesh_surf_mesh', *args, **kwargs)
        def hypermesh_vol_mesh(self, *args, **kwargs):
            """
            Read a volume mesh from a HYPERMESH ascii file.
            """
            return PyMenu(self.service).execute('/file/import/hypermesh_vol_mesh', *args, **kwargs)
        def ideas_surf_mesh(self, *args, **kwargs):
            """
            Read a surface mesh from an IDEAS universal file.
            """
            return PyMenu(self.service).execute('/file/import/ideas_surf_mesh', *args, **kwargs)
        def ideas_vol_mesh(self, *args, **kwargs):
            """
            Read a volume mesh from an IDEAS universal file.
            """
            return PyMenu(self.service).execute('/file/import/ideas_vol_mesh', *args, **kwargs)
        def nastran_surf_mesh(self, *args, **kwargs):
            """
            Read a surface mesh from a NASTRAN file.
            """
            return PyMenu(self.service).execute('/file/import/nastran_surf_mesh', *args, **kwargs)
        def nastran_vol_mesh(self, *args, **kwargs):
            """
            Read a volume mesh from a NASTRAN file.
            """
            return PyMenu(self.service).execute('/file/import/nastran_vol_mesh', *args, **kwargs)
        def patran_surf_mesh(self, *args, **kwargs):
            """
            Read a surface mesh from a PATRAN neutral file.
            """
            return PyMenu(self.service).execute('/file/import/patran_surf_mesh', *args, **kwargs)
        def patran_vol_mesh(self, *args, **kwargs):
            """
            Read a volume mesh from a PATRAN neutral file.
            """
            return PyMenu(self.service).execute('/file/import/patran_vol_mesh', *args, **kwargs)
        def cad(self, *args, **kwargs):
            """
            Reads the following CAD formats:
                ACIS  *.sat, *.sab
                Ansys DesignModeler  *.agdb
                Ansys ICEM CFD  *.tin
                Ansys Workbench  *.meshdat, *.mechdat
                Autodesk Inventor  *.ipt, *.iam
                CATIA V4  *.model, *.exp, *.session, *.dlv
                CATIA V5  *.CATPart, *.CATProduct
                Creo Parametric  *.prt, *.asm
                GAMBIT  *.dbs
                IGES  *.igs, *.iges
                JTOpen  *.jt
                NX  *.prt
                Parasolid  *.x_t, *.xmt_txt, *.x_b, *.xmt_bin
                SolidWorks  *.sldprt, *.sldasm
                STEP  *.stp, *.step
                STL  *.stl
            """
            return PyMenu(self.service).execute('/file/import/cad', *args, **kwargs)
        def cad_geometry(self, *args, **kwargs):
            """
            Reads the following CAD formats:
                ACIS  *.sat, *.sab
                Ansys DesignModeler  *.agdb
                Ansys ICEM CFD  *.tin
                Ansys Workbench  *.meshdat, *.mechdat
                Autodesk Inventor  *.ipt, *.iam
                CATIA V4  *.model, *.exp, *.session, *.dlv
                CATIA V5  *.CATPart, *.CATProduct
                Creo Parametric  *.prt, *.asm
                GAMBIT  *.dbs
                IGES  *.igs, *.iges
                JTOpen  *.jt
                NX  *.prt
                Parasolid  *.x_t, *.xmt_txt, *.x_b, *.xmt_bin
                SolidWorks  *.sldprt, *.sldasm
                STEP  *.stp, *.step
                STL  *.stl
            """
            return PyMenu(self.service).execute('/file/import/cad_geometry', *args, **kwargs)
        def stl(self, *args, **kwargs):
            """
            Read a surface mesh from a stereolithography (STL) file.
            """
            return PyMenu(self.service).execute('/file/import/stl', *args, **kwargs)
        def reimport_last_with_cfd_surface_mesh(self, *args, **kwargs):
            """
            Reimport CAD using the size field
            """
            return PyMenu(self.service).execute('/file/import/reimport_last_with_cfd_surface_mesh', *args, **kwargs)

        class cad_options(metaclass=PyMenuMeta):
            __doc__ = 'Make settings for cad import'
            def read_all_cad_in_subdirectories(self, *args, **kwargs):
                """
                Recursive search for CAD files in sub-directories.
                """
                return PyMenu(self.service).execute('/file/import/cad_options/read_all_cad_in_subdirectories', *args, **kwargs)
            def continue_on_error(self, *args, **kwargs):
                """
                Continue on error during cad import.
                """
                return PyMenu(self.service).execute('/file/import/cad_options/continue_on_error', *args, **kwargs)
            def save_PMDB(self, *args, **kwargs):
                """
                Saves PMDB file in the directory containing the CAD files imported.
                """
                return PyMenu(self.service).execute('/file/import/cad_options/save_PMDB', *args, **kwargs)
            def tessellation(self, *args, **kwargs):
                """
                Set tessellation controls for cad import.
                """
                return PyMenu(self.service).execute('/file/import/cad_options/tessellation', *args, **kwargs)
            def named_selections(self, *args, **kwargs):
                """
                Allows to import Named Selections from the CAD file.
                """
                return PyMenu(self.service).execute('/file/import/cad_options/named_selections', *args, **kwargs)
            def enclosure_symm_processing(self, *args, **kwargs):
                """
                Processing of enclosure and symmetry named selections during import.
                """
                return PyMenu(self.service).execute('/file/import/cad_options/enclosure_symm_processing', *args, **kwargs)
            def reconstruct_topology(self, *args, **kwargs):
                """
                Reconstruct topology for STL files.
                """
                return PyMenu(self.service).execute('/file/import/cad_options/reconstruct_topology', *args, **kwargs)
            def import_part_names(self, *args, **kwargs):
                """
                Import Part names from the CAD files.
                """
                return PyMenu(self.service).execute('/file/import/cad_options/import_part_names', *args, **kwargs)
            def import_body_names(self, *args, **kwargs):
                """
                Import Body names from the CAD files.
                """
                return PyMenu(self.service).execute('/file/import/cad_options/import_body_names', *args, **kwargs)
            def separate_features_by_type(self, *args, **kwargs):
                """
                Separate features by type
                """
                return PyMenu(self.service).execute('/file/import/cad_options/separate_features_by_type', *args, **kwargs)
            def single_connected_edge_label(self, *args, **kwargs):
                """
                Single connected edge label for CAD files.
                """
                return PyMenu(self.service).execute('/file/import/cad_options/single_connected_edge_label', *args, **kwargs)
            def double_connected_face_label(self, *args, **kwargs):
                """
                Double connected face label for CAD files.
                """
                return PyMenu(self.service).execute('/file/import/cad_options/double_connected_face_label', *args, **kwargs)
            def use_collection_names(self, *args, **kwargs):
                """
                Use collection names for CAD files.
                """
                return PyMenu(self.service).execute('/file/import/cad_options/use_collection_names', *args, **kwargs)
            def use_component_names(self, *args, **kwargs):
                """
                Use component names for CAD files.
                """
                return PyMenu(self.service).execute('/file/import/cad_options/use_component_names', *args, **kwargs)
            def name_separator_character(self, *args, **kwargs):
                """
                Character to be used as a separator in all names.
                """
                return PyMenu(self.service).execute('/file/import/cad_options/name_separator_character', *args, **kwargs)
            def object_type(self, *args, **kwargs):
                """
                Object type for CAD files.
                """
                return PyMenu(self.service).execute('/file/import/cad_options/object_type', *args, **kwargs)
            def one_object_per(self, *args, **kwargs):
                """
                Set one object per body, part or file.
                """
                return PyMenu(self.service).execute('/file/import/cad_options/one_object_per', *args, **kwargs)
            def one_face_zone_per(self, *args, **kwargs):
                """
                Set one object per body, face or object.
                """
                return PyMenu(self.service).execute('/file/import/cad_options/one_face_zone_per', *args, **kwargs)
            def named_selection_tessellation_failure(self, *args, **kwargs):
                """
                Set named selection for CFD surface mesh failures.
                """
                return PyMenu(self.service).execute('/file/import/cad_options/named_selection_tessellation_failure', *args, **kwargs)
            def use_body_names(self, *args, **kwargs):
                """
                Use body names for CAD files.
                """
                return PyMenu(self.service).execute('/file/import/cad_options/use_body_names', *args, **kwargs)
            def use_part_names(self, *args, **kwargs):
                """
                Use part names for CAD files.
                """
                return PyMenu(self.service).execute('/file/import/cad_options/use_part_names', *args, **kwargs)
            def replacement_character(self, *args, **kwargs):
                """
                Name replacement character.
                """
                return PyMenu(self.service).execute('/file/import/cad_options/replacement_character', *args, **kwargs)
            def derive_zone_name_from_object_scope(self, *args, **kwargs):
                """
                Derive zone names from object scope.
                """
                return PyMenu(self.service).execute('/file/import/cad_options/derive_zone_name_from_object_scope', *args, **kwargs)
            def merge_nodes(self, *args, **kwargs):
                """
                Merge Nodes for CAD import.
                """
                return PyMenu(self.service).execute('/file/import/cad_options/merge_nodes', *args, **kwargs)
            def create_cad_assemblies(self, *args, **kwargs):
                """
                Import CAD Assemblies.
                """
                return PyMenu(self.service).execute('/file/import/cad_options/create_cad_assemblies', *args, **kwargs)
            def modify_all_duplicate_names(self, *args, **kwargs):
                """
                Modify all duplicate names by suffixing it with incremental integers.
                """
                return PyMenu(self.service).execute('/file/import/cad_options/modify_all_duplicate_names', *args, **kwargs)
            def use_part_or_body_names_as_suffix_to_named_selections(self, *args, **kwargs):
                """
                Part or Body names are used as suffix for named selections spanning over multiple parts or bodies.
                """
                return PyMenu(self.service).execute('/file/import/cad_options/use_part_or_body_names_as_suffix_to_named_selections', *args, **kwargs)
            def strip_file_name_extension_from_naming(self, *args, **kwargs):
                """
                Strip file name extension from naming.
                """
                return PyMenu(self.service).execute('/file/import/cad_options/strip_file_name_extension_from_naming', *args, **kwargs)
            def import_label_for_body_named_selection(self, *args, **kwargs):
                """
                Import face zone labels for body named selections.
                """
                return PyMenu(self.service).execute('/file/import/cad_options/import_label_for_body_named_selection', *args, **kwargs)
            def strip_path_prefix_from_names(self, *args, **kwargs):
                """
                Strip path prefixes from naming.
                """
                return PyMenu(self.service).execute('/file/import/cad_options/strip_path_prefix_from_names', *args, **kwargs)
            def merge_objects_per_body_named_selection(self, *args, **kwargs):
                """
                Merge Objects per body named selection.
                """
                return PyMenu(self.service).execute('/file/import/cad_options/merge_objects_per_body_named_selection', *args, **kwargs)
            def extract_features(self, *args, **kwargs):
                """
                set the feature angle
                """
                return PyMenu(self.service).execute('/file/import/cad_options/extract_features', *args, **kwargs)
            def import_curvature_data_from_CAD(self, *args, **kwargs):
                """
                Import Curvature Data from CAD
                """
                return PyMenu(self.service).execute('/file/import/cad_options/import_curvature_data_from_CAD', *args, **kwargs)
            def create_label_per_body_during_cad_faceting(self, *args, **kwargs):
                """
                Create label Per Body during cad faceting.
                """
                return PyMenu(self.service).execute('/file/import/cad_options/create_label_per_body_during_cad_faceting', *args, **kwargs)

    class checkpoint(metaclass=PyMenuMeta):
        __doc__ = 'Checkpoint stores the mesh in the memory instead of writing it to a file.'
        def write_checkpoint(self, *args, **kwargs):
            """
            Write checkpoint.
            """
            return PyMenu(self.service).execute('/file/checkpoint/write_checkpoint', *args, **kwargs)
        def restore_checkpoint(self, *args, **kwargs):
            """
            Restore to checkpoint.
            """
            return PyMenu(self.service).execute('/file/checkpoint/restore_checkpoint', *args, **kwargs)
        def list_checkpoint_names(self, *args, **kwargs):
            """
            Get all checkpoint names.
            """
            return PyMenu(self.service).execute('/file/checkpoint/list_checkpoint_names', *args, **kwargs)
        def delete_checkpoint(self, *args, **kwargs):
            """
            Delete checkpoint.
            """
            return PyMenu(self.service).execute('/file/checkpoint/delete_checkpoint', *args, **kwargs)

    class parametric_project(metaclass=PyMenuMeta):
        __doc__ = 'Enter to create new project, read project, and save project'
        def new(self, *args, **kwargs):
            """
            Create New Project
            """
            return PyMenu(self.service).execute('/file/parametric_project/new', *args, **kwargs)
        def open(self, *args, **kwargs):
            """
            Open project
            """
            return PyMenu(self.service).execute('/file/parametric_project/open', *args, **kwargs)
        def save(self, *args, **kwargs):
            """
            Save Project
            """
            return PyMenu(self.service).execute('/file/parametric_project/save', *args, **kwargs)
        def save_as(self, *args, **kwargs):
            """
            Save As Project
            """
            return PyMenu(self.service).execute('/file/parametric_project/save_as', *args, **kwargs)
        def save_as_copy(self, *args, **kwargs):
            """
            Save As Copy
            """
            return PyMenu(self.service).execute('/file/parametric_project/save_as_copy', *args, **kwargs)
        def archive(self, *args, **kwargs):
            """
            Archive Project
            """
            return PyMenu(self.service).execute('/file/parametric_project/archive', *args, **kwargs)

class boundary(metaclass=PyMenuMeta):
    __doc__ = 'Enter the boundary menu'
    def auto_slit_faces(self, *args, **kwargs):
        """
        Automatically slits all embedded boundary face zones.
        """
        return PyMenu(self.service).execute('/boundary/auto_slit_faces', *args, **kwargs)
    def orient_faces_by_point(self, *args, **kwargs):
        """
        Orient Region based on Material Point.
        """
        return PyMenu(self.service).execute('/boundary/orient_faces_by_point', *args, **kwargs)
    def check_boundary_mesh(self, *args, **kwargs):
        """
        Report number of Delaunay violations on surface mesh and unused nodes.
        """
        return PyMenu(self.service).execute('/boundary/check_boundary_mesh', *args, **kwargs)
    def check_duplicate_geom(self, *args, **kwargs):
        """
        Check duplicated face threads in the geometry
        """
        return PyMenu(self.service).execute('/boundary/check_duplicate_geom', *args, **kwargs)
    def clear_marked_faces(self, *args, **kwargs):
        """
        Clear previously marked faces.
        """
        return PyMenu(self.service).execute('/boundary/clear_marked_faces', *args, **kwargs)
    def clear_marked_nodes(self, *args, **kwargs):
        """
        Clear previously marked nodes.
        """
        return PyMenu(self.service).execute('/boundary/clear_marked_nodes', *args, **kwargs)
    def coarsen_boundary_faces(self, *args, **kwargs):
        """
        Coarsen boundary face zones.
        """
        return PyMenu(self.service).execute('/boundary/coarsen_boundary_faces', *args, **kwargs)
    def count_marked_faces(self, *args, **kwargs):
        """
        Count marked faces.
        """
        return PyMenu(self.service).execute('/boundary/count_marked_faces', *args, **kwargs)
    def count_free_nodes(self, *args, **kwargs):
        """
        Count number of free nodes.
        """
        return PyMenu(self.service).execute('/boundary/count_free_nodes', *args, **kwargs)
    def count_unused_nodes(self, *args, **kwargs):
        """
        Count number of unused nodes.
        """
        return PyMenu(self.service).execute('/boundary/count_unused_nodes', *args, **kwargs)
    def count_unused_bound_node(self, *args, **kwargs):
        """
        Count number of unused boundary nodes.
        """
        return PyMenu(self.service).execute('/boundary/count_unused_bound_node', *args, **kwargs)
    def count_unused_faces(self, *args, **kwargs):
        """
        Count number of unused faces.
        """
        return PyMenu(self.service).execute('/boundary/count_unused_faces', *args, **kwargs)
    def compute_bounding_box(self, *args, **kwargs):
        """
        Computes bounding box for given zones.
        """
        return PyMenu(self.service).execute('/boundary/compute_bounding_box', *args, **kwargs)
    def create_bounding_box(self, *args, **kwargs):
        """
        Create bounding box for given zones.
        """
        return PyMenu(self.service).execute('/boundary/create_bounding_box', *args, **kwargs)
    def create_cylinder(self, *args, **kwargs):
        """
        Create cylinder using two axis end nodes/positions or, three points on the arc defining the cylinder.
        """
        return PyMenu(self.service).execute('/boundary/create_cylinder', *args, **kwargs)
    def create_plane_surface(self, *args, **kwargs):
        """
        Create plane surface
        """
        return PyMenu(self.service).execute('/boundary/create_plane_surface', *args, **kwargs)
    def create_swept_surface(self, *args, **kwargs):
        """
        Create surface by sweeping the edge along the vector
        """
        return PyMenu(self.service).execute('/boundary/create_swept_surface', *args, **kwargs)
    def create_revolved_surface(self, *args, **kwargs):
        """
        Create surface by revolving the edge along the vector
        """
        return PyMenu(self.service).execute('/boundary/create_revolved_surface', *args, **kwargs)
    def delete_duplicate_faces(self, *args, **kwargs):
        """
        Delete duplicate faces on specified zones.
        """
        return PyMenu(self.service).execute('/boundary/delete_duplicate_faces', *args, **kwargs)
    def delete_all_dup_faces(self, *args, **kwargs):
        """
        Delete all duplicate faces on all boundary zones.
        """
        return PyMenu(self.service).execute('/boundary/delete_all_dup_faces', *args, **kwargs)
    def delete_island_faces(self, *args, **kwargs):
        """
        Delete island faces or cavity.
        """
        return PyMenu(self.service).execute('/boundary/delete_island_faces', *args, **kwargs)
    def delete_unused_nodes(self, *args, **kwargs):
        """
        Delete nodes not belonging to any boundary faces.
        """
        return PyMenu(self.service).execute('/boundary/delete_unused_nodes', *args, **kwargs)
    def delete_unused_faces(self, *args, **kwargs):
        """
        Delete unused boundary faces.
        """
        return PyMenu(self.service).execute('/boundary/delete_unused_faces', *args, **kwargs)
    def delete_unconnected_faces(self, *args, **kwargs):
        """
        Delete unconnected face zones.
        """
        return PyMenu(self.service).execute('/boundary/delete_unconnected_faces', *args, **kwargs)
    def edge_limits(self, *args, **kwargs):
        """
        Print shortest and largest edges on boundary mesh.
        """
        return PyMenu(self.service).execute('/boundary/edge_limits', *args, **kwargs)
    def expand_marked_faces_by_rings(self, *args, **kwargs):
        """
        Mark rings of faces around marked faces
        """
        return PyMenu(self.service).execute('/boundary/expand_marked_faces_by_rings', *args, **kwargs)
    def face_distribution(self, *args, **kwargs):
        """
        Show face quality distribution.
        """
        return PyMenu(self.service).execute('/boundary/face_distribution', *args, **kwargs)
    def face_skewness(self, *args, **kwargs):
        """
        Show worse face skewness.
        """
        return PyMenu(self.service).execute('/boundary/face_skewness', *args, **kwargs)
    def jiggle_boundary_nodes(self, *args, **kwargs):
        """
        Perturb randomly nodal position.
        """
        return PyMenu(self.service).execute('/boundary/jiggle_boundary_nodes', *args, **kwargs)
    def improve_surface_mesh(self, *args, **kwargs):
        """
        Improve surface mesh by swapping face edges
        where Delaunay violations occur.
        """
        return PyMenu(self.service).execute('/boundary/improve_surface_mesh', *args, **kwargs)
    def make_periodic(self, *args, **kwargs):
        """
        Make periodic zone pair.
        """
        return PyMenu(self.service).execute('/boundary/make_periodic', *args, **kwargs)
    def recover_periodic_surfaces(self, *args, **kwargs):
        """
        Recover periodic surfaces
        """
        return PyMenu(self.service).execute('/boundary/recover_periodic_surfaces', *args, **kwargs)
    def set_periodicity(self, *args, **kwargs):
        """
        Set size field periodicity
        """
        return PyMenu(self.service).execute('/boundary/set_periodicity', *args, **kwargs)
    def mark_bad_quality_faces(self, *args, **kwargs):
        """
        Mark Bad Quality Faces
        """
        return PyMenu(self.service).execute('/boundary/mark_bad_quality_faces', *args, **kwargs)
    def mark_faces_in_region(self, *args, **kwargs):
        """
        Mark faces in local region.
        """
        return PyMenu(self.service).execute('/boundary/mark_faces_in_region', *args, **kwargs)
    def mark_face_intersection(self, *args, **kwargs):
        """
        Mark face intersection in face zones.
        """
        return PyMenu(self.service).execute('/boundary/mark_face_intersection', *args, **kwargs)
    def resolve_face_intersection(self, *args, **kwargs):
        """
        Resolve face intersection in tri-face zones.
        """
        return PyMenu(self.service).execute('/boundary/resolve_face_intersection', *args, **kwargs)
    def mark_face_proximity(self, *args, **kwargs):
        """
        Mark faces that are in proximity.
        """
        return PyMenu(self.service).execute('/boundary/mark_face_proximity', *args, **kwargs)
    def mark_duplicate_nodes(self, *args, **kwargs):
        """
        Mark duplicate nodes.
        """
        return PyMenu(self.service).execute('/boundary/mark_duplicate_nodes', *args, **kwargs)
    def merge_nodes(self, *args, **kwargs):
        """
        Merge duplicate nodes.  If a face has two of
        its nodes merged, then it is deleted.
        """
        return PyMenu(self.service).execute('/boundary/merge_nodes', *args, **kwargs)
    def merge_small_face_zones(self, *args, **kwargs):
        """
        Merge face zones having area less than min area with largest zone in its neighbor
        """
        return PyMenu(self.service).execute('/boundary/merge_small_face_zones', *args, **kwargs)
    def print_info(self, *args, **kwargs):
        """
        Print node/face/cell info.
        """
        return PyMenu(self.service).execute('/boundary/print_info', *args, **kwargs)
    def project_face_zone(self, *args, **kwargs):
        """
        Project face zone to a background mesh.
        """
        return PyMenu(self.service).execute('/boundary/project_face_zone', *args, **kwargs)
    def reset_element_type(self, *args, **kwargs):
        """
        Reset the element type (mixed, linear, tri or quad) of a boundary zone.
        """
        return PyMenu(self.service).execute('/boundary/reset_element_type', *args, **kwargs)
    def scale_nodes(self, *args, **kwargs):
        """
        Scale all nodes by the scale factor.
        """
        return PyMenu(self.service).execute('/boundary/scale_nodes', *args, **kwargs)
    def slit_boundary_face(self, *args, **kwargs):
        """
        Make slit in mesh at boundary face.
        All faces must have normals oriented in the same direction.
        """
        return PyMenu(self.service).execute('/boundary/slit_boundary_face', *args, **kwargs)
    def unmark_selected_faces(self, *args, **kwargs):
        """
        Clear mark on selected faces
        """
        return PyMenu(self.service).execute('/boundary/unmark_selected_faces', *args, **kwargs)
    def smooth_marked_faces(self, *args, **kwargs):
        """
        Smooth Marked faces on threads
        """
        return PyMenu(self.service).execute('/boundary/smooth_marked_faces', *args, **kwargs)
    def wrapper(self, *args, **kwargs):
        """
        Enter surface wrapper menu.
        """
        return PyMenu(self.service).execute('/boundary/wrapper', *args, **kwargs)
    def unmark_faces_in_zones(self, *args, **kwargs):
        """
        Unmark faces in zones
        """
        return PyMenu(self.service).execute('/boundary/unmark_faces_in_zones', *args, **kwargs)
    def delete_free_edge_faces(self, *args, **kwargs):
        """
        Remove faces with specified number of free edges.
        """
        return PyMenu(self.service).execute('/boundary/delete_free_edge_faces', *args, **kwargs)
    def fix_mconnected_edges(self, *args, **kwargs):
        """
        fix multi connected edges.
        """
        return PyMenu(self.service).execute('/boundary/fix_mconnected_edges', *args, **kwargs)

    class feature(metaclass=PyMenuMeta):
        __doc__ = 'Enter bounday feature menu.'
        def copy_edge_zones(self, *args, **kwargs):
            """
            Copy edge zones.
            """
            return PyMenu(self.service).execute('/boundary/feature/copy_edge_zones', *args, **kwargs)
        def create_edge_zones(self, *args, **kwargs):
            """
            Create edge loops of thread based on feature angle.
            """
            return PyMenu(self.service).execute('/boundary/feature/create_edge_zones', *args, **kwargs)
        def delete_edge_zones(self, *args, **kwargs):
            """
            Delete edge zones.
            """
            return PyMenu(self.service).execute('/boundary/feature/delete_edge_zones', *args, **kwargs)
        def delete_degenerated_edges(self, *args, **kwargs):
            """
            Delete from Edge Zones, Edges whose two end nodes are the same.
            """
            return PyMenu(self.service).execute('/boundary/feature/delete_degenerated_edges', *args, **kwargs)
        def edge_size_limits(self, *args, **kwargs):
            """
            Report edge size limits.
            """
            return PyMenu(self.service).execute('/boundary/feature/edge_size_limits', *args, **kwargs)
        def intersect_edge_zones(self, *args, **kwargs):
            """
            Intersect edge zones.
            """
            return PyMenu(self.service).execute('/boundary/feature/intersect_edge_zones', *args, **kwargs)
        def group(self, *args, **kwargs):
            """
            Group face and edge zones together.
            """
            return PyMenu(self.service).execute('/boundary/feature/group', *args, **kwargs)
        def list_edge_zones(self, *args, **kwargs):
            """
            List edge zones.
            """
            return PyMenu(self.service).execute('/boundary/feature/list_edge_zones', *args, **kwargs)
        def merge_edge_zones(self, *args, **kwargs):
            """
            Merge edge zones.
            """
            return PyMenu(self.service).execute('/boundary/feature/merge_edge_zones', *args, **kwargs)
        def orient_edge_direction(self, *args, **kwargs):
            """
            Orient edge zone directions.
            """
            return PyMenu(self.service).execute('/boundary/feature/orient_edge_direction', *args, **kwargs)
        def project_edge_zones(self, *args, **kwargs):
            """
            Project edge zones on specified face zone.
            """
            return PyMenu(self.service).execute('/boundary/feature/project_edge_zones', *args, **kwargs)
        def remesh_edge_zones(self, *args, **kwargs):
            """
            Remesh edge zones.
            """
            return PyMenu(self.service).execute('/boundary/feature/remesh_edge_zones', *args, **kwargs)
        def reverse_edge_direction(self, *args, **kwargs):
            """
            Reverse direction of edge loops.
            """
            return PyMenu(self.service).execute('/boundary/feature/reverse_edge_direction', *args, **kwargs)
        def separate_edge_zones(self, *args, **kwargs):
            """
            Separate edge zones based on connectivity and feature angle.
            """
            return PyMenu(self.service).execute('/boundary/feature/separate_edge_zones', *args, **kwargs)
        def separate_edge_zones_by_seed(self, *args, **kwargs):
            """
            Separate edge zones by seed.
            """
            return PyMenu(self.service).execute('/boundary/feature/separate_edge_zones_by_seed', *args, **kwargs)
        def toggle_edge_type(self, *args, **kwargs):
            """
            Toggle edge type between boundary and interior.
            """
            return PyMenu(self.service).execute('/boundary/feature/toggle_edge_type', *args, **kwargs)
        def ungroup(self, *args, **kwargs):
            """
            Ungroup previously grouped face and edge zones.
            """
            return PyMenu(self.service).execute('/boundary/feature/ungroup', *args, **kwargs)
        def separate_delete_small_edges(self, *args, **kwargs):
            """
            separates and deletes small edges.
            """
            return PyMenu(self.service).execute('/boundary/feature/separate_delete_small_edges', *args, **kwargs)

    class modify(metaclass=PyMenuMeta):
        __doc__ = 'Enter boundary modify menu.'
        def analyze_bnd_connectvty(self, *args, **kwargs):
            """
            Find and mark free edges/nodes and mutliple-connected edges/nodes.
            """
            return PyMenu(self.service).execute('/boundary/modify/analyze_bnd_connectvty', *args, **kwargs)
        def clear_selections(self, *args, **kwargs):
            """
            Clear all selections.
            """
            return PyMenu(self.service).execute('/boundary/modify/clear_selections', *args, **kwargs)
        def create(self, *args, **kwargs):
            """
            Create either nodes or faces.
            """
            return PyMenu(self.service).execute('/boundary/modify/create', *args, **kwargs)
        def auto_patch_holes(self, *args, **kwargs):
            """
            Patch zone(s) by filling holes.
            """
            return PyMenu(self.service).execute('/boundary/modify/auto_patch_holes', *args, **kwargs)
        def create_mid_node(self, *args, **kwargs):
            """
            Create a node at the midpoint between two selected nodes.
            """
            return PyMenu(self.service).execute('/boundary/modify/create_mid_node', *args, **kwargs)
        def collapse(self, *args, **kwargs):
            """
            Collapse pairs of nodes or edges or faces.
            """
            return PyMenu(self.service).execute('/boundary/modify/collapse', *args, **kwargs)
        def delete(self, *args, **kwargs):
            """
            Delete either nodes, faces or zones.
            """
            return PyMenu(self.service).execute('/boundary/modify/delete', *args, **kwargs)
        def deselect_last(self, *args, **kwargs):
            """
            Deselect last selection.
            """
            return PyMenu(self.service).execute('/boundary/modify/deselect_last', *args, **kwargs)
        def clear_skew_faces(self, *args, **kwargs):
            """
            Clear faces previously marked as skewed.
            """
            return PyMenu(self.service).execute('/boundary/modify/clear_skew_faces', *args, **kwargs)
        def list_selections(self, *args, **kwargs):
            """
            List selections.
            """
            return PyMenu(self.service).execute('/boundary/modify/list_selections', *args, **kwargs)
        def mark_skew_face(self, *args, **kwargs):
            """
            Mark face to skip when reporting worst skew face.
            """
            return PyMenu(self.service).execute('/boundary/modify/mark_skew_face', *args, **kwargs)
        def merge(self, *args, **kwargs):
            """
            Merge nodes.
            """
            return PyMenu(self.service).execute('/boundary/modify/merge', *args, **kwargs)
        def move(self, *args, **kwargs):
            """
            Move nodes to new positions.
            """
            return PyMenu(self.service).execute('/boundary/modify/move', *args, **kwargs)
        def delta_move(self, *args, **kwargs):
            """
            Move nodes to new positions.
            """
            return PyMenu(self.service).execute('/boundary/modify/delta_move', *args, **kwargs)
        def rezone(self, *args, **kwargs):
            """
            Change the zone faces belong to.
            """
            return PyMenu(self.service).execute('/boundary/modify/rezone', *args, **kwargs)
        def select_entity(self, *args, **kwargs):
            """
            Select a entity.
            """
            return PyMenu(self.service).execute('/boundary/modify/select_entity', *args, **kwargs)
        def select_filter(self, *args, **kwargs):
            """
            Select probe filter.
            """
            return PyMenu(self.service).execute('/boundary/modify/select_filter', *args, **kwargs)
        def select_probe(self, *args, **kwargs):
            """
            Select probe function.
            """
            return PyMenu(self.service).execute('/boundary/modify/select_probe', *args, **kwargs)
        def select_position(self, *args, **kwargs):
            """
            Select a position.
            """
            return PyMenu(self.service).execute('/boundary/modify/select_position', *args, **kwargs)
        def select_zone(self, *args, **kwargs):
            """
            Select a zone.
            """
            return PyMenu(self.service).execute('/boundary/modify/select_zone', *args, **kwargs)
        def show_filter(self, *args, **kwargs):
            """
            Show current probe filter.
            """
            return PyMenu(self.service).execute('/boundary/modify/show_filter', *args, **kwargs)
        def show_probe(self, *args, **kwargs):
            """
            Show current probe function.
            """
            return PyMenu(self.service).execute('/boundary/modify/show_probe', *args, **kwargs)
        def skew(self, *args, **kwargs):
            """
            Display the highest skewed boundary face.
            """
            return PyMenu(self.service).execute('/boundary/modify/skew', *args, **kwargs)
        def smooth(self, *args, **kwargs):
            """
            Smooth selected nodes.
            """
            return PyMenu(self.service).execute('/boundary/modify/smooth', *args, **kwargs)
        def split_face(self, *args, **kwargs):
            """
            Split two selected faces into four.
            """
            return PyMenu(self.service).execute('/boundary/modify/split_face', *args, **kwargs)
        def swap(self, *args, **kwargs):
            """
            Swap edges.
            """
            return PyMenu(self.service).execute('/boundary/modify/swap', *args, **kwargs)
        def hole_feature_angle(self, *args, **kwargs):
            """
            Angle defining boundary of hole.
            """
            return PyMenu(self.service).execute('/boundary/modify/hole_feature_angle', *args, **kwargs)
        def undo(self, *args, **kwargs):
            """
            Undo last modification.
            """
            return PyMenu(self.service).execute('/boundary/modify/undo', *args, **kwargs)
        def next_skew(self, *args, **kwargs):
            """
            Display the next highest skewed boundary face.
            """
            return PyMenu(self.service).execute('/boundary/modify/next_skew', *args, **kwargs)
        def skew_report_zone(self, *args, **kwargs):
            """
            Face zone for which skewness has to be reported
            """
            return PyMenu(self.service).execute('/boundary/modify/skew_report_zone', *args, **kwargs)
        def local_remesh(self, *args, **kwargs):
            """
            Remesh locally starting from face seeds.
            """
            return PyMenu(self.service).execute('/boundary/modify/local_remesh', *args, **kwargs)
        def select_visible_entities(self, *args, **kwargs):
            """
            Set visual selection mode of entities
            """
            return PyMenu(self.service).execute('/boundary/modify/select_visible_entities', *args, **kwargs)

        class patch_options(metaclass=PyMenuMeta):
            __doc__ = 'Settings for Patching zone(s) by filling holes.'
            def remesh(self, *args, **kwargs):
                """
                Remeshes newly added patches
                """
                return PyMenu(self.service).execute('/boundary/modify/patch_options/remesh', *args, **kwargs)
            def separate(self, *args, **kwargs):
                """
                Separates newly added patches
                """
                return PyMenu(self.service).execute('/boundary/modify/patch_options/separate', *args, **kwargs)

    class refine(metaclass=PyMenuMeta):
        __doc__ = 'Enter refine boundary face menu.'
        def auto_refine(self, *args, **kwargs):
            """
            Automatically refine faces based on proximity with other faces.
            """
            return PyMenu(self.service).execute('/boundary/refine/auto_refine', *args, **kwargs)
        def clear(self, *args, **kwargs):
            """
            Clear the refine flag at the faces.
            """
            return PyMenu(self.service).execute('/boundary/refine/clear', *args, **kwargs)
        def count(self, *args, **kwargs):
            """
            Count the number of faces flagged on thread(s).
            """
            return PyMenu(self.service).execute('/boundary/refine/count', *args, **kwargs)
        def mark(self, *args, **kwargs):
            """
            Mark faces in region for refinement
            """
            return PyMenu(self.service).execute('/boundary/refine/mark', *args, **kwargs)
        def limits(self, *args, **kwargs):
            """
            List face zone information on number of faces flagged and range of face size.
            """
            return PyMenu(self.service).execute('/boundary/refine/limits', *args, **kwargs)
        def refine(self, *args, **kwargs):
            """
            Refine the flagged faces
            """
            return PyMenu(self.service).execute('/boundary/refine/refine', *args, **kwargs)

        class local_regions(metaclass=PyMenuMeta):
            __doc__ = 'Enter the refine-local menu'
            def define(self, *args, **kwargs):
                """
                Define a refinement region's parameters.
                """
                return PyMenu(self.service).execute('/boundary/refine/local_regions/define', *args, **kwargs)
            def delete(self, *args, **kwargs):
                """
                Delete a refinement region.
                """
                return PyMenu(self.service).execute('/boundary/refine/local_regions/delete', *args, **kwargs)
            def init(self, *args, **kwargs):
                """
                Delete all current regions and add the default refinement region.
                """
                return PyMenu(self.service).execute('/boundary/refine/local_regions/init', *args, **kwargs)
            def list_all_regions(self, *args, **kwargs):
                """
                List all refinement regions.
                """
                return PyMenu(self.service).execute('/boundary/refine/local_regions/list_all_regions', *args, **kwargs)

    class remesh(metaclass=PyMenuMeta):
        __doc__ = 'Enter remeshing boundary face zone menu.'
        def create_edge_loops(self, *args, **kwargs):
            """
            Create edge loops of thread based on feature angle.
            """
            return PyMenu(self.service).execute('/boundary/remesh/create_edge_loops', *args, **kwargs)
        def create_intersect_loop(self, *args, **kwargs):
            """
            Create edge loop of intersection.
            """
            return PyMenu(self.service).execute('/boundary/remesh/create_intersect_loop', *args, **kwargs)
        def create_all_intrst_loops(self, *args, **kwargs):
            """
            Create edge loop of intersection for all boundary zones in current domain.
            """
            return PyMenu(self.service).execute('/boundary/remesh/create_all_intrst_loops', *args, **kwargs)
        def create_join_loop(self, *args, **kwargs):
            """
            Create edge loop of overlap region.
            """
            return PyMenu(self.service).execute('/boundary/remesh/create_join_loop', *args, **kwargs)
        def create_stitch_loop(self, *args, **kwargs):
            """
            Create edge loop of stitch edges.
            """
            return PyMenu(self.service).execute('/boundary/remesh/create_stitch_loop', *args, **kwargs)
        def delete_overlapped_edges(self, *args, **kwargs):
            """
            Delete edges that overlapped selected loops.
            """
            return PyMenu(self.service).execute('/boundary/remesh/delete_overlapped_edges', *args, **kwargs)
        def intersect_face_zones(self, *args, **kwargs):
            """
            Intersection face zones.
            """
            return PyMenu(self.service).execute('/boundary/remesh/intersect_face_zones', *args, **kwargs)
        def intersect_all_face_zones(self, *args, **kwargs):
            """
            Intersect all face zones.
            """
            return PyMenu(self.service).execute('/boundary/remesh/intersect_all_face_zones', *args, **kwargs)
        def remesh_face_zone(self, *args, **kwargs):
            """
            Retriangulate a face zone.
            """
            return PyMenu(self.service).execute('/boundary/remesh/remesh_face_zone', *args, **kwargs)
        def remesh_marked_faces(self, *args, **kwargs):
            """
            Locally remesh marked faces
            """
            return PyMenu(self.service).execute('/boundary/remesh/remesh_marked_faces', *args, **kwargs)
        def mark_intersecting_faces(self, *args, **kwargs):
            """
            Mark faces on zones.
            """
            return PyMenu(self.service).execute('/boundary/remesh/mark_intersecting_faces', *args, **kwargs)
        def remesh_face_zones_conformally(self, *args, **kwargs):
            """
            Retriangulate face zones while maintaining conformity.
            """
            return PyMenu(self.service).execute('/boundary/remesh/remesh_face_zones_conformally', *args, **kwargs)
        def remesh_constant_size(self, *args, **kwargs):
            """
            Retriangulate face zones to constant triangle size while maintaining conformity.
            """
            return PyMenu(self.service).execute('/boundary/remesh/remesh_constant_size', *args, **kwargs)
        def coarsen_and_refine(self, *args, **kwargs):
            """
            Coarsen and refine face zones according to size function.
            """
            return PyMenu(self.service).execute('/boundary/remesh/coarsen_and_refine', *args, **kwargs)
        def remesh_overlapping_zones(self, *args, **kwargs):
            """
            Remeshing overlapping face zones.
            """
            return PyMenu(self.service).execute('/boundary/remesh/remesh_overlapping_zones', *args, **kwargs)
        def join_face_zones(self, *args, **kwargs):
            """
            Join face zones.
            """
            return PyMenu(self.service).execute('/boundary/remesh/join_face_zones', *args, **kwargs)
        def join_all_face_zones(self, *args, **kwargs):
            """
            Intersect all face zones.
            """
            return PyMenu(self.service).execute('/boundary/remesh/join_all_face_zones', *args, **kwargs)
        def mark_join_faces(self, *args, **kwargs):
            """
            Mark faces on zones.
            """
            return PyMenu(self.service).execute('/boundary/remesh/mark_join_faces', *args, **kwargs)
        def stitch_face_zones(self, *args, **kwargs):
            """
            Stitch edges on zones.
            """
            return PyMenu(self.service).execute('/boundary/remesh/stitch_face_zones', *args, **kwargs)
        def stitch_all_face_zones(self, *args, **kwargs):
            """
            Intersect all face zones.
            """
            return PyMenu(self.service).execute('/boundary/remesh/stitch_all_face_zones', *args, **kwargs)
        def triangulate(self, *args, **kwargs):
            """
            Create triangulation from existing quad face zone.
            """
            return PyMenu(self.service).execute('/boundary/remesh/triangulate', *args, **kwargs)
        def mark_stitch_faces(self, *args, **kwargs):
            """
            Mark faces on zones.
            """
            return PyMenu(self.service).execute('/boundary/remesh/mark_stitch_faces', *args, **kwargs)
        def faceted_stitch_zones(self, *args, **kwargs):
            """
            Stitch free edges on zones.
            """
            return PyMenu(self.service).execute('/boundary/remesh/faceted_stitch_zones', *args, **kwargs)
        def insert_edge_zone(self, *args, **kwargs):
            """
            Insert edge into face zonoe.
            """
            return PyMenu(self.service).execute('/boundary/remesh/insert_edge_zone', *args, **kwargs)
        def clear_marked_faces(self, *args, **kwargs):
            """
            Clear previously marked faces
            """
            return PyMenu(self.service).execute('/boundary/remesh/clear_marked_faces', *args, **kwargs)
        def stitch_with_preserve_boundary(self, *args, **kwargs):
            """
            Stitch volume to boundary zone at free faces
            """
            return PyMenu(self.service).execute('/boundary/remesh/stitch_with_preserve_boundary', *args, **kwargs)

        class controls(metaclass=PyMenuMeta):
            __doc__ = 'Edge loop tools text menu.'
            def remesh_method(self, *args, **kwargs):
                """
                Available methods: 1-constant 2-arithmetic 3-geometric.
                """
                return PyMenu(self.service).execute('/boundary/remesh/controls/remesh_method', *args, **kwargs)
            def quadratic_recon(self, *args, **kwargs):
                """
                Turn on/off quadratic reconstruction of edge loops.
                """
                return PyMenu(self.service).execute('/boundary/remesh/controls/quadratic_recon', *args, **kwargs)
            def spacing(self, *args, **kwargs):
                """
                Set first and last edge spacing.
                """
                return PyMenu(self.service).execute('/boundary/remesh/controls/spacing', *args, **kwargs)
            def delete_overlapped(self, *args, **kwargs):
                """
                Turn on/off deletion of overlapped edges.
                """
                return PyMenu(self.service).execute('/boundary/remesh/controls/delete_overlapped', *args, **kwargs)
            def tolerance(self, *args, **kwargs):
                """
                Set intersection tolerance (absolute unit)
                """
                return PyMenu(self.service).execute('/boundary/remesh/controls/tolerance', *args, **kwargs)
            def project_method(self, *args, **kwargs):
                """
                Available methods: 0-closest 1-direction
                """
                return PyMenu(self.service).execute('/boundary/remesh/controls/project_method', *args, **kwargs)
            def direction(self, *args, **kwargs):
                """
                Set direction of edge loop projection
                """
                return PyMenu(self.service).execute('/boundary/remesh/controls/direction', *args, **kwargs)
            def proximity_local_search(self, *args, **kwargs):
                """
                Include selected face for proximity calculation
                """
                return PyMenu(self.service).execute('/boundary/remesh/controls/proximity_local_search', *args, **kwargs)

            class intersect(metaclass=PyMenuMeta):
                __doc__ = 'Enter the intersect control menu.'
                def within_tolerance(self, *args, **kwargs):
                    """
                    Turn on/off tolerant intersection.
                    """
                    return PyMenu(self.service).execute('/boundary/remesh/controls/intersect/within_tolerance', *args, **kwargs)
                def delete_overlap(self, *args, **kwargs):
                    """
                    Turn on/off deletion of overlapped region.
                    """
                    return PyMenu(self.service).execute('/boundary/remesh/controls/intersect/delete_overlap', *args, **kwargs)
                def ignore_parallel_faces(self, *args, **kwargs):
                    """
                    Turn on/off ignore parallel faces.
                    """
                    return PyMenu(self.service).execute('/boundary/remesh/controls/intersect/ignore_parallel_faces', *args, **kwargs)
                def refine_region(self, *args, **kwargs):
                    """
                    Turn on/off refinement of intersection region.
                    """
                    return PyMenu(self.service).execute('/boundary/remesh/controls/intersect/refine_region', *args, **kwargs)
                def separate(self, *args, **kwargs):
                    """
                    Turn on/off separation of intersection region.
                    """
                    return PyMenu(self.service).execute('/boundary/remesh/controls/intersect/separate', *args, **kwargs)
                def absolute_tolerance(self, *args, **kwargs):
                    """
                    Turn on/off absolute tolerance.
                    """
                    return PyMenu(self.service).execute('/boundary/remesh/controls/intersect/absolute_tolerance', *args, **kwargs)
                def retri_improve(self, *args, **kwargs):
                    """
                    Turn on/off mesh improvement.
                    """
                    return PyMenu(self.service).execute('/boundary/remesh/controls/intersect/retri_improve', *args, **kwargs)
                def stitch_preserve(self, *args, **kwargs):
                    """
                    Turn on/off stitch preserve first zone shape.
                    """
                    return PyMenu(self.service).execute('/boundary/remesh/controls/intersect/stitch_preserve', *args, **kwargs)
                def tolerance(self, *args, **kwargs):
                    """
                    Intersection tolerance.
                    """
                    return PyMenu(self.service).execute('/boundary/remesh/controls/intersect/tolerance', *args, **kwargs)
                def join_match_angle(self, *args, **kwargs):
                    """
                    Max allowable angle between normals of faces to join.
                    """
                    return PyMenu(self.service).execute('/boundary/remesh/controls/intersect/join_match_angle', *args, **kwargs)
                def feature_angle(self, *args, **kwargs):
                    """
                    Angle used to determine angle feature edges.
                    """
                    return PyMenu(self.service).execute('/boundary/remesh/controls/intersect/feature_angle', *args, **kwargs)
                def join_project_angle(self, *args, **kwargs):
                    """
                    Max allowable angle between face normal and project direction for join.
                    """
                    return PyMenu(self.service).execute('/boundary/remesh/controls/intersect/join_project_angle', *args, **kwargs)
                def remesh_post_intersection(self, *args, **kwargs):
                    """
                    Remesh after intersection
                    """
                    return PyMenu(self.service).execute('/boundary/remesh/controls/intersect/remesh_post_intersection', *args, **kwargs)

        class size_functions(metaclass=PyMenuMeta):
            __doc__ = 'Enable specification of size functions'
            def create(self, *args, **kwargs):
                """
                Add size function
                """
                return PyMenu(self.service).execute('/boundary/remesh/size_functions/create', *args, **kwargs)
            def delete(self, *args, **kwargs):
                """
                Delete Size Functions
                """
                return PyMenu(self.service).execute('/boundary/remesh/size_functions/delete', *args, **kwargs)
            def delete_all(self, *args, **kwargs):
                """
                Delete All Size Functions
                """
                return PyMenu(self.service).execute('/boundary/remesh/size_functions/delete_all', *args, **kwargs)
            def compute(self, *args, **kwargs):
                """
                Compute Size-functions
                """
                return PyMenu(self.service).execute('/boundary/remesh/size_functions/compute', *args, **kwargs)
            def list(self, *args, **kwargs):
                """
                List all Size function parameters.
                """
                return PyMenu(self.service).execute('/boundary/remesh/size_functions/list', *args, **kwargs)
            def create_defaults(self, *args, **kwargs):
                """
                Creates default curvature & proximty size functions acting on all faces and edges.
                """
                return PyMenu(self.service).execute('/boundary/remesh/size_functions/create_defaults', *args, **kwargs)
            def set_global_controls(self, *args, **kwargs):
                """
                Set controls for global controls
                """
                return PyMenu(self.service).execute('/boundary/remesh/size_functions/set_global_controls', *args, **kwargs)
            def enable_periodicity_filter(self, *args, **kwargs):
                """
                Enable size field periodicity
                """
                return PyMenu(self.service).execute('/boundary/remesh/size_functions/enable_periodicity_filter', *args, **kwargs)
            def disable_periodicity_filter(self, *args, **kwargs):
                """
                Disable size field periodicity
                """
                return PyMenu(self.service).execute('/boundary/remesh/size_functions/disable_periodicity_filter', *args, **kwargs)
            def list_periodicity_filter(self, *args, **kwargs):
                """
                List periodic in size field
                """
                return PyMenu(self.service).execute('/boundary/remesh/size_functions/list_periodicity_filter', *args, **kwargs)
            def set_scaling_filter(self, *args, **kwargs):
                """
                Set scaling filter on size field.
                """
                return PyMenu(self.service).execute('/boundary/remesh/size_functions/set_scaling_filter', *args, **kwargs)
            def reset_global_controls(self, *args, **kwargs):
                """
                Reset controls for global controls
                """
                return PyMenu(self.service).execute('/boundary/remesh/size_functions/reset_global_controls', *args, **kwargs)
            def set_prox_gap_tolerance(self, *args, **kwargs):
                """
                Set proximity min gap tolerance relative to global min-size
                """
                return PyMenu(self.service).execute('/boundary/remesh/size_functions/set_prox_gap_tolerance', *args, **kwargs)
            def triangulate_quad_faces(self, *args, **kwargs):
                """
                Replace non-triangular face zones with triangulated face zones during size field computation
                """
                return PyMenu(self.service).execute('/boundary/remesh/size_functions/triangulate_quad_faces', *args, **kwargs)
            def use_cad_imported_curvature(self, *args, **kwargs):
                """
                Use curvature data imported from CAD
                """
                return PyMenu(self.service).execute('/boundary/remesh/size_functions/use_cad_imported_curvature', *args, **kwargs)

            class contours(metaclass=PyMenuMeta):
                __doc__ = 'Menu to contour of size field'
                def draw(self, *args, **kwargs):
                    """
                    Draw size field contour on face zones
                    """
                    return PyMenu(self.service).execute('/boundary/remesh/size_functions/contours/draw', *args, **kwargs)

                class set(metaclass=PyMenuMeta):
                    __doc__ = 'Set contour options.'
                    def refine_facets(self, *args, **kwargs):
                        """
                        Option to refine facets virtually? for better contour resolution
                        """
                        return PyMenu(self.service).execute('/boundary/remesh/size_functions/contours/set/refine_facets', *args, **kwargs)

            class controls(metaclass=PyMenuMeta):
                __doc__ = 'Menu to control different behavior of sf'
                def meshed_sf_behavior(self, *args, **kwargs):
                    """
                    set meshed size function processing to hard
                    """
                    return PyMenu(self.service).execute('/boundary/remesh/size_functions/controls/meshed_sf_behavior', *args, **kwargs)
                def curvature_method(self, *args, **kwargs):
                    """
                    Option to get facet curvature
                    """
                    return PyMenu(self.service).execute('/boundary/remesh/size_functions/controls/curvature_method', *args, **kwargs)

    class improve(metaclass=PyMenuMeta):
        __doc__ = 'Enter Imporve  boundary face zone menu.'
        def collapse_bad_faces(self, *args, **kwargs):
            """
            Collapse short edge of faces with high aspect ratio.
            """
            return PyMenu(self.service).execute('/boundary/improve/collapse_bad_faces', *args, **kwargs)
        def improve(self, *args, **kwargs):
            """
            Improve skewness of tri boundary face zones.
            """
            return PyMenu(self.service).execute('/boundary/improve/improve', *args, **kwargs)
        def smooth(self, *args, **kwargs):
            """
            Smooth  face zones using laplace smoothing.
            """
            return PyMenu(self.service).execute('/boundary/improve/smooth', *args, **kwargs)
        def swap(self, *args, **kwargs):
            """
            Improve surface mesh by swapping face edges
            where Delaunay violations occur.
            """
            return PyMenu(self.service).execute('/boundary/improve/swap', *args, **kwargs)
        def degree_swap(self, *args, **kwargs):
            """
            Perform swap on boundary mesh based on node degree.
            """
            return PyMenu(self.service).execute('/boundary/improve/degree_swap', *args, **kwargs)

    class separate(metaclass=PyMenuMeta):
        __doc__ = 'Enter separate boundary face menu.'
        def mark_faces_in_region(self, *args, **kwargs):
            """
            Mark faces in local region.
            """
            return PyMenu(self.service).execute('/boundary/separate/mark_faces_in_region', *args, **kwargs)
        def sep_face_zone_by_angle(self, *args, **kwargs):
            """
            Move faces to a new zone based on significant angle.
            """
            return PyMenu(self.service).execute('/boundary/separate/sep_face_zone_by_angle', *args, **kwargs)
        def sep_face_zone_by_cnbor(self, *args, **kwargs):
            """
            Move faces to a new zone based on cell neighbors.
            """
            return PyMenu(self.service).execute('/boundary/separate/sep_face_zone_by_cnbor', *args, **kwargs)
        def sep_face_zone_by_mark(self, *args, **kwargs):
            """
            Move faces marked to new zone.
            """
            return PyMenu(self.service).execute('/boundary/separate/sep_face_zone_by_mark', *args, **kwargs)
        def sep_face_zone_by_region(self, *args, **kwargs):
            """
            Move non-contiguous faces or faces separated by an intersecting wall to a new zone.
            """
            return PyMenu(self.service).execute('/boundary/separate/sep_face_zone_by_region', *args, **kwargs)
        def sep_face_zone_by_seed(self, *args, **kwargs):
            """
            Move faces connected to seed whose angle satisfies given angle constraint.
            """
            return PyMenu(self.service).execute('/boundary/separate/sep_face_zone_by_seed', *args, **kwargs)
        def sep_face_zone_by_seed_angle(self, *args, **kwargs):
            """
            Move faces connected to seed whose normal fall within the specified cone.
            """
            return PyMenu(self.service).execute('/boundary/separate/sep_face_zone_by_seed_angle', *args, **kwargs)
        def sep_face_zone_by_shape(self, *args, **kwargs):
            """
            Move faces based on face shape.
            """
            return PyMenu(self.service).execute('/boundary/separate/sep_face_zone_by_shape', *args, **kwargs)

        class local_regions(metaclass=PyMenuMeta):
            __doc__ = 'Enter the separate-local menu'
            def define(self, *args, **kwargs):
                """
                Define a refinement region's parameters.
                """
                return PyMenu(self.service).execute('/boundary/separate/local_regions/define', *args, **kwargs)
            def delete(self, *args, **kwargs):
                """
                Delete a refinement region.
                """
                return PyMenu(self.service).execute('/boundary/separate/local_regions/delete', *args, **kwargs)
            def init(self, *args, **kwargs):
                """
                Delete all current regions and add the default refinement region.
                """
                return PyMenu(self.service).execute('/boundary/separate/local_regions/init', *args, **kwargs)
            def list_all_regions(self, *args, **kwargs):
                """
                List all refinement regions.
                """
                return PyMenu(self.service).execute('/boundary/separate/local_regions/list_all_regions', *args, **kwargs)

    class manage(metaclass=PyMenuMeta):
        __doc__ = 'Enter face zone menu.'
        def auto_delete_nodes(self, *args, **kwargs):
            """
            Automatically delete unused nodes after deleting faces.
            """
            return PyMenu(self.service).execute('/boundary/manage/auto_delete_nodes', *args, **kwargs)
        def copy(self, *args, **kwargs):
            """
            Copy all nodes and faces of specified face zones.
            """
            return PyMenu(self.service).execute('/boundary/manage/copy', *args, **kwargs)
        def change_prefix(self, *args, **kwargs):
            """
            Change the prefix for specified face zones.
            """
            return PyMenu(self.service).execute('/boundary/manage/change_prefix', *args, **kwargs)
        def change_suffix(self, *args, **kwargs):
            """
            Change the suffix for specified face zones.
            """
            return PyMenu(self.service).execute('/boundary/manage/change_suffix', *args, **kwargs)
        def create(self, *args, **kwargs):
            """
            Create new face zone.
            """
            return PyMenu(self.service).execute('/boundary/manage/create', *args, **kwargs)
        def delete(self, *args, **kwargs):
            """
            Delete face zone, leaving nodes.
            """
            return PyMenu(self.service).execute('/boundary/manage/delete', *args, **kwargs)
        def flip(self, *args, **kwargs):
            """
            Flip the orientation of all face normals on the face zone.
            """
            return PyMenu(self.service).execute('/boundary/manage/flip', *args, **kwargs)
        def id(self, *args, **kwargs):
            """
            Give zone a new id number.
            """
            return PyMenu(self.service).execute('/boundary/manage/id', *args, **kwargs)
        def list(self, *args, **kwargs):
            """
            List boundary face zones.
            """
            return PyMenu(self.service).execute('/boundary/manage/list', *args, **kwargs)
        def merge(self, *args, **kwargs):
            """
            Merge two or more face zones.
            """
            return PyMenu(self.service).execute('/boundary/manage/merge', *args, **kwargs)
        def name(self, *args, **kwargs):
            """
            Give zone a new name.
            """
            return PyMenu(self.service).execute('/boundary/manage/name', *args, **kwargs)
        def remove_suffix(self, *args, **kwargs):
            """
            Remove the leftmost ':' and the characters after it in the face zone names.
            """
            return PyMenu(self.service).execute('/boundary/manage/remove_suffix', *args, **kwargs)
        def orient(self, *args, **kwargs):
            """
            Consistently orient zones.
            """
            return PyMenu(self.service).execute('/boundary/manage/orient', *args, **kwargs)
        def origin(self, *args, **kwargs):
            """
            Set the origin of the mesh coordinates.
            """
            return PyMenu(self.service).execute('/boundary/manage/origin', *args, **kwargs)
        def rotate(self, *args, **kwargs):
            """
            Rotate all nodes of specified face zones.
            """
            return PyMenu(self.service).execute('/boundary/manage/rotate', *args, **kwargs)
        def rotate_model(self, *args, **kwargs):
            """
            Rotate all nodes.
            """
            return PyMenu(self.service).execute('/boundary/manage/rotate_model', *args, **kwargs)
        def scale(self, *args, **kwargs):
            """
            Scale all nodes of specified face zones.
            """
            return PyMenu(self.service).execute('/boundary/manage/scale', *args, **kwargs)
        def scale_model(self, *args, **kwargs):
            """
            Scale all nodes.
            """
            return PyMenu(self.service).execute('/boundary/manage/scale_model', *args, **kwargs)
        def translate(self, *args, **kwargs):
            """
            Translate all nodes of specified face zones.
            """
            return PyMenu(self.service).execute('/boundary/manage/translate', *args, **kwargs)
        def translate_model(self, *args, **kwargs):
            """
            Translate all nodes.
            """
            return PyMenu(self.service).execute('/boundary/manage/translate_model', *args, **kwargs)
        def type(self, *args, **kwargs):
            """
            Change face zone type.
            """
            return PyMenu(self.service).execute('/boundary/manage/type', *args, **kwargs)

        class user_defined_groups(metaclass=PyMenuMeta):
            __doc__ = 'Collect boundary zones to form logical groups.'
            def create(self, *args, **kwargs):
                """
                Create a new User Defined Group.
                """
                return PyMenu(self.service).execute('/boundary/manage/user_defined_groups/create', *args, **kwargs)
            def activate(self, *args, **kwargs):
                """
                Activate a User Defined Group.
                """
                return PyMenu(self.service).execute('/boundary/manage/user_defined_groups/activate', *args, **kwargs)
            def update(self, *args, **kwargs):
                """
                Update a User Defined Group.
                """
                return PyMenu(self.service).execute('/boundary/manage/user_defined_groups/update', *args, **kwargs)
            def delete(self, *args, **kwargs):
                """
                Delete a User Defined Group.
                """
                return PyMenu(self.service).execute('/boundary/manage/user_defined_groups/delete', *args, **kwargs)
            def list(self, *args, **kwargs):
                """
                List User Defined Groups.
                """
                return PyMenu(self.service).execute('/boundary/manage/user_defined_groups/list', *args, **kwargs)

    class shell_boundary_layer(metaclass=PyMenuMeta):
        __doc__ = 'Enter the shell boundary layer menu.'
        def create(self, *args, **kwargs):
            """
            Create shell boundary layers from one or more face zones.
            """
            return PyMenu(self.service).execute('/boundary/shell_boundary_layer/create', *args, **kwargs)

        class controls(metaclass=PyMenuMeta):
            __doc__ = 'Shell Boundary Layer Controls'

            class zone_specific_growth(metaclass=PyMenuMeta):
                __doc__ = 'Shell boundary Layer Growth Controls'
                def apply_growth(self, *args, **kwargs):
                    """
                    Apply  shell boundary la growth on individual edge zones.
                    """
                    return PyMenu(self.service).execute('/boundary/shell_boundary_layer/controls/zone_specific_growth/apply_growth', *args, **kwargs)
                def clear_growth(self, *args, **kwargs):
                    """
                    Clear shell boundary layer specific growth on individual edge zones.
                    """
                    return PyMenu(self.service).execute('/boundary/shell_boundary_layer/controls/zone_specific_growth/clear_growth', *args, **kwargs)

    class boundary_conditions(metaclass=PyMenuMeta):
        __doc__ = 'Enter manage boundary conditions menu.'
        def copy(self, *args, **kwargs):
            """
            Copy boundary conditions.
            """
            return PyMenu(self.service).execute('/boundary/boundary_conditions/copy', *args, **kwargs)
        def clear(self, *args, **kwargs):
            """
            Clear boundary conditions.
            """
            return PyMenu(self.service).execute('/boundary/boundary_conditions/clear', *args, **kwargs)
        def clear_all(self, *args, **kwargs):
            """
            Clear all boundary conditions.
            """
            return PyMenu(self.service).execute('/boundary/boundary_conditions/clear_all', *args, **kwargs)

class cad_assemblies(metaclass=PyMenuMeta):
    __doc__ = 'Menu for cad assemblies'
    def draw(self, *args, **kwargs):
        """
        Draw CAD assemblies.
        """
        return PyMenu(self.service).execute('/cad_assemblies/draw', *args, **kwargs)
    def create_objects(self, *args, **kwargs):
        """
        Create Objects from CAD assemblies.
        """
        return PyMenu(self.service).execute('/cad_assemblies/create_objects', *args, **kwargs)
    def add_to_object(self, *args, **kwargs):
        """
        Add CAD assemblies to existing object.
        """
        return PyMenu(self.service).execute('/cad_assemblies/add_to_object', *args, **kwargs)
    def replace_object(self, *args, **kwargs):
        """
        Replace CAD assemblies in existing object.
        """
        return PyMenu(self.service).execute('/cad_assemblies/replace_object', *args, **kwargs)
    def extract_edges_zones(self, *args, **kwargs):
        """
        Extract feature edges for CAD assemblies.
        """
        return PyMenu(self.service).execute('/cad_assemblies/extract_edges_zones', *args, **kwargs)
    def update_cad_assemblies(self, *args, **kwargs):
        """
        Update CAD assemblies.
        """
        return PyMenu(self.service).execute('/cad_assemblies/update_cad_assemblies', *args, **kwargs)
    def rename(self, *args, **kwargs):
        """
        Rename CAD entity.
        """
        return PyMenu(self.service).execute('/cad_assemblies/rename', *args, **kwargs)
    def add_prefix(self, *args, **kwargs):
        """
        Add Prefix to CAD entity.
        """
        return PyMenu(self.service).execute('/cad_assemblies/add_prefix', *args, **kwargs)
    def delete_cad_assemblies(self, *args, **kwargs):
        """
        Delete CAD Assemblies.
        """
        return PyMenu(self.service).execute('/cad_assemblies/delete_cad_assemblies', *args, **kwargs)

    class draw_options(metaclass=PyMenuMeta):
        __doc__ = 'CAD draw options.'
        def add_to_graphics(self, *args, **kwargs):
            """
            Add CAD entity to graphics.
            """
            return PyMenu(self.service).execute('/cad_assemblies/draw_options/add_to_graphics', *args, **kwargs)
        def remove_from_graphics(self, *args, **kwargs):
            """
            Set one object per body, face or object.
            """
            return PyMenu(self.service).execute('/cad_assemblies/draw_options/remove_from_graphics', *args, **kwargs)
        def draw_unlabelled_zones(self, *args, **kwargs):
            """
            Import edge zones for update.
            """
            return PyMenu(self.service).execute('/cad_assemblies/draw_options/draw_unlabelled_zones', *args, **kwargs)

    class manage_state(metaclass=PyMenuMeta):
        __doc__ = 'States for CAD assemblies.'
        def unlock(self, *args, **kwargs):
            """
            Unlock CAD assemblies.
            """
            return PyMenu(self.service).execute('/cad_assemblies/manage_state/unlock', *args, **kwargs)
        def suppress(self, *args, **kwargs):
            """
            Suppress CAD assemblies.
            """
            return PyMenu(self.service).execute('/cad_assemblies/manage_state/suppress', *args, **kwargs)
        def unsuppress(self, *args, **kwargs):
            """
            Unsuppress CAD assemblies.
            """
            return PyMenu(self.service).execute('/cad_assemblies/manage_state/unsuppress', *args, **kwargs)

    class labels(metaclass=PyMenuMeta):
        __doc__ = 'CAD label options.'
        def draw(self, *args, **kwargs):
            """
            Draw Labels.
            """
            return PyMenu(self.service).execute('/cad_assemblies/labels/draw', *args, **kwargs)
        def add_to_graphics(self, *args, **kwargs):
            """
            Add Labels to graphics.
            """
            return PyMenu(self.service).execute('/cad_assemblies/labels/add_to_graphics', *args, **kwargs)
        def remove_from_graphics(self, *args, **kwargs):
            """
            Remove Labels from graphics.
            """
            return PyMenu(self.service).execute('/cad_assemblies/labels/remove_from_graphics', *args, **kwargs)
        def delete(self, *args, **kwargs):
            """
            Delete Labels.
            """
            return PyMenu(self.service).execute('/cad_assemblies/labels/delete', *args, **kwargs)
        def rename(self, *args, **kwargs):
            """
            Rename Labels.
            """
            return PyMenu(self.service).execute('/cad_assemblies/labels/rename', *args, **kwargs)

    class update_options(metaclass=PyMenuMeta):
        __doc__ = 'Settings for CAD update.'
        def tessellation(self, *args, **kwargs):
            """
            Set tessellation controls for cad import.
            """
            return PyMenu(self.service).execute('/cad_assemblies/update_options/tessellation', *args, **kwargs)
        def one_zone_per(self, *args, **kwargs):
            """
            Set one object per body, face or object.
            """
            return PyMenu(self.service).execute('/cad_assemblies/update_options/one_zone_per', *args, **kwargs)
        def one_object_per(self, *args, **kwargs):
            """
            Set one leaf entity per body, part or file.
            """
            return PyMenu(self.service).execute('/cad_assemblies/update_options/one_object_per', *args, **kwargs)
        def import_edge_zones(self, *args, **kwargs):
            """
            Import edge zones for update.
            """
            return PyMenu(self.service).execute('/cad_assemblies/update_options/import_edge_zones', *args, **kwargs)

class preferences(metaclass=PyMenuMeta):
    __doc__ = 'Set preferences'

    class appearance(metaclass=PyMenuMeta):
        __doc__ = ''
        def application_font_size(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/application_font_size', *args, **kwargs)
        def axis_triad(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/axis_triad', *args, **kwargs)
        def color_theme(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/color_theme', *args, **kwargs)
        def completer(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/completer', *args, **kwargs)
        def custom_title_bar(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/custom_title_bar', *args, **kwargs)
        def default_view(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/default_view', *args, **kwargs)
        def graphics_background_color1(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/graphics_background_color1', *args, **kwargs)
        def graphics_background_color2(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/graphics_background_color2', *args, **kwargs)
        def graphics_background_style(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/graphics_background_style', *args, **kwargs)
        def graphics_color_theme(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/graphics_color_theme', *args, **kwargs)
        def graphics_default_manual_face_color(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/graphics_default_manual_face_color', *args, **kwargs)
        def graphics_default_manual_node_color(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/graphics_default_manual_node_color', *args, **kwargs)
        def graphics_edge_color(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/graphics_edge_color', *args, **kwargs)
        def graphics_foreground_color(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/graphics_foreground_color', *args, **kwargs)
        def graphics_partition_boundary_color(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/graphics_partition_boundary_color', *args, **kwargs)
        def graphics_surface_color(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/graphics_surface_color', *args, **kwargs)
        def graphics_title_window_framecolor(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/graphics_title_window_framecolor', *args, **kwargs)
        def graphics_view(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/graphics_view', *args, **kwargs)
        def graphics_wall_face_color(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/graphics_wall_face_color', *args, **kwargs)
        def group_by_tree_view(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/group_by_tree_view', *args, **kwargs)
        def model_color_scheme(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/model_color_scheme', *args, **kwargs)
        def number_of_files_recently_used(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/number_of_files_recently_used', *args, **kwargs)
        def number_of_pastel_colors(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/number_of_pastel_colors', *args, **kwargs)
        def pastel_color_saturation(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/pastel_color_saturation', *args, **kwargs)
        def pastel_color_value(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/pastel_color_value', *args, **kwargs)
        def quick_property_view(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/quick_property_view', *args, **kwargs)
        def ruler(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/ruler', *args, **kwargs)
        def show_enabled_models(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/show_enabled_models', *args, **kwargs)
        def show_interface_children_zone(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/show_interface_children_zone', *args, **kwargs)
        def show_model_edges(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/show_model_edges', *args, **kwargs)
        def solution_mode_edge_color_in_meshing_mode(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/solution_mode_edge_color_in_meshing_mode', *args, **kwargs)
        def startup_page(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/startup_page', *args, **kwargs)
        def surface_emissivity(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/surface_emissivity', *args, **kwargs)
        def surface_specularity(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/surface_specularity', *args, **kwargs)
        def surface_specularity_for_contours(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/surface_specularity_for_contours', *args, **kwargs)
        def titles(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/titles', *args, **kwargs)
        def titles_border_offset(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/appearance/titles_border_offset', *args, **kwargs)

        class ansys_logo(metaclass=PyMenuMeta):
            __doc__ = ''
            def color(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/appearance/ansys_logo/color', *args, **kwargs)
            def visible(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/appearance/ansys_logo/visible', *args, **kwargs)

        class charts(metaclass=PyMenuMeta):
            __doc__ = ''
            def curve_colors(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/appearance/charts/curve_colors', *args, **kwargs)
            def enable_open_glfor_modern_plots(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/appearance/charts/enable_open_glfor_modern_plots', *args, **kwargs)
            def legend_alignment(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/appearance/charts/legend_alignment', *args, **kwargs)
            def legend_visibility(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/appearance/charts/legend_visibility', *args, **kwargs)
            def modern_plots_enabled(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/appearance/charts/modern_plots_enabled', *args, **kwargs)
            def modern_plots_points_threshold(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/appearance/charts/modern_plots_points_threshold', *args, **kwargs)
            def plots_behavior(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/appearance/charts/plots_behavior', *args, **kwargs)
            def print_plot_data(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/appearance/charts/print_plot_data', *args, **kwargs)
            def print_residuals_data(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/appearance/charts/print_residuals_data', *args, **kwargs)
            def threshold(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/appearance/charts/threshold', *args, **kwargs)

            class font(metaclass=PyMenuMeta):
                __doc__ = ''
                def axes(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/appearance/charts/font/axes', *args, **kwargs)
                def axes_titles(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/appearance/charts/font/axes_titles', *args, **kwargs)
                def legend(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/appearance/charts/font/legend', *args, **kwargs)
                def title(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/appearance/charts/font/title', *args, **kwargs)

            class text_color(metaclass=PyMenuMeta):
                __doc__ = ''
                def axes(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/appearance/charts/text_color/axes', *args, **kwargs)
                def axes_titles(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/appearance/charts/text_color/axes_titles', *args, **kwargs)
                def legend(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/appearance/charts/text_color/legend', *args, **kwargs)
                def title(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/appearance/charts/text_color/title', *args, **kwargs)

        class selections(metaclass=PyMenuMeta):
            __doc__ = ''
            def general_displacement(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/appearance/selections/general_displacement', *args, **kwargs)
            def highlight_edge_color(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/appearance/selections/highlight_edge_color', *args, **kwargs)
            def highlight_edge_weight(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/appearance/selections/highlight_edge_weight', *args, **kwargs)
            def highlight_face_color(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/appearance/selections/highlight_face_color', *args, **kwargs)
            def highlight_gloss(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/appearance/selections/highlight_gloss', *args, **kwargs)
            def highlight_specular_component(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/appearance/selections/highlight_specular_component', *args, **kwargs)
            def highlight_transparency(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/appearance/selections/highlight_transparency', *args, **kwargs)
            def mouse_hover_probe_values_enabled(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/appearance/selections/mouse_hover_probe_values_enabled', *args, **kwargs)
            def mouse_over_highlight_enabled(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/appearance/selections/mouse_over_highlight_enabled', *args, **kwargs)
            def probe_tooltip_hide_delay_timer(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/appearance/selections/probe_tooltip_hide_delay_timer', *args, **kwargs)
            def probe_tooltip_show_delay_timer(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/appearance/selections/probe_tooltip_show_delay_timer', *args, **kwargs)

    class general(metaclass=PyMenuMeta):
        __doc__ = ''
        def advanced_partition(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/general/advanced_partition', *args, **kwargs)
        def automatic_transcript(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/general/automatic_transcript', *args, **kwargs)
        def default_ioformat(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/general/default_ioformat', *args, **kwargs)
        def dock_editor(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/general/dock_editor', *args, **kwargs)
        def enable_parametric_study(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/general/enable_parametric_study', *args, **kwargs)
        def enable_project_file(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/general/enable_project_file', *args, **kwargs)
        def flow_model(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/general/flow_model', *args, **kwargs)
        def idle_timeout(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/general/idle_timeout', *args, **kwargs)
        def key_behavioral_changes_message(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/general/key_behavioral_changes_message', *args, **kwargs)
        def qaservice_message(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/general/qaservice_message', *args, **kwargs)
        def utlcreate_physics_on_mode_change(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/general/utlcreate_physics_on_mode_change', *args, **kwargs)
        def utlmode(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/general/utlmode', *args, **kwargs)

    class gpuapp(metaclass=PyMenuMeta):
        __doc__ = ''
        def alpha_features(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/gpuapp/alpha_features', *args, **kwargs)

    class graphics(metaclass=PyMenuMeta):
        __doc__ = ''
        def animation_option(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/graphics/animation_option', *args, **kwargs)
        def double_buffering(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/graphics/double_buffering', *args, **kwargs)
        def enable_non_object_based_workflow(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/graphics/enable_non_object_based_workflow', *args, **kwargs)
        def event_poll_interval(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/graphics/event_poll_interval', *args, **kwargs)
        def event_poll_timeout(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/graphics/event_poll_timeout', *args, **kwargs)
        def force_key_frame_animation_markers_to_off(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/graphics/force_key_frame_animation_markers_to_off', *args, **kwargs)
        def graphics_window_line_width(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/graphics/graphics_window_line_width', *args, **kwargs)
        def graphics_window_point_symbol(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/graphics/graphics_window_point_symbol', *args, **kwargs)
        def hidden_surface_removal_method(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/graphics/hidden_surface_removal_method', *args, **kwargs)
        def higher_resolution_graphics_window_line_width(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/graphics/higher_resolution_graphics_window_line_width', *args, **kwargs)
        def lower_resolution_graphics_window_line_width(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/graphics/lower_resolution_graphics_window_line_width', *args, **kwargs)
        def marker_drawing_mode(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/graphics/marker_drawing_mode', *args, **kwargs)
        def max_graphics_text_size(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/graphics/max_graphics_text_size', *args, **kwargs)
        def min_graphics_text_size(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/graphics/min_graphics_text_size', *args, **kwargs)
        def plot_legend_margin(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/graphics/plot_legend_margin', *args, **kwargs)
        def point_tool_size(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/graphics/point_tool_size', *args, **kwargs)
        def remove_partition_lines(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/graphics/remove_partition_lines', *args, **kwargs)
        def remove_partition_lines_tolerance(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/graphics/remove_partition_lines_tolerance', *args, **kwargs)
        def rotation_centerpoint_visible(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/graphics/rotation_centerpoint_visible', *args, **kwargs)
        def scroll_wheel_event_end_timer(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/graphics/scroll_wheel_event_end_timer', *args, **kwargs)
        def set_camera_normal_to_surface_increments(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/graphics/set_camera_normal_to_surface_increments', *args, **kwargs)
        def show_hidden_lines(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/graphics/show_hidden_lines', *args, **kwargs)
        def show_hidden_surfaces(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/graphics/show_hidden_surfaces', *args, **kwargs)
        def switch_to_open_glfor_remote_visualization(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/graphics/switch_to_open_glfor_remote_visualization', *args, **kwargs)
        def test_use_external_function(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/graphics/test_use_external_function', *args, **kwargs)
        def text_window_line_width(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/graphics/text_window_line_width', *args, **kwargs)

        class boundary_markers(metaclass=PyMenuMeta):
            __doc__ = ''
            def color_option(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/boundary_markers/color_option', *args, **kwargs)
            def enabled(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/boundary_markers/enabled', *args, **kwargs)
            def exclude_from_bounding(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/boundary_markers/exclude_from_bounding', *args, **kwargs)
            def inlet_color(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/boundary_markers/inlet_color', *args, **kwargs)
            def marker_fraction(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/boundary_markers/marker_fraction', *args, **kwargs)
            def marker_size_limiting_scale_multiplier(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/boundary_markers/marker_size_limiting_scale_multiplier', *args, **kwargs)
            def markers_limit(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/boundary_markers/markers_limit', *args, **kwargs)
            def outlet_color(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/boundary_markers/outlet_color', *args, **kwargs)
            def scale_marker(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/boundary_markers/scale_marker', *args, **kwargs)
            def show_inlet_markers(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/boundary_markers/show_inlet_markers', *args, **kwargs)
            def show_outlet_markers(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/boundary_markers/show_outlet_markers', *args, **kwargs)

        class colormap_settings(metaclass=PyMenuMeta):
            __doc__ = ''
            def alignment(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/colormap_settings/alignment', *args, **kwargs)
            def aspect_ratio_when_horizontal(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/colormap_settings/aspect_ratio_when_horizontal', *args, **kwargs)
            def aspect_ratio_when_vertical(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/colormap_settings/aspect_ratio_when_vertical', *args, **kwargs)
            def auto_refit_on_resize(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/colormap_settings/auto_refit_on_resize', *args, **kwargs)
            def automatic_resize(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/colormap_settings/automatic_resize', *args, **kwargs)
            def border_style(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/colormap_settings/border_style', *args, **kwargs)
            def colormap(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/colormap_settings/colormap', *args, **kwargs)
            def isolines_position_offset(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/colormap_settings/isolines_position_offset', *args, **kwargs)
            def labels(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/colormap_settings/labels', *args, **kwargs)
            def levels(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/colormap_settings/levels', *args, **kwargs)
            def log_scale(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/colormap_settings/log_scale', *args, **kwargs)
            def major_length_to_screen_ratio_when_horizontal(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/colormap_settings/major_length_to_screen_ratio_when_horizontal', *args, **kwargs)
            def major_length_to_screen_ratio_when_vertical(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/colormap_settings/major_length_to_screen_ratio_when_vertical', *args, **kwargs)
            def margin_from_edge_to_screen_ratio(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/colormap_settings/margin_from_edge_to_screen_ratio', *args, **kwargs)
            def max_size_scale_factor(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/colormap_settings/max_size_scale_factor', *args, **kwargs)
            def min_size_scale_factor(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/colormap_settings/min_size_scale_factor', *args, **kwargs)
            def number_format_precision(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/colormap_settings/number_format_precision', *args, **kwargs)
            def number_format_type(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/colormap_settings/number_format_type', *args, **kwargs)
            def show_colormap(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/colormap_settings/show_colormap', *args, **kwargs)
            def skip_value(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/colormap_settings/skip_value', *args, **kwargs)
            def text_behavior(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/colormap_settings/text_behavior', *args, **kwargs)
            def text_font_automatic_horizontal_size(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/colormap_settings/text_font_automatic_horizontal_size', *args, **kwargs)
            def text_font_automatic_size(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/colormap_settings/text_font_automatic_size', *args, **kwargs)
            def text_font_automatic_units(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/colormap_settings/text_font_automatic_units', *args, **kwargs)
            def text_font_automatic_vertical_size(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/colormap_settings/text_font_automatic_vertical_size', *args, **kwargs)
            def text_font_fixed_horizontal_size(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/colormap_settings/text_font_fixed_horizontal_size', *args, **kwargs)
            def text_font_fixed_size(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/colormap_settings/text_font_fixed_size', *args, **kwargs)
            def text_font_fixed_units(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/colormap_settings/text_font_fixed_units', *args, **kwargs)
            def text_font_fixed_vertical_size(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/colormap_settings/text_font_fixed_vertical_size', *args, **kwargs)
            def text_font_name(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/colormap_settings/text_font_name', *args, **kwargs)
            def text_truncation_limit_for_horizontal_colormaps(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/colormap_settings/text_truncation_limit_for_horizontal_colormaps', *args, **kwargs)
            def text_truncation_limit_for_vertical_colormaps(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/colormap_settings/text_truncation_limit_for_vertical_colormaps', *args, **kwargs)
            def type(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/colormap_settings/type', *args, **kwargs)
            def use_no_sub_windows(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/colormap_settings/use_no_sub_windows', *args, **kwargs)

        class embedded_windows(metaclass=PyMenuMeta):
            __doc__ = ''
            def default_embedded_mesh_windows_view(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/embedded_windows/default_embedded_mesh_windows_view', *args, **kwargs)
            def default_embedded_windows_view(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/embedded_windows/default_embedded_windows_view', *args, **kwargs)
            def save_embedded_window_layout(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/embedded_windows/save_embedded_window_layout', *args, **kwargs)
            def show_border_for_embedded_window(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/embedded_windows/show_border_for_embedded_window', *args, **kwargs)

        class export_video_settings(metaclass=PyMenuMeta):
            __doc__ = ''
            def video_format(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/export_video_settings/video_format', *args, **kwargs)
            def video_fps(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/export_video_settings/video_fps', *args, **kwargs)
            def video_quality(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/export_video_settings/video_quality', *args, **kwargs)
            def video_resoution_x(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/export_video_settings/video_resoution_x', *args, **kwargs)
            def video_resoution_y(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/export_video_settings/video_resoution_y', *args, **kwargs)
            def video_scale(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/export_video_settings/video_scale', *args, **kwargs)
            def video_smooth_scaling(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/export_video_settings/video_smooth_scaling', *args, **kwargs)
            def video_use_frame_resolution(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/export_video_settings/video_use_frame_resolution', *args, **kwargs)

            class advanced_video_quality_options(metaclass=PyMenuMeta):
                __doc__ = ''
                def bit_rate_quality(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/graphics/export_video_settings/advanced_video_quality_options/bit_rate_quality', *args, **kwargs)
                def bitrate(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/graphics/export_video_settings/advanced_video_quality_options/bitrate', *args, **kwargs)
                def compression_method(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/graphics/export_video_settings/advanced_video_quality_options/compression_method', *args, **kwargs)
                def enable_h264(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/graphics/export_video_settings/advanced_video_quality_options/enable_h264', *args, **kwargs)
                def key_frames(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/graphics/export_video_settings/advanced_video_quality_options/key_frames', *args, **kwargs)

        class graphics_effects(metaclass=PyMenuMeta):
            __doc__ = ''
            def ambient_occlusion_enabled(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/graphics_effects/ambient_occlusion_enabled', *args, **kwargs)
            def ambient_occlusion_quality(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/graphics_effects/ambient_occlusion_quality', *args, **kwargs)
            def ambient_occlusion_strength(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/graphics_effects/ambient_occlusion_strength', *args, **kwargs)
            def anti_aliasing(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/graphics_effects/anti_aliasing', *args, **kwargs)
            def bloom_blur(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/graphics_effects/bloom_blur', *args, **kwargs)
            def bloom_enabled(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/graphics_effects/bloom_enabled', *args, **kwargs)
            def bloom_strength(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/graphics_effects/bloom_strength', *args, **kwargs)
            def grid_color(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/graphics_effects/grid_color', *args, **kwargs)
            def grid_plane_count(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/graphics_effects/grid_plane_count', *args, **kwargs)
            def grid_plane_enabled(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/graphics_effects/grid_plane_enabled', *args, **kwargs)
            def grid_plane_offset(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/graphics_effects/grid_plane_offset', *args, **kwargs)
            def grid_plane_size_factor(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/graphics_effects/grid_plane_size_factor', *args, **kwargs)
            def plane_direction(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/graphics_effects/plane_direction', *args, **kwargs)
            def reflections_enabled(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/graphics_effects/reflections_enabled', *args, **kwargs)
            def shadow_map_enabled(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/graphics_effects/shadow_map_enabled', *args, **kwargs)
            def show_edge_reflections(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/graphics_effects/show_edge_reflections', *args, **kwargs)
            def show_marker_reflections(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/graphics_effects/show_marker_reflections', *args, **kwargs)
            def simple_shadows_enabled(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/graphics_effects/simple_shadows_enabled', *args, **kwargs)
            def update_after_mouse_release(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/graphics_effects/update_after_mouse_release', *args, **kwargs)

        class hardcopy_settings(metaclass=PyMenuMeta):
            __doc__ = ''
            def export_edges_for_avz(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/hardcopy_settings/export_edges_for_avz', *args, **kwargs)
            def hardcopy_driver(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/hardcopy_settings/hardcopy_driver', *args, **kwargs)
            def hardcopy_line_width(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/hardcopy_settings/hardcopy_line_width', *args, **kwargs)
            def hardware_image_accel(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/hardcopy_settings/hardware_image_accel', *args, **kwargs)
            def post_script_permission_override(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/hardcopy_settings/post_script_permission_override', *args, **kwargs)
            def save_embedded_hardcopies_separately(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/hardcopy_settings/save_embedded_hardcopies_separately', *args, **kwargs)
            def save_embedded_windows_in_hardcopy(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/hardcopy_settings/save_embedded_windows_in_hardcopy', *args, **kwargs)
            def transparent_embedded_windows(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/hardcopy_settings/transparent_embedded_windows', *args, **kwargs)

        class lighting(metaclass=PyMenuMeta):
            __doc__ = ''
            def ambient_light_intensity(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/lighting/ambient_light_intensity', *args, **kwargs)
            def headlight(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/lighting/headlight', *args, **kwargs)
            def headlight_intensity(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/lighting/headlight_intensity', *args, **kwargs)
            def lighting_method(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/lighting/lighting_method', *args, **kwargs)

        class manage_hoops_memory(metaclass=PyMenuMeta):
            __doc__ = ''
            def enabled(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/manage_hoops_memory/enabled', *args, **kwargs)
            def hsfimport_limit(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/manage_hoops_memory/hsfimport_limit', *args, **kwargs)

        class material_effects(metaclass=PyMenuMeta):
            __doc__ = ''
            def decimation_filter(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/material_effects/decimation_filter', *args, **kwargs)
            def parameterization_source(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/material_effects/parameterization_source', *args, **kwargs)
            def tiling_style(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/material_effects/tiling_style', *args, **kwargs)

        class meshing_mode(metaclass=PyMenuMeta):
            __doc__ = ''
            def graphics_window_display_timeout(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/meshing_mode/graphics_window_display_timeout', *args, **kwargs)
            def graphics_window_display_timeout_value(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/meshing_mode/graphics_window_display_timeout_value', *args, **kwargs)

        class performance(metaclass=PyMenuMeta):
            __doc__ = ''
            def optimize_for(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/performance/optimize_for', *args, **kwargs)
            def ratio_of_target_frame_rate_to_classify_heavy_geometry(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/performance/ratio_of_target_frame_rate_to_classify_heavy_geometry', *args, **kwargs)
            def ratio_of_target_frame_rate_to_declassify_heavy_geometry(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/performance/ratio_of_target_frame_rate_to_declassify_heavy_geometry', *args, **kwargs)

            class fast_display_mode(metaclass=PyMenuMeta):
                __doc__ = ''
                def culling(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/graphics/performance/fast_display_mode/culling', *args, **kwargs)
                def faces_shown(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/graphics/performance/fast_display_mode/faces_shown', *args, **kwargs)
                def markers_decimation(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/graphics/performance/fast_display_mode/markers_decimation', *args, **kwargs)
                def nodes_shown(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/graphics/performance/fast_display_mode/nodes_shown', *args, **kwargs)
                def perimeter_edges_shown(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/graphics/performance/fast_display_mode/perimeter_edges_shown', *args, **kwargs)
                def silhouette_shown(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/graphics/performance/fast_display_mode/silhouette_shown', *args, **kwargs)
                def status(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/graphics/performance/fast_display_mode/status', *args, **kwargs)
                def transparency(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/graphics/performance/fast_display_mode/transparency', *args, **kwargs)

            class minimum_frame_rate(metaclass=PyMenuMeta):
                __doc__ = ''
                def dynamic_adjustment(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/graphics/performance/minimum_frame_rate/dynamic_adjustment', *args, **kwargs)
                def enabled(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/graphics/performance/minimum_frame_rate/enabled', *args, **kwargs)
                def fixed_culling_value(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/graphics/performance/minimum_frame_rate/fixed_culling_value', *args, **kwargs)
                def maximum_culling_threshold(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/graphics/performance/minimum_frame_rate/maximum_culling_threshold', *args, **kwargs)
                def minimum_culling_threshold(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/graphics/performance/minimum_frame_rate/minimum_culling_threshold', *args, **kwargs)
                def target_fps(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/graphics/performance/minimum_frame_rate/target_fps', *args, **kwargs)

        class transparency(metaclass=PyMenuMeta):
            __doc__ = ''
            def algorithm_for_modern_drivers(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/transparency/algorithm_for_modern_drivers', *args, **kwargs)
            def depth_peeling_layers(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/transparency/depth_peeling_layers', *args, **kwargs)
            def depth_peeling_preference(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/transparency/depth_peeling_preference', *args, **kwargs)
            def quick_moves(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/transparency/quick_moves', *args, **kwargs)
            def zsort_options(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/transparency/zsort_options', *args, **kwargs)

        class vector_settings(metaclass=PyMenuMeta):
            __doc__ = ''
            def arrow3_dradius1_factor(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/vector_settings/arrow3_dradius1_factor', *args, **kwargs)
            def arrow3_dradius2_factor(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/vector_settings/arrow3_dradius2_factor', *args, **kwargs)
            def arrowhead3_dradius1_factor(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/vector_settings/arrowhead3_dradius1_factor', *args, **kwargs)
            def line_arrow3_dperpendicular_radius(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/graphics/vector_settings/line_arrow3_dperpendicular_radius', *args, **kwargs)

    class mat_pro_app(metaclass=PyMenuMeta):
        __doc__ = ''
        def beta_features(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/mat_pro_app/beta_features', *args, **kwargs)
        def console(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/mat_pro_app/console', *args, **kwargs)
        def focus(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/mat_pro_app/focus', *args, **kwargs)
        def warning(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/mat_pro_app/warning', *args, **kwargs)

    class meshing_workflow(metaclass=PyMenuMeta):
        __doc__ = ''
        def checkpointing_option(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/meshing_workflow/checkpointing_option', *args, **kwargs)
        def save_checkpoint_files(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/meshing_workflow/save_checkpoint_files', *args, **kwargs)
        def temp_folder(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/meshing_workflow/temp_folder', *args, **kwargs)
        def templates_folder(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/meshing_workflow/templates_folder', *args, **kwargs)
        def verbosity(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/meshing_workflow/verbosity', *args, **kwargs)

        class draw_settings(metaclass=PyMenuMeta):
            __doc__ = ''
            def auto_draw(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/meshing_workflow/draw_settings/auto_draw', *args, **kwargs)
            def face_zone_limit(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/meshing_workflow/draw_settings/face_zone_limit', *args, **kwargs)
            def facet_limit(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/meshing_workflow/draw_settings/facet_limit', *args, **kwargs)

    class navigation(metaclass=PyMenuMeta):
        __doc__ = ''

        class mouse_mapping(metaclass=PyMenuMeta):
            __doc__ = ''
            def mousemaptheme(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/navigation/mouse_mapping/mousemaptheme', *args, **kwargs)

            class additional(metaclass=PyMenuMeta):
                __doc__ = ''
                def ctrllmbclick(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/navigation/mouse_mapping/additional/ctrllmbclick', *args, **kwargs)
                def ctrllmbdrag(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/navigation/mouse_mapping/additional/ctrllmbdrag', *args, **kwargs)
                def ctrlmmbclick(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/navigation/mouse_mapping/additional/ctrlmmbclick', *args, **kwargs)
                def ctrlmmbdrag(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/navigation/mouse_mapping/additional/ctrlmmbdrag', *args, **kwargs)
                def ctrlrmbclick(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/navigation/mouse_mapping/additional/ctrlrmbclick', *args, **kwargs)
                def ctrlrmbdrag(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/navigation/mouse_mapping/additional/ctrlrmbdrag', *args, **kwargs)
                def mouseprobe(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/navigation/mouse_mapping/additional/mouseprobe', *args, **kwargs)
                def mousewheel(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/navigation/mouse_mapping/additional/mousewheel', *args, **kwargs)
                def mousewheelsensitivity(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/navigation/mouse_mapping/additional/mousewheelsensitivity', *args, **kwargs)
                def reversewheeldirection(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/navigation/mouse_mapping/additional/reversewheeldirection', *args, **kwargs)
                def shiftlmbclick(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/navigation/mouse_mapping/additional/shiftlmbclick', *args, **kwargs)
                def shiftlmbdrag(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/navigation/mouse_mapping/additional/shiftlmbdrag', *args, **kwargs)
                def shiftmmbclick(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/navigation/mouse_mapping/additional/shiftmmbclick', *args, **kwargs)
                def shiftmmbdrag(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/navigation/mouse_mapping/additional/shiftmmbdrag', *args, **kwargs)
                def shiftrmbclick(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/navigation/mouse_mapping/additional/shiftrmbclick', *args, **kwargs)
                def shiftrmbdrag(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/navigation/mouse_mapping/additional/shiftrmbdrag', *args, **kwargs)

            class basic(metaclass=PyMenuMeta):
                __doc__ = ''
                def lmb(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/navigation/mouse_mapping/basic/lmb', *args, **kwargs)
                def lmbclick(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/navigation/mouse_mapping/basic/lmbclick', *args, **kwargs)
                def mmb(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/navigation/mouse_mapping/basic/mmb', *args, **kwargs)
                def mmbclick(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/navigation/mouse_mapping/basic/mmbclick', *args, **kwargs)
                def rmb(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/navigation/mouse_mapping/basic/rmb', *args, **kwargs)
                def rmbclick(self, *args, **kwargs):
                    """
                    """
                    return PyMenu(self.service).execute('/preferences/navigation/mouse_mapping/basic/rmbclick', *args, **kwargs)

    class prj_app(metaclass=PyMenuMeta):
        __doc__ = ''
        def advanced_flag(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/prj_app/advanced_flag', *args, **kwargs)
        def beta_flag(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/prj_app/beta_flag', *args, **kwargs)
        def cffoutput(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/prj_app/cffoutput', *args, **kwargs)
        def default_folder(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/prj_app/default_folder', *args, **kwargs)
        def display_mesh_after_case_load(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/prj_app/display_mesh_after_case_load', *args, **kwargs)
        def multi_console(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/prj_app/multi_console', *args, **kwargs)
        def ncpu(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/prj_app/ncpu', *args, **kwargs)
        def session_color(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/prj_app/session_color', *args, **kwargs)
        def show_fluent_window(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/prj_app/show_fluent_window', *args, **kwargs)
        def uilayout(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/prj_app/uilayout', *args, **kwargs)
        def use_default_folder(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/prj_app/use_default_folder', *args, **kwargs)
        def use_fluent_graphics(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/prj_app/use_fluent_graphics', *args, **kwargs)
        def use_launcher(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/prj_app/use_launcher', *args, **kwargs)

    class simulation(metaclass=PyMenuMeta):
        __doc__ = ''
        def flow_model(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/simulation/flow_model', *args, **kwargs)
        def local_residual_scaling(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/simulation/local_residual_scaling', *args, **kwargs)

        class report_definitions(metaclass=PyMenuMeta):
            __doc__ = ''
            def automatic_plot_file(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/simulation/report_definitions/automatic_plot_file', *args, **kwargs)
            def report_plot_history_data_size(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/simulation/report_definitions/report_plot_history_data_size', *args, **kwargs)

    class turbo_workflow(metaclass=PyMenuMeta):
        __doc__ = ''
        def checkpointing_option(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/turbo_workflow/checkpointing_option', *args, **kwargs)
        def save_checkpoint_files(self, *args, **kwargs):
            """
            """
            return PyMenu(self.service).execute('/preferences/turbo_workflow/save_checkpoint_files', *args, **kwargs)

        class cell_zone_settings(metaclass=PyMenuMeta):
            __doc__ = ''
            def czsearch_order(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/turbo_workflow/cell_zone_settings/czsearch_order', *args, **kwargs)
            def rotating(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/turbo_workflow/cell_zone_settings/rotating', *args, **kwargs)
            def stationary(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/turbo_workflow/cell_zone_settings/stationary', *args, **kwargs)

        class face_zone_settings(metaclass=PyMenuMeta):
            __doc__ = ''
            def blade_region(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/turbo_workflow/face_zone_settings/blade_region', *args, **kwargs)
            def fzsearch_order(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/turbo_workflow/face_zone_settings/fzsearch_order', *args, **kwargs)
            def hub_region(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/turbo_workflow/face_zone_settings/hub_region', *args, **kwargs)
            def inlet_region(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/turbo_workflow/face_zone_settings/inlet_region', *args, **kwargs)
            def interior_region(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/turbo_workflow/face_zone_settings/interior_region', *args, **kwargs)
            def outlet_region(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/turbo_workflow/face_zone_settings/outlet_region', *args, **kwargs)
            def periodic1_region(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/turbo_workflow/face_zone_settings/periodic1_region', *args, **kwargs)
            def periodic2_region(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/turbo_workflow/face_zone_settings/periodic2_region', *args, **kwargs)
            def shroud_region(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/turbo_workflow/face_zone_settings/shroud_region', *args, **kwargs)
            def symmetry_region(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/turbo_workflow/face_zone_settings/symmetry_region', *args, **kwargs)
            def tip1_region(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/turbo_workflow/face_zone_settings/tip1_region', *args, **kwargs)
            def tip2_region(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/turbo_workflow/face_zone_settings/tip2_region', *args, **kwargs)

        class graphics_settings(metaclass=PyMenuMeta):
            __doc__ = ''
            def auto_draw(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/preferences/turbo_workflow/graphics_settings/auto_draw', *args, **kwargs)

class size_functions(metaclass=PyMenuMeta):
    __doc__ = 'Manage advanced size functions.'
    def create(self, *args, **kwargs):
        """
        Add size function
        """
        return PyMenu(self.service).execute('/size_functions/create', *args, **kwargs)
    def delete(self, *args, **kwargs):
        """
        Delete Size Functions
        """
        return PyMenu(self.service).execute('/size_functions/delete', *args, **kwargs)
    def delete_all(self, *args, **kwargs):
        """
        Delete All Size Functions
        """
        return PyMenu(self.service).execute('/size_functions/delete_all', *args, **kwargs)
    def compute(self, *args, **kwargs):
        """
        Compute Size-functions
        """
        return PyMenu(self.service).execute('/size_functions/compute', *args, **kwargs)
    def list(self, *args, **kwargs):
        """
        List all Size function parameters.
        """
        return PyMenu(self.service).execute('/size_functions/list', *args, **kwargs)
    def create_defaults(self, *args, **kwargs):
        """
        Creates default curvature & proximty size functions acting on all faces and edges.
        """
        return PyMenu(self.service).execute('/size_functions/create_defaults', *args, **kwargs)
    def set_global_controls(self, *args, **kwargs):
        """
        Set controls for global controls
        """
        return PyMenu(self.service).execute('/size_functions/set_global_controls', *args, **kwargs)
    def enable_periodicity_filter(self, *args, **kwargs):
        """
        Enable size field periodicity
        """
        return PyMenu(self.service).execute('/size_functions/enable_periodicity_filter', *args, **kwargs)
    def disable_periodicity_filter(self, *args, **kwargs):
        """
        Disable size field periodicity
        """
        return PyMenu(self.service).execute('/size_functions/disable_periodicity_filter', *args, **kwargs)
    def list_periodicity_filter(self, *args, **kwargs):
        """
        List periodic in size field
        """
        return PyMenu(self.service).execute('/size_functions/list_periodicity_filter', *args, **kwargs)
    def set_scaling_filter(self, *args, **kwargs):
        """
        Set scaling filter on size field.
        """
        return PyMenu(self.service).execute('/size_functions/set_scaling_filter', *args, **kwargs)
    def reset_global_controls(self, *args, **kwargs):
        """
        Reset controls for global controls
        """
        return PyMenu(self.service).execute('/size_functions/reset_global_controls', *args, **kwargs)
    def set_prox_gap_tolerance(self, *args, **kwargs):
        """
        Set proximity min gap tolerance relative to global min-size
        """
        return PyMenu(self.service).execute('/size_functions/set_prox_gap_tolerance', *args, **kwargs)
    def triangulate_quad_faces(self, *args, **kwargs):
        """
        Replace non-triangular face zones with triangulated face zones during size field computation
        """
        return PyMenu(self.service).execute('/size_functions/triangulate_quad_faces', *args, **kwargs)
    def use_cad_imported_curvature(self, *args, **kwargs):
        """
        Use curvature data imported from CAD
        """
        return PyMenu(self.service).execute('/size_functions/use_cad_imported_curvature', *args, **kwargs)

    class contours(metaclass=PyMenuMeta):
        __doc__ = 'Menu to contour of size field'
        def draw(self, *args, **kwargs):
            """
            Draw size field contour on face zones
            """
            return PyMenu(self.service).execute('/size_functions/contours/draw', *args, **kwargs)

        class set(metaclass=PyMenuMeta):
            __doc__ = 'Set contour options.'
            def refine_facets(self, *args, **kwargs):
                """
                Option to refine facets virtually? for better contour resolution
                """
                return PyMenu(self.service).execute('/size_functions/contours/set/refine_facets', *args, **kwargs)

    class controls(metaclass=PyMenuMeta):
        __doc__ = 'Menu to control different behavior of sf'
        def meshed_sf_behavior(self, *args, **kwargs):
            """
            set meshed size function processing to hard
            """
            return PyMenu(self.service).execute('/size_functions/controls/meshed_sf_behavior', *args, **kwargs)
        def curvature_method(self, *args, **kwargs):
            """
            Option to get facet curvature
            """
            return PyMenu(self.service).execute('/size_functions/controls/curvature_method', *args, **kwargs)

class scoped_sizing(metaclass=PyMenuMeta):
    __doc__ = 'Manage scoped sizing.'
    def create(self, *args, **kwargs):
        """
        Create new scoped sizing
        """
        return PyMenu(self.service).execute('/scoped_sizing/create', *args, **kwargs)
    def modify(self, *args, **kwargs):
        """
        Modify scoped sizing
        """
        return PyMenu(self.service).execute('/scoped_sizing/modify', *args, **kwargs)
    def delete(self, *args, **kwargs):
        """
        Delete scoped sizing
        """
        return PyMenu(self.service).execute('/scoped_sizing/delete', *args, **kwargs)
    def delete_all(self, *args, **kwargs):
        """
        Delete all scoped sizing
        """
        return PyMenu(self.service).execute('/scoped_sizing/delete_all', *args, **kwargs)
    def compute(self, *args, **kwargs):
        """
        Compute scoped sizing/functions
        """
        return PyMenu(self.service).execute('/scoped_sizing/compute', *args, **kwargs)
    def list(self, *args, **kwargs):
        """
        List all scoped sizing  parameters.
        """
        return PyMenu(self.service).execute('/scoped_sizing/list', *args, **kwargs)
    def list_zones_uncovered_by_controls(self, *args, **kwargs):
        """
        List all Zones not covered by scoepd sizing.
        """
        return PyMenu(self.service).execute('/scoped_sizing/list_zones_uncovered_by_controls', *args, **kwargs)
    def delete_size_field(self, *args, **kwargs):
        """
        Reset all the processed sizing functions/scoped sizing.
        """
        return PyMenu(self.service).execute('/scoped_sizing/delete_size_field', *args, **kwargs)
    def read(self, *args, **kwargs):
        """
        Read scoped sizing from a file
        """
        return PyMenu(self.service).execute('/scoped_sizing/read', *args, **kwargs)
    def write(self, *args, **kwargs):
        """
        Write scoped sizing to a file
        """
        return PyMenu(self.service).execute('/scoped_sizing/write', *args, **kwargs)
    def validate(self, *args, **kwargs):
        """
        Validate scoped sizing
        """
        return PyMenu(self.service).execute('/scoped_sizing/validate', *args, **kwargs)

class objects(metaclass=PyMenuMeta):
    __doc__ = 'Manage objects.'
    def create(self, *args, **kwargs):
        """
        create an object with closed face zones.
        """
        return PyMenu(self.service).execute('/objects/create', *args, **kwargs)
    def create_multiple(self, *args, **kwargs):
        """
        create multiple objects one for each face zone passed.
        """
        return PyMenu(self.service).execute('/objects/create_multiple', *args, **kwargs)
    def delete(self, *args, **kwargs):
        """
        delete Objects.
        """
        return PyMenu(self.service).execute('/objects/delete', *args, **kwargs)
    def delete_all(self, *args, **kwargs):
        """
        Delete all objects.
        """
        return PyMenu(self.service).execute('/objects/delete_all', *args, **kwargs)
    def delete_all_geom(self, *args, **kwargs):
        """
        Delete all objects of type geom
        """
        return PyMenu(self.service).execute('/objects/delete_all_geom', *args, **kwargs)
    def merge(self, *args, **kwargs):
        """
        merge volume objects.
        """
        return PyMenu(self.service).execute('/objects/merge', *args, **kwargs)
    def list(self, *args, **kwargs):
        """
        print existing objects.
        """
        return PyMenu(self.service).execute('/objects/list', *args, **kwargs)
    def extract_edges(self, *args, **kwargs):
        """
        extract edges for the Objects
        """
        return PyMenu(self.service).execute('/objects/extract_edges', *args, **kwargs)
    def update(self, *args, **kwargs):
        """
        remove invalid/deleted zones from object's face/edge list
        """
        return PyMenu(self.service).execute('/objects/update', *args, **kwargs)
    def merge_walls(self, *args, **kwargs):
        """
        merge walls of Objects
        """
        return PyMenu(self.service).execute('/objects/merge_walls', *args, **kwargs)
    def merge_edges(self, *args, **kwargs):
        """
        merge edges of Objects
        """
        return PyMenu(self.service).execute('/objects/merge_edges', *args, **kwargs)
    def separate_faces_by_angle(self, *args, **kwargs):
        """
        separate faces of object
        """
        return PyMenu(self.service).execute('/objects/separate_faces_by_angle', *args, **kwargs)
    def separate_faces_by_seed(self, *args, **kwargs):
        """
        separate faces of all object based on given face seed and angle
        """
        return PyMenu(self.service).execute('/objects/separate_faces_by_seed', *args, **kwargs)
    def create_and_activate_domain(self, *args, **kwargs):
        """
        create and activate domain with all face zones of Objects
        """
        return PyMenu(self.service).execute('/objects/create_and_activate_domain', *args, **kwargs)
    def create_groups(self, *args, **kwargs):
        """
        create a face and edge zone group from Objects
        """
        return PyMenu(self.service).execute('/objects/create_groups', *args, **kwargs)
    def delete_unreferenced_faces_and_edges(self, *args, **kwargs):
        """
        delete unreferenced faces and edges
        """
        return PyMenu(self.service).execute('/objects/delete_unreferenced_faces_and_edges', *args, **kwargs)
    def improve_object_quality(self, *args, **kwargs):
        """
        Improve mesh objects quality
        """
        return PyMenu(self.service).execute('/objects/improve_object_quality', *args, **kwargs)
    def merge_voids(self, *args, **kwargs):
        """
        Merge voids/packets
        """
        return PyMenu(self.service).execute('/objects/merge_voids', *args, **kwargs)
    def create_intersection_loops(self, *args, **kwargs):
        """
        Create intersection loops for face zones of objects
        """
        return PyMenu(self.service).execute('/objects/create_intersection_loops', *args, **kwargs)
    def change_object_type(self, *args, **kwargs):
        """
        Change object type
        """
        return PyMenu(self.service).execute('/objects/change_object_type', *args, **kwargs)
    def improve_feature_capture(self, *args, **kwargs):
        """
        Imprint edges of object on to faces of object
        """
        return PyMenu(self.service).execute('/objects/improve_feature_capture', *args, **kwargs)
    def sew(self, *args, **kwargs):
        """
        Enter the sew operation menu.
        """
        return PyMenu(self.service).execute('/objects/sew', *args, **kwargs)
    def merge_nodes(self, *args, **kwargs):
        """
        Merge nodes of an object
        """
        return PyMenu(self.service).execute('/objects/merge_nodes', *args, **kwargs)
    def translate(self, *args, **kwargs):
        """
        Translate objects
        """
        return PyMenu(self.service).execute('/objects/translate', *args, **kwargs)
    def rotate(self, *args, **kwargs):
        """
        Rotate objects
        """
        return PyMenu(self.service).execute('/objects/rotate', *args, **kwargs)
    def scale(self, *args, **kwargs):
        """
        Scale objects
        """
        return PyMenu(self.service).execute('/objects/scale', *args, **kwargs)
    def rename_object_zones(self, *args, **kwargs):
        """
        Rename zones of the objects based on the object name
        """
        return PyMenu(self.service).execute('/objects/rename_object_zones', *args, **kwargs)
    def rename_object(self, *args, **kwargs):
        """
        Rename object name
        """
        return PyMenu(self.service).execute('/objects/rename_object', *args, **kwargs)
    def check_mesh(self, *args, **kwargs):
        """
        Check mesh
        """
        return PyMenu(self.service).execute('/objects/check_mesh', *args, **kwargs)
    def rename_cell_zone_boundaries_using_labels(self, *args, **kwargs):
        """
        Rename cell zone boundaries using the label names
        """
        return PyMenu(self.service).execute('/objects/rename_cell_zone_boundaries_using_labels', *args, **kwargs)
    def summary(self, *args, **kwargs):
        """
        list summary by object name or geom/mesh group
        """
        return PyMenu(self.service).execute('/objects/summary', *args, **kwargs)
    def restore_faces(self, *args, **kwargs):
        """
        Restore object boundaries.
        """
        return PyMenu(self.service).execute('/objects/restore_faces', *args, **kwargs)
    def clear_backup(self, *args, **kwargs):
        """
        Clear backup data of objects.
        """
        return PyMenu(self.service).execute('/objects/clear_backup', *args, **kwargs)
    def change_prefix(self, *args, **kwargs):
        """
        Change the prefix for specified objects
        """
        return PyMenu(self.service).execute('/objects/change_prefix', *args, **kwargs)
    def change_suffix(self, *args, **kwargs):
        """
        Change the suffix for specified objects
        """
        return PyMenu(self.service).execute('/objects/change_suffix', *args, **kwargs)

    class cad_association(metaclass=PyMenuMeta):
        __doc__ = 'Objects association with CAD entities.'
        def attach_cad(self, *args, **kwargs):
            """
            Attach Object association.
            """
            return PyMenu(self.service).execute('/objects/cad_association/attach_cad', *args, **kwargs)
        def update_all_objects(self, *args, **kwargs):
            """
            Update all Objects from CAD association.
            """
            return PyMenu(self.service).execute('/objects/cad_association/update_all_objects', *args, **kwargs)
        def detach_all_objects(self, *args, **kwargs):
            """
            Detach all Objects from CAD association.
            """
            return PyMenu(self.service).execute('/objects/cad_association/detach_all_objects', *args, **kwargs)
        def update_objects(self, *args, **kwargs):
            """
            Update Objects from CAD association.
            """
            return PyMenu(self.service).execute('/objects/cad_association/update_objects', *args, **kwargs)
        def detach_objects(self, *args, **kwargs):
            """
            Detach Objects from CAD association.
            """
            return PyMenu(self.service).execute('/objects/cad_association/detach_objects', *args, **kwargs)
        def query_object_association(self, *args, **kwargs):
            """
            Query Object associations.
            """
            return PyMenu(self.service).execute('/objects/cad_association/query_object_association', *args, **kwargs)
        def unlock_cad(self, *args, **kwargs):
            """
            Unlock Object associations.
            """
            return PyMenu(self.service).execute('/objects/cad_association/unlock_cad', *args, **kwargs)
        def restore_cad(self, *args, **kwargs):
            """
            Restore Object associations.
            """
            return PyMenu(self.service).execute('/objects/cad_association/restore_cad', *args, **kwargs)

    class set(metaclass=PyMenuMeta):
        __doc__ = 'set object parameters'
        def set_edge_feature_angle(self, *args, **kwargs):
            """
            Set edge feature angle for edge extraction
            """
            return PyMenu(self.service).execute('/objects/set/set_edge_feature_angle', *args, **kwargs)
        def show_face_zones(self, *args, **kwargs):
            """
            show object faces on display
            """
            return PyMenu(self.service).execute('/objects/set/show_face_zones', *args, **kwargs)
        def show_edge_zones(self, *args, **kwargs):
            """
            show object edges on display
            """
            return PyMenu(self.service).execute('/objects/set/show_edge_zones', *args, **kwargs)

    class deprecated(metaclass=PyMenuMeta):
        __doc__ = 'deprecated features'
        def create_mesh_object_from_wrap(self, *args, **kwargs):
            """
            Create mesh object from a wrap object
            """
            return PyMenu(self.service).execute('/objects/deprecated/create_mesh_object_from_wrap', *args, **kwargs)

    class wrap(metaclass=PyMenuMeta):
        __doc__ = 'Enter the wrapping operation menu'
        def wrap(self, *args, **kwargs):
            """
            Wrap the object
            """
            return PyMenu(self.service).execute('/objects/wrap/wrap', *args, **kwargs)
        def check_holes(self, *args, **kwargs):
            """
            Check for holes on wrapped objects
            """
            return PyMenu(self.service).execute('/objects/wrap/check_holes', *args, **kwargs)
        def object_zone_separate(self, *args, **kwargs):
            """
            Separate Object Face Zones
            """
            return PyMenu(self.service).execute('/objects/wrap/object_zone_separate', *args, **kwargs)
        def debug(self, *args, **kwargs):
            """
            Debug from intermediate objects
            """
            return PyMenu(self.service).execute('/objects/wrap/debug', *args, **kwargs)

        class set(metaclass=PyMenuMeta):
            __doc__ = 'Set wrap options'
            def use_ray_tracing(self, *args, **kwargs):
                """
                use ray tracing
                """
                return PyMenu(self.service).execute('/objects/wrap/set/use_ray_tracing', *args, **kwargs)
            def delete_far_edges(self, *args, **kwargs):
                """
                delete-far-edges-after-wrap
                """
                return PyMenu(self.service).execute('/objects/wrap/set/delete_far_edges', *args, **kwargs)
            def use_smooth_folded_faces(self, *args, **kwargs):
                """
                use smooth folded faces
                """
                return PyMenu(self.service).execute('/objects/wrap/set/use_smooth_folded_faces', *args, **kwargs)
            def include_thin_cut_edges_and_faces(self, *args, **kwargs):
                """
                Include thin cut Face zones and Edge zones.
                """
                return PyMenu(self.service).execute('/objects/wrap/set/include_thin_cut_edges_and_faces', *args, **kwargs)
            def shrink_wrap_rezone_parameters(self, *args, **kwargs):
                """
                Set wrapper rezone parameters
                """
                return PyMenu(self.service).execute('/objects/wrap/set/shrink_wrap_rezone_parameters', *args, **kwargs)
            def zone_name_prefix(self, *args, **kwargs):
                """
                Prefix to be used for names of wrap face zones created
                """
                return PyMenu(self.service).execute('/objects/wrap/set/zone_name_prefix', *args, **kwargs)
            def relative_feature_tolerance(self, *args, **kwargs):
                """
                Relative Feature Tolerance
                """
                return PyMenu(self.service).execute('/objects/wrap/set/relative_feature_tolerance', *args, **kwargs)
            def minimum_topo_area(self, *args, **kwargs):
                """
                Minimum Topo Area
                """
                return PyMenu(self.service).execute('/objects/wrap/set/minimum_topo_area', *args, **kwargs)
            def minimum_relative_topo_area(self, *args, **kwargs):
                """
                Minimum Relative Topo Area
                """
                return PyMenu(self.service).execute('/objects/wrap/set/minimum_relative_topo_area', *args, **kwargs)
            def minimum_topo_count(self, *args, **kwargs):
                """
                Minimum Topo Face Count
                """
                return PyMenu(self.service).execute('/objects/wrap/set/minimum_topo_count', *args, **kwargs)
            def minimum_relative_topo_count(self, *args, **kwargs):
                """
                Minimum Relative Topo Face Count
                """
                return PyMenu(self.service).execute('/objects/wrap/set/minimum_relative_topo_count', *args, **kwargs)
            def resolution_factor(self, *args, **kwargs):
                """
                Resolution Factor
                """
                return PyMenu(self.service).execute('/objects/wrap/set/resolution_factor', *args, **kwargs)
            def report_holes(self, *args, **kwargs):
                """
                Detect holes in wrapped objects
                """
                return PyMenu(self.service).execute('/objects/wrap/set/report_holes', *args, **kwargs)
            def max_free_edges_for_hole_patching(self, *args, **kwargs):
                """
                Maximum length of free edge loop for filling holes
                """
                return PyMenu(self.service).execute('/objects/wrap/set/max_free_edges_for_hole_patching', *args, **kwargs)
            def add_geometry_recovery_level_to_zones(self, *args, **kwargs):
                """
                Update zones with geometry recovery level attributes
                """
                return PyMenu(self.service).execute('/objects/wrap/set/add_geometry_recovery_level_to_zones', *args, **kwargs)
            def list_zones_geometry_recovery_levels(self, *args, **kwargs):
                """
                List zones with medium and high geometry recovery levels
                """
                return PyMenu(self.service).execute('/objects/wrap/set/list_zones_geometry_recovery_levels', *args, **kwargs)

    class remove_gaps(metaclass=PyMenuMeta):
        __doc__ = 'Enter the gap removal operation menu'
        def remove_gaps(self, *args, **kwargs):
            """
            Remove gaps between objects or remove thickness in objects
            """
            return PyMenu(self.service).execute('/objects/remove_gaps/remove_gaps', *args, **kwargs)
        def show_gaps(self, *args, **kwargs):
            """
            Mark faces at gaps
            """
            return PyMenu(self.service).execute('/objects/remove_gaps/show_gaps', *args, **kwargs)
        def ignore_orientation(self, *args, **kwargs):
            """
            Set if gaps should be identified considering orientation
            """
            return PyMenu(self.service).execute('/objects/remove_gaps/ignore_orientation', *args, **kwargs)

    class join_intersect(metaclass=PyMenuMeta):
        __doc__ = 'join, intersect and build regions in a mesh object'
        def create_mesh_object(self, *args, **kwargs):
            """
            create mesh object from wrap objects
            """
            return PyMenu(self.service).execute('/objects/join_intersect/create_mesh_object', *args, **kwargs)
        def add_objects_to_mesh_object(self, *args, **kwargs):
            """
            add mesh and wrap objects to a mesh object
            """
            return PyMenu(self.service).execute('/objects/join_intersect/add_objects_to_mesh_object', *args, **kwargs)
        def join(self, *args, **kwargs):
            """
            join all face zones in mesh object
            """
            return PyMenu(self.service).execute('/objects/join_intersect/join', *args, **kwargs)
        def intersect(self, *args, **kwargs):
            """
            intersect all face zones in mesh object
            """
            return PyMenu(self.service).execute('/objects/join_intersect/intersect', *args, **kwargs)
        def compute_regions(self, *args, **kwargs):
            """
            Recompute mesh object topo regions
            """
            return PyMenu(self.service).execute('/objects/join_intersect/compute_regions', *args, **kwargs)
        def rename_region(self, *args, **kwargs):
            """
            rename a region in mesh object
            """
            return PyMenu(self.service).execute('/objects/join_intersect/rename_region', *args, **kwargs)
        def delete_region(self, *args, **kwargs):
            """
            delete regions in the object
            """
            return PyMenu(self.service).execute('/objects/join_intersect/delete_region', *args, **kwargs)
        def merge_regions(self, *args, **kwargs):
            """
            merge regions in the object
            """
            return PyMenu(self.service).execute('/objects/join_intersect/merge_regions', *args, **kwargs)
        def change_region_type(self, *args, **kwargs):
            """
            change type of region
            """
            return PyMenu(self.service).execute('/objects/join_intersect/change_region_type', *args, **kwargs)
        def list_regions(self, *args, **kwargs):
            """
            list regions of mesh object
            """
            return PyMenu(self.service).execute('/objects/join_intersect/list_regions', *args, **kwargs)

        class controls(metaclass=PyMenuMeta):
            __doc__ = 'build topology controls'
            def remesh_post_intersection(self, *args, **kwargs):
                """
                Remesh after intersection
                """
                return PyMenu(self.service).execute('/objects/join_intersect/controls/remesh_post_intersection', *args, **kwargs)

    class fix_holes(metaclass=PyMenuMeta):
        __doc__ = 'Fix holes in surface mesh using octree.'
        def find_holes(self, *args, **kwargs):
            """
            Find holes in objects using octree.
            """
            return PyMenu(self.service).execute('/objects/fix_holes/find_holes', *args, **kwargs)
        def reset_material_point(self, *args, **kwargs):
            """
            Reset material point of of region of interest.
            """
            return PyMenu(self.service).execute('/objects/fix_holes/reset_material_point', *args, **kwargs)
        def patch_all_holes(self, *args, **kwargs):
            """
            Patch all wetted holes of the material point.
            """
            return PyMenu(self.service).execute('/objects/fix_holes/patch_all_holes', *args, **kwargs)
        def open_all_holes(self, *args, **kwargs):
            """
            Open all wetted holes of the material point.
            """
            return PyMenu(self.service).execute('/objects/fix_holes/open_all_holes', *args, **kwargs)
        def patch_holes(self, *args, **kwargs):
            """
            Patch holes even not connected by material point.
            """
            return PyMenu(self.service).execute('/objects/fix_holes/patch_holes', *args, **kwargs)
        def open_holes(self, *args, **kwargs):
            """
            Open holes even not connected by material point.
            """
            return PyMenu(self.service).execute('/objects/fix_holes/open_holes', *args, **kwargs)
        def shrink_wrap(self, *args, **kwargs):
            """
            Shrink wrap wetted region of material point.
            """
            return PyMenu(self.service).execute('/objects/fix_holes/shrink_wrap', *args, **kwargs)

        class advanced(metaclass=PyMenuMeta):
            __doc__ = 'Advanced fix holes options.'
            def patch_holes_between_material_points(self, *args, **kwargs):
                """
                Patch holes separating the material points.
                """
                return PyMenu(self.service).execute('/objects/fix_holes/advanced/patch_holes_between_material_points', *args, **kwargs)
            def open_holes_between_material_points(self, *args, **kwargs):
                """
                open holes separating the material points to merge them.
                """
                return PyMenu(self.service).execute('/objects/fix_holes/advanced/open_holes_between_material_points', *args, **kwargs)
            def open_traced_holes_between_material_points(self, *args, **kwargs):
                """
                Trace a path between material points and open holes part of the traced path.
                """
                return PyMenu(self.service).execute('/objects/fix_holes/advanced/open_traced_holes_between_material_points', *args, **kwargs)
            def patch_holes_connected_to_material_points(self, *args, **kwargs):
                """
                Patch all holes wetted by material points.
                """
                return PyMenu(self.service).execute('/objects/fix_holes/advanced/patch_holes_connected_to_material_points', *args, **kwargs)
            def open_holes_connected_to_material_points(self, *args, **kwargs):
                """
                Open all holes wetted by material points.
                """
                return PyMenu(self.service).execute('/objects/fix_holes/advanced/open_holes_connected_to_material_points', *args, **kwargs)
            def patch_holes_not_connected_to_material_points(self, *args, **kwargs):
                """
                Patch all holes other than holes wetted by material points.
                """
                return PyMenu(self.service).execute('/objects/fix_holes/advanced/patch_holes_not_connected_to_material_points', *args, **kwargs)
            def open_holes_not_connected_to_material_points(self, *args, **kwargs):
                """
                Open all holes other than holes wetted by material points.
                """
                return PyMenu(self.service).execute('/objects/fix_holes/advanced/open_holes_not_connected_to_material_points', *args, **kwargs)

    class create_new_mesh_object(metaclass=PyMenuMeta):
        __doc__ = 'Create new mesh objects br wrap or remesh.'
        def wrap(self, *args, **kwargs):
            """
            Wrap objects
            """
            return PyMenu(self.service).execute('/objects/create_new_mesh_object/wrap', *args, **kwargs)
        def remesh(self, *args, **kwargs):
            """
            Remesh objects
            """
            return PyMenu(self.service).execute('/objects/create_new_mesh_object/remesh', *args, **kwargs)

    class labels(metaclass=PyMenuMeta):
        __doc__ = 'Manage Face Zones Labels of an object'
        def create(self, *args, **kwargs):
            """
            Create a new label with face zones
            """
            return PyMenu(self.service).execute('/objects/labels/create', *args, **kwargs)
        def create_label_per_object(self, *args, **kwargs):
            """
            Create label per object
            """
            return PyMenu(self.service).execute('/objects/labels/create_label_per_object', *args, **kwargs)
        def rename(self, *args, **kwargs):
            """
            Rename an existing label of an object
            """
            return PyMenu(self.service).execute('/objects/labels/rename', *args, **kwargs)
        def merge(self, *args, **kwargs):
            """
            Merge multiple labels of an object
            """
            return PyMenu(self.service).execute('/objects/labels/merge', *args, **kwargs)
        def delete(self, *args, **kwargs):
            """
            Delete labels of an object
            """
            return PyMenu(self.service).execute('/objects/labels/delete', *args, **kwargs)
        def add_zones(self, *args, **kwargs):
            """
            Add face zones to existing label
            """
            return PyMenu(self.service).execute('/objects/labels/add_zones', *args, **kwargs)
        def label_unlabeled_zones(self, *args, **kwargs):
            """
            Label unlabeled zones
            """
            return PyMenu(self.service).execute('/objects/labels/label_unlabeled_zones', *args, **kwargs)
        def remove_zones(self, *args, **kwargs):
            """
            Remove face zones from existing label
            """
            return PyMenu(self.service).execute('/objects/labels/remove_zones', *args, **kwargs)
        def remove_all_labels_on_zones(self, *args, **kwargs):
            """
            Clear all labels on selected zones
            """
            return PyMenu(self.service).execute('/objects/labels/remove_all_labels_on_zones', *args, **kwargs)
        def create_label_per_zone(self, *args, **kwargs):
            """
            Create a label for zone with it's name
            """
            return PyMenu(self.service).execute('/objects/labels/create_label_per_zone', *args, **kwargs)

        class cavity(metaclass=PyMenuMeta):
            __doc__ = 'Enter menu to create cavity using labels'
            def replace(self, *args, **kwargs):
                """
                Create cavity by replacing labels from another mesh object.
                """
                return PyMenu(self.service).execute('/objects/labels/cavity/replace', *args, **kwargs)
            def remove(self, *args, **kwargs):
                """
                Create cavity by removing labels.
                """
                return PyMenu(self.service).execute('/objects/labels/cavity/remove', *args, **kwargs)
            def add(self, *args, **kwargs):
                """
                Create cavity by adding labels from another mesh object.
                """
                return PyMenu(self.service).execute('/objects/labels/cavity/add', *args, **kwargs)

    class volumetric_regions(metaclass=PyMenuMeta):
        __doc__ = 'Manage volumetric regions of an object'
        def compute(self, *args, **kwargs):
            """
            Recompute mesh object topo regions using face zone labels
            """
            return PyMenu(self.service).execute('/objects/volumetric_regions/compute', *args, **kwargs)
        def update(self, *args, **kwargs):
            """
            update mesh object topo regions
            """
            return PyMenu(self.service).execute('/objects/volumetric_regions/update', *args, **kwargs)
        def rename(self, *args, **kwargs):
            """
            rename a region in mesh object
            """
            return PyMenu(self.service).execute('/objects/volumetric_regions/rename', *args, **kwargs)
        def delete(self, *args, **kwargs):
            """
            delete regions in the object
            """
            return PyMenu(self.service).execute('/objects/volumetric_regions/delete', *args, **kwargs)
        def merge(self, *args, **kwargs):
            """
            merge regions in the object
            """
            return PyMenu(self.service).execute('/objects/volumetric_regions/merge', *args, **kwargs)
        def change_type(self, *args, **kwargs):
            """
            change type of region
            """
            return PyMenu(self.service).execute('/objects/volumetric_regions/change_type', *args, **kwargs)
        def list(self, *args, **kwargs):
            """
            list regions of mesh object
            """
            return PyMenu(self.service).execute('/objects/volumetric_regions/list', *args, **kwargs)
        def auto_fill_volume(self, *args, **kwargs):
            """
            Auto mesh selected regions
            """
            return PyMenu(self.service).execute('/objects/volumetric_regions/auto_fill_volume', *args, **kwargs)
        def fill_empty_volume(self, *args, **kwargs):
            """
            Fill empty volume of selected regions
            """
            return PyMenu(self.service).execute('/objects/volumetric_regions/fill_empty_volume', *args, **kwargs)
        def merge_cells(self, *args, **kwargs):
            """
            Merge all cell zones assocaited to a region.
            """
            return PyMenu(self.service).execute('/objects/volumetric_regions/merge_cells', *args, **kwargs)
        def delete_cells(self, *args, **kwargs):
            """
            delete all cell zones assocaited to selected regions.
            """
            return PyMenu(self.service).execute('/objects/volumetric_regions/delete_cells', *args, **kwargs)

        class scoped_prism(metaclass=PyMenuMeta):
            __doc__ = 'Enter the scoped prisms menu.'
            def generate(self, *args, **kwargs):
                """
                Grow prism into selected region using scoped prism controls
                """
                return PyMenu(self.service).execute('/objects/volumetric_regions/scoped_prism/generate', *args, **kwargs)

            class set(metaclass=PyMenuMeta):
                __doc__ = 'Enter scoped prism settings.'
                def create(self, *args, **kwargs):
                    """
                    Create new scoped prism
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/scoped_prism/set/create', *args, **kwargs)
                def modify(self, *args, **kwargs):
                    """
                    Modify scoped prisms
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/scoped_prism/set/modify', *args, **kwargs)
                def delete(self, *args, **kwargs):
                    """
                    Delete scoped prisms
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/scoped_prism/set/delete', *args, **kwargs)
                def list(self, *args, **kwargs):
                    """
                    List all scoped prisms parameters.
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/scoped_prism/set/list', *args, **kwargs)
                def read(self, *args, **kwargs):
                    """
                    Read scoped prisms from a file
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/scoped_prism/set/read', *args, **kwargs)
                def set_no_imprint_zones(self, *args, **kwargs):
                    """
                    Set zones which should not be imprinted during prism generation
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/scoped_prism/set/set_no_imprint_zones', *args, **kwargs)
                def write(self, *args, **kwargs):
                    """
                    Write scoped prisms to a file
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/scoped_prism/set/write', *args, **kwargs)
                def growth_options(self, *args, **kwargs):
                    """
                    Set scoped prisms growth options
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/scoped_prism/set/growth_options', *args, **kwargs)
                def set_overset_prism_controls(self, *args, **kwargs):
                    """
                    Set boundary layer controls for overset mesh generation.
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/scoped_prism/set/set_overset_prism_controls', *args, **kwargs)
                def set_advanced_controls(self, *args, **kwargs):
                    """
                    Set scoped boundary layer controls.
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/scoped_prism/set/set_advanced_controls', *args, **kwargs)

        class tet(metaclass=PyMenuMeta):
            __doc__ = 'Enter the tetrahedral menu.'
            def generate(self, *args, **kwargs):
                """
                Fill empty volume of selected regions with tets
                """
                return PyMenu(self.service).execute('/objects/volumetric_regions/tet/generate', *args, **kwargs)

            class set(metaclass=PyMenuMeta):
                __doc__ = 'Enter tet settings'
                def cell_sizing(self, *args, **kwargs):
                    """
                    Allow cell volume distribution to be determined based on boundary.
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/cell_sizing', *args, **kwargs)
                def set_zone_growth_rate(self, *args, **kwargs):
                    """
                    Set zone specific geometric growth rates.
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/set_zone_growth_rate', *args, **kwargs)
                def clear_zone_growth_rate(self, *args, **kwargs):
                    """
                    Clear zone specific geometric growth rates.
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/clear_zone_growth_rate', *args, **kwargs)
                def compute_max_cell_volume(self, *args, **kwargs):
                    """
                    Computes max cell size.
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/compute_max_cell_volume', *args, **kwargs)
                def delete_dead_zones(self, *args, **kwargs):
                    """
                    Automatically delete dead face and cell zones?.
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/delete_dead_zones', *args, **kwargs)
                def max_cell_length(self, *args, **kwargs):
                    """
                    Set max-cell-length.
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/max_cell_length', *args, **kwargs)
                def max_cell_volume(self, *args, **kwargs):
                    """
                    Set max-cell-volume.
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/max_cell_volume', *args, **kwargs)
                def use_max_cell_size(self, *args, **kwargs):
                    """
                    Use max cell size for objects in auto-mesh and do not recompute it based on the object being meshed
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/use_max_cell_size', *args, **kwargs)
                def non_fluid_type(self, *args, **kwargs):
                    """
                    Select the default non-fluid cell zone type.
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/non_fluid_type', *args, **kwargs)
                def refine_method(self, *args, **kwargs):
                    """
                    Define refinement method.
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/refine_method', *args, **kwargs)
                def set_region_based_sizing(self, *args, **kwargs):
                    """
                    Set region based sizings.
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/set_region_based_sizing', *args, **kwargs)
                def print_region_based_sizing(self, *args, **kwargs):
                    """
                    Print region based sizings.
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/print_region_based_sizing', *args, **kwargs)
                def skewness_method(self, *args, **kwargs):
                    """
                    Skewness refinement controls.
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/skewness_method', *args, **kwargs)

                class improve_mesh(metaclass=PyMenuMeta):
                    __doc__ = 'Improve mesh controls.'
                    def improve(self, *args, **kwargs):
                        """
                        Automatically improve mesh.
                        """
                        return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/improve_mesh/improve', *args, **kwargs)
                    def swap(self, *args, **kwargs):
                        """
                        Face swap parameters.
                        """
                        return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/improve_mesh/swap', *args, **kwargs)
                    def skewness_smooth(self, *args, **kwargs):
                        """
                        Skewness smooth parametersx.
                        """
                        return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/improve_mesh/skewness_smooth', *args, **kwargs)
                    def laplace_smooth(self, *args, **kwargs):
                        """
                        Laplace smooth parameters.
                        """
                        return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/improve_mesh/laplace_smooth', *args, **kwargs)

                class adv_front_method(metaclass=PyMenuMeta):
                    __doc__ = 'Advancing front refinement controls.'
                    def refine_parameters(self, *args, **kwargs):
                        """
                        Define refine parameters.
                        """
                        return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/adv_front_method/refine_parameters', *args, **kwargs)
                    def first_improve_params(self, *args, **kwargs):
                        """
                        Define refine front improve parameters.
                        """
                        return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/adv_front_method/first_improve_params', *args, **kwargs)
                    def second_improve_params(self, *args, **kwargs):
                        """
                        Define cell zone improve parameters.
                        """
                        return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/adv_front_method/second_improve_params', *args, **kwargs)

                    class skew_improve(metaclass=PyMenuMeta):
                        __doc__ = 'Refine improve controls.'
                        def boundary_sliver_skew(self, *args, **kwargs):
                            """
                            Refine improve boundary sliver skew.
                            """
                            return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/adv_front_method/skew_improve/boundary_sliver_skew', *args, **kwargs)
                        def sliver_skew(self, *args, **kwargs):
                            """
                            Refine improve sliver skew.
                            """
                            return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/adv_front_method/skew_improve/sliver_skew', *args, **kwargs)
                        def target(self, *args, **kwargs):
                            """
                            Activate target skew refinement.
                            """
                            return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/adv_front_method/skew_improve/target', *args, **kwargs)
                        def target_skew(self, *args, **kwargs):
                            """
                            Refine improve target skew.
                            """
                            return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/adv_front_method/skew_improve/target_skew', *args, **kwargs)
                        def target_low_skew(self, *args, **kwargs):
                            """
                            Refine improve target low skew.
                            """
                            return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/adv_front_method/skew_improve/target_low_skew', *args, **kwargs)
                        def attempts(self, *args, **kwargs):
                            """
                            Refine improve attempts.
                            """
                            return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/adv_front_method/skew_improve/attempts', *args, **kwargs)
                        def iterations(self, *args, **kwargs):
                            """
                            Refine improve iterations.
                            """
                            return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/adv_front_method/skew_improve/iterations', *args, **kwargs)

                class remove_slivers(metaclass=PyMenuMeta):
                    __doc__ = 'Sliver remove controls.'
                    def remove(self, *args, **kwargs):
                        """
                        Automatically remove slivers.
                        """
                        return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/remove_slivers/remove', *args, **kwargs)
                    def skew(self, *args, **kwargs):
                        """
                        Remove sliver skew.
                        """
                        return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/remove_slivers/skew', *args, **kwargs)
                    def low_skew(self, *args, **kwargs):
                        """
                        Remove sliver low skew.
                        """
                        return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/remove_slivers/low_skew', *args, **kwargs)
                    def angle(self, *args, **kwargs):
                        """
                        Max dihedral angle defining a valid boundary sliver.
                        """
                        return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/remove_slivers/angle', *args, **kwargs)
                    def attempts(self, *args, **kwargs):
                        """
                        Sliver remove attempts.
                        """
                        return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/remove_slivers/attempts', *args, **kwargs)
                    def iterations(self, *args, **kwargs):
                        """
                        Sliver remove iterations.
                        """
                        return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/remove_slivers/iterations', *args, **kwargs)
                    def method(self, *args, **kwargs):
                        """
                        Sliver remove method.
                        """
                        return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/remove_slivers/method', *args, **kwargs)

                class tet_improve(metaclass=PyMenuMeta):
                    __doc__ = 'Improve cells controls.'
                    def skew(self, *args, **kwargs):
                        """
                        Remove skew.
                        """
                        return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/tet_improve/skew', *args, **kwargs)
                    def angle(self, *args, **kwargs):
                        """
                        Max dihedral angle defining a valid boundary cell.
                        """
                        return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/tet_improve/angle', *args, **kwargs)
                    def attempts(self, *args, **kwargs):
                        """
                        Improve attempts.
                        """
                        return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/tet_improve/attempts', *args, **kwargs)
                    def iterations(self, *args, **kwargs):
                        """
                        Improve iterations.
                        """
                        return PyMenu(self.service).execute('/objects/volumetric_regions/tet/set/tet_improve/iterations', *args, **kwargs)

        class hexcore(metaclass=PyMenuMeta):
            __doc__ = 'Enter the hexcore menu.'
            def generate(self, *args, **kwargs):
                """
                Fill empty volume of selected regions with hexcore
                """
                return PyMenu(self.service).execute('/objects/volumetric_regions/hexcore/generate', *args, **kwargs)

            class set(metaclass=PyMenuMeta):
                __doc__ = 'Enter hexcore settings'
                def define_hexcore_extents(self, *args, **kwargs):
                    """
                    Enables sspecificaton of hexcore outer domain parameters
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/hexcore/set/define_hexcore_extents', *args, **kwargs)
                def buffer_layers(self, *args, **kwargs):
                    """
                    Number of addition cells to mark for subdivision.
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/hexcore/set/buffer_layers', *args, **kwargs)
                def delete_dead_zones(self, *args, **kwargs):
                    """
                    Delete dead zones after hexcore creation.
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/hexcore/set/delete_dead_zones', *args, **kwargs)
                def maximum_cell_length(self, *args, **kwargs):
                    """
                    Maximum cell length
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/hexcore/set/maximum_cell_length', *args, **kwargs)
                def compute_max_cell_length(self, *args, **kwargs):
                    """
                    Compute maximum cell length
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/hexcore/set/compute_max_cell_length', *args, **kwargs)
                def maximum_initial_cells(self, *args, **kwargs):
                    """
                    Maximum number of initial Cartesian cells.
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/hexcore/set/maximum_initial_cells', *args, **kwargs)
                def non_fluid_type(self, *args, **kwargs):
                    """
                    Set non fluid type for cell zones.
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/hexcore/set/non_fluid_type', *args, **kwargs)
                def peel_layers(self, *args, **kwargs):
                    """
                    Number of hexcore cells to peel back from boundary.
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/hexcore/set/peel_layers', *args, **kwargs)
                def skip_tet_refinement(self, *args, **kwargs):
                    """
                    Skip tethedral refinement in transition cell generation.
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/hexcore/set/skip_tet_refinement', *args, **kwargs)
                def merge_tets_to_pyramids(self, *args, **kwargs):
                    """
                    Merge tets into pyramids.
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/hexcore/set/merge_tets_to_pyramids', *args, **kwargs)
                def octree_hexcore(self, *args, **kwargs):
                    """
                    Create hexcore using size-function driven octree
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/hexcore/set/octree_hexcore', *args, **kwargs)
                def avoid_1_by_8_cell_jump_in_hexcore(self, *args, **kwargs):
                    """
                    avoid-1:8-cell-jump-in-hexcore
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/hexcore/set/avoid_1_by_8_cell_jump_in_hexcore', *args, **kwargs)
                def set_region_based_sizing(self, *args, **kwargs):
                    """
                    Set region based sizings.
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/hexcore/set/set_region_based_sizing', *args, **kwargs)
                def print_region_based_sizing(self, *args, **kwargs):
                    """
                    Print region based sizings.
                    """
                    return PyMenu(self.service).execute('/objects/volumetric_regions/hexcore/set/print_region_based_sizing', *args, **kwargs)

                class outer_domain_params(metaclass=PyMenuMeta):
                    __doc__ = 'Define outer domain parameters'
                    def specify_coordinates(self, *args, **kwargs):
                        """
                        Enables specification of coordinates of hexcore outer box
                        """
                        return PyMenu(self.service).execute('/objects/volumetric_regions/hexcore/set/outer_domain_params/specify_coordinates', *args, **kwargs)
                    def coordinates(self, *args, **kwargs):
                        """
                        Secifiy coordinates of outer box
                        """
                        return PyMenu(self.service).execute('/objects/volumetric_regions/hexcore/set/outer_domain_params/coordinates', *args, **kwargs)
                    def specify_boundaries(self, *args, **kwargs):
                        """
                        Set parameters to get hex mesh to boundary(s)
                        """
                        return PyMenu(self.service).execute('/objects/volumetric_regions/hexcore/set/outer_domain_params/specify_boundaries', *args, **kwargs)
                    def boundaries(self, *args, **kwargs):
                        """
                        Set box-aligned zones which  have to be removed from hexcore meshing
                        """
                        return PyMenu(self.service).execute('/objects/volumetric_regions/hexcore/set/outer_domain_params/boundaries', *args, **kwargs)
                    def auto_align(self, *args, **kwargs):
                        """
                        Enable auto-align?
                        """
                        return PyMenu(self.service).execute('/objects/volumetric_regions/hexcore/set/outer_domain_params/auto_align', *args, **kwargs)
                    def auto_align_tolerance(self, *args, **kwargs):
                        """
                        Set auto-align-tolerance
                        """
                        return PyMenu(self.service).execute('/objects/volumetric_regions/hexcore/set/outer_domain_params/auto_align_tolerance', *args, **kwargs)
                    def auto_align_boundaries(self, *args, **kwargs):
                        """
                        auto-align selected boundaries
                        """
                        return PyMenu(self.service).execute('/objects/volumetric_regions/hexcore/set/outer_domain_params/auto_align_boundaries', *args, **kwargs)
                    def delete_old_face_zones(self, *args, **kwargs):
                        """
                        Delete replaced old tri face zones
                        """
                        return PyMenu(self.service).execute('/objects/volumetric_regions/hexcore/set/outer_domain_params/delete_old_face_zones', *args, **kwargs)
                    def list(self, *args, **kwargs):
                        """
                        List the face zones selected for hexcore up to boundaries
                        """
                        return PyMenu(self.service).execute('/objects/volumetric_regions/hexcore/set/outer_domain_params/list', *args, **kwargs)

class diagnostics(metaclass=PyMenuMeta):
    __doc__ = 'Diagnostic tools.'
    def set_scope(self, *args, **kwargs):
        """
        ti-diagnose-set-scope
        """
        return PyMenu(self.service).execute('/diagnostics/set_scope', *args, **kwargs)
    def auto_check(self, *args, **kwargs):
        """
        Performs all necessary checks...
        """
        return PyMenu(self.service).execute('/diagnostics/auto_check', *args, **kwargs)

    class face_connectivity(metaclass=PyMenuMeta):
        __doc__ = 'diagnose-face-connectivity'
        def fix_free_faces(self, *args, **kwargs):
            """
            Fix free faces using
            merge-nodes - Individually on each object or on given face zone list
            stitch - Individually on each object or on given face zone list
            delete-free-edge-faces - Of given face zone list or all face zones of given objects
            delete-fringes - Of given face zone list or all face zones of given objects
            delete-skewed-faces - Of given face zone list or all face zones of given objects
            """
            return PyMenu(self.service).execute('/diagnostics/face_connectivity/fix_free_faces', *args, **kwargs)
        def fix_multi_faces(self, *args, **kwargs):
            """
            Fix milti faces using
            delete-fringes - Of given face zone list or all face zones of given objects
            delete-overlaps - Of given face zone list or all face zones of given objects
            disconnect - Given face zone list or all face zones of given objects
            all-above - on given face zone list or all face zones of given objects
            """
            return PyMenu(self.service).execute('/diagnostics/face_connectivity/fix_multi_faces', *args, **kwargs)
        def fix_self_intersections(self, *args, **kwargs):
            """
            Fix self intersections
            fix-self-intersections - Of given face zone list or all face zones of given objects
            fix-folded-faces - Smooth folded faces of given face zone list or all face zones of given objects
            """
            return PyMenu(self.service).execute('/diagnostics/face_connectivity/fix_self_intersections', *args, **kwargs)
        def fix_duplicate_faces(self, *args, **kwargs):
            """
            Fix duplicate faces
            by deleting duplicate faces of given face zone list or all face zones of given objects
            """
            return PyMenu(self.service).execute('/diagnostics/face_connectivity/fix_duplicate_faces', *args, **kwargs)
        def fix_spikes(self, *args, **kwargs):
            """
            Fix spikes
            by smoothing spikes from given face zone list or all face zones of given objects
            """
            return PyMenu(self.service).execute('/diagnostics/face_connectivity/fix_spikes', *args, **kwargs)
        def fix_islands(self, *args, **kwargs):
            """
            Fix spikes
            by removing islands from given face zone list or all face zones of given objects
            """
            return PyMenu(self.service).execute('/diagnostics/face_connectivity/fix_islands', *args, **kwargs)
        def fix_steps(self, *args, **kwargs):
            """
            Fix steps
            smooth - Steps from given face zone list or all face zones of given objects
            collapse - Steps from given face zone list or all face zones of given objects
            """
            return PyMenu(self.service).execute('/diagnostics/face_connectivity/fix_steps', *args, **kwargs)
        def fix_slivers(self, *args, **kwargs):
            """
            Fix Slivers
            by collapsing slivers from given face zone list or all face zones of given objects
            """
            return PyMenu(self.service).execute('/diagnostics/face_connectivity/fix_slivers', *args, **kwargs)
        def fix_deviations(self, *args, **kwargs):
            """
            Fix deviations
            by imprinting edges for given set of face and edge zones or zones of each object individually.
            """
            return PyMenu(self.service).execute('/diagnostics/face_connectivity/fix_deviations', *args, **kwargs)
        def fix_point_contacts(self, *args, **kwargs):
            """
            Fix point contacts
            by removing point contacts from given face zone list or all face zones of given objects
            """
            return PyMenu(self.service).execute('/diagnostics/face_connectivity/fix_point_contacts', *args, **kwargs)
        def fix_invalid_normals(self, *args, **kwargs):
            """
            Fix invalid normals
            by smoothing invalid normals from given face zone list or all face zones of given objects
            """
            return PyMenu(self.service).execute('/diagnostics/face_connectivity/fix_invalid_normals', *args, **kwargs)
        def add_label_to_small_neighbors(self, *args, **kwargs):
            """
            Change small connected islands label to input.
            """
            return PyMenu(self.service).execute('/diagnostics/face_connectivity/add_label_to_small_neighbors', *args, **kwargs)
        def remove_label_from_small_islands(self, *args, **kwargs):
            """
            Change small disconnected island labels to their connected neighbors
            """
            return PyMenu(self.service).execute('/diagnostics/face_connectivity/remove_label_from_small_islands', *args, **kwargs)

    class quality(metaclass=PyMenuMeta):
        __doc__ = 'diagnose-face-quality'
        def general_improve(self, *args, **kwargs):
            """
            General Improve
            on  given face zone list or all face zones of given objects
            """
            return PyMenu(self.service).execute('/diagnostics/quality/general_improve', *args, **kwargs)
        def smooth(self, *args, **kwargs):
            """
            Smooth individually on each object or on given face zone list
            """
            return PyMenu(self.service).execute('/diagnostics/quality/smooth', *args, **kwargs)
        def collapse(self, *args, **kwargs):
            """
            collapse faces from given face zone list or all face zones of given objects
            """
            return PyMenu(self.service).execute('/diagnostics/quality/collapse', *args, **kwargs)
        def delaunay_swap(self, *args, **kwargs):
            """
            delaunay swap the faces given face zone list or all face zones of given objects
            """
            return PyMenu(self.service).execute('/diagnostics/quality/delaunay_swap', *args, **kwargs)

class material_point(metaclass=PyMenuMeta):
    __doc__ = 'Manage material points'
    def create_material_point(self, *args, **kwargs):
        """
        Add a material point
        """
        return PyMenu(self.service).execute('/material_point/create_material_point', *args, **kwargs)
    def delete_material_point(self, *args, **kwargs):
        """
        Delete a material point
        """
        return PyMenu(self.service).execute('/material_point/delete_material_point', *args, **kwargs)
    def delete_all_material_points(self, *args, **kwargs):
        """
        Delete all material points
        """
        return PyMenu(self.service).execute('/material_point/delete_all_material_points', *args, **kwargs)
    def list_material_points(self, *args, **kwargs):
        """
        List material points
        """
        return PyMenu(self.service).execute('/material_point/list_material_points', *args, **kwargs)

class mesh(metaclass=PyMenuMeta):
    __doc__ = 'Enter the grid menu'
    def activate_lean_datastructures(self, *args, **kwargs):
        """
        Activates Lean data structures to reduce memory
        """
        return PyMenu(self.service).execute('/mesh/activate_lean_datastructures', *args, **kwargs)
    def deactivate_lean_datastructures(self, *args, **kwargs):
        """
        Deactivates Lean data structures
        """
        return PyMenu(self.service).execute('/mesh/deactivate_lean_datastructures', *args, **kwargs)
    def auto_mesh(self, *args, **kwargs):
        """
        Automatically executes initialization and refinement of mesh.
        """
        return PyMenu(self.service).execute('/mesh/auto_mesh', *args, **kwargs)
    def auto_mesh_multiple_objects(self, *args, **kwargs):
        """
        Automatically executes initialization and refinement of mesh for multiple objects.
        """
        return PyMenu(self.service).execute('/mesh/auto_mesh_multiple_objects', *args, **kwargs)
    def check_mesh(self, *args, **kwargs):
        """
        Check mesh for topological errors.
        """
        return PyMenu(self.service).execute('/mesh/check_mesh', *args, **kwargs)
    def selective_mesh_check(self, *args, **kwargs):
        """
        Selective mesh check.
        """
        return PyMenu(self.service).execute('/mesh/selective_mesh_check', *args, **kwargs)
    def check_quality(self, *args, **kwargs):
        """
        Check mesh quality.
        """
        return PyMenu(self.service).execute('/mesh/check_quality', *args, **kwargs)
    def check_quality_level(self, *args, **kwargs):
        """
        Check mesh quality level.
        """
        return PyMenu(self.service).execute('/mesh/check_quality_level', *args, **kwargs)
    def clear_mesh(self, *args, **kwargs):
        """
        Clear internal mesh, leaving boundary faces.
        """
        return PyMenu(self.service).execute('/mesh/clear_mesh', *args, **kwargs)
    def clear_undo_stack(self, *args, **kwargs):
        """
        Clears undo stack.
        """
        return PyMenu(self.service).execute('/mesh/clear_undo_stack', *args, **kwargs)
    def create_heat_exchanger(self, *args, **kwargs):
        """
        Create heat exchanger zones using four points and 3 intervals.
        """
        return PyMenu(self.service).execute('/mesh/create_heat_exchanger', *args, **kwargs)
    def create_frustrum(self, *args, **kwargs):
        """
        Create a cylindrical hex mesh
        """
        return PyMenu(self.service).execute('/mesh/create_frustrum', *args, **kwargs)
    def list_mesh_parameter(self, *args, **kwargs):
        """
        Show all mesh parameters.
        """
        return PyMenu(self.service).execute('/mesh/list_mesh_parameter', *args, **kwargs)
    def repair_face_handedness(self, *args, **kwargs):
        """
        Reverse face node orientation.
        """
        return PyMenu(self.service).execute('/mesh/repair_face_handedness', *args, **kwargs)
    def laplace_smooth_nodes(self, *args, **kwargs):
        """
        Laplace smooth nodes.
        """
        return PyMenu(self.service).execute('/mesh/laplace_smooth_nodes', *args, **kwargs)
    def reset_mesh(self, *args, **kwargs):
        """
        Clear entire mesh.
        """
        return PyMenu(self.service).execute('/mesh/reset_mesh', *args, **kwargs)
    def reset_mesh_parameter(self, *args, **kwargs):
        """
        Reset all parameters to their default values.
        """
        return PyMenu(self.service).execute('/mesh/reset_mesh_parameter', *args, **kwargs)
    def auto_prefix_cell_zones(self, *args, **kwargs):
        """
        Prefix cell zones with user defined name.
        """
        return PyMenu(self.service).execute('/mesh/auto_prefix_cell_zones', *args, **kwargs)
    def cutcell(self, *args, **kwargs):
        """
        Enter the CutCell meshing menu.
        """
        return PyMenu(self.service).execute('/mesh/cutcell', *args, **kwargs)
    def prepare_for_solve(self, *args, **kwargs):
        """
        Performs the following cleanup operations:
            -Delete dead zones
            -Delete geom and wrap objects
            -Delete all edge zones
            -Delete unused faces
            -Delete unused nodes
        """
        return PyMenu(self.service).execute('/mesh/prepare_for_solve', *args, **kwargs)
    def zone_names_clean_up(self, *args, **kwargs):
        """
        Cleanup face and cell zone names
        """
        return PyMenu(self.service).execute('/mesh/zone_names_clean_up', *args, **kwargs)

    class cartesian(metaclass=PyMenuMeta):
        __doc__ = 'Enter Cartesian mesh menu.'
        def mesh(self, *args, **kwargs):
            """
            Generate Cartesian mesh
            """
            return PyMenu(self.service).execute('/mesh/cartesian/mesh', *args, **kwargs)

    class cavity(metaclass=PyMenuMeta):
        __doc__ = 'Enter cavity menu.'
        def replace_zones(self, *args, **kwargs):
            """
            Create a cavity for remeshing.
            """
            return PyMenu(self.service).execute('/mesh/cavity/replace_zones', *args, **kwargs)
        def add_zones(self, *args, **kwargs):
            """
            Create a cavity for remeshing.
            """
            return PyMenu(self.service).execute('/mesh/cavity/add_zones', *args, **kwargs)
        def remove_zones(self, *args, **kwargs):
            """
            Create a cavity for remeshing.
            """
            return PyMenu(self.service).execute('/mesh/cavity/remove_zones', *args, **kwargs)
        def region(self, *args, **kwargs):
            """
            Create a cavity for remeshing.
            """
            return PyMenu(self.service).execute('/mesh/cavity/region', *args, **kwargs)
        def merge_cavity(self, *args, **kwargs):
            """
            Merge a cavity domain with a domain.
            """
            return PyMenu(self.service).execute('/mesh/cavity/merge_cavity', *args, **kwargs)
        def create_hexcore_cavity_by_region(self, *args, **kwargs):
            """
            Create a cavity in hexcore mesh for remeshing.
            """
            return PyMenu(self.service).execute('/mesh/cavity/create_hexcore_cavity_by_region', *args, **kwargs)
        def create_hexcore_cavity_by_scale(self, *args, **kwargs):
            """
            Create a cavity in hexcore mesh for remeshing by scale.
            """
            return PyMenu(self.service).execute('/mesh/cavity/create_hexcore_cavity_by_scale', *args, **kwargs)
        def remesh_hexcore_cavity(self, *args, **kwargs):
            """
            Remesh a cavity in hexcore mesh.
            """
            return PyMenu(self.service).execute('/mesh/cavity/remesh_hexcore_cavity', *args, **kwargs)

    class domains(metaclass=PyMenuMeta):
        __doc__ = 'Enter domains menu.'
        def activate(self, *args, **kwargs):
            """
            Activate the domain for subsequent meshing operations.
            """
            return PyMenu(self.service).execute('/mesh/domains/activate', *args, **kwargs)
        def create_by_cell_zone(self, *args, **kwargs):
            """
            Create new domain using cell zones.
            """
            return PyMenu(self.service).execute('/mesh/domains/create_by_cell_zone', *args, **kwargs)
        def create_by_point(self, *args, **kwargs):
            """
            Create new domain using material point.
            """
            return PyMenu(self.service).execute('/mesh/domains/create_by_point', *args, **kwargs)
        def draw(self, *args, **kwargs):
            """
            Draw the boundary face zones of the domain.
            """
            return PyMenu(self.service).execute('/mesh/domains/draw', *args, **kwargs)
        def create(self, *args, **kwargs):
            """
            Create a new domain by specifying the boundary face zones.
            """
            return PyMenu(self.service).execute('/mesh/domains/create', *args, **kwargs)
        def delete(self, *args, **kwargs):
            """
            Delete the specified domain.
            """
            return PyMenu(self.service).execute('/mesh/domains/delete', *args, **kwargs)
        def print(self, *args, **kwargs):
            """
            Print domain content.
            """
            return PyMenu(self.service).execute('/mesh/domains/print', *args, **kwargs)

    class hexcore(metaclass=PyMenuMeta):
        __doc__ = 'Enter the hexcore menu.'
        def create(self, *args, **kwargs):
            """
            Create hexcore mesh from boundary zone list.
            """
            return PyMenu(self.service).execute('/mesh/hexcore/create', *args, **kwargs)
        def merge_tets_to_pyramids(self, *args, **kwargs):
            """
            Merge tets into pyramids.
            """
            return PyMenu(self.service).execute('/mesh/hexcore/merge_tets_to_pyramids', *args, **kwargs)

        class controls(metaclass=PyMenuMeta):
            __doc__ = 'Enter hexcore controls menu'
            def define_hexcore_extents(self, *args, **kwargs):
                """
                Enables sspecificaton of hexcore outer domain parameters
                """
                return PyMenu(self.service).execute('/mesh/hexcore/controls/define_hexcore_extents', *args, **kwargs)
            def buffer_layers(self, *args, **kwargs):
                """
                Number of addition cells to mark for subdivision.
                """
                return PyMenu(self.service).execute('/mesh/hexcore/controls/buffer_layers', *args, **kwargs)
            def delete_dead_zones(self, *args, **kwargs):
                """
                Delete dead zones after hexcore creation.
                """
                return PyMenu(self.service).execute('/mesh/hexcore/controls/delete_dead_zones', *args, **kwargs)
            def maximum_cell_length(self, *args, **kwargs):
                """
                Maximum cell length
                """
                return PyMenu(self.service).execute('/mesh/hexcore/controls/maximum_cell_length', *args, **kwargs)
            def compute_max_cell_length(self, *args, **kwargs):
                """
                Compute maximum cell length
                """
                return PyMenu(self.service).execute('/mesh/hexcore/controls/compute_max_cell_length', *args, **kwargs)
            def maximum_initial_cells(self, *args, **kwargs):
                """
                Maximum number of initial Cartesian cells.
                """
                return PyMenu(self.service).execute('/mesh/hexcore/controls/maximum_initial_cells', *args, **kwargs)
            def non_fluid_type(self, *args, **kwargs):
                """
                Set non fluid type for cell zones.
                """
                return PyMenu(self.service).execute('/mesh/hexcore/controls/non_fluid_type', *args, **kwargs)
            def peel_layers(self, *args, **kwargs):
                """
                Number of hexcore cells to peel back from boundary.
                """
                return PyMenu(self.service).execute('/mesh/hexcore/controls/peel_layers', *args, **kwargs)
            def skip_tet_refinement(self, *args, **kwargs):
                """
                Skip tethedral refinement in transition cell generation.
                """
                return PyMenu(self.service).execute('/mesh/hexcore/controls/skip_tet_refinement', *args, **kwargs)
            def merge_tets_to_pyramids(self, *args, **kwargs):
                """
                Merge tets into pyramids.
                """
                return PyMenu(self.service).execute('/mesh/hexcore/controls/merge_tets_to_pyramids', *args, **kwargs)
            def octree_hexcore(self, *args, **kwargs):
                """
                Create hexcore using size-function driven octree
                """
                return PyMenu(self.service).execute('/mesh/hexcore/controls/octree_hexcore', *args, **kwargs)
            def avoid_1_by_8_cell_jump_in_hexcore(self, *args, **kwargs):
                """
                avoid-1:8-cell-jump-in-hexcore
                """
                return PyMenu(self.service).execute('/mesh/hexcore/controls/avoid_1_by_8_cell_jump_in_hexcore', *args, **kwargs)
            def set_region_based_sizing(self, *args, **kwargs):
                """
                Set region based sizings.
                """
                return PyMenu(self.service).execute('/mesh/hexcore/controls/set_region_based_sizing', *args, **kwargs)
            def print_region_based_sizing(self, *args, **kwargs):
                """
                Print region based sizings.
                """
                return PyMenu(self.service).execute('/mesh/hexcore/controls/print_region_based_sizing', *args, **kwargs)

            class outer_domain_params(metaclass=PyMenuMeta):
                __doc__ = 'Define outer domain parameters'
                def specify_coordinates(self, *args, **kwargs):
                    """
                    Enables specification of coordinates of hexcore outer box
                    """
                    return PyMenu(self.service).execute('/mesh/hexcore/controls/outer_domain_params/specify_coordinates', *args, **kwargs)
                def coordinates(self, *args, **kwargs):
                    """
                    Secifiy coordinates of outer box
                    """
                    return PyMenu(self.service).execute('/mesh/hexcore/controls/outer_domain_params/coordinates', *args, **kwargs)
                def specify_boundaries(self, *args, **kwargs):
                    """
                    Set parameters to get hex mesh to boundary(s)
                    """
                    return PyMenu(self.service).execute('/mesh/hexcore/controls/outer_domain_params/specify_boundaries', *args, **kwargs)
                def boundaries(self, *args, **kwargs):
                    """
                    Set box-aligned zones which  have to be removed from hexcore meshing
                    """
                    return PyMenu(self.service).execute('/mesh/hexcore/controls/outer_domain_params/boundaries', *args, **kwargs)
                def auto_align(self, *args, **kwargs):
                    """
                    Enable auto-align?
                    """
                    return PyMenu(self.service).execute('/mesh/hexcore/controls/outer_domain_params/auto_align', *args, **kwargs)
                def auto_align_tolerance(self, *args, **kwargs):
                    """
                    Set auto-align-tolerance
                    """
                    return PyMenu(self.service).execute('/mesh/hexcore/controls/outer_domain_params/auto_align_tolerance', *args, **kwargs)
                def auto_align_boundaries(self, *args, **kwargs):
                    """
                    auto-align selected boundaries
                    """
                    return PyMenu(self.service).execute('/mesh/hexcore/controls/outer_domain_params/auto_align_boundaries', *args, **kwargs)
                def delete_old_face_zones(self, *args, **kwargs):
                    """
                    Delete replaced old tri face zones
                    """
                    return PyMenu(self.service).execute('/mesh/hexcore/controls/outer_domain_params/delete_old_face_zones', *args, **kwargs)
                def list(self, *args, **kwargs):
                    """
                    List the face zones selected for hexcore up to boundaries
                    """
                    return PyMenu(self.service).execute('/mesh/hexcore/controls/outer_domain_params/list', *args, **kwargs)

        class local_regions(metaclass=PyMenuMeta):
            __doc__ = 'Enter the hexcore refine-local menu'
            def activate(self, *args, **kwargs):
                """
                Activate regions for hexcore refinement
                """
                return PyMenu(self.service).execute('/mesh/hexcore/local_regions/activate', *args, **kwargs)
            def deactivate(self, *args, **kwargs):
                """
                Activate regions for hexcore refinement
                """
                return PyMenu(self.service).execute('/mesh/hexcore/local_regions/deactivate', *args, **kwargs)
            def define(self, *args, **kwargs):
                """
                Define a refinement region's parameters.
                """
                return PyMenu(self.service).execute('/mesh/hexcore/local_regions/define', *args, **kwargs)
            def delete(self, *args, **kwargs):
                """
                Delete a refinement region.
                """
                return PyMenu(self.service).execute('/mesh/hexcore/local_regions/delete', *args, **kwargs)
            def init(self, *args, **kwargs):
                """
                Delete all current regions and add the default refinement region.
                """
                return PyMenu(self.service).execute('/mesh/hexcore/local_regions/init', *args, **kwargs)
            def list_all_regions(self, *args, **kwargs):
                """
                List all refinement regions.
                """
                return PyMenu(self.service).execute('/mesh/hexcore/local_regions/list_all_regions', *args, **kwargs)
            def ideal_hex_vol(self, *args, **kwargs):
                """
                Ideal hex volume for given edge length.
                """
                return PyMenu(self.service).execute('/mesh/hexcore/local_regions/ideal_hex_vol', *args, **kwargs)
            def ideal_quad_area(self, *args, **kwargs):
                """
                Ideal quad area for given edge length.
                """
                return PyMenu(self.service).execute('/mesh/hexcore/local_regions/ideal_quad_area', *args, **kwargs)

    class modify(metaclass=PyMenuMeta):
        __doc__ = 'Enter the mesh modify menu'
        def clear_selections(self, *args, **kwargs):
            """
            Clear all selections.
            """
            return PyMenu(self.service).execute('/mesh/modify/clear_selections', *args, **kwargs)
        def extract_unused_nodes(self, *args, **kwargs):
            """
            Extract all unused nodes into a separate interior node zone.
            """
            return PyMenu(self.service).execute('/mesh/modify/extract_unused_nodes', *args, **kwargs)
        def smooth_node(self, *args, **kwargs):
            """
            Laplace smooth nodes in probe list.
            """
            return PyMenu(self.service).execute('/mesh/modify/smooth_node', *args, **kwargs)
        def list_selections(self, *args, **kwargs):
            """
            List selections.
            """
            return PyMenu(self.service).execute('/mesh/modify/list_selections', *args, **kwargs)
        def list_skewed_cells(self, *args, **kwargs):
            """
            List cells between skewness limits.
            """
            return PyMenu(self.service).execute('/mesh/modify/list_skewed_cells', *args, **kwargs)
        def mesh_node(self, *args, **kwargs):
            """
            Introduce new node into existing mesh.
            """
            return PyMenu(self.service).execute('/mesh/modify/mesh_node', *args, **kwargs)
        def mesh_nodes_on_zone(self, *args, **kwargs):
            """
            Insert nodes associated with node or face thread into volume mesh.  If a face thread is specified, the faces are deleted before the nodes are introduced into the mesh.
            """
            return PyMenu(self.service).execute('/mesh/modify/mesh_nodes_on_zone', *args, **kwargs)
        def neighborhood_skew(self, *args, **kwargs):
            """
            Report max skew of all cells using node.
            """
            return PyMenu(self.service).execute('/mesh/modify/neighborhood_skew', *args, **kwargs)
        def refine_cell(self, *args, **kwargs):
            """
            Refine cells in probe list with node near centroid.
            """
            return PyMenu(self.service).execute('/mesh/modify/refine_cell', *args, **kwargs)
        def deselect_last(self, *args, **kwargs):
            """
            Deselect last selection.
            """
            return PyMenu(self.service).execute('/mesh/modify/deselect_last', *args, **kwargs)
        def select_entity(self, *args, **kwargs):
            """
            Select a entity.
            """
            return PyMenu(self.service).execute('/mesh/modify/select_entity', *args, **kwargs)
        def auto_node_move(self, *args, **kwargs):
            """
            Improve the quality of the mesh by node movement
            """
            return PyMenu(self.service).execute('/mesh/modify/auto_node_move', *args, **kwargs)
        def repair_negative_volume_cells(self, *args, **kwargs):
            """
            Improves negative volume cells by node movement
            """
            return PyMenu(self.service).execute('/mesh/modify/repair_negative_volume_cells', *args, **kwargs)
        def auto_improve_warp(self, *args, **kwargs):
            """
            Improve the warp of the faces by node movement.
            """
            return PyMenu(self.service).execute('/mesh/modify/auto_improve_warp', *args, **kwargs)

    class non_conformals(metaclass=PyMenuMeta):
        __doc__ = 'Enter the non conformals controls menu.'
        def create(self, *args, **kwargs):
            """
            Create layer of non conformals on one or more face zones.
            """
            return PyMenu(self.service).execute('/mesh/non_conformals/create', *args, **kwargs)
        def separate(self, *args, **kwargs):
            """
            Separate non-conformal interfaces between cell zones
            """
            return PyMenu(self.service).execute('/mesh/non_conformals/separate', *args, **kwargs)

        class controls(metaclass=PyMenuMeta):
            __doc__ = 'Enter the non conformals controls menu.'
            def enable(self, *args, **kwargs):
                """
                Enable creation of non conformal interface. The quads will be split into tris.
                """
                return PyMenu(self.service).execute('/mesh/non_conformals/controls/enable', *args, **kwargs)
            def retri_method(self, *args, **kwargs):
                """
                Enable triangulation of non-conformal interfaces instead of quad splitting.
                """
                return PyMenu(self.service).execute('/mesh/non_conformals/controls/retri_method', *args, **kwargs)

    class rapid_octree(metaclass=PyMenuMeta):
        __doc__ = 'Enter the octree menu.'
        def verbosity(self, *args, **kwargs):
            """
            Set rapid octree verbosity.
            """
            return PyMenu(self.service).execute('/mesh/rapid_octree/verbosity', *args, **kwargs)
        def estimate_cell_count(self, *args, **kwargs):
            """
            Give a quick estimate about the expected number of cells.
            """
            return PyMenu(self.service).execute('/mesh/rapid_octree/estimate_cell_count', *args, **kwargs)
        def distribute_geometry(self, *args, **kwargs):
            """
            Distributes input geometry across partitions to reduce memory requirements.
            """
            return PyMenu(self.service).execute('/mesh/rapid_octree/distribute_geometry', *args, **kwargs)
        def dry_run(self, *args, **kwargs):
            """
            If yes: Just print diagnostic information, do not create a mesh.
            """
            return PyMenu(self.service).execute('/mesh/rapid_octree/dry_run', *args, **kwargs)
        def undo_last_meshing_operation(self, *args, **kwargs):
            """
            Attempt to undo the last meshing operation
            """
            return PyMenu(self.service).execute('/mesh/rapid_octree/undo_last_meshing_operation', *args, **kwargs)
        def boundary_treatment(self, *args, **kwargs):
            """
            Choose the boundary treatment option (0: Projection , 1: Snapping).
            """
            return PyMenu(self.service).execute('/mesh/rapid_octree/boundary_treatment', *args, **kwargs)
        def bounding_box(self, *args, **kwargs):
            """
            Define/Modify the bounding box around the geometry.
            """
            return PyMenu(self.service).execute('/mesh/rapid_octree/bounding_box', *args, **kwargs)
        def reset_bounding_box(self, *args, **kwargs):
            """
            Redefine the bounding box extends to encompass the currently selected geoemtry.
            """
            return PyMenu(self.service).execute('/mesh/rapid_octree/reset_bounding_box', *args, **kwargs)
        def geometry(self, *args, **kwargs):
            """
            Specify the boundary geometry for the Rapid Octree mesher.
            """
            return PyMenu(self.service).execute('/mesh/rapid_octree/geometry', *args, **kwargs)
        def flow_volume(self, *args, **kwargs):
            """
            Specify the volume to be filled by the mesh.
            """
            return PyMenu(self.service).execute('/mesh/rapid_octree/flow_volume', *args, **kwargs)
        def create(self, *args, **kwargs):
            """
            Create rapid octree mesh.
            """
            return PyMenu(self.service).execute('/mesh/rapid_octree/create', *args, **kwargs)
        def create_stair_step_mesh(self, *args, **kwargs):
            """
            Create rapid octree mesh with a cartesian boundary approximation.
            """
            return PyMenu(self.service).execute('/mesh/rapid_octree/create_stair_step_mesh', *args, **kwargs)
        def is_manifold_geo(self, *args, **kwargs):
            """
            Set to yes if the geomety is manifold (speed up mesh generation).
            """
            return PyMenu(self.service).execute('/mesh/rapid_octree/is_manifold_geo', *args, **kwargs)
        def projection_mesh_optimization(self, *args, **kwargs):
            """
            Set optimization for projection mesh. 0 to deactivate.
            """
            return PyMenu(self.service).execute('/mesh/rapid_octree/projection_mesh_optimization', *args, **kwargs)

        class refinement_regions(metaclass=PyMenuMeta):
            __doc__ = 'Enter the rapid octree refinement region menu.'
            def add(self, *args, **kwargs):
                """
                Add a refinement region to the domain.
                """
                return PyMenu(self.service).execute('/mesh/rapid_octree/refinement_regions/add', *args, **kwargs)
            def delete(self, *args, **kwargs):
                """
                Delete a refinement region.
                """
                return PyMenu(self.service).execute('/mesh/rapid_octree/refinement_regions/delete', *args, **kwargs)
            def list(self, *args, **kwargs):
                """
                List all refinement regions.
                """
                return PyMenu(self.service).execute('/mesh/rapid_octree/refinement_regions/list', *args, **kwargs)

        class mesh_sizing(metaclass=PyMenuMeta):
            __doc__ = 'Define cell sizes.'
            def max_cell_size(self, *args, **kwargs):
                """
                Set maximum cell size in octree mesh.
                """
                return PyMenu(self.service).execute('/mesh/rapid_octree/mesh_sizing/max_cell_size', *args, **kwargs)
            def boundary_cell_size(self, *args, **kwargs):
                """
                Set the default cell size on the geometry.
                """
                return PyMenu(self.service).execute('/mesh/rapid_octree/mesh_sizing/boundary_cell_size', *args, **kwargs)
            def boundary_layers(self, *args, **kwargs):
                """
                Set the minimum number of constant size cells adjacent to the geometry.
                """
                return PyMenu(self.service).execute('/mesh/rapid_octree/mesh_sizing/boundary_layers', *args, **kwargs)
            def prism_layers(self, *args, **kwargs):
                """
                Specify the number of prismatic layers for surface zones.
                """
                return PyMenu(self.service).execute('/mesh/rapid_octree/mesh_sizing/prism_layers', *args, **kwargs)
            def prism_layer_height_adjustment(self, *args, **kwargs):
                """
                Set scheme for adjusting the prism layer height.
                """
                return PyMenu(self.service).execute('/mesh/rapid_octree/mesh_sizing/prism_layer_height_adjustment', *args, **kwargs)
            def buffer_layers(self, *args, **kwargs):
                """
                Set the number of buffer layers.
                """
                return PyMenu(self.service).execute('/mesh/rapid_octree/mesh_sizing/buffer_layers', *args, **kwargs)
            def feature_angle_refinement(self, *args, **kwargs):
                """
                Define angular threshold and number of refinement levels for features.
                """
                return PyMenu(self.service).execute('/mesh/rapid_octree/mesh_sizing/feature_angle_refinement', *args, **kwargs)
            def add_surface_sizing(self, *args, **kwargs):
                """
                Add a target mesh size for a list of surface zones.
                """
                return PyMenu(self.service).execute('/mesh/rapid_octree/mesh_sizing/add_surface_sizing', *args, **kwargs)
            def change_surface_sizing(self, *args, **kwargs):
                """
                Change a size definition.
                """
                return PyMenu(self.service).execute('/mesh/rapid_octree/mesh_sizing/change_surface_sizing', *args, **kwargs)
            def clear_all_surface_sizings(self, *args, **kwargs):
                """
                Remove all defined size functions.
                """
                return PyMenu(self.service).execute('/mesh/rapid_octree/mesh_sizing/clear_all_surface_sizings', *args, **kwargs)
            def list_surface_sizings(self, *args, **kwargs):
                """
                List all defined size functions.
                """
                return PyMenu(self.service).execute('/mesh/rapid_octree/mesh_sizing/list_surface_sizings', *args, **kwargs)
            def delete_surface_sizing(self, *args, **kwargs):
                """
                Delete a size definition.
                """
                return PyMenu(self.service).execute('/mesh/rapid_octree/mesh_sizing/delete_surface_sizing', *args, **kwargs)

        class advanced_meshing_options(metaclass=PyMenuMeta):
            __doc__ = 'Advanced and experimental options for octree mesh generation'
            def pseudo_normal_mode(self, *args, **kwargs):
                """
                Sets the mode for cumputing projection front sudo normals.
                """
                return PyMenu(self.service).execute('/mesh/rapid_octree/advanced_meshing_options/pseudo_normal_mode', *args, **kwargs)
            def target_cell_orthoskew(self, *args, **kwargs):
                """
                Set target orthoskew in mesh (0.0-1.0). Smaller values are likely to increase pullback.
                """
                return PyMenu(self.service).execute('/mesh/rapid_octree/advanced_meshing_options/target_cell_orthoskew', *args, **kwargs)
            def distance_erosion_factor(self, *args, **kwargs):
                """
                Set distance erosion factor as a factor of prism edge length.
                """
                return PyMenu(self.service).execute('/mesh/rapid_octree/advanced_meshing_options/distance_erosion_factor', *args, **kwargs)
            def aspect_ratio_skewness_limit(self, *args, **kwargs):
                """
                Ignore cells with higher skew in aspect ratio improvement.
                """
                return PyMenu(self.service).execute('/mesh/rapid_octree/advanced_meshing_options/aspect_ratio_skewness_limit', *args, **kwargs)
            def projection_priority_zones(self, *args, **kwargs):
                """
                Prioritize zone association of faces crossing multiple boundary zones.
                """
                return PyMenu(self.service).execute('/mesh/rapid_octree/advanced_meshing_options/projection_priority_zones', *args, **kwargs)
            def rename_bounding_box_zones(self, *args, **kwargs):
                """
                Set flag to change naming scheme of bounding box surface zones.
                """
                return PyMenu(self.service).execute('/mesh/rapid_octree/advanced_meshing_options/rename_bounding_box_zones', *args, **kwargs)

    class prism(metaclass=PyMenuMeta):
        __doc__ = 'Enter the scoped prisms menu.'
        def create(self, *args, **kwargs):
            """
            Create prism layers on one or more face zones.
            """
            return PyMenu(self.service).execute('/mesh/prism/create', *args, **kwargs)
        def mark_ignore_faces(self, *args, **kwargs):
            """
            Mark prism base faces which will be ignored
            """
            return PyMenu(self.service).execute('/mesh/prism/mark_ignore_faces', *args, **kwargs)
        def mark_nonmanifold_nodes(self, *args, **kwargs):
            """
            Mark prism base nodes which have invalid manifold around them
            """
            return PyMenu(self.service).execute('/mesh/prism/mark_nonmanifold_nodes', *args, **kwargs)
        def mark_proximity_faces(self, *args, **kwargs):
            """
            Mark prism base faces with certain gap
            """
            return PyMenu(self.service).execute('/mesh/prism/mark_proximity_faces', *args, **kwargs)
        def list_parameters(self, *args, **kwargs):
            """
            Show all prism mesh parameters.
            """
            return PyMenu(self.service).execute('/mesh/prism/list_parameters', *args, **kwargs)
        def reset_parameters(self, *args, **kwargs):
            """
            Reset Prism Parameters
            """
            return PyMenu(self.service).execute('/mesh/prism/reset_parameters', *args, **kwargs)
        def quality_method(self, *args, **kwargs):
            """
            Set prism quality method
            """
            return PyMenu(self.service).execute('/mesh/prism/quality_method', *args, **kwargs)

        class improve(metaclass=PyMenuMeta):
            __doc__ = 'Prism Improve Menu'
            def smooth_prism_cells(self, *args, **kwargs):
                """
                Optimization based smoothing
                """
                return PyMenu(self.service).execute('/mesh/prism/improve/smooth_prism_cells', *args, **kwargs)
            def improve_prism_cells(self, *args, **kwargs):
                """
                Smoothing cells by collecting rings of cells around them
                """
                return PyMenu(self.service).execute('/mesh/prism/improve/improve_prism_cells', *args, **kwargs)
            def smooth_improve_prism_cells(self, *args, **kwargs):
                """
                combination of smooth and improve prism cells
                """
                return PyMenu(self.service).execute('/mesh/prism/improve/smooth_improve_prism_cells', *args, **kwargs)
            def smooth_sliver_skew(self, *args, **kwargs):
                """
                Prism Cells above this skewness will be smoothed.
                """
                return PyMenu(self.service).execute('/mesh/prism/improve/smooth_sliver_skew', *args, **kwargs)
            def smooth_brute_force(self, *args, **kwargs):
                """
                Brute Force smooth cell if cell skewness is still higher after regular smoothing
                """
                return PyMenu(self.service).execute('/mesh/prism/improve/smooth_brute_force', *args, **kwargs)
            def smooth_cell_rings(self, *args, **kwargs):
                """
                No. of Cell rings around the skewed cell used by improve-prism-cells.
                """
                return PyMenu(self.service).execute('/mesh/prism/improve/smooth_cell_rings', *args, **kwargs)

        class post_ignore(metaclass=PyMenuMeta):
            __doc__ = 'Prism Post-Ignore Menu'
            def mark_prism_cap(self, *args, **kwargs):
                """
                post mark cell quality ignore cap.
                """
                return PyMenu(self.service).execute('/mesh/prism/post_ignore/mark_prism_cap', *args, **kwargs)
            def post_remove_cells(self, *args, **kwargs):
                """
                post cell quality ignore.
                """
                return PyMenu(self.service).execute('/mesh/prism/post_ignore/post_remove_cells', *args, **kwargs)
            def create_cavity(self, *args, **kwargs):
                """
                post tet cell quality ignore.
                """
                return PyMenu(self.service).execute('/mesh/prism/post_ignore/create_cavity', *args, **kwargs)
            def mark_cavity_prism_cap(self, *args, **kwargs):
                """
                mark post-ignore tet cell cavity prism cap faces.
                """
                return PyMenu(self.service).execute('/mesh/prism/post_ignore/mark_cavity_prism_cap', *args, **kwargs)

        class split(metaclass=PyMenuMeta):
            __doc__ = 'Prism Post-Split Menu'
            def split(self, *args, **kwargs):
                """
                split prism layer cells.
                """
                return PyMenu(self.service).execute('/mesh/prism/split/split', *args, **kwargs)

        class controls(metaclass=PyMenuMeta):
            __doc__ = 'Prism Controls'
            def merge_ignored_threads(self, *args, **kwargs):
                """
                Automatically merge all ignored zones related to a base thread into one thread?
                """
                return PyMenu(self.service).execute('/mesh/prism/controls/merge_ignored_threads', *args, **kwargs)
            def check_quality(self, *args, **kwargs):
                """
                Check the volume, skewness, and handedness
                of each new cell and face?
                """
                return PyMenu(self.service).execute('/mesh/prism/controls/check_quality', *args, **kwargs)
            def remove_invalid_layer(self, *args, **kwargs):
                """
                remove the last layer if it fails in the quality check
                """
                return PyMenu(self.service).execute('/mesh/prism/controls/remove_invalid_layer', *args, **kwargs)
            def set_post_mesh_controls(self, *args, **kwargs):
                """
                set controls specific to growing prisms post volume mesh
                """
                return PyMenu(self.service).execute('/mesh/prism/controls/set_post_mesh_controls', *args, **kwargs)
            def split(self, *args, **kwargs):
                """
                Split prism cells after prism mesh is done.
                """
                return PyMenu(self.service).execute('/mesh/prism/controls/split', *args, **kwargs)
            def set_overset_prism_controls(self, *args, **kwargs):
                """
                Set boundary layer controls for overset mesh generation.
                """
                return PyMenu(self.service).execute('/mesh/prism/controls/set_overset_prism_controls', *args, **kwargs)

            class morph(metaclass=PyMenuMeta):
                __doc__ = 'Morpher Controls'
                def improve_threshold(self, *args, **kwargs):
                    """
                    Quality threshold used during the morpher improve operation.
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/morph/improve_threshold', *args, **kwargs)
                def morphing_frequency(self, *args, **kwargs):
                    """
                    number of layers created between each morphing call.
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/morph/morphing_frequency', *args, **kwargs)
                def morphing_convergence_limit(self, *args, **kwargs):
                    """
                    relative convergence criterion of the iterative linear solver .
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/morph/morphing_convergence_limit', *args, **kwargs)

            class offset(metaclass=PyMenuMeta):
                __doc__ = 'Prism Offset Controls'
                def min_aspect_ratio(self, *args, **kwargs):
                    """
                    Minimum base-length-over-height for prism cells
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/offset/min_aspect_ratio', *args, **kwargs)
                def first_aspect_ratio_min(self, *args, **kwargs):
                    """
                    Minimum base-length-over-height for prism cells
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/offset/first_aspect_ratio_min', *args, **kwargs)

            class proximity(metaclass=PyMenuMeta):
                __doc__ = 'Prism Proximity Controls'
                def gap_factor(self, *args, **kwargs):
                    """
                    Gap rate to determine the space in proximity region.
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/proximity/gap_factor', *args, **kwargs)
                def allow_ignore(self, *args, **kwargs):
                    """
                    Ignore nodes where shrink factor can't be maintained.
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/proximity/allow_ignore', *args, **kwargs)
                def max_shrink_factor(self, *args, **kwargs):
                    """
                    Shrink factor to determine the maximum shrinkage of prism layer.
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/proximity/max_shrink_factor', *args, **kwargs)
                def max_aspect_ratio(self, *args, **kwargs):
                    """
                    Minimum offset to fall back to avoid degenerate cells
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/proximity/max_aspect_ratio', *args, **kwargs)
                def allow_shrinkage(self, *args, **kwargs):
                    """
                    Allow shrinkage while growing each layer
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/proximity/allow_shrinkage', *args, **kwargs)
                def keep_first_layer_offsets(self, *args, **kwargs):
                    """
                    Fix first layer offsets while performing proximity detection?
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/proximity/keep_first_layer_offsets', *args, **kwargs)

            class normal(metaclass=PyMenuMeta):
                __doc__ = 'Prism Normal Controls'
                def ignore_invalid_normals(self, *args, **kwargs):
                    """
                    Ignore nodes which have very poor normals.
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/normal/ignore_invalid_normals', *args, **kwargs)
                def direction_method(self, *args, **kwargs):
                    """
                    Grow layers normal to surfaces or along a specified direction vector?
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/normal/direction_method', *args, **kwargs)
                def orient_mesh_object_face_normals(self, *args, **kwargs):
                    """
                    Orient Face Normals Of Mesh Object
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/normal/orient_mesh_object_face_normals', *args, **kwargs)
                def compute_normal(self, *args, **kwargs):
                    """
                    Compute normal for the given face zone.
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/normal/compute_normal', *args, **kwargs)
                def direction_vector(self, *args, **kwargs):
                    """
                    Direction vector for prism extrusion.
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/normal/direction_vector', *args, **kwargs)
                def bisect_angle(self, *args, **kwargs):
                    """
                    Advancement vectors are forced onto bisecting planes
                    in sharp corners with angles less than this.
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/normal/bisect_angle', *args, **kwargs)
                def max_angle_change(self, *args, **kwargs):
                    """
                    Smoothing changes in advancement vectors are constrained by this angle.
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/normal/max_angle_change', *args, **kwargs)
                def orthogonal_layers(self, *args, **kwargs):
                    """
                    Number of layers to preserve orthogonality.
                    All smoothing is deferred until after these layers.
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/normal/orthogonal_layers', *args, **kwargs)

            class improve(metaclass=PyMenuMeta):
                __doc__ = 'Prism Smoothing Controls'
                def edge_swap_base_angle(self, *args, **kwargs):
                    """
                    Skewness-driven edge swapping is only allowed between base faces whose normals
                    are within this angle.
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/improve/edge_swap_base_angle', *args, **kwargs)
                def edge_swap_cap_angle(self, *args, **kwargs):
                    """
                    Skewness-driven edge swapping is only allowed between cap faces whose normals
                    are within this angle.
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/improve/edge_swap_cap_angle', *args, **kwargs)
                def max_allowable_cap_skew(self, *args, **kwargs):
                    """
                    Layer growth is stopped if any cap face has
                    skewness > this value (after all smoothing).
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/improve/max_allowable_cap_skew', *args, **kwargs)
                def max_allowable_cell_skew(self, *args, **kwargs):
                    """
                    Cell quality criteria for smoothing and quality checking.
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/improve/max_allowable_cell_skew', *args, **kwargs)
                def corner_height_weight(self, *args, **kwargs):
                    """
                    Improve cell quality/shape by adjusting heights at large corners?
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/improve/corner_height_weight', *args, **kwargs)
                def improve_warp(self, *args, **kwargs):
                    """
                    Perform node movement to improve warp of quad face?
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/improve/improve_warp', *args, **kwargs)
                def face_smooth_skew(self, *args, **kwargs):
                    """
                    Min. skewness to smooth cap faces.
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/improve/face_smooth_skew', *args, **kwargs)
                def check_allowable_skew(self, *args, **kwargs):
                    """
                    Check skewness for cap every layer?
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/improve/check_allowable_skew', *args, **kwargs)
                def left_hand_check(self, *args, **kwargs):
                    """
                    check for left handedness of faces
                    (0 - no check, 1 - only cap faces, 2 - faces of all cells in current layer).
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/improve/left_hand_check', *args, **kwargs)
                def smooth_improve_prism_cells(self, *args, **kwargs):
                    """
                    smooth and improve prism cells.
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/improve/smooth_improve_prism_cells', *args, **kwargs)

            class post_ignore(metaclass=PyMenuMeta):
                __doc__ = 'Prism Post Ignore Controls'
                def post_remove_cells(self, *args, **kwargs):
                    """
                    Post remove bad prism cells.
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/post_ignore/post_remove_cells', *args, **kwargs)

            class adjacent_zone(metaclass=PyMenuMeta):
                __doc__ = 'Prism Adjacent Zone Controls'
                def side_feature_angle(self, *args, **kwargs):
                    """
                    This angle (degrees) is used for computing feature normals (more flexible than retriangulation-feature-angle).
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/adjacent_zone/side_feature_angle', *args, **kwargs)
                def project_adjacent_angle(self, *args, **kwargs):
                    """
                    Outer edges of advancing layers are projected to
                    adjacent planar zones whose angles relative to the growth direction are
                    less than or equal to this angle.
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/adjacent_zone/project_adjacent_angle', *args, **kwargs)

            class zone_specific_growth(metaclass=PyMenuMeta):
                __doc__ = 'Prism Growth Controls'
                def apply_growth(self, *args, **kwargs):
                    """
                    Apply prism growth on individual zones.
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/zone_specific_growth/apply_growth', *args, **kwargs)
                def clear_growth(self, *args, **kwargs):
                    """
                    Clear zone specific growth on individual zones.
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/zone_specific_growth/clear_growth', *args, **kwargs)
                def list_growth(self, *args, **kwargs):
                    """
                    List zone specific growth on applied zones.
                    """
                    return PyMenu(self.service).execute('/mesh/prism/controls/zone_specific_growth/list_growth', *args, **kwargs)

    class pyramid(metaclass=PyMenuMeta):
        __doc__ = 'Enter the pyramid controls menu.'
        def create(self, *args, **kwargs):
            """
            Create layer of pyramids on quad face zone.
            """
            return PyMenu(self.service).execute('/mesh/pyramid/create', *args, **kwargs)

        class controls(metaclass=PyMenuMeta):
            __doc__ = 'Enter the pyramid controls menu.'
            def neighbor_angle(self, *args, **kwargs):
                """
                Dihedral angle threshold used to limit which neighboring faces are considered in the creation of pyramids.
                """
                return PyMenu(self.service).execute('/mesh/pyramid/controls/neighbor_angle', *args, **kwargs)
            def offset_scaling(self, *args, **kwargs):
                """
                The node created to produce a pyramid from a face is positioned along a vector emanating from the face centroid in the direction of the face's normal.  This factor scales the distance along this vector, unity represents an equilateral pyramid.
                """
                return PyMenu(self.service).execute('/mesh/pyramid/controls/offset_scaling', *args, **kwargs)
            def vertex_method(self, *args, **kwargs):
                """
                Method by which offset distances are determined.
                """
                return PyMenu(self.service).execute('/mesh/pyramid/controls/vertex_method', *args, **kwargs)
            def offset_factor(self, *args, **kwargs):
                """
                Factor of pyramid height used to randomly adjust the height of the pyramids during pyramid creation. Default is 0.
                """
                return PyMenu(self.service).execute('/mesh/pyramid/controls/offset_factor', *args, **kwargs)

    class thin_volume_mesh(metaclass=PyMenuMeta):
        __doc__ = 'Enter the thin volume mesh controls menu.'
        def create(self, *args, **kwargs):
            """
            Create thin volume mesh on one or more face zones.
            """
            return PyMenu(self.service).execute('/mesh/thin_volume_mesh/create', *args, **kwargs)

    class separate(metaclass=PyMenuMeta):
        __doc__ = 'Separate cells by various user defined methods.'
        def separate_cell_by_face(self, *args, **kwargs):
            """
            Separate prism cell with source faces.
            """
            return PyMenu(self.service).execute('/mesh/separate/separate_cell_by_face', *args, **kwargs)
        def separate_cell_by_mark(self, *args, **kwargs):
            """
            Separate cell by marks.
            """
            return PyMenu(self.service).execute('/mesh/separate/separate_cell_by_mark', *args, **kwargs)
        def separate_prisms_from_poly(self, *args, **kwargs):
            """
            Separate poly-prism cells from poly.
            """
            return PyMenu(self.service).execute('/mesh/separate/separate_prisms_from_poly', *args, **kwargs)
        def separate_cell_by_region(self, *args, **kwargs):
            """
            Separate cell by region.
            """
            return PyMenu(self.service).execute('/mesh/separate/separate_cell_by_region', *args, **kwargs)
        def separate_cell_by_shape(self, *args, **kwargs):
            """
            Separate cell thread by cell shape.
            """
            return PyMenu(self.service).execute('/mesh/separate/separate_cell_by_shape', *args, **kwargs)
        def separate_cell_by_skew(self, *args, **kwargs):
            """
            Separate cell thread by cell skewness.
            """
            return PyMenu(self.service).execute('/mesh/separate/separate_cell_by_skew', *args, **kwargs)
        def separate_cell_by_size(self, *args, **kwargs):
            """
            Separate cell thread by cell size.
            """
            return PyMenu(self.service).execute('/mesh/separate/separate_cell_by_size', *args, **kwargs)

        class local_regions(metaclass=PyMenuMeta):
            __doc__ = 'Enter the refine-local menu'
            def define(self, *args, **kwargs):
                """
                Define a refinement region's parameters.
                """
                return PyMenu(self.service).execute('/mesh/separate/local_regions/define', *args, **kwargs)
            def delete(self, *args, **kwargs):
                """
                Delete a refinement region.
                """
                return PyMenu(self.service).execute('/mesh/separate/local_regions/delete', *args, **kwargs)
            def init(self, *args, **kwargs):
                """
                Delete all current regions and add the default refinement region.
                """
                return PyMenu(self.service).execute('/mesh/separate/local_regions/init', *args, **kwargs)
            def list_all_regions(self, *args, **kwargs):
                """
                List all refinement regions.
                """
                return PyMenu(self.service).execute('/mesh/separate/local_regions/list_all_regions', *args, **kwargs)

    class tet(metaclass=PyMenuMeta):
        __doc__ = 'Enter the triangulation menu.'
        def delete_virtual_cells(self, *args, **kwargs):
            """
            Delete virtual face/dead cells left by activating keep-virtual-entities?
            """
            return PyMenu(self.service).execute('/mesh/tet/delete_virtual_cells', *args, **kwargs)
        def init(self, *args, **kwargs):
            """
            Tet mesh initialization.
            """
            return PyMenu(self.service).execute('/mesh/tet/init', *args, **kwargs)
        def init_refine(self, *args, **kwargs):
            """
            Tet initialization and refinement of mesh.
            """
            return PyMenu(self.service).execute('/mesh/tet/init_refine', *args, **kwargs)
        def mesh_object(self, *args, **kwargs):
            """
            Tet mesh object of type mesh.
            """
            return PyMenu(self.service).execute('/mesh/tet/mesh_object', *args, **kwargs)
        def preserve_cell_zone(self, *args, **kwargs):
            """
            Preserve cell zone.
            """
            return PyMenu(self.service).execute('/mesh/tet/preserve_cell_zone', *args, **kwargs)
        def un_preserve_cell_zone(self, *args, **kwargs):
            """
            Un-preserve cell zone.
            """
            return PyMenu(self.service).execute('/mesh/tet/un_preserve_cell_zone', *args, **kwargs)
        def refine(self, *args, **kwargs):
            """
            Tet mesh refinement.
            """
            return PyMenu(self.service).execute('/mesh/tet/refine', *args, **kwargs)
        def trace_path_between_cells(self, *args, **kwargs):
            """
            Trace path between two cell.
            """
            return PyMenu(self.service).execute('/mesh/tet/trace_path_between_cells', *args, **kwargs)

        class controls(metaclass=PyMenuMeta):
            __doc__ = 'tet controls'
            def cell_sizing(self, *args, **kwargs):
                """
                Allow cell volume distribution to be determined based on boundary.
                """
                return PyMenu(self.service).execute('/mesh/tet/controls/cell_sizing', *args, **kwargs)
            def set_zone_growth_rate(self, *args, **kwargs):
                """
                Set zone specific geometric growth rates.
                """
                return PyMenu(self.service).execute('/mesh/tet/controls/set_zone_growth_rate', *args, **kwargs)
            def clear_zone_growth_rate(self, *args, **kwargs):
                """
                Clear zone specific geometric growth rates.
                """
                return PyMenu(self.service).execute('/mesh/tet/controls/clear_zone_growth_rate', *args, **kwargs)
            def compute_max_cell_volume(self, *args, **kwargs):
                """
                Computes max cell size.
                """
                return PyMenu(self.service).execute('/mesh/tet/controls/compute_max_cell_volume', *args, **kwargs)
            def delete_dead_zones(self, *args, **kwargs):
                """
                Automatically delete dead face and cell zones?.
                """
                return PyMenu(self.service).execute('/mesh/tet/controls/delete_dead_zones', *args, **kwargs)
            def max_cell_length(self, *args, **kwargs):
                """
                Set max-cell-length.
                """
                return PyMenu(self.service).execute('/mesh/tet/controls/max_cell_length', *args, **kwargs)
            def max_cell_volume(self, *args, **kwargs):
                """
                Set max-cell-volume.
                """
                return PyMenu(self.service).execute('/mesh/tet/controls/max_cell_volume', *args, **kwargs)
            def use_max_cell_size(self, *args, **kwargs):
                """
                Use max cell size for objects in auto-mesh and do not recompute it based on the object being meshed
                """
                return PyMenu(self.service).execute('/mesh/tet/controls/use_max_cell_size', *args, **kwargs)
            def non_fluid_type(self, *args, **kwargs):
                """
                Select the default non-fluid cell zone type.
                """
                return PyMenu(self.service).execute('/mesh/tet/controls/non_fluid_type', *args, **kwargs)
            def refine_method(self, *args, **kwargs):
                """
                Define refinement method.
                """
                return PyMenu(self.service).execute('/mesh/tet/controls/refine_method', *args, **kwargs)
            def set_region_based_sizing(self, *args, **kwargs):
                """
                Set region based sizings.
                """
                return PyMenu(self.service).execute('/mesh/tet/controls/set_region_based_sizing', *args, **kwargs)
            def print_region_based_sizing(self, *args, **kwargs):
                """
                Print region based sizings.
                """
                return PyMenu(self.service).execute('/mesh/tet/controls/print_region_based_sizing', *args, **kwargs)
            def skewness_method(self, *args, **kwargs):
                """
                Skewness refinement controls.
                """
                return PyMenu(self.service).execute('/mesh/tet/controls/skewness_method', *args, **kwargs)

            class improve_mesh(metaclass=PyMenuMeta):
                __doc__ = 'Improve mesh controls.'
                def improve(self, *args, **kwargs):
                    """
                    Automatically improve mesh.
                    """
                    return PyMenu(self.service).execute('/mesh/tet/controls/improve_mesh/improve', *args, **kwargs)
                def swap(self, *args, **kwargs):
                    """
                    Face swap parameters.
                    """
                    return PyMenu(self.service).execute('/mesh/tet/controls/improve_mesh/swap', *args, **kwargs)
                def skewness_smooth(self, *args, **kwargs):
                    """
                    Skewness smooth parametersx.
                    """
                    return PyMenu(self.service).execute('/mesh/tet/controls/improve_mesh/skewness_smooth', *args, **kwargs)
                def laplace_smooth(self, *args, **kwargs):
                    """
                    Laplace smooth parameters.
                    """
                    return PyMenu(self.service).execute('/mesh/tet/controls/improve_mesh/laplace_smooth', *args, **kwargs)

            class adv_front_method(metaclass=PyMenuMeta):
                __doc__ = 'Advancing front refinement controls.'
                def refine_parameters(self, *args, **kwargs):
                    """
                    Define refine parameters.
                    """
                    return PyMenu(self.service).execute('/mesh/tet/controls/adv_front_method/refine_parameters', *args, **kwargs)
                def first_improve_params(self, *args, **kwargs):
                    """
                    Define refine front improve parameters.
                    """
                    return PyMenu(self.service).execute('/mesh/tet/controls/adv_front_method/first_improve_params', *args, **kwargs)
                def second_improve_params(self, *args, **kwargs):
                    """
                    Define cell zone improve parameters.
                    """
                    return PyMenu(self.service).execute('/mesh/tet/controls/adv_front_method/second_improve_params', *args, **kwargs)

                class skew_improve(metaclass=PyMenuMeta):
                    __doc__ = 'Refine improve controls.'
                    def boundary_sliver_skew(self, *args, **kwargs):
                        """
                        Refine improve boundary sliver skew.
                        """
                        return PyMenu(self.service).execute('/mesh/tet/controls/adv_front_method/skew_improve/boundary_sliver_skew', *args, **kwargs)
                    def sliver_skew(self, *args, **kwargs):
                        """
                        Refine improve sliver skew.
                        """
                        return PyMenu(self.service).execute('/mesh/tet/controls/adv_front_method/skew_improve/sliver_skew', *args, **kwargs)
                    def target(self, *args, **kwargs):
                        """
                        Activate target skew refinement.
                        """
                        return PyMenu(self.service).execute('/mesh/tet/controls/adv_front_method/skew_improve/target', *args, **kwargs)
                    def target_skew(self, *args, **kwargs):
                        """
                        Refine improve target skew.
                        """
                        return PyMenu(self.service).execute('/mesh/tet/controls/adv_front_method/skew_improve/target_skew', *args, **kwargs)
                    def target_low_skew(self, *args, **kwargs):
                        """
                        Refine improve target low skew.
                        """
                        return PyMenu(self.service).execute('/mesh/tet/controls/adv_front_method/skew_improve/target_low_skew', *args, **kwargs)
                    def attempts(self, *args, **kwargs):
                        """
                        Refine improve attempts.
                        """
                        return PyMenu(self.service).execute('/mesh/tet/controls/adv_front_method/skew_improve/attempts', *args, **kwargs)
                    def iterations(self, *args, **kwargs):
                        """
                        Refine improve iterations.
                        """
                        return PyMenu(self.service).execute('/mesh/tet/controls/adv_front_method/skew_improve/iterations', *args, **kwargs)

            class remove_slivers(metaclass=PyMenuMeta):
                __doc__ = 'Sliver remove controls.'
                def remove(self, *args, **kwargs):
                    """
                    Automatically remove slivers.
                    """
                    return PyMenu(self.service).execute('/mesh/tet/controls/remove_slivers/remove', *args, **kwargs)
                def skew(self, *args, **kwargs):
                    """
                    Remove sliver skew.
                    """
                    return PyMenu(self.service).execute('/mesh/tet/controls/remove_slivers/skew', *args, **kwargs)
                def low_skew(self, *args, **kwargs):
                    """
                    Remove sliver low skew.
                    """
                    return PyMenu(self.service).execute('/mesh/tet/controls/remove_slivers/low_skew', *args, **kwargs)
                def angle(self, *args, **kwargs):
                    """
                    Max dihedral angle defining a valid boundary sliver.
                    """
                    return PyMenu(self.service).execute('/mesh/tet/controls/remove_slivers/angle', *args, **kwargs)
                def attempts(self, *args, **kwargs):
                    """
                    Sliver remove attempts.
                    """
                    return PyMenu(self.service).execute('/mesh/tet/controls/remove_slivers/attempts', *args, **kwargs)
                def iterations(self, *args, **kwargs):
                    """
                    Sliver remove iterations.
                    """
                    return PyMenu(self.service).execute('/mesh/tet/controls/remove_slivers/iterations', *args, **kwargs)
                def method(self, *args, **kwargs):
                    """
                    Sliver remove method.
                    """
                    return PyMenu(self.service).execute('/mesh/tet/controls/remove_slivers/method', *args, **kwargs)

            class tet_improve(metaclass=PyMenuMeta):
                __doc__ = 'Improve cells controls.'
                def skew(self, *args, **kwargs):
                    """
                    Remove skew.
                    """
                    return PyMenu(self.service).execute('/mesh/tet/controls/tet_improve/skew', *args, **kwargs)
                def angle(self, *args, **kwargs):
                    """
                    Max dihedral angle defining a valid boundary cell.
                    """
                    return PyMenu(self.service).execute('/mesh/tet/controls/tet_improve/angle', *args, **kwargs)
                def attempts(self, *args, **kwargs):
                    """
                    Improve attempts.
                    """
                    return PyMenu(self.service).execute('/mesh/tet/controls/tet_improve/attempts', *args, **kwargs)
                def iterations(self, *args, **kwargs):
                    """
                    Improve iterations.
                    """
                    return PyMenu(self.service).execute('/mesh/tet/controls/tet_improve/iterations', *args, **kwargs)

        class improve(metaclass=PyMenuMeta):
            __doc__ = 'Enter the Tet improve menu'
            def swap_faces(self, *args, **kwargs):
                """
                Perform interior face swapping to improve cell skewness.
                """
                return PyMenu(self.service).execute('/mesh/tet/improve/swap_faces', *args, **kwargs)
            def refine_slivers(self, *args, **kwargs):
                """
                Refine sliver cells by introducing
                node near centroid.
                """
                return PyMenu(self.service).execute('/mesh/tet/improve/refine_slivers', *args, **kwargs)
            def sliver_boundary_swap(self, *args, **kwargs):
                """
                Remove boundary slivers by moving the boundary
                to exclude the cells from the zone.
                """
                return PyMenu(self.service).execute('/mesh/tet/improve/sliver_boundary_swap', *args, **kwargs)
            def refine_boundary_slivers(self, *args, **kwargs):
                """
                Refine boundary slivers by edge-split.
                """
                return PyMenu(self.service).execute('/mesh/tet/improve/refine_boundary_slivers', *args, **kwargs)
            def collapse_slivers(self, *args, **kwargs):
                """
                Remove skewed cells by edge collapse.
                """
                return PyMenu(self.service).execute('/mesh/tet/improve/collapse_slivers', *args, **kwargs)
            def improve_cells(self, *args, **kwargs):
                """
                Improve skewed cells.
                """
                return PyMenu(self.service).execute('/mesh/tet/improve/improve_cells', *args, **kwargs)
            def smooth_boundary_sliver(self, *args, **kwargs):
                """
                Smooth skewed cells with all nodes on the boundary.
                """
                return PyMenu(self.service).execute('/mesh/tet/improve/smooth_boundary_sliver', *args, **kwargs)
            def smooth_interior_sliver(self, *args, **kwargs):
                """
                Smooth skewed cells with some interior node.
                """
                return PyMenu(self.service).execute('/mesh/tet/improve/smooth_interior_sliver', *args, **kwargs)
            def smooth_nodes(self, *args, **kwargs):
                """
                Smooth node locations.
                """
                return PyMenu(self.service).execute('/mesh/tet/improve/smooth_nodes', *args, **kwargs)
            def skew_smooth_nodes(self, *args, **kwargs):
                """
                Smooth node locations.
                """
                return PyMenu(self.service).execute('/mesh/tet/improve/skew_smooth_nodes', *args, **kwargs)

        class local_regions(metaclass=PyMenuMeta):
            __doc__ = 'Enter the refine-local menu'
            def activate(self, *args, **kwargs):
                """
                Activate regions for tet refinement
                """
                return PyMenu(self.service).execute('/mesh/tet/local_regions/activate', *args, **kwargs)
            def deactivate(self, *args, **kwargs):
                """
                Activate regions for tet refinement
                """
                return PyMenu(self.service).execute('/mesh/tet/local_regions/deactivate', *args, **kwargs)
            def define(self, *args, **kwargs):
                """
                Define a refinement region's parameters.
                """
                return PyMenu(self.service).execute('/mesh/tet/local_regions/define', *args, **kwargs)
            def delete(self, *args, **kwargs):
                """
                Delete a refinement region.
                """
                return PyMenu(self.service).execute('/mesh/tet/local_regions/delete', *args, **kwargs)
            def init(self, *args, **kwargs):
                """
                Delete all current regions and add the default refinement region.
                """
                return PyMenu(self.service).execute('/mesh/tet/local_regions/init', *args, **kwargs)
            def list_all_regions(self, *args, **kwargs):
                """
                List all refinement regions.
                """
                return PyMenu(self.service).execute('/mesh/tet/local_regions/list_all_regions', *args, **kwargs)
            def refine(self, *args, **kwargs):
                """
                Refine live cells inside region based on refinement parameters.
                """
                return PyMenu(self.service).execute('/mesh/tet/local_regions/refine', *args, **kwargs)
            def ideal_vol(self, *args, **kwargs):
                """
                Ideal tet volume for given edge length.
                """
                return PyMenu(self.service).execute('/mesh/tet/local_regions/ideal_vol', *args, **kwargs)
            def ideal_area(self, *args, **kwargs):
                """
                Ideal triangle area for given edge length.
                """
                return PyMenu(self.service).execute('/mesh/tet/local_regions/ideal_area', *args, **kwargs)

    class manage(metaclass=PyMenuMeta):
        __doc__ = 'Enter cell zone menu.'
        def adjacent_face_zones(self, *args, **kwargs):
            """
            List all face zones referring the specified cell zone.
            """
            return PyMenu(self.service).execute('/mesh/manage/adjacent_face_zones', *args, **kwargs)
        def auto_set_active(self, *args, **kwargs):
            """
            Set active zones based on prescribed points.
            """
            return PyMenu(self.service).execute('/mesh/manage/auto_set_active', *args, **kwargs)
        def active_list(self, *args, **kwargs):
            """
            List active cell zones.
            """
            return PyMenu(self.service).execute('/mesh/manage/active_list', *args, **kwargs)
        def copy(self, *args, **kwargs):
            """
            copy the zone.
            """
            return PyMenu(self.service).execute('/mesh/manage/copy', *args, **kwargs)
        def change_prefix(self, *args, **kwargs):
            """
            Change the prefix for specified face zones.
            """
            return PyMenu(self.service).execute('/mesh/manage/change_prefix', *args, **kwargs)
        def change_suffix(self, *args, **kwargs):
            """
            Change the suffix for specified face zones.
            """
            return PyMenu(self.service).execute('/mesh/manage/change_suffix', *args, **kwargs)
        def delete(self, *args, **kwargs):
            """
            Delete cell zone.
            """
            return PyMenu(self.service).execute('/mesh/manage/delete', *args, **kwargs)
        def id(self, *args, **kwargs):
            """
            Give zone a new id number.
            """
            return PyMenu(self.service).execute('/mesh/manage/id', *args, **kwargs)
        def list(self, *args, **kwargs):
            """
            List all cell zones.
            """
            return PyMenu(self.service).execute('/mesh/manage/list', *args, **kwargs)
        def merge(self, *args, **kwargs):
            """
            Merge two or more cell zones.
            """
            return PyMenu(self.service).execute('/mesh/manage/merge', *args, **kwargs)
        def name(self, *args, **kwargs):
            """
            Give zone a new name.
            """
            return PyMenu(self.service).execute('/mesh/manage/name', *args, **kwargs)
        def origin(self, *args, **kwargs):
            """
            Set the origin of the mesh coordinates.
            """
            return PyMenu(self.service).execute('/mesh/manage/origin', *args, **kwargs)
        def rotate(self, *args, **kwargs):
            """
            Rotate all nodes of specified cell zones.
            """
            return PyMenu(self.service).execute('/mesh/manage/rotate', *args, **kwargs)
        def rotate_model(self, *args, **kwargs):
            """
            Rotate all nodes.
            """
            return PyMenu(self.service).execute('/mesh/manage/rotate_model', *args, **kwargs)
        def revolve_face_zone(self, *args, **kwargs):
            """
            Generate cells by revolving a face thread
            """
            return PyMenu(self.service).execute('/mesh/manage/revolve_face_zone', *args, **kwargs)
        def scale(self, *args, **kwargs):
            """
            Scale all nodes of specified cell zones.
            """
            return PyMenu(self.service).execute('/mesh/manage/scale', *args, **kwargs)
        def scale_model(self, *args, **kwargs):
            """
            Scale all nodes.
            """
            return PyMenu(self.service).execute('/mesh/manage/scale_model', *args, **kwargs)
        def set_active(self, *args, **kwargs):
            """
            Refine/swap/display only cells in these cell zones.
            """
            return PyMenu(self.service).execute('/mesh/manage/set_active', *args, **kwargs)
        def translate(self, *args, **kwargs):
            """
            Translate all nodes of specified cell zones.
            """
            return PyMenu(self.service).execute('/mesh/manage/translate', *args, **kwargs)
        def translate_model(self, *args, **kwargs):
            """
            Translate all nodes.
            """
            return PyMenu(self.service).execute('/mesh/manage/translate_model', *args, **kwargs)
        def type(self, *args, **kwargs):
            """
            Change cell zone type.
            """
            return PyMenu(self.service).execute('/mesh/manage/type', *args, **kwargs)
        def merge_dead_zones(self, *args, **kwargs):
            """
            Merge dead zones.
            """
            return PyMenu(self.service).execute('/mesh/manage/merge_dead_zones', *args, **kwargs)
        def get_material_point(self, *args, **kwargs):
            """
            Returns material point coordinates for all regions of a cell zone.
            """
            return PyMenu(self.service).execute('/mesh/manage/get_material_point', *args, **kwargs)

    class cell_zone_conditions(metaclass=PyMenuMeta):
        __doc__ = 'Enter manage cell zone conditions menu.'
        def copy(self, *args, **kwargs):
            """
            Copy cell zone conditions.
            """
            return PyMenu(self.service).execute('/mesh/cell_zone_conditions/copy', *args, **kwargs)
        def clear(self, *args, **kwargs):
            """
            Clear cell zone conditions.
            """
            return PyMenu(self.service).execute('/mesh/cell_zone_conditions/clear', *args, **kwargs)
        def clear_all(self, *args, **kwargs):
            """
            Clear all cell zone conditions.
            """
            return PyMenu(self.service).execute('/mesh/cell_zone_conditions/clear_all', *args, **kwargs)

    class poly(metaclass=PyMenuMeta):
        __doc__ = 'Enter the poly menu.'
        def improve(self, *args, **kwargs):
            """
            Smooth poly mesh.
            """
            return PyMenu(self.service).execute('/mesh/poly/improve', *args, **kwargs)
        def collapse(self, *args, **kwargs):
            """
            Collapse short edges and small faces.
            """
            return PyMenu(self.service).execute('/mesh/poly/collapse', *args, **kwargs)
        def remesh(self, *args, **kwargs):
            """
            Remesh local region.
            """
            return PyMenu(self.service).execute('/mesh/poly/remesh', *args, **kwargs)
        def quality_method(self, *args, **kwargs):
            """
            Set poly quality method
            """
            return PyMenu(self.service).execute('/mesh/poly/quality_method', *args, **kwargs)

        class controls(metaclass=PyMenuMeta):
            __doc__ = 'Poly controls'
            def cell_sizing(self, *args, **kwargs):
                """
                Allow cell volume distribution to be determined based on boundary.
                """
                return PyMenu(self.service).execute('/mesh/poly/controls/cell_sizing', *args, **kwargs)
            def non_fluid_type(self, *args, **kwargs):
                """
                Select the default non-fluid cell zone type.
                """
                return PyMenu(self.service).execute('/mesh/poly/controls/non_fluid_type', *args, **kwargs)
            def improve(self, *args, **kwargs):
                """
                Improve the poly mesh by smoothing?
                """
                return PyMenu(self.service).execute('/mesh/poly/controls/improve', *args, **kwargs)
            def feature_angle(self, *args, **kwargs):
                """
                Feature angle.
                """
                return PyMenu(self.service).execute('/mesh/poly/controls/feature_angle', *args, **kwargs)
            def edge_size_ratio(self, *args, **kwargs):
                """
                Size ratio tolerance of two connected edges.
                """
                return PyMenu(self.service).execute('/mesh/poly/controls/edge_size_ratio', *args, **kwargs)
            def face_size_ratio(self, *args, **kwargs):
                """
                Size ratio tolerance of two faces in one cell.
                """
                return PyMenu(self.service).execute('/mesh/poly/controls/face_size_ratio', *args, **kwargs)
            def sliver_cell_area_fraction(self, *args, **kwargs):
                """
                Fraction tolerance between face area and cell surface area.
                """
                return PyMenu(self.service).execute('/mesh/poly/controls/sliver_cell_area_fraction', *args, **kwargs)
            def merge_skew(self, *args, **kwargs):
                """
                Merge minimum skewness.
                """
                return PyMenu(self.service).execute('/mesh/poly/controls/merge_skew', *args, **kwargs)
            def remesh_skew(self, *args, **kwargs):
                """
                Remesh target skewness.
                """
                return PyMenu(self.service).execute('/mesh/poly/controls/remesh_skew', *args, **kwargs)

            class smooth_controls(metaclass=PyMenuMeta):
                __doc__ = 'Poly smooth controls'
                def laplace_smooth_iterations(self, *args, **kwargs):
                    """
                    Laplace smoothing iterations.
                    """
                    return PyMenu(self.service).execute('/mesh/poly/controls/smooth_controls/laplace_smooth_iterations', *args, **kwargs)
                def edge_smooth_iterations(self, *args, **kwargs):
                    """
                    Edge smoothing iterations.
                    """
                    return PyMenu(self.service).execute('/mesh/poly/controls/smooth_controls/edge_smooth_iterations', *args, **kwargs)
                def centroid_smooth_iterations(self, *args, **kwargs):
                    """
                    Centroid smoothing iterations.
                    """
                    return PyMenu(self.service).execute('/mesh/poly/controls/smooth_controls/centroid_smooth_iterations', *args, **kwargs)
                def smooth_iterations(self, *args, **kwargs):
                    """
                    Smooth iterations.
                    """
                    return PyMenu(self.service).execute('/mesh/poly/controls/smooth_controls/smooth_iterations', *args, **kwargs)
                def smooth_attempts(self, *args, **kwargs):
                    """
                    Smooth attempts.
                    """
                    return PyMenu(self.service).execute('/mesh/poly/controls/smooth_controls/smooth_attempts', *args, **kwargs)
                def smooth_boundary(self, *args, **kwargs):
                    """
                    Smooth boundary as part of cell smoothing.
                    """
                    return PyMenu(self.service).execute('/mesh/poly/controls/smooth_controls/smooth_boundary', *args, **kwargs)
                def smooth_on_layer(self, *args, **kwargs):
                    """
                    Smooth poly-prism nodes on layer.
                    """
                    return PyMenu(self.service).execute('/mesh/poly/controls/smooth_controls/smooth_on_layer', *args, **kwargs)
                def smooth_skew(self, *args, **kwargs):
                    """
                    Smooth minimum skewness.
                    """
                    return PyMenu(self.service).execute('/mesh/poly/controls/smooth_controls/smooth_skew', *args, **kwargs)

            class prism(metaclass=PyMenuMeta):
                __doc__ = 'Poly prism transition controls.'
                def apply_growth(self, *args, **kwargs):
                    """
                    Apply growth settings.
                    """
                    return PyMenu(self.service).execute('/mesh/poly/controls/prism/apply_growth', *args, **kwargs)
                def clear_growth(self, *args, **kwargs):
                    """
                    Clear growth settings.
                    """
                    return PyMenu(self.service).execute('/mesh/poly/controls/prism/clear_growth', *args, **kwargs)
                def list_growth(self, *args, **kwargs):
                    """
                    List growth settings.
                    """
                    return PyMenu(self.service).execute('/mesh/poly/controls/prism/list_growth', *args, **kwargs)

        class local_regions(metaclass=PyMenuMeta):
            __doc__ = 'Enter the refine-local menu'
            def activate(self, *args, **kwargs):
                """
                Activate regions for tet refinement
                """
                return PyMenu(self.service).execute('/mesh/poly/local_regions/activate', *args, **kwargs)
            def deactivate(self, *args, **kwargs):
                """
                Activate regions for tet refinement
                """
                return PyMenu(self.service).execute('/mesh/poly/local_regions/deactivate', *args, **kwargs)
            def define(self, *args, **kwargs):
                """
                Define a refinement region's parameters.
                """
                return PyMenu(self.service).execute('/mesh/poly/local_regions/define', *args, **kwargs)
            def delete(self, *args, **kwargs):
                """
                Delete a refinement region.
                """
                return PyMenu(self.service).execute('/mesh/poly/local_regions/delete', *args, **kwargs)
            def init(self, *args, **kwargs):
                """
                Delete all current regions and add the default refinement region.
                """
                return PyMenu(self.service).execute('/mesh/poly/local_regions/init', *args, **kwargs)
            def list_all_regions(self, *args, **kwargs):
                """
                List all refinement regions.
                """
                return PyMenu(self.service).execute('/mesh/poly/local_regions/list_all_regions', *args, **kwargs)
            def refine(self, *args, **kwargs):
                """
                Refine live cells inside region based on refinement parameters.
                """
                return PyMenu(self.service).execute('/mesh/poly/local_regions/refine', *args, **kwargs)
            def ideal_vol(self, *args, **kwargs):
                """
                Ideal tet volume for given edge length.
                """
                return PyMenu(self.service).execute('/mesh/poly/local_regions/ideal_vol', *args, **kwargs)
            def ideal_area(self, *args, **kwargs):
                """
                Ideal triangle area for given edge length.
                """
                return PyMenu(self.service).execute('/mesh/poly/local_regions/ideal_area', *args, **kwargs)

    class poly_hexcore(metaclass=PyMenuMeta):
        __doc__ = 'Enter the poly-hexcore menu.'

        class controls(metaclass=PyMenuMeta):
            __doc__ = 'Enter poly-hexcore controls menu'
            def mark_core_region_cell_type_as_hex(self, *args, **kwargs):
                """
                mark-core-region-cell-type-as-hex?
                """
                return PyMenu(self.service).execute('/mesh/poly_hexcore/controls/mark_core_region_cell_type_as_hex', *args, **kwargs)
            def avoid_1_by_8_cell_jump_in_hexcore(self, *args, **kwargs):
                """
                avoid-1:8-cell-jump-in-hexcore
                """
                return PyMenu(self.service).execute('/mesh/poly_hexcore/controls/avoid_1_by_8_cell_jump_in_hexcore', *args, **kwargs)
            def only_polyhedra_for_selected_regions(self, *args, **kwargs):
                """
                only-polyhedra-for-selected-regions
                """
                return PyMenu(self.service).execute('/mesh/poly_hexcore/controls/only_polyhedra_for_selected_regions', *args, **kwargs)

    class auto_mesh_controls(metaclass=PyMenuMeta):
        __doc__ = 'automesh controls'
        def backup_object(self, *args, **kwargs):
            """
            Option to create a back up for object
            """
            return PyMenu(self.service).execute('/mesh/auto_mesh_controls/backup_object', *args, **kwargs)

    class scoped_prisms(metaclass=PyMenuMeta):
        __doc__ = 'Manage scoped prisms.'
        def create(self, *args, **kwargs):
            """
            Create new scoped prism
            """
            return PyMenu(self.service).execute('/mesh/scoped_prisms/create', *args, **kwargs)
        def modify(self, *args, **kwargs):
            """
            Modify scoped prisms
            """
            return PyMenu(self.service).execute('/mesh/scoped_prisms/modify', *args, **kwargs)
        def delete(self, *args, **kwargs):
            """
            Delete scoped prisms
            """
            return PyMenu(self.service).execute('/mesh/scoped_prisms/delete', *args, **kwargs)
        def list(self, *args, **kwargs):
            """
            List all scoped prisms parameters.
            """
            return PyMenu(self.service).execute('/mesh/scoped_prisms/list', *args, **kwargs)
        def read(self, *args, **kwargs):
            """
            Read scoped prisms from a file
            """
            return PyMenu(self.service).execute('/mesh/scoped_prisms/read', *args, **kwargs)
        def set_no_imprint_zones(self, *args, **kwargs):
            """
            Set zones which should not be imprinted during prism generation
            """
            return PyMenu(self.service).execute('/mesh/scoped_prisms/set_no_imprint_zones', *args, **kwargs)
        def write(self, *args, **kwargs):
            """
            Write scoped prisms to a file
            """
            return PyMenu(self.service).execute('/mesh/scoped_prisms/write', *args, **kwargs)
        def growth_options(self, *args, **kwargs):
            """
            Set scoped prisms growth options
            """
            return PyMenu(self.service).execute('/mesh/scoped_prisms/growth_options', *args, **kwargs)
        def set_overset_prism_controls(self, *args, **kwargs):
            """
            Set boundary layer controls for overset mesh generation.
            """
            return PyMenu(self.service).execute('/mesh/scoped_prisms/set_overset_prism_controls', *args, **kwargs)
        def set_advanced_controls(self, *args, **kwargs):
            """
            Set scoped boundary layer controls.
            """
            return PyMenu(self.service).execute('/mesh/scoped_prisms/set_advanced_controls', *args, **kwargs)

class display(metaclass=PyMenuMeta):
    __doc__ = 'Enter the display menu'
    def annotate(self, *args, **kwargs):
        """
        Add a text annotation string to the active graphics window.
        """
        return PyMenu(self.service).execute('/display/annotate', *args, **kwargs)
    def boundary_cells(self, *args, **kwargs):
        """
        Display boundary cells on the specified face zones.
        """
        return PyMenu(self.service).execute('/display/boundary_cells', *args, **kwargs)
    def boundary_grid(self, *args, **kwargs):
        """
        Display boundary zones on the specified face zones.
        """
        return PyMenu(self.service).execute('/display/boundary_grid', *args, **kwargs)
    def center_view_on(self, *args, **kwargs):
        """
        Set camera target to be center (centroid) of grid node/face/cell.
        """
        return PyMenu(self.service).execute('/display/center_view_on', *args, **kwargs)
    def clear(self, *args, **kwargs):
        """
        Clear active graphics window.
        """
        return PyMenu(self.service).execute('/display/clear', *args, **kwargs)
    def clear_annotation(self, *args, **kwargs):
        """
        Delete annotation text.
        """
        return PyMenu(self.service).execute('/display/clear_annotation', *args, **kwargs)
    def draw_zones(self, *args, **kwargs):
        """
        Draw the specified zones using the default grid parameters.
        """
        return PyMenu(self.service).execute('/display/draw_zones', *args, **kwargs)
    def draw_cells_using_faces(self, *args, **kwargs):
        """
        Draw cells using selected faces.
        """
        return PyMenu(self.service).execute('/display/draw_cells_using_faces', *args, **kwargs)
    def draw_cells_using_nodes(self, *args, **kwargs):
        """
        Draw cells using selected nodes.
        """
        return PyMenu(self.service).execute('/display/draw_cells_using_nodes', *args, **kwargs)
    def draw_face_zones_using_entities(self, *args, **kwargs):
        """
        Draw face zone connected to node.
        """
        return PyMenu(self.service).execute('/display/draw_face_zones_using_entities', *args, **kwargs)
    def all_grid(self, *args, **kwargs):
        """
        Display grid zones according to parameters in set-grid.
        """
        return PyMenu(self.service).execute('/display/all_grid', *args, **kwargs)
    def save_picture(self, *args, **kwargs):
        """
        Generate a "hardcopy" of the active window.
        """
        return PyMenu(self.service).execute('/display/save_picture', *args, **kwargs)
    def redisplay(self, *args, **kwargs):
        """
        Re-display grid.
        """
        return PyMenu(self.service).execute('/display/redisplay', *args, **kwargs)
    def show_hide_clipping_plane_triad(self, *args, **kwargs):
        """
        Show/Hide clipping plane triad.
        """
        return PyMenu(self.service).execute('/display/show_hide_clipping_plane_triad', *args, **kwargs)
    def set_list_tree_separator(self, *args, **kwargs):
        """
        Set the separator character for list tree.
        """
        return PyMenu(self.service).execute('/display/set_list_tree_separator', *args, **kwargs)
    def update_layout(self, *args, **kwargs):
        """
        update the fluent layout
        """
        return PyMenu(self.service).execute('/display/update_layout', *args, **kwargs)

    class set(metaclass=PyMenuMeta):
        __doc__ = 'Menu to set display parameters.'
        def highlight_tree_selection(self, *args, **kwargs):
            """
            Turn on/off outline display of tree selection in graphics window.
            """
            return PyMenu(self.service).execute('/display/set/highlight_tree_selection', *args, **kwargs)
        def remote_display_defaults(self, *args, **kwargs):
            """
            Apply display settings recommended for remote display.
            """
            return PyMenu(self.service).execute('/display/set/remote_display_defaults', *args, **kwargs)
        def native_display_defaults(self, *args, **kwargs):
            """
            Apply display settings recommended for native display.
            """
            return PyMenu(self.service).execute('/display/set/native_display_defaults', *args, **kwargs)
        def edges(self, *args, **kwargs):
            """
            Turn on/off display of face/cell edges.
            """
            return PyMenu(self.service).execute('/display/set/edges', *args, **kwargs)
        def filled_grid(self, *args, **kwargs):
            """
            Turn on/off filled grid option.
            """
            return PyMenu(self.service).execute('/display/set/filled_grid', *args, **kwargs)
        def quick_moves_algorithm(self, *args, **kwargs):
            """
            Select quick moves algorithm for icons and helptext overlay.
            """
            return PyMenu(self.service).execute('/display/set/quick_moves_algorithm', *args, **kwargs)
        def line_weight(self, *args, **kwargs):
            """
            Set the window's line-weight factor.
            """
            return PyMenu(self.service).execute('/display/set/line_weight', *args, **kwargs)
        def overlays(self, *args, **kwargs):
            """
            Turn on/off overlays.
            """
            return PyMenu(self.service).execute('/display/set/overlays', *args, **kwargs)
        def re_render(self, *args, **kwargs):
            """
            Re-render current window after modifying variables in set menu.
            """
            return PyMenu(self.service).execute('/display/set/re_render', *args, **kwargs)
        def reset_graphics(self, *args, **kwargs):
            """
            Reset the graphics system.
            """
            return PyMenu(self.service).execute('/display/set/reset_graphics', *args, **kwargs)
        def shrink_factor(self, *args, **kwargs):
            """
            Set grid shrink factor.
            """
            return PyMenu(self.service).execute('/display/set/shrink_factor', *args, **kwargs)
        def title(self, *args, **kwargs):
            """
            Set problem title
            """
            return PyMenu(self.service).execute('/display/set/title', *args, **kwargs)

        class colors(metaclass=PyMenuMeta):
            __doc__ = 'Color options menu.'
            def background(self, *args, **kwargs):
                """
                Set the background (window) color.
                """
                return PyMenu(self.service).execute('/display/set/colors/background', *args, **kwargs)
            def color_by_type(self, *args, **kwargs):
                """
                Determine whether to color meshes by type or by surface (ID).
                """
                return PyMenu(self.service).execute('/display/set/colors/color_by_type', *args, **kwargs)
            def foreground(self, *args, **kwargs):
                """
                Set the foreground (text and window frame) color.
                """
                return PyMenu(self.service).execute('/display/set/colors/foreground', *args, **kwargs)
            def far_field_faces(self, *args, **kwargs):
                """
                Set the color of far field faces.
                """
                return PyMenu(self.service).execute('/display/set/colors/far_field_faces', *args, **kwargs)
            def inlet_faces(self, *args, **kwargs):
                """
                Set the color of inlet faces.
                """
                return PyMenu(self.service).execute('/display/set/colors/inlet_faces', *args, **kwargs)
            def interior_faces(self, *args, **kwargs):
                """
                Set the color of interior faces.
                """
                return PyMenu(self.service).execute('/display/set/colors/interior_faces', *args, **kwargs)
            def internal_faces(self, *args, **kwargs):
                """
                Set the color of internal interface faces
                """
                return PyMenu(self.service).execute('/display/set/colors/internal_faces', *args, **kwargs)
            def outlet_faces(self, *args, **kwargs):
                """
                Set the color of outlet faces.
                """
                return PyMenu(self.service).execute('/display/set/colors/outlet_faces', *args, **kwargs)
            def overset_faces(self, *args, **kwargs):
                """
                Set the color of overset faces.
                """
                return PyMenu(self.service).execute('/display/set/colors/overset_faces', *args, **kwargs)
            def periodic_faces(self, *args, **kwargs):
                """
                Set the color of periodic faces.
                """
                return PyMenu(self.service).execute('/display/set/colors/periodic_faces', *args, **kwargs)
            def rans_les_interface_faces(self, *args, **kwargs):
                """
                Set the color of RANS/LES interface faces.
                """
                return PyMenu(self.service).execute('/display/set/colors/rans_les_interface_faces', *args, **kwargs)
            def reset_user_colors(self, *args, **kwargs):
                """
                Reset all user colors
                """
                return PyMenu(self.service).execute('/display/set/colors/reset_user_colors', *args, **kwargs)
            def show_user_colors(self, *args, **kwargs):
                """
                List currently defined user colors
                """
                return PyMenu(self.service).execute('/display/set/colors/show_user_colors', *args, **kwargs)
            def symmetry_faces(self, *args, **kwargs):
                """
                Set the color of symmetric faces.
                """
                return PyMenu(self.service).execute('/display/set/colors/symmetry_faces', *args, **kwargs)
            def axis_faces(self, *args, **kwargs):
                """
                Set the color of axisymmetric faces.
                """
                return PyMenu(self.service).execute('/display/set/colors/axis_faces', *args, **kwargs)
            def free_surface_faces(self, *args, **kwargs):
                """
                Set the color of free-surface faces.
                """
                return PyMenu(self.service).execute('/display/set/colors/free_surface_faces', *args, **kwargs)
            def traction_faces(self, *args, **kwargs):
                """
                Set the color of traction faces.
                """
                return PyMenu(self.service).execute('/display/set/colors/traction_faces', *args, **kwargs)
            def user_color(self, *args, **kwargs):
                """
                Explicitly set color of display zone
                """
                return PyMenu(self.service).execute('/display/set/colors/user_color', *args, **kwargs)
            def wall_faces(self, *args, **kwargs):
                """
                Set the color of wall faces.
                """
                return PyMenu(self.service).execute('/display/set/colors/wall_faces', *args, **kwargs)
            def interface_faces(self, *args, **kwargs):
                """
                Set the color of mesh Interfaces.
                """
                return PyMenu(self.service).execute('/display/set/colors/interface_faces', *args, **kwargs)
            def list(self, *args, **kwargs):
                """
                List available colors.
                """
                return PyMenu(self.service).execute('/display/set/colors/list', *args, **kwargs)
            def reset_colors(self, *args, **kwargs):
                """
                Reset individual mesh surface colors to the defaults.
                """
                return PyMenu(self.service).execute('/display/set/colors/reset_colors', *args, **kwargs)
            def surface(self, *args, **kwargs):
                """
                Set the color of surfaces.
                """
                return PyMenu(self.service).execute('/display/set/colors/surface', *args, **kwargs)
            def skip_label(self, *args, **kwargs):
                """
                Set the number of labels to be skipped in the colopmap scale.
                """
                return PyMenu(self.service).execute('/display/set/colors/skip_label', *args, **kwargs)
            def automatic_skip(self, *args, **kwargs):
                """
                Determine whether to skip labels in the colopmap scale automatically.
                """
                return PyMenu(self.service).execute('/display/set/colors/automatic_skip', *args, **kwargs)
            def graphics_color_theme(self, *args, **kwargs):
                """
                Enter the graphics color theme menu.
                """
                return PyMenu(self.service).execute('/display/set/colors/graphics_color_theme', *args, **kwargs)

            class by_type(metaclass=PyMenuMeta):
                __doc__ = 'Enter the zone type color and material assignment menu.'
                def only_list_case_boundaries(self, *args, **kwargs):
                    """
                    Only list the boundary types that are assigned in this case.
                    """
                    return PyMenu(self.service).execute('/display/set/colors/by_type/only_list_case_boundaries', *args, **kwargs)
                def reset(self, *args, **kwargs):
                    """
                    To reset colors and/or materials to the defaults.
                    """
                    return PyMenu(self.service).execute('/display/set/colors/by_type/reset', *args, **kwargs)

                class type_name(metaclass=PyMenuMeta):
                    __doc__ = 'Select the boundary type to specify colors and/or materials.'

                    class axis(metaclass=PyMenuMeta):
                        __doc__ = 'Set the material and/or color for the selected boundary type.'
                        def color(self, *args, **kwargs):
                            """
                            Set a color for the selected boundary type.
                            """
                            return PyMenu(self.service).execute('/display/set/colors/by_type/type_name/axis/color', *args, **kwargs)
                        def material(self, *args, **kwargs):
                            """
                            Set a material for the selected boundary type.
                            """
                            return PyMenu(self.service).execute('/display/set/colors/by_type/type_name/axis/material', *args, **kwargs)

                    class far_field(metaclass=PyMenuMeta):
                        __doc__ = 'Set the material and/or color for the selected boundary type.'
                        def color(self, *args, **kwargs):
                            """
                            Set a color for the selected boundary type.
                            """
                            return PyMenu(self.service).execute('/display/set/colors/by_type/type_name/far_field/color', *args, **kwargs)
                        def material(self, *args, **kwargs):
                            """
                            Set a material for the selected boundary type.
                            """
                            return PyMenu(self.service).execute('/display/set/colors/by_type/type_name/far_field/material', *args, **kwargs)

                    class free_surface(metaclass=PyMenuMeta):
                        __doc__ = 'Set the material and/or color for the selected boundary type.'
                        def color(self, *args, **kwargs):
                            """
                            Set a color for the selected boundary type.
                            """
                            return PyMenu(self.service).execute('/display/set/colors/by_type/type_name/free_surface/color', *args, **kwargs)
                        def material(self, *args, **kwargs):
                            """
                            Set a material for the selected boundary type.
                            """
                            return PyMenu(self.service).execute('/display/set/colors/by_type/type_name/free_surface/material', *args, **kwargs)

                    class inlet(metaclass=PyMenuMeta):
                        __doc__ = 'Set the material and/or color for the selected boundary type.'
                        def color(self, *args, **kwargs):
                            """
                            Set a color for the selected boundary type.
                            """
                            return PyMenu(self.service).execute('/display/set/colors/by_type/type_name/inlet/color', *args, **kwargs)
                        def material(self, *args, **kwargs):
                            """
                            Set a material for the selected boundary type.
                            """
                            return PyMenu(self.service).execute('/display/set/colors/by_type/type_name/inlet/material', *args, **kwargs)

                    class interface(metaclass=PyMenuMeta):
                        __doc__ = 'Set the material and/or color for the selected boundary type.'
                        def color(self, *args, **kwargs):
                            """
                            Set a color for the selected boundary type.
                            """
                            return PyMenu(self.service).execute('/display/set/colors/by_type/type_name/interface/color', *args, **kwargs)
                        def material(self, *args, **kwargs):
                            """
                            Set a material for the selected boundary type.
                            """
                            return PyMenu(self.service).execute('/display/set/colors/by_type/type_name/interface/material', *args, **kwargs)

                    class interior(metaclass=PyMenuMeta):
                        __doc__ = 'Set the material and/or color for the selected boundary type.'
                        def color(self, *args, **kwargs):
                            """
                            Set a color for the selected boundary type.
                            """
                            return PyMenu(self.service).execute('/display/set/colors/by_type/type_name/interior/color', *args, **kwargs)
                        def material(self, *args, **kwargs):
                            """
                            Set a material for the selected boundary type.
                            """
                            return PyMenu(self.service).execute('/display/set/colors/by_type/type_name/interior/material', *args, **kwargs)

                    class internal(metaclass=PyMenuMeta):
                        __doc__ = 'Set the material and/or color for the selected boundary type.'
                        def color(self, *args, **kwargs):
                            """
                            Set a color for the selected boundary type.
                            """
                            return PyMenu(self.service).execute('/display/set/colors/by_type/type_name/internal/color', *args, **kwargs)
                        def material(self, *args, **kwargs):
                            """
                            Set a material for the selected boundary type.
                            """
                            return PyMenu(self.service).execute('/display/set/colors/by_type/type_name/internal/material', *args, **kwargs)

                    class outlet(metaclass=PyMenuMeta):
                        __doc__ = 'Set the material and/or color for the selected boundary type.'
                        def color(self, *args, **kwargs):
                            """
                            Set a color for the selected boundary type.
                            """
                            return PyMenu(self.service).execute('/display/set/colors/by_type/type_name/outlet/color', *args, **kwargs)
                        def material(self, *args, **kwargs):
                            """
                            Set a material for the selected boundary type.
                            """
                            return PyMenu(self.service).execute('/display/set/colors/by_type/type_name/outlet/material', *args, **kwargs)

                    class overset(metaclass=PyMenuMeta):
                        __doc__ = 'Set the material and/or color for the selected boundary type.'
                        def color(self, *args, **kwargs):
                            """
                            Set a color for the selected boundary type.
                            """
                            return PyMenu(self.service).execute('/display/set/colors/by_type/type_name/overset/color', *args, **kwargs)
                        def material(self, *args, **kwargs):
                            """
                            Set a material for the selected boundary type.
                            """
                            return PyMenu(self.service).execute('/display/set/colors/by_type/type_name/overset/material', *args, **kwargs)

                    class periodic(metaclass=PyMenuMeta):
                        __doc__ = 'Set the material and/or color for the selected boundary type.'
                        def color(self, *args, **kwargs):
                            """
                            Set a color for the selected boundary type.
                            """
                            return PyMenu(self.service).execute('/display/set/colors/by_type/type_name/periodic/color', *args, **kwargs)
                        def material(self, *args, **kwargs):
                            """
                            Set a material for the selected boundary type.
                            """
                            return PyMenu(self.service).execute('/display/set/colors/by_type/type_name/periodic/material', *args, **kwargs)

                    class rans_les_interface(metaclass=PyMenuMeta):
                        __doc__ = 'Set the material and/or color for the selected boundary type.'
                        def color(self, *args, **kwargs):
                            """
                            Set a color for the selected boundary type.
                            """
                            return PyMenu(self.service).execute('/display/set/colors/by_type/type_name/rans_les_interface/color', *args, **kwargs)
                        def material(self, *args, **kwargs):
                            """
                            Set a material for the selected boundary type.
                            """
                            return PyMenu(self.service).execute('/display/set/colors/by_type/type_name/rans_les_interface/material', *args, **kwargs)

                    class surface(metaclass=PyMenuMeta):
                        __doc__ = 'Set the material and/or color for the selected boundary type.'
                        def color(self, *args, **kwargs):
                            """
                            Set a color for the selected boundary type.
                            """
                            return PyMenu(self.service).execute('/display/set/colors/by_type/type_name/surface/color', *args, **kwargs)
                        def material(self, *args, **kwargs):
                            """
                            Set a material for the selected boundary type.
                            """
                            return PyMenu(self.service).execute('/display/set/colors/by_type/type_name/surface/material', *args, **kwargs)

                    class symmetry(metaclass=PyMenuMeta):
                        __doc__ = 'Set the material and/or color for the selected boundary type.'
                        def color(self, *args, **kwargs):
                            """
                            Set a color for the selected boundary type.
                            """
                            return PyMenu(self.service).execute('/display/set/colors/by_type/type_name/symmetry/color', *args, **kwargs)
                        def material(self, *args, **kwargs):
                            """
                            Set a material for the selected boundary type.
                            """
                            return PyMenu(self.service).execute('/display/set/colors/by_type/type_name/symmetry/material', *args, **kwargs)

                    class traction(metaclass=PyMenuMeta):
                        __doc__ = 'Set the material and/or color for the selected boundary type.'
                        def color(self, *args, **kwargs):
                            """
                            Set a color for the selected boundary type.
                            """
                            return PyMenu(self.service).execute('/display/set/colors/by_type/type_name/traction/color', *args, **kwargs)
                        def material(self, *args, **kwargs):
                            """
                            Set a material for the selected boundary type.
                            """
                            return PyMenu(self.service).execute('/display/set/colors/by_type/type_name/traction/material', *args, **kwargs)

                    class wall(metaclass=PyMenuMeta):
                        __doc__ = 'Set the material and/or color for the selected boundary type.'
                        def color(self, *args, **kwargs):
                            """
                            Set a color for the selected boundary type.
                            """
                            return PyMenu(self.service).execute('/display/set/colors/by_type/type_name/wall/color', *args, **kwargs)
                        def material(self, *args, **kwargs):
                            """
                            Set a material for the selected boundary type.
                            """
                            return PyMenu(self.service).execute('/display/set/colors/by_type/type_name/wall/material', *args, **kwargs)

        class picture(metaclass=PyMenuMeta):
            __doc__ = 'Hardcopy options menu.'
            def invert_background(self, *args, **kwargs):
                """
                Exchange foreground/background colors for hardcopy.
                """
                return PyMenu(self.service).execute('/display/set/picture/invert_background', *args, **kwargs)
            def landscape(self, *args, **kwargs):
                """
                Plot hardcopies in landscape or portrait orientation.
                """
                return PyMenu(self.service).execute('/display/set/picture/landscape', *args, **kwargs)
            def preview(self, *args, **kwargs):
                """
                Display a preview image of a hardcopy.
                """
                return PyMenu(self.service).execute('/display/set/picture/preview', *args, **kwargs)
            def x_resolution(self, *args, **kwargs):
                """
                Set the width of raster-formatted images in pixels (0 implies current window size).
                """
                return PyMenu(self.service).execute('/display/set/picture/x_resolution', *args, **kwargs)
            def y_resolution(self, *args, **kwargs):
                """
                Set the height of raster-formatted images in pixels (0 implies current window size).
                """
                return PyMenu(self.service).execute('/display/set/picture/y_resolution', *args, **kwargs)
            def dpi(self, *args, **kwargs):
                """
                Set the DPI for EPS and Postscript files, specifies the resolution in dots per inch (DPI) instead of setting the width and height
                """
                return PyMenu(self.service).execute('/display/set/picture/dpi', *args, **kwargs)
            def use_window_resolution(self, *args, **kwargs):
                """
                Use the currently active window's resolution for hardcopy (ignores the x-resolution and y-resolution in this case).
                """
                return PyMenu(self.service).execute('/display/set/picture/use_window_resolution', *args, **kwargs)
            def set_standard_resolution(self, *args, **kwargs):
                """
                Select from pre-defined resolution list.
                """
                return PyMenu(self.service).execute('/display/set/picture/set_standard_resolution', *args, **kwargs)
            def jpeg_hardcopy_quality(self, *args, **kwargs):
                """
                To set jpeg hardcopy quality.
                """
                return PyMenu(self.service).execute('/display/set/picture/jpeg_hardcopy_quality', *args, **kwargs)

            class color_mode(metaclass=PyMenuMeta):
                __doc__ = 'Enter the hardcopy color mode menu.'
                def color(self, *args, **kwargs):
                    """
                    Plot hardcopies in color.
                    """
                    return PyMenu(self.service).execute('/display/set/picture/color_mode/color', *args, **kwargs)
                def gray_scale(self, *args, **kwargs):
                    """
                    Convert color to grayscale for hardcopy.
                    """
                    return PyMenu(self.service).execute('/display/set/picture/color_mode/gray_scale', *args, **kwargs)
                def mono_chrome(self, *args, **kwargs):
                    """
                    Convert color to monochrome (black and white) for hardcopy.
                    """
                    return PyMenu(self.service).execute('/display/set/picture/color_mode/mono_chrome', *args, **kwargs)
                def list(self, *args, **kwargs):
                    """
                    Display the current hardcopy color mode.
                    """
                    return PyMenu(self.service).execute('/display/set/picture/color_mode/list', *args, **kwargs)

            class driver(metaclass=PyMenuMeta):
                __doc__ = 'Enter the set hardcopy driver menu.'
                def dump_window(self, *args, **kwargs):
                    """
                    Set the command used to dump the graphics window to a file.
                    """
                    return PyMenu(self.service).execute('/display/set/picture/driver/dump_window', *args, **kwargs)
                def eps(self, *args, **kwargs):
                    """
                    Produce encapsulated PostScript (EPS) output for hardcopies.
                    """
                    return PyMenu(self.service).execute('/display/set/picture/driver/eps', *args, **kwargs)
                def jpeg(self, *args, **kwargs):
                    """
                    Produce JPEG output for hardcopies.
                    """
                    return PyMenu(self.service).execute('/display/set/picture/driver/jpeg', *args, **kwargs)
                def post_script(self, *args, **kwargs):
                    """
                    Produce PostScript output for hardcopies.
                    """
                    return PyMenu(self.service).execute('/display/set/picture/driver/post_script', *args, **kwargs)
                def ppm(self, *args, **kwargs):
                    """
                    Produce PPM output for hardcopies.
                    """
                    return PyMenu(self.service).execute('/display/set/picture/driver/ppm', *args, **kwargs)
                def tiff(self, *args, **kwargs):
                    """
                    Use TIFF output for hardcopies.
                    """
                    return PyMenu(self.service).execute('/display/set/picture/driver/tiff', *args, **kwargs)
                def png(self, *args, **kwargs):
                    """
                    Use PNG output for hardcopies.
                    """
                    return PyMenu(self.service).execute('/display/set/picture/driver/png', *args, **kwargs)
                def hsf(self, *args, **kwargs):
                    """
                    Use HSF output for hardcopies.
                    """
                    return PyMenu(self.service).execute('/display/set/picture/driver/hsf', *args, **kwargs)
                def avz(self, *args, **kwargs):
                    """
                    Use AVZ output for hardcopies.
                    """
                    return PyMenu(self.service).execute('/display/set/picture/driver/avz', *args, **kwargs)
                def glb(self, *args, **kwargs):
                    """
                    Use GLB output for hardcopies.
                    """
                    return PyMenu(self.service).execute('/display/set/picture/driver/glb', *args, **kwargs)
                def vrml(self, *args, **kwargs):
                    """
                    Use VRML output for hardcopies.
                    """
                    return PyMenu(self.service).execute('/display/set/picture/driver/vrml', *args, **kwargs)
                def list(self, *args, **kwargs):
                    """
                    List the current hardcopy driver.
                    """
                    return PyMenu(self.service).execute('/display/set/picture/driver/list', *args, **kwargs)
                def options(self, *args, **kwargs):
                    """
                    Set the hardcopy options. Available options are:
                    \\n               	"no gamma correction", disables gamma correction of colors,
                    \\n               	"physical size = (width,height)", where width and height
                              are the actual measurements of the printable area of the page
                              in centimeters.
                    \\n               	"subscreen = (left,right,bottom,top)", where left,right,
                              bottom, and top are numbers in [-1,1] describing a subwindow on
                              the page in which to place the hardcopy.
                    
                    \\n          The options may be combined by separating them with commas.
                    """
                    return PyMenu(self.service).execute('/display/set/picture/driver/options', *args, **kwargs)

                class post_format(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the PostScript driver format menu.'
                    def fast_raster(self, *args, **kwargs):
                        """
                        Use the new raster format.
                        """
                        return PyMenu(self.service).execute('/display/set/picture/driver/post_format/fast_raster', *args, **kwargs)
                    def raster(self, *args, **kwargs):
                        """
                        Use the original raster format.
                        """
                        return PyMenu(self.service).execute('/display/set/picture/driver/post_format/raster', *args, **kwargs)
                    def rle_raster(self, *args, **kwargs):
                        """
                        Use the run-length encoded raster format.
                        """
                        return PyMenu(self.service).execute('/display/set/picture/driver/post_format/rle_raster', *args, **kwargs)
                    def vector(self, *args, **kwargs):
                        """
                        Use vector format.
                        """
                        return PyMenu(self.service).execute('/display/set/picture/driver/post_format/vector', *args, **kwargs)

        class lights(metaclass=PyMenuMeta):
            __doc__ = 'Lights menu.'
            def lights_on(self, *args, **kwargs):
                """
                Turn all active lighting on/off.
                """
                return PyMenu(self.service).execute('/display/set/lights/lights_on', *args, **kwargs)
            def set_ambient_color(self, *args, **kwargs):
                """
                Set the ambient light color for the scene.
                """
                return PyMenu(self.service).execute('/display/set/lights/set_ambient_color', *args, **kwargs)
            def set_light(self, *args, **kwargs):
                """
                Add or modify a directional, colored light.
                """
                return PyMenu(self.service).execute('/display/set/lights/set_light', *args, **kwargs)
            def headlight_on(self, *args, **kwargs):
                """
                Turn the light that moves with the camera on or off.
                """
                return PyMenu(self.service).execute('/display/set/lights/headlight_on', *args, **kwargs)

            class lighting_interpolation(metaclass=PyMenuMeta):
                __doc__ = 'Set lighting interpolation method.'
                def automatic(self, *args, **kwargs):
                    """
                    Choose Automatic to automatically select the best lighting method for a given graphics object.
                    """
                    return PyMenu(self.service).execute('/display/set/lights/lighting_interpolation/automatic', *args, **kwargs)
                def flat(self, *args, **kwargs):
                    """
                    Use flat shading for meshes and polygons.
                    """
                    return PyMenu(self.service).execute('/display/set/lights/lighting_interpolation/flat', *args, **kwargs)
                def gouraud(self, *args, **kwargs):
                    """
                    Use Gouraud shading to calculate the color at each vertex of a polygon and interpolate it in the interior.
                    """
                    return PyMenu(self.service).execute('/display/set/lights/lighting_interpolation/gouraud', *args, **kwargs)
                def phong(self, *args, **kwargs):
                    """
                    Use Phong shading to interpolate the normals for each pixel of a polygon and compute a color at every pixel.
                    """
                    return PyMenu(self.service).execute('/display/set/lights/lighting_interpolation/phong', *args, **kwargs)

        class rendering_options(metaclass=PyMenuMeta):
            __doc__ = 'Rendering options menu'
            def auto_spin(self, *args, **kwargs):
                """
                Enable/disable mouse view rotations to continue to spin the display after the button is released.
                """
                return PyMenu(self.service).execute('/display/set/rendering_options/auto_spin', *args, **kwargs)
            def device_info(self, *args, **kwargs):
                """
                List information for the graphics device.
                """
                return PyMenu(self.service).execute('/display/set/rendering_options/device_info', *args, **kwargs)
            def double_buffering(self, *args, **kwargs):
                """
                Enable/disable double-buffering.
                """
                return PyMenu(self.service).execute('/display/set/rendering_options/double_buffering', *args, **kwargs)
            def driver(self, *args, **kwargs):
                """
                Change the current graphics driver.
                """
                return PyMenu(self.service).execute('/display/set/rendering_options/driver', *args, **kwargs)
            def hidden_surfaces(self, *args, **kwargs):
                """
                Enable/disable hidden surface removal.
                """
                return PyMenu(self.service).execute('/display/set/rendering_options/hidden_surfaces', *args, **kwargs)
            def hidden_surface_method(self, *args, **kwargs):
                """
                Specify the method to perform hidden line and hidden surface rendering.
                """
                return PyMenu(self.service).execute('/display/set/rendering_options/hidden_surface_method', *args, **kwargs)
            def outer_face_cull(self, *args, **kwargs):
                """
                Enable/disable discarding outer faces during display.
                """
                return PyMenu(self.service).execute('/display/set/rendering_options/outer_face_cull', *args, **kwargs)
            def surface_edge_visibility(self, *args, **kwargs):
                """
                Set edge visibility flags for surfaces.
                """
                return PyMenu(self.service).execute('/display/set/rendering_options/surface_edge_visibility', *args, **kwargs)
            def animation_option(self, *args, **kwargs):
                """
                Using Wireframe / All option during animation
                """
                return PyMenu(self.service).execute('/display/set/rendering_options/animation_option', *args, **kwargs)
            def color_map_alignment(self, *args, **kwargs):
                """
                Set the color bar alignment.
                """
                return PyMenu(self.service).execute('/display/set/rendering_options/color_map_alignment', *args, **kwargs)
            def help_text_color(self, *args, **kwargs):
                """
                Set the color of screen help text.
                """
                return PyMenu(self.service).execute('/display/set/rendering_options/help_text_color', *args, **kwargs)
            def face_displacement(self, *args, **kwargs):
                """
                Set face displacement value in Z-buffer units along the Camera Z-axis.
                """
                return PyMenu(self.service).execute('/display/set/rendering_options/face_displacement', *args, **kwargs)
            def set_rendering_options(self, *args, **kwargs):
                """
                Set the rendering options.
                """
                return PyMenu(self.service).execute('/display/set/rendering_options/set_rendering_options', *args, **kwargs)
            def show_colormap(self, *args, **kwargs):
                """
                Enable/Disable colormap.
                """
                return PyMenu(self.service).execute('/display/set/rendering_options/show_colormap', *args, **kwargs)

        class styles(metaclass=PyMenuMeta):
            __doc__ = 'Display style menu.'
            def cell_quality(self, *args, **kwargs):
                """
                Set the display attributes of the cell-quality style.
                """
                return PyMenu(self.service).execute('/display/set/styles/cell_quality', *args, **kwargs)
            def cell_size(self, *args, **kwargs):
                """
                Set the display attributes of the cell-size style.
                """
                return PyMenu(self.service).execute('/display/set/styles/cell_size', *args, **kwargs)
            def dummy(self, *args, **kwargs):
                """
                """
                return PyMenu(self.service).execute('/display/set/styles/dummy', *args, **kwargs)
            def face_quality(self, *args, **kwargs):
                """
                Set the display attributes of the face-quality style.
                """
                return PyMenu(self.service).execute('/display/set/styles/face_quality', *args, **kwargs)
            def face_size(self, *args, **kwargs):
                """
                Set the display attributes of the face-size style.
                """
                return PyMenu(self.service).execute('/display/set/styles/face_size', *args, **kwargs)
            def free(self, *args, **kwargs):
                """
                Set the display attributes of the free style.
                """
                return PyMenu(self.service).execute('/display/set/styles/free', *args, **kwargs)
            def left_handed(self, *args, **kwargs):
                """
                Set the display attributes of the left-handed style.
                """
                return PyMenu(self.service).execute('/display/set/styles/left_handed', *args, **kwargs)
            def mark(self, *args, **kwargs):
                """
                Set the display attributes of the mark style.
                """
                return PyMenu(self.service).execute('/display/set/styles/mark', *args, **kwargs)
            def multi(self, *args, **kwargs):
                """
                Set the display attributes of the multi style.
                """
                return PyMenu(self.service).execute('/display/set/styles/multi', *args, **kwargs)
            def refine(self, *args, **kwargs):
                """
                Set the display attributes of the refine style.
                """
                return PyMenu(self.service).execute('/display/set/styles/refine', *args, **kwargs)
            def tag(self, *args, **kwargs):
                """
                Set the display attributes of the tag style.
                """
                return PyMenu(self.service).execute('/display/set/styles/tag', *args, **kwargs)
            def unmeshed(self, *args, **kwargs):
                """
                Set the display attributes of the unmeshed style.
                """
                return PyMenu(self.service).execute('/display/set/styles/unmeshed', *args, **kwargs)
            def unused(self, *args, **kwargs):
                """
                Set the display attributes of the unused style.
                """
                return PyMenu(self.service).execute('/display/set/styles/unused', *args, **kwargs)

        class windows(metaclass=PyMenuMeta):
            __doc__ = 'Window options menu.'
            def aspect_ratio(self, *args, **kwargs):
                """
                Set the aspect ratio of the active window.
                """
                return PyMenu(self.service).execute('/display/set/windows/aspect_ratio', *args, **kwargs)
            def logo(self, *args, **kwargs):
                """
                Enable/disable visibility of the logo in graphics window.
                """
                return PyMenu(self.service).execute('/display/set/windows/logo', *args, **kwargs)
            def ruler(self, *args, **kwargs):
                """
                Enable/disable ruler visibility.
                """
                return PyMenu(self.service).execute('/display/set/windows/ruler', *args, **kwargs)
            def logo_color(self, *args, **kwargs):
                """
                Set logo color to white/black.
                """
                return PyMenu(self.service).execute('/display/set/windows/logo_color', *args, **kwargs)

            class axes(metaclass=PyMenuMeta):
                __doc__ = 'Enter the axes window options menu.'
                def border(self, *args, **kwargs):
                    """
                    Enable/disable drawing of a border around the axes window.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/axes/border', *args, **kwargs)
                def bottom(self, *args, **kwargs):
                    """
                    Set the bottom boundary of the axes window.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/axes/bottom', *args, **kwargs)
                def clear(self, *args, **kwargs):
                    """
                    Set the transparency of the axes window.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/axes/clear', *args, **kwargs)
                def right(self, *args, **kwargs):
                    """
                    Set the right boundary of the axes window.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/axes/right', *args, **kwargs)
                def visible(self, *args, **kwargs):
                    """
                    Enable/disable axes visibility.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/axes/visible', *args, **kwargs)

            class main(metaclass=PyMenuMeta):
                __doc__ = 'Enter the main view window options menu.'
                def border(self, *args, **kwargs):
                    """
                    Enable/disable drawing of borders around the main viewing window.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/main/border', *args, **kwargs)
                def bottom(self, *args, **kwargs):
                    """
                    Set the bottom boundary of the main viewing window.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/main/bottom', *args, **kwargs)
                def left(self, *args, **kwargs):
                    """
                    Set the left boundary of the main viewing window.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/main/left', *args, **kwargs)
                def right(self, *args, **kwargs):
                    """
                    Set the right boundary of the main viewing window.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/main/right', *args, **kwargs)
                def top(self, *args, **kwargs):
                    """
                    Set the top boundary of the main viewing window.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/main/top', *args, **kwargs)
                def visible(self, *args, **kwargs):
                    """
                    Enable/disable visibility of the main viewing window.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/main/visible', *args, **kwargs)

            class scale(metaclass=PyMenuMeta):
                __doc__ = 'Enter the color scale window options menu.'
                def border(self, *args, **kwargs):
                    """
                    Enable/disable drawing of borders around the color scale window.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/scale/border', *args, **kwargs)
                def bottom(self, *args, **kwargs):
                    """
                    Set the bottom boundary of the color scale window.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/scale/bottom', *args, **kwargs)
                def clear(self, *args, **kwargs):
                    """
                    Set the transparency of the scale window.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/scale/clear', *args, **kwargs)
                def format(self, *args, **kwargs):
                    """
                    Set the number format of the color scale window (e.g. %0.2e).
                    """
                    return PyMenu(self.service).execute('/display/set/windows/scale/format', *args, **kwargs)
                def font_size(self, *args, **kwargs):
                    """
                    Set the font size of the color scale window.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/scale/font_size', *args, **kwargs)
                def left(self, *args, **kwargs):
                    """
                    Set the left boundary of the color scale window.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/scale/left', *args, **kwargs)
                def margin(self, *args, **kwargs):
                    """
                    Set the margin of the color scale window.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/scale/margin', *args, **kwargs)
                def right(self, *args, **kwargs):
                    """
                    Set the right boundary of the color scale window.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/scale/right', *args, **kwargs)
                def top(self, *args, **kwargs):
                    """
                    Set the top boundary of the color scale window.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/scale/top', *args, **kwargs)
                def visible(self, *args, **kwargs):
                    """
                    Enable/disable visibility of the color scale window.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/scale/visible', *args, **kwargs)
                def alignment(self, *args, **kwargs):
                    """
                    Set colormap to bottom/left/top/right
                    """
                    return PyMenu(self.service).execute('/display/set/windows/scale/alignment', *args, **kwargs)

            class text(metaclass=PyMenuMeta):
                __doc__ = 'Enter the text window options menu.'
                def application(self, *args, **kwargs):
                    """
                    Enable/disable the application name in the picture.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/text/application', *args, **kwargs)
                def border(self, *args, **kwargs):
                    """
                    Enable/disable drawing of borders around the text window.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/text/border', *args, **kwargs)
                def bottom(self, *args, **kwargs):
                    """
                    Set the bottom boundary of the text window.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/text/bottom', *args, **kwargs)
                def clear(self, *args, **kwargs):
                    """
                    Enable/disable text window transparency.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/text/clear', *args, **kwargs)
                def company(self, *args, **kwargs):
                    """
                    Enable/disable the company name in the picture.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/text/company', *args, **kwargs)
                def date(self, *args, **kwargs):
                    """
                    Enable/disable the date in the picture.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/text/date', *args, **kwargs)
                def left(self, *args, **kwargs):
                    """
                    Set the left boundary of the text window.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/text/left', *args, **kwargs)
                def right(self, *args, **kwargs):
                    """
                    Set the right boundary of the text window.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/text/right', *args, **kwargs)
                def top(self, *args, **kwargs):
                    """
                    Set the top boundary of the text window.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/text/top', *args, **kwargs)
                def visible(self, *args, **kwargs):
                    """
                    Enable/disable text window transparency.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/text/visible', *args, **kwargs)

            class video(metaclass=PyMenuMeta):
                __doc__ = 'Enter the video window options menu.'
                def background(self, *args, **kwargs):
                    """
                    Set the background color in the video picture.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/video/background', *args, **kwargs)
                def color_filter(self, *args, **kwargs):
                    """
                    Set the color filter options for the picture.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/video/color_filter', *args, **kwargs)
                def foreground(self, *args, **kwargs):
                    """
                    Set the foreground color in the video picture.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/video/foreground', *args, **kwargs)
                def on(self, *args, **kwargs):
                    """
                    Enable/disable video picture settings.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/video/on', *args, **kwargs)
                def pixel_size(self, *args, **kwargs):
                    """
                    Set the window size in pixels.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/video/pixel_size', *args, **kwargs)

            class xy(metaclass=PyMenuMeta):
                __doc__ = 'Enter the X-Y plot window options menu.'
                def border(self, *args, **kwargs):
                    """
                    Enable/disable drawing of a border around the X-Y plotter window.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/xy/border', *args, **kwargs)
                def bottom(self, *args, **kwargs):
                    """
                    Set the bottom boundary of the X-Y plotter window.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/xy/bottom', *args, **kwargs)
                def left(self, *args, **kwargs):
                    """
                    Set the left boundary of the X-Y plotter window.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/xy/left', *args, **kwargs)
                def right(self, *args, **kwargs):
                    """
                    Set the right boundary of the X-Y plotter window.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/xy/right', *args, **kwargs)
                def top(self, *args, **kwargs):
                    """
                    Set the top boundary of the X-Y plotter window.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/xy/top', *args, **kwargs)
                def visible(self, *args, **kwargs):
                    """
                    Enable/disable X-Y plotter window visibility.
                    """
                    return PyMenu(self.service).execute('/display/set/windows/xy/visible', *args, **kwargs)

    class set_grid(metaclass=PyMenuMeta):
        __doc__ = 'Enter the set-grid menu'
        def all_cells(self, *args, **kwargs):
            """
            Draw all elements in cell zones.
            """
            return PyMenu(self.service).execute('/display/set_grid/all_cells', *args, **kwargs)
        def all_faces(self, *args, **kwargs):
            """
            Draw all elements in face zones.
            """
            return PyMenu(self.service).execute('/display/set_grid/all_faces', *args, **kwargs)
        def all_nodes(self, *args, **kwargs):
            """
            Draw all elements in node zones.
            """
            return PyMenu(self.service).execute('/display/set_grid/all_nodes', *args, **kwargs)
        def free(self, *args, **kwargs):
            """
            Draw free elements.
            """
            return PyMenu(self.service).execute('/display/set_grid/free', *args, **kwargs)
        def left_handed(self, *args, **kwargs):
            """
            Draw left-handed elements.
            """
            return PyMenu(self.service).execute('/display/set_grid/left_handed', *args, **kwargs)
        def multi(self, *args, **kwargs):
            """
            Draw multiply-connected elements.
            """
            return PyMenu(self.service).execute('/display/set_grid/multi', *args, **kwargs)
        def refine(self, *args, **kwargs):
            """
            Draw refine marked elements.
            """
            return PyMenu(self.service).execute('/display/set_grid/refine', *args, **kwargs)
        def unmeshed(self, *args, **kwargs):
            """
            Draw unmeshed elements.
            """
            return PyMenu(self.service).execute('/display/set_grid/unmeshed', *args, **kwargs)
        def unused(self, *args, **kwargs):
            """
            Draw unused nodes.
            """
            return PyMenu(self.service).execute('/display/set_grid/unused', *args, **kwargs)
        def marked(self, *args, **kwargs):
            """
            Draw marked elements.
            """
            return PyMenu(self.service).execute('/display/set_grid/marked', *args, **kwargs)
        def tagged(self, *args, **kwargs):
            """
            Draw tagged elements.
            """
            return PyMenu(self.service).execute('/display/set_grid/tagged', *args, **kwargs)
        def face_quality(self, *args, **kwargs):
            """
            Draw faces only in specified quality range.
            """
            return PyMenu(self.service).execute('/display/set_grid/face_quality', *args, **kwargs)
        def cell_quality(self, *args, **kwargs):
            """
            Draw cells only in specified quality range.
            """
            return PyMenu(self.service).execute('/display/set_grid/cell_quality', *args, **kwargs)
        def neighborhood(self, *args, **kwargs):
            """
            Set display bounds to draw entities in the neighborhood of a entity.
            """
            return PyMenu(self.service).execute('/display/set_grid/neighborhood', *args, **kwargs)
        def x_range(self, *args, **kwargs):
            """
            Draw only entities with x coordinates in specified range.
            """
            return PyMenu(self.service).execute('/display/set_grid/x_range', *args, **kwargs)
        def y_range(self, *args, **kwargs):
            """
            Draw only entities with y coordinates in specified range.
            """
            return PyMenu(self.service).execute('/display/set_grid/y_range', *args, **kwargs)
        def z_range(self, *args, **kwargs):
            """
            Draw only entities with z coordinates in specified range.
            """
            return PyMenu(self.service).execute('/display/set_grid/z_range', *args, **kwargs)
        def normals(self, *args, **kwargs):
            """
            Turn on/off face normals.
            """
            return PyMenu(self.service).execute('/display/set_grid/normals', *args, **kwargs)
        def normal_scale(self, *args, **kwargs):
            """
            Face normal scale.
            """
            return PyMenu(self.service).execute('/display/set_grid/normal_scale', *args, **kwargs)
        def labels(self, *args, **kwargs):
            """
            Turn on/off labeling.
            """
            return PyMenu(self.service).execute('/display/set_grid/labels', *args, **kwargs)
        def label_alignment(self, *args, **kwargs):
            """
            Set label alignment; chose from "^v<>*".
            """
            return PyMenu(self.service).execute('/display/set_grid/label_alignment', *args, **kwargs)
        def label_font(self, *args, **kwargs):
            """
            Set label font.
            """
            return PyMenu(self.service).execute('/display/set_grid/label_font', *args, **kwargs)
        def label_scale(self, *args, **kwargs):
            """
            Set label scale.
            """
            return PyMenu(self.service).execute('/display/set_grid/label_scale', *args, **kwargs)
        def node_size(self, *args, **kwargs):
            """
            Set node symbol scaling factor.
            """
            return PyMenu(self.service).execute('/display/set_grid/node_size', *args, **kwargs)
        def node_symbol(self, *args, **kwargs):
            """
            Set node symbol.
            """
            return PyMenu(self.service).execute('/display/set_grid/node_symbol', *args, **kwargs)
        def list(self, *args, **kwargs):
            """
            List display variables.
            """
            return PyMenu(self.service).execute('/display/set_grid/list', *args, **kwargs)
        def default(self, *args, **kwargs):
            """
            Reset all display variables to their default value.
            """
            return PyMenu(self.service).execute('/display/set_grid/default', *args, **kwargs)

    class views(metaclass=PyMenuMeta):
        __doc__ = 'Enter the view menu.'
        def auto_scale(self, *args, **kwargs):
            """
            Scale and center the current scene.
            """
            return PyMenu(self.service).execute('/display/views/auto_scale', *args, **kwargs)
        def default_view(self, *args, **kwargs):
            """
            Reset view to front and center.
            """
            return PyMenu(self.service).execute('/display/views/default_view', *args, **kwargs)
        def delete_view(self, *args, **kwargs):
            """
            Remove a view from the list.
            """
            return PyMenu(self.service).execute('/display/views/delete_view', *args, **kwargs)
        def last_view(self, *args, **kwargs):
            """
            Return to the camera position before the last manipulation.
            """
            return PyMenu(self.service).execute('/display/views/last_view', *args, **kwargs)
        def next_view(self, *args, **kwargs):
            """
            Return to the camera position after the current position in the stack.
            """
            return PyMenu(self.service).execute('/display/views/next_view', *args, **kwargs)
        def list_views(self, *args, **kwargs):
            """
            List predefined and saved views.
            """
            return PyMenu(self.service).execute('/display/views/list_views', *args, **kwargs)
        def restore_view(self, *args, **kwargs):
            """
            Use a saved view.
            """
            return PyMenu(self.service).execute('/display/views/restore_view', *args, **kwargs)
        def read_views(self, *args, **kwargs):
            """
            Read views from a view file.
            """
            return PyMenu(self.service).execute('/display/views/read_views', *args, **kwargs)
        def save_view(self, *args, **kwargs):
            """
            Save the current view to the view list.
            """
            return PyMenu(self.service).execute('/display/views/save_view', *args, **kwargs)
        def write_views(self, *args, **kwargs):
            """
            Write selected views to a view file.
            """
            return PyMenu(self.service).execute('/display/views/write_views', *args, **kwargs)

        class camera(metaclass=PyMenuMeta):
            __doc__ = 'Enter the camera menu to modify the current viewing parameters.'
            def dolly_camera(self, *args, **kwargs):
                """
                Adjust the camera position and target.
                """
                return PyMenu(self.service).execute('/display/views/camera/dolly_camera', *args, **kwargs)
            def field(self, *args, **kwargs):
                """
                Set the field of view (width and height).
                """
                return PyMenu(self.service).execute('/display/views/camera/field', *args, **kwargs)
            def orbit_camera(self, *args, **kwargs):
                """
                Adjust the camera position without modifying the target.
                """
                return PyMenu(self.service).execute('/display/views/camera/orbit_camera', *args, **kwargs)
            def pan_camera(self, *args, **kwargs):
                """
                Adjust the camera target without modifying the position.
                """
                return PyMenu(self.service).execute('/display/views/camera/pan_camera', *args, **kwargs)
            def position(self, *args, **kwargs):
                """
                Set the camera position.
                """
                return PyMenu(self.service).execute('/display/views/camera/position', *args, **kwargs)
            def projection(self, *args, **kwargs):
                """
                Set the camera projection type.
                """
                return PyMenu(self.service).execute('/display/views/camera/projection', *args, **kwargs)
            def roll_camera(self, *args, **kwargs):
                """
                Adjust the camera up-vector.
                """
                return PyMenu(self.service).execute('/display/views/camera/roll_camera', *args, **kwargs)
            def target(self, *args, **kwargs):
                """
                Set the point to be the center of the camera view.
                """
                return PyMenu(self.service).execute('/display/views/camera/target', *args, **kwargs)
            def up_vector(self, *args, **kwargs):
                """
                Set the camera up-vector.
                """
                return PyMenu(self.service).execute('/display/views/camera/up_vector', *args, **kwargs)
            def zoom_camera(self, *args, **kwargs):
                """
                Adjust the camera field of view.
                """
                return PyMenu(self.service).execute('/display/views/camera/zoom_camera', *args, **kwargs)

    class display_states(metaclass=PyMenuMeta):
        __doc__ = 'Enter the display state menu.'
        def list(self, *args, **kwargs):
            """
            Print the names of the available display states to the console.
            """
            return PyMenu(self.service).execute('/display/display_states/list', *args, **kwargs)
        def apply(self, *args, **kwargs):
            """
            Apply a display state to the active window.
            """
            return PyMenu(self.service).execute('/display/display_states/apply', *args, **kwargs)
        def delete(self, *args, **kwargs):
            """
            Delete a display state.
            """
            return PyMenu(self.service).execute('/display/display_states/delete', *args, **kwargs)
        def use_active(self, *args, **kwargs):
            """
            Update an existing display state's settings to match those of the active graphics window.
            """
            return PyMenu(self.service).execute('/display/display_states/use_active', *args, **kwargs)
        def copy(self, *args, **kwargs):
            """
            Create a new display state with settings copied from an existing display state.
            """
            return PyMenu(self.service).execute('/display/display_states/copy', *args, **kwargs)
        def read(self, *args, **kwargs):
            """
            Read display states from a file.
            """
            return PyMenu(self.service).execute('/display/display_states/read', *args, **kwargs)
        def write(self, *args, **kwargs):
            """
            Write display states to a file.
            """
            return PyMenu(self.service).execute('/display/display_states/write', *args, **kwargs)
        def edit(self, *args, **kwargs):
            """
            Edit a particular display state setting.
            """
            return PyMenu(self.service).execute('/display/display_states/edit', *args, **kwargs)
        def create(self, *args, **kwargs):
            """
            Create a new display state.
            """
            return PyMenu(self.service).execute('/display/display_states/create', *args, **kwargs)

    class xy_plot(metaclass=PyMenuMeta):
        __doc__ = 'Enter X-Y plot menu.'
        def file(self, *args, **kwargs):
            """
            Over-plot data from file.
            """
            return PyMenu(self.service).execute('/display/xy_plot/file', *args, **kwargs)
        def cell_distribution(self, *args, **kwargs):
            """
            Display chart of distribution of cell quality.
            """
            return PyMenu(self.service).execute('/display/xy_plot/cell_distribution', *args, **kwargs)
        def face_distribution(self, *args, **kwargs):
            """
            Display chart of distribution of face quality.
            """
            return PyMenu(self.service).execute('/display/xy_plot/face_distribution', *args, **kwargs)
        def set(self, *args, **kwargs):
            """
            Set histogram plot parameters.
            """
            return PyMenu(self.service).execute('/display/xy_plot/set', *args, **kwargs)

    class update_scene(metaclass=PyMenuMeta):
        __doc__ = 'Enter the scene options menu.'
        def select_geometry(self, *args, **kwargs):
            """
            Select geometry to be updated.
            """
            return PyMenu(self.service).execute('/display/update_scene/select_geometry', *args, **kwargs)
        def overlays(self, *args, **kwargs):
            """
            Enable/disable the overlays option.
            """
            return PyMenu(self.service).execute('/display/update_scene/overlays', *args, **kwargs)
        def draw_frame(self, *args, **kwargs):
            """
            Enable/disable drawing of the bounding frame.
            """
            return PyMenu(self.service).execute('/display/update_scene/draw_frame', *args, **kwargs)
        def delete(self, *args, **kwargs):
            """
            Delete selected geometries.
            """
            return PyMenu(self.service).execute('/display/update_scene/delete', *args, **kwargs)
        def display(self, *args, **kwargs):
            """
            Display selected geometries.
            """
            return PyMenu(self.service).execute('/display/update_scene/display', *args, **kwargs)
        def transform(self, *args, **kwargs):
            """
            Apply transformation matrix on selected geometries.
            """
            return PyMenu(self.service).execute('/display/update_scene/transform', *args, **kwargs)
        def pathline(self, *args, **kwargs):
            """
            Change pathline attributes.
            """
            return PyMenu(self.service).execute('/display/update_scene/pathline', *args, **kwargs)
        def iso_sweep(self, *args, **kwargs):
            """
            Change iso-sweep values.
            """
            return PyMenu(self.service).execute('/display/update_scene/iso_sweep', *args, **kwargs)
        def time(self, *args, **kwargs):
            """
            Change time-step value.
            """
            return PyMenu(self.service).execute('/display/update_scene/time', *args, **kwargs)
        def set_frame(self, *args, **kwargs):
            """
            Change frame options.
            """
            return PyMenu(self.service).execute('/display/update_scene/set_frame', *args, **kwargs)

    class objects(metaclass=PyMenuMeta):
        __doc__ = 'Enter the objects menu.'
        is_extended_tui = True
        def show_all(self, *args, **kwargs):
            """
            Show all displayed objects.
            """
            return PyMenu(self.service).execute('/display/objects/show_all', *args, **kwargs)
        def explode(self, *args, **kwargs):
            """
            Explode all displayed objects.
            """
            return PyMenu(self.service).execute('/display/objects/explode', *args, **kwargs)
        def toggle_color_palette(self, *args, **kwargs):
            """
            Toggle between default and classic color palettes.
            """
            return PyMenu(self.service).execute('/display/objects/toggle_color_palette', *args, **kwargs)
        def implode(self, *args, **kwargs):
            """
            Implode all displayed objects.
            """
            return PyMenu(self.service).execute('/display/objects/implode', *args, **kwargs)
        def display_similar_area(self, *args, **kwargs):
            """
            Shows all similar surface area objects.
            """
            return PyMenu(self.service).execute('/display/objects/display_similar_area', *args, **kwargs)
        def toggle_color_mode(self, *args, **kwargs):
            """
            Toggles color mode between color by objects/threads.
            """
            return PyMenu(self.service).execute('/display/objects/toggle_color_mode', *args, **kwargs)
        def make_transparent(self, *args, **kwargs):
            """
            Toggle Transparent view based on object selection.
            """
            return PyMenu(self.service).execute('/display/objects/make_transparent', *args, **kwargs)
        def select_all_visible(self, *args, **kwargs):
            """
            Probe select all visible objects.
            """
            return PyMenu(self.service).execute('/display/objects/select_all_visible', *args, **kwargs)
        def display_neighborhood(self, *args, **kwargs):
            """
            Displays neighboring objects also.
            """
            return PyMenu(self.service).execute('/display/objects/display_neighborhood', *args, **kwargs)
        def hide_objects(self, *args, **kwargs):
            """
            Hide selected objects from view.
            """
            return PyMenu(self.service).execute('/display/objects/hide_objects', *args, **kwargs)
        def isolate_objects(self, *args, **kwargs):
            """
            Hide selected objects from view.
            """
            return PyMenu(self.service).execute('/display/objects/isolate_objects', *args, **kwargs)

        class xy_plot(metaclass=PyNamedObjectMeta):
            __doc__ = ''
            is_extended_tui = True

            class name(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class uid(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class options(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

                class node_values(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class position_on_x_axis(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class position_on_y_axis(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

            class plot_direction(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

                class direction_vector(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                    class x_component(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class y_component(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class z_component(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                class curve_length(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                    class default(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class reverse(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

            class x_axis_function(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class y_axis_function(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class surfaces_list(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class physics(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class geometry(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class surfaces(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

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

            class physics(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class geometry(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class surfaces(metaclass=PyMenuMeta):
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

            class physics(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class geometry(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class surfaces(metaclass=PyMenuMeta):
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

            class physics(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class geometry(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class surfaces(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

        class pathlines(metaclass=PyNamedObjectMeta):
            __doc__ = ''
            is_extended_tui = True

            class name(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class uid(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class options(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

                class oil_flow(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class reverse(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class node_values(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class relative(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

            class range(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

                class auto_range(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class clip_to_range(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                    class min_value(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class max_value(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

            class style_attribute(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

                class style(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class line_width(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class arrow_space(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class arrow_scale(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class marker_size(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class sphere_size(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class sphere_lod(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class radius(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class ribbon(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                    class field(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class scalefactor(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

            class accuracy_control(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

                class step_size(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class tolerance(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

            class plot(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

                class x_axis_function(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class enabled(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

            class step(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class skip(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class coarsen(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class onzone(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class field(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class surfaces_list(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class velocity_domain(metaclass=PyMenuMeta):
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

            class physics(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class geometry(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class surfaces(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

        class particle_tracks(metaclass=PyNamedObjectMeta):
            __doc__ = ''
            is_extended_tui = True

            class name(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class uid(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class options(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

                class node_values(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

            class filter_settings(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

                class field(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class options(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                    class inside(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class outside(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                class enabled(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class filter_minimum(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class filter_maximum(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

            class range(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

                class auto_range(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class clip_to_range(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                    class min_value(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class max_value(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

            class style_attribute(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

                class style(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class line_width(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class arrow_space(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class arrow_scale(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class marker_size(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class sphere_size(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class sphere_lod(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class radius(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class ribbon_settings(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                    class field(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class scalefactor(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                class sphere_settings(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                    class scale(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class sphere_lod(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class options(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                        class constant(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                            class diameter(metaclass=PyMenuMeta):
                                __doc__ = ''
                                is_extended_tui = True

                        class variable(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                            class size_by(metaclass=PyMenuMeta):
                                __doc__ = ''
                                is_extended_tui = True

                            class range(metaclass=PyMenuMeta):
                                __doc__ = ''
                                is_extended_tui = True

                                class auto_range(metaclass=PyMenuMeta):
                                    __doc__ = ''
                                    is_extended_tui = True

                                class clip_to_range(metaclass=PyMenuMeta):
                                    __doc__ = ''
                                    is_extended_tui = True

                                    class min_value(metaclass=PyMenuMeta):
                                        __doc__ = ''
                                        is_extended_tui = True

                                    class max_value(metaclass=PyMenuMeta):
                                        __doc__ = ''
                                        is_extended_tui = True

            class vector_settings(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

                class style(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class vector_length(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                    class constant_length(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class variable_length(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                class constant_color(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                    class enabled(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class color(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                class vector_of(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class scale(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class length_to_head_ratio(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

            class plot(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

                class x_axis_function(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class enabled(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

            class track_single_particle_stream(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

                class enabled(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class stream_id(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

            class skip(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class coarsen(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class field(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class injections_list(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class free_stream_particles(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class wall_film_particles(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class track_pdf_particles(metaclass=PyMenuMeta):
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

        class scene(metaclass=PyNamedObjectMeta):
            __doc__ = ''
            is_extended_tui = True

            class name(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class title(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class temporary(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

            class display_state_name(metaclass=PyMenuMeta):
                __doc__ = ''
                is_extended_tui = True

    class zones(metaclass=PyMenuMeta):
        __doc__ = 'Enter the zones menu.'
        def show_all(self, *args, **kwargs):
            """
            Show all displayed objects.
            """
            return PyMenu(self.service).execute('/display/zones/show_all', *args, **kwargs)
        def toggle_color_palette(self, *args, **kwargs):
            """
            Toggle between default and classic color palettes.
            """
            return PyMenu(self.service).execute('/display/zones/toggle_color_palette', *args, **kwargs)
        def display_similar_area(self, *args, **kwargs):
            """
            Shows all similar surface area objects.
            """
            return PyMenu(self.service).execute('/display/zones/display_similar_area', *args, **kwargs)
        def toggle_color_mode(self, *args, **kwargs):
            """
            Toggles color mode between color by objects/threads.
            """
            return PyMenu(self.service).execute('/display/zones/toggle_color_mode', *args, **kwargs)
        def make_transparent(self, *args, **kwargs):
            """
            Toggle Transparent view based on object selection.
            """
            return PyMenu(self.service).execute('/display/zones/make_transparent', *args, **kwargs)
        def select_all_visible(self, *args, **kwargs):
            """
            Probe select all visible objects.
            """
            return PyMenu(self.service).execute('/display/zones/select_all_visible', *args, **kwargs)
        def display_neighborhood(self, *args, **kwargs):
            """
            Displays neighboring objects also.
            """
            return PyMenu(self.service).execute('/display/zones/display_neighborhood', *args, **kwargs)
        def hide_zones(self, *args, **kwargs):
            """
            Hide selected objects from view.
            """
            return PyMenu(self.service).execute('/display/zones/hide_zones', *args, **kwargs)
        def isolate_zones(self, *args, **kwargs):
            """
            Hide selected objects from view.
            """
            return PyMenu(self.service).execute('/display/zones/isolate_zones', *args, **kwargs)

    class advanced_rendering(metaclass=PyMenuMeta):
        __doc__ = 'Enter the advanced rendering menu.'
        def max_extent_culling(self, *args, **kwargs):
            """
            Truncates zones smaller that the maximum extent culling pixel value.
            """
            return PyMenu(self.service).execute('/display/advanced_rendering/max_extent_culling', *args, **kwargs)
        def static_model(self, *args, **kwargs):
            """
            Static model driver setting.
            """
            return PyMenu(self.service).execute('/display/advanced_rendering/static_model', *args, **kwargs)
        def simple_shadow(self, *args, **kwargs):
            """
            Enhances viewability by adding a simple shadow.
            """
            return PyMenu(self.service).execute('/display/advanced_rendering/simple_shadow', *args, **kwargs)
        def fast_silhouette_edges(self, *args, **kwargs):
            """
            Enhances viewability by adding fast silhouette edges.
            """
            return PyMenu(self.service).execute('/display/advanced_rendering/fast_silhouette_edges', *args, **kwargs)
        def edge_color(self, *args, **kwargs):
            """
            choose between black and body colored edges.
            """
            return PyMenu(self.service).execute('/display/advanced_rendering/edge_color', *args, **kwargs)

class report(metaclass=PyMenuMeta):
    __doc__ = 'Enter the report menu'
    def face_node_degree_distribution(self, *args, **kwargs):
        """
        Report face node degree of boundary faces
        """
        return PyMenu(self.service).execute('/report/face_node_degree_distribution', *args, **kwargs)
    def boundary_cell_quality(self, *args, **kwargs):
        """
        Report quality of boundary cells.
        """
        return PyMenu(self.service).execute('/report/boundary_cell_quality', *args, **kwargs)
    def cell_distribution(self, *args, **kwargs):
        """
        Report distribution of cell quality.
        """
        return PyMenu(self.service).execute('/report/cell_distribution', *args, **kwargs)
    def face_distribution(self, *args, **kwargs):
        """
        Reports the distribution of face quality.
        """
        return PyMenu(self.service).execute('/report/face_distribution', *args, **kwargs)
    def cell_zone_volume(self, *args, **kwargs):
        """
        Report volume of a cell zone.
        """
        return PyMenu(self.service).execute('/report/cell_zone_volume', *args, **kwargs)
    def cell_zone_at_location(self, *args, **kwargs):
        """
        Report cell zone at given location.
        """
        return PyMenu(self.service).execute('/report/cell_zone_at_location', *args, **kwargs)
    def face_zone_at_location(self, *args, **kwargs):
        """
        Report face zone at given location.
        """
        return PyMenu(self.service).execute('/report/face_zone_at_location', *args, **kwargs)
    def number_meshed(self, *args, **kwargs):
        """
        Report number of nodes and faces that have been meshed.
        """
        return PyMenu(self.service).execute('/report/number_meshed', *args, **kwargs)
    def list_cell_quality(self, *args, **kwargs):
        """
        List cells between quality limits.
        """
        return PyMenu(self.service).execute('/report/list_cell_quality', *args, **kwargs)
    def mesh_size(self, *args, **kwargs):
        """
        Report number of each type of grid object.
        """
        return PyMenu(self.service).execute('/report/mesh_size', *args, **kwargs)
    def mesh_statistics(self, *args, **kwargs):
        """
        Write vital mesh statistics to file.
        """
        return PyMenu(self.service).execute('/report/mesh_statistics', *args, **kwargs)
    def meshing_time(self, *args, **kwargs):
        """
        Report meshing time.
        """
        return PyMenu(self.service).execute('/report/meshing_time', *args, **kwargs)
    def memory_usage(self, *args, **kwargs):
        """
        Report memory usage.
        """
        return PyMenu(self.service).execute('/report/memory_usage', *args, **kwargs)
    def print_info(self, *args, **kwargs):
        """
        Print node/face/cell info.
        """
        return PyMenu(self.service).execute('/report/print_info', *args, **kwargs)
    def edge_size_limits(self, *args, **kwargs):
        """
        Report edge size limits.
        """
        return PyMenu(self.service).execute('/report/edge_size_limits', *args, **kwargs)
    def face_size_limits(self, *args, **kwargs):
        """
        Report face size limits.
        """
        return PyMenu(self.service).execute('/report/face_size_limits', *args, **kwargs)
    def face_quality_limits(self, *args, **kwargs):
        """
        Report face quality limits.
        """
        return PyMenu(self.service).execute('/report/face_quality_limits', *args, **kwargs)
    def face_zone_area(self, *args, **kwargs):
        """
        Report area of a face zone.
        """
        return PyMenu(self.service).execute('/report/face_zone_area', *args, **kwargs)
    def cell_size_limits(self, *args, **kwargs):
        """
        Report cell size limits.
        """
        return PyMenu(self.service).execute('/report/cell_size_limits', *args, **kwargs)
    def cell_quality_limits(self, *args, **kwargs):
        """
        Report cell quality limits.
        """
        return PyMenu(self.service).execute('/report/cell_quality_limits', *args, **kwargs)
    def neighborhood_quality(self, *args, **kwargs):
        """
        Report max quality measure of all cells using node.
        """
        return PyMenu(self.service).execute('/report/neighborhood_quality', *args, **kwargs)
    def quality_method(self, *args, **kwargs):
        """
        Method to use for measuring face and cell quality.
        """
        return PyMenu(self.service).execute('/report/quality_method', *args, **kwargs)
    def enhanced_orthogonal_quality(self, *args, **kwargs):
        """
        Enable enhanced orthogonal quality method.
        """
        return PyMenu(self.service).execute('/report/enhanced_orthogonal_quality', *args, **kwargs)
    def unrefined_cells(self, *args, **kwargs):
        """
        Report number of cells not refined.
        """
        return PyMenu(self.service).execute('/report/unrefined_cells', *args, **kwargs)
    def update_bounding_box(self, *args, **kwargs):
        """
        Updates bounding box
        """
        return PyMenu(self.service).execute('/report/update_bounding_box', *args, **kwargs)
    def verbosity_level(self, *args, **kwargs):
        """
        Verbosity level control.
        """
        return PyMenu(self.service).execute('/report/verbosity_level', *args, **kwargs)
    def spy_level(self, *args, **kwargs):
        """
        Spy on meshing process.
        """
        return PyMenu(self.service).execute('/report/spy_level', *args, **kwargs)

class parallel(metaclass=PyMenuMeta):
    __doc__ = 'Enter the parallel menu'
    def spawn_solver_processes(self, *args, **kwargs):
        """
        Spawn additional solver processes
        """
        return PyMenu(self.service).execute('/parallel/spawn_solver_processes', *args, **kwargs)
    def auto_partition(self, *args, **kwargs):
        """
        Auto Partition Prism Base Zones?
        """
        return PyMenu(self.service).execute('/parallel/auto_partition', *args, **kwargs)
    def agglomerate(self, *args, **kwargs):
        """
        Agglomerate mesh into compute node 0.
        """
        return PyMenu(self.service).execute('/parallel/agglomerate', *args, **kwargs)
    def print_partition_info(self, *args, **kwargs):
        """
        Prints Partition Info to console
        """
        return PyMenu(self.service).execute('/parallel/print_partition_info', *args, **kwargs)
    def thread_number_control(self, *args, **kwargs):
        """
        thread number control
        """
        return PyMenu(self.service).execute('/parallel/thread_number_control', *args, **kwargs)

class openmp_controls(metaclass=PyMenuMeta):
    __doc__ = 'Enter the openmp menu'
    def get_max_cores(self, *args, **kwargs):
        """
        Max Number of Cores
        """
        return PyMenu(self.service).execute('/openmp_controls/get_max_cores', *args, **kwargs)
    def get_active_cores(self, *args, **kwargs):
        """
        Number of Active Cores
        """
        return PyMenu(self.service).execute('/openmp_controls/get_active_cores', *args, **kwargs)
    def set_num_cores(self, *args, **kwargs):
        """
        Enter Number of Cores
        """
        return PyMenu(self.service).execute('/openmp_controls/set_num_cores', *args, **kwargs)

class reference_frames(metaclass=PyMenuMeta):
    __doc__ = 'Manage reference frames'
    def add(self, *args, **kwargs):
        """
        Add a new object
        """
        return PyMenu(self.service).execute('/reference_frames/add', *args, **kwargs)
    def display(self, *args, **kwargs):
        """
        Display Reference Frame
        """
        return PyMenu(self.service).execute('/reference_frames/display', *args, **kwargs)
    def display_edit(self, *args, **kwargs):
        """
        display and edit reference frame from graphics
        """
        return PyMenu(self.service).execute('/reference_frames/display_edit', *args, **kwargs)
    def edit(self, *args, **kwargs):
        """
        Edit an object
        """
        return PyMenu(self.service).execute('/reference_frames/edit', *args, **kwargs)
    def delete(self, *args, **kwargs):
        """
        Delete an object
        """
        return PyMenu(self.service).execute('/reference_frames/delete', *args, **kwargs)
    def hide(self, *args, **kwargs):
        """
        Hide Reference Frame
        """
        return PyMenu(self.service).execute('/reference_frames/hide', *args, **kwargs)
    def list(self, *args, **kwargs):
        """
        List objects
        """
        return PyMenu(self.service).execute('/reference_frames/list', *args, **kwargs)
    def list_properties(self, *args, **kwargs):
        """
        List properties of an object
        """
        return PyMenu(self.service).execute('/reference_frames/list_properties', *args, **kwargs)
