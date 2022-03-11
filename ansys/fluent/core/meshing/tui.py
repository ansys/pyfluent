"""
This is an auto-generated file.  DO NOT EDIT!
"""
# pylint: disable=line-too-long

from ansys.fluent.core.meta import PyMenuMeta, PyNamedObjectMeta
from ansys.fluent.core.services.datamodel_tui import PyMenu


def beta_feature_access(self, *args, **kwargs):
    """
    Enable access to beta features in the interface.
    """
    return PyMenu(self.service, "/beta_feature_access").execute(*args, **kwargs)
def close_fluent(self, *args, **kwargs):
    """
    Exit Fluent Meshing.
    """
    return PyMenu(self.service, "/close_fluent").execute(*args, **kwargs)
def exit(self, *args, **kwargs):
    """
    Exit Fluent Meshing.
    """
    return PyMenu(self.service, "/exit").execute(*args, **kwargs)
def switch_to_solution_mode(self, *args, **kwargs):
    """
    Switch to solution mode.
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
    def append_mesh(self, *args, **kwargs):
        """
        Append a new mesh to the existing mesh.
        """
        return PyMenu(self.service, "/file/append_mesh").execute(*args, **kwargs)
    def append_meshes_by_tmerge(self, *args, **kwargs):
        """
        Append mesh files, or the meshes from case files.
        """
        return PyMenu(self.service, "/file/append_meshes_by_tmerge").execute(*args, **kwargs)
    def file_format(self, *args, **kwargs):
        """
        Indicate whether to write formatted or unformatted files.
        """
        return PyMenu(self.service, "/file/file_format").execute(*args, **kwargs)
    def filter_list(self, *args, **kwargs):
        """
        List all filter names.
        """
        return PyMenu(self.service, "/file/filter_list").execute(*args, **kwargs)
    def filter_options(self, *args, **kwargs):
        """
        Change filter extension and/or its arguments.
        """
        return PyMenu(self.service, "/file/filter_options").execute(*args, **kwargs)
    def hdf_files(self, *args, **kwargs):
        """
        Indicate whether to write Ansys common fluids format (CFF) files or legacy case files.
        """
        return PyMenu(self.service, "/file/hdf_files").execute(*args, **kwargs)
    def cff_files(self, *args, **kwargs):
        """
        Indicate whether to write Ansys common fluids format (CFF) files or legacy case files.
        """
        return PyMenu(self.service, "/file/cff_files").execute(*args, **kwargs)
    def read_boundary_mesh(self, *args, **kwargs):
        """
        Read the boundary mesh from either a mesh or case file.
        """
        return PyMenu(self.service, "/file/read_boundary_mesh").execute(*args, **kwargs)
    def read_mesh(self, *args, **kwargs):
        """
        Read a mesh file, or the mesh from a case file.
        """
        return PyMenu(self.service, "/file/read_mesh").execute(*args, **kwargs)
    def read_meshes_by_tmerge(self, *args, **kwargs):
        """
        Read mesh files, or the meshes from case files.
        """
        return PyMenu(self.service, "/file/read_meshes_by_tmerge").execute(*args, **kwargs)
    def read_multi_bound_mesh(self, *args, **kwargs):
        """
        Read multiple boundary meshes.
        """
        return PyMenu(self.service, "/file/read_multi_bound_mesh").execute(*args, **kwargs)
    def read_case(self, *args, **kwargs):
        """
        Read a case file.
        Parameters
        ----------
        case_file_name : str
        """
        return PyMenu(self.service, "/file/read_case").execute(*args, **kwargs)
    def read_domains(self, *args, **kwargs):
        """
        Read TGrid domains from a file.
        """
        return PyMenu(self.service, "/file/read_domains").execute(*args, **kwargs)
    def read_size_field(self, *args, **kwargs):
        """
        Read TGrid Size-field from a file.
        """
        return PyMenu(self.service, "/file/read_size_field").execute(*args, **kwargs)
    def write_size_field(self, *args, **kwargs):
        """
        Write TGrid Size-field into a file.
        """
        return PyMenu(self.service, "/file/write_size_field").execute(*args, **kwargs)
    def read_journal(self, *args, **kwargs):
        """
        Start a main-menu that takes its input from a file.
        """
        return PyMenu(self.service, "/file/read_journal").execute(*args, **kwargs)
    def read_mesh_vars(self, *args, **kwargs):
        """
        Reads mesh varaibles from a mesh file.
        """
        return PyMenu(self.service, "/file/read_mesh_vars").execute(*args, **kwargs)
    def read_multiple_mesh(self, *args, **kwargs):
        """
        Read multiple mesh files, or the meshes from multiple case files.
        """
        return PyMenu(self.service, "/file/read_multiple_mesh").execute(*args, **kwargs)
    def read_options(self, *args, **kwargs):
        """
        Set read options.
        """
        return PyMenu(self.service, "/file/read_options").execute(*args, **kwargs)
    def show_configuration(self, *args, **kwargs):
        """
        Display current release and version information.
        """
        return PyMenu(self.service, "/file/show_configuration").execute(*args, **kwargs)
    def start_journal(self, *args, **kwargs):
        """
        Start recording all input in a file.
        """
        return PyMenu(self.service, "/file/start_journal").execute(*args, **kwargs)
    def start_transcript(self, *args, **kwargs):
        """
        Start recording input and output in a file.
        """
        return PyMenu(self.service, "/file/start_transcript").execute(*args, **kwargs)
    def stop_journal(self, *args, **kwargs):
        """
        Stop recording input and close journal file.
        """
        return PyMenu(self.service, "/file/stop_journal").execute(*args, **kwargs)
    def stop_transcript(self, *args, **kwargs):
        """
        Stop recording input and output and close transcript file.
        """
        return PyMenu(self.service, "/file/stop_transcript").execute(*args, **kwargs)
    def confirm_overwrite(self, *args, **kwargs):
        """
        Indicate whether or not to confirm attempts to overwrite existing files.
        """
        return PyMenu(self.service, "/file/confirm_overwrite").execute(*args, **kwargs)
    def write_boundaries(self, *args, **kwargs):
        """
        Write the mesh file of selected boundary face zones.
        """
        return PyMenu(self.service, "/file/write_boundaries").execute(*args, **kwargs)
    def write_case(self, *args, **kwargs):
        """
        Write the mesh to a case file.
        """
        return PyMenu(self.service, "/file/write_case").execute(*args, **kwargs)
    def write_domains(self, *args, **kwargs):
        """
        Write all (except global) domains of the mesh into a file.
        """
        return PyMenu(self.service, "/file/write_domains").execute(*args, **kwargs)
    def write_mesh(self, *args, **kwargs):
        """
        Write a mesh file.
        """
        return PyMenu(self.service, "/file/write_mesh").execute(*args, **kwargs)
    def write_mesh_vars(self, *args, **kwargs):
        """
        Writes mesh varaibles to a file.
        """
        return PyMenu(self.service, "/file/write_mesh_vars").execute(*args, **kwargs)
    def write_options(self, *args, **kwargs):
        """
        Set write options.
        """
        return PyMenu(self.service, "/file/write_options").execute(*args, **kwargs)
    def set_idle_timeout(self, *args, **kwargs):
        """
        Set the idle timeout.
        """
        return PyMenu(self.service, "/file/set_idle_timeout").execute(*args, **kwargs)
    def load_act_tool(self, *args, **kwargs):
        """
        Load ACT Start Page.
        """
        return PyMenu(self.service, "/file/load_act_tool").execute(*args, **kwargs)
    def set_tui_version(self, *args, **kwargs):
        """
        Set the version of the TUI commands.
        """
        return PyMenu(self.service, "/file/set_tui_version").execute(*args, **kwargs)

    class export(metaclass=PyMenuMeta):
        """
        Export surface and volume meshes to non-native formats.
        """
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
            Write a NASTRAN mesh file.
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
        Import surface and volume meshes from non-native formats.
        """
        def ansys_surf_mesh(self, *args, **kwargs):
            """
            Read a surface mesh from an Ansys prep7 or cdb file.
            """
            return PyMenu(self.service, "/file/import/ansys_surf_mesh").execute(*args, **kwargs)
        def ansys_vol_mesh(self, *args, **kwargs):
            """
            Read a volume mesh from an Ansys prep7 or cdb file.
            """
            return PyMenu(self.service, "/file/import/ansys_vol_mesh").execute(*args, **kwargs)
        def cgns_vol_mesh(self, *args, **kwargs):
            """
            Read a volume mesh from an CGNS format file.
            """
            return PyMenu(self.service, "/file/import/cgns_vol_mesh").execute(*args, **kwargs)
        def cgns_surf_mesh(self, *args, **kwargs):
            """
            Read a surface mesh from a CGNS format file.
            """
            return PyMenu(self.service, "/file/import/cgns_surf_mesh").execute(*args, **kwargs)
        def fidap_surf_mesh(self, *args, **kwargs):
            """
            Read a surface mesh from a FIDAP neutral file.
            """
            return PyMenu(self.service, "/file/import/fidap_surf_mesh").execute(*args, **kwargs)
        def fidap_vol_mesh(self, *args, **kwargs):
            """
            Read a volume mesh from a FIDAP neutral file.
            """
            return PyMenu(self.service, "/file/import/fidap_vol_mesh").execute(*args, **kwargs)
        def fl_uns2_mesh(self, *args, **kwargs):
            """
            Read a mesh from a Fluent UNS V2 case file.
            """
            return PyMenu(self.service, "/file/import/fl_uns2_mesh").execute(*args, **kwargs)
        def fluent_2d_mesh(self, *args, **kwargs):
            """
            Read a 2D mesh.
            """
            return PyMenu(self.service, "/file/import/fluent_2d_mesh").execute(*args, **kwargs)
        def fluent_3d_mesh(self, *args, **kwargs):
            """
            Read a 3D mesh.
            """
            return PyMenu(self.service, "/file/import/fluent_3d_mesh").execute(*args, **kwargs)
        def gambit_surf_mesh(self, *args, **kwargs):
            """
            Read a surface mesh from a GAMBIT neutral file.
            """
            return PyMenu(self.service, "/file/import/gambit_surf_mesh").execute(*args, **kwargs)
        def gambit_vol_mesh(self, *args, **kwargs):
            """
            Read a volume mesh from a GAMBIT neutral file.
            """
            return PyMenu(self.service, "/file/import/gambit_vol_mesh").execute(*args, **kwargs)
        def hypermesh_surf_mesh(self, *args, **kwargs):
            """
            Read a surface mesh from a HYPERMESH ascii file.
            """
            return PyMenu(self.service, "/file/import/hypermesh_surf_mesh").execute(*args, **kwargs)
        def hypermesh_vol_mesh(self, *args, **kwargs):
            """
            Read a volume mesh from a HYPERMESH ascii file.
            """
            return PyMenu(self.service, "/file/import/hypermesh_vol_mesh").execute(*args, **kwargs)
        def ideas_surf_mesh(self, *args, **kwargs):
            """
            Read a surface mesh from an IDEAS universal file.
            """
            return PyMenu(self.service, "/file/import/ideas_surf_mesh").execute(*args, **kwargs)
        def ideas_vol_mesh(self, *args, **kwargs):
            """
            Read a volume mesh from an IDEAS universal file.
            """
            return PyMenu(self.service, "/file/import/ideas_vol_mesh").execute(*args, **kwargs)
        def nastran_surf_mesh(self, *args, **kwargs):
            """
            Read a surface mesh from a NASTRAN file.
            """
            return PyMenu(self.service, "/file/import/nastran_surf_mesh").execute(*args, **kwargs)
        def nastran_vol_mesh(self, *args, **kwargs):
            """
            Read a volume mesh from a NASTRAN file.
            """
            return PyMenu(self.service, "/file/import/nastran_vol_mesh").execute(*args, **kwargs)
        def patran_surf_mesh(self, *args, **kwargs):
            """
            Read a surface mesh from a PATRAN neutral file.
            """
            return PyMenu(self.service, "/file/import/patran_surf_mesh").execute(*args, **kwargs)
        def patran_vol_mesh(self, *args, **kwargs):
            """
            Read a volume mesh from a PATRAN neutral file.
            """
            return PyMenu(self.service, "/file/import/patran_vol_mesh").execute(*args, **kwargs)
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
                STL  *.stl.
            """
            return PyMenu(self.service, "/file/import/cad").execute(*args, **kwargs)
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
                STL  *.stl.
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
            Make settings for cad import.
            """
            def read_all_cad_in_subdirectories(self, *args, **kwargs):
                """
                Recursive search for CAD files in sub-directories.
                """
                return PyMenu(self.service, "/file/import/cad_options/read_all_cad_in_subdirectories").execute(*args, **kwargs)
            def continue_on_error(self, *args, **kwargs):
                """
                Continue on error during cad import.
                """
                return PyMenu(self.service, "/file/import/cad_options/continue_on_error").execute(*args, **kwargs)
            def save_PMDB(self, *args, **kwargs):
                """
                Saves PMDB file in the directory containing the CAD files imported.
                """
                return PyMenu(self.service, "/file/import/cad_options/save_PMDB").execute(*args, **kwargs)
            def tessellation(self, *args, **kwargs):
                """
                Set tessellation controls for cad import.
                """
                return PyMenu(self.service, "/file/import/cad_options/tessellation").execute(*args, **kwargs)
            def named_selections(self, *args, **kwargs):
                """
                Allows to import Named Selections from the CAD file.
                """
                return PyMenu(self.service, "/file/import/cad_options/named_selections").execute(*args, **kwargs)
            def enclosure_symm_processing(self, *args, **kwargs):
                """
                Processing of enclosure and symmetry named selections during import.
                """
                return PyMenu(self.service, "/file/import/cad_options/enclosure_symm_processing").execute(*args, **kwargs)
            def reconstruct_topology(self, *args, **kwargs):
                """
                Reconstruct topology for STL files.
                """
                return PyMenu(self.service, "/file/import/cad_options/reconstruct_topology").execute(*args, **kwargs)
            def import_part_names(self, *args, **kwargs):
                """
                Import Part names from the CAD files.
                """
                return PyMenu(self.service, "/file/import/cad_options/import_part_names").execute(*args, **kwargs)
            def import_body_names(self, *args, **kwargs):
                """
                Import Body names from the CAD files.
                """
                return PyMenu(self.service, "/file/import/cad_options/import_body_names").execute(*args, **kwargs)
            def separate_features_by_type(self, *args, **kwargs):
                """
                Separate features by type.
                """
                return PyMenu(self.service, "/file/import/cad_options/separate_features_by_type").execute(*args, **kwargs)
            def single_connected_edge_label(self, *args, **kwargs):
                """
                Single connected edge label for CAD files.
                """
                return PyMenu(self.service, "/file/import/cad_options/single_connected_edge_label").execute(*args, **kwargs)
            def double_connected_face_label(self, *args, **kwargs):
                """
                Double connected face label for CAD files.
                """
                return PyMenu(self.service, "/file/import/cad_options/double_connected_face_label").execute(*args, **kwargs)
            def use_collection_names(self, *args, **kwargs):
                """
                Use collection names for CAD files.
                """
                return PyMenu(self.service, "/file/import/cad_options/use_collection_names").execute(*args, **kwargs)
            def use_component_names(self, *args, **kwargs):
                """
                Use component names for CAD files.
                """
                return PyMenu(self.service, "/file/import/cad_options/use_component_names").execute(*args, **kwargs)
            def name_separator_character(self, *args, **kwargs):
                """
                Character to be used as a separator in all names.
                """
                return PyMenu(self.service, "/file/import/cad_options/name_separator_character").execute(*args, **kwargs)
            def object_type(self, *args, **kwargs):
                """
                Object type for CAD files.
                """
                return PyMenu(self.service, "/file/import/cad_options/object_type").execute(*args, **kwargs)
            def one_object_per(self, *args, **kwargs):
                """
                Set one object per body, part or file.
                """
                return PyMenu(self.service, "/file/import/cad_options/one_object_per").execute(*args, **kwargs)
            def one_face_zone_per(self, *args, **kwargs):
                """
                Set one object per body, face or object.
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
                Use part names for CAD files.
                """
                return PyMenu(self.service, "/file/import/cad_options/use_part_names").execute(*args, **kwargs)
            def replacement_character(self, *args, **kwargs):
                """
                Name replacement character.
                """
                return PyMenu(self.service, "/file/import/cad_options/replacement_character").execute(*args, **kwargs)
            def derive_zone_name_from_object_scope(self, *args, **kwargs):
                """
                Derive zone names from object scope.
                """
                return PyMenu(self.service, "/file/import/cad_options/derive_zone_name_from_object_scope").execute(*args, **kwargs)
            def merge_nodes(self, *args, **kwargs):
                """
                Merge Nodes for CAD import.
                """
                return PyMenu(self.service, "/file/import/cad_options/merge_nodes").execute(*args, **kwargs)
            def create_cad_assemblies(self, *args, **kwargs):
                """
                Import CAD Assemblies.
                """
                return PyMenu(self.service, "/file/import/cad_options/create_cad_assemblies").execute(*args, **kwargs)
            def modify_all_duplicate_names(self, *args, **kwargs):
                """
                Modify all duplicate names by suffixing it with incremental integers.
                """
                return PyMenu(self.service, "/file/import/cad_options/modify_all_duplicate_names").execute(*args, **kwargs)
            def use_part_or_body_names_as_suffix_to_named_selections(self, *args, **kwargs):
                """
                Part or Body names are used as suffix for named selections spanning over multiple parts or bodies.
                """
                return PyMenu(self.service, "/file/import/cad_options/use_part_or_body_names_as_suffix_to_named_selections").execute(*args, **kwargs)
            def strip_file_name_extension_from_naming(self, *args, **kwargs):
                """
                Strip file name extension from naming.
                """
                return PyMenu(self.service, "/file/import/cad_options/strip_file_name_extension_from_naming").execute(*args, **kwargs)
            def import_label_for_body_named_selection(self, *args, **kwargs):
                """
                Import face zone labels for body named selections.
                """
                return PyMenu(self.service, "/file/import/cad_options/import_label_for_body_named_selection").execute(*args, **kwargs)
            def strip_path_prefix_from_names(self, *args, **kwargs):
                """
                Strip path prefixes from naming.
                """
                return PyMenu(self.service, "/file/import/cad_options/strip_path_prefix_from_names").execute(*args, **kwargs)
            def merge_objects_per_body_named_selection(self, *args, **kwargs):
                """
                Merge Objects per body named selection.
                """
                return PyMenu(self.service, "/file/import/cad_options/merge_objects_per_body_named_selection").execute(*args, **kwargs)
            def extract_features(self, *args, **kwargs):
                """
                Set the feature angle.
                """
                return PyMenu(self.service, "/file/import/cad_options/extract_features").execute(*args, **kwargs)
            def import_curvature_data_from_CAD(self, *args, **kwargs):
                """
                Import Curvature Data from CAD.
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

    class parametric_project(metaclass=PyMenuMeta):
        """
        Enter to create new project, read project, and save project.
        """
        def new(self, *args, **kwargs):
            """
            Create New Project.
            """
            return PyMenu(self.service, "/file/parametric_project/new").execute(*args, **kwargs)
        def open(self, *args, **kwargs):
            """
            Open project.
            """
            return PyMenu(self.service, "/file/parametric_project/open").execute(*args, **kwargs)
        def save(self, *args, **kwargs):
            """
            Save Project.
            """
            return PyMenu(self.service, "/file/parametric_project/save").execute(*args, **kwargs)
        def save_as(self, *args, **kwargs):
            """
            Save As Project.
            """
            return PyMenu(self.service, "/file/parametric_project/save_as").execute(*args, **kwargs)
        def save_as_copy(self, *args, **kwargs):
            """
            Save As Copy.
            """
            return PyMenu(self.service, "/file/parametric_project/save_as_copy").execute(*args, **kwargs)
        def archive(self, *args, **kwargs):
            """
            Archive Project.
            """
            return PyMenu(self.service, "/file/parametric_project/archive").execute(*args, **kwargs)

class boundary(metaclass=PyMenuMeta):
    """
    Enter the boundary menu.
    """
    def auto_slit_faces(self, *args, **kwargs):
        """
        Automatically slits all embedded boundary face zones.
        .
        """
        return PyMenu(self.service, "/boundary/auto_slit_faces").execute(*args, **kwargs)
    def orient_faces_by_point(self, *args, **kwargs):
        """
        Orient Region based on Material Point.
        """
        return PyMenu(self.service, "/boundary/orient_faces_by_point").execute(*args, **kwargs)
    def check_boundary_mesh(self, *args, **kwargs):
        """
        Report number of Delaunay violations on surface mesh and unused nodes.
        """
        return PyMenu(self.service, "/boundary/check_boundary_mesh").execute(*args, **kwargs)
    def check_duplicate_geom(self, *args, **kwargs):
        """
        Check duplicated face threads in the geometry.
        """
        return PyMenu(self.service, "/boundary/check_duplicate_geom").execute(*args, **kwargs)
    def clear_marked_faces(self, *args, **kwargs):
        """
        Clear previously marked faces.
        """
        return PyMenu(self.service, "/boundary/clear_marked_faces").execute(*args, **kwargs)
    def clear_marked_nodes(self, *args, **kwargs):
        """
        Clear previously marked nodes.
        """
        return PyMenu(self.service, "/boundary/clear_marked_nodes").execute(*args, **kwargs)
    def coarsen_boundary_faces(self, *args, **kwargs):
        """
        Coarsen boundary face zones.
        """
        return PyMenu(self.service, "/boundary/coarsen_boundary_faces").execute(*args, **kwargs)
    def count_marked_faces(self, *args, **kwargs):
        """
        Count marked faces.
        """
        return PyMenu(self.service, "/boundary/count_marked_faces").execute(*args, **kwargs)
    def count_free_nodes(self, *args, **kwargs):
        """
        Count number of free nodes.
        """
        return PyMenu(self.service, "/boundary/count_free_nodes").execute(*args, **kwargs)
    def count_unused_nodes(self, *args, **kwargs):
        """
        Count number of unused nodes.
        """
        return PyMenu(self.service, "/boundary/count_unused_nodes").execute(*args, **kwargs)
    def count_unused_bound_node(self, *args, **kwargs):
        """
        Count number of unused boundary nodes.
        """
        return PyMenu(self.service, "/boundary/count_unused_bound_node").execute(*args, **kwargs)
    def count_unused_faces(self, *args, **kwargs):
        """
        Count number of unused faces.
        """
        return PyMenu(self.service, "/boundary/count_unused_faces").execute(*args, **kwargs)
    def compute_bounding_box(self, *args, **kwargs):
        """
        Computes bounding box for given zones.
        """
        return PyMenu(self.service, "/boundary/compute_bounding_box").execute(*args, **kwargs)
    def create_bounding_box(self, *args, **kwargs):
        """
        Create bounding box for given zones.
        """
        return PyMenu(self.service, "/boundary/create_bounding_box").execute(*args, **kwargs)
    def create_cylinder(self, *args, **kwargs):
        """
        Create cylinder using two axis end nodes/positions or, three points on the arc defining the cylinder.
        """
        return PyMenu(self.service, "/boundary/create_cylinder").execute(*args, **kwargs)
    def create_plane_surface(self, *args, **kwargs):
        """
        Create plane surface.
        """
        return PyMenu(self.service, "/boundary/create_plane_surface").execute(*args, **kwargs)
    def create_swept_surface(self, *args, **kwargs):
        """
        Create surface by sweeping the edge along the vector.
        """
        return PyMenu(self.service, "/boundary/create_swept_surface").execute(*args, **kwargs)
    def create_revolved_surface(self, *args, **kwargs):
        """
        Create surface by revolving the edge along the vector.
        """
        return PyMenu(self.service, "/boundary/create_revolved_surface").execute(*args, **kwargs)
    def delete_duplicate_faces(self, *args, **kwargs):
        """
        Delete duplicate faces on specified zones.
        """
        return PyMenu(self.service, "/boundary/delete_duplicate_faces").execute(*args, **kwargs)
    def delete_all_dup_faces(self, *args, **kwargs):
        """
        Delete all duplicate faces on all boundary zones.
        """
        return PyMenu(self.service, "/boundary/delete_all_dup_faces").execute(*args, **kwargs)
    def delete_island_faces(self, *args, **kwargs):
        """
        Delete island faces or cavity.
        """
        return PyMenu(self.service, "/boundary/delete_island_faces").execute(*args, **kwargs)
    def delete_unused_nodes(self, *args, **kwargs):
        """
        Delete nodes not belonging to any boundary faces.
        """
        return PyMenu(self.service, "/boundary/delete_unused_nodes").execute(*args, **kwargs)
    def delete_unused_faces(self, *args, **kwargs):
        """
        Delete unused boundary faces.
        """
        return PyMenu(self.service, "/boundary/delete_unused_faces").execute(*args, **kwargs)
    def delete_unconnected_faces(self, *args, **kwargs):
        """
        Delete unconnected face zones.
        """
        return PyMenu(self.service, "/boundary/delete_unconnected_faces").execute(*args, **kwargs)
    def edge_limits(self, *args, **kwargs):
        """
        Print shortest and largest edges on boundary mesh.
        """
        return PyMenu(self.service, "/boundary/edge_limits").execute(*args, **kwargs)
    def expand_marked_faces_by_rings(self, *args, **kwargs):
        """
        Mark rings of faces around marked faces.
        """
        return PyMenu(self.service, "/boundary/expand_marked_faces_by_rings").execute(*args, **kwargs)
    def face_distribution(self, *args, **kwargs):
        """
        Show face quality distribution.
        """
        return PyMenu(self.service, "/boundary/face_distribution").execute(*args, **kwargs)
    def face_skewness(self, *args, **kwargs):
        """
        Show worse face skewness.
        """
        return PyMenu(self.service, "/boundary/face_skewness").execute(*args, **kwargs)
    def jiggle_boundary_nodes(self, *args, **kwargs):
        """
        Perturb randomly nodal position.
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
        Make periodic zone pair.
        """
        return PyMenu(self.service, "/boundary/make_periodic").execute(*args, **kwargs)
    def recover_periodic_surfaces(self, *args, **kwargs):
        """
        Recover periodic surfaces.
        """
        return PyMenu(self.service, "/boundary/recover_periodic_surfaces").execute(*args, **kwargs)
    def set_periodicity(self, *args, **kwargs):
        """
        Set size field periodicity.
        """
        return PyMenu(self.service, "/boundary/set_periodicity").execute(*args, **kwargs)
    def mark_bad_quality_faces(self, *args, **kwargs):
        """
        Mark Bad Quality Faces.
        """
        return PyMenu(self.service, "/boundary/mark_bad_quality_faces").execute(*args, **kwargs)
    def mark_faces_in_region(self, *args, **kwargs):
        """
        Mark faces in local region.
        """
        return PyMenu(self.service, "/boundary/mark_faces_in_region").execute(*args, **kwargs)
    def mark_face_intersection(self, *args, **kwargs):
        """
        Mark face intersection in face zones.
        """
        return PyMenu(self.service, "/boundary/mark_face_intersection").execute(*args, **kwargs)
    def resolve_face_intersection(self, *args, **kwargs):
        """
        Resolve face intersection in tri-face zones.
        """
        return PyMenu(self.service, "/boundary/resolve_face_intersection").execute(*args, **kwargs)
    def mark_face_proximity(self, *args, **kwargs):
        """
        Mark faces that are in proximity.
        """
        return PyMenu(self.service, "/boundary/mark_face_proximity").execute(*args, **kwargs)
    def mark_duplicate_nodes(self, *args, **kwargs):
        """
        Mark duplicate nodes.
        """
        return PyMenu(self.service, "/boundary/mark_duplicate_nodes").execute(*args, **kwargs)
    def merge_nodes(self, *args, **kwargs):
        """
        Merge duplicate nodes.  If a face has two of
        its nodes merged, then it is deleted.
        """
        return PyMenu(self.service, "/boundary/merge_nodes").execute(*args, **kwargs)
    def merge_small_face_zones(self, *args, **kwargs):
        """
        Merge face zones having area less than min area with largest zone in its neighbor.
        """
        return PyMenu(self.service, "/boundary/merge_small_face_zones").execute(*args, **kwargs)
    def print_info(self, *args, **kwargs):
        """
        Print node/face/cell info.
        """
        return PyMenu(self.service, "/boundary/print_info").execute(*args, **kwargs)
    def project_face_zone(self, *args, **kwargs):
        """
        Project face zone to a background mesh.
        """
        return PyMenu(self.service, "/boundary/project_face_zone").execute(*args, **kwargs)
    def reset_element_type(self, *args, **kwargs):
        """
        Reset the element type (mixed, linear, tri or quad) of a boundary zone.
        """
        return PyMenu(self.service, "/boundary/reset_element_type").execute(*args, **kwargs)
    def scale_nodes(self, *args, **kwargs):
        """
        Scale all nodes by the scale factor.
        """
        return PyMenu(self.service, "/boundary/scale_nodes").execute(*args, **kwargs)
    def slit_boundary_face(self, *args, **kwargs):
        """
        Make slit in mesh at boundary face.
        All faces must have normals oriented in the same direction.
        .
        """
        return PyMenu(self.service, "/boundary/slit_boundary_face").execute(*args, **kwargs)
    def unmark_selected_faces(self, *args, **kwargs):
        """
        Clear mark on selected faces.
        """
        return PyMenu(self.service, "/boundary/unmark_selected_faces").execute(*args, **kwargs)
    def smooth_marked_faces(self, *args, **kwargs):
        """
        Smooth Marked faces on threads.
        """
        return PyMenu(self.service, "/boundary/smooth_marked_faces").execute(*args, **kwargs)
    def wrapper(self, *args, **kwargs):
        """
        Enter surface wrapper menu.
        """
        return PyMenu(self.service, "/boundary/wrapper").execute(*args, **kwargs)
    def unmark_faces_in_zones(self, *args, **kwargs):
        """
        Unmark faces in zones.
        """
        return PyMenu(self.service, "/boundary/unmark_faces_in_zones").execute(*args, **kwargs)
    def delete_free_edge_faces(self, *args, **kwargs):
        """
        Remove faces with specified number of free edges.
        """
        return PyMenu(self.service, "/boundary/delete_free_edge_faces").execute(*args, **kwargs)
    def fix_mconnected_edges(self, *args, **kwargs):
        """
        Fix multi connected edges.
        """
        return PyMenu(self.service, "/boundary/fix_mconnected_edges").execute(*args, **kwargs)

    class feature(metaclass=PyMenuMeta):
        """
        Enter bounday feature menu.
        """
        def copy_edge_zones(self, *args, **kwargs):
            """
            Copy edge zones.
            """
            return PyMenu(self.service, "/boundary/feature/copy_edge_zones").execute(*args, **kwargs)
        def create_edge_zones(self, *args, **kwargs):
            """
            Create edge loops of thread based on feature angle.
            """
            return PyMenu(self.service, "/boundary/feature/create_edge_zones").execute(*args, **kwargs)
        def delete_edge_zones(self, *args, **kwargs):
            """
            Delete edge zones.
            """
            return PyMenu(self.service, "/boundary/feature/delete_edge_zones").execute(*args, **kwargs)
        def delete_degenerated_edges(self, *args, **kwargs):
            """
            Delete from Edge Zones, Edges whose two end nodes are the same.
            """
            return PyMenu(self.service, "/boundary/feature/delete_degenerated_edges").execute(*args, **kwargs)
        def edge_size_limits(self, *args, **kwargs):
            """
            Report edge size limits.
            """
            return PyMenu(self.service, "/boundary/feature/edge_size_limits").execute(*args, **kwargs)
        def intersect_edge_zones(self, *args, **kwargs):
            """
            Intersect edge zones.
            """
            return PyMenu(self.service, "/boundary/feature/intersect_edge_zones").execute(*args, **kwargs)
        def group(self, *args, **kwargs):
            """
            Group face and edge zones together.
            """
            return PyMenu(self.service, "/boundary/feature/group").execute(*args, **kwargs)
        def list_edge_zones(self, *args, **kwargs):
            """
            List edge zones.
            """
            return PyMenu(self.service, "/boundary/feature/list_edge_zones").execute(*args, **kwargs)
        def merge_edge_zones(self, *args, **kwargs):
            """
            Merge edge zones.
            """
            return PyMenu(self.service, "/boundary/feature/merge_edge_zones").execute(*args, **kwargs)
        def orient_edge_direction(self, *args, **kwargs):
            """
            Orient edge zone directions.
            """
            return PyMenu(self.service, "/boundary/feature/orient_edge_direction").execute(*args, **kwargs)
        def project_edge_zones(self, *args, **kwargs):
            """
            Project edge zones on specified face zone.
            """
            return PyMenu(self.service, "/boundary/feature/project_edge_zones").execute(*args, **kwargs)
        def remesh_edge_zones(self, *args, **kwargs):
            """
            Remesh edge zones.
            """
            return PyMenu(self.service, "/boundary/feature/remesh_edge_zones").execute(*args, **kwargs)
        def reverse_edge_direction(self, *args, **kwargs):
            """
            Reverse direction of edge loops.
            """
            return PyMenu(self.service, "/boundary/feature/reverse_edge_direction").execute(*args, **kwargs)
        def separate_edge_zones(self, *args, **kwargs):
            """
            Separate edge zones based on connectivity and feature angle.
            """
            return PyMenu(self.service, "/boundary/feature/separate_edge_zones").execute(*args, **kwargs)
        def separate_edge_zones_by_seed(self, *args, **kwargs):
            """
            Separate edge zones by seed.
            """
            return PyMenu(self.service, "/boundary/feature/separate_edge_zones_by_seed").execute(*args, **kwargs)
        def toggle_edge_type(self, *args, **kwargs):
            """
            Toggle edge type between boundary and interior.
            """
            return PyMenu(self.service, "/boundary/feature/toggle_edge_type").execute(*args, **kwargs)
        def ungroup(self, *args, **kwargs):
            """
            Ungroup previously grouped face and edge zones.
            """
            return PyMenu(self.service, "/boundary/feature/ungroup").execute(*args, **kwargs)
        def separate_delete_small_edges(self, *args, **kwargs):
            """
            Separates and deletes small edges.
            """
            return PyMenu(self.service, "/boundary/feature/separate_delete_small_edges").execute(*args, **kwargs)

    class modify(metaclass=PyMenuMeta):
        """
        Enter boundary modify menu.
        """
        def analyze_bnd_connectvty(self, *args, **kwargs):
            """
            Find and mark free edges/nodes and mutliple-connected edges/nodes.
            """
            return PyMenu(self.service, "/boundary/modify/analyze_bnd_connectvty").execute(*args, **kwargs)
        def clear_selections(self, *args, **kwargs):
            """
            Clear all selections.
            """
            return PyMenu(self.service, "/boundary/modify/clear_selections").execute(*args, **kwargs)
        def create(self, *args, **kwargs):
            """
            Create either nodes or faces.
            """
            return PyMenu(self.service, "/boundary/modify/create").execute(*args, **kwargs)
        def auto_patch_holes(self, *args, **kwargs):
            """
            Patch zone(s) by filling holes.
            """
            return PyMenu(self.service, "/boundary/modify/auto_patch_holes").execute(*args, **kwargs)
        def create_mid_node(self, *args, **kwargs):
            """
            Create a node at the midpoint between two selected nodes.
            """
            return PyMenu(self.service, "/boundary/modify/create_mid_node").execute(*args, **kwargs)
        def collapse(self, *args, **kwargs):
            """
            Collapse pairs of nodes or edges or faces.
            """
            return PyMenu(self.service, "/boundary/modify/collapse").execute(*args, **kwargs)
        def delete(self, *args, **kwargs):
            """
            Delete either nodes, faces or zones.
            """
            return PyMenu(self.service, "/boundary/modify/delete").execute(*args, **kwargs)
        def deselect_last(self, *args, **kwargs):
            """
            Deselect last selection.
            """
            return PyMenu(self.service, "/boundary/modify/deselect_last").execute(*args, **kwargs)
        def clear_skew_faces(self, *args, **kwargs):
            """
            Clear faces previously marked as skewed.
            """
            return PyMenu(self.service, "/boundary/modify/clear_skew_faces").execute(*args, **kwargs)
        def list_selections(self, *args, **kwargs):
            """
            List selections.
            """
            return PyMenu(self.service, "/boundary/modify/list_selections").execute(*args, **kwargs)
        def mark_skew_face(self, *args, **kwargs):
            """
            Mark face to skip when reporting worst skew face.
            """
            return PyMenu(self.service, "/boundary/modify/mark_skew_face").execute(*args, **kwargs)
        def merge(self, *args, **kwargs):
            """
            Merge nodes.
            """
            return PyMenu(self.service, "/boundary/modify/merge").execute(*args, **kwargs)
        def move(self, *args, **kwargs):
            """
            Move nodes to new positions.
            """
            return PyMenu(self.service, "/boundary/modify/move").execute(*args, **kwargs)
        def delta_move(self, *args, **kwargs):
            """
            Move nodes to new positions.
            """
            return PyMenu(self.service, "/boundary/modify/delta_move").execute(*args, **kwargs)
        def rezone(self, *args, **kwargs):
            """
            Change the zone faces belong to.
            """
            return PyMenu(self.service, "/boundary/modify/rezone").execute(*args, **kwargs)
        def select_entity(self, *args, **kwargs):
            """
            Select a entity.
            """
            return PyMenu(self.service, "/boundary/modify/select_entity").execute(*args, **kwargs)
        def select_filter(self, *args, **kwargs):
            """
            Select probe filter.
            """
            return PyMenu(self.service, "/boundary/modify/select_filter").execute(*args, **kwargs)
        def select_probe(self, *args, **kwargs):
            """
            Select probe function.
            """
            return PyMenu(self.service, "/boundary/modify/select_probe").execute(*args, **kwargs)
        def select_position(self, *args, **kwargs):
            """
            Select a position.
            """
            return PyMenu(self.service, "/boundary/modify/select_position").execute(*args, **kwargs)
        def select_zone(self, *args, **kwargs):
            """
            Select a zone.
            """
            return PyMenu(self.service, "/boundary/modify/select_zone").execute(*args, **kwargs)
        def show_filter(self, *args, **kwargs):
            """
            Show current probe filter.
            """
            return PyMenu(self.service, "/boundary/modify/show_filter").execute(*args, **kwargs)
        def show_probe(self, *args, **kwargs):
            """
            Show current probe function.
            """
            return PyMenu(self.service, "/boundary/modify/show_probe").execute(*args, **kwargs)
        def skew(self, *args, **kwargs):
            """
            Display the highest skewed boundary face.
            """
            return PyMenu(self.service, "/boundary/modify/skew").execute(*args, **kwargs)
        def smooth(self, *args, **kwargs):
            """
            Smooth selected nodes.
            """
            return PyMenu(self.service, "/boundary/modify/smooth").execute(*args, **kwargs)
        def split_face(self, *args, **kwargs):
            """
            Split two selected faces into four.
            """
            return PyMenu(self.service, "/boundary/modify/split_face").execute(*args, **kwargs)
        def swap(self, *args, **kwargs):
            """
            Swap edges.
            """
            return PyMenu(self.service, "/boundary/modify/swap").execute(*args, **kwargs)
        def hole_feature_angle(self, *args, **kwargs):
            """
            Angle defining boundary of hole.
            """
            return PyMenu(self.service, "/boundary/modify/hole_feature_angle").execute(*args, **kwargs)
        def undo(self, *args, **kwargs):
            """
            Undo last modification.
            """
            return PyMenu(self.service, "/boundary/modify/undo").execute(*args, **kwargs)
        def next_skew(self, *args, **kwargs):
            """
            Display the next highest skewed boundary face.
            """
            return PyMenu(self.service, "/boundary/modify/next_skew").execute(*args, **kwargs)
        def skew_report_zone(self, *args, **kwargs):
            """
            Face zone for which skewness has to be reported.
            """
            return PyMenu(self.service, "/boundary/modify/skew_report_zone").execute(*args, **kwargs)
        def local_remesh(self, *args, **kwargs):
            """
            Remesh locally starting from face seeds.
            """
            return PyMenu(self.service, "/boundary/modify/local_remesh").execute(*args, **kwargs)
        def select_visible_entities(self, *args, **kwargs):
            """
            Set visual selection mode of entities.
            """
            return PyMenu(self.service, "/boundary/modify/select_visible_entities").execute(*args, **kwargs)

        class patch_options(metaclass=PyMenuMeta):
            """
            Settings for Patching zone(s) by filling holes.
            """
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
        Enter refine boundary face menu.
        """
        def auto_refine(self, *args, **kwargs):
            """
            Automatically refine faces based on proximity with other faces.
            """
            return PyMenu(self.service, "/boundary/refine/auto_refine").execute(*args, **kwargs)
        def clear(self, *args, **kwargs):
            """
            Clear the refine flag at the faces.
            """
            return PyMenu(self.service, "/boundary/refine/clear").execute(*args, **kwargs)
        def count(self, *args, **kwargs):
            """
            Count the number of faces flagged on thread(s).
            """
            return PyMenu(self.service, "/boundary/refine/count").execute(*args, **kwargs)
        def mark(self, *args, **kwargs):
            """
            Mark faces in region for refinement.
            """
            return PyMenu(self.service, "/boundary/refine/mark").execute(*args, **kwargs)
        def limits(self, *args, **kwargs):
            """
            List face zone information on number of faces flagged and range of face size.
            """
            return PyMenu(self.service, "/boundary/refine/limits").execute(*args, **kwargs)
        def refine(self, *args, **kwargs):
            """
            Refine the flagged faces.
            """
            return PyMenu(self.service, "/boundary/refine/refine").execute(*args, **kwargs)

        class local_regions(metaclass=PyMenuMeta):
            """
            Enter the refine-local menu.
            """
            def define(self, *args, **kwargs):
                """
                Define a refinement region's parameters.
                """
                return PyMenu(self.service, "/boundary/refine/local_regions/define").execute(*args, **kwargs)
            def delete(self, *args, **kwargs):
                """
                Delete a refinement region.
                """
                return PyMenu(self.service, "/boundary/refine/local_regions/delete").execute(*args, **kwargs)
            def init(self, *args, **kwargs):
                """
                Delete all current regions and add the default refinement region.
                """
                return PyMenu(self.service, "/boundary/refine/local_regions/init").execute(*args, **kwargs)
            def list_all_regions(self, *args, **kwargs):
                """
                List all refinement regions.
                """
                return PyMenu(self.service, "/boundary/refine/local_regions/list_all_regions").execute(*args, **kwargs)

    class remesh(metaclass=PyMenuMeta):
        """
        Enter remeshing boundary face zone menu.
        """
        def create_edge_loops(self, *args, **kwargs):
            """
            Create edge loops of thread based on feature angle.
            """
            return PyMenu(self.service, "/boundary/remesh/create_edge_loops").execute(*args, **kwargs)
        def create_intersect_loop(self, *args, **kwargs):
            """
            Create edge loop of intersection.
            """
            return PyMenu(self.service, "/boundary/remesh/create_intersect_loop").execute(*args, **kwargs)
        def create_all_intrst_loops(self, *args, **kwargs):
            """
            Create edge loop of intersection for all boundary zones in current domain.
            """
            return PyMenu(self.service, "/boundary/remesh/create_all_intrst_loops").execute(*args, **kwargs)
        def create_join_loop(self, *args, **kwargs):
            """
            Create edge loop of overlap region.
            """
            return PyMenu(self.service, "/boundary/remesh/create_join_loop").execute(*args, **kwargs)
        def create_stitch_loop(self, *args, **kwargs):
            """
            Create edge loop of stitch edges.
            """
            return PyMenu(self.service, "/boundary/remesh/create_stitch_loop").execute(*args, **kwargs)
        def delete_overlapped_edges(self, *args, **kwargs):
            """
            Delete edges that overlapped selected loops.
            """
            return PyMenu(self.service, "/boundary/remesh/delete_overlapped_edges").execute(*args, **kwargs)
        def intersect_face_zones(self, *args, **kwargs):
            """
            Intersection face zones.
            """
            return PyMenu(self.service, "/boundary/remesh/intersect_face_zones").execute(*args, **kwargs)
        def intersect_all_face_zones(self, *args, **kwargs):
            """
            Intersect all face zones.
            """
            return PyMenu(self.service, "/boundary/remesh/intersect_all_face_zones").execute(*args, **kwargs)
        def remesh_face_zone(self, *args, **kwargs):
            """
            Retriangulate a face zone.
            """
            return PyMenu(self.service, "/boundary/remesh/remesh_face_zone").execute(*args, **kwargs)
        def remesh_marked_faces(self, *args, **kwargs):
            """
            Locally remesh marked faces.
            """
            return PyMenu(self.service, "/boundary/remesh/remesh_marked_faces").execute(*args, **kwargs)
        def mark_intersecting_faces(self, *args, **kwargs):
            """
            Mark faces on zones.
            """
            return PyMenu(self.service, "/boundary/remesh/mark_intersecting_faces").execute(*args, **kwargs)
        def remesh_face_zones_conformally(self, *args, **kwargs):
            """
            Retriangulate face zones while maintaining conformity.
            """
            return PyMenu(self.service, "/boundary/remesh/remesh_face_zones_conformally").execute(*args, **kwargs)
        def remesh_constant_size(self, *args, **kwargs):
            """
            Retriangulate face zones to constant triangle size while maintaining conformity.
            """
            return PyMenu(self.service, "/boundary/remesh/remesh_constant_size").execute(*args, **kwargs)
        def coarsen_and_refine(self, *args, **kwargs):
            """
            Coarsen and refine face zones according to size function.
            """
            return PyMenu(self.service, "/boundary/remesh/coarsen_and_refine").execute(*args, **kwargs)
        def remesh_overlapping_zones(self, *args, **kwargs):
            """
            Remeshing overlapping face zones.
            """
            return PyMenu(self.service, "/boundary/remesh/remesh_overlapping_zones").execute(*args, **kwargs)
        def join_face_zones(self, *args, **kwargs):
            """
            Join face zones.
            """
            return PyMenu(self.service, "/boundary/remesh/join_face_zones").execute(*args, **kwargs)
        def join_all_face_zones(self, *args, **kwargs):
            """
            Intersect all face zones.
            """
            return PyMenu(self.service, "/boundary/remesh/join_all_face_zones").execute(*args, **kwargs)
        def mark_join_faces(self, *args, **kwargs):
            """
            Mark faces on zones.
            """
            return PyMenu(self.service, "/boundary/remesh/mark_join_faces").execute(*args, **kwargs)
        def stitch_face_zones(self, *args, **kwargs):
            """
            Stitch edges on zones.
            """
            return PyMenu(self.service, "/boundary/remesh/stitch_face_zones").execute(*args, **kwargs)
        def stitch_all_face_zones(self, *args, **kwargs):
            """
            Intersect all face zones.
            """
            return PyMenu(self.service, "/boundary/remesh/stitch_all_face_zones").execute(*args, **kwargs)
        def triangulate(self, *args, **kwargs):
            """
            Create triangulation from existing quad face zone.
            """
            return PyMenu(self.service, "/boundary/remesh/triangulate").execute(*args, **kwargs)
        def mark_stitch_faces(self, *args, **kwargs):
            """
            Mark faces on zones.
            """
            return PyMenu(self.service, "/boundary/remesh/mark_stitch_faces").execute(*args, **kwargs)
        def faceted_stitch_zones(self, *args, **kwargs):
            """
            Stitch free edges on zones.
            """
            return PyMenu(self.service, "/boundary/remesh/faceted_stitch_zones").execute(*args, **kwargs)
        def insert_edge_zone(self, *args, **kwargs):
            """
            Insert edge into face zonoe.
            """
            return PyMenu(self.service, "/boundary/remesh/insert_edge_zone").execute(*args, **kwargs)
        def clear_marked_faces(self, *args, **kwargs):
            """
            Clear previously marked faces.
            """
            return PyMenu(self.service, "/boundary/remesh/clear_marked_faces").execute(*args, **kwargs)
        def stitch_with_preserve_boundary(self, *args, **kwargs):
            """
            Stitch volume to boundary zone at free faces.
            """
            return PyMenu(self.service, "/boundary/remesh/stitch_with_preserve_boundary").execute(*args, **kwargs)

        class controls(metaclass=PyMenuMeta):
            """
            Edge loop tools text menu.
            """
            def remesh_method(self, *args, **kwargs):
                """
                Available methods: 1-constant 2-arithmetic 3-geometric.
                """
                return PyMenu(self.service, "/boundary/remesh/controls/remesh_method").execute(*args, **kwargs)
            def quadratic_recon(self, *args, **kwargs):
                """
                Turn on/off quadratic reconstruction of edge loops.
                """
                return PyMenu(self.service, "/boundary/remesh/controls/quadratic_recon").execute(*args, **kwargs)
            def spacing(self, *args, **kwargs):
                """
                Set first and last edge spacing.
                """
                return PyMenu(self.service, "/boundary/remesh/controls/spacing").execute(*args, **kwargs)
            def delete_overlapped(self, *args, **kwargs):
                """
                Turn on/off deletion of overlapped edges.
                """
                return PyMenu(self.service, "/boundary/remesh/controls/delete_overlapped").execute(*args, **kwargs)
            def tolerance(self, *args, **kwargs):
                """
                Set intersection tolerance (absolute unit).
                """
                return PyMenu(self.service, "/boundary/remesh/controls/tolerance").execute(*args, **kwargs)
            def project_method(self, *args, **kwargs):
                """
                Available methods: 0-closest 1-direction.
                """
                return PyMenu(self.service, "/boundary/remesh/controls/project_method").execute(*args, **kwargs)
            def direction(self, *args, **kwargs):
                """
                Set direction of edge loop projection.
                """
                return PyMenu(self.service, "/boundary/remesh/controls/direction").execute(*args, **kwargs)
            def proximity_local_search(self, *args, **kwargs):
                """
                Include selected face for proximity calculation.
                """
                return PyMenu(self.service, "/boundary/remesh/controls/proximity_local_search").execute(*args, **kwargs)

            class intersect(metaclass=PyMenuMeta):
                """
                Enter the intersect control menu.
                """
                def within_tolerance(self, *args, **kwargs):
                    """
                    Turn on/off tolerant intersection.
                    """
                    return PyMenu(self.service, "/boundary/remesh/controls/intersect/within_tolerance").execute(*args, **kwargs)
                def delete_overlap(self, *args, **kwargs):
                    """
                    Turn on/off deletion of overlapped region.
                    """
                    return PyMenu(self.service, "/boundary/remesh/controls/intersect/delete_overlap").execute(*args, **kwargs)
                def ignore_parallel_faces(self, *args, **kwargs):
                    """
                    Turn on/off ignore parallel faces.
                    """
                    return PyMenu(self.service, "/boundary/remesh/controls/intersect/ignore_parallel_faces").execute(*args, **kwargs)
                def refine_region(self, *args, **kwargs):
                    """
                    Turn on/off refinement of intersection region.
                    """
                    return PyMenu(self.service, "/boundary/remesh/controls/intersect/refine_region").execute(*args, **kwargs)
                def separate(self, *args, **kwargs):
                    """
                    Turn on/off separation of intersection region.
                    """
                    return PyMenu(self.service, "/boundary/remesh/controls/intersect/separate").execute(*args, **kwargs)
                def absolute_tolerance(self, *args, **kwargs):
                    """
                    Turn on/off absolute tolerance.
                    """
                    return PyMenu(self.service, "/boundary/remesh/controls/intersect/absolute_tolerance").execute(*args, **kwargs)
                def retri_improve(self, *args, **kwargs):
                    """
                    Turn on/off mesh improvement.
                    """
                    return PyMenu(self.service, "/boundary/remesh/controls/intersect/retri_improve").execute(*args, **kwargs)
                def stitch_preserve(self, *args, **kwargs):
                    """
                    Turn on/off stitch preserve first zone shape.
                    """
                    return PyMenu(self.service, "/boundary/remesh/controls/intersect/stitch_preserve").execute(*args, **kwargs)
                def tolerance(self, *args, **kwargs):
                    """
                    Intersection tolerance.
                    """
                    return PyMenu(self.service, "/boundary/remesh/controls/intersect/tolerance").execute(*args, **kwargs)
                def join_match_angle(self, *args, **kwargs):
                    """
                    Max allowable angle between normals of faces to join.
                    """
                    return PyMenu(self.service, "/boundary/remesh/controls/intersect/join_match_angle").execute(*args, **kwargs)
                def feature_angle(self, *args, **kwargs):
                    """
                    Angle used to determine angle feature edges.
                    """
                    return PyMenu(self.service, "/boundary/remesh/controls/intersect/feature_angle").execute(*args, **kwargs)
                def join_project_angle(self, *args, **kwargs):
                    """
                    Max allowable angle between face normal and project direction for join.
                    """
                    return PyMenu(self.service, "/boundary/remesh/controls/intersect/join_project_angle").execute(*args, **kwargs)
                def remesh_post_intersection(self, *args, **kwargs):
                    """
                    Remesh after intersection.
                    """
                    return PyMenu(self.service, "/boundary/remesh/controls/intersect/remesh_post_intersection").execute(*args, **kwargs)

        class size_functions(metaclass=PyMenuMeta):
            """
            Enable specification of size functions.
            """
            def create(self, *args, **kwargs):
                """
                Add size function.
                """
                return PyMenu(self.service, "/boundary/remesh/size_functions/create").execute(*args, **kwargs)
            def delete(self, *args, **kwargs):
                """
                Delete Size Functions.
                """
                return PyMenu(self.service, "/boundary/remesh/size_functions/delete").execute(*args, **kwargs)
            def delete_all(self, *args, **kwargs):
                """
                Delete All Size Functions.
                """
                return PyMenu(self.service, "/boundary/remesh/size_functions/delete_all").execute(*args, **kwargs)
            def compute(self, *args, **kwargs):
                """
                Compute Size-functions.
                """
                return PyMenu(self.service, "/boundary/remesh/size_functions/compute").execute(*args, **kwargs)
            def list(self, *args, **kwargs):
                """
                List all Size function parameters.
                """
                return PyMenu(self.service, "/boundary/remesh/size_functions/list").execute(*args, **kwargs)
            def create_defaults(self, *args, **kwargs):
                """
                Creates default curvature & proximty size functions acting on all faces and edges.
                """
                return PyMenu(self.service, "/boundary/remesh/size_functions/create_defaults").execute(*args, **kwargs)
            def set_global_controls(self, *args, **kwargs):
                """
                Set controls for global controls.
                """
                return PyMenu(self.service, "/boundary/remesh/size_functions/set_global_controls").execute(*args, **kwargs)
            def enable_periodicity_filter(self, *args, **kwargs):
                """
                Enable size field periodicity.
                """
                return PyMenu(self.service, "/boundary/remesh/size_functions/enable_periodicity_filter").execute(*args, **kwargs)
            def disable_periodicity_filter(self, *args, **kwargs):
                """
                Disable size field periodicity.
                """
                return PyMenu(self.service, "/boundary/remesh/size_functions/disable_periodicity_filter").execute(*args, **kwargs)
            def list_periodicity_filter(self, *args, **kwargs):
                """
                List periodic in size field.
                """
                return PyMenu(self.service, "/boundary/remesh/size_functions/list_periodicity_filter").execute(*args, **kwargs)
            def set_scaling_filter(self, *args, **kwargs):
                """
                Set scaling filter on size field.
                """
                return PyMenu(self.service, "/boundary/remesh/size_functions/set_scaling_filter").execute(*args, **kwargs)
            def reset_global_controls(self, *args, **kwargs):
                """
                Reset controls for global controls.
                """
                return PyMenu(self.service, "/boundary/remesh/size_functions/reset_global_controls").execute(*args, **kwargs)
            def set_prox_gap_tolerance(self, *args, **kwargs):
                """
                Set proximity min gap tolerance relative to global min-size.
                """
                return PyMenu(self.service, "/boundary/remesh/size_functions/set_prox_gap_tolerance").execute(*args, **kwargs)
            def triangulate_quad_faces(self, *args, **kwargs):
                """
                Replace non-triangular face zones with triangulated face zones during size field computation.
                """
                return PyMenu(self.service, "/boundary/remesh/size_functions/triangulate_quad_faces").execute(*args, **kwargs)
            def use_cad_imported_curvature(self, *args, **kwargs):
                """
                Use curvature data imported from CAD.
                """
                return PyMenu(self.service, "/boundary/remesh/size_functions/use_cad_imported_curvature").execute(*args, **kwargs)

            class contours(metaclass=PyMenuMeta):
                """
                Menu to contour of size field.
                """
                def draw(self, *args, **kwargs):
                    """
                    Draw size field contour on face zones.
                    """
                    return PyMenu(self.service, "/boundary/remesh/size_functions/contours/draw").execute(*args, **kwargs)

                class set(metaclass=PyMenuMeta):
                    """
                    Set contour options.
                    """
                    def refine_facets(self, *args, **kwargs):
                        """
                        Option to refine facets virtually? for better contour resolution.
                        """
                        return PyMenu(self.service, "/boundary/remesh/size_functions/contours/set/refine_facets").execute(*args, **kwargs)

            class controls(metaclass=PyMenuMeta):
                """
                Menu to control different behavior of sf.
                """
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
        Enter Imporve  boundary face zone menu.
        """
        def collapse_bad_faces(self, *args, **kwargs):
            """
            Collapse short edge of faces with high aspect ratio.
            """
            return PyMenu(self.service, "/boundary/improve/collapse_bad_faces").execute(*args, **kwargs)
        def improve(self, *args, **kwargs):
            """
            Improve skewness of tri boundary face zones.
            """
            return PyMenu(self.service, "/boundary/improve/improve").execute(*args, **kwargs)
        def smooth(self, *args, **kwargs):
            """
            Smooth  face zones using laplace smoothing.
            .
            """
            return PyMenu(self.service, "/boundary/improve/smooth").execute(*args, **kwargs)
        def swap(self, *args, **kwargs):
            """
            Improve surface mesh by swapping face edges
            where Delaunay violations occur.
            """
            return PyMenu(self.service, "/boundary/improve/swap").execute(*args, **kwargs)
        def degree_swap(self, *args, **kwargs):
            """
            Perform swap on boundary mesh based on node degree.
            """
            return PyMenu(self.service, "/boundary/improve/degree_swap").execute(*args, **kwargs)

    class separate(metaclass=PyMenuMeta):
        """
        Enter separate boundary face menu.
        """
        def mark_faces_in_region(self, *args, **kwargs):
            """
            Mark faces in local region.
            """
            return PyMenu(self.service, "/boundary/separate/mark_faces_in_region").execute(*args, **kwargs)
        def sep_face_zone_by_angle(self, *args, **kwargs):
            """
            Move faces to a new zone based on significant angle.
            """
            return PyMenu(self.service, "/boundary/separate/sep_face_zone_by_angle").execute(*args, **kwargs)
        def sep_face_zone_by_cnbor(self, *args, **kwargs):
            """
            Move faces to a new zone based on cell neighbors.
            """
            return PyMenu(self.service, "/boundary/separate/sep_face_zone_by_cnbor").execute(*args, **kwargs)
        def sep_face_zone_by_mark(self, *args, **kwargs):
            """
            Move faces marked to new zone.
            """
            return PyMenu(self.service, "/boundary/separate/sep_face_zone_by_mark").execute(*args, **kwargs)
        def sep_face_zone_by_region(self, *args, **kwargs):
            """
            Move non-contiguous faces or faces separated by an intersecting wall to a new zone.
            """
            return PyMenu(self.service, "/boundary/separate/sep_face_zone_by_region").execute(*args, **kwargs)
        def sep_face_zone_by_seed(self, *args, **kwargs):
            """
            Move faces connected to seed whose angle satisfies given angle constraint.
            """
            return PyMenu(self.service, "/boundary/separate/sep_face_zone_by_seed").execute(*args, **kwargs)
        def sep_face_zone_by_seed_angle(self, *args, **kwargs):
            """
            Move faces connected to seed whose normal fall within the specified cone.
            """
            return PyMenu(self.service, "/boundary/separate/sep_face_zone_by_seed_angle").execute(*args, **kwargs)
        def sep_face_zone_by_shape(self, *args, **kwargs):
            """
            Move faces based on face shape.
            """
            return PyMenu(self.service, "/boundary/separate/sep_face_zone_by_shape").execute(*args, **kwargs)

        class local_regions(metaclass=PyMenuMeta):
            """
            Enter the separate-local menu.
            """
            def define(self, *args, **kwargs):
                """
                Define a refinement region's parameters.
                """
                return PyMenu(self.service, "/boundary/separate/local_regions/define").execute(*args, **kwargs)
            def delete(self, *args, **kwargs):
                """
                Delete a refinement region.
                """
                return PyMenu(self.service, "/boundary/separate/local_regions/delete").execute(*args, **kwargs)
            def init(self, *args, **kwargs):
                """
                Delete all current regions and add the default refinement region.
                """
                return PyMenu(self.service, "/boundary/separate/local_regions/init").execute(*args, **kwargs)
            def list_all_regions(self, *args, **kwargs):
                """
                List all refinement regions.
                """
                return PyMenu(self.service, "/boundary/separate/local_regions/list_all_regions").execute(*args, **kwargs)

    class manage(metaclass=PyMenuMeta):
        """
        Enter face zone menu.
        """
        def auto_delete_nodes(self, *args, **kwargs):
            """
            Automatically delete unused nodes after deleting faces.
            """
            return PyMenu(self.service, "/boundary/manage/auto_delete_nodes").execute(*args, **kwargs)
        def copy(self, *args, **kwargs):
            """
            Copy all nodes and faces of specified face zones.
            """
            return PyMenu(self.service, "/boundary/manage/copy").execute(*args, **kwargs)
        def change_prefix(self, *args, **kwargs):
            """
            Change the prefix for specified face zones.
            """
            return PyMenu(self.service, "/boundary/manage/change_prefix").execute(*args, **kwargs)
        def change_suffix(self, *args, **kwargs):
            """
            Change the suffix for specified face zones.
            """
            return PyMenu(self.service, "/boundary/manage/change_suffix").execute(*args, **kwargs)
        def create(self, *args, **kwargs):
            """
            Create new face zone.
            """
            return PyMenu(self.service, "/boundary/manage/create").execute(*args, **kwargs)
        def delete(self, *args, **kwargs):
            """
            Delete face zone, leaving nodes.
            """
            return PyMenu(self.service, "/boundary/manage/delete").execute(*args, **kwargs)
        def flip(self, *args, **kwargs):
            """
            Flip the orientation of all face normals on the face zone.
            """
            return PyMenu(self.service, "/boundary/manage/flip").execute(*args, **kwargs)
        def id(self, *args, **kwargs):
            """
            Give zone a new id number.
            """
            return PyMenu(self.service, "/boundary/manage/id").execute(*args, **kwargs)
        def list(self, *args, **kwargs):
            """
            List boundary face zones.
            """
            return PyMenu(self.service, "/boundary/manage/list").execute(*args, **kwargs)
        def merge(self, *args, **kwargs):
            """
            Merge two or more face zones.
            """
            return PyMenu(self.service, "/boundary/manage/merge").execute(*args, **kwargs)
        def name(self, *args, **kwargs):
            """
            Give zone a new name.
            """
            return PyMenu(self.service, "/boundary/manage/name").execute(*args, **kwargs)
        def remove_suffix(self, *args, **kwargs):
            """
            Remove the leftmost ':' and the characters after it in the face zone names.
            """
            return PyMenu(self.service, "/boundary/manage/remove_suffix").execute(*args, **kwargs)
        def orient(self, *args, **kwargs):
            """
            Consistently orient zones.
            """
            return PyMenu(self.service, "/boundary/manage/orient").execute(*args, **kwargs)
        def origin(self, *args, **kwargs):
            """
            Set the origin of the mesh coordinates.
            """
            return PyMenu(self.service, "/boundary/manage/origin").execute(*args, **kwargs)
        def rotate(self, *args, **kwargs):
            """
            Rotate all nodes of specified face zones.
            """
            return PyMenu(self.service, "/boundary/manage/rotate").execute(*args, **kwargs)
        def rotate_model(self, *args, **kwargs):
            """
            Rotate all nodes.
            """
            return PyMenu(self.service, "/boundary/manage/rotate_model").execute(*args, **kwargs)
        def scale(self, *args, **kwargs):
            """
            Scale all nodes of specified face zones.
            """
            return PyMenu(self.service, "/boundary/manage/scale").execute(*args, **kwargs)
        def scale_model(self, *args, **kwargs):
            """
            Scale all nodes.
            """
            return PyMenu(self.service, "/boundary/manage/scale_model").execute(*args, **kwargs)
        def translate(self, *args, **kwargs):
            """
            Translate all nodes of specified face zones.
            """
            return PyMenu(self.service, "/boundary/manage/translate").execute(*args, **kwargs)
        def translate_model(self, *args, **kwargs):
            """
            Translate all nodes.
            """
            return PyMenu(self.service, "/boundary/manage/translate_model").execute(*args, **kwargs)
        def type(self, *args, **kwargs):
            """
            Change face zone type.
            """
            return PyMenu(self.service, "/boundary/manage/type").execute(*args, **kwargs)

        class user_defined_groups(metaclass=PyMenuMeta):
            """
            Collect boundary zones to form logical groups.
            """
            def create(self, *args, **kwargs):
                """
                Create a new User Defined Group.
                """
                return PyMenu(self.service, "/boundary/manage/user_defined_groups/create").execute(*args, **kwargs)
            def activate(self, *args, **kwargs):
                """
                Activate a User Defined Group.
                """
                return PyMenu(self.service, "/boundary/manage/user_defined_groups/activate").execute(*args, **kwargs)
            def update(self, *args, **kwargs):
                """
                Update a User Defined Group.
                """
                return PyMenu(self.service, "/boundary/manage/user_defined_groups/update").execute(*args, **kwargs)
            def delete(self, *args, **kwargs):
                """
                Delete a User Defined Group.
                """
                return PyMenu(self.service, "/boundary/manage/user_defined_groups/delete").execute(*args, **kwargs)
            def list(self, *args, **kwargs):
                """
                List User Defined Groups.
                """
                return PyMenu(self.service, "/boundary/manage/user_defined_groups/list").execute(*args, **kwargs)

    class shell_boundary_layer(metaclass=PyMenuMeta):
        """
        Enter the shell boundary layer menu.
        """
        def create(self, *args, **kwargs):
            """
            Create shell boundary layers from one or more face zones.
            """
            return PyMenu(self.service, "/boundary/shell_boundary_layer/create").execute(*args, **kwargs)

        class controls(metaclass=PyMenuMeta):
            """
            Shell Boundary Layer Controls.
            """

            class zone_specific_growth(metaclass=PyMenuMeta):
                """
                Shell boundary Layer Growth Controls.
                """
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
        Enter manage boundary conditions menu.
        """
        def copy(self, *args, **kwargs):
            """
            Copy boundary conditions.
            """
            return PyMenu(self.service, "/boundary/boundary_conditions/copy").execute(*args, **kwargs)
        def clear(self, *args, **kwargs):
            """
            Clear boundary conditions.
            """
            return PyMenu(self.service, "/boundary/boundary_conditions/clear").execute(*args, **kwargs)
        def clear_all(self, *args, **kwargs):
            """
            Clear all boundary conditions.
            """
            return PyMenu(self.service, "/boundary/boundary_conditions/clear_all").execute(*args, **kwargs)

class cad_assemblies(metaclass=PyMenuMeta):
    """
    Menu for cad assemblies.
    """
    def draw(self, *args, **kwargs):
        """
        Draw CAD assemblies.
        """
        return PyMenu(self.service, "/cad_assemblies/draw").execute(*args, **kwargs)
    def create_objects(self, *args, **kwargs):
        """
        Create Objects from CAD assemblies.
        """
        return PyMenu(self.service, "/cad_assemblies/create_objects").execute(*args, **kwargs)
    def add_to_object(self, *args, **kwargs):
        """
        Add CAD assemblies to existing object.
        """
        return PyMenu(self.service, "/cad_assemblies/add_to_object").execute(*args, **kwargs)
    def replace_object(self, *args, **kwargs):
        """
        Replace CAD assemblies in existing object.
        """
        return PyMenu(self.service, "/cad_assemblies/replace_object").execute(*args, **kwargs)
    def extract_edges_zones(self, *args, **kwargs):
        """
        Extract feature edges for CAD assemblies.
        """
        return PyMenu(self.service, "/cad_assemblies/extract_edges_zones").execute(*args, **kwargs)
    def update_cad_assemblies(self, *args, **kwargs):
        """
        Update CAD assemblies.
        """
        return PyMenu(self.service, "/cad_assemblies/update_cad_assemblies").execute(*args, **kwargs)
    def rename(self, *args, **kwargs):
        """
        Rename CAD entity.
        """
        return PyMenu(self.service, "/cad_assemblies/rename").execute(*args, **kwargs)
    def add_prefix(self, *args, **kwargs):
        """
        Add Prefix to CAD entity.
        """
        return PyMenu(self.service, "/cad_assemblies/add_prefix").execute(*args, **kwargs)
    def delete_cad_assemblies(self, *args, **kwargs):
        """
        Delete CAD Assemblies.
        """
        return PyMenu(self.service, "/cad_assemblies/delete_cad_assemblies").execute(*args, **kwargs)

    class draw_options(metaclass=PyMenuMeta):
        """
        CAD draw options.
        """
        def add_to_graphics(self, *args, **kwargs):
            """
            Add CAD entity to graphics.
            """
            return PyMenu(self.service, "/cad_assemblies/draw_options/add_to_graphics").execute(*args, **kwargs)
        def remove_from_graphics(self, *args, **kwargs):
            """
            Set one object per body, face or object.
            """
            return PyMenu(self.service, "/cad_assemblies/draw_options/remove_from_graphics").execute(*args, **kwargs)
        def draw_unlabelled_zones(self, *args, **kwargs):
            """
            Import edge zones for update.
            """
            return PyMenu(self.service, "/cad_assemblies/draw_options/draw_unlabelled_zones").execute(*args, **kwargs)

    class manage_state(metaclass=PyMenuMeta):
        """
        States for CAD assemblies.
        """
        def unlock(self, *args, **kwargs):
            """
            Unlock CAD assemblies.
            """
            return PyMenu(self.service, "/cad_assemblies/manage_state/unlock").execute(*args, **kwargs)
        def suppress(self, *args, **kwargs):
            """
            Suppress CAD assemblies.
            """
            return PyMenu(self.service, "/cad_assemblies/manage_state/suppress").execute(*args, **kwargs)
        def unsuppress(self, *args, **kwargs):
            """
            Unsuppress CAD assemblies.
            """
            return PyMenu(self.service, "/cad_assemblies/manage_state/unsuppress").execute(*args, **kwargs)

    class labels(metaclass=PyMenuMeta):
        """
        CAD label options.
        """
        def draw(self, *args, **kwargs):
            """
            Draw Labels.
            """
            return PyMenu(self.service, "/cad_assemblies/labels/draw").execute(*args, **kwargs)
        def add_to_graphics(self, *args, **kwargs):
            """
            Add Labels to graphics.
            """
            return PyMenu(self.service, "/cad_assemblies/labels/add_to_graphics").execute(*args, **kwargs)
        def remove_from_graphics(self, *args, **kwargs):
            """
            Remove Labels from graphics.
            """
            return PyMenu(self.service, "/cad_assemblies/labels/remove_from_graphics").execute(*args, **kwargs)
        def delete(self, *args, **kwargs):
            """
            Delete Labels.
            """
            return PyMenu(self.service, "/cad_assemblies/labels/delete").execute(*args, **kwargs)
        def rename(self, *args, **kwargs):
            """
            Rename Labels.
            """
            return PyMenu(self.service, "/cad_assemblies/labels/rename").execute(*args, **kwargs)

    class update_options(metaclass=PyMenuMeta):
        """
        Settings for CAD update.
        """
        def tessellation(self, *args, **kwargs):
            """
            Set tessellation controls for cad import.
            """
            return PyMenu(self.service, "/cad_assemblies/update_options/tessellation").execute(*args, **kwargs)
        def one_zone_per(self, *args, **kwargs):
            """
            Set one object per body, face or object.
            """
            return PyMenu(self.service, "/cad_assemblies/update_options/one_zone_per").execute(*args, **kwargs)
        def one_object_per(self, *args, **kwargs):
            """
            Set one leaf entity per body, part or file.
            """
            return PyMenu(self.service, "/cad_assemblies/update_options/one_object_per").execute(*args, **kwargs)
        def import_edge_zones(self, *args, **kwargs):
            """
            Import edge zones for update.
            """
            return PyMenu(self.service, "/cad_assemblies/update_options/import_edge_zones").execute(*args, **kwargs)

class preferences(metaclass=PyMenuMeta):
    """
    Set preferences.
    """

    class appearance(metaclass=PyMenuMeta):
        """
        .
        """
        def application_font_size(self, *args, **kwargs):
            """
            .
            """
            return PyMenu(self.service, "/preferences/appearance/application_font_size").execute(*args, **kwargs)
        def axis_triad(self, *args, **kwargs):
            """
            .
            """
            return PyMenu(self.service, "/preferences/appearance/axis_triad").execute(*args, **kwargs)
        def color_theme(self, *args, **kwargs):
            """
            .
            """
            return PyMenu(self.service, "/preferences/appearance/color_theme").execute(*args, **kwargs)
        def completer(self, *args, **kwargs):
            """
            .
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
            .
            """
            return PyMenu(self.service, "/preferences/appearance/graphics_background_color1").execute(*args, **kwargs)
        def graphics_background_color2(self, *args, **kwargs):
            """
            .
            """
            return PyMenu(self.service, "/preferences/appearance/graphics_background_color2").execute(*args, **kwargs)
        def graphics_background_style(self, *args, **kwargs):
            """
            .
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
            .
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
            .
            """
            return PyMenu(self.service, "/preferences/appearance/graphics_view").execute(*args, **kwargs)
        def graphics_wall_face_color(self, *args, **kwargs):
            """
            .
            """
            return PyMenu(self.service, "/preferences/appearance/graphics_wall_face_color").execute(*args, **kwargs)
        def group_by_tree_view(self, *args, **kwargs):
            """
            .
            """
            return PyMenu(self.service, "/preferences/appearance/group_by_tree_view").execute(*args, **kwargs)
        def model_color_scheme(self, *args, **kwargs):
            """
            .
            """
            return PyMenu(self.service, "/preferences/appearance/model_color_scheme").execute(*args, **kwargs)
        def number_of_files_recently_used(self, *args, **kwargs):
            """
            .
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
            .
            """
            return PyMenu(self.service, "/preferences/appearance/quick_property_view").execute(*args, **kwargs)
        def ruler(self, *args, **kwargs):
            """
            .
            """
            return PyMenu(self.service, "/preferences/appearance/ruler").execute(*args, **kwargs)
        def show_enabled_models(self, *args, **kwargs):
            """
            .
            """
            return PyMenu(self.service, "/preferences/appearance/show_enabled_models").execute(*args, **kwargs)
        def show_interface_children_zone(self, *args, **kwargs):
            """
            .
            """
            return PyMenu(self.service, "/preferences/appearance/show_interface_children_zone").execute(*args, **kwargs)
        def show_model_edges(self, *args, **kwargs):
            """
            .
            """
            return PyMenu(self.service, "/preferences/appearance/show_model_edges").execute(*args, **kwargs)
        def solution_mode_edge_color_in_meshing_mode(self, *args, **kwargs):
            """
            .
            """
            return PyMenu(self.service, "/preferences/appearance/solution_mode_edge_color_in_meshing_mode").execute(*args, **kwargs)
        def startup_page(self, *args, **kwargs):
            """
            .
            """
            return PyMenu(self.service, "/preferences/appearance/startup_page").execute(*args, **kwargs)
        def surface_emissivity(self, *args, **kwargs):
            """
            .
            """
            return PyMenu(self.service, "/preferences/appearance/surface_emissivity").execute(*args, **kwargs)
        def surface_specularity(self, *args, **kwargs):
            """
            .
            """
            return PyMenu(self.service, "/preferences/appearance/surface_specularity").execute(*args, **kwargs)
        def surface_specularity_for_contours(self, *args, **kwargs):
            """
            .
            """
            return PyMenu(self.service, "/preferences/appearance/surface_specularity_for_contours").execute(*args, **kwargs)
        def titles(self, *args, **kwargs):
            """
            .
            """
            return PyMenu(self.service, "/preferences/appearance/titles").execute(*args, **kwargs)
        def titles_border_offset(self, *args, **kwargs):
            """
            .
            """
            return PyMenu(self.service, "/preferences/appearance/titles_border_offset").execute(*args, **kwargs)

        class ansys_logo(metaclass=PyMenuMeta):
            """
            .
            """
            def color(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/appearance/ansys_logo/color").execute(*args, **kwargs)
            def visible(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/appearance/ansys_logo/visible").execute(*args, **kwargs)

        class charts(metaclass=PyMenuMeta):
            """
            .
            """
            def curve_colors(self, *args, **kwargs):
                """
                .
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
                .
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
            .
            """
            def general_displacement(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/appearance/selections/general_displacement").execute(*args, **kwargs)
            def highlight_edge_color(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/appearance/selections/highlight_edge_color").execute(*args, **kwargs)
            def highlight_edge_weight(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/appearance/selections/highlight_edge_weight").execute(*args, **kwargs)
            def highlight_face_color(self, *args, **kwargs):
                """
                .
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
                .
                """
                return PyMenu(self.service, "/preferences/appearance/selections/highlight_transparency").execute(*args, **kwargs)
            def mouse_hover_probe_values_enabled(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/appearance/selections/mouse_hover_probe_values_enabled").execute(*args, **kwargs)
            def mouse_over_highlight_enabled(self, *args, **kwargs):
                """
                .
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
        .
        """
        def advanced_partition(self, *args, **kwargs):
            """
            .
            """
            return PyMenu(self.service, "/preferences/general/advanced_partition").execute(*args, **kwargs)
        def automatic_transcript(self, *args, **kwargs):
            """
            .
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
        def enable_project_file(self, *args, **kwargs):
            """
            .
            """
            return PyMenu(self.service, "/preferences/general/enable_project_file").execute(*args, **kwargs)
        def flow_model(self, *args, **kwargs):
            """
            .
            """
            return PyMenu(self.service, "/preferences/general/flow_model").execute(*args, **kwargs)
        def idle_timeout(self, *args, **kwargs):
            """
            .
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
        def alpha_features(self, *args, **kwargs):
            """
            .
            """
            return PyMenu(self.service, "/preferences/gpuapp/alpha_features").execute(*args, **kwargs)

    class graphics(metaclass=PyMenuMeta):
        """
        .
        """
        def animation_option(self, *args, **kwargs):
            """
            .
            """
            return PyMenu(self.service, "/preferences/graphics/animation_option").execute(*args, **kwargs)
        def double_buffering(self, *args, **kwargs):
            """
            .
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
            .
            """
            return PyMenu(self.service, "/preferences/graphics/graphics_window_line_width").execute(*args, **kwargs)
        def graphics_window_point_symbol(self, *args, **kwargs):
            """
            .
            """
            return PyMenu(self.service, "/preferences/graphics/graphics_window_point_symbol").execute(*args, **kwargs)
        def hidden_surface_removal_method(self, *args, **kwargs):
            """
            .
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
        def plot_legend_margin(self, *args, **kwargs):
            """
            .
            """
            return PyMenu(self.service, "/preferences/graphics/plot_legend_margin").execute(*args, **kwargs)
        def point_tool_size(self, *args, **kwargs):
            """
            .
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
            .
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
            .
            """
            def color_option(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/boundary_markers/color_option").execute(*args, **kwargs)
            def enabled(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/boundary_markers/enabled").execute(*args, **kwargs)
            def exclude_from_bounding(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/boundary_markers/exclude_from_bounding").execute(*args, **kwargs)
            def inlet_color(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/boundary_markers/inlet_color").execute(*args, **kwargs)
            def marker_fraction(self, *args, **kwargs):
                """
                .
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
                .
                """
                return PyMenu(self.service, "/preferences/graphics/boundary_markers/outlet_color").execute(*args, **kwargs)
            def scale_marker(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/boundary_markers/scale_marker").execute(*args, **kwargs)
            def show_inlet_markers(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/boundary_markers/show_inlet_markers").execute(*args, **kwargs)
            def show_outlet_markers(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/boundary_markers/show_outlet_markers").execute(*args, **kwargs)

        class colormap_settings(metaclass=PyMenuMeta):
            """
            .
            """
            def alignment(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/colormap_settings/alignment").execute(*args, **kwargs)
            def aspect_ratio_when_horizontal(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/colormap_settings/aspect_ratio_when_horizontal").execute(*args, **kwargs)
            def aspect_ratio_when_vertical(self, *args, **kwargs):
                """
                .
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
                .
                """
                return PyMenu(self.service, "/preferences/graphics/colormap_settings/border_style").execute(*args, **kwargs)
            def colormap(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/colormap_settings/colormap").execute(*args, **kwargs)
            def isolines_position_offset(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/colormap_settings/isolines_position_offset").execute(*args, **kwargs)
            def labels(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/colormap_settings/labels").execute(*args, **kwargs)
            def levels(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/colormap_settings/levels").execute(*args, **kwargs)
            def log_scale(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/colormap_settings/log_scale").execute(*args, **kwargs)
            def major_length_to_screen_ratio_when_horizontal(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/colormap_settings/major_length_to_screen_ratio_when_horizontal").execute(*args, **kwargs)
            def major_length_to_screen_ratio_when_vertical(self, *args, **kwargs):
                """
                .
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
                .
                """
                return PyMenu(self.service, "/preferences/graphics/colormap_settings/number_format_precision").execute(*args, **kwargs)
            def number_format_type(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/colormap_settings/number_format_type").execute(*args, **kwargs)
            def show_colormap(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/colormap_settings/show_colormap").execute(*args, **kwargs)
            def skip_value(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/colormap_settings/skip_value").execute(*args, **kwargs)
            def text_behavior(self, *args, **kwargs):
                """
                .
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
                .
                """
                return PyMenu(self.service, "/preferences/graphics/colormap_settings/text_font_automatic_vertical_size").execute(*args, **kwargs)
            def text_font_fixed_horizontal_size(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/colormap_settings/text_font_fixed_horizontal_size").execute(*args, **kwargs)
            def text_font_fixed_size(self, *args, **kwargs):
                """
                .
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
                .
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
            .
            """
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
                .
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
                .
                """
                return PyMenu(self.service, "/preferences/graphics/graphics_effects/grid_color").execute(*args, **kwargs)
            def grid_plane_count(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/graphics_effects/grid_plane_count").execute(*args, **kwargs)
            def grid_plane_enabled(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/graphics_effects/grid_plane_enabled").execute(*args, **kwargs)
            def grid_plane_offset(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/graphics_effects/grid_plane_offset").execute(*args, **kwargs)
            def grid_plane_size_factor(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/graphics_effects/grid_plane_size_factor").execute(*args, **kwargs)
            def plane_direction(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/graphics_effects/plane_direction").execute(*args, **kwargs)
            def reflections_enabled(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/graphics_effects/reflections_enabled").execute(*args, **kwargs)
            def shadow_map_enabled(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/graphics_effects/shadow_map_enabled").execute(*args, **kwargs)
            def show_edge_reflections(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/graphics_effects/show_edge_reflections").execute(*args, **kwargs)
            def show_marker_reflections(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/graphics_effects/show_marker_reflections").execute(*args, **kwargs)
            def simple_shadows_enabled(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/graphics_effects/simple_shadows_enabled").execute(*args, **kwargs)
            def update_after_mouse_release(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/graphics_effects/update_after_mouse_release").execute(*args, **kwargs)

        class hardcopy_settings(metaclass=PyMenuMeta):
            """
            .
            """
            def export_edges_for_avz(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/hardcopy_settings/export_edges_for_avz").execute(*args, **kwargs)
            def hardcopy_driver(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/hardcopy_settings/hardcopy_driver").execute(*args, **kwargs)
            def hardcopy_line_width(self, *args, **kwargs):
                """
                .
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
            .
            """
            def ambient_light_intensity(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/lighting/ambient_light_intensity").execute(*args, **kwargs)
            def headlight(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/lighting/headlight").execute(*args, **kwargs)
            def headlight_intensity(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/lighting/headlight_intensity").execute(*args, **kwargs)
            def lighting_method(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/lighting/lighting_method").execute(*args, **kwargs)

        class manage_hoops_memory(metaclass=PyMenuMeta):
            """
            .
            """
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
            .
            """
            def graphics_window_display_timeout(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/meshing_mode/graphics_window_display_timeout").execute(*args, **kwargs)
            def graphics_window_display_timeout_value(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/graphics/meshing_mode/graphics_window_display_timeout_value").execute(*args, **kwargs)

        class performance(metaclass=PyMenuMeta):
            """
            .
            """
            def optimize_for(self, *args, **kwargs):
                """
                .
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
                .
                """
                def dynamic_adjustment(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/performance/minimum_frame_rate/dynamic_adjustment").execute(*args, **kwargs)
                def enabled(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/performance/minimum_frame_rate/enabled").execute(*args, **kwargs)
                def fixed_culling_value(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/performance/minimum_frame_rate/fixed_culling_value").execute(*args, **kwargs)
                def maximum_culling_threshold(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/performance/minimum_frame_rate/maximum_culling_threshold").execute(*args, **kwargs)
                def minimum_culling_threshold(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/performance/minimum_frame_rate/minimum_culling_threshold").execute(*args, **kwargs)
                def target_fps(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/graphics/performance/minimum_frame_rate/target_fps").execute(*args, **kwargs)

        class transparency(metaclass=PyMenuMeta):
            """
            .
            """
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
        .
        """
        def checkpointing_option(self, *args, **kwargs):
            """
            .
            """
            return PyMenu(self.service, "/preferences/meshing_workflow/checkpointing_option").execute(*args, **kwargs)
        def save_checkpoint_files(self, *args, **kwargs):
            """
            .
            """
            return PyMenu(self.service, "/preferences/meshing_workflow/save_checkpoint_files").execute(*args, **kwargs)
        def temp_folder(self, *args, **kwargs):
            """
            .
            """
            return PyMenu(self.service, "/preferences/meshing_workflow/temp_folder").execute(*args, **kwargs)
        def templates_folder(self, *args, **kwargs):
            """
            .
            """
            return PyMenu(self.service, "/preferences/meshing_workflow/templates_folder").execute(*args, **kwargs)
        def verbosity(self, *args, **kwargs):
            """
            .
            """
            return PyMenu(self.service, "/preferences/meshing_workflow/verbosity").execute(*args, **kwargs)

        class draw_settings(metaclass=PyMenuMeta):
            """
            .
            """
            def auto_draw(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/meshing_workflow/draw_settings/auto_draw").execute(*args, **kwargs)
            def face_zone_limit(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/meshing_workflow/draw_settings/face_zone_limit").execute(*args, **kwargs)
            def facet_limit(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/meshing_workflow/draw_settings/facet_limit").execute(*args, **kwargs)

    class navigation(metaclass=PyMenuMeta):
        """
        .
        """

        class mouse_mapping(metaclass=PyMenuMeta):
            """
            .
            """
            def mousemaptheme(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/navigation/mouse_mapping/mousemaptheme").execute(*args, **kwargs)

            class additional(metaclass=PyMenuMeta):
                """
                .
                """
                def ctrllmbclick(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/navigation/mouse_mapping/additional/ctrllmbclick").execute(*args, **kwargs)
                def ctrllmbdrag(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/navigation/mouse_mapping/additional/ctrllmbdrag").execute(*args, **kwargs)
                def ctrlmmbclick(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/navigation/mouse_mapping/additional/ctrlmmbclick").execute(*args, **kwargs)
                def ctrlmmbdrag(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/navigation/mouse_mapping/additional/ctrlmmbdrag").execute(*args, **kwargs)
                def ctrlrmbclick(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/navigation/mouse_mapping/additional/ctrlrmbclick").execute(*args, **kwargs)
                def ctrlrmbdrag(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/navigation/mouse_mapping/additional/ctrlrmbdrag").execute(*args, **kwargs)
                def mouseprobe(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/navigation/mouse_mapping/additional/mouseprobe").execute(*args, **kwargs)
                def mousewheel(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/navigation/mouse_mapping/additional/mousewheel").execute(*args, **kwargs)
                def mousewheelsensitivity(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/navigation/mouse_mapping/additional/mousewheelsensitivity").execute(*args, **kwargs)
                def reversewheeldirection(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/navigation/mouse_mapping/additional/reversewheeldirection").execute(*args, **kwargs)
                def shiftlmbclick(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/navigation/mouse_mapping/additional/shiftlmbclick").execute(*args, **kwargs)
                def shiftlmbdrag(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/navigation/mouse_mapping/additional/shiftlmbdrag").execute(*args, **kwargs)
                def shiftmmbclick(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/navigation/mouse_mapping/additional/shiftmmbclick").execute(*args, **kwargs)
                def shiftmmbdrag(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/navigation/mouse_mapping/additional/shiftmmbdrag").execute(*args, **kwargs)
                def shiftrmbclick(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/navigation/mouse_mapping/additional/shiftrmbclick").execute(*args, **kwargs)
                def shiftrmbdrag(self, *args, **kwargs):
                    """
                    .
                    """
                    return PyMenu(self.service, "/preferences/navigation/mouse_mapping/additional/shiftrmbdrag").execute(*args, **kwargs)

            class basic(metaclass=PyMenuMeta):
                """
                .
                """
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
            .
            """
            def automatic_plot_file(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/simulation/report_definitions/automatic_plot_file").execute(*args, **kwargs)
            def report_plot_history_data_size(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/simulation/report_definitions/report_plot_history_data_size").execute(*args, **kwargs)

    class turbo_workflow(metaclass=PyMenuMeta):
        """
        .
        """
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
            def auto_draw(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/preferences/turbo_workflow/graphics_settings/auto_draw").execute(*args, **kwargs)

class size_functions(metaclass=PyMenuMeta):
    """
    Manage advanced size functions.
    """
    def create(self, *args, **kwargs):
        """
        Add size function.
        """
        return PyMenu(self.service, "/size_functions/create").execute(*args, **kwargs)
    def delete(self, *args, **kwargs):
        """
        Delete Size Functions.
        """
        return PyMenu(self.service, "/size_functions/delete").execute(*args, **kwargs)
    def delete_all(self, *args, **kwargs):
        """
        Delete All Size Functions.
        """
        return PyMenu(self.service, "/size_functions/delete_all").execute(*args, **kwargs)
    def compute(self, *args, **kwargs):
        """
        Compute Size-functions.
        """
        return PyMenu(self.service, "/size_functions/compute").execute(*args, **kwargs)
    def list(self, *args, **kwargs):
        """
        List all Size function parameters.
        """
        return PyMenu(self.service, "/size_functions/list").execute(*args, **kwargs)
    def create_defaults(self, *args, **kwargs):
        """
        Creates default curvature & proximty size functions acting on all faces and edges.
        """
        return PyMenu(self.service, "/size_functions/create_defaults").execute(*args, **kwargs)
    def set_global_controls(self, *args, **kwargs):
        """
        Set controls for global controls.
        """
        return PyMenu(self.service, "/size_functions/set_global_controls").execute(*args, **kwargs)
    def enable_periodicity_filter(self, *args, **kwargs):
        """
        Enable size field periodicity.
        """
        return PyMenu(self.service, "/size_functions/enable_periodicity_filter").execute(*args, **kwargs)
    def disable_periodicity_filter(self, *args, **kwargs):
        """
        Disable size field periodicity.
        """
        return PyMenu(self.service, "/size_functions/disable_periodicity_filter").execute(*args, **kwargs)
    def list_periodicity_filter(self, *args, **kwargs):
        """
        List periodic in size field.
        """
        return PyMenu(self.service, "/size_functions/list_periodicity_filter").execute(*args, **kwargs)
    def set_scaling_filter(self, *args, **kwargs):
        """
        Set scaling filter on size field.
        """
        return PyMenu(self.service, "/size_functions/set_scaling_filter").execute(*args, **kwargs)
    def reset_global_controls(self, *args, **kwargs):
        """
        Reset controls for global controls.
        """
        return PyMenu(self.service, "/size_functions/reset_global_controls").execute(*args, **kwargs)
    def set_prox_gap_tolerance(self, *args, **kwargs):
        """
        Set proximity min gap tolerance relative to global min-size.
        """
        return PyMenu(self.service, "/size_functions/set_prox_gap_tolerance").execute(*args, **kwargs)
    def triangulate_quad_faces(self, *args, **kwargs):
        """
        Replace non-triangular face zones with triangulated face zones during size field computation.
        """
        return PyMenu(self.service, "/size_functions/triangulate_quad_faces").execute(*args, **kwargs)
    def use_cad_imported_curvature(self, *args, **kwargs):
        """
        Use curvature data imported from CAD.
        """
        return PyMenu(self.service, "/size_functions/use_cad_imported_curvature").execute(*args, **kwargs)

    class contours(metaclass=PyMenuMeta):
        """
        Menu to contour of size field.
        """
        def draw(self, *args, **kwargs):
            """
            Draw size field contour on face zones.
            """
            return PyMenu(self.service, "/size_functions/contours/draw").execute(*args, **kwargs)

        class set(metaclass=PyMenuMeta):
            """
            Set contour options.
            """
            def refine_facets(self, *args, **kwargs):
                """
                Option to refine facets virtually? for better contour resolution.
                """
                return PyMenu(self.service, "/size_functions/contours/set/refine_facets").execute(*args, **kwargs)

    class controls(metaclass=PyMenuMeta):
        """
        Menu to control different behavior of sf.
        """
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
    def create(self, *args, **kwargs):
        """
        Create new scoped sizing.
        """
        return PyMenu(self.service, "/scoped_sizing/create").execute(*args, **kwargs)
    def modify(self, *args, **kwargs):
        """
        Modify scoped sizing.
        """
        return PyMenu(self.service, "/scoped_sizing/modify").execute(*args, **kwargs)
    def delete(self, *args, **kwargs):
        """
        Delete scoped sizing.
        """
        return PyMenu(self.service, "/scoped_sizing/delete").execute(*args, **kwargs)
    def delete_all(self, *args, **kwargs):
        """
        Delete all scoped sizing.
        """
        return PyMenu(self.service, "/scoped_sizing/delete_all").execute(*args, **kwargs)
    def compute(self, *args, **kwargs):
        """
        Compute scoped sizing/functions.
        """
        return PyMenu(self.service, "/scoped_sizing/compute").execute(*args, **kwargs)
    def list(self, *args, **kwargs):
        """
        List all scoped sizing  parameters.
        """
        return PyMenu(self.service, "/scoped_sizing/list").execute(*args, **kwargs)
    def list_zones_uncovered_by_controls(self, *args, **kwargs):
        """
        List all Zones not covered by scoepd sizing.
        """
        return PyMenu(self.service, "/scoped_sizing/list_zones_uncovered_by_controls").execute(*args, **kwargs)
    def delete_size_field(self, *args, **kwargs):
        """
        Reset all the processed sizing functions/scoped sizing.
        """
        return PyMenu(self.service, "/scoped_sizing/delete_size_field").execute(*args, **kwargs)
    def read(self, *args, **kwargs):
        """
        Read scoped sizing from a file.
        """
        return PyMenu(self.service, "/scoped_sizing/read").execute(*args, **kwargs)
    def write(self, *args, **kwargs):
        """
        Write scoped sizing to a file.
        """
        return PyMenu(self.service, "/scoped_sizing/write").execute(*args, **kwargs)
    def validate(self, *args, **kwargs):
        """
        Validate scoped sizing.
        """
        return PyMenu(self.service, "/scoped_sizing/validate").execute(*args, **kwargs)

class objects(metaclass=PyMenuMeta):
    """
    Manage objects.
    """
    def create(self, *args, **kwargs):
        """
        Create an object with closed face zones.
        """
        return PyMenu(self.service, "/objects/create").execute(*args, **kwargs)
    def create_multiple(self, *args, **kwargs):
        """
        Create multiple objects one for each face zone passed.
        """
        return PyMenu(self.service, "/objects/create_multiple").execute(*args, **kwargs)
    def delete(self, *args, **kwargs):
        """
        Delete Objects.
        """
        return PyMenu(self.service, "/objects/delete").execute(*args, **kwargs)
    def delete_all(self, *args, **kwargs):
        """
        Delete all objects.
        """
        return PyMenu(self.service, "/objects/delete_all").execute(*args, **kwargs)
    def delete_all_geom(self, *args, **kwargs):
        """
        Delete all objects of type geom.
        """
        return PyMenu(self.service, "/objects/delete_all_geom").execute(*args, **kwargs)
    def merge(self, *args, **kwargs):
        """
        Merge volume objects.
        """
        return PyMenu(self.service, "/objects/merge").execute(*args, **kwargs)
    def list(self, *args, **kwargs):
        """
        Print existing objects.
        """
        return PyMenu(self.service, "/objects/list").execute(*args, **kwargs)
    def extract_edges(self, *args, **kwargs):
        """
        Extract edges for the Objects.
        """
        return PyMenu(self.service, "/objects/extract_edges").execute(*args, **kwargs)
    def update(self, *args, **kwargs):
        """
        Remove invalid/deleted zones from object's face/edge list.
        """
        return PyMenu(self.service, "/objects/update").execute(*args, **kwargs)
    def merge_walls(self, *args, **kwargs):
        """
        Merge walls of Objects.
        """
        return PyMenu(self.service, "/objects/merge_walls").execute(*args, **kwargs)
    def merge_edges(self, *args, **kwargs):
        """
        Merge edges of Objects.
        """
        return PyMenu(self.service, "/objects/merge_edges").execute(*args, **kwargs)
    def separate_faces_by_angle(self, *args, **kwargs):
        """
        Separate faces of object.
        """
        return PyMenu(self.service, "/objects/separate_faces_by_angle").execute(*args, **kwargs)
    def separate_faces_by_seed(self, *args, **kwargs):
        """
        Separate faces of all object based on given face seed and angle.
        """
        return PyMenu(self.service, "/objects/separate_faces_by_seed").execute(*args, **kwargs)
    def create_and_activate_domain(self, *args, **kwargs):
        """
        Create and activate domain with all face zones of Objects.
        """
        return PyMenu(self.service, "/objects/create_and_activate_domain").execute(*args, **kwargs)
    def create_groups(self, *args, **kwargs):
        """
        Create a face and edge zone group from Objects.
        """
        return PyMenu(self.service, "/objects/create_groups").execute(*args, **kwargs)
    def delete_unreferenced_faces_and_edges(self, *args, **kwargs):
        """
        Delete unreferenced faces and edges.
        """
        return PyMenu(self.service, "/objects/delete_unreferenced_faces_and_edges").execute(*args, **kwargs)
    def improve_object_quality(self, *args, **kwargs):
        """
        Improve mesh objects quality.
        """
        return PyMenu(self.service, "/objects/improve_object_quality").execute(*args, **kwargs)
    def merge_voids(self, *args, **kwargs):
        """
        Merge voids/packets.
        """
        return PyMenu(self.service, "/objects/merge_voids").execute(*args, **kwargs)
    def create_intersection_loops(self, *args, **kwargs):
        """
        Create intersection loops for face zones of objects.
        """
        return PyMenu(self.service, "/objects/create_intersection_loops").execute(*args, **kwargs)
    def change_object_type(self, *args, **kwargs):
        """
        Change object type.
        """
        return PyMenu(self.service, "/objects/change_object_type").execute(*args, **kwargs)
    def improve_feature_capture(self, *args, **kwargs):
        """
        Imprint edges of object on to faces of object.
        """
        return PyMenu(self.service, "/objects/improve_feature_capture").execute(*args, **kwargs)
    def sew(self, *args, **kwargs):
        """
        Enter the sew operation menu.
        """
        return PyMenu(self.service, "/objects/sew").execute(*args, **kwargs)
    def merge_nodes(self, *args, **kwargs):
        """
        Merge nodes of an object.
        """
        return PyMenu(self.service, "/objects/merge_nodes").execute(*args, **kwargs)
    def translate(self, *args, **kwargs):
        """
        Translate objects.
        """
        return PyMenu(self.service, "/objects/translate").execute(*args, **kwargs)
    def rotate(self, *args, **kwargs):
        """
        Rotate objects.
        """
        return PyMenu(self.service, "/objects/rotate").execute(*args, **kwargs)
    def scale(self, *args, **kwargs):
        """
        Scale objects.
        """
        return PyMenu(self.service, "/objects/scale").execute(*args, **kwargs)
    def rename_object_zones(self, *args, **kwargs):
        """
        Rename zones of the objects based on the object name.
        """
        return PyMenu(self.service, "/objects/rename_object_zones").execute(*args, **kwargs)
    def rename_object(self, *args, **kwargs):
        """
        Rename object name.
        """
        return PyMenu(self.service, "/objects/rename_object").execute(*args, **kwargs)
    def check_mesh(self, *args, **kwargs):
        """
        Check mesh.
        """
        return PyMenu(self.service, "/objects/check_mesh").execute(*args, **kwargs)
    def rename_cell_zone_boundaries_using_labels(self, *args, **kwargs):
        """
        Rename cell zone boundaries using the label names.
        """
        return PyMenu(self.service, "/objects/rename_cell_zone_boundaries_using_labels").execute(*args, **kwargs)
    def summary(self, *args, **kwargs):
        """
        List summary by object name or geom/mesh group.
        """
        return PyMenu(self.service, "/objects/summary").execute(*args, **kwargs)
    def restore_faces(self, *args, **kwargs):
        """
        Restore object boundaries.
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
        Objects association with CAD entities.
        """
        def attach_cad(self, *args, **kwargs):
            """
            Attach Object association.
            """
            return PyMenu(self.service, "/objects/cad_association/attach_cad").execute(*args, **kwargs)
        def update_all_objects(self, *args, **kwargs):
            """
            Update all Objects from CAD association.
            """
            return PyMenu(self.service, "/objects/cad_association/update_all_objects").execute(*args, **kwargs)
        def detach_all_objects(self, *args, **kwargs):
            """
            Detach all Objects from CAD association.
            """
            return PyMenu(self.service, "/objects/cad_association/detach_all_objects").execute(*args, **kwargs)
        def update_objects(self, *args, **kwargs):
            """
            Update Objects from CAD association.
            """
            return PyMenu(self.service, "/objects/cad_association/update_objects").execute(*args, **kwargs)
        def detach_objects(self, *args, **kwargs):
            """
            Detach Objects from CAD association.
            """
            return PyMenu(self.service, "/objects/cad_association/detach_objects").execute(*args, **kwargs)
        def query_object_association(self, *args, **kwargs):
            """
            Query Object associations.
            """
            return PyMenu(self.service, "/objects/cad_association/query_object_association").execute(*args, **kwargs)
        def unlock_cad(self, *args, **kwargs):
            """
            Unlock Object associations.
            """
            return PyMenu(self.service, "/objects/cad_association/unlock_cad").execute(*args, **kwargs)
        def restore_cad(self, *args, **kwargs):
            """
            Restore Object associations.
            """
            return PyMenu(self.service, "/objects/cad_association/restore_cad").execute(*args, **kwargs)

    class set(metaclass=PyMenuMeta):
        """
        Set object parameters.
        """
        def set_edge_feature_angle(self, *args, **kwargs):
            """
            Set edge feature angle for edge extraction.
            """
            return PyMenu(self.service, "/objects/set/set_edge_feature_angle").execute(*args, **kwargs)
        def show_face_zones(self, *args, **kwargs):
            """
            Show object faces on display.
            """
            return PyMenu(self.service, "/objects/set/show_face_zones").execute(*args, **kwargs)
        def show_edge_zones(self, *args, **kwargs):
            """
            Show object edges on display.
            """
            return PyMenu(self.service, "/objects/set/show_edge_zones").execute(*args, **kwargs)

    class deprecated(metaclass=PyMenuMeta):
        """
        Deprecated features.
        """
        def create_mesh_object_from_wrap(self, *args, **kwargs):
            """
            Create mesh object from a wrap object.
            """
            return PyMenu(self.service, "/objects/deprecated/create_mesh_object_from_wrap").execute(*args, **kwargs)

    class wrap(metaclass=PyMenuMeta):
        """
        Enter the wrapping operation menu.
        """
        def wrap(self, *args, **kwargs):
            """
            Wrap the object.
            """
            return PyMenu(self.service, "/objects/wrap/wrap").execute(*args, **kwargs)
        def check_holes(self, *args, **kwargs):
            """
            Check for holes on wrapped objects.
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
            Set wrap options.
            """
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
                Include thin cut Face zones and Edge zones.
                """
                return PyMenu(self.service, "/objects/wrap/set/include_thin_cut_edges_and_faces").execute(*args, **kwargs)
            def shrink_wrap_rezone_parameters(self, *args, **kwargs):
                """
                Set wrapper rezone parameters.
                """
                return PyMenu(self.service, "/objects/wrap/set/shrink_wrap_rezone_parameters").execute(*args, **kwargs)
            def zone_name_prefix(self, *args, **kwargs):
                """
                Prefix to be used for names of wrap face zones created.
                """
                return PyMenu(self.service, "/objects/wrap/set/zone_name_prefix").execute(*args, **kwargs)
            def relative_feature_tolerance(self, *args, **kwargs):
                """
                Relative Feature Tolerance.
                """
                return PyMenu(self.service, "/objects/wrap/set/relative_feature_tolerance").execute(*args, **kwargs)
            def minimum_topo_area(self, *args, **kwargs):
                """
                Minimum Topo Area.
                """
                return PyMenu(self.service, "/objects/wrap/set/minimum_topo_area").execute(*args, **kwargs)
            def minimum_relative_topo_area(self, *args, **kwargs):
                """
                Minimum Relative Topo Area.
                """
                return PyMenu(self.service, "/objects/wrap/set/minimum_relative_topo_area").execute(*args, **kwargs)
            def minimum_topo_count(self, *args, **kwargs):
                """
                Minimum Topo Face Count.
                """
                return PyMenu(self.service, "/objects/wrap/set/minimum_topo_count").execute(*args, **kwargs)
            def minimum_relative_topo_count(self, *args, **kwargs):
                """
                Minimum Relative Topo Face Count.
                """
                return PyMenu(self.service, "/objects/wrap/set/minimum_relative_topo_count").execute(*args, **kwargs)
            def resolution_factor(self, *args, **kwargs):
                """
                Resolution Factor.
                """
                return PyMenu(self.service, "/objects/wrap/set/resolution_factor").execute(*args, **kwargs)
            def report_holes(self, *args, **kwargs):
                """
                Detect holes in wrapped objects.
                """
                return PyMenu(self.service, "/objects/wrap/set/report_holes").execute(*args, **kwargs)
            def max_free_edges_for_hole_patching(self, *args, **kwargs):
                """
                Maximum length of free edge loop for filling holes.
                """
                return PyMenu(self.service, "/objects/wrap/set/max_free_edges_for_hole_patching").execute(*args, **kwargs)
            def add_geometry_recovery_level_to_zones(self, *args, **kwargs):
                """
                Update zones with geometry recovery level attributes.
                """
                return PyMenu(self.service, "/objects/wrap/set/add_geometry_recovery_level_to_zones").execute(*args, **kwargs)
            def list_zones_geometry_recovery_levels(self, *args, **kwargs):
                """
                List zones with medium and high geometry recovery levels.
                """
                return PyMenu(self.service, "/objects/wrap/set/list_zones_geometry_recovery_levels").execute(*args, **kwargs)

    class remove_gaps(metaclass=PyMenuMeta):
        """
        Enter the gap removal operation menu.
        """
        def remove_gaps(self, *args, **kwargs):
            """
            Remove gaps between objects or remove thickness in objects.
            """
            return PyMenu(self.service, "/objects/remove_gaps/remove_gaps").execute(*args, **kwargs)
        def show_gaps(self, *args, **kwargs):
            """
            Mark faces at gaps.
            """
            return PyMenu(self.service, "/objects/remove_gaps/show_gaps").execute(*args, **kwargs)
        def ignore_orientation(self, *args, **kwargs):
            """
            Set if gaps should be identified considering orientation.
            """
            return PyMenu(self.service, "/objects/remove_gaps/ignore_orientation").execute(*args, **kwargs)

    class join_intersect(metaclass=PyMenuMeta):
        """
        Join, intersect and build regions in a mesh object.
        """
        def create_mesh_object(self, *args, **kwargs):
            """
            Create mesh object from wrap objects.
            """
            return PyMenu(self.service, "/objects/join_intersect/create_mesh_object").execute(*args, **kwargs)
        def add_objects_to_mesh_object(self, *args, **kwargs):
            """
            Add mesh and wrap objects to a mesh object.
            """
            return PyMenu(self.service, "/objects/join_intersect/add_objects_to_mesh_object").execute(*args, **kwargs)
        def join(self, *args, **kwargs):
            """
            Join all face zones in mesh object.
            """
            return PyMenu(self.service, "/objects/join_intersect/join").execute(*args, **kwargs)
        def intersect(self, *args, **kwargs):
            """
            Intersect all face zones in mesh object.
            """
            return PyMenu(self.service, "/objects/join_intersect/intersect").execute(*args, **kwargs)
        def compute_regions(self, *args, **kwargs):
            """
            Recompute mesh object topo regions.
            """
            return PyMenu(self.service, "/objects/join_intersect/compute_regions").execute(*args, **kwargs)
        def rename_region(self, *args, **kwargs):
            """
            Rename a region in mesh object.
            """
            return PyMenu(self.service, "/objects/join_intersect/rename_region").execute(*args, **kwargs)
        def delete_region(self, *args, **kwargs):
            """
            Delete regions in the object.
            """
            return PyMenu(self.service, "/objects/join_intersect/delete_region").execute(*args, **kwargs)
        def merge_regions(self, *args, **kwargs):
            """
            Merge regions in the object.
            """
            return PyMenu(self.service, "/objects/join_intersect/merge_regions").execute(*args, **kwargs)
        def change_region_type(self, *args, **kwargs):
            """
            Change type of region.
            """
            return PyMenu(self.service, "/objects/join_intersect/change_region_type").execute(*args, **kwargs)
        def list_regions(self, *args, **kwargs):
            """
            List regions of mesh object.
            """
            return PyMenu(self.service, "/objects/join_intersect/list_regions").execute(*args, **kwargs)

        class controls(metaclass=PyMenuMeta):
            """
            Build topology controls.
            """
            def remesh_post_intersection(self, *args, **kwargs):
                """
                Remesh after intersection.
                """
                return PyMenu(self.service, "/objects/join_intersect/controls/remesh_post_intersection").execute(*args, **kwargs)

    class fix_holes(metaclass=PyMenuMeta):
        """
        Fix holes in surface mesh using octree.
        """
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
        Create new mesh objects br wrap or remesh.
        """
        def wrap(self, *args, **kwargs):
            """
            Wrap objects.
            """
            return PyMenu(self.service, "/objects/create_new_mesh_object/wrap").execute(*args, **kwargs)
        def remesh(self, *args, **kwargs):
            """
            Remesh objects.
            """
            return PyMenu(self.service, "/objects/create_new_mesh_object/remesh").execute(*args, **kwargs)

    class labels(metaclass=PyMenuMeta):
        """
        Manage Face Zones Labels of an object.
        """
        def create(self, *args, **kwargs):
            """
            Create a new label with face zones.
            """
            return PyMenu(self.service, "/objects/labels/create").execute(*args, **kwargs)
        def create_label_per_object(self, *args, **kwargs):
            """
            Create label per object.
            """
            return PyMenu(self.service, "/objects/labels/create_label_per_object").execute(*args, **kwargs)
        def rename(self, *args, **kwargs):
            """
            Rename an existing label of an object.
            """
            return PyMenu(self.service, "/objects/labels/rename").execute(*args, **kwargs)
        def merge(self, *args, **kwargs):
            """
            Merge multiple labels of an object.
            """
            return PyMenu(self.service, "/objects/labels/merge").execute(*args, **kwargs)
        def delete(self, *args, **kwargs):
            """
            Delete labels of an object.
            """
            return PyMenu(self.service, "/objects/labels/delete").execute(*args, **kwargs)
        def add_zones(self, *args, **kwargs):
            """
            Add face zones to existing label.
            """
            return PyMenu(self.service, "/objects/labels/add_zones").execute(*args, **kwargs)
        def label_unlabeled_zones(self, *args, **kwargs):
            """
            Label unlabeled zones.
            """
            return PyMenu(self.service, "/objects/labels/label_unlabeled_zones").execute(*args, **kwargs)
        def remove_zones(self, *args, **kwargs):
            """
            Remove face zones from existing label.
            """
            return PyMenu(self.service, "/objects/labels/remove_zones").execute(*args, **kwargs)
        def remove_all_labels_on_zones(self, *args, **kwargs):
            """
            Clear all labels on selected zones.
            """
            return PyMenu(self.service, "/objects/labels/remove_all_labels_on_zones").execute(*args, **kwargs)
        def create_label_per_zone(self, *args, **kwargs):
            """
            Create a label for zone with it's name.
            """
            return PyMenu(self.service, "/objects/labels/create_label_per_zone").execute(*args, **kwargs)

        class cavity(metaclass=PyMenuMeta):
            """
            Enter menu to create cavity using labels.
            """
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
        def compute(self, *args, **kwargs):
            """
            Recompute mesh object topo regions using face zone labels.
            """
            return PyMenu(self.service, "/objects/volumetric_regions/compute").execute(*args, **kwargs)
        def update(self, *args, **kwargs):
            """
            Update mesh object topo regions.
            """
            return PyMenu(self.service, "/objects/volumetric_regions/update").execute(*args, **kwargs)
        def rename(self, *args, **kwargs):
            """
            Rename a region in mesh object.
            """
            return PyMenu(self.service, "/objects/volumetric_regions/rename").execute(*args, **kwargs)
        def delete(self, *args, **kwargs):
            """
            Delete regions in the object.
            """
            return PyMenu(self.service, "/objects/volumetric_regions/delete").execute(*args, **kwargs)
        def merge(self, *args, **kwargs):
            """
            Merge regions in the object.
            """
            return PyMenu(self.service, "/objects/volumetric_regions/merge").execute(*args, **kwargs)
        def change_type(self, *args, **kwargs):
            """
            Change type of region.
            """
            return PyMenu(self.service, "/objects/volumetric_regions/change_type").execute(*args, **kwargs)
        def list(self, *args, **kwargs):
            """
            List regions of mesh object.
            """
            return PyMenu(self.service, "/objects/volumetric_regions/list").execute(*args, **kwargs)
        def auto_fill_volume(self, *args, **kwargs):
            """
            Auto mesh selected regions.
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
            Delete all cell zones assocaited to selected regions.
            """
            return PyMenu(self.service, "/objects/volumetric_regions/delete_cells").execute(*args, **kwargs)

        class scoped_prism(metaclass=PyMenuMeta):
            """
            Enter the scoped prisms menu.
            """
            def generate(self, *args, **kwargs):
                """
                Grow prism into selected region using scoped prism controls.
                """
                return PyMenu(self.service, "/objects/volumetric_regions/scoped_prism/generate").execute(*args, **kwargs)

            class set(metaclass=PyMenuMeta):
                """
                Enter scoped prism settings.
                """
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
            Enter the tetrahedral menu.
            """
            def generate(self, *args, **kwargs):
                """
                Fill empty volume of selected regions with tets.
                """
                return PyMenu(self.service, "/objects/volumetric_regions/tet/generate").execute(*args, **kwargs)

            class set(metaclass=PyMenuMeta):
                """
                Enter tet settings.
                """
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
            Enter the hexcore menu.
            """
            def generate(self, *args, **kwargs):
                """
                Fill empty volume of selected regions with hexcore.
                """
                return PyMenu(self.service, "/objects/volumetric_regions/hexcore/generate").execute(*args, **kwargs)

            class set(metaclass=PyMenuMeta):
                """
                Enter hexcore settings.
                """
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
        Diagnose-face-connectivity.
        """
        def fix_free_faces(self, *args, **kwargs):
            """
            Fix free faces using
            merge-nodes - Individually on each object or on given face zone list
            stitch - Individually on each object or on given face zone list
            delete-free-edge-faces - Of given face zone list or all face zones of given objects
            delete-fringes - Of given face zone list or all face zones of given objects
            delete-skewed-faces - Of given face zone list or all face zones of given objects.
            """
            return PyMenu(self.service, "/diagnostics/face_connectivity/fix_free_faces").execute(*args, **kwargs)
        def fix_multi_faces(self, *args, **kwargs):
            """
            Fix milti faces using
            delete-fringes - Of given face zone list or all face zones of given objects
            delete-overlaps - Of given face zone list or all face zones of given objects
            disconnect - Given face zone list or all face zones of given objects
            all-above - on given face zone list or all face zones of given objects.
            """
            return PyMenu(self.service, "/diagnostics/face_connectivity/fix_multi_faces").execute(*args, **kwargs)
        def fix_self_intersections(self, *args, **kwargs):
            """
            Fix self intersections
            fix-self-intersections - Of given face zone list or all face zones of given objects
            fix-folded-faces - Smooth folded faces of given face zone list or all face zones of given objects.
            """
            return PyMenu(self.service, "/diagnostics/face_connectivity/fix_self_intersections").execute(*args, **kwargs)
        def fix_duplicate_faces(self, *args, **kwargs):
            """
            Fix duplicate faces
            by deleting duplicate faces of given face zone list or all face zones of given objects.
            """
            return PyMenu(self.service, "/diagnostics/face_connectivity/fix_duplicate_faces").execute(*args, **kwargs)
        def fix_spikes(self, *args, **kwargs):
            """
            Fix spikes
            by smoothing spikes from given face zone list or all face zones of given objects.
            """
            return PyMenu(self.service, "/diagnostics/face_connectivity/fix_spikes").execute(*args, **kwargs)
        def fix_islands(self, *args, **kwargs):
            """
            Fix spikes
            by removing islands from given face zone list or all face zones of given objects.
            """
            return PyMenu(self.service, "/diagnostics/face_connectivity/fix_islands").execute(*args, **kwargs)
        def fix_steps(self, *args, **kwargs):
            """
            Fix steps
            smooth - Steps from given face zone list or all face zones of given objects
            collapse - Steps from given face zone list or all face zones of given objects.
            """
            return PyMenu(self.service, "/diagnostics/face_connectivity/fix_steps").execute(*args, **kwargs)
        def fix_slivers(self, *args, **kwargs):
            """
            Fix Slivers
            by collapsing slivers from given face zone list or all face zones of given objects.
            """
            return PyMenu(self.service, "/diagnostics/face_connectivity/fix_slivers").execute(*args, **kwargs)
        def fix_deviations(self, *args, **kwargs):
            """
            Fix deviations
            by imprinting edges for given set of face and edge zones or zones of each object individually.
            """
            return PyMenu(self.service, "/diagnostics/face_connectivity/fix_deviations").execute(*args, **kwargs)
        def fix_point_contacts(self, *args, **kwargs):
            """
            Fix point contacts
            by removing point contacts from given face zone list or all face zones of given objects.
            """
            return PyMenu(self.service, "/diagnostics/face_connectivity/fix_point_contacts").execute(*args, **kwargs)
        def fix_invalid_normals(self, *args, **kwargs):
            """
            Fix invalid normals
            by smoothing invalid normals from given face zone list or all face zones of given objects.
            """
            return PyMenu(self.service, "/diagnostics/face_connectivity/fix_invalid_normals").execute(*args, **kwargs)
        def add_label_to_small_neighbors(self, *args, **kwargs):
            """
            Change small connected islands label to input.
            """
            return PyMenu(self.service, "/diagnostics/face_connectivity/add_label_to_small_neighbors").execute(*args, **kwargs)
        def remove_label_from_small_islands(self, *args, **kwargs):
            """
            Change small disconnected island labels to their connected neighbors.
            """
            return PyMenu(self.service, "/diagnostics/face_connectivity/remove_label_from_small_islands").execute(*args, **kwargs)

    class quality(metaclass=PyMenuMeta):
        """
        Diagnose-face-quality.
        """
        def general_improve(self, *args, **kwargs):
            """
            General Improve
            on  given face zone list or all face zones of given objects.
            """
            return PyMenu(self.service, "/diagnostics/quality/general_improve").execute(*args, **kwargs)
        def smooth(self, *args, **kwargs):
            """
            Smooth individually on each object or on given face zone list.
            """
            return PyMenu(self.service, "/diagnostics/quality/smooth").execute(*args, **kwargs)
        def collapse(self, *args, **kwargs):
            """
            Collapse faces from given face zone list or all face zones of given objects.
            """
            return PyMenu(self.service, "/diagnostics/quality/collapse").execute(*args, **kwargs)
        def delaunay_swap(self, *args, **kwargs):
            """
            Delaunay swap the faces given face zone list or all face zones of given objects.
            """
            return PyMenu(self.service, "/diagnostics/quality/delaunay_swap").execute(*args, **kwargs)

class material_point(metaclass=PyMenuMeta):
    """
    Manage material points.
    """
    def create_material_point(self, *args, **kwargs):
        """
        Add a material point.
        """
        return PyMenu(self.service, "/material_point/create_material_point").execute(*args, **kwargs)
    def delete_material_point(self, *args, **kwargs):
        """
        Delete a material point.
        """
        return PyMenu(self.service, "/material_point/delete_material_point").execute(*args, **kwargs)
    def delete_all_material_points(self, *args, **kwargs):
        """
        Delete all material points.
        """
        return PyMenu(self.service, "/material_point/delete_all_material_points").execute(*args, **kwargs)
    def list_material_points(self, *args, **kwargs):
        """
        List material points.
        """
        return PyMenu(self.service, "/material_point/list_material_points").execute(*args, **kwargs)

class mesh(metaclass=PyMenuMeta):
    """
    Enter the grid menu.
    """
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
        Automatically executes initialization and refinement of mesh.
        """
        return PyMenu(self.service, "/mesh/auto_mesh").execute(*args, **kwargs)
    def auto_mesh_multiple_objects(self, *args, **kwargs):
        """
        Automatically executes initialization and refinement of mesh for multiple objects.
        """
        return PyMenu(self.service, "/mesh/auto_mesh_multiple_objects").execute(*args, **kwargs)
    def check_mesh(self, *args, **kwargs):
        """
        Check mesh for topological errors.
        """
        return PyMenu(self.service, "/mesh/check_mesh").execute(*args, **kwargs)
    def selective_mesh_check(self, *args, **kwargs):
        """
        Selective mesh check.
        """
        return PyMenu(self.service, "/mesh/selective_mesh_check").execute(*args, **kwargs)
    def check_quality(self, *args, **kwargs):
        """
        Check mesh quality.
        """
        return PyMenu(self.service, "/mesh/check_quality").execute(*args, **kwargs)
    def check_quality_level(self, *args, **kwargs):
        """
        Check mesh quality level.
        """
        return PyMenu(self.service, "/mesh/check_quality_level").execute(*args, **kwargs)
    def clear_mesh(self, *args, **kwargs):
        """
        Clear internal mesh, leaving boundary faces.
        """
        return PyMenu(self.service, "/mesh/clear_mesh").execute(*args, **kwargs)
    def clear_undo_stack(self, *args, **kwargs):
        """
        Clears undo stack.
        """
        return PyMenu(self.service, "/mesh/clear_undo_stack").execute(*args, **kwargs)
    def create_heat_exchanger(self, *args, **kwargs):
        """
        Create heat exchanger zones using four points and 3 intervals.
        """
        return PyMenu(self.service, "/mesh/create_heat_exchanger").execute(*args, **kwargs)
    def create_frustrum(self, *args, **kwargs):
        """
        Create a cylindrical hex mesh.
        """
        return PyMenu(self.service, "/mesh/create_frustrum").execute(*args, **kwargs)
    def list_mesh_parameter(self, *args, **kwargs):
        """
        Show all mesh parameters.
        """
        return PyMenu(self.service, "/mesh/list_mesh_parameter").execute(*args, **kwargs)
    def repair_face_handedness(self, *args, **kwargs):
        """
        Reverse face node orientation.
        """
        return PyMenu(self.service, "/mesh/repair_face_handedness").execute(*args, **kwargs)
    def laplace_smooth_nodes(self, *args, **kwargs):
        """
        Laplace smooth nodes.
        """
        return PyMenu(self.service, "/mesh/laplace_smooth_nodes").execute(*args, **kwargs)
    def reset_mesh(self, *args, **kwargs):
        """
        Clear entire mesh.
        """
        return PyMenu(self.service, "/mesh/reset_mesh").execute(*args, **kwargs)
    def reset_mesh_parameter(self, *args, **kwargs):
        """
        Reset all parameters to their default values.
        """
        return PyMenu(self.service, "/mesh/reset_mesh_parameter").execute(*args, **kwargs)
    def auto_prefix_cell_zones(self, *args, **kwargs):
        """
        Prefix cell zones with user defined name.
        """
        return PyMenu(self.service, "/mesh/auto_prefix_cell_zones").execute(*args, **kwargs)
    def cutcell(self, *args, **kwargs):
        """
        Enter the CutCell meshing menu.
        """
        return PyMenu(self.service, "/mesh/cutcell").execute(*args, **kwargs)
    def prepare_for_solve(self, *args, **kwargs):
        """
        Performs the following cleanup operations:
            -Delete dead zones
            -Delete geom and wrap objects
            -Delete all edge zones
            -Delete unused faces
            -Delete unused nodes
        .
        """
        return PyMenu(self.service, "/mesh/prepare_for_solve").execute(*args, **kwargs)
    def zone_names_clean_up(self, *args, **kwargs):
        """
        Cleanup face and cell zone names.
        """
        return PyMenu(self.service, "/mesh/zone_names_clean_up").execute(*args, **kwargs)

    class cartesian(metaclass=PyMenuMeta):
        """
        Enter Cartesian mesh menu.
        """
        def mesh(self, *args, **kwargs):
            """
            Generate Cartesian mesh.
            """
            return PyMenu(self.service, "/mesh/cartesian/mesh").execute(*args, **kwargs)

    class cavity(metaclass=PyMenuMeta):
        """
        Enter cavity menu.
        """
        def replace_zones(self, *args, **kwargs):
            """
            Create a cavity for remeshing.
            """
            return PyMenu(self.service, "/mesh/cavity/replace_zones").execute(*args, **kwargs)
        def add_zones(self, *args, **kwargs):
            """
            Create a cavity for remeshing.
            """
            return PyMenu(self.service, "/mesh/cavity/add_zones").execute(*args, **kwargs)
        def remove_zones(self, *args, **kwargs):
            """
            Create a cavity for remeshing.
            """
            return PyMenu(self.service, "/mesh/cavity/remove_zones").execute(*args, **kwargs)
        def region(self, *args, **kwargs):
            """
            Create a cavity for remeshing.
            """
            return PyMenu(self.service, "/mesh/cavity/region").execute(*args, **kwargs)
        def merge_cavity(self, *args, **kwargs):
            """
            Merge a cavity domain with a domain.
            """
            return PyMenu(self.service, "/mesh/cavity/merge_cavity").execute(*args, **kwargs)
        def create_hexcore_cavity_by_region(self, *args, **kwargs):
            """
            Create a cavity in hexcore mesh for remeshing.
            """
            return PyMenu(self.service, "/mesh/cavity/create_hexcore_cavity_by_region").execute(*args, **kwargs)
        def create_hexcore_cavity_by_scale(self, *args, **kwargs):
            """
            Create a cavity in hexcore mesh for remeshing by scale.
            """
            return PyMenu(self.service, "/mesh/cavity/create_hexcore_cavity_by_scale").execute(*args, **kwargs)
        def remesh_hexcore_cavity(self, *args, **kwargs):
            """
            Remesh a cavity in hexcore mesh.
            """
            return PyMenu(self.service, "/mesh/cavity/remesh_hexcore_cavity").execute(*args, **kwargs)

    class domains(metaclass=PyMenuMeta):
        """
        Enter domains menu.
        """
        def activate(self, *args, **kwargs):
            """
            Activate the domain for subsequent meshing operations.
            .
            """
            return PyMenu(self.service, "/mesh/domains/activate").execute(*args, **kwargs)
        def create_by_cell_zone(self, *args, **kwargs):
            """
            Create new domain using cell zones.
            .
            """
            return PyMenu(self.service, "/mesh/domains/create_by_cell_zone").execute(*args, **kwargs)
        def create_by_point(self, *args, **kwargs):
            """
            Create new domain using material point.
            .
            """
            return PyMenu(self.service, "/mesh/domains/create_by_point").execute(*args, **kwargs)
        def draw(self, *args, **kwargs):
            """
            Draw the boundary face zones of the domain.
            .
            """
            return PyMenu(self.service, "/mesh/domains/draw").execute(*args, **kwargs)
        def create(self, *args, **kwargs):
            """
            Create a new domain by specifying the boundary face zones.
            .
            """
            return PyMenu(self.service, "/mesh/domains/create").execute(*args, **kwargs)
        def delete(self, *args, **kwargs):
            """
            Delete the specified domain.
            .
            """
            return PyMenu(self.service, "/mesh/domains/delete").execute(*args, **kwargs)
        def print(self, *args, **kwargs):
            """
            Print domain content.
            .
            """
            return PyMenu(self.service, "/mesh/domains/print").execute(*args, **kwargs)

    class hexcore(metaclass=PyMenuMeta):
        """
        Enter the hexcore menu.
        """
        def create(self, *args, **kwargs):
            """
            Create hexcore mesh from boundary zone list.
            """
            return PyMenu(self.service, "/mesh/hexcore/create").execute(*args, **kwargs)
        def merge_tets_to_pyramids(self, *args, **kwargs):
            """
            Merge tets into pyramids.
            """
            return PyMenu(self.service, "/mesh/hexcore/merge_tets_to_pyramids").execute(*args, **kwargs)

        class controls(metaclass=PyMenuMeta):
            """
            Enter hexcore controls menu.
            """
            def define_hexcore_extents(self, *args, **kwargs):
                """
                Enables sspecificaton of hexcore outer domain parameters.
                """
                return PyMenu(self.service, "/mesh/hexcore/controls/define_hexcore_extents").execute(*args, **kwargs)
            def buffer_layers(self, *args, **kwargs):
                """
                Number of addition cells to mark for subdivision.
                """
                return PyMenu(self.service, "/mesh/hexcore/controls/buffer_layers").execute(*args, **kwargs)
            def delete_dead_zones(self, *args, **kwargs):
                """
                Delete dead zones after hexcore creation.
                """
                return PyMenu(self.service, "/mesh/hexcore/controls/delete_dead_zones").execute(*args, **kwargs)
            def maximum_cell_length(self, *args, **kwargs):
                """
                Maximum cell length.
                """
                return PyMenu(self.service, "/mesh/hexcore/controls/maximum_cell_length").execute(*args, **kwargs)
            def compute_max_cell_length(self, *args, **kwargs):
                """
                Compute maximum cell length.
                """
                return PyMenu(self.service, "/mesh/hexcore/controls/compute_max_cell_length").execute(*args, **kwargs)
            def maximum_initial_cells(self, *args, **kwargs):
                """
                Maximum number of initial Cartesian cells.
                """
                return PyMenu(self.service, "/mesh/hexcore/controls/maximum_initial_cells").execute(*args, **kwargs)
            def non_fluid_type(self, *args, **kwargs):
                """
                Set non fluid type for cell zones.
                """
                return PyMenu(self.service, "/mesh/hexcore/controls/non_fluid_type").execute(*args, **kwargs)
            def peel_layers(self, *args, **kwargs):
                """
                Number of hexcore cells to peel back from boundary.
                """
                return PyMenu(self.service, "/mesh/hexcore/controls/peel_layers").execute(*args, **kwargs)
            def skip_tet_refinement(self, *args, **kwargs):
                """
                Skip tethedral refinement in transition cell generation.
                """
                return PyMenu(self.service, "/mesh/hexcore/controls/skip_tet_refinement").execute(*args, **kwargs)
            def merge_tets_to_pyramids(self, *args, **kwargs):
                """
                Merge tets into pyramids.
                """
                return PyMenu(self.service, "/mesh/hexcore/controls/merge_tets_to_pyramids").execute(*args, **kwargs)
            def octree_hexcore(self, *args, **kwargs):
                """
                Create hexcore using size-function driven octree.
                """
                return PyMenu(self.service, "/mesh/hexcore/controls/octree_hexcore").execute(*args, **kwargs)
            def avoid_1_by_8_cell_jump_in_hexcore(self, *args, **kwargs):
                """
                Avoid-1:8-cell-jump-in-hexcore.
                """
                return PyMenu(self.service, "/mesh/hexcore/controls/avoid_1_by_8_cell_jump_in_hexcore").execute(*args, **kwargs)
            def set_region_based_sizing(self, *args, **kwargs):
                """
                Set region based sizings.
                """
                return PyMenu(self.service, "/mesh/hexcore/controls/set_region_based_sizing").execute(*args, **kwargs)
            def print_region_based_sizing(self, *args, **kwargs):
                """
                Print region based sizings.
                """
                return PyMenu(self.service, "/mesh/hexcore/controls/print_region_based_sizing").execute(*args, **kwargs)

            class outer_domain_params(metaclass=PyMenuMeta):
                """
                Define outer domain parameters.
                """
                def specify_coordinates(self, *args, **kwargs):
                    """
                    Enables specification of coordinates of hexcore outer box.
                    """
                    return PyMenu(self.service, "/mesh/hexcore/controls/outer_domain_params/specify_coordinates").execute(*args, **kwargs)
                def coordinates(self, *args, **kwargs):
                    """
                    Secifiy coordinates of outer box.
                    """
                    return PyMenu(self.service, "/mesh/hexcore/controls/outer_domain_params/coordinates").execute(*args, **kwargs)
                def specify_boundaries(self, *args, **kwargs):
                    """
                    Set parameters to get hex mesh to boundary(s).
                    """
                    return PyMenu(self.service, "/mesh/hexcore/controls/outer_domain_params/specify_boundaries").execute(*args, **kwargs)
                def boundaries(self, *args, **kwargs):
                    """
                    Set box-aligned zones which  have to be removed from hexcore meshing.
                    """
                    return PyMenu(self.service, "/mesh/hexcore/controls/outer_domain_params/boundaries").execute(*args, **kwargs)
                def auto_align(self, *args, **kwargs):
                    """
                    Enable auto-align?.
                    """
                    return PyMenu(self.service, "/mesh/hexcore/controls/outer_domain_params/auto_align").execute(*args, **kwargs)
                def auto_align_tolerance(self, *args, **kwargs):
                    """
                    Set auto-align-tolerance.
                    """
                    return PyMenu(self.service, "/mesh/hexcore/controls/outer_domain_params/auto_align_tolerance").execute(*args, **kwargs)
                def auto_align_boundaries(self, *args, **kwargs):
                    """
                    Auto-align selected boundaries.
                    """
                    return PyMenu(self.service, "/mesh/hexcore/controls/outer_domain_params/auto_align_boundaries").execute(*args, **kwargs)
                def delete_old_face_zones(self, *args, **kwargs):
                    """
                    Delete replaced old tri face zones.
                    """
                    return PyMenu(self.service, "/mesh/hexcore/controls/outer_domain_params/delete_old_face_zones").execute(*args, **kwargs)
                def list(self, *args, **kwargs):
                    """
                    List the face zones selected for hexcore up to boundaries.
                    """
                    return PyMenu(self.service, "/mesh/hexcore/controls/outer_domain_params/list").execute(*args, **kwargs)

        class local_regions(metaclass=PyMenuMeta):
            """
            Enter the hexcore refine-local menu.
            """
            def activate(self, *args, **kwargs):
                """
                Activate regions for hexcore refinement.
                """
                return PyMenu(self.service, "/mesh/hexcore/local_regions/activate").execute(*args, **kwargs)
            def deactivate(self, *args, **kwargs):
                """
                Activate regions for hexcore refinement.
                """
                return PyMenu(self.service, "/mesh/hexcore/local_regions/deactivate").execute(*args, **kwargs)
            def define(self, *args, **kwargs):
                """
                Define a refinement region's parameters.
                """
                return PyMenu(self.service, "/mesh/hexcore/local_regions/define").execute(*args, **kwargs)
            def delete(self, *args, **kwargs):
                """
                Delete a refinement region.
                """
                return PyMenu(self.service, "/mesh/hexcore/local_regions/delete").execute(*args, **kwargs)
            def init(self, *args, **kwargs):
                """
                Delete all current regions and add the default refinement region.
                """
                return PyMenu(self.service, "/mesh/hexcore/local_regions/init").execute(*args, **kwargs)
            def list_all_regions(self, *args, **kwargs):
                """
                List all refinement regions.
                """
                return PyMenu(self.service, "/mesh/hexcore/local_regions/list_all_regions").execute(*args, **kwargs)
            def ideal_hex_vol(self, *args, **kwargs):
                """
                Ideal hex volume for given edge length.
                """
                return PyMenu(self.service, "/mesh/hexcore/local_regions/ideal_hex_vol").execute(*args, **kwargs)
            def ideal_quad_area(self, *args, **kwargs):
                """
                Ideal quad area for given edge length.
                """
                return PyMenu(self.service, "/mesh/hexcore/local_regions/ideal_quad_area").execute(*args, **kwargs)

    class modify(metaclass=PyMenuMeta):
        """
        Enter the mesh modify menu.
        """
        def clear_selections(self, *args, **kwargs):
            """
            Clear all selections.
            """
            return PyMenu(self.service, "/mesh/modify/clear_selections").execute(*args, **kwargs)
        def extract_unused_nodes(self, *args, **kwargs):
            """
            Extract all unused nodes into a separate interior node zone.
            """
            return PyMenu(self.service, "/mesh/modify/extract_unused_nodes").execute(*args, **kwargs)
        def smooth_node(self, *args, **kwargs):
            """
            Laplace smooth nodes in probe list.
            """
            return PyMenu(self.service, "/mesh/modify/smooth_node").execute(*args, **kwargs)
        def list_selections(self, *args, **kwargs):
            """
            List selections.
            """
            return PyMenu(self.service, "/mesh/modify/list_selections").execute(*args, **kwargs)
        def list_skewed_cells(self, *args, **kwargs):
            """
            List cells between skewness limits.
            """
            return PyMenu(self.service, "/mesh/modify/list_skewed_cells").execute(*args, **kwargs)
        def mesh_node(self, *args, **kwargs):
            """
            Introduce new node into existing mesh.
            """
            return PyMenu(self.service, "/mesh/modify/mesh_node").execute(*args, **kwargs)
        def mesh_nodes_on_zone(self, *args, **kwargs):
            """
            Insert nodes associated with node or face thread into volume mesh.  If a face thread is specified, the faces are deleted before the nodes are introduced into the mesh.
            """
            return PyMenu(self.service, "/mesh/modify/mesh_nodes_on_zone").execute(*args, **kwargs)
        def neighborhood_skew(self, *args, **kwargs):
            """
            Report max skew of all cells using node.
            """
            return PyMenu(self.service, "/mesh/modify/neighborhood_skew").execute(*args, **kwargs)
        def refine_cell(self, *args, **kwargs):
            """
            Refine cells in probe list with node near centroid.
            """
            return PyMenu(self.service, "/mesh/modify/refine_cell").execute(*args, **kwargs)
        def deselect_last(self, *args, **kwargs):
            """
            Deselect last selection.
            """
            return PyMenu(self.service, "/mesh/modify/deselect_last").execute(*args, **kwargs)
        def select_entity(self, *args, **kwargs):
            """
            Select a entity.
            """
            return PyMenu(self.service, "/mesh/modify/select_entity").execute(*args, **kwargs)
        def auto_node_move(self, *args, **kwargs):
            """
            Improve the quality of the mesh by node movement.
            """
            return PyMenu(self.service, "/mesh/modify/auto_node_move").execute(*args, **kwargs)
        def repair_negative_volume_cells(self, *args, **kwargs):
            """
            Improves negative volume cells by node movement.
            """
            return PyMenu(self.service, "/mesh/modify/repair_negative_volume_cells").execute(*args, **kwargs)
        def auto_improve_warp(self, *args, **kwargs):
            """
            Improve the warp of the faces by node movement.
            """
            return PyMenu(self.service, "/mesh/modify/auto_improve_warp").execute(*args, **kwargs)

    class non_conformals(metaclass=PyMenuMeta):
        """
        Enter the non conformals controls menu.
        """
        def create(self, *args, **kwargs):
            """
            Create layer of non conformals on one or more face zones.
            """
            return PyMenu(self.service, "/mesh/non_conformals/create").execute(*args, **kwargs)
        def separate(self, *args, **kwargs):
            """
            Separate non-conformal interfaces between cell zones.
            """
            return PyMenu(self.service, "/mesh/non_conformals/separate").execute(*args, **kwargs)

        class controls(metaclass=PyMenuMeta):
            """
            Enter the non conformals controls menu.
            """
            def enable(self, *args, **kwargs):
                """
                Enable creation of non conformal interface. The quads will be split into tris.
                """
                return PyMenu(self.service, "/mesh/non_conformals/controls/enable").execute(*args, **kwargs)
            def retri_method(self, *args, **kwargs):
                """
                Enable triangulation of non-conformal interfaces instead of quad splitting.
                """
                return PyMenu(self.service, "/mesh/non_conformals/controls/retri_method").execute(*args, **kwargs)

    class rapid_octree(metaclass=PyMenuMeta):
        """
        Enter the octree menu.
        """
        def verbosity(self, *args, **kwargs):
            """
            Set rapid octree verbosity.
            """
            return PyMenu(self.service, "/mesh/rapid_octree/verbosity").execute(*args, **kwargs)
        def estimate_cell_count(self, *args, **kwargs):
            """
            Give a quick estimate about the expected number of cells.
            """
            return PyMenu(self.service, "/mesh/rapid_octree/estimate_cell_count").execute(*args, **kwargs)
        def distribute_geometry(self, *args, **kwargs):
            """
            Distributes input geometry across partitions to reduce memory requirements.
            """
            return PyMenu(self.service, "/mesh/rapid_octree/distribute_geometry").execute(*args, **kwargs)
        def dry_run(self, *args, **kwargs):
            """
            If yes: Just print diagnostic information, do not create a mesh.
            """
            return PyMenu(self.service, "/mesh/rapid_octree/dry_run").execute(*args, **kwargs)
        def undo_last_meshing_operation(self, *args, **kwargs):
            """
            Attempt to undo the last meshing operation.
            """
            return PyMenu(self.service, "/mesh/rapid_octree/undo_last_meshing_operation").execute(*args, **kwargs)
        def boundary_treatment(self, *args, **kwargs):
            """
            Choose the boundary treatment option (0: Projection , 1: Snapping).
            """
            return PyMenu(self.service, "/mesh/rapid_octree/boundary_treatment").execute(*args, **kwargs)
        def bounding_box(self, *args, **kwargs):
            """
            Define/Modify the bounding box around the geometry.
            """
            return PyMenu(self.service, "/mesh/rapid_octree/bounding_box").execute(*args, **kwargs)
        def reset_bounding_box(self, *args, **kwargs):
            """
            Redefine the bounding box extends to encompass the currently selected geoemtry.
            """
            return PyMenu(self.service, "/mesh/rapid_octree/reset_bounding_box").execute(*args, **kwargs)
        def geometry(self, *args, **kwargs):
            """
            Specify the boundary geometry for the Rapid Octree mesher.
            """
            return PyMenu(self.service, "/mesh/rapid_octree/geometry").execute(*args, **kwargs)
        def flow_volume(self, *args, **kwargs):
            """
            Specify the volume to be filled by the mesh.
            """
            return PyMenu(self.service, "/mesh/rapid_octree/flow_volume").execute(*args, **kwargs)
        def create(self, *args, **kwargs):
            """
            Create rapid octree mesh.
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

        class refinement_regions(metaclass=PyMenuMeta):
            """
            Enter the rapid octree refinement region menu.
            """
            def add(self, *args, **kwargs):
                """
                Add a refinement region to the domain.
                """
                return PyMenu(self.service, "/mesh/rapid_octree/refinement_regions/add").execute(*args, **kwargs)
            def delete(self, *args, **kwargs):
                """
                Delete a refinement region.
                """
                return PyMenu(self.service, "/mesh/rapid_octree/refinement_regions/delete").execute(*args, **kwargs)
            def list(self, *args, **kwargs):
                """
                List all refinement regions.
                """
                return PyMenu(self.service, "/mesh/rapid_octree/refinement_regions/list").execute(*args, **kwargs)

        class mesh_sizing(metaclass=PyMenuMeta):
            """
            Define cell sizes.
            """
            def max_cell_size(self, *args, **kwargs):
                """
                Set maximum cell size in octree mesh.
                """
                return PyMenu(self.service, "/mesh/rapid_octree/mesh_sizing/max_cell_size").execute(*args, **kwargs)
            def boundary_cell_size(self, *args, **kwargs):
                """
                Set the default cell size on the geometry.
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
                Define angular threshold and number of refinement levels for features.
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
        Enter the scoped prisms menu.
        """
        def create(self, *args, **kwargs):
            """
            Create prism layers on one or more face zones.
            """
            return PyMenu(self.service, "/mesh/prism/create").execute(*args, **kwargs)
        def mark_ignore_faces(self, *args, **kwargs):
            """
            Mark prism base faces which will be ignored.
            """
            return PyMenu(self.service, "/mesh/prism/mark_ignore_faces").execute(*args, **kwargs)
        def mark_nonmanifold_nodes(self, *args, **kwargs):
            """
            Mark prism base nodes which have invalid manifold around them.
            """
            return PyMenu(self.service, "/mesh/prism/mark_nonmanifold_nodes").execute(*args, **kwargs)
        def mark_proximity_faces(self, *args, **kwargs):
            """
            Mark prism base faces with certain gap.
            """
            return PyMenu(self.service, "/mesh/prism/mark_proximity_faces").execute(*args, **kwargs)
        def list_parameters(self, *args, **kwargs):
            """
            Show all prism mesh parameters.
            """
            return PyMenu(self.service, "/mesh/prism/list_parameters").execute(*args, **kwargs)
        def reset_parameters(self, *args, **kwargs):
            """
            Reset Prism Parameters.
            """
            return PyMenu(self.service, "/mesh/prism/reset_parameters").execute(*args, **kwargs)
        def quality_method(self, *args, **kwargs):
            """
            Set prism quality method.
            """
            return PyMenu(self.service, "/mesh/prism/quality_method").execute(*args, **kwargs)

        class improve(metaclass=PyMenuMeta):
            """
            Prism Improve Menu.
            """
            def smooth_prism_cells(self, *args, **kwargs):
                """
                Optimization based smoothing.
                """
                return PyMenu(self.service, "/mesh/prism/improve/smooth_prism_cells").execute(*args, **kwargs)
            def improve_prism_cells(self, *args, **kwargs):
                """
                Smoothing cells by collecting rings of cells around them.
                """
                return PyMenu(self.service, "/mesh/prism/improve/improve_prism_cells").execute(*args, **kwargs)
            def smooth_improve_prism_cells(self, *args, **kwargs):
                """
                Combination of smooth and improve prism cells.
                """
                return PyMenu(self.service, "/mesh/prism/improve/smooth_improve_prism_cells").execute(*args, **kwargs)
            def smooth_sliver_skew(self, *args, **kwargs):
                """
                Prism Cells above this skewness will be smoothed.
                """
                return PyMenu(self.service, "/mesh/prism/improve/smooth_sliver_skew").execute(*args, **kwargs)
            def smooth_brute_force(self, *args, **kwargs):
                """
                Brute Force smooth cell if cell skewness is still higher after regular smoothing.
                """
                return PyMenu(self.service, "/mesh/prism/improve/smooth_brute_force").execute(*args, **kwargs)
            def smooth_cell_rings(self, *args, **kwargs):
                """
                No. of Cell rings around the skewed cell used by improve-prism-cells.
                """
                return PyMenu(self.service, "/mesh/prism/improve/smooth_cell_rings").execute(*args, **kwargs)

        class post_ignore(metaclass=PyMenuMeta):
            """
            Prism Post-Ignore Menu.
            """
            def mark_prism_cap(self, *args, **kwargs):
                """
                Post mark cell quality ignore cap.
                """
                return PyMenu(self.service, "/mesh/prism/post_ignore/mark_prism_cap").execute(*args, **kwargs)
            def post_remove_cells(self, *args, **kwargs):
                """
                Post cell quality ignore.
                """
                return PyMenu(self.service, "/mesh/prism/post_ignore/post_remove_cells").execute(*args, **kwargs)
            def create_cavity(self, *args, **kwargs):
                """
                Post tet cell quality ignore.
                """
                return PyMenu(self.service, "/mesh/prism/post_ignore/create_cavity").execute(*args, **kwargs)
            def mark_cavity_prism_cap(self, *args, **kwargs):
                """
                Mark post-ignore tet cell cavity prism cap faces.
                """
                return PyMenu(self.service, "/mesh/prism/post_ignore/mark_cavity_prism_cap").execute(*args, **kwargs)

        class split(metaclass=PyMenuMeta):
            """
            Prism Post-Split Menu.
            """
            def split(self, *args, **kwargs):
                """
                Split prism layer cells.
                """
                return PyMenu(self.service, "/mesh/prism/split/split").execute(*args, **kwargs)

        class controls(metaclass=PyMenuMeta):
            """
            Prism Controls.
            """
            def merge_ignored_threads(self, *args, **kwargs):
                """
                Automatically merge all ignored zones related to a base thread into one thread?.
                """
                return PyMenu(self.service, "/mesh/prism/controls/merge_ignored_threads").execute(*args, **kwargs)
            def check_quality(self, *args, **kwargs):
                """
                Check the volume, skewness, and handedness
                of each new cell and face?.
                """
                return PyMenu(self.service, "/mesh/prism/controls/check_quality").execute(*args, **kwargs)
            def remove_invalid_layer(self, *args, **kwargs):
                """
                Remove the last layer if it fails in the quality check.
                """
                return PyMenu(self.service, "/mesh/prism/controls/remove_invalid_layer").execute(*args, **kwargs)
            def set_post_mesh_controls(self, *args, **kwargs):
                """
                Set controls specific to growing prisms post volume mesh.
                """
                return PyMenu(self.service, "/mesh/prism/controls/set_post_mesh_controls").execute(*args, **kwargs)
            def split(self, *args, **kwargs):
                """
                Split prism cells after prism mesh is done.
                """
                return PyMenu(self.service, "/mesh/prism/controls/split").execute(*args, **kwargs)
            def set_overset_prism_controls(self, *args, **kwargs):
                """
                Set boundary layer controls for overset mesh generation.
                """
                return PyMenu(self.service, "/mesh/prism/controls/set_overset_prism_controls").execute(*args, **kwargs)

            class morph(metaclass=PyMenuMeta):
                """
                Morpher Controls.
                """
                def improve_threshold(self, *args, **kwargs):
                    """
                    Quality threshold used during the morpher improve operation.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/morph/improve_threshold").execute(*args, **kwargs)
                def morphing_frequency(self, *args, **kwargs):
                    """
                    Number of layers created between each morphing call.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/morph/morphing_frequency").execute(*args, **kwargs)
                def morphing_convergence_limit(self, *args, **kwargs):
                    """
                    Relative convergence criterion of the iterative linear solver .
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/morph/morphing_convergence_limit").execute(*args, **kwargs)

            class offset(metaclass=PyMenuMeta):
                """
                Prism Offset Controls.
                """
                def min_aspect_ratio(self, *args, **kwargs):
                    """
                    Minimum base-length-over-height for prism cells.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/offset/min_aspect_ratio").execute(*args, **kwargs)
                def first_aspect_ratio_min(self, *args, **kwargs):
                    """
                    Minimum base-length-over-height for prism cells.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/offset/first_aspect_ratio_min").execute(*args, **kwargs)

            class proximity(metaclass=PyMenuMeta):
                """
                Prism Proximity Controls.
                """
                def gap_factor(self, *args, **kwargs):
                    """
                    Gap rate to determine the space in proximity region.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/proximity/gap_factor").execute(*args, **kwargs)
                def allow_ignore(self, *args, **kwargs):
                    """
                    Ignore nodes where shrink factor can't be maintained.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/proximity/allow_ignore").execute(*args, **kwargs)
                def max_shrink_factor(self, *args, **kwargs):
                    """
                    Shrink factor to determine the maximum shrinkage of prism layer.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/proximity/max_shrink_factor").execute(*args, **kwargs)
                def max_aspect_ratio(self, *args, **kwargs):
                    """
                    Minimum offset to fall back to avoid degenerate cells.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/proximity/max_aspect_ratio").execute(*args, **kwargs)
                def allow_shrinkage(self, *args, **kwargs):
                    """
                    Allow shrinkage while growing each layer.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/proximity/allow_shrinkage").execute(*args, **kwargs)
                def keep_first_layer_offsets(self, *args, **kwargs):
                    """
                    Fix first layer offsets while performing proximity detection?.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/proximity/keep_first_layer_offsets").execute(*args, **kwargs)

            class normal(metaclass=PyMenuMeta):
                """
                Prism Normal Controls.
                """
                def ignore_invalid_normals(self, *args, **kwargs):
                    """
                    Ignore nodes which have very poor normals.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/normal/ignore_invalid_normals").execute(*args, **kwargs)
                def direction_method(self, *args, **kwargs):
                    """
                    Grow layers normal to surfaces or along a specified direction vector?.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/normal/direction_method").execute(*args, **kwargs)
                def orient_mesh_object_face_normals(self, *args, **kwargs):
                    """
                    Orient Face Normals Of Mesh Object.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/normal/orient_mesh_object_face_normals").execute(*args, **kwargs)
                def compute_normal(self, *args, **kwargs):
                    """
                    Compute normal for the given face zone.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/normal/compute_normal").execute(*args, **kwargs)
                def direction_vector(self, *args, **kwargs):
                    """
                    Direction vector for prism extrusion.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/normal/direction_vector").execute(*args, **kwargs)
                def bisect_angle(self, *args, **kwargs):
                    """
                    Advancement vectors are forced onto bisecting planes
                    in sharp corners with angles less than this.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/normal/bisect_angle").execute(*args, **kwargs)
                def max_angle_change(self, *args, **kwargs):
                    """
                    Smoothing changes in advancement vectors are constrained by this angle.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/normal/max_angle_change").execute(*args, **kwargs)
                def orthogonal_layers(self, *args, **kwargs):
                    """
                    Number of layers to preserve orthogonality.
                    All smoothing is deferred until after these layers.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/normal/orthogonal_layers").execute(*args, **kwargs)

            class improve(metaclass=PyMenuMeta):
                """
                Prism Smoothing Controls.
                """
                def edge_swap_base_angle(self, *args, **kwargs):
                    """
                    Skewness-driven edge swapping is only allowed between base faces whose normals
                    are within this angle.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/improve/edge_swap_base_angle").execute(*args, **kwargs)
                def edge_swap_cap_angle(self, *args, **kwargs):
                    """
                    Skewness-driven edge swapping is only allowed between cap faces whose normals
                    are within this angle.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/improve/edge_swap_cap_angle").execute(*args, **kwargs)
                def max_allowable_cap_skew(self, *args, **kwargs):
                    """
                    Layer growth is stopped if any cap face has
                    skewness > this value (after all smoothing).
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/improve/max_allowable_cap_skew").execute(*args, **kwargs)
                def max_allowable_cell_skew(self, *args, **kwargs):
                    """
                    Cell quality criteria for smoothing and quality checking.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/improve/max_allowable_cell_skew").execute(*args, **kwargs)
                def corner_height_weight(self, *args, **kwargs):
                    """
                    Improve cell quality/shape by adjusting heights at large corners?.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/improve/corner_height_weight").execute(*args, **kwargs)
                def improve_warp(self, *args, **kwargs):
                    """
                    Perform node movement to improve warp of quad face?.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/improve/improve_warp").execute(*args, **kwargs)
                def face_smooth_skew(self, *args, **kwargs):
                    """
                    Min. skewness to smooth cap faces.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/improve/face_smooth_skew").execute(*args, **kwargs)
                def check_allowable_skew(self, *args, **kwargs):
                    """
                    Check skewness for cap every layer?.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/improve/check_allowable_skew").execute(*args, **kwargs)
                def left_hand_check(self, *args, **kwargs):
                    """
                    Check for left handedness of faces
                    (0 - no check, 1 - only cap faces, 2 - faces of all cells in current layer).
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/improve/left_hand_check").execute(*args, **kwargs)
                def smooth_improve_prism_cells(self, *args, **kwargs):
                    """
                    Smooth and improve prism cells.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/improve/smooth_improve_prism_cells").execute(*args, **kwargs)

            class post_ignore(metaclass=PyMenuMeta):
                """
                Prism Post Ignore Controls.
                """
                def post_remove_cells(self, *args, **kwargs):
                    """
                    Post remove bad prism cells.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/post_ignore/post_remove_cells").execute(*args, **kwargs)

            class adjacent_zone(metaclass=PyMenuMeta):
                """
                Prism Adjacent Zone Controls.
                """
                def side_feature_angle(self, *args, **kwargs):
                    """
                    This angle (degrees) is used for computing feature normals (more flexible than retriangulation-feature-angle).
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/adjacent_zone/side_feature_angle").execute(*args, **kwargs)
                def project_adjacent_angle(self, *args, **kwargs):
                    """
                    Outer edges of advancing layers are projected to
                    adjacent planar zones whose angles relative to the growth direction are
                    less than or equal to this angle.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/adjacent_zone/project_adjacent_angle").execute(*args, **kwargs)

            class zone_specific_growth(metaclass=PyMenuMeta):
                """
                Prism Growth Controls.
                """
                def apply_growth(self, *args, **kwargs):
                    """
                    Apply prism growth on individual zones.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/zone_specific_growth/apply_growth").execute(*args, **kwargs)
                def clear_growth(self, *args, **kwargs):
                    """
                    Clear zone specific growth on individual zones.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/zone_specific_growth/clear_growth").execute(*args, **kwargs)
                def list_growth(self, *args, **kwargs):
                    """
                    List zone specific growth on applied zones.
                    """
                    return PyMenu(self.service, "/mesh/prism/controls/zone_specific_growth/list_growth").execute(*args, **kwargs)

    class pyramid(metaclass=PyMenuMeta):
        """
        Enter the pyramid controls menu.
        """
        def create(self, *args, **kwargs):
            """
            Create layer of pyramids on quad face zone.
            """
            return PyMenu(self.service, "/mesh/pyramid/create").execute(*args, **kwargs)

        class controls(metaclass=PyMenuMeta):
            """
            Enter the pyramid controls menu.
            """
            def neighbor_angle(self, *args, **kwargs):
                """
                Dihedral angle threshold used to limit which neighboring faces are considered in the creation of pyramids.
                """
                return PyMenu(self.service, "/mesh/pyramid/controls/neighbor_angle").execute(*args, **kwargs)
            def offset_scaling(self, *args, **kwargs):
                """
                The node created to produce a pyramid from a face is positioned along a vector emanating from the face centroid in the direction of the face's normal.  This factor scales the distance along this vector, unity represents an equilateral pyramid.
                """
                return PyMenu(self.service, "/mesh/pyramid/controls/offset_scaling").execute(*args, **kwargs)
            def vertex_method(self, *args, **kwargs):
                """
                Method by which offset distances are determined.
                """
                return PyMenu(self.service, "/mesh/pyramid/controls/vertex_method").execute(*args, **kwargs)
            def offset_factor(self, *args, **kwargs):
                """
                Factor of pyramid height used to randomly adjust the height of the pyramids during pyramid creation. Default is 0.
                """
                return PyMenu(self.service, "/mesh/pyramid/controls/offset_factor").execute(*args, **kwargs)

    class thin_volume_mesh(metaclass=PyMenuMeta):
        """
        Enter the thin volume mesh controls menu.
        """
        def create(self, *args, **kwargs):
            """
            Create thin volume mesh on one or more face zones.
            """
            return PyMenu(self.service, "/mesh/thin_volume_mesh/create").execute(*args, **kwargs)

    class separate(metaclass=PyMenuMeta):
        """
        Separate cells by various user defined methods.
        """
        def separate_cell_by_face(self, *args, **kwargs):
            """
            Separate prism cell with source faces.
            """
            return PyMenu(self.service, "/mesh/separate/separate_cell_by_face").execute(*args, **kwargs)
        def separate_cell_by_mark(self, *args, **kwargs):
            """
            Separate cell by marks.
            """
            return PyMenu(self.service, "/mesh/separate/separate_cell_by_mark").execute(*args, **kwargs)
        def separate_prisms_from_poly(self, *args, **kwargs):
            """
            Separate poly-prism cells from poly.
            """
            return PyMenu(self.service, "/mesh/separate/separate_prisms_from_poly").execute(*args, **kwargs)
        def separate_cell_by_region(self, *args, **kwargs):
            """
            Separate cell by region.
            """
            return PyMenu(self.service, "/mesh/separate/separate_cell_by_region").execute(*args, **kwargs)
        def separate_cell_by_shape(self, *args, **kwargs):
            """
            Separate cell thread by cell shape.
            """
            return PyMenu(self.service, "/mesh/separate/separate_cell_by_shape").execute(*args, **kwargs)
        def separate_cell_by_skew(self, *args, **kwargs):
            """
            Separate cell thread by cell skewness.
            """
            return PyMenu(self.service, "/mesh/separate/separate_cell_by_skew").execute(*args, **kwargs)
        def separate_cell_by_size(self, *args, **kwargs):
            """
            Separate cell thread by cell size.
            """
            return PyMenu(self.service, "/mesh/separate/separate_cell_by_size").execute(*args, **kwargs)

        class local_regions(metaclass=PyMenuMeta):
            """
            Enter the refine-local menu.
            """
            def define(self, *args, **kwargs):
                """
                Define a refinement region's parameters.
                """
                return PyMenu(self.service, "/mesh/separate/local_regions/define").execute(*args, **kwargs)
            def delete(self, *args, **kwargs):
                """
                Delete a refinement region.
                """
                return PyMenu(self.service, "/mesh/separate/local_regions/delete").execute(*args, **kwargs)
            def init(self, *args, **kwargs):
                """
                Delete all current regions and add the default refinement region.
                """
                return PyMenu(self.service, "/mesh/separate/local_regions/init").execute(*args, **kwargs)
            def list_all_regions(self, *args, **kwargs):
                """
                List all refinement regions.
                """
                return PyMenu(self.service, "/mesh/separate/local_regions/list_all_regions").execute(*args, **kwargs)

    class tet(metaclass=PyMenuMeta):
        """
        Enter the triangulation menu.
        """
        def delete_virtual_cells(self, *args, **kwargs):
            """
            Delete virtual face/dead cells left by activating keep-virtual-entities?.
            """
            return PyMenu(self.service, "/mesh/tet/delete_virtual_cells").execute(*args, **kwargs)
        def init(self, *args, **kwargs):
            """
            Tet mesh initialization.
            """
            return PyMenu(self.service, "/mesh/tet/init").execute(*args, **kwargs)
        def init_refine(self, *args, **kwargs):
            """
            Tet initialization and refinement of mesh.
            """
            return PyMenu(self.service, "/mesh/tet/init_refine").execute(*args, **kwargs)
        def mesh_object(self, *args, **kwargs):
            """
            Tet mesh object of type mesh.
            """
            return PyMenu(self.service, "/mesh/tet/mesh_object").execute(*args, **kwargs)
        def preserve_cell_zone(self, *args, **kwargs):
            """
            Preserve cell zone.
            """
            return PyMenu(self.service, "/mesh/tet/preserve_cell_zone").execute(*args, **kwargs)
        def un_preserve_cell_zone(self, *args, **kwargs):
            """
            Un-preserve cell zone.
            """
            return PyMenu(self.service, "/mesh/tet/un_preserve_cell_zone").execute(*args, **kwargs)
        def refine(self, *args, **kwargs):
            """
            Tet mesh refinement.
            """
            return PyMenu(self.service, "/mesh/tet/refine").execute(*args, **kwargs)
        def trace_path_between_cells(self, *args, **kwargs):
            """
            Trace path between two cell.
            """
            return PyMenu(self.service, "/mesh/tet/trace_path_between_cells").execute(*args, **kwargs)

        class controls(metaclass=PyMenuMeta):
            """
            Tet controls.
            """
            def cell_sizing(self, *args, **kwargs):
                """
                Allow cell volume distribution to be determined based on boundary.
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
                Computes max cell size.
                """
                return PyMenu(self.service, "/mesh/tet/controls/compute_max_cell_volume").execute(*args, **kwargs)
            def delete_dead_zones(self, *args, **kwargs):
                """
                Automatically delete dead face and cell zones?.
                """
                return PyMenu(self.service, "/mesh/tet/controls/delete_dead_zones").execute(*args, **kwargs)
            def max_cell_length(self, *args, **kwargs):
                """
                Set max-cell-length.
                """
                return PyMenu(self.service, "/mesh/tet/controls/max_cell_length").execute(*args, **kwargs)
            def max_cell_volume(self, *args, **kwargs):
                """
                Set max-cell-volume.
                """
                return PyMenu(self.service, "/mesh/tet/controls/max_cell_volume").execute(*args, **kwargs)
            def use_max_cell_size(self, *args, **kwargs):
                """
                Use max cell size for objects in auto-mesh and do not recompute it based on the object being meshed.
                """
                return PyMenu(self.service, "/mesh/tet/controls/use_max_cell_size").execute(*args, **kwargs)
            def non_fluid_type(self, *args, **kwargs):
                """
                Select the default non-fluid cell zone type.
                """
                return PyMenu(self.service, "/mesh/tet/controls/non_fluid_type").execute(*args, **kwargs)
            def refine_method(self, *args, **kwargs):
                """
                Define refinement method.
                """
                return PyMenu(self.service, "/mesh/tet/controls/refine_method").execute(*args, **kwargs)
            def set_region_based_sizing(self, *args, **kwargs):
                """
                Set region based sizings.
                """
                return PyMenu(self.service, "/mesh/tet/controls/set_region_based_sizing").execute(*args, **kwargs)
            def print_region_based_sizing(self, *args, **kwargs):
                """
                Print region based sizings.
                """
                return PyMenu(self.service, "/mesh/tet/controls/print_region_based_sizing").execute(*args, **kwargs)
            def skewness_method(self, *args, **kwargs):
                """
                Skewness refinement controls.
                """
                return PyMenu(self.service, "/mesh/tet/controls/skewness_method").execute(*args, **kwargs)

            class improve_mesh(metaclass=PyMenuMeta):
                """
                Improve mesh controls.
                """
                def improve(self, *args, **kwargs):
                    """
                    Automatically improve mesh.
                    """
                    return PyMenu(self.service, "/mesh/tet/controls/improve_mesh/improve").execute(*args, **kwargs)
                def swap(self, *args, **kwargs):
                    """
                    Face swap parameters.
                    """
                    return PyMenu(self.service, "/mesh/tet/controls/improve_mesh/swap").execute(*args, **kwargs)
                def skewness_smooth(self, *args, **kwargs):
                    """
                    Skewness smooth parametersx.
                    """
                    return PyMenu(self.service, "/mesh/tet/controls/improve_mesh/skewness_smooth").execute(*args, **kwargs)
                def laplace_smooth(self, *args, **kwargs):
                    """
                    Laplace smooth parameters.
                    """
                    return PyMenu(self.service, "/mesh/tet/controls/improve_mesh/laplace_smooth").execute(*args, **kwargs)

            class adv_front_method(metaclass=PyMenuMeta):
                """
                Advancing front refinement controls.
                """
                def refine_parameters(self, *args, **kwargs):
                    """
                    Define refine parameters.
                    """
                    return PyMenu(self.service, "/mesh/tet/controls/adv_front_method/refine_parameters").execute(*args, **kwargs)
                def first_improve_params(self, *args, **kwargs):
                    """
                    Define refine front improve parameters.
                    """
                    return PyMenu(self.service, "/mesh/tet/controls/adv_front_method/first_improve_params").execute(*args, **kwargs)
                def second_improve_params(self, *args, **kwargs):
                    """
                    Define cell zone improve parameters.
                    """
                    return PyMenu(self.service, "/mesh/tet/controls/adv_front_method/second_improve_params").execute(*args, **kwargs)

                class skew_improve(metaclass=PyMenuMeta):
                    """
                    Refine improve controls.
                    """
                    def boundary_sliver_skew(self, *args, **kwargs):
                        """
                        Refine improve boundary sliver skew.
                        """
                        return PyMenu(self.service, "/mesh/tet/controls/adv_front_method/skew_improve/boundary_sliver_skew").execute(*args, **kwargs)
                    def sliver_skew(self, *args, **kwargs):
                        """
                        Refine improve sliver skew.
                        """
                        return PyMenu(self.service, "/mesh/tet/controls/adv_front_method/skew_improve/sliver_skew").execute(*args, **kwargs)
                    def target(self, *args, **kwargs):
                        """
                        Activate target skew refinement.
                        """
                        return PyMenu(self.service, "/mesh/tet/controls/adv_front_method/skew_improve/target").execute(*args, **kwargs)
                    def target_skew(self, *args, **kwargs):
                        """
                        Refine improve target skew.
                        """
                        return PyMenu(self.service, "/mesh/tet/controls/adv_front_method/skew_improve/target_skew").execute(*args, **kwargs)
                    def target_low_skew(self, *args, **kwargs):
                        """
                        Refine improve target low skew.
                        """
                        return PyMenu(self.service, "/mesh/tet/controls/adv_front_method/skew_improve/target_low_skew").execute(*args, **kwargs)
                    def attempts(self, *args, **kwargs):
                        """
                        Refine improve attempts.
                        """
                        return PyMenu(self.service, "/mesh/tet/controls/adv_front_method/skew_improve/attempts").execute(*args, **kwargs)
                    def iterations(self, *args, **kwargs):
                        """
                        Refine improve iterations.
                        """
                        return PyMenu(self.service, "/mesh/tet/controls/adv_front_method/skew_improve/iterations").execute(*args, **kwargs)

            class remove_slivers(metaclass=PyMenuMeta):
                """
                Sliver remove controls.
                """
                def remove(self, *args, **kwargs):
                    """
                    Automatically remove slivers.
                    """
                    return PyMenu(self.service, "/mesh/tet/controls/remove_slivers/remove").execute(*args, **kwargs)
                def skew(self, *args, **kwargs):
                    """
                    Remove sliver skew.
                    """
                    return PyMenu(self.service, "/mesh/tet/controls/remove_slivers/skew").execute(*args, **kwargs)
                def low_skew(self, *args, **kwargs):
                    """
                    Remove sliver low skew.
                    """
                    return PyMenu(self.service, "/mesh/tet/controls/remove_slivers/low_skew").execute(*args, **kwargs)
                def angle(self, *args, **kwargs):
                    """
                    Max dihedral angle defining a valid boundary sliver.
                    """
                    return PyMenu(self.service, "/mesh/tet/controls/remove_slivers/angle").execute(*args, **kwargs)
                def attempts(self, *args, **kwargs):
                    """
                    Sliver remove attempts.
                    """
                    return PyMenu(self.service, "/mesh/tet/controls/remove_slivers/attempts").execute(*args, **kwargs)
                def iterations(self, *args, **kwargs):
                    """
                    Sliver remove iterations.
                    """
                    return PyMenu(self.service, "/mesh/tet/controls/remove_slivers/iterations").execute(*args, **kwargs)
                def method(self, *args, **kwargs):
                    """
                    Sliver remove method.
                    """
                    return PyMenu(self.service, "/mesh/tet/controls/remove_slivers/method").execute(*args, **kwargs)

            class tet_improve(metaclass=PyMenuMeta):
                """
                Improve cells controls.
                """
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
            Enter the Tet improve menu.
            """
            def swap_faces(self, *args, **kwargs):
                """
                Perform interior face swapping to improve cell skewness.
                """
                return PyMenu(self.service, "/mesh/tet/improve/swap_faces").execute(*args, **kwargs)
            def refine_slivers(self, *args, **kwargs):
                """
                Refine sliver cells by introducing
                node near centroid.
                """
                return PyMenu(self.service, "/mesh/tet/improve/refine_slivers").execute(*args, **kwargs)
            def sliver_boundary_swap(self, *args, **kwargs):
                """
                Remove boundary slivers by moving the boundary
                to exclude the cells from the zone.
                """
                return PyMenu(self.service, "/mesh/tet/improve/sliver_boundary_swap").execute(*args, **kwargs)
            def refine_boundary_slivers(self, *args, **kwargs):
                """
                Refine boundary slivers by edge-split.
                """
                return PyMenu(self.service, "/mesh/tet/improve/refine_boundary_slivers").execute(*args, **kwargs)
            def collapse_slivers(self, *args, **kwargs):
                """
                Remove skewed cells by edge collapse.
                """
                return PyMenu(self.service, "/mesh/tet/improve/collapse_slivers").execute(*args, **kwargs)
            def improve_cells(self, *args, **kwargs):
                """
                Improve skewed cells.
                """
                return PyMenu(self.service, "/mesh/tet/improve/improve_cells").execute(*args, **kwargs)
            def smooth_boundary_sliver(self, *args, **kwargs):
                """
                Smooth skewed cells with all nodes on the boundary.
                """
                return PyMenu(self.service, "/mesh/tet/improve/smooth_boundary_sliver").execute(*args, **kwargs)
            def smooth_interior_sliver(self, *args, **kwargs):
                """
                Smooth skewed cells with some interior node.
                """
                return PyMenu(self.service, "/mesh/tet/improve/smooth_interior_sliver").execute(*args, **kwargs)
            def smooth_nodes(self, *args, **kwargs):
                """
                Smooth node locations.
                """
                return PyMenu(self.service, "/mesh/tet/improve/smooth_nodes").execute(*args, **kwargs)
            def skew_smooth_nodes(self, *args, **kwargs):
                """
                Smooth node locations.
                """
                return PyMenu(self.service, "/mesh/tet/improve/skew_smooth_nodes").execute(*args, **kwargs)

        class local_regions(metaclass=PyMenuMeta):
            """
            Enter the refine-local menu.
            """
            def activate(self, *args, **kwargs):
                """
                Activate regions for tet refinement.
                """
                return PyMenu(self.service, "/mesh/tet/local_regions/activate").execute(*args, **kwargs)
            def deactivate(self, *args, **kwargs):
                """
                Activate regions for tet refinement.
                """
                return PyMenu(self.service, "/mesh/tet/local_regions/deactivate").execute(*args, **kwargs)
            def define(self, *args, **kwargs):
                """
                Define a refinement region's parameters.
                """
                return PyMenu(self.service, "/mesh/tet/local_regions/define").execute(*args, **kwargs)
            def delete(self, *args, **kwargs):
                """
                Delete a refinement region.
                """
                return PyMenu(self.service, "/mesh/tet/local_regions/delete").execute(*args, **kwargs)
            def init(self, *args, **kwargs):
                """
                Delete all current regions and add the default refinement region.
                """
                return PyMenu(self.service, "/mesh/tet/local_regions/init").execute(*args, **kwargs)
            def list_all_regions(self, *args, **kwargs):
                """
                List all refinement regions.
                """
                return PyMenu(self.service, "/mesh/tet/local_regions/list_all_regions").execute(*args, **kwargs)
            def refine(self, *args, **kwargs):
                """
                Refine live cells inside region based on refinement parameters.
                """
                return PyMenu(self.service, "/mesh/tet/local_regions/refine").execute(*args, **kwargs)
            def ideal_vol(self, *args, **kwargs):
                """
                Ideal tet volume for given edge length.
                """
                return PyMenu(self.service, "/mesh/tet/local_regions/ideal_vol").execute(*args, **kwargs)
            def ideal_area(self, *args, **kwargs):
                """
                Ideal triangle area for given edge length.
                """
                return PyMenu(self.service, "/mesh/tet/local_regions/ideal_area").execute(*args, **kwargs)

    class manage(metaclass=PyMenuMeta):
        """
        Enter cell zone menu.
        """
        def adjacent_face_zones(self, *args, **kwargs):
            """
            List all face zones referring the specified cell zone.
            """
            return PyMenu(self.service, "/mesh/manage/adjacent_face_zones").execute(*args, **kwargs)
        def auto_set_active(self, *args, **kwargs):
            """
            Set active zones based on prescribed points.
            """
            return PyMenu(self.service, "/mesh/manage/auto_set_active").execute(*args, **kwargs)
        def active_list(self, *args, **kwargs):
            """
            List active cell zones.
            """
            return PyMenu(self.service, "/mesh/manage/active_list").execute(*args, **kwargs)
        def copy(self, *args, **kwargs):
            """
            Copy the zone.
            """
            return PyMenu(self.service, "/mesh/manage/copy").execute(*args, **kwargs)
        def change_prefix(self, *args, **kwargs):
            """
            Change the prefix for specified face zones.
            """
            return PyMenu(self.service, "/mesh/manage/change_prefix").execute(*args, **kwargs)
        def change_suffix(self, *args, **kwargs):
            """
            Change the suffix for specified face zones.
            """
            return PyMenu(self.service, "/mesh/manage/change_suffix").execute(*args, **kwargs)
        def delete(self, *args, **kwargs):
            """
            Delete cell zone.
            """
            return PyMenu(self.service, "/mesh/manage/delete").execute(*args, **kwargs)
        def id(self, *args, **kwargs):
            """
            Give zone a new id number.
            """
            return PyMenu(self.service, "/mesh/manage/id").execute(*args, **kwargs)
        def list(self, *args, **kwargs):
            """
            List all cell zones.
            """
            return PyMenu(self.service, "/mesh/manage/list").execute(*args, **kwargs)
        def merge(self, *args, **kwargs):
            """
            Merge two or more cell zones.
            """
            return PyMenu(self.service, "/mesh/manage/merge").execute(*args, **kwargs)
        def name(self, *args, **kwargs):
            """
            Give zone a new name.
            """
            return PyMenu(self.service, "/mesh/manage/name").execute(*args, **kwargs)
        def origin(self, *args, **kwargs):
            """
            Set the origin of the mesh coordinates.
            """
            return PyMenu(self.service, "/mesh/manage/origin").execute(*args, **kwargs)
        def rotate(self, *args, **kwargs):
            """
            Rotate all nodes of specified cell zones.
            """
            return PyMenu(self.service, "/mesh/manage/rotate").execute(*args, **kwargs)
        def rotate_model(self, *args, **kwargs):
            """
            Rotate all nodes.
            """
            return PyMenu(self.service, "/mesh/manage/rotate_model").execute(*args, **kwargs)
        def revolve_face_zone(self, *args, **kwargs):
            """
            Generate cells by revolving a face thread.
            """
            return PyMenu(self.service, "/mesh/manage/revolve_face_zone").execute(*args, **kwargs)
        def scale(self, *args, **kwargs):
            """
            Scale all nodes of specified cell zones.
            """
            return PyMenu(self.service, "/mesh/manage/scale").execute(*args, **kwargs)
        def scale_model(self, *args, **kwargs):
            """
            Scale all nodes.
            """
            return PyMenu(self.service, "/mesh/manage/scale_model").execute(*args, **kwargs)
        def set_active(self, *args, **kwargs):
            """
            Refine/swap/display only cells in these cell zones.
            """
            return PyMenu(self.service, "/mesh/manage/set_active").execute(*args, **kwargs)
        def translate(self, *args, **kwargs):
            """
            Translate all nodes of specified cell zones.
            """
            return PyMenu(self.service, "/mesh/manage/translate").execute(*args, **kwargs)
        def translate_model(self, *args, **kwargs):
            """
            Translate all nodes.
            """
            return PyMenu(self.service, "/mesh/manage/translate_model").execute(*args, **kwargs)
        def type(self, *args, **kwargs):
            """
            Change cell zone type.
            """
            return PyMenu(self.service, "/mesh/manage/type").execute(*args, **kwargs)
        def merge_dead_zones(self, *args, **kwargs):
            """
            Merge dead zones.
            """
            return PyMenu(self.service, "/mesh/manage/merge_dead_zones").execute(*args, **kwargs)
        def get_material_point(self, *args, **kwargs):
            """
            Returns material point coordinates for all regions of a cell zone.
            """
            return PyMenu(self.service, "/mesh/manage/get_material_point").execute(*args, **kwargs)

    class cell_zone_conditions(metaclass=PyMenuMeta):
        """
        Enter manage cell zone conditions menu.
        """
        def copy(self, *args, **kwargs):
            """
            Copy cell zone conditions.
            """
            return PyMenu(self.service, "/mesh/cell_zone_conditions/copy").execute(*args, **kwargs)
        def clear(self, *args, **kwargs):
            """
            Clear cell zone conditions.
            """
            return PyMenu(self.service, "/mesh/cell_zone_conditions/clear").execute(*args, **kwargs)
        def clear_all(self, *args, **kwargs):
            """
            Clear all cell zone conditions.
            """
            return PyMenu(self.service, "/mesh/cell_zone_conditions/clear_all").execute(*args, **kwargs)

    class poly(metaclass=PyMenuMeta):
        """
        Enter the poly menu.
        """
        def improve(self, *args, **kwargs):
            """
            Smooth poly mesh.
            """
            return PyMenu(self.service, "/mesh/poly/improve").execute(*args, **kwargs)
        def collapse(self, *args, **kwargs):
            """
            Collapse short edges and small faces.
            """
            return PyMenu(self.service, "/mesh/poly/collapse").execute(*args, **kwargs)
        def remesh(self, *args, **kwargs):
            """
            Remesh local region.
            """
            return PyMenu(self.service, "/mesh/poly/remesh").execute(*args, **kwargs)
        def quality_method(self, *args, **kwargs):
            """
            Set poly quality method.
            """
            return PyMenu(self.service, "/mesh/poly/quality_method").execute(*args, **kwargs)

        class controls(metaclass=PyMenuMeta):
            """
            Poly controls.
            """
            def cell_sizing(self, *args, **kwargs):
                """
                Allow cell volume distribution to be determined based on boundary.
                """
                return PyMenu(self.service, "/mesh/poly/controls/cell_sizing").execute(*args, **kwargs)
            def non_fluid_type(self, *args, **kwargs):
                """
                Select the default non-fluid cell zone type.
                """
                return PyMenu(self.service, "/mesh/poly/controls/non_fluid_type").execute(*args, **kwargs)
            def improve(self, *args, **kwargs):
                """
                Improve the poly mesh by smoothing?.
                """
                return PyMenu(self.service, "/mesh/poly/controls/improve").execute(*args, **kwargs)
            def feature_angle(self, *args, **kwargs):
                """
                Feature angle.
                """
                return PyMenu(self.service, "/mesh/poly/controls/feature_angle").execute(*args, **kwargs)
            def edge_size_ratio(self, *args, **kwargs):
                """
                Size ratio tolerance of two connected edges.
                """
                return PyMenu(self.service, "/mesh/poly/controls/edge_size_ratio").execute(*args, **kwargs)
            def face_size_ratio(self, *args, **kwargs):
                """
                Size ratio tolerance of two faces in one cell.
                """
                return PyMenu(self.service, "/mesh/poly/controls/face_size_ratio").execute(*args, **kwargs)
            def sliver_cell_area_fraction(self, *args, **kwargs):
                """
                Fraction tolerance between face area and cell surface area.
                """
                return PyMenu(self.service, "/mesh/poly/controls/sliver_cell_area_fraction").execute(*args, **kwargs)
            def merge_skew(self, *args, **kwargs):
                """
                Merge minimum skewness.
                """
                return PyMenu(self.service, "/mesh/poly/controls/merge_skew").execute(*args, **kwargs)
            def remesh_skew(self, *args, **kwargs):
                """
                Remesh target skewness.
                """
                return PyMenu(self.service, "/mesh/poly/controls/remesh_skew").execute(*args, **kwargs)

            class smooth_controls(metaclass=PyMenuMeta):
                """
                Poly smooth controls.
                """
                def laplace_smooth_iterations(self, *args, **kwargs):
                    """
                    Laplace smoothing iterations.
                    """
                    return PyMenu(self.service, "/mesh/poly/controls/smooth_controls/laplace_smooth_iterations").execute(*args, **kwargs)
                def edge_smooth_iterations(self, *args, **kwargs):
                    """
                    Edge smoothing iterations.
                    """
                    return PyMenu(self.service, "/mesh/poly/controls/smooth_controls/edge_smooth_iterations").execute(*args, **kwargs)
                def centroid_smooth_iterations(self, *args, **kwargs):
                    """
                    Centroid smoothing iterations.
                    """
                    return PyMenu(self.service, "/mesh/poly/controls/smooth_controls/centroid_smooth_iterations").execute(*args, **kwargs)
                def smooth_iterations(self, *args, **kwargs):
                    """
                    Smooth iterations.
                    """
                    return PyMenu(self.service, "/mesh/poly/controls/smooth_controls/smooth_iterations").execute(*args, **kwargs)
                def smooth_attempts(self, *args, **kwargs):
                    """
                    Smooth attempts.
                    """
                    return PyMenu(self.service, "/mesh/poly/controls/smooth_controls/smooth_attempts").execute(*args, **kwargs)
                def smooth_boundary(self, *args, **kwargs):
                    """
                    Smooth boundary as part of cell smoothing.
                    """
                    return PyMenu(self.service, "/mesh/poly/controls/smooth_controls/smooth_boundary").execute(*args, **kwargs)
                def smooth_on_layer(self, *args, **kwargs):
                    """
                    Smooth poly-prism nodes on layer.
                    """
                    return PyMenu(self.service, "/mesh/poly/controls/smooth_controls/smooth_on_layer").execute(*args, **kwargs)
                def smooth_skew(self, *args, **kwargs):
                    """
                    Smooth minimum skewness.
                    """
                    return PyMenu(self.service, "/mesh/poly/controls/smooth_controls/smooth_skew").execute(*args, **kwargs)

            class prism(metaclass=PyMenuMeta):
                """
                Poly prism transition controls.
                """
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
            Enter the refine-local menu.
            """
            def activate(self, *args, **kwargs):
                """
                Activate regions for tet refinement.
                """
                return PyMenu(self.service, "/mesh/poly/local_regions/activate").execute(*args, **kwargs)
            def deactivate(self, *args, **kwargs):
                """
                Activate regions for tet refinement.
                """
                return PyMenu(self.service, "/mesh/poly/local_regions/deactivate").execute(*args, **kwargs)
            def define(self, *args, **kwargs):
                """
                Define a refinement region's parameters.
                """
                return PyMenu(self.service, "/mesh/poly/local_regions/define").execute(*args, **kwargs)
            def delete(self, *args, **kwargs):
                """
                Delete a refinement region.
                """
                return PyMenu(self.service, "/mesh/poly/local_regions/delete").execute(*args, **kwargs)
            def init(self, *args, **kwargs):
                """
                Delete all current regions and add the default refinement region.
                """
                return PyMenu(self.service, "/mesh/poly/local_regions/init").execute(*args, **kwargs)
            def list_all_regions(self, *args, **kwargs):
                """
                List all refinement regions.
                """
                return PyMenu(self.service, "/mesh/poly/local_regions/list_all_regions").execute(*args, **kwargs)
            def refine(self, *args, **kwargs):
                """
                Refine live cells inside region based on refinement parameters.
                """
                return PyMenu(self.service, "/mesh/poly/local_regions/refine").execute(*args, **kwargs)
            def ideal_vol(self, *args, **kwargs):
                """
                Ideal tet volume for given edge length.
                """
                return PyMenu(self.service, "/mesh/poly/local_regions/ideal_vol").execute(*args, **kwargs)
            def ideal_area(self, *args, **kwargs):
                """
                Ideal triangle area for given edge length.
                """
                return PyMenu(self.service, "/mesh/poly/local_regions/ideal_area").execute(*args, **kwargs)

    class poly_hexcore(metaclass=PyMenuMeta):
        """
        Enter the poly-hexcore menu.
        """

        class controls(metaclass=PyMenuMeta):
            """
            Enter poly-hexcore controls menu.
            """
            def mark_core_region_cell_type_as_hex(self, *args, **kwargs):
                """
                Mark-core-region-cell-type-as-hex?.
                """
                return PyMenu(self.service, "/mesh/poly_hexcore/controls/mark_core_region_cell_type_as_hex").execute(*args, **kwargs)
            def avoid_1_by_8_cell_jump_in_hexcore(self, *args, **kwargs):
                """
                Avoid-1:8-cell-jump-in-hexcore.
                """
                return PyMenu(self.service, "/mesh/poly_hexcore/controls/avoid_1_by_8_cell_jump_in_hexcore").execute(*args, **kwargs)
            def only_polyhedra_for_selected_regions(self, *args, **kwargs):
                """
                Only-polyhedra-for-selected-regions.
                """
                return PyMenu(self.service, "/mesh/poly_hexcore/controls/only_polyhedra_for_selected_regions").execute(*args, **kwargs)

    class auto_mesh_controls(metaclass=PyMenuMeta):
        """
        Automesh controls.
        """
        def backup_object(self, *args, **kwargs):
            """
            Option to create a back up for object.
            """
            return PyMenu(self.service, "/mesh/auto_mesh_controls/backup_object").execute(*args, **kwargs)

    class scoped_prisms(metaclass=PyMenuMeta):
        """
        Manage scoped prisms.
        """
        def create(self, *args, **kwargs):
            """
            Create new scoped prism.
            """
            return PyMenu(self.service, "/mesh/scoped_prisms/create").execute(*args, **kwargs)
        def modify(self, *args, **kwargs):
            """
            Modify scoped prisms.
            """
            return PyMenu(self.service, "/mesh/scoped_prisms/modify").execute(*args, **kwargs)
        def delete(self, *args, **kwargs):
            """
            Delete scoped prisms.
            """
            return PyMenu(self.service, "/mesh/scoped_prisms/delete").execute(*args, **kwargs)
        def list(self, *args, **kwargs):
            """
            List all scoped prisms parameters.
            """
            return PyMenu(self.service, "/mesh/scoped_prisms/list").execute(*args, **kwargs)
        def read(self, *args, **kwargs):
            """
            Read scoped prisms from a file.
            """
            return PyMenu(self.service, "/mesh/scoped_prisms/read").execute(*args, **kwargs)
        def set_no_imprint_zones(self, *args, **kwargs):
            """
            Set zones which should not be imprinted during prism generation.
            """
            return PyMenu(self.service, "/mesh/scoped_prisms/set_no_imprint_zones").execute(*args, **kwargs)
        def write(self, *args, **kwargs):
            """
            Write scoped prisms to a file.
            """
            return PyMenu(self.service, "/mesh/scoped_prisms/write").execute(*args, **kwargs)
        def growth_options(self, *args, **kwargs):
            """
            Set scoped prisms growth options.
            """
            return PyMenu(self.service, "/mesh/scoped_prisms/growth_options").execute(*args, **kwargs)
        def set_overset_prism_controls(self, *args, **kwargs):
            """
            Set boundary layer controls for overset mesh generation.
            """
            return PyMenu(self.service, "/mesh/scoped_prisms/set_overset_prism_controls").execute(*args, **kwargs)
        def set_advanced_controls(self, *args, **kwargs):
            """
            Set scoped boundary layer controls.
            """
            return PyMenu(self.service, "/mesh/scoped_prisms/set_advanced_controls").execute(*args, **kwargs)

class display(metaclass=PyMenuMeta):
    """
    Enter the display menu.
    """
    def annotate(self, *args, **kwargs):
        """
        Add a text annotation string to the active graphics window.
        """
        return PyMenu(self.service, "/display/annotate").execute(*args, **kwargs)
    def boundary_cells(self, *args, **kwargs):
        """
        Display boundary cells on the specified face zones.
        """
        return PyMenu(self.service, "/display/boundary_cells").execute(*args, **kwargs)
    def boundary_grid(self, *args, **kwargs):
        """
        Display boundary zones on the specified face zones.
        """
        return PyMenu(self.service, "/display/boundary_grid").execute(*args, **kwargs)
    def center_view_on(self, *args, **kwargs):
        """
        Set camera target to be center (centroid) of grid node/face/cell.
        """
        return PyMenu(self.service, "/display/center_view_on").execute(*args, **kwargs)
    def clear(self, *args, **kwargs):
        """
        Clear active graphics window.
        """
        return PyMenu(self.service, "/display/clear").execute(*args, **kwargs)
    def clear_annotation(self, *args, **kwargs):
        """
        Delete annotation text.
        """
        return PyMenu(self.service, "/display/clear_annotation").execute(*args, **kwargs)
    def draw_zones(self, *args, **kwargs):
        """
        Draw the specified zones using the default grid parameters.
        """
        return PyMenu(self.service, "/display/draw_zones").execute(*args, **kwargs)
    def draw_cells_using_faces(self, *args, **kwargs):
        """
        Draw cells using selected faces.
        """
        return PyMenu(self.service, "/display/draw_cells_using_faces").execute(*args, **kwargs)
    def draw_cells_using_nodes(self, *args, **kwargs):
        """
        Draw cells using selected nodes.
        """
        return PyMenu(self.service, "/display/draw_cells_using_nodes").execute(*args, **kwargs)
    def draw_face_zones_using_entities(self, *args, **kwargs):
        """
        Draw face zone connected to node.
        """
        return PyMenu(self.service, "/display/draw_face_zones_using_entities").execute(*args, **kwargs)
    def all_grid(self, *args, **kwargs):
        """
        Display grid zones according to parameters in set-grid.
        """
        return PyMenu(self.service, "/display/all_grid").execute(*args, **kwargs)
    def save_picture(self, *args, **kwargs):
        """
        Generate a "hardcopy" of the active window.
        """
        return PyMenu(self.service, "/display/save_picture").execute(*args, **kwargs)
    def redisplay(self, *args, **kwargs):
        """
        Re-display grid.
        """
        return PyMenu(self.service, "/display/redisplay").execute(*args, **kwargs)
    def show_hide_clipping_plane_triad(self, *args, **kwargs):
        """
        Show/Hide clipping plane triad.
        """
        return PyMenu(self.service, "/display/show_hide_clipping_plane_triad").execute(*args, **kwargs)
    def set_list_tree_separator(self, *args, **kwargs):
        """
        Set the separator character for list tree.
        """
        return PyMenu(self.service, "/display/set_list_tree_separator").execute(*args, **kwargs)
    def update_layout(self, *args, **kwargs):
        """
        Update the fluent layout.
        """
        return PyMenu(self.service, "/display/update_layout").execute(*args, **kwargs)

    class set(metaclass=PyMenuMeta):
        """
        Menu to set display parameters.
        """
        def highlight_tree_selection(self, *args, **kwargs):
            """
            Turn on/off outline display of tree selection in graphics window.
            """
            return PyMenu(self.service, "/display/set/highlight_tree_selection").execute(*args, **kwargs)
        def remote_display_defaults(self, *args, **kwargs):
            """
            Apply display settings recommended for remote display.
            """
            return PyMenu(self.service, "/display/set/remote_display_defaults").execute(*args, **kwargs)
        def native_display_defaults(self, *args, **kwargs):
            """
            Apply display settings recommended for native display.
            """
            return PyMenu(self.service, "/display/set/native_display_defaults").execute(*args, **kwargs)
        def edges(self, *args, **kwargs):
            """
            Turn on/off display of face/cell edges.
            """
            return PyMenu(self.service, "/display/set/edges").execute(*args, **kwargs)
        def filled_grid(self, *args, **kwargs):
            """
            Turn on/off filled grid option.
            """
            return PyMenu(self.service, "/display/set/filled_grid").execute(*args, **kwargs)
        def quick_moves_algorithm(self, *args, **kwargs):
            """
            Select quick moves algorithm for icons and helptext overlay.
            """
            return PyMenu(self.service, "/display/set/quick_moves_algorithm").execute(*args, **kwargs)
        def line_weight(self, *args, **kwargs):
            """
            Set the window's line-weight factor.
            """
            return PyMenu(self.service, "/display/set/line_weight").execute(*args, **kwargs)
        def overlays(self, *args, **kwargs):
            """
            Turn on/off overlays.
            """
            return PyMenu(self.service, "/display/set/overlays").execute(*args, **kwargs)
        def re_render(self, *args, **kwargs):
            """
            Re-render current window after modifying variables in set menu.
            """
            return PyMenu(self.service, "/display/set/re_render").execute(*args, **kwargs)
        def reset_graphics(self, *args, **kwargs):
            """
            Reset the graphics system.
            """
            return PyMenu(self.service, "/display/set/reset_graphics").execute(*args, **kwargs)
        def shrink_factor(self, *args, **kwargs):
            """
            Set grid shrink factor.
            """
            return PyMenu(self.service, "/display/set/shrink_factor").execute(*args, **kwargs)
        def title(self, *args, **kwargs):
            """
            Set problem title.
            """
            return PyMenu(self.service, "/display/set/title").execute(*args, **kwargs)

        class colors(metaclass=PyMenuMeta):
            """
            Color options menu.
            """
            def background(self, *args, **kwargs):
                """
                Set the background (window) color.
                """
                return PyMenu(self.service, "/display/set/colors/background").execute(*args, **kwargs)
            def color_by_type(self, *args, **kwargs):
                """
                Determine whether to color meshes by type or by surface (ID).
                """
                return PyMenu(self.service, "/display/set/colors/color_by_type").execute(*args, **kwargs)
            def foreground(self, *args, **kwargs):
                """
                Set the foreground (text and window frame) color.
                """
                return PyMenu(self.service, "/display/set/colors/foreground").execute(*args, **kwargs)
            def far_field_faces(self, *args, **kwargs):
                """
                Set the color of far field faces.
                """
                return PyMenu(self.service, "/display/set/colors/far_field_faces").execute(*args, **kwargs)
            def inlet_faces(self, *args, **kwargs):
                """
                Set the color of inlet faces.
                """
                return PyMenu(self.service, "/display/set/colors/inlet_faces").execute(*args, **kwargs)
            def interior_faces(self, *args, **kwargs):
                """
                Set the color of interior faces.
                """
                return PyMenu(self.service, "/display/set/colors/interior_faces").execute(*args, **kwargs)
            def internal_faces(self, *args, **kwargs):
                """
                Set the color of internal interface faces.
                """
                return PyMenu(self.service, "/display/set/colors/internal_faces").execute(*args, **kwargs)
            def outlet_faces(self, *args, **kwargs):
                """
                Set the color of outlet faces.
                """
                return PyMenu(self.service, "/display/set/colors/outlet_faces").execute(*args, **kwargs)
            def overset_faces(self, *args, **kwargs):
                """
                Set the color of overset faces.
                """
                return PyMenu(self.service, "/display/set/colors/overset_faces").execute(*args, **kwargs)
            def periodic_faces(self, *args, **kwargs):
                """
                Set the color of periodic faces.
                """
                return PyMenu(self.service, "/display/set/colors/periodic_faces").execute(*args, **kwargs)
            def rans_les_interface_faces(self, *args, **kwargs):
                """
                Set the color of RANS/LES interface faces.
                """
                return PyMenu(self.service, "/display/set/colors/rans_les_interface_faces").execute(*args, **kwargs)
            def reset_user_colors(self, *args, **kwargs):
                """
                Reset all user colors.
                """
                return PyMenu(self.service, "/display/set/colors/reset_user_colors").execute(*args, **kwargs)
            def show_user_colors(self, *args, **kwargs):
                """
                List currently defined user colors.
                """
                return PyMenu(self.service, "/display/set/colors/show_user_colors").execute(*args, **kwargs)
            def symmetry_faces(self, *args, **kwargs):
                """
                Set the color of symmetric faces.
                """
                return PyMenu(self.service, "/display/set/colors/symmetry_faces").execute(*args, **kwargs)
            def axis_faces(self, *args, **kwargs):
                """
                Set the color of axisymmetric faces.
                """
                return PyMenu(self.service, "/display/set/colors/axis_faces").execute(*args, **kwargs)
            def free_surface_faces(self, *args, **kwargs):
                """
                Set the color of free-surface faces.
                """
                return PyMenu(self.service, "/display/set/colors/free_surface_faces").execute(*args, **kwargs)
            def traction_faces(self, *args, **kwargs):
                """
                Set the color of traction faces.
                """
                return PyMenu(self.service, "/display/set/colors/traction_faces").execute(*args, **kwargs)
            def user_color(self, *args, **kwargs):
                """
                Explicitly set color of display zone.
                """
                return PyMenu(self.service, "/display/set/colors/user_color").execute(*args, **kwargs)
            def wall_faces(self, *args, **kwargs):
                """
                Set the color of wall faces.
                """
                return PyMenu(self.service, "/display/set/colors/wall_faces").execute(*args, **kwargs)
            def interface_faces(self, *args, **kwargs):
                """
                Set the color of mesh Interfaces.
                """
                return PyMenu(self.service, "/display/set/colors/interface_faces").execute(*args, **kwargs)
            def list(self, *args, **kwargs):
                """
                List available colors.
                """
                return PyMenu(self.service, "/display/set/colors/list").execute(*args, **kwargs)
            def reset_colors(self, *args, **kwargs):
                """
                Reset individual mesh surface colors to the defaults.
                """
                return PyMenu(self.service, "/display/set/colors/reset_colors").execute(*args, **kwargs)
            def surface(self, *args, **kwargs):
                """
                Set the color of surfaces.
                """
                return PyMenu(self.service, "/display/set/colors/surface").execute(*args, **kwargs)
            def skip_label(self, *args, **kwargs):
                """
                Set the number of labels to be skipped in the colopmap scale.
                """
                return PyMenu(self.service, "/display/set/colors/skip_label").execute(*args, **kwargs)
            def automatic_skip(self, *args, **kwargs):
                """
                Determine whether to skip labels in the colopmap scale automatically.
                """
                return PyMenu(self.service, "/display/set/colors/automatic_skip").execute(*args, **kwargs)
            def graphics_color_theme(self, *args, **kwargs):
                """
                Enter the graphics color theme menu.
                """
                return PyMenu(self.service, "/display/set/colors/graphics_color_theme").execute(*args, **kwargs)

            class by_type(metaclass=PyMenuMeta):
                """
                Enter the zone type color and material assignment menu.
                """
                def only_list_case_boundaries(self, *args, **kwargs):
                    """
                    Only list the boundary types that are assigned in this case.
                    """
                    return PyMenu(self.service, "/display/set/colors/by_type/only_list_case_boundaries").execute(*args, **kwargs)
                def reset(self, *args, **kwargs):
                    """
                    To reset colors and/or materials to the defaults.
                    """
                    return PyMenu(self.service, "/display/set/colors/by_type/reset").execute(*args, **kwargs)

                class type_name(metaclass=PyMenuMeta):
                    """
                    Select the boundary type to specify colors and/or materials.
                    """

                    class axis(metaclass=PyMenuMeta):
                        """
                        Set the material and/or color for the selected boundary type.
                        """
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

        class picture(metaclass=PyMenuMeta):
            """
            Hardcopy options menu.
            """
            def invert_background(self, *args, **kwargs):
                """
                Use a white background when the picture is saved.
                """
                return PyMenu(self.service, "/display/set/picture/invert_background").execute(*args, **kwargs)
            def landscape(self, *args, **kwargs):
                """
                Plot hardcopies in landscape or portrait orientation.
                """
                return PyMenu(self.service, "/display/set/picture/landscape").execute(*args, **kwargs)
            def preview(self, *args, **kwargs):
                """
                Display a preview image of a hardcopy.
                """
                return PyMenu(self.service, "/display/set/picture/preview").execute(*args, **kwargs)
            def x_resolution(self, *args, **kwargs):
                """
                Set the width of raster-formatted images in pixels (0 implies current window size).
                """
                return PyMenu(self.service, "/display/set/picture/x_resolution").execute(*args, **kwargs)
            def y_resolution(self, *args, **kwargs):
                """
                Set the height of raster-formatted images in pixels (0 implies current window size).
                """
                return PyMenu(self.service, "/display/set/picture/y_resolution").execute(*args, **kwargs)
            def dpi(self, *args, **kwargs):
                """
                Set the DPI for EPS and Postscript files, specifies the resolution in dots per inch (DPI) instead of setting the width and height.
                """
                return PyMenu(self.service, "/display/set/picture/dpi").execute(*args, **kwargs)
            def use_window_resolution(self, *args, **kwargs):
                """
                Use the currently active window's resolution for hardcopy (ignores the x-resolution and y-resolution in this case).
                """
                return PyMenu(self.service, "/display/set/picture/use_window_resolution").execute(*args, **kwargs)
            def set_standard_resolution(self, *args, **kwargs):
                """
                Select from pre-defined resolution list.
                """
                return PyMenu(self.service, "/display/set/picture/set_standard_resolution").execute(*args, **kwargs)
            def jpeg_hardcopy_quality(self, *args, **kwargs):
                """
                To set jpeg hardcopy quality.
                """
                return PyMenu(self.service, "/display/set/picture/jpeg_hardcopy_quality").execute(*args, **kwargs)

            class color_mode(metaclass=PyMenuMeta):
                """
                Enter the hardcopy color mode menu.
                """
                def color(self, *args, **kwargs):
                    """
                    Plot hardcopies in color.
                    """
                    return PyMenu(self.service, "/display/set/picture/color_mode/color").execute(*args, **kwargs)
                def gray_scale(self, *args, **kwargs):
                    """
                    Convert color to grayscale for hardcopy.
                    """
                    return PyMenu(self.service, "/display/set/picture/color_mode/gray_scale").execute(*args, **kwargs)
                def mono_chrome(self, *args, **kwargs):
                    """
                    Convert color to monochrome (black and white) for hardcopy.
                    """
                    return PyMenu(self.service, "/display/set/picture/color_mode/mono_chrome").execute(*args, **kwargs)
                def list(self, *args, **kwargs):
                    """
                    Display the current hardcopy color mode.
                    """
                    return PyMenu(self.service, "/display/set/picture/color_mode/list").execute(*args, **kwargs)

            class driver(metaclass=PyMenuMeta):
                """
                Enter the set hardcopy driver menu.
                """
                def dump_window(self, *args, **kwargs):
                    """
                    Set the command used to dump the graphics window to a file.
                    """
                    return PyMenu(self.service, "/display/set/picture/driver/dump_window").execute(*args, **kwargs)
                def eps(self, *args, **kwargs):
                    """
                    Produce encapsulated PostScript (EPS) output for hardcopies.
                    """
                    return PyMenu(self.service, "/display/set/picture/driver/eps").execute(*args, **kwargs)
                def jpeg(self, *args, **kwargs):
                    """
                    Produce JPEG output for hardcopies.
                    """
                    return PyMenu(self.service, "/display/set/picture/driver/jpeg").execute(*args, **kwargs)
                def post_script(self, *args, **kwargs):
                    """
                    Produce PostScript output for hardcopies.
                    """
                    return PyMenu(self.service, "/display/set/picture/driver/post_script").execute(*args, **kwargs)
                def ppm(self, *args, **kwargs):
                    """
                    Produce PPM output for hardcopies.
                    """
                    return PyMenu(self.service, "/display/set/picture/driver/ppm").execute(*args, **kwargs)
                def tiff(self, *args, **kwargs):
                    """
                    Use TIFF output for hardcopies.
                    """
                    return PyMenu(self.service, "/display/set/picture/driver/tiff").execute(*args, **kwargs)
                def png(self, *args, **kwargs):
                    """
                    Use PNG output for hardcopies.
                    """
                    return PyMenu(self.service, "/display/set/picture/driver/png").execute(*args, **kwargs)
                def hsf(self, *args, **kwargs):
                    """
                    Use HSF output for hardcopies.
                    """
                    return PyMenu(self.service, "/display/set/picture/driver/hsf").execute(*args, **kwargs)
                def avz(self, *args, **kwargs):
                    """
                    Use AVZ output for hardcopies.
                    """
                    return PyMenu(self.service, "/display/set/picture/driver/avz").execute(*args, **kwargs)
                def glb(self, *args, **kwargs):
                    """
                    Use GLB output for hardcopies.
                    """
                    return PyMenu(self.service, "/display/set/picture/driver/glb").execute(*args, **kwargs)
                def vrml(self, *args, **kwargs):
                    """
                    Use VRML output for hardcopies.
                    """
                    return PyMenu(self.service, "/display/set/picture/driver/vrml").execute(*args, **kwargs)
                def list(self, *args, **kwargs):
                    """
                    List the current hardcopy driver.
                    """
                    return PyMenu(self.service, "/display/set/picture/driver/list").execute(*args, **kwargs)
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
                    return PyMenu(self.service, "/display/set/picture/driver/options").execute(*args, **kwargs)

                class post_format(metaclass=PyMenuMeta):
                    """
                    Enter the PostScript driver format menu.
                    """
                    def fast_raster(self, *args, **kwargs):
                        """
                        Use the new raster format.
                        """
                        return PyMenu(self.service, "/display/set/picture/driver/post_format/fast_raster").execute(*args, **kwargs)
                    def raster(self, *args, **kwargs):
                        """
                        Use the original raster format.
                        """
                        return PyMenu(self.service, "/display/set/picture/driver/post_format/raster").execute(*args, **kwargs)
                    def rle_raster(self, *args, **kwargs):
                        """
                        Use the run-length encoded raster format.
                        """
                        return PyMenu(self.service, "/display/set/picture/driver/post_format/rle_raster").execute(*args, **kwargs)
                    def vector(self, *args, **kwargs):
                        """
                        Use vector format.
                        """
                        return PyMenu(self.service, "/display/set/picture/driver/post_format/vector").execute(*args, **kwargs)

        class lights(metaclass=PyMenuMeta):
            """
            Lights menu.
            """
            def lights_on(self, *args, **kwargs):
                """
                Turn all active lighting on/off.
                """
                return PyMenu(self.service, "/display/set/lights/lights_on").execute(*args, **kwargs)
            def set_ambient_color(self, *args, **kwargs):
                """
                Set the ambient light color for the scene.
                """
                return PyMenu(self.service, "/display/set/lights/set_ambient_color").execute(*args, **kwargs)
            def set_light(self, *args, **kwargs):
                """
                Add or modify a directional, colored light.
                """
                return PyMenu(self.service, "/display/set/lights/set_light").execute(*args, **kwargs)
            def headlight_on(self, *args, **kwargs):
                """
                Turn the light that moves with the camera on or off.
                """
                return PyMenu(self.service, "/display/set/lights/headlight_on").execute(*args, **kwargs)

            class lighting_interpolation(metaclass=PyMenuMeta):
                """
                Set lighting interpolation method.
                """
                def automatic(self, *args, **kwargs):
                    """
                    Choose Automatic to automatically select the best lighting method for a given graphics object.
                    """
                    return PyMenu(self.service, "/display/set/lights/lighting_interpolation/automatic").execute(*args, **kwargs)
                def flat(self, *args, **kwargs):
                    """
                    Use flat shading for meshes and polygons.
                    """
                    return PyMenu(self.service, "/display/set/lights/lighting_interpolation/flat").execute(*args, **kwargs)
                def gouraud(self, *args, **kwargs):
                    """
                    Use Gouraud shading to calculate the color at each vertex of a polygon and interpolate it in the interior.
                    """
                    return PyMenu(self.service, "/display/set/lights/lighting_interpolation/gouraud").execute(*args, **kwargs)
                def phong(self, *args, **kwargs):
                    """
                    Use Phong shading to interpolate the normals for each pixel of a polygon and compute a color at every pixel.
                    """
                    return PyMenu(self.service, "/display/set/lights/lighting_interpolation/phong").execute(*args, **kwargs)

        class rendering_options(metaclass=PyMenuMeta):
            """
            Rendering options menu.
            """
            def auto_spin(self, *args, **kwargs):
                """
                Enable/disable mouse view rotations to continue to spin the display after the button is released.
                """
                return PyMenu(self.service, "/display/set/rendering_options/auto_spin").execute(*args, **kwargs)
            def device_info(self, *args, **kwargs):
                """
                List information for the graphics device.
                """
                return PyMenu(self.service, "/display/set/rendering_options/device_info").execute(*args, **kwargs)
            def double_buffering(self, *args, **kwargs):
                """
                Enable/disable double-buffering.
                """
                return PyMenu(self.service, "/display/set/rendering_options/double_buffering").execute(*args, **kwargs)
            def driver(self, *args, **kwargs):
                """
                Change the current graphics driver.
                """
                return PyMenu(self.service, "/display/set/rendering_options/driver").execute(*args, **kwargs)
            def hidden_surfaces(self, *args, **kwargs):
                """
                Enable/disable hidden surface removal.
                """
                return PyMenu(self.service, "/display/set/rendering_options/hidden_surfaces").execute(*args, **kwargs)
            def hidden_surface_method(self, *args, **kwargs):
                """
                Specify the method to perform hidden line and hidden surface rendering.
                """
                return PyMenu(self.service, "/display/set/rendering_options/hidden_surface_method").execute(*args, **kwargs)
            def outer_face_cull(self, *args, **kwargs):
                """
                Enable/disable discarding outer faces during display.
                """
                return PyMenu(self.service, "/display/set/rendering_options/outer_face_cull").execute(*args, **kwargs)
            def surface_edge_visibility(self, *args, **kwargs):
                """
                Set edge visibility flags for surfaces.
                """
                return PyMenu(self.service, "/display/set/rendering_options/surface_edge_visibility").execute(*args, **kwargs)
            def animation_option(self, *args, **kwargs):
                """
                Using Wireframe / All option during animation.
                """
                return PyMenu(self.service, "/display/set/rendering_options/animation_option").execute(*args, **kwargs)
            def color_map_alignment(self, *args, **kwargs):
                """
                Set the color bar alignment.
                """
                return PyMenu(self.service, "/display/set/rendering_options/color_map_alignment").execute(*args, **kwargs)
            def help_text_color(self, *args, **kwargs):
                """
                Set the color of screen help text.
                """
                return PyMenu(self.service, "/display/set/rendering_options/help_text_color").execute(*args, **kwargs)
            def face_displacement(self, *args, **kwargs):
                """
                Set face displacement value in Z-buffer units along the Camera Z-axis.
                """
                return PyMenu(self.service, "/display/set/rendering_options/face_displacement").execute(*args, **kwargs)
            def set_rendering_options(self, *args, **kwargs):
                """
                Set the rendering options.
                """
                return PyMenu(self.service, "/display/set/rendering_options/set_rendering_options").execute(*args, **kwargs)
            def show_colormap(self, *args, **kwargs):
                """
                Enable/Disable colormap.
                """
                return PyMenu(self.service, "/display/set/rendering_options/show_colormap").execute(*args, **kwargs)

        class styles(metaclass=PyMenuMeta):
            """
            Display style menu.
            """
            def cell_quality(self, *args, **kwargs):
                """
                Set the display attributes of the cell-quality style.
                """
                return PyMenu(self.service, "/display/set/styles/cell_quality").execute(*args, **kwargs)
            def cell_size(self, *args, **kwargs):
                """
                Set the display attributes of the cell-size style.
                """
                return PyMenu(self.service, "/display/set/styles/cell_size").execute(*args, **kwargs)
            def dummy(self, *args, **kwargs):
                """
                .
                """
                return PyMenu(self.service, "/display/set/styles/dummy").execute(*args, **kwargs)
            def face_quality(self, *args, **kwargs):
                """
                Set the display attributes of the face-quality style.
                """
                return PyMenu(self.service, "/display/set/styles/face_quality").execute(*args, **kwargs)
            def face_size(self, *args, **kwargs):
                """
                Set the display attributes of the face-size style.
                """
                return PyMenu(self.service, "/display/set/styles/face_size").execute(*args, **kwargs)
            def free(self, *args, **kwargs):
                """
                Set the display attributes of the free style.
                """
                return PyMenu(self.service, "/display/set/styles/free").execute(*args, **kwargs)
            def left_handed(self, *args, **kwargs):
                """
                Set the display attributes of the left-handed style.
                """
                return PyMenu(self.service, "/display/set/styles/left_handed").execute(*args, **kwargs)
            def mark(self, *args, **kwargs):
                """
                Set the display attributes of the mark style.
                """
                return PyMenu(self.service, "/display/set/styles/mark").execute(*args, **kwargs)
            def multi(self, *args, **kwargs):
                """
                Set the display attributes of the multi style.
                """
                return PyMenu(self.service, "/display/set/styles/multi").execute(*args, **kwargs)
            def refine(self, *args, **kwargs):
                """
                Set the display attributes of the refine style.
                """
                return PyMenu(self.service, "/display/set/styles/refine").execute(*args, **kwargs)
            def tag(self, *args, **kwargs):
                """
                Set the display attributes of the tag style.
                """
                return PyMenu(self.service, "/display/set/styles/tag").execute(*args, **kwargs)
            def unmeshed(self, *args, **kwargs):
                """
                Set the display attributes of the unmeshed style.
                """
                return PyMenu(self.service, "/display/set/styles/unmeshed").execute(*args, **kwargs)
            def unused(self, *args, **kwargs):
                """
                Set the display attributes of the unused style.
                """
                return PyMenu(self.service, "/display/set/styles/unused").execute(*args, **kwargs)

        class windows(metaclass=PyMenuMeta):
            """
            Window options menu.
            """
            def aspect_ratio(self, *args, **kwargs):
                """
                Set the aspect ratio of the active window.
                """
                return PyMenu(self.service, "/display/set/windows/aspect_ratio").execute(*args, **kwargs)
            def logo(self, *args, **kwargs):
                """
                Enable/disable visibility of the logo in graphics window.
                """
                return PyMenu(self.service, "/display/set/windows/logo").execute(*args, **kwargs)
            def ruler(self, *args, **kwargs):
                """
                Enable/disable ruler visibility.
                """
                return PyMenu(self.service, "/display/set/windows/ruler").execute(*args, **kwargs)
            def logo_color(self, *args, **kwargs):
                """
                Set logo color to white/black.
                """
                return PyMenu(self.service, "/display/set/windows/logo_color").execute(*args, **kwargs)

            class axes(metaclass=PyMenuMeta):
                """
                Enter the axes window options menu.
                """
                def border(self, *args, **kwargs):
                    """
                    Enable/disable drawing of a border around the axes window.
                    """
                    return PyMenu(self.service, "/display/set/windows/axes/border").execute(*args, **kwargs)
                def bottom(self, *args, **kwargs):
                    """
                    Set the bottom boundary of the axes window.
                    """
                    return PyMenu(self.service, "/display/set/windows/axes/bottom").execute(*args, **kwargs)
                def clear(self, *args, **kwargs):
                    """
                    Set the transparency of the axes window.
                    """
                    return PyMenu(self.service, "/display/set/windows/axes/clear").execute(*args, **kwargs)
                def right(self, *args, **kwargs):
                    """
                    Set the right boundary of the axes window.
                    """
                    return PyMenu(self.service, "/display/set/windows/axes/right").execute(*args, **kwargs)
                def visible(self, *args, **kwargs):
                    """
                    Enable/disable axes visibility.
                    """
                    return PyMenu(self.service, "/display/set/windows/axes/visible").execute(*args, **kwargs)

            class main(metaclass=PyMenuMeta):
                """
                Enter the main view window options menu.
                """
                def border(self, *args, **kwargs):
                    """
                    Enable/disable drawing of borders around the main viewing window.
                    """
                    return PyMenu(self.service, "/display/set/windows/main/border").execute(*args, **kwargs)
                def bottom(self, *args, **kwargs):
                    """
                    Set the bottom boundary of the main viewing window.
                    """
                    return PyMenu(self.service, "/display/set/windows/main/bottom").execute(*args, **kwargs)
                def left(self, *args, **kwargs):
                    """
                    Set the left boundary of the main viewing window.
                    """
                    return PyMenu(self.service, "/display/set/windows/main/left").execute(*args, **kwargs)
                def right(self, *args, **kwargs):
                    """
                    Set the right boundary of the main viewing window.
                    """
                    return PyMenu(self.service, "/display/set/windows/main/right").execute(*args, **kwargs)
                def top(self, *args, **kwargs):
                    """
                    Set the top boundary of the main viewing window.
                    """
                    return PyMenu(self.service, "/display/set/windows/main/top").execute(*args, **kwargs)
                def visible(self, *args, **kwargs):
                    """
                    Enable/disable visibility of the main viewing window.
                    """
                    return PyMenu(self.service, "/display/set/windows/main/visible").execute(*args, **kwargs)

            class scale(metaclass=PyMenuMeta):
                """
                Enter the color scale window options menu.
                """
                def border(self, *args, **kwargs):
                    """
                    Enable/disable drawing of borders around the color scale window.
                    """
                    return PyMenu(self.service, "/display/set/windows/scale/border").execute(*args, **kwargs)
                def bottom(self, *args, **kwargs):
                    """
                    Set the bottom boundary of the color scale window.
                    """
                    return PyMenu(self.service, "/display/set/windows/scale/bottom").execute(*args, **kwargs)
                def clear(self, *args, **kwargs):
                    """
                    Set the transparency of the scale window.
                    """
                    return PyMenu(self.service, "/display/set/windows/scale/clear").execute(*args, **kwargs)
                def format(self, *args, **kwargs):
                    """
                    Set the number format of the color scale window (e.g. %0.2e).
                    """
                    return PyMenu(self.service, "/display/set/windows/scale/format").execute(*args, **kwargs)
                def font_size(self, *args, **kwargs):
                    """
                    Set the font size of the color scale window.
                    """
                    return PyMenu(self.service, "/display/set/windows/scale/font_size").execute(*args, **kwargs)
                def left(self, *args, **kwargs):
                    """
                    Set the left boundary of the color scale window.
                    """
                    return PyMenu(self.service, "/display/set/windows/scale/left").execute(*args, **kwargs)
                def margin(self, *args, **kwargs):
                    """
                    Set the margin of the color scale window.
                    """
                    return PyMenu(self.service, "/display/set/windows/scale/margin").execute(*args, **kwargs)
                def right(self, *args, **kwargs):
                    """
                    Set the right boundary of the color scale window.
                    """
                    return PyMenu(self.service, "/display/set/windows/scale/right").execute(*args, **kwargs)
                def top(self, *args, **kwargs):
                    """
                    Set the top boundary of the color scale window.
                    """
                    return PyMenu(self.service, "/display/set/windows/scale/top").execute(*args, **kwargs)
                def visible(self, *args, **kwargs):
                    """
                    Enable/disable visibility of the color scale window.
                    """
                    return PyMenu(self.service, "/display/set/windows/scale/visible").execute(*args, **kwargs)
                def alignment(self, *args, **kwargs):
                    """
                    Set colormap to bottom/left/top/right.
                    """
                    return PyMenu(self.service, "/display/set/windows/scale/alignment").execute(*args, **kwargs)

            class text(metaclass=PyMenuMeta):
                """
                Enter the text window options menu.
                """
                def application(self, *args, **kwargs):
                    """
                    Enable/disable the application name in the picture.
                    """
                    return PyMenu(self.service, "/display/set/windows/text/application").execute(*args, **kwargs)
                def border(self, *args, **kwargs):
                    """
                    Enable/disable drawing of borders around the text window.
                    """
                    return PyMenu(self.service, "/display/set/windows/text/border").execute(*args, **kwargs)
                def bottom(self, *args, **kwargs):
                    """
                    Set the bottom boundary of the text window.
                    """
                    return PyMenu(self.service, "/display/set/windows/text/bottom").execute(*args, **kwargs)
                def clear(self, *args, **kwargs):
                    """
                    Enable/disable text window transparency.
                    """
                    return PyMenu(self.service, "/display/set/windows/text/clear").execute(*args, **kwargs)
                def company(self, *args, **kwargs):
                    """
                    Enable/disable the company name in the picture.
                    """
                    return PyMenu(self.service, "/display/set/windows/text/company").execute(*args, **kwargs)
                def date(self, *args, **kwargs):
                    """
                    Enable/disable the date in the picture.
                    """
                    return PyMenu(self.service, "/display/set/windows/text/date").execute(*args, **kwargs)
                def left(self, *args, **kwargs):
                    """
                    Set the left boundary of the text window.
                    """
                    return PyMenu(self.service, "/display/set/windows/text/left").execute(*args, **kwargs)
                def right(self, *args, **kwargs):
                    """
                    Set the right boundary of the text window.
                    """
                    return PyMenu(self.service, "/display/set/windows/text/right").execute(*args, **kwargs)
                def top(self, *args, **kwargs):
                    """
                    Set the top boundary of the text window.
                    """
                    return PyMenu(self.service, "/display/set/windows/text/top").execute(*args, **kwargs)
                def visible(self, *args, **kwargs):
                    """
                    Enable/disable text window transparency.
                    """
                    return PyMenu(self.service, "/display/set/windows/text/visible").execute(*args, **kwargs)

            class video(metaclass=PyMenuMeta):
                """
                Enter the video window options menu.
                """
                def background(self, *args, **kwargs):
                    """
                    Set the background color in the video picture.
                    """
                    return PyMenu(self.service, "/display/set/windows/video/background").execute(*args, **kwargs)
                def color_filter(self, *args, **kwargs):
                    """
                    Set the color filter options for the picture.
                    """
                    return PyMenu(self.service, "/display/set/windows/video/color_filter").execute(*args, **kwargs)
                def foreground(self, *args, **kwargs):
                    """
                    Set the foreground color in the video picture.
                    """
                    return PyMenu(self.service, "/display/set/windows/video/foreground").execute(*args, **kwargs)
                def on(self, *args, **kwargs):
                    """
                    Enable/disable video picture settings.
                    """
                    return PyMenu(self.service, "/display/set/windows/video/on").execute(*args, **kwargs)
                def pixel_size(self, *args, **kwargs):
                    """
                    Set the window size in pixels.
                    """
                    return PyMenu(self.service, "/display/set/windows/video/pixel_size").execute(*args, **kwargs)

            class xy(metaclass=PyMenuMeta):
                """
                Enter the X-Y plot window options menu.
                """
                def border(self, *args, **kwargs):
                    """
                    Enable/disable drawing of a border around the X-Y plotter window.
                    """
                    return PyMenu(self.service, "/display/set/windows/xy/border").execute(*args, **kwargs)
                def bottom(self, *args, **kwargs):
                    """
                    Set the bottom boundary of the X-Y plotter window.
                    """
                    return PyMenu(self.service, "/display/set/windows/xy/bottom").execute(*args, **kwargs)
                def left(self, *args, **kwargs):
                    """
                    Set the left boundary of the X-Y plotter window.
                    """
                    return PyMenu(self.service, "/display/set/windows/xy/left").execute(*args, **kwargs)
                def right(self, *args, **kwargs):
                    """
                    Set the right boundary of the X-Y plotter window.
                    """
                    return PyMenu(self.service, "/display/set/windows/xy/right").execute(*args, **kwargs)
                def top(self, *args, **kwargs):
                    """
                    Set the top boundary of the X-Y plotter window.
                    """
                    return PyMenu(self.service, "/display/set/windows/xy/top").execute(*args, **kwargs)
                def visible(self, *args, **kwargs):
                    """
                    Enable/disable X-Y plotter window visibility.
                    """
                    return PyMenu(self.service, "/display/set/windows/xy/visible").execute(*args, **kwargs)

    class set_grid(metaclass=PyMenuMeta):
        """
        Enter the set-grid menu.
        """
        def all_cells(self, *args, **kwargs):
            """
            Draw all elements in cell zones.
            """
            return PyMenu(self.service, "/display/set_grid/all_cells").execute(*args, **kwargs)
        def all_faces(self, *args, **kwargs):
            """
            Draw all elements in face zones.
            """
            return PyMenu(self.service, "/display/set_grid/all_faces").execute(*args, **kwargs)
        def all_nodes(self, *args, **kwargs):
            """
            Draw all elements in node zones.
            """
            return PyMenu(self.service, "/display/set_grid/all_nodes").execute(*args, **kwargs)
        def free(self, *args, **kwargs):
            """
            Draw free elements.
            """
            return PyMenu(self.service, "/display/set_grid/free").execute(*args, **kwargs)
        def left_handed(self, *args, **kwargs):
            """
            Draw left-handed elements.
            """
            return PyMenu(self.service, "/display/set_grid/left_handed").execute(*args, **kwargs)
        def multi(self, *args, **kwargs):
            """
            Draw multiply-connected elements.
            """
            return PyMenu(self.service, "/display/set_grid/multi").execute(*args, **kwargs)
        def refine(self, *args, **kwargs):
            """
            Draw refine marked elements.
            """
            return PyMenu(self.service, "/display/set_grid/refine").execute(*args, **kwargs)
        def unmeshed(self, *args, **kwargs):
            """
            Draw unmeshed elements.
            """
            return PyMenu(self.service, "/display/set_grid/unmeshed").execute(*args, **kwargs)
        def unused(self, *args, **kwargs):
            """
            Draw unused nodes.
            """
            return PyMenu(self.service, "/display/set_grid/unused").execute(*args, **kwargs)
        def marked(self, *args, **kwargs):
            """
            Draw marked elements.
            """
            return PyMenu(self.service, "/display/set_grid/marked").execute(*args, **kwargs)
        def tagged(self, *args, **kwargs):
            """
            Draw tagged elements.
            """
            return PyMenu(self.service, "/display/set_grid/tagged").execute(*args, **kwargs)
        def face_quality(self, *args, **kwargs):
            """
            Draw faces only in specified quality range.
            """
            return PyMenu(self.service, "/display/set_grid/face_quality").execute(*args, **kwargs)
        def cell_quality(self, *args, **kwargs):
            """
            Draw cells only in specified quality range.
            """
            return PyMenu(self.service, "/display/set_grid/cell_quality").execute(*args, **kwargs)
        def neighborhood(self, *args, **kwargs):
            """
            Set display bounds to draw entities in the neighborhood of a entity.
            """
            return PyMenu(self.service, "/display/set_grid/neighborhood").execute(*args, **kwargs)
        def x_range(self, *args, **kwargs):
            """
            Draw only entities with x coordinates in specified range.
            """
            return PyMenu(self.service, "/display/set_grid/x_range").execute(*args, **kwargs)
        def y_range(self, *args, **kwargs):
            """
            Draw only entities with y coordinates in specified range.
            """
            return PyMenu(self.service, "/display/set_grid/y_range").execute(*args, **kwargs)
        def z_range(self, *args, **kwargs):
            """
            Draw only entities with z coordinates in specified range.
            """
            return PyMenu(self.service, "/display/set_grid/z_range").execute(*args, **kwargs)
        def normals(self, *args, **kwargs):
            """
            Turn on/off face normals.
            """
            return PyMenu(self.service, "/display/set_grid/normals").execute(*args, **kwargs)
        def normal_scale(self, *args, **kwargs):
            """
            Face normal scale.
            """
            return PyMenu(self.service, "/display/set_grid/normal_scale").execute(*args, **kwargs)
        def labels(self, *args, **kwargs):
            """
            Turn on/off labeling.
            """
            return PyMenu(self.service, "/display/set_grid/labels").execute(*args, **kwargs)
        def label_alignment(self, *args, **kwargs):
            """
            Set label alignment; chose from "^v<>*".
            """
            return PyMenu(self.service, "/display/set_grid/label_alignment").execute(*args, **kwargs)
        def label_font(self, *args, **kwargs):
            """
            Set label font.
            """
            return PyMenu(self.service, "/display/set_grid/label_font").execute(*args, **kwargs)
        def label_scale(self, *args, **kwargs):
            """
            Set label scale.
            """
            return PyMenu(self.service, "/display/set_grid/label_scale").execute(*args, **kwargs)
        def node_size(self, *args, **kwargs):
            """
            Set node symbol scaling factor.
            """
            return PyMenu(self.service, "/display/set_grid/node_size").execute(*args, **kwargs)
        def node_symbol(self, *args, **kwargs):
            """
            Set node symbol.
            """
            return PyMenu(self.service, "/display/set_grid/node_symbol").execute(*args, **kwargs)
        def list(self, *args, **kwargs):
            """
            List display variables.
            """
            return PyMenu(self.service, "/display/set_grid/list").execute(*args, **kwargs)
        def default(self, *args, **kwargs):
            """
            Reset all display variables to their default value.
            """
            return PyMenu(self.service, "/display/set_grid/default").execute(*args, **kwargs)

    class views(metaclass=PyMenuMeta):
        """
        Enter the view menu.
        """
        def auto_scale(self, *args, **kwargs):
            """
            Scale and center the current scene.
            """
            return PyMenu(self.service, "/display/views/auto_scale").execute(*args, **kwargs)
        def default_view(self, *args, **kwargs):
            """
            Reset view to front and center.
            """
            return PyMenu(self.service, "/display/views/default_view").execute(*args, **kwargs)
        def delete_view(self, *args, **kwargs):
            """
            Remove a view from the list.
            """
            return PyMenu(self.service, "/display/views/delete_view").execute(*args, **kwargs)
        def last_view(self, *args, **kwargs):
            """
            Return to the camera position before the last manipulation.
            """
            return PyMenu(self.service, "/display/views/last_view").execute(*args, **kwargs)
        def next_view(self, *args, **kwargs):
            """
            Return to the camera position after the current position in the stack.
            """
            return PyMenu(self.service, "/display/views/next_view").execute(*args, **kwargs)
        def list_views(self, *args, **kwargs):
            """
            List predefined and saved views.
            """
            return PyMenu(self.service, "/display/views/list_views").execute(*args, **kwargs)
        def restore_view(self, *args, **kwargs):
            """
            Use a saved view.
            """
            return PyMenu(self.service, "/display/views/restore_view").execute(*args, **kwargs)
        def read_views(self, *args, **kwargs):
            """
            Read views from a view file.
            """
            return PyMenu(self.service, "/display/views/read_views").execute(*args, **kwargs)
        def save_view(self, *args, **kwargs):
            """
            Save the current view to the view list.
            """
            return PyMenu(self.service, "/display/views/save_view").execute(*args, **kwargs)
        def write_views(self, *args, **kwargs):
            """
            Write selected views to a view file.
            """
            return PyMenu(self.service, "/display/views/write_views").execute(*args, **kwargs)

        class camera(metaclass=PyMenuMeta):
            """
            Enter the camera menu to modify the current viewing parameters.
            """
            def dolly_camera(self, *args, **kwargs):
                """
                Adjust the camera position and target.
                """
                return PyMenu(self.service, "/display/views/camera/dolly_camera").execute(*args, **kwargs)
            def field(self, *args, **kwargs):
                """
                Set the field of view (width and height).
                """
                return PyMenu(self.service, "/display/views/camera/field").execute(*args, **kwargs)
            def orbit_camera(self, *args, **kwargs):
                """
                Adjust the camera position without modifying the target.
                """
                return PyMenu(self.service, "/display/views/camera/orbit_camera").execute(*args, **kwargs)
            def pan_camera(self, *args, **kwargs):
                """
                Adjust the camera target without modifying the position.
                """
                return PyMenu(self.service, "/display/views/camera/pan_camera").execute(*args, **kwargs)
            def position(self, *args, **kwargs):
                """
                Set the camera position.
                """
                return PyMenu(self.service, "/display/views/camera/position").execute(*args, **kwargs)
            def projection(self, *args, **kwargs):
                """
                Set the camera projection type.
                """
                return PyMenu(self.service, "/display/views/camera/projection").execute(*args, **kwargs)
            def roll_camera(self, *args, **kwargs):
                """
                Adjust the camera up-vector.
                """
                return PyMenu(self.service, "/display/views/camera/roll_camera").execute(*args, **kwargs)
            def target(self, *args, **kwargs):
                """
                Set the point to be the center of the camera view.
                """
                return PyMenu(self.service, "/display/views/camera/target").execute(*args, **kwargs)
            def up_vector(self, *args, **kwargs):
                """
                Set the camera up-vector.
                """
                return PyMenu(self.service, "/display/views/camera/up_vector").execute(*args, **kwargs)
            def zoom_camera(self, *args, **kwargs):
                """
                Adjust the camera field of view.
                """
                return PyMenu(self.service, "/display/views/camera/zoom_camera").execute(*args, **kwargs)

    class display_states(metaclass=PyMenuMeta):
        """
        Enter the display state menu.
        """
        def list(self, *args, **kwargs):
            """
            Print the names of the available display states to the console.
            """
            return PyMenu(self.service, "/display/display_states/list").execute(*args, **kwargs)
        def apply(self, *args, **kwargs):
            """
            Apply a display state to the active window.
            """
            return PyMenu(self.service, "/display/display_states/apply").execute(*args, **kwargs)
        def delete(self, *args, **kwargs):
            """
            Delete a display state.
            """
            return PyMenu(self.service, "/display/display_states/delete").execute(*args, **kwargs)
        def use_active(self, *args, **kwargs):
            """
            Update an existing display state's settings to match those of the active graphics window.
            """
            return PyMenu(self.service, "/display/display_states/use_active").execute(*args, **kwargs)
        def copy(self, *args, **kwargs):
            """
            Create a new display state with settings copied from an existing display state.
            """
            return PyMenu(self.service, "/display/display_states/copy").execute(*args, **kwargs)
        def read(self, *args, **kwargs):
            """
            Read display states from a file.
            """
            return PyMenu(self.service, "/display/display_states/read").execute(*args, **kwargs)
        def write(self, *args, **kwargs):
            """
            Write display states to a file.
            """
            return PyMenu(self.service, "/display/display_states/write").execute(*args, **kwargs)
        def edit(self, *args, **kwargs):
            """
            Edit a particular display state setting.
            """
            return PyMenu(self.service, "/display/display_states/edit").execute(*args, **kwargs)
        def create(self, *args, **kwargs):
            """
            Create a new display state.
            """
            return PyMenu(self.service, "/display/display_states/create").execute(*args, **kwargs)

    class xy_plot(metaclass=PyMenuMeta):
        """
        Enter X-Y plot menu.
        """
        def file(self, *args, **kwargs):
            """
            Over-plot data from file.
            """
            return PyMenu(self.service, "/display/xy_plot/file").execute(*args, **kwargs)
        def cell_distribution(self, *args, **kwargs):
            """
            Display chart of distribution of cell quality.
            """
            return PyMenu(self.service, "/display/xy_plot/cell_distribution").execute(*args, **kwargs)
        def face_distribution(self, *args, **kwargs):
            """
            Display chart of distribution of face quality.
            """
            return PyMenu(self.service, "/display/xy_plot/face_distribution").execute(*args, **kwargs)
        def set(self, *args, **kwargs):
            """
            Set histogram plot parameters.
            """
            return PyMenu(self.service, "/display/xy_plot/set").execute(*args, **kwargs)

    class update_scene(metaclass=PyMenuMeta):
        """
        Enter the scene options menu.
        """
        def select_geometry(self, *args, **kwargs):
            """
            Select geometry to be updated.
            """
            return PyMenu(self.service, "/display/update_scene/select_geometry").execute(*args, **kwargs)
        def overlays(self, *args, **kwargs):
            """
            Enable/disable the overlays option.
            """
            return PyMenu(self.service, "/display/update_scene/overlays").execute(*args, **kwargs)
        def draw_frame(self, *args, **kwargs):
            """
            Enable/disable drawing of the bounding frame.
            """
            return PyMenu(self.service, "/display/update_scene/draw_frame").execute(*args, **kwargs)
        def delete(self, *args, **kwargs):
            """
            Delete selected geometries.
            """
            return PyMenu(self.service, "/display/update_scene/delete").execute(*args, **kwargs)
        def display(self, *args, **kwargs):
            """
            Display selected geometries.
            """
            return PyMenu(self.service, "/display/update_scene/display").execute(*args, **kwargs)
        def transform(self, *args, **kwargs):
            """
            Apply transformation matrix on selected geometries.
            """
            return PyMenu(self.service, "/display/update_scene/transform").execute(*args, **kwargs)
        def pathline(self, *args, **kwargs):
            """
            Change pathline attributes.
            """
            return PyMenu(self.service, "/display/update_scene/pathline").execute(*args, **kwargs)
        def iso_sweep(self, *args, **kwargs):
            """
            Change iso-sweep values.
            """
            return PyMenu(self.service, "/display/update_scene/iso_sweep").execute(*args, **kwargs)
        def time(self, *args, **kwargs):
            """
            Change time-step value.
            """
            return PyMenu(self.service, "/display/update_scene/time").execute(*args, **kwargs)
        def set_frame(self, *args, **kwargs):
            """
            Change frame options.
            """
            return PyMenu(self.service, "/display/update_scene/set_frame").execute(*args, **kwargs)

    class objects(metaclass=PyMenuMeta):
        """
        Enter the objects menu.
        """
        is_extended_tui = True
        def show_all(self, *args, **kwargs):
            """
            Show all displayed objects.
            """
            return PyMenu(self.service, "/display/objects/show_all").execute(*args, **kwargs)
        def explode(self, *args, **kwargs):
            """
            Explode all displayed objects.
            """
            return PyMenu(self.service, "/display/objects/explode").execute(*args, **kwargs)
        def toggle_color_palette(self, *args, **kwargs):
            """
            Toggle between default and classic color palettes.
            """
            return PyMenu(self.service, "/display/objects/toggle_color_palette").execute(*args, **kwargs)
        def implode(self, *args, **kwargs):
            """
            Implode all displayed objects.
            """
            return PyMenu(self.service, "/display/objects/implode").execute(*args, **kwargs)
        def display_similar_area(self, *args, **kwargs):
            """
            Shows all similar surface area objects.
            """
            return PyMenu(self.service, "/display/objects/display_similar_area").execute(*args, **kwargs)
        def toggle_color_mode(self, *args, **kwargs):
            """
            Toggles color mode between color by objects/threads.
            """
            return PyMenu(self.service, "/display/objects/toggle_color_mode").execute(*args, **kwargs)
        def make_transparent(self, *args, **kwargs):
            """
            Toggle Transparent view based on object selection.
            """
            return PyMenu(self.service, "/display/objects/make_transparent").execute(*args, **kwargs)
        def select_all_visible(self, *args, **kwargs):
            """
            Probe select all visible objects.
            """
            return PyMenu(self.service, "/display/objects/select_all_visible").execute(*args, **kwargs)
        def display_neighborhood(self, *args, **kwargs):
            """
            Displays neighboring objects also.
            """
            return PyMenu(self.service, "/display/objects/display_neighborhood").execute(*args, **kwargs)
        def hide_objects(self, *args, **kwargs):
            """
            Hide selected objects from view.
            """
            return PyMenu(self.service, "/display/objects/hide_objects").execute(*args, **kwargs)
        def isolate_objects(self, *args, **kwargs):
            """
            Hide selected objects from view.
            """
            return PyMenu(self.service, "/display/objects/isolate_objects").execute(*args, **kwargs)

        class xy_plot(metaclass=PyNamedObjectMeta):
            """
            """
            is_extended_tui = True

            class name(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class uid(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class options(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

                class node_values(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class position_on_x_axis(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class position_on_y_axis(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

            class plot_direction(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

                class direction_vector(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                    class x_component(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

                    class y_component(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

                    class z_component(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

                class curve_length(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                    class default(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

                    class reverse(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

            class x_axis_function(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class y_axis_function(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class surfaces_list(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class physics(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class geometry(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class surfaces(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

        class mesh(metaclass=PyNamedObjectMeta):
            """
            """
            is_extended_tui = True

            class name(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class options(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

                class nodes(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class edges(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class faces(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class partitions(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class overset(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class gap(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

            class edge_type(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

                class all(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class feature(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                    class feature_angle(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

                class outline(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

            class shrink_factor(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class surfaces_list(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class coloring(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

                class automatic(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                    class type(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

                    class id(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

                    class normal(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

                    class partition(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

                class manual(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                    class faces(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

                    class edges(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

                    class nodes(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

                    class material_color(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

            class display_state_name(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class physics(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class geometry(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class surfaces(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

        class contour(metaclass=PyNamedObjectMeta):
            """
            """
            is_extended_tui = True

            class name(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class field(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class filled(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class boundary_values(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class contour_lines(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class node_values(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class surfaces_list(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class range_option(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

                class auto_range_on(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                    class global_range(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

                class auto_range_off(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                    class clip_to_range(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

                    class minimum(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

                    class maximum(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

            class coloring(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

                class smooth(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class banded(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

            class color_map(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

                class visible(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class size(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class color(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class log_scale(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class format(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class user_skip(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class show_all(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class position(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class font_name(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class font_automatic(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class font_size(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class length(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class width(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

            class draw_mesh(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class mesh_object(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class display_state_name(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class physics(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class geometry(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class surfaces(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

        class vector(metaclass=PyNamedObjectMeta):
            """
            """
            is_extended_tui = True

            class name(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class field(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class vector_field(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class surfaces_list(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class scale(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

                class auto_scale(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class scale_f(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

            class style(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class skip(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class vector_opt(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

                class in_plane(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class fixed_length(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class x_comp(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class y_comp(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class z_comp(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class scale_head(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class color(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

            class range_option(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

                class auto_range_on(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                    class global_range(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

                class auto_range_off(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                    class clip_to_range(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

                    class minimum(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

                    class maximum(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

            class color_map(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

                class visible(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class size(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class color(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class log_scale(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class format(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class user_skip(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class show_all(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class position(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class font_name(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class font_automatic(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class font_size(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class length(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class width(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

            class draw_mesh(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class mesh_object(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class display_state_name(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class physics(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class geometry(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class surfaces(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

        class pathlines(metaclass=PyNamedObjectMeta):
            """
            """
            is_extended_tui = True

            class name(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class uid(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class options(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

                class oil_flow(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class reverse(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class node_values(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class relative(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

            class range(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

                class auto_range(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class clip_to_range(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                    class min_value(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

                    class max_value(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

            class style_attribute(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

                class style(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class line_width(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class arrow_space(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class arrow_scale(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class marker_size(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class sphere_size(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class sphere_lod(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class radius(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class ribbon(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                    class field(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

                    class scalefactor(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

            class accuracy_control(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

                class step_size(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class tolerance(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

            class plot(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

                class x_axis_function(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class enabled(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

            class step(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class skip(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class coarsen(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class onzone(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class field(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class surfaces_list(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class velocity_domain(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class color_map(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

                class visible(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class size(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class color(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class log_scale(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class format(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class user_skip(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class show_all(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class position(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class font_name(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class font_automatic(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class font_size(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class length(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class width(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

            class draw_mesh(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class mesh_object(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class display_state_name(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class physics(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class geometry(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class surfaces(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

        class particle_tracks(metaclass=PyNamedObjectMeta):
            """
            """
            is_extended_tui = True

            class name(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class uid(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class options(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

                class node_values(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

            class filter_settings(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

                class field(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class options(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                    class inside(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

                    class outside(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

                class enabled(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class filter_minimum(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class filter_maximum(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

            class range(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

                class auto_range(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class clip_to_range(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                    class min_value(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

                    class max_value(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

            class style_attribute(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

                class style(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class line_width(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class arrow_space(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class arrow_scale(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class marker_size(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class sphere_size(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class sphere_lod(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class radius(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class ribbon_settings(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                    class field(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

                    class scalefactor(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

                class sphere_settings(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                    class scale(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

                    class sphere_lod(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

                    class options(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

                        class constant(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True

                            class diameter(metaclass=PyMenuMeta):
                                """
                                """
                                is_extended_tui = True

                        class variable(metaclass=PyMenuMeta):
                            """
                            """
                            is_extended_tui = True

                            class size_by(metaclass=PyMenuMeta):
                                """
                                """
                                is_extended_tui = True

                            class range(metaclass=PyMenuMeta):
                                """
                                """
                                is_extended_tui = True

                                class auto_range(metaclass=PyMenuMeta):
                                    """
                                    """
                                    is_extended_tui = True

                                class clip_to_range(metaclass=PyMenuMeta):
                                    """
                                    """
                                    is_extended_tui = True

                                    class min_value(metaclass=PyMenuMeta):
                                        """
                                        """
                                        is_extended_tui = True

                                    class max_value(metaclass=PyMenuMeta):
                                        """
                                        """
                                        is_extended_tui = True

            class vector_settings(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

                class style(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class vector_length(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                    class constant_length(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

                    class variable_length(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

                class constant_color(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                    class enabled(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

                    class color(metaclass=PyMenuMeta):
                        """
                        """
                        is_extended_tui = True

                class vector_of(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class scale(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class length_to_head_ratio(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

            class plot(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

                class x_axis_function(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class enabled(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

            class track_single_particle_stream(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

                class enabled(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class stream_id(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

            class skip(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class coarsen(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class field(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class injections_list(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class free_stream_particles(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class wall_film_particles(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class track_pdf_particles(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class color_map(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

                class visible(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class size(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class color(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class log_scale(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class format(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class user_skip(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class show_all(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class position(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class font_name(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class font_automatic(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class font_size(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class length(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

                class width(metaclass=PyMenuMeta):
                    """
                    """
                    is_extended_tui = True

            class draw_mesh(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class mesh_object(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class display_state_name(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

        class scene(metaclass=PyNamedObjectMeta):
            """
            """
            is_extended_tui = True

            class name(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class title(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class temporary(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

            class display_state_name(metaclass=PyMenuMeta):
                """
                """
                is_extended_tui = True

    class zones(metaclass=PyMenuMeta):
        """
        Enter the zones menu.
        """
        def show_all(self, *args, **kwargs):
            """
            Show all displayed objects.
            """
            return PyMenu(self.service, "/display/zones/show_all").execute(*args, **kwargs)
        def toggle_color_palette(self, *args, **kwargs):
            """
            Toggle between default and classic color palettes.
            """
            return PyMenu(self.service, "/display/zones/toggle_color_palette").execute(*args, **kwargs)
        def display_similar_area(self, *args, **kwargs):
            """
            Shows all similar surface area objects.
            """
            return PyMenu(self.service, "/display/zones/display_similar_area").execute(*args, **kwargs)
        def toggle_color_mode(self, *args, **kwargs):
            """
            Toggles color mode between color by objects/threads.
            """
            return PyMenu(self.service, "/display/zones/toggle_color_mode").execute(*args, **kwargs)
        def make_transparent(self, *args, **kwargs):
            """
            Toggle Transparent view based on object selection.
            """
            return PyMenu(self.service, "/display/zones/make_transparent").execute(*args, **kwargs)
        def select_all_visible(self, *args, **kwargs):
            """
            Probe select all visible objects.
            """
            return PyMenu(self.service, "/display/zones/select_all_visible").execute(*args, **kwargs)
        def display_neighborhood(self, *args, **kwargs):
            """
            Displays neighboring objects also.
            """
            return PyMenu(self.service, "/display/zones/display_neighborhood").execute(*args, **kwargs)
        def hide_zones(self, *args, **kwargs):
            """
            Hide selected objects from view.
            """
            return PyMenu(self.service, "/display/zones/hide_zones").execute(*args, **kwargs)
        def isolate_zones(self, *args, **kwargs):
            """
            Hide selected objects from view.
            """
            return PyMenu(self.service, "/display/zones/isolate_zones").execute(*args, **kwargs)

    class advanced_rendering(metaclass=PyMenuMeta):
        """
        Enter the advanced rendering menu.
        """
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
    def face_node_degree_distribution(self, *args, **kwargs):
        """
        Report face node degree of boundary faces.
        """
        return PyMenu(self.service, "/report/face_node_degree_distribution").execute(*args, **kwargs)
    def boundary_cell_quality(self, *args, **kwargs):
        """
        Report quality of boundary cells.
        """
        return PyMenu(self.service, "/report/boundary_cell_quality").execute(*args, **kwargs)
    def cell_distribution(self, *args, **kwargs):
        """
        Report distribution of cell quality.
        """
        return PyMenu(self.service, "/report/cell_distribution").execute(*args, **kwargs)
    def face_distribution(self, *args, **kwargs):
        """
        Reports the distribution of face quality.
        """
        return PyMenu(self.service, "/report/face_distribution").execute(*args, **kwargs)
    def cell_zone_volume(self, *args, **kwargs):
        """
        Report volume of a cell zone.
        """
        return PyMenu(self.service, "/report/cell_zone_volume").execute(*args, **kwargs)
    def cell_zone_at_location(self, *args, **kwargs):
        """
        Report cell zone at given location.
        """
        return PyMenu(self.service, "/report/cell_zone_at_location").execute(*args, **kwargs)
    def face_zone_at_location(self, *args, **kwargs):
        """
        Report face zone at given location.
        """
        return PyMenu(self.service, "/report/face_zone_at_location").execute(*args, **kwargs)
    def number_meshed(self, *args, **kwargs):
        """
        Report number of nodes and faces that have been meshed.
        """
        return PyMenu(self.service, "/report/number_meshed").execute(*args, **kwargs)
    def list_cell_quality(self, *args, **kwargs):
        """
        List cells between quality limits.
        """
        return PyMenu(self.service, "/report/list_cell_quality").execute(*args, **kwargs)
    def mesh_size(self, *args, **kwargs):
        """
        Report number of each type of grid object.
        """
        return PyMenu(self.service, "/report/mesh_size").execute(*args, **kwargs)
    def mesh_statistics(self, *args, **kwargs):
        """
        Write vital mesh statistics to file.
        """
        return PyMenu(self.service, "/report/mesh_statistics").execute(*args, **kwargs)
    def meshing_time(self, *args, **kwargs):
        """
        Report meshing time.
        """
        return PyMenu(self.service, "/report/meshing_time").execute(*args, **kwargs)
    def memory_usage(self, *args, **kwargs):
        """
        Report memory usage.
        """
        return PyMenu(self.service, "/report/memory_usage").execute(*args, **kwargs)
    def print_info(self, *args, **kwargs):
        """
        Print node/face/cell info.
        """
        return PyMenu(self.service, "/report/print_info").execute(*args, **kwargs)
    def edge_size_limits(self, *args, **kwargs):
        """
        Report edge size limits.
        """
        return PyMenu(self.service, "/report/edge_size_limits").execute(*args, **kwargs)
    def face_size_limits(self, *args, **kwargs):
        """
        Report face size limits.
        """
        return PyMenu(self.service, "/report/face_size_limits").execute(*args, **kwargs)
    def face_quality_limits(self, *args, **kwargs):
        """
        Report face quality limits.
        """
        return PyMenu(self.service, "/report/face_quality_limits").execute(*args, **kwargs)
    def face_zone_area(self, *args, **kwargs):
        """
        Report area of a face zone.
        """
        return PyMenu(self.service, "/report/face_zone_area").execute(*args, **kwargs)
    def cell_size_limits(self, *args, **kwargs):
        """
        Report cell size limits.
        """
        return PyMenu(self.service, "/report/cell_size_limits").execute(*args, **kwargs)
    def cell_quality_limits(self, *args, **kwargs):
        """
        Report cell quality limits.
        """
        return PyMenu(self.service, "/report/cell_quality_limits").execute(*args, **kwargs)
    def neighborhood_quality(self, *args, **kwargs):
        """
        Report max quality measure of all cells using node.
        """
        return PyMenu(self.service, "/report/neighborhood_quality").execute(*args, **kwargs)
    def quality_method(self, *args, **kwargs):
        """
        Method to use for measuring face and cell quality.
        """
        return PyMenu(self.service, "/report/quality_method").execute(*args, **kwargs)
    def enhanced_orthogonal_quality(self, *args, **kwargs):
        """
        Enable enhanced orthogonal quality method.
        """
        return PyMenu(self.service, "/report/enhanced_orthogonal_quality").execute(*args, **kwargs)
    def unrefined_cells(self, *args, **kwargs):
        """
        Report number of cells not refined.
        """
        return PyMenu(self.service, "/report/unrefined_cells").execute(*args, **kwargs)
    def update_bounding_box(self, *args, **kwargs):
        """
        Updates bounding box.
        """
        return PyMenu(self.service, "/report/update_bounding_box").execute(*args, **kwargs)
    def verbosity_level(self, *args, **kwargs):
        """
        Verbosity level control.
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
    def spawn_solver_processes(self, *args, **kwargs):
        """
        Spawn additional solver processes.
        """
        return PyMenu(self.service, "/parallel/spawn_solver_processes").execute(*args, **kwargs)
    def auto_partition(self, *args, **kwargs):
        """
        Auto Partition Prism Base Zones?.
        """
        return PyMenu(self.service, "/parallel/auto_partition").execute(*args, **kwargs)
    def agglomerate(self, *args, **kwargs):
        """
        Agglomerate mesh into compute node 0.
        """
        return PyMenu(self.service, "/parallel/agglomerate").execute(*args, **kwargs)
    def print_partition_info(self, *args, **kwargs):
        """
        Prints Partition Info to console.
        """
        return PyMenu(self.service, "/parallel/print_partition_info").execute(*args, **kwargs)
    def thread_number_control(self, *args, **kwargs):
        """
        Thread number control.
        """
        return PyMenu(self.service, "/parallel/thread_number_control").execute(*args, **kwargs)

class openmp_controls(metaclass=PyMenuMeta):
    """
    Enter the openmp menu.
    """
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
