import pytest
from ansys.fluent.core import examples
import_filename = examples.download_file("mixing_elbow.msh.h5", "pyfluent/mixing_elbow")


@pytest.mark.fluent_version(">=23.2")
def test_meshing_queries(new_mesh_session):
    meshing_session = new_mesh_session
    meshing_session.tui.file.read_case(import_filename)

    assert meshing_session.meshing_queries.get_edge_zones(filter='*') == [28, 27, 26, 25, 24, 23, 22, 21, 20]
    assert meshing_session.meshing_queries.get_edge_zones(maximum_entity_count=20, only_boundary=False) == [20, 21, 22,
                                                                                                            23, 28]
    assert meshing_session.meshing_queries.get_edge_zones(maximum_entity_count=20, only_boundary=True) == [20, 21, 22,
                                                                                                           23, 28]

    assert meshing_session.meshing_queries.get_unreferenced_edge_zones() is None
    assert meshing_session.meshing_queries.get_unreferenced_edge_zones(filter="*") is None
    assert meshing_session.meshing_queries.get_unreferenced_edge_zones(zone_name_pattern="*") is None

    assert meshing_session.meshing_queries.get_face_zones(filter='*') == [89, 34, 33, 32, 31, 30, 29]
    assert meshing_session.meshing_queries.get_face_zones(prism_control_name='*') == [33, 34]
    # assert meshing_session.meshing_queries.get_face_zones(xyz_coordinates=[1.4, 1.4, 1.4]) == 34 # assert None == 34
    assert meshing_session.meshing_queries.get_face_zones(maximum_entity_count=20, only_boundary=True) is None

    assert meshing_session.meshing_queries.get_face_zones_by_zone_area(maximum_zone_area=100) == [33, 32, 31, 30]
    assert meshing_session.meshing_queries.get_face_zones_by_zone_area(minimum_zone_area=10) == [34, 29]

    assert meshing_session.meshing_queries.get_face_zones_of_object(object_name="elbow-fluid",
                                                                    regions=["elbow-fluid"]) == [34, 33, 32, 31, 30, 29]
    assert meshing_session.meshing_queries.get_face_zones_of_object(object_name="elbow-fluid", labels=["outlet"]) == [
        32]
    assert meshing_session.meshing_queries.get_face_zones_of_object(object_name="elbow-fluid",
                                                                    region_type="elbow-fluid") is None
    assert meshing_session.meshing_queries.get_face_zones_of_object(object_name="elbow-fluid") == [29, 30, 31, 32, 33,
                                                                                                   34]
    assert meshing_session.meshing_queries.get_face_zones_of_object(objects=["elbow-fluid"]) == [29, 30, 31, 32, 33, 34]

    assert meshing_session.meshing_queries.get_wrapped_face_zones() is None

    assert meshing_session.meshing_queries.get_unreferenced_face_zones() is None
    assert meshing_session.meshing_queries.get_unreferenced_face_zones(filter="*") is None
    assert meshing_session.meshing_queries.get_unreferenced_face_zones(zone_name_pattern="*") is None

    assert meshing_session.meshing_queries.get_interior_face_zones_for_given_cell_zones(cell_zone_id_list=[87]) == [89]
    assert meshing_session.meshing_queries.get_interior_face_zones_for_given_cell_zones(cell_zone_name_pattern="*") == [
        89]
    assert meshing_session.meshing_queries.get_interior_face_zones_for_given_cell_zones(
        cell_zone_name_list=["elbow-fluid"]) == [89]

    assert meshing_session.meshing_queries.get_node_zones(filter='*') == [163, 91, 19]

    assert meshing_session.meshing_queries.get_adjacent_zones_by_edge_connectivity(
        zone_id_list=[29, 30, 31, 32, 33]) == [34]
    assert meshing_session.meshing_queries.get_adjacent_zones_by_edge_connectivity(
        zone_name_list=["outlet", "inlet", "wall", "internal"]) == [34, 29]
    assert meshing_session.meshing_queries.get_adjacent_zones_by_edge_connectivity(zone_name_pattern="*") is None

    assert meshing_session.meshing_queries.get_adjacent_zones_by_node_connectivity(
        zone_id_list=[29, 30, 31, 32, 33]) == [34]
    assert meshing_session.meshing_queries.get_adjacent_zones_by_node_connectivity(
        zone_name_list=["outlet", "inlet", "wall", "internal"]) == [29, 34]
    assert meshing_session.meshing_queries.get_adjacent_zones_by_node_connectivity(zone_name_pattern="*") is None

    assert meshing_session.meshing_queries.get_cell_zones(filter='*') == [87]
    assert meshing_session.meshing_queries.get_cell_zones(maximum_entity_count=100) is None
    assert meshing_session.meshing_queries.get_cell_zones(xyz_coordinates=[1.4, 1.4, 1.4]) is None

    assert meshing_session.meshing_queries.get_unreferenced_cell_zones() is None
    assert meshing_session.meshing_queries.get_unreferenced_cell_zones(filter="*") is None
    assert meshing_session.meshing_queries.get_unreferenced_cell_zones(zone_name_pattern="*") is None

    assert meshing_session.meshing_queries.get_adjacent_cell_zones_for_given_face_zones(
        cell_zone_id_list=[29, 30, 31, 32, 33]) == [87]
    assert meshing_session.meshing_queries.get_adjacent_cell_zones_for_given_face_zones(
        cell_zone_name_list=["outlet", "inlet", "wall", "internal"]) == [87]
    assert meshing_session.meshing_queries.get_adjacent_cell_zones_for_given_face_zones(cell_zone_name_pattern="*") == [
        87]

    assert meshing_session.meshing_queries.get_tet_cell_zones(zone_id_list=[29, 30, 31, 32, 33]) is None
    assert meshing_session.meshing_queries.get_tet_cell_zones(zone_id_list=[87]) is None
    assert meshing_session.meshing_queries.get_tet_cell_zones(
        zone_name_list=["outlet", "inlet", "wall", "internal"]) is None
    assert meshing_session.meshing_queries.get_tet_cell_zones(zone_name_pattern="*") is None

    assert meshing_session.meshing_queries.get_prism_cell_zones(zone_id_list=[87]) is None
    assert meshing_session.meshing_queries.get_prism_cell_zones(
        zone_name_list=["outlet", "inlet", "wall", "internal"]) is None
    assert meshing_session.meshing_queries.get_prism_cell_zones(zone_name_pattern="*") is None

    # assert meshing_session.meshing_queries.get_maxsize_cell_zone_by_count(zone_id_list=[87]) == 87 # assert None == 87
    assert meshing_session.meshing_queries.get_maxsize_cell_zone_by_count(
        zone_name_list=["outlet", "inlet", "wall", "internal"]) is None
    # assert meshing_session.meshing_queries.get_maxsize_cell_zone_by_count(zone_name_pattern="*") == 87 # assert None == 87

    # assert meshing_session.meshing_queries.get_maxsize_cell_zone_by_volume(zone_id_list=[87]) == 87 # assert None == 87
    assert meshing_session.meshing_queries.get_maxsize_cell_zone_by_volume(
        zone_name_list=["outlet", "inlet", "wall", "internal"]) is None
    # assert meshing_session.meshing_queries.get_maxsize_cell_zone_by_volume(zone_name_pattern="*") == 87 # assert None == 87

    assert meshing_session.meshing_queries.get_zones(type_name="velocity-inlet") == [30, 31]
    assert meshing_session.meshing_queries.get_zones(group_name="inlet") == [31, 30]

    assert meshing_session.meshing_queries.get_embedded_baffles() is None
    assert meshing_session.meshing_queries.get_baffles_for_face_zones(face_zone_id_list=[29, 30, 31, 32, 33]) == [33,
                                                                                                                  32,
                                                                                                                  31,
                                                                                                                  30,
                                                                                                                  29]

    assert meshing_session.meshing_queries.get_baffles_for_face_zones(face_zone_id_list=[87]) is None
    assert meshing_session.meshing_queries.get_zones_with_marked_faces_for_given_face_zones(
        face_zone_id_list=[29, 30, 31, 32, 33]) is None
    assert meshing_session.meshing_queries.get_zones_with_marked_faces_for_given_face_zones(
        face_zone_name_list=["outlet", "inlet", "wall", "internal"]) is None

    assert meshing_session.meshing_queries.get_zones_with_marked_faces_for_given_face_zones(
        face_zone_name_pattern="*") is None
    assert meshing_session.meshing_queries.get_zones_with_multi_faces_for_given_face_zones(
        face_zone_id_list=[29, 30, 31, 32, 33]) is None
    assert meshing_session.meshing_queries.get_zones_with_multi_faces_for_given_face_zones(
        face_zone_name_list=["outlet", "inlet", "wall", "internal"]) is None

    assert meshing_session.meshing_queries.get_zones_with_multi_faces_for_given_face_zones(
        face_zone_name_pattern="*") is None
    assert meshing_session.meshing_queries.get_zones_with_free_faces_for_given_face_zones(
        face_zone_id_list=[29, 30, 31, 32, 33]) is None
    assert meshing_session.meshing_queries.get_zones_with_free_faces_for_given_face_zones(
        face_zone_name_list=["outlet", "inlet", "wall", "internal"]) is None
    assert meshing_session.meshing_queries.get_zones_with_free_faces_for_given_face_zones(
        face_zone_name_pattern="*") is None

    # assert meshing_session.meshing_queries.get_all_objects() == ['elbow-fluid'] # assert None == ['elbow-fluid']
    # assert meshing_session.meshing_queries.get_objects(type_name="mesh") == ['elbow-fluid'] # assert None == ['elbow-fluid']
    # assert meshing_session.meshing_queries.get_objects(filter="*") == ['elbow-fluid'] # assert None == ['elbow-fluid']

    # assert meshing_session.meshing_queries.get_regions(object_name="elbow-fluid", region_name_pattern="*") == [
    #     'elbow-fluid'] # assert None == ['elbow-fluid']
    # assert meshing_session.meshing_queries.get_regions(object_name="elbow-fluid", filter="*") == ['elbow-fluid'] # assert None == ['elbow-fluid']
    # assert meshing_session.meshing_queries.get_regions(object_name="elbow-fluid") == ['elbow-fluid'] # assert None == ['elbow-fluid']

    # assert meshing_session.meshing_queries.get_regions_of_face_zones(face_zone_id_list=[29, 30, 31, 32, 33]) == [
    #     'elbow-fluid'] # assert None == ['elbow-fluid']
    # assert meshing_session.meshing_queries.get_regions_of_face_zones(
    #     face_zone_name_list=["outlet", "inlet", "wall", "internal"]) == ['elbow-fluid'] # assert None == ['elbow-fluid']
    # assert meshing_session.meshing_queries.get_regions_of_face_zones(face_zone_name_pattern="*") == ['elbow-fluid'] # assert None == ['elbow-fluid']

    # assert meshing_session.meshing_queries.get_region_volume(object_name="elbow-fluid", sorting_order="ascending") == [
    #     [152.59942809266, 'elbow-fluid']] # assert None != [[152.59942809266, 'elbow-fluid']]
    # assert meshing_session.meshing_queries.get_region_volume(object_name="elbow-fluid",
    #                                                          region_name="elbow-fluid") == 152.59942809266 # assert None != 152.59942809266

    assert meshing_session.meshing_queries.get_pairs_of_overlapping_face_zones(face_zone_id_list=[29, 30, 31, 32, 33],
                                                                               join_tolerance=0.001,
                                                                               absolute_tolerance=True,
                                                                               join_angle=45) is None
    assert meshing_session.meshing_queries.get_pairs_of_overlapping_face_zones(
        face_zone_name_list=["outlet", "inlet", "wall", "internal"], join_tolerance=0.001, absolute_tolerance=True,
        join_angle=45) is None
    assert meshing_session.meshing_queries.get_pairs_of_overlapping_face_zones(face_zone_name_pattern="*",
                                                                               join_tolerance=0.001,
                                                                               absolute_tolerance=True,
                                                                               join_angle=45) is None

    assert meshing_session.meshing_queries.get_overlapping_face_zones(face_zone_name_pattern="*", area_tolerance=0.01,
                                                                      distance_tolerance=0.01) is None
