import pytest

from ansys.fluent.core import examples

import_filename = examples.download_file(
    "elbow.cas.h5", "pyfluent/examples/DOE-ML-Mixing-Elbow"
)


@pytest.mark.fluent_232
def test_meshing_queries(new_mesh_session):
    meshing_session = new_mesh_session
    meshing_session.tui.file.read_case(import_filename)

    assert (
        meshing_session.meshing_queries.get_face_zone_at_location([1.4, 1.4, 1.4]) == 34
    )

    assert meshing_session.meshing_queries.get_zones_of_type("velocity-inlet") == [
        30,
        31,
    ]

    assert meshing_session.meshing_queries.get_zones_of_group("inlet") == [31, 30]

    assert meshing_session.meshing_queries.get_face_zones_of_filter("*") == [
        3462,
        34,
        33,
        32,
        31,
        30,
        29,
    ]

    assert meshing_session.meshing_queries.get_cell_zones_of_filter("*") == [3460]

    assert meshing_session.meshing_queries.get_edge_zones_of_filter("*") == []

    assert meshing_session.meshing_queries.get_node_zones_of_filter("*") == [3625, 3624]

    assert meshing_session.meshing_queries.get_objects_of_type("mesh") == [
        "elbow-fluid"
    ]

    assert meshing_session.meshing_queries.get_face_zone_id_list_of_object(
        "elbow-fluid"
    ) == [
        29,
        30,
        31,
        32,
        33,
        34,
    ]

    assert (
        meshing_session.meshing_queries.get_edge_zone_id_list_of_object("elbow-fluid")
        == []
    )

    assert meshing_session.meshing_queries.get_cell_zone_id_list_of_object(
        "elbow-fluid"
    ) == [3460]

    assert (
        meshing_session.meshing_queries.get_face_zones_shared_by_regions_of_type(
            "elbow-fluid", "fluid-fluid"
        )
        == []
    )

    assert meshing_session.meshing_queries.get_face_zones_of_regions(
        "elbow-fluid", ["fluid"]
    ) == [34, 33, 32, 31, 30, 29]

    assert meshing_session.meshing_queries.get_face_zones_of_labels(
        "elbow-fluid", ["inlet", "outlet", "wall", "internal"]
    ) == [32]

    assert meshing_session.meshing_queries.get_face_zone_id_list_of_labels(
        "elbow-fluid", ["outlet"]
    ) == [32]

    assert meshing_session.meshing_queries.get_face_zones_of_objects(
        ["elbow-fluid"]
    ) == [
        29,
        30,
        31,
        32,
        33,
        34,
    ]

    assert (
        meshing_session.meshing_queries.get_edge_zones_of_objects(["elbow-fluid"]) == []
    )

    assert meshing_session.meshing_queries.get_face_zone_id_list_of_regions(
        "elbow-fluid", ["fluid"]
    ) == [
        34,
        33,
        32,
        31,
        30,
        29,
    ]

    assert (
        meshing_session.meshing_queries.get_prism_cell_zones(["inlet", "outlet"]) == []
    )

    assert meshing_session.meshing_queries.get_prism_cell_zones("*") == []

    assert meshing_session.meshing_queries.get_tet_cell_zones(["inlet", "outlet"]) == []

    assert meshing_session.meshing_queries.get_tet_cell_zones("*") == []

    assert meshing_session.meshing_queries.get_adjacent_cell_zones([30]) == [3460]

    assert meshing_session.meshing_queries.get_adjacent_cell_zones("*") == [3460]

    assert meshing_session.meshing_queries.get_adjacent_face_zones([3460]) == [
        29,
        30,
        31,
        32,
        33,
        34,
    ]

    assert meshing_session.meshing_queries.get_adjacent_face_zones("*") == [
        29,
        30,
        31,
        32,
        33,
        34,
    ]

    assert meshing_session.meshing_queries.get_shared_boundary_zones("*") == []

    assert meshing_session.meshing_queries.get_shared_boundary_zones([3460]) == []

    assert (
        meshing_session.meshing_queries.get_adjacent_interior_and_boundary_face_zones(
            [30]
        )
        == []
    )

    assert (
        meshing_session.meshing_queries.get_adjacent_interior_and_boundary_face_zones(
            "fluid"
        )
        == [29, 30, 31, 32, 33, 34, 3462]
    )

    assert (
        meshing_session.meshing_queries.get_adjacent_interior_and_boundary_face_zones(
            "*"
        )
        == [
            29,
            30,
            31,
            32,
            33,
            34,
            3462,
        ]
    )

    assert meshing_session.meshing_queries.get_adjacent_zones_by_edge_connectivity(
        [30]
    ) == [
        33,
        29,
    ]

    assert (
        meshing_session.meshing_queries.get_adjacent_zones_by_edge_connectivity("*")
        == []
    )

    assert meshing_session.meshing_queries.get_adjacent_zones_by_node_connectivity(
        [30]
    ) == [
        29,
        33,
    ]

    assert (
        meshing_session.meshing_queries.get_adjacent_zones_by_node_connectivity("*")
        == []
    )

    assert meshing_session.meshing_queries.get_interior_zones_connected_to_cell_zones(
        [3460]
    ) == [3462]

    assert meshing_session.meshing_queries.get_interior_zones_connected_to_cell_zones(
        "*"
    ) == [3462]

    assert (
        meshing_session.meshing_queries.get_face_zones_with_zone_specific_prisms_applied()
        == []
    )

    assert meshing_session.meshing_queries.get_face_zones_of_prism_controls("*") == [
        33,
        34,
    ]

    assert meshing_session.meshing_queries.get_baffles([29, 30]) == [30, 29]

    assert meshing_session.meshing_queries.get_embedded_baffles() == []

    assert meshing_session.meshing_queries.get_wrapped_zones() == []

    assert meshing_session.meshing_queries.get_unreferenced_edge_zones() == []

    assert meshing_session.meshing_queries.get_unreferenced_face_zones() == []

    assert meshing_session.meshing_queries.get_unreferenced_cell_zones() == []

    assert (
        meshing_session.meshing_queries.get_unreferenced_edge_zones_of_filter("*") == []
    )

    assert (
        meshing_session.meshing_queries.get_unreferenced_face_zones_of_filter("*") == []
    )

    assert (
        meshing_session.meshing_queries.get_unreferenced_cell_zones_of_filter("*") == []
    )

    assert (
        meshing_session.meshing_queries.get_unreferenced_edge_zone_id_list_of_pattern(
            "*"
        )
        == []
    )

    assert (
        meshing_session.meshing_queries.get_unreferenced_face_zone_id_list_of_pattern(
            "*"
        )
        == []
    )

    assert (
        meshing_session.meshing_queries.get_unreferenced_cell_zone_id_list_of_pattern(
            "*"
        )
        == []
    )

    assert meshing_session.meshing_queries.get_maxsize_cell_zone_by_volume("*") == 3460

    assert (
        meshing_session.meshing_queries.get_maxsize_cell_zone_by_volume([3460]) == 3460
    )

    assert meshing_session.meshing_queries.get_maxsize_cell_zone_by_count("*") == 3460

    assert (
        meshing_session.meshing_queries.get_maxsize_cell_zone_by_count([3460]) == 3460
    )

    assert meshing_session.meshing_queries.get_minsize_face_zone_by_area("*") == 30

    assert (
        meshing_session.meshing_queries.get_minsize_face_zone_by_area(
            [29, 30, 31, 32, 33, 34]
        )
        == 30
    )

    assert meshing_session.meshing_queries.get_minsize_face_zone_by_count("*") == 30

    assert (
        meshing_session.meshing_queries.get_minsize_face_zone_by_count(
            [29, 30, 31, 32, 33, 34]
        )
        == 30
    )

    assert (
        meshing_session.meshing_queries.get_face_zone_list_by_maximum_entity_count(
            20, True
        )
        == []
    )

    assert (
        meshing_session.meshing_queries.get_edge_zone_list_by_maximum_entity_count(
            20, False
        )
        == []
    )

    assert (
        meshing_session.meshing_queries.get_cell_zone_list_by_maximum_entity_count(1)
        == []
    )

    assert meshing_session.meshing_queries.get_face_zone_list_by_maximum_zone_area(
        100
    ) == [
        33,
        32,
        31,
        30,
    ]

    assert meshing_session.meshing_queries.get_face_zone_list_by_minimum_zone_area(
        10
    ) == [
        34,
        29,
    ]

    assert meshing_session.meshing_queries.get_zones_with_free_faces("*") == []
    assert (
        meshing_session.meshing_queries.get_zones_with_free_faces([29, 30, 31, 32])
        == []
    )
    assert (
        meshing_session.meshing_queries.get_zones_with_free_faces(["inlet", "outlet"])
        == []
    )

    assert meshing_session.meshing_queries.get_zones_with_multi_faces("*") == []
    assert (
        meshing_session.meshing_queries.get_zones_with_multi_faces([29, 30, 31, 32])
        == []
    )
    assert (
        meshing_session.meshing_queries.get_zones_with_multi_faces(["inlet", "outlet"])
        == []
    )

    assert (
        meshing_session.meshing_queries.get_overlapping_face_zones("*", 0.1, 0.1) == []
    )

    assert meshing_session.meshing_queries.get_zones_with_marked_faces("*") == []
    assert (
        meshing_session.meshing_queries.get_zones_with_marked_faces([29, 30, 31, 32])
        == []
    )
    assert (
        meshing_session.meshing_queries.get_zones_with_marked_faces(["inlet", "outlet"])
        == []
    )

    assert meshing_session.meshing_queries.get_all_object_name_list() == ["elbow-fluid"]

    assert meshing_session.meshing_queries.get_object_name_list_of_type("mesh") == [
        "elbow-fluid"
    ]

    assert meshing_session.meshing_queries.get_objects_of_filter("*") == ["elbow-fluid"]

    assert meshing_session.meshing_queries.get_regions_of_object("elbow-fluid") == [
        "fluid"
    ]

    assert meshing_session.meshing_queries.get_region_name_list_of_object(
        "elbow-fluid"
    ) == ["fluid"]

    assert (
        str(
            meshing_session.meshing_queries.sort_regions_by_volume(
                "elbow-fluid", "ascending"
            )
        )
        == '[volume: 152.599422561798\nregion: "fluid"\n]'
    )

    assert (
        meshing_session.meshing_queries.get_region_volume("elbow-fluid", "fluid")
        == 152.599422561798
    )

    assert meshing_session.meshing_queries.get_regions_of_filter(
        "elbow-fluid", "*"
    ) == ["fluid"]

    assert meshing_session.meshing_queries.get_region_name_list_of_pattern(
        "elbow-fluid", "*"
    ) == ["fluid"]

    assert meshing_session.meshing_queries.get_regions_of_face_zones(
        [29, 30, 31, 32, 33, 34]
    ) == ["fluid"]

    assert (
        str(meshing_session.meshing_queries.find_join_pairs("outlet", 0.1, True, 40))
        == "[]"
    )

    assert (
        str(meshing_session.meshing_queries.find_join_pairs([32], 0.1, True, 40))
        == "[]"
    )

    assert (
        str(meshing_session.meshing_queries.find_join_pairs(["outlet"], 0.1, True, 40))
        == "[]"
    )

    assert meshing_session.meshing_queries.get_region_name_list_of_face_zones(
        [29, 30, 31, 32, 33, 34]
    ) == ["fluid"]
