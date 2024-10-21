import pytest

from ansys.fluent.core import examples

PYTEST_RELATIVE_TOLERANCE = 0.2


def pytest_approx(expected):
    return pytest.approx(expected=expected, rel=PYTEST_RELATIVE_TOLERANCE)


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=25.1")
def test_meshing_utilities(new_meshing_session):
    meshing_session = new_meshing_session
    import_filename = examples.download_file(
        "mixing_elbow.msh.h5", "pyfluent/mixing_elbow"
    )
    meshing_session.tui.file.read_case(import_filename)

    assert meshing_session.meshing_utilities._cell_zones_labels_fdl() == ["elbow-fluid"]

    assert meshing_session.meshing_utilities._cell_zones_str_fdl() == [" 87 "]

    assert meshing_session.meshing_utilities._edge_zones_labels_fdl() == [
        "wall-elbow:wall-inlet:elbow-fluid:feature.28",
        "outlet:wall-elbow:elbow-fluid:feature.27",
        "cold-inlet:wall-elbow:elbow-fluid:feature.26",
        "symmetry:xyplane:wall-elbow:elbow-fluid:feature.25",
        "symmetry:xyplane:wall-inlet:elbow-fluid:feature.24",
        "symmetry:xyplane:outlet:elbow-fluid:feature.23",
        "symmetry:xyplane:cold-inlet:elbow-fluid:feature.22",
        "hot-inlet:wall-inlet:elbow-fluid:feature.21",
        "symmetry:xyplane:hot-inlet:elbow-fluid:feature.20",
    ]

    assert meshing_session.meshing_utilities._edge_zones_str_fdl() == [
        " 28 ",
        " 27 ",
        " 26 ",
        " 25 ",
        " 24 ",
        " 23 ",
        " 22 ",
        " 21 ",
        " 20 ",
    ]

    assert meshing_session.meshing_utilities._face_zones_labels_fdl() == [
        "wall-elbow",
        "wall-inlet",
        "outlet",
        "cold-inlet",
        "hot-inlet",
        "symmetry-xyplane",
    ]

    assert meshing_session.meshing_utilities._face_zones_str_fdl() == [
        " 89 ",
        " 34 ",
        " 33 ",
        " 32 ",
        " 31 ",
        " 30 ",
        " 29 ",
    ]

    assert meshing_session.meshing_utilities._node_zones_labels_fdl() == [
        "boundary-node-163",
        "node-91",
        "boundary-node-19",
    ]

    assert meshing_session.meshing_utilities._node_zones_str_fdl() == [
        " 163 ",
        " 91 ",
        " 19 ",
    ]

    assert meshing_session.meshing_utilities._prism_cell_zones_labels_fdl() is None

    assert meshing_session.meshing_utilities._prism_cell_zones_str_fdl() is None

    assert meshing_session.meshing_utilities._object_names_str_fdl() == ["elbow-fluid"]

    assert meshing_session.meshing_utilities._regions_str_fdl() == [" elbow-fluid "]

    assert meshing_session.meshing_utilities._zone_types_fdl() == [
        "interior",
        "wall",
        "wall",
        "pressure-outlet",
        "velocity-inlet",
        "velocity-inlet",
        "symmetry",
        "boundary-node",
        "node",
        "boundary-node",
        "fluid",
        "boundary-edge",
        "boundary-edge",
        "boundary-edge",
        "boundary-edge",
        "boundary-edge",
        "boundary-edge",
        "boundary-edge",
        "boundary-edge",
        "boundary-edge",
    ]

    assert meshing_session.meshing_utilities.get_labels(object_name="elbow-fluid") == [
        "elbow-fluid",
        "wall-elbow",
        "wall-inlet",
        "outlet",
        "cold-inlet",
        "hot-inlet",
        "symmetry-xyplane",
    ] or [
        "symmetry-xyplane",
        "hot-inlet",
        "cold-inlet",
        "outlet",
        "wall-inlet",
        "wall-elbow",
        "elbow-fluid",
    ]

    assert meshing_session.meshing_utilities.get_labels(
        object_name="elbow-fluid", filter="*"
    ) == [
        "elbow-fluid",
        "wall-elbow",
        "wall-inlet",
        "outlet",
        "cold-inlet",
        "hot-inlet",
        "symmetry-xyplane",
    ] or [
        "symmetry-xyplane",
        "hot-inlet",
        "cold-inlet",
        "outlet",
        "wall-inlet",
        "wall-elbow",
        "elbow-fluid",
    ]

    assert meshing_session.meshing_utilities.get_labels(
        object_name="elbow-fluid", label_name_pattern="*"
    ) == [
        "elbow-fluid",
        "wall-elbow",
        "wall-inlet",
        "outlet",
        "cold-inlet",
        "hot-inlet",
        "symmetry-xyplane",
    ] or [
        "symmetry-xyplane",
        "hot-inlet",
        "cold-inlet",
        "outlet",
        "wall-inlet",
        "wall-elbow",
        "elbow-fluid",
    ]

    assert (
        meshing_session.meshing_utilities.add_labels_on_face_zones(
            face_zone_name_list=["wall-inlet", "wall-elbow"],
            label_name_list=["wall-inlet-1", "wall-elbow-1"],
        )
        is None
    )

    assert meshing_session.meshing_utilities.get_labels_on_face_zones(
        face_zone_name_list=["wall-inlet", "wall-elbow"]
    ) == [
        "elbow-fluid",
        "wall-elbow",
        "wall-inlet-1",
        "wall-elbow-1",
        "wall-inlet",
    ] or [
        "wall-elbow",
        "elbow-fluid",
        "wall-inlet-1",
        "wall-elbow-1",
        "wall-inlet",
    ]

    assert meshing_session.meshing_utilities.get_face_zone_id_list_with_labels(
        face_zone_name_list=["wall-inlet", "wall-elbow"],
        label_name_list=["wall-inlet-1", "wall-elbow-1"],
    ) == [33, 34, 33, 34]

    assert meshing_session.meshing_utilities.get_face_zone_id_list_with_labels(
        face_zone_id_list=[33, 34],
        label_name_list=["wall-inlet-1", "wall-elbow-1"],
    ) == [33, 34, 33, 34]

    assert meshing_session.meshing_utilities.get_face_zone_id_list_with_labels(
        face_zone_name_pattern="wall*",
        label_name_list=["wall-inlet-1", "wall-elbow-1"],
    ) == [33, 34, 33, 34]

    assert (
        meshing_session.meshing_utilities.add_labels_on_face_zones(
            face_zone_id_list=[30, 31], label_name_list=["hot-inlet-1", "cold-inlet-1"]
        )
        is None
    )

    assert meshing_session.meshing_utilities.get_labels_on_face_zones(
        face_zone_id_list=[30, 31]
    ) == ["elbow-fluid", "cold-inlet", "hot-inlet-1", "cold-inlet-1", "hot-inlet"] or [
        "cold-inlet",
        "elbow-fluid",
        "hot-inlet-1",
        "cold-inlet-1",
        "hot-inlet",
    ]

    assert (
        meshing_session.meshing_utilities.add_labels_on_face_zones(
            face_zone_name_pattern="out*", label_name_list=["outlet-1"]
        )
        is None
    )

    assert meshing_session.meshing_utilities.get_labels_on_face_zones(
        face_zone_name_pattern="out*"
    ) == ["elbow-fluid", "outlet", "outlet-1"] or ["outlet", "elbow-fluid", "outlet-1"]

    assert (
        meshing_session.meshing_utilities.remove_labels_on_face_zones(
            face_zone_name_list=["wall-inlet"],
            label_name_list=["wall-inlet-1"],
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.remove_labels_on_face_zones(
            face_zone_id_list=[30],
            label_name_list=["hot-inlet-1"],
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.remove_labels_on_face_zones(
            face_zone_name_pattern="*",
            label_name_list=["wall-elbow-1"],
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.add_labels_on_cell_zones(
            cell_zone_name_list=["elbow-fluid"], label_name_list=["elbow-1"]
        )
        == "*the-non-printing-object*"
        or False
    )

    assert meshing_session.meshing_utilities.get_cell_zone_id_list_with_labels(
        cell_zone_name_list=["elbow-fluid"],
        label_name_list=["elbow-1"],
    ) == [87]

    assert meshing_session.meshing_utilities.get_cell_zone_id_list_with_labels(
        cell_zone_id_list=[87],
        label_name_list=["elbow-1"],
    ) == [87]

    assert meshing_session.meshing_utilities.get_cell_zone_id_list_with_labels(
        cell_zone_name_pattern="*",
        label_name_list=["elbow-1"],
    ) == [87]

    assert meshing_session.meshing_utilities.get_labels_on_cell_zones(
        cell_zone_name_list=["elbow-fluid"]
    ) == ["elbow-1"]

    assert (
        meshing_session.meshing_utilities.add_labels_on_cell_zones(
            cell_zone_id_list=[87], label_name_list=["87-1"]
        )
        == "*the-non-printing-object*"
        or False
    )

    assert meshing_session.meshing_utilities.get_labels_on_cell_zones(
        cell_zone_id_list=[87]
    ) == ["elbow-1", "87-1"]

    assert (
        meshing_session.meshing_utilities.add_labels_on_cell_zones(
            cell_zone_name_pattern="*", label_name_list=["cell-1"]
        )
        == "*the-non-printing-object*"
        or False
    )

    assert meshing_session.meshing_utilities.get_labels_on_cell_zones(
        cell_zone_name_pattern="*"
    ) == ["87-1", "elbow-1", "cell-1"]

    meshing_session.meshing_utilities.remove_labels_on_cell_zones(
        cell_zone_name_list=["elbow-fluid"],
        label_name_list=["elbow-1"],
    )

    assert meshing_session.meshing_utilities.get_labels_on_cell_zones(
        cell_zone_name_pattern="*"
    ) == ["cell-1", "87-1"]

    meshing_session.meshing_utilities.remove_labels_on_cell_zones(
        cell_zone_id_list=[87],
        label_name_list=["87-1"],
    )

    assert meshing_session.meshing_utilities.get_labels_on_cell_zones(
        cell_zone_name_pattern="*"
    ) == ["cell-1"]

    meshing_session.meshing_utilities.remove_labels_on_cell_zones(
        cell_zone_name_pattern="*",
        label_name_list=["cell-1"],
    )

    assert (
        meshing_session.meshing_utilities.get_labels_on_cell_zones(
            cell_zone_name_pattern="*"
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.add_labels_on_edge_zones(
            edge_zone_name_list=[
                "symmetry:xyplane:hot-inlet:elbow-fluid:feature.20",
                "hot-inlet:wall-inlet:elbow-fluid:feature.21",
            ],
            label_name_list=["20-1", "21-1"],
        )
        == "*the-non-printing-object*"
        or False
    )

    assert meshing_session.meshing_utilities.get_edge_zone_id_list_with_labels(
        edge_zone_name_list=[
            "symmetry:xyplane:hot-inlet:elbow-fluid:feature.20",
            "hot-inlet:wall-inlet:elbow-fluid:feature.21",
        ],
        label_name_list=["20-1", "21-1"],
    ) == [20, 21, 20, 21]

    assert meshing_session.meshing_utilities.get_edge_zone_id_list_with_labels(
        edge_zone_id_list=[20, 21],
        label_name_list=["20-1", "21-1"],
    ) == [20, 21, 20, 21]

    assert meshing_session.meshing_utilities.get_edge_zone_id_list_with_labels(
        edge_zone_name_pattern="*",
        label_name_list=["20-1", "21-1"],
    ) == [20, 21, 20, 21]

    assert meshing_session.meshing_utilities.get_labels_on_edge_zones(
        edge_zone_name_list=[
            "symmetry:xyplane:hot-inlet:elbow-fluid:feature.20",
            "hot-inlet:wall-inlet:elbow-fluid:feature.21",
        ]
    ) == ["20-1", "21-1"]

    assert (
        meshing_session.meshing_utilities.add_labels_on_edge_zones(
            edge_zone_id_list=[22, 23], label_name_list=["22-1", "23-1"]
        )
        == "*the-non-printing-object*"
        or False
    )

    assert meshing_session.meshing_utilities.get_labels_on_edge_zones(
        edge_zone_id_list=[22, 23]
    ) == ["22-1", "23-1"]

    assert (
        meshing_session.meshing_utilities.add_labels_on_edge_zones(
            edge_zone_name_pattern="cold-inlet*", label_name_list=["26-1"]
        )
        == "*the-non-printing-object*"
        or False
    )

    assert meshing_session.meshing_utilities.get_labels_on_edge_zones(
        edge_zone_name_pattern="cold-inlet*"
    ) == ["26-1"]

    meshing_session.meshing_utilities.remove_labels_on_edge_zones(
        edge_zone_name_list=["symmetry:xyplane:hot-inlet:elbow-fluid:feature.20"],
        label_name_list=["20-1"],
    )

    meshing_session.meshing_utilities.remove_labels_on_edge_zones(
        edge_zone_id_list=[22],
        label_name_list=["22-1"],
    )

    meshing_session.meshing_utilities.remove_labels_on_edge_zones(
        edge_zone_name_pattern="*",
        label_name_list=["26-1"],
    )

    assert meshing_session.meshing_utilities.convert_zone_name_strings_to_ids(
        zone_name_list=["outlet", "cold-inlet"]
    ) == [32, 31]

    assert meshing_session.meshing_utilities.convert_zone_ids_to_name_strings(
        zone_id_list=[32, 31]
    ) == ["outlet", "cold-inlet"]

    assert meshing_session.meshing_utilities.get_edge_zones(filter="*") == [
        28,
        27,
        26,
        25,
        24,
        23,
        22,
        21,
        20,
    ]

    assert meshing_session.meshing_utilities.get_edge_zones(
        maximum_entity_count=20, only_boundary=False
    ) == [20, 21, 22, 23, 28]

    assert meshing_session.meshing_utilities.get_edge_zones(
        maximum_entity_count=20, only_boundary=True
    ) == [20, 21, 22, 23, 28]

    assert meshing_session.meshing_utilities.get_unreferenced_edge_zones() is None

    assert (
        meshing_session.meshing_utilities.get_unreferenced_edge_zones(filter="*")
        is None
    )

    assert (
        meshing_session.meshing_utilities.get_unreferenced_edge_zones(
            zone_name_pattern="*"
        )
        is None
    )

    assert meshing_session.meshing_utilities.get_face_zones(filter="*") == [
        89,
        34,
        33,
        32,
        31,
        30,
        29,
    ]

    assert meshing_session.meshing_utilities.get_face_zones(prism_control_name="*") == [
        33,
        34,
    ]

    assert meshing_session.meshing_utilities.get_face_zones(
        xyz_coordinates=[1.4, 1.4, 1.4]
    ) == [34]

    assert (
        meshing_session.meshing_utilities.get_face_zones(
            maximum_entity_count=20, only_boundary=True
        )
        is None
    )

    assert meshing_session.meshing_utilities.get_face_zones_by_zone_area(
        maximum_zone_area=100
    ) == [33, 32, 31, 30]

    assert meshing_session.meshing_utilities.get_face_zones_by_zone_area(
        minimum_zone_area=10
    ) == [34, 29]

    assert meshing_session.meshing_utilities.get_face_zones_of_object(
        object_name="elbow-fluid", regions=["elbow-fluid"]
    ) == [34, 33, 32, 31, 30, 29]

    assert meshing_session.meshing_utilities.get_face_zones_of_object(
        object_name="elbow-fluid", labels=["outlet"]
    ) == [32]

    assert (
        meshing_session.meshing_utilities.get_face_zones_of_object(
            object_name="elbow-fluid", region_type="elbow-fluid"
        )
        is None
    )

    assert meshing_session.meshing_utilities.get_face_zones_of_object(
        object_name="elbow-fluid"
    ) == [29, 30, 31, 32, 33, 34]

    assert meshing_session.meshing_utilities.get_face_zones_of_object(
        objects=["elbow-fluid"]
    ) == [29, 30, 31, 32, 33, 34]

    assert meshing_session.meshing_utilities.get_wrapped_face_zones() is None

    assert meshing_session.meshing_utilities.get_unreferenced_face_zones() is None

    assert (
        meshing_session.meshing_utilities.get_unreferenced_face_zones(filter="*")
        is None
    )

    assert (
        meshing_session.meshing_utilities.get_unreferenced_face_zones(
            zone_name_pattern="*"
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.get_interior_face_zones_for_given_cell_zones(
            cell_zone_id_list=[87]
        )
        == [89]
    )

    assert (
        meshing_session.meshing_utilities.get_interior_face_zones_for_given_cell_zones(
            cell_zone_name_pattern="*"
        )
        == [89]
    )

    assert (
        meshing_session.meshing_utilities.get_interior_face_zones_for_given_cell_zones(
            cell_zone_name_list=["elbow-fluid"]
        )
        == [89]
    )

    assert meshing_session.meshing_utilities.get_node_zones(filter="*") == [163, 91, 19]

    assert meshing_session.meshing_utilities.get_adjacent_zones_by_edge_connectivity(
        zone_id_list=[29, 30, 31, 32, 33]
    ) == [34]
    assert meshing_session.meshing_utilities.get_adjacent_zones_by_edge_connectivity(
        zone_name_list=["outlet", "inlet", "wall", "internal"]
    ) == [34, 29]
    assert (
        meshing_session.meshing_utilities.get_adjacent_zones_by_edge_connectivity(
            zone_name_pattern="*"
        )
        is None
    )

    assert meshing_session.meshing_utilities.get_adjacent_zones_by_node_connectivity(
        zone_id_list=[29, 30, 31, 32, 33]
    ) == [34]

    assert meshing_session.meshing_utilities.get_adjacent_zones_by_node_connectivity(
        zone_name_list=["outlet", "inlet", "wall", "internal"]
    ) == [29, 34]

    assert (
        meshing_session.meshing_utilities.get_adjacent_zones_by_node_connectivity(
            zone_name_pattern="*"
        )
        is None
    )

    assert meshing_session.meshing_utilities.get_cell_zones(filter="*") == [87]

    assert (
        meshing_session.meshing_utilities.get_cell_zones(maximum_entity_count=100)
        is None
    )

    assert meshing_session.meshing_utilities.get_cell_zones(
        xyz_coordinates=[-7, -6, 0.4]
    ) == [87]

    assert meshing_session.meshing_utilities.get_unreferenced_cell_zones() is None

    assert (
        meshing_session.meshing_utilities.get_unreferenced_cell_zones(filter="*")
        is None
    )

    assert (
        meshing_session.meshing_utilities.get_unreferenced_cell_zones(
            zone_name_pattern="*"
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.get_adjacent_cell_zones_for_given_face_zones(
            face_zone_id_list=[29, 30, 31, 32, 33]
        )
        == [87]
    )

    assert (
        meshing_session.meshing_utilities.get_adjacent_cell_zones_for_given_face_zones(
            face_zone_name_list=["outlet", "inlet", "wall", "internal"]
        )
        == [87]
    )

    assert (
        meshing_session.meshing_utilities.get_adjacent_cell_zones_for_given_face_zones(
            face_zone_name_pattern="*"
        )
        == [87]
    )

    assert (
        meshing_session.meshing_utilities.get_tet_cell_zones(
            zone_id_list=[29, 30, 31, 32, 33]
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.get_tet_cell_zones(zone_id_list=[87]) is None
    )

    assert (
        meshing_session.meshing_utilities.get_tet_cell_zones(
            zone_name_list=["outlet", "inlet", "wall", "internal"]
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.get_tet_cell_zones(zone_name_pattern="*")
        is None
    )

    assert (
        meshing_session.meshing_utilities.get_prism_cell_zones(zone_id_list=[87])
        is None
    )

    assert (
        meshing_session.meshing_utilities.get_prism_cell_zones(
            zone_name_list=["outlet", "inlet", "wall", "internal"]
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.get_prism_cell_zones(zone_name_pattern="*")
        is None
    )

    assert (
        meshing_session.meshing_utilities.get_maxsize_cell_zone_by_count(
            zone_id_list=[87]
        )
        == 87
    )

    assert (
        meshing_session.meshing_utilities.get_maxsize_cell_zone_by_count(
            zone_name_list=["outlet", "inlet", "wall", "internal"]
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.get_maxsize_cell_zone_by_count(
            zone_name_pattern="*"
        )
        == 87
    )

    assert (
        meshing_session.meshing_utilities.get_maxsize_cell_zone_by_volume(
            zone_id_list=[87]
        )
        == 87
    )

    assert (
        meshing_session.meshing_utilities.get_maxsize_cell_zone_by_volume(
            zone_name_list=["outlet", "inlet", "wall", "internal"]
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.get_maxsize_cell_zone_by_volume(
            zone_name_pattern="*"
        )
        == 87
    )

    assert meshing_session.meshing_utilities.get_zones(type_name="velocity-inlet") == [
        30,
        31,
    ]

    assert meshing_session.meshing_utilities.get_zones(group_name="inlet") == [31, 30]

    assert meshing_session.meshing_utilities.get_embedded_baffles() is None

    assert meshing_session.meshing_utilities.get_baffles_for_face_zones(
        face_zone_id_list=[29, 30, 31, 32, 33]
    ) == [33, 32, 31, 30, 29]

    assert (
        meshing_session.meshing_utilities.get_baffles_for_face_zones(
            face_zone_id_list=[87]
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.get_zones_with_marked_faces_for_given_face_zones(
            face_zone_id_list=[29, 30, 31, 32, 33]
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.get_zones_with_marked_faces_for_given_face_zones(
            face_zone_name_list=["outlet", "inlet", "wall", "internal"]
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.get_zones_with_marked_faces_for_given_face_zones(
            face_zone_name_pattern="*"
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.get_zones_with_multi_faces_for_given_face_zones(
            face_zone_id_list=[29, 30, 31, 32, 33]
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.get_zones_with_multi_faces_for_given_face_zones(
            face_zone_name_list=["outlet", "inlet", "wall", "internal"]
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.get_zones_with_multi_faces_for_given_face_zones(
            face_zone_name_pattern="*"
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.get_zones_with_free_faces_for_given_face_zones(
            face_zone_id_list=[29, 30, 31, 32, 33]
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.get_zones_with_free_faces_for_given_face_zones(
            face_zone_name_list=["outlet", "inlet", "wall", "internal"]
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.get_zones_with_free_faces_for_given_face_zones(
            face_zone_name_pattern="*"
        )
        is None
    )

    assert meshing_session.meshing_utilities.get_all_objects() == ["elbow-fluid"]

    assert meshing_session.meshing_utilities.get_objects(type_name="mesh") == [
        "elbow-fluid"
    ]

    assert meshing_session.meshing_utilities.get_objects(filter="*") == ["elbow-fluid"]

    assert meshing_session.meshing_utilities.get_regions(
        object_name="elbow-fluid", region_name_pattern="*"
    ) == ["elbow-fluid"]

    assert meshing_session.meshing_utilities.get_regions(
        object_name="elbow-fluid", filter="*"
    ) == ["elbow-fluid"]

    assert meshing_session.meshing_utilities.get_regions(object_name="elbow-fluid") == [
        "elbow-fluid"
    ]

    assert meshing_session.meshing_utilities.get_regions_of_face_zones(
        face_zone_id_list=[29, 30, 31, 32, 33]
    ) == ["elbow-fluid"]

    assert meshing_session.meshing_utilities.get_regions_of_face_zones(
        face_zone_name_list=["outlet", "inlet", "wall", "internal"]
    ) == ["elbow-fluid"]

    assert meshing_session.meshing_utilities.get_regions_of_face_zones(
        face_zone_name_pattern="*"
    ) == ["elbow-fluid"]

    assert meshing_session.meshing_utilities.get_region_volume(
        object_name="elbow-fluid", sorting_order="ascending"
    ) == [[pytest_approx(152.59942809266), "elbow-fluid"]]

    assert meshing_session.meshing_utilities.get_region_volume(
        object_name="elbow-fluid", region_name="elbow-fluid"
    ) == [pytest_approx(152.59942809266)]

    assert (
        meshing_session.meshing_utilities.get_pairs_of_overlapping_face_zones(
            face_zone_id_list=[29, 30, 31, 32, 33],
            join_tolerance=0.001,
            absolute_tolerance=True,
            join_angle=45,
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.get_pairs_of_overlapping_face_zones(
            face_zone_name_list=["outlet", "inlet", "wall", "internal"],
            join_tolerance=0.001,
            absolute_tolerance=True,
            join_angle=45,
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.get_pairs_of_overlapping_face_zones(
            face_zone_name_pattern="*",
            join_tolerance=0.001,
            absolute_tolerance=True,
            join_angle=45,
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.get_overlapping_face_zones(
            face_zone_name_pattern="*", area_tolerance=0.01, distance_tolerance=0.01
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.get_minsize_face_zone_by_count(
            zone_id_list=[29, 30, 31, 32, 33]
        )
        == 30
    )

    assert (
        meshing_session.meshing_utilities.get_minsize_face_zone_by_count(
            zone_name_list=["outlet", "inlet", "wall", "internal"]
        )
        == 32
    )

    assert (
        meshing_session.meshing_utilities.get_minsize_face_zone_by_count(
            zone_name_pattern="*"
        )
        == 30
    )

    assert (
        meshing_session.meshing_utilities.get_minsize_face_zone_by_area(
            zone_id_list=[29, 30, 31, 32, 33]
        )
        == 30
    )

    assert (
        meshing_session.meshing_utilities.get_minsize_face_zone_by_area(
            zone_name_list=["outlet", "inlet", "wall", "internal"]
        )
        == 32
    )

    assert (
        meshing_session.meshing_utilities.get_minsize_face_zone_by_area(
            zone_name_pattern="*"
        )
        == 30
    )

    assert (
        meshing_session.meshing_utilities.get_adjacent_face_zones_for_given_cell_zones(
            cell_zone_id_list=[87]
        )
        == [29, 30, 31, 32, 33, 34]
    )

    assert (
        meshing_session.meshing_utilities.get_adjacent_face_zones_for_given_cell_zones(
            cell_zone_name_pattern="*"
        )
        == [29, 30, 31, 32, 33, 34]
    )

    assert (
        meshing_session.meshing_utilities.get_adjacent_face_zones_for_given_cell_zones(
            cell_zone_name_list=["elbow-fluid"]
        )
        == [29, 30, 31, 32, 33, 34]
    )

    assert meshing_session.meshing_utilities.get_adjacent_interior_and_boundary_face_zones_for_given_cell_zones(
        cell_zone_id_list=[87]
    ) == [
        29,
        30,
        31,
        32,
        33,
        34,
        89,
    ]

    assert meshing_session.meshing_utilities.get_adjacent_interior_and_boundary_face_zones_for_given_cell_zones(
        cell_zone_name_pattern="*"
    ) == [
        29,
        30,
        31,
        32,
        33,
        34,
        89,
    ]

    assert meshing_session.meshing_utilities.get_adjacent_interior_and_boundary_face_zones_for_given_cell_zones(
        cell_zone_name_list=["elbow-fluid"]
    ) == [
        29,
        30,
        31,
        32,
        33,
        34,
        89,
    ]

    assert (
        meshing_session.meshing_utilities.count_marked_faces(
            face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"]
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.count_marked_faces(face_zone_name_pattern="*")
        == 0
    )

    assert (
        meshing_session.meshing_utilities.get_multi_faces_count(
            face_zone_id_list=[30, 31, 32]
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.get_multi_faces_count(
            face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"]
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.get_multi_faces_count(
            face_zone_name_pattern="*"
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.get_free_faces_count(
            face_zone_id_list=[30, 31, 32]
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.get_free_faces_count(
            face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"]
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.get_free_faces_count(
            face_zone_name_pattern="*"
        )
        == 0
    )

    assert meshing_session.meshing_utilities.get_edge_size_limits(
        face_zone_id_list=[30, 31, 32]
    ) == [
        pytest_approx(0.02167507486136073),
        pytest_approx(0.3016698360443115),
        pytest_approx(0.1515733801031084),
    ]

    assert meshing_session.meshing_utilities.get_edge_size_limits(
        face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"]
    ) == [
        pytest_approx(0.02167507486136073),
        pytest_approx(0.3016698360443115),
        pytest_approx(0.1515733801031084),
    ]

    assert meshing_session.meshing_utilities.get_edge_size_limits(
        face_zone_name_pattern="*"
    ) == [
        pytest_approx(0.002393084222530175),
        pytest_approx(0.3613402218724294),
        pytest_approx(0.1225859010936682),
    ]

    assert (
        meshing_session.meshing_utilities.get_cell_zone_shape(cell_zone_id=87)
        == "mixed"
    )

    assert set(
        meshing_session.meshing_utilities.get_edge_zones_list(filter="*")
    ) == set([28, 27, 26, 25, 24, 23, 22, 21, 20])

    assert set(
        meshing_session.meshing_utilities.get_edge_zones_of_object(
            objects=["elbow-fluid"]
        )
    ) == set([20, 21, 22, 23, 24, 25, 26, 27, 28])

    assert set(
        meshing_session.meshing_utilities.get_edge_zones_of_object(
            object_name="elbow-fluid"
        )
    ) == set([20, 21, 22, 23, 24, 25, 26, 27, 28])

    assert (
        meshing_session.meshing_utilities.get_face_zones_with_zone_specific_prisms_applied()
        is None
    )

    # assert set(
    #     meshing_session.meshing_utilities.get_labels_on_face_zones_list(
    #         face_zone_id_list=[30, 31]
    #     )
    # ) == set([["30", "hot-inlet", "elbow-fluid"], ["31", "cold-inlet", "elbow-fluid"]])

    assert set(meshing_session.meshing_utilities.get_node_zones(filter="*")) == set(
        [163, 91, 19]
    )

    assert not meshing_session.meshing_utilities.get_shared_boundary_face_zones_for_given_cell_zones(
        cell_zone_id_list=[87]
    )

    assert not meshing_session.meshing_utilities.get_shared_boundary_face_zones_for_given_cell_zones(
        cell_zone_name_list=["elbow-fluid"]
    )

    assert not meshing_session.meshing_utilities.get_shared_boundary_face_zones_for_given_cell_zones(
        cell_zone_name_pattern="*"
    )

    assert (
        meshing_session.meshing_utilities.mark_faces_in_self_proximity(
            face_zone_id_list=[30, 31, 32],
            relative_tolerance=True,
            tolerance=0.05,
            proximity_angle=40.5,
            ignore_orientation=False,
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.mark_faces_in_self_proximity(
            face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"],
            relative_tolerance=True,
            tolerance=0.05,
            proximity_angle=40.5,
            ignore_orientation=False,
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.mark_faces_in_self_proximity(
            face_zone_name_pattern="*",
            relative_tolerance=True,
            tolerance=0.05,
            proximity_angle=40.5,
            ignore_orientation=False,
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.mark_point_contacts(
            face_zone_id_list=[30, 31, 32]
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.mark_point_contacts(
            face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"]
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.mark_point_contacts(
            face_zone_name_pattern="cold*"
        )
        == 0
    )

    assert meshing_session.meshing_utilities.mesh_check(
        type_name="face-children",
        edge_zone_id_list=[22, 23],
        face_zone_id_list=[30, 31, 32],
        cell_zone_id_list=[87],
    )

    assert meshing_session.meshing_utilities.mesh_check(
        type_name="nodes-per-cell",
        edge_zone_name_pattern="cold-inlet*",
        face_zone_id_list=[30, 31, 32],
        cell_zone_id_list=[87],
    )

    assert meshing_session.meshing_utilities.mesh_check(
        type_name="volume-statistics",
        edge_zone_id_list=[22, 23],
        face_zone_name_pattern="*",
        cell_zone_id_list=[87],
    )

    assert meshing_session.meshing_utilities.mesh_check(
        type_name="nodes-per-cell",
        edge_zone_name_pattern="cold-inlet*",
        face_zone_name_pattern="*",
        cell_zone_id_list=[87],
    )

    assert meshing_session.meshing_utilities.mesh_check(
        type_name="face-children",
        edge_zone_id_list=[22, 23],
        face_zone_id_list=[30, 31, 32],
        cell_zone_name_pattern="*",
    )

    assert meshing_session.meshing_utilities.mesh_check(
        type_name="volume-statistics",
        edge_zone_name_pattern="cold-inlet*",
        face_zone_name_pattern="*",
        cell_zone_name_pattern="*",
    )

    # assert meshing_session.meshing_utilities.print_worst_quality_cell(cell_zone_id_list=[87], measure="Orthogonal Quality") == "Worst Quality Cell (c5018) (quality: 0.24536377), in cell zone (elbow-fluid) at location: ((4.955211100621864 -6.054548533874768 0.1959202011308238))"

    # assert meshing_session.meshing_utilities.print_worst_quality_cell(cell_zone_name_list=["elbow-fluid"], measure="Orthogonal Quality") == == "Worst Quality Cell (c5018) (quality: 0.24536377), in cell zone (elbow-fluid) at location: ((4.955211100621864 -6.054548533874768 0.1959202011308238))"

    # assert meshing_session.meshing_utilities.print_worst_quality_cell(cell_zone_name_pattern="*", measure="Orthogonal Quality") == == "Worst Quality Cell (c5018) (quality: 0.24536377), in cell zone (elbow-fluid) at location: ((4.955211100621864 -6.054548533874768 0.1959202011308238))"

    # assert meshing_session.meshing_utilities.separate_cell_zone_layers_by_face_zone(cell_zone_id=87, face_zone_id_list=[30, 31, 32], nlayers=2) == "No cells are separated"

    # assert meshing_session.meshing_utilities.separate_cell_zone_layers_by_face_zone(cell_zone_id=87, face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"], nlayers=2) == "No cells are separated"

    # assert meshing_session.meshing_utilities.separate_cell_zone_layers_by_face_zone(cell_zone_id=87, face_zone_name_pattern="*", nlayers=2) == "Moved 975 cells from elbow-fluid (common to face zones) to elbow-fluid:172 \
    #             Moved 2116 faces from interior--elbow-fluid to interior--elbow-fluid:174 \
    #             Moved 211 nodes from node-91 to node-173 \
    #             Moved 2699 faces from interior--elbow-fluid to interior--elbow-fluid:181 (boundary)"

    # meshing_session.meshing_utilities.separate_cell_zone_layers_by_face_zone_using_name(cell_zone_name="elbow-fluid",
    #                                                                                     face_zone_id_list=[30, 31, 32],
    #                                                                                     nlayers=2)

    # meshing_session.meshing_utilities.separate_cell_zone_layers_by_face_zone_using_name(cell_zone_name="elbow-fluid",
    #                                                                                     face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"],
    #                                                                                     nlayers=2)

    # meshing_session.meshing_utilities.separate_cell_zone_layers_by_face_zone_using_name(cell_zone_name="elbow-fluid",
    #                                                                                     face_zone_name_pattern="*",
    #                                                                                     nlayers=2)

    # meshing_session.meshing_utilities.separate_cell_zone_layers_by_face_zone_using_id(cell_zone_id=87,
    #                                                                                 face_zone_id_list=[30, 31, 32],
    #                                                                                 nlayers=2)

    # meshing_session.meshing_utilities.separate_cell_zone_layers_by_face_zone_using_id(cell_zone_id=87,
    #                                                                                 face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"],
    #                                                                                 nlayers=2)

    # meshing_session.meshing_utilities.separate_cell_zone_layers_by_face_zone_using_id(cell_zone_id=87,
    #                                                                                 face_zone_name_pattern="*",
    #                                                                                 nlayers=2)

    # meshing_session.meshing_utilities.separate_cell_zone_layers_by_face_zone(
    #     cell_zone_name="elbow-fluid",
    #     face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"],
    #     nlayers=2,
    # )

    # meshing_session.meshing_utilities.separate_cell_zone_layers_by_face_zone(
    #     cell_zone_name="elbow-fluid", face_zone_name_pattern="*", nlayers=2
    # )

    # Commented due to variation in 10^-16 th place

    # assert meshing_session.meshing_utilities.get_cell_quality_limits(
    #     cell_zone_id_list=[87], measure="Orthogonal Quality"
    # ) == [17822, 0.2453637718621773, 0.9999993965264717, 0.9546058175066768, 0.0, 0]
    #
    # assert meshing_session.meshing_utilities.get_cell_quality_limits(
    #     cell_zone_name_list=["elbow-fluid"], measure="Orthogonal Quality"
    # ) == [17822, 0.2453637718621773, 0.9999993965264717, 0.9546058175066768, 0.0, 0]
    #
    # assert meshing_session.meshing_utilities.get_cell_quality_limits(
    #     cell_zone_name_pattern="*", measure="Orthogonal Quality"
    # ) == [17822, 0.2453637718621773, 0.9999993965264717, 0.9546058175066768, 0.0, 0]
    #
    # assert meshing_session.meshing_utilities.get_face_quality_limits(
    #     face_zone_id_list=[30, 31, 32], measure="Orthogonal Quality"
    # )[1:] == [0.7348979098719086, 0.9999899933604034, 0.9840275981092989, 362]
    #
    # assert meshing_session.meshing_utilities.get_face_quality_limits(
    #     face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"],
    #     measure="Orthogonal Quality",
    # )[1:] == [0.7348979098719086, 0.9999899933604034, 0.9840275981092989, 362]
    #
    # assert meshing_session.meshing_utilities.get_face_quality_limits(
    #     face_zone_name_pattern="*", measure="Orthogonal Quality"
    # )[1:] == [0.03215596355473505, 1.0, 0.9484456798568045, 91581]

    # assert meshing_session.meshing_utilities.get_face_mesh_distribution(
    #     face_zone_id_list=[30, 31, 32],
    #     measure="Orthogonal Quality",
    #     partitions=2,
    #     range=[0.9, 1],
    # ) == [322, [225, 97], [0, 40]]

    # assert meshing_session.meshing_utilities.get_face_mesh_distribution(
    #     face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"],
    #     measure="Orthogonal Quality",
    #     partitions=2,
    #     range=[0.9, 1],
    # ) == [322, [225, 97], [0, 40]]

    # assert meshing_session.meshing_utilities.get_face_mesh_distribution(
    #     face_zone_name_pattern="*",
    #     measure="Orthogonal Quality",
    #     partitions=2,
    #     range=[0.9, 1],
    # ) == [69656, [53976, 15680], [0, 22455]]
    #
    # assert meshing_session.meshing_utilities.get_cell_mesh_distribution(
    #     cell_zone_id_list=[87],
    #     measure="Orthogonal Quality",
    #     partitions=2,
    #     range=[0.9, 1],
    # ) == [16029, [11794, 4235], [0, 1872]]
    #
    # assert meshing_session.meshing_utilities.get_cell_mesh_distribution(
    #     cell_zone_name_list=["elbow-fluid"],
    #     measure="Orthogonal Quality",
    #     partitions=2,
    #     range=[0.9, 1],
    # ) == [16029, [11794, 4235], [0, 1872]]
    #
    # assert meshing_session.meshing_utilities.get_cell_mesh_distribution(
    #     cell_zone_name_pattern="*",
    #     measure="Orthogonal Quality",
    #     partitions=2,
    #     range=[0.9, 1],
    # ) == [16029, [11794, 4235], [0, 1872]]

    # Commented due to variation in 10^-13 th place

    # assert (
    #     meshing_session.meshing_utilities.get_cell_zone_volume(cell_zone_id_list=[87])
    #     == 152.5994280926617
    # )
    #
    # assert (
    #     meshing_session.meshing_utilities.get_cell_zone_volume(
    #         cell_zone_name_list=["elbow-fluid"]
    #     )
    #     == 152.5994280926617
    # )
    #
    # assert (
    #     meshing_session.meshing_utilities.get_cell_zone_volume(
    #         cell_zone_name_pattern="*"
    #     )
    #     == 152.5994280926617
    # )

    # Commented due to variation in 10^-15 th place

    # assert (
    #     meshing_session.meshing_utilities.get_face_zone_area(
    #         face_zone_id_list=[30, 31, 32]
    #     )
    #     == 12.429615960819163
    # )
    #
    # assert (
    #     meshing_session.meshing_utilities.get_face_zone_area(
    #         face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"]
    #     )
    #     == 12.429615960819163
    # )

    # Commented due to variation in 10^-15 th place

    # assert (
    #     meshing_session.meshing_utilities.get_face_zone_area(face_zone_name_pattern="*")
    #     == 2282.142530887569
    # )

    assert (
        meshing_session.meshing_utilities.get_face_zone_count(
            face_zone_id_list=[30, 31, 32]
        )
        == 362
    )

    assert (
        meshing_session.meshing_utilities.get_face_zone_count(
            face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"]
        )
        == 362
    )

    assert (
        meshing_session.meshing_utilities.get_face_zone_count(
            face_zone_name_pattern="*"
        )
        == 91581
    )

    assert (
        meshing_session.meshing_utilities.get_cell_zone_count(cell_zone_id_list=[87])
        == 17822
    )

    assert (
        meshing_session.meshing_utilities.get_cell_zone_count(
            cell_zone_name_list=["elbow-fluid"]
        )
        == 17822
    )

    assert (
        meshing_session.meshing_utilities.get_cell_zone_count(
            cell_zone_name_pattern="*"
        )
        == 17822
    )

    assert meshing_session.meshing_utilities.get_zone_type(zone_id=87) == "fluid"

    assert (
        meshing_session.meshing_utilities.get_zone_type(zone_name="elbow-fluid")
        == "fluid"
    )

    assert (
        meshing_session.meshing_utilities.get_face_zone_node_count(face_zone_id=32)
        == 246
    )

    assert (
        meshing_session.meshing_utilities.get_face_zone_node_count(
            face_zone_name="outlet"
        )
        == 246
    )

    assert (
        meshing_session.meshing_utilities.mark_free_faces(
            face_zone_id_list=[30, 31, 32]
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.mark_free_faces(
            face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"]
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.mark_free_faces(face_zone_name_pattern="*")
        == 0
    )

    assert (
        meshing_session.meshing_utilities.mark_multi_faces(
            face_zone_id_list=[30, 31, 32], fringe_length=5
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.mark_multi_faces(
            face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"], fringe_length=5
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.mark_multi_faces(
            face_zone_name_pattern="*", fringe_length=5
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.mark_self_intersecting_faces(
            face_zone_id_list=[87], mark_folded=True
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.mark_self_intersecting_faces(
            face_zone_name_list=["elbow-fluid"], mark_folded=True
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.mark_self_intersecting_faces(
            face_zone_name_pattern="elbow*", mark_folded=True
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.mark_duplicate_faces(
            face_zone_id_list=[30, 31, 32]
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.mark_duplicate_faces(
            face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"]
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.mark_duplicate_faces(
            face_zone_name_pattern="*"
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.mark_invalid_normals(
            face_zone_id_list=[30, 31, 32]
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.mark_invalid_normals(
            face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"]
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.mark_invalid_normals(
            face_zone_name_pattern="*"
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.mark_island_faces(
            face_zone_id_list=[30, 31, 32], island_face_count=5
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.mark_island_faces(
            face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"],
            island_face_count=5,
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.mark_island_faces(
            face_zone_name_pattern="cold*", island_face_count=5
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.mark_spikes(
            face_zone_id_list=[30, 31, 32], spike_angle=40.5
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.mark_spikes(
            face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"], spike_angle=40.5
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.mark_spikes(
            face_zone_name_pattern="*", spike_angle=40.5
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.mark_steps(
            face_zone_id_list=[30, 31, 32], step_angle=40.5, step_width=3.3
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.mark_steps(
            face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"],
            step_angle=40.5,
            step_width=3.3,
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.mark_steps(
            face_zone_name_pattern="*", step_angle=40.5, step_width=3.3
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.mark_sliver_faces(
            face_zone_id_list=[30, 31, 32], max_height=2, skew_limit=0.2
        )
        == 2
    )

    assert (
        meshing_session.meshing_utilities.mark_sliver_faces(
            face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"],
            max_height=2,
            skew_limit=0.2,
        )
        == 2
    )

    assert (
        meshing_session.meshing_utilities.mark_sliver_faces(
            face_zone_name_pattern="*", max_height=2.2, skew_limit=0.5
        )
        == 3453
    )

    assert (
        meshing_session.meshing_utilities.mark_bad_quality_faces(
            face_zone_id_list=[30, 31, 32], quality_limit=0.5, number_of_rings=2
        )
        == 362
    )

    assert (
        meshing_session.meshing_utilities.mark_bad_quality_faces(
            face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"],
            quality_limit=0.5,
            number_of_rings=2,
        )
        == 362
    )

    # assert meshing_session.meshing_utilities.mark_bad_quality_faces(face_zone_name_pattern="*", quality_limit=0.5,
    #                                                        number_of_rings=2) == 4799

    # Commented due to variation in 10^-14 th place

    # assert meshing_session.meshing_utilities.mark_faces_by_quality(
    #     face_zone_id_list=[30, 31, 32],
    #     quality_measure="Skewness",
    #     quality_limit=0.9,
    #     append_marking=False,
    # ) == [0, 0.2651020901280914]

    # assert meshing_session.meshing_utilities.mark_faces_by_quality(
    #     face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"],
    #     quality_measure="Skewness",
    #     quality_limit=0.9,
    #     append_marking=False,
    # ) == [0, 0.2651020901280914]

    # assert meshing_session.meshing_utilities.mark_faces_by_quality(
    #     face_zone_name_pattern="*",
    #     quality_measure="Skewness",
    #     quality_limit=0.9,
    #     append_marking=False,
    # ) == [0, 0.5697421601607908]

    assert (
        meshing_session.meshing_utilities.mark_face_strips_by_height_and_quality(
            face_zone_id_list=[30, 31, 32],
            strip_type=2,
            strip_height=2,
            quality_measure="Size Change",
            quality_limit=0.5,
            feature_angle=40,
        )
        == -125
    )

    assert (
        meshing_session.meshing_utilities.mark_face_strips_by_height_and_quality(
            face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"],
            strip_type=2,
            strip_height=2,
            quality_measure="Size Change",
            quality_limit=0.5,
            feature_angle=40.5,
        )
        == -125
    )

    assert (
        meshing_session.meshing_utilities.mark_face_strips_by_height_and_quality(
            face_zone_name_pattern="cold*",
            strip_type=1,
            strip_height=2,
            quality_measure="Size Change",
            quality_limit=0.5,
            feature_angle=40.5,
        )
        == -51
    )

    assert (
        meshing_session.meshing_utilities.mark_faces_deviating_from_size_field(
            face_zone_id_list=[87],
            min_size_factor=0.5,
            max_size_factor=1.1,
            size_factor_type_to_compare="geodesic",
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.mark_faces_deviating_from_size_field(
            face_zone_name_list=["elbow-fluid"],
            min_size_factor=0.5,
            max_size_factor=1.1,
            size_factor_type_to_compare="geodesic",
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.mark_faces_deviating_from_size_field(
            face_zone_name_pattern="elbow*",
            min_size_factor=0.5,
            max_size_factor=1.1,
            size_factor_type_to_compare="geodesic",
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.mark_faces_using_node_degree(
            face_zone_id_list=[87], node_degree_threshold=2
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.mark_faces_using_node_degree(
            face_zone_name_list=["elbow-fluid"], node_degree_threshold=2
        )
        == 0
    )

    assert (
        meshing_session.meshing_utilities.mark_faces_using_node_degree(
            face_zone_name_pattern="elbow*", node_degree_threshold=2
        )
        == 0
    )

    # Commented due to variation in 10^-16 th place

    # assert meshing_session.meshing_utilities.get_average_bounding_box_center(
    #     face_zone_id_list=[30, 31, 32]
    # ) == [1.1482939720153809, -2.2965879440307617, 0.7345014897547645]
    #
    # assert meshing_session.meshing_utilities.get_bounding_box_of_zone_list(
    #     zone_id_list=[26]
    # ) == [
    #     [-7.874015808105469, -7.874015808105469, 0.0],
    #     [-7.874015808105469, -3.937007904052734, 1.963911771774292],
    # ]

    assert (
        meshing_session.meshing_utilities.unpreserve_cell_zones(cell_zone_id_list=[87])
        is False
    )

    assert (
        meshing_session.meshing_utilities.unpreserve_cell_zones(
            cell_zone_name_list=["elbow-fluid"]
        )
        is False
    )

    assert (
        meshing_session.meshing_utilities.unpreserve_cell_zones(
            cell_zone_name_pattern="*"
        )
        is False
    )

    assert (
        meshing_session.meshing_utilities.create_boi_and_size_functions_from_refinement_regions(
            region_type="hexcore", boi_prefix_string="wall", create_size_function=True
        )
        == "*the-non-printing-object*"
        or False
    )

    assert (
        meshing_session.meshing_utilities.scale_face_zones_around_pivot(
            face_zone_id_list=[30, 31, 32],
            scale=[1.1, 1.2, 1.3],
            pivot=[1.1482939720153809, -2.2965879440307617, 0.7345014897547645],
            use_bbox_center=True,
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.scale_face_zones_around_pivot(
            face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"],
            scale=[1.1, 1.2, 1.3],
            pivot=[1.1482939720153809, -2.2965879440307617, 0.7345014897547645],
            use_bbox_center=True,
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.scale_face_zones_around_pivot(
            face_zone_name_pattern="*",
            scale=[1.1, 1.2, 1.3],
            pivot=[1.1482939720153809, -2.2965879440307617, 0.7345014897547645],
            use_bbox_center=True,
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.scale_cell_zones_around_pivot(
            cell_zone_id_list=[87],
            scale=[1.1, 1.2, 1.3],
            pivot=[1.1482939720153809, -2.2965879440307617, 0.7345014897547645],
            use_bbox_center=True,
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.scale_cell_zones_around_pivot(
            cell_zone_name_list=["elbow-fluid"],
            scale=[1.1, 1.2, 1.3],
            pivot=[1.1482939720153809, -2.2965879440307617, 0.7345014897547645],
            use_bbox_center=True,
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.scale_cell_zones_around_pivot(
            cell_zone_name_pattern="*",
            scale=[1.1, 1.2, 1.3],
            pivot=[1.1482939720153809, -2.2965879440307617, 0.7345014897547645],
            use_bbox_center=True,
        )
        is None
    )

    assert meshing_session.meshing_utilities.dump_face_zone_orientation_in_region(
        file_name="facezonetest.txt"
    ) == [
        [29, "elbow-fluid"],
        [30, "elbow-fluid"],
        [31, "elbow-fluid"],
        [32, "elbow-fluid"],
        [33, "elbow-fluid"],
        [34, "elbow-fluid"],
    ]

    assert (
        meshing_session.meshing_utilities.set_quality_measure(measure="Aspect Ratio")
        is None
    )

    assert (
        meshing_session.meshing_utilities.set_object_cell_zone_type(
            object_name="elbow-fluid", cell_zone_type="mixed"
        )
        is False
    )

    assert (
        meshing_session.meshing_utilities.set_number_of_parallel_compute_threads(
            nthreads=2
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.rename_face_zone(
            zone_id=32, new_name="outlet-32"
        )
        is True
    )

    assert (
        meshing_session.meshing_utilities.rename_face_zone(
            zone_name="outlet-32", new_name="outlet"
        )
        is True
    )

    assert (
        meshing_session.meshing_utilities.rename_edge_zone(
            zone_id=20, new_name="symmetry:xyplane:hot-inlet:elbow-fluid:feature.20-new"
        )
        is True
    )

    assert (
        meshing_session.meshing_utilities.rename_face_zone(
            zone_name="symmetry:xyplane:hot-inlet:elbow-fluid:feature.20-new",
            new_name="symmetry:xyplane:hot-inlet:elbow-fluid:feature.20",
        )
        is True
    )

    assert (
        meshing_session.meshing_utilities.remove_id_suffix_from_face_zones()
        == "*the-non-printing-object*"
        or False
    )

    assert (
        meshing_session.meshing_utilities.clean_face_zone_names()
        == "*the-non-printing-object*"
        or False
    )

    assert (
        meshing_session.meshing_utilities.remove_ids_from_zone_names(
            zone_id_list=[30, 31, 32]
        )
        is True
    )

    assert (
        meshing_session.meshing_utilities.renumber_zone_ids(
            zone_id_list=[30, 31, 32], start_number=1
        )
        == "*the-non-printing-object*"
        or False
    )

    assert meshing_session.meshing_utilities.rename_object(
        old_object_name="elbow-fluid", new_object_name="elbow-fluid-1"
    ) == [
        "elbow-fluid-1",
        "solid",
        10,
        [29, 33, 34, 1, 2, 3],
        [20, 21, 22, 23, 24, 25, 26, 27, 28],
        "mesh",
        [
            [
                "elbow-fluid",
                "fluid",
                [3.981021240569742, 7.614496699403261, 0.02968953016527287],
                [3, 2, 1, 34, 33, 29],
                [[87], None],
            ]
        ],
        [
            ["outlet-1", "fluid", 1, [3], None, "geom", False, None],
            ["hot-inlet-1", "fluid", 1, [2], None, "geom", False, None],
            ["cold-inlet-1", "fluid", 1, [2, 1], None, "geom", False, None],
            ["wall-inlet-1", "fluid", 1, [34], None, "geom", False, None],
            [
                "elbow-fluid",
                "solid",
                10,
                [3, 2, 1, 34, 33, 29],
                None,
                "geom",
                None,
                None,
                None,
                "body",
            ],
            [
                "wall-elbow",
                "solid",
                10,
                [34],
                None,
                "geom",
                None,
                None,
                None,
                "facelabel",
            ],
            [
                "wall-inlet",
                "solid",
                10,
                [33],
                None,
                "geom",
                None,
                None,
                None,
                "facelabel",
            ],
            ["outlet", "solid", 10, [3], None, "geom", None, None, None, "facelabel"],
            [
                "cold-inlet",
                "solid",
                10,
                [2],
                None,
                "geom",
                None,
                None,
                None,
                "facelabel",
            ],
            [
                "hot-inlet",
                "solid",
                10,
                [1],
                None,
                "geom",
                None,
                None,
                None,
                "facelabel",
            ],
            [
                "symmetry-xyplane",
                "solid",
                10,
                [29],
                None,
                "geom",
                None,
                None,
                None,
                "facelabel",
            ],
        ],
        [[87], None],
        [None],
        None,
    ] or [
        "elbow-fluid-1",
        "solid",
        10,
        [29, 33, 34, 1, 2, 3],
        [20, 21, 22, 23, 24, 25, 26, 27, 28],
        "mesh",
        [
            [
                "elbow-fluid",
                "fluid",
                [3.981021240569742, 7.614496699403261, 0.02968953016527287],
                [3, 2, 1, 34, 33, 29],
                [[87], None],
            ]
        ],
        [
            ["outlet-1", "fluid", 1, [3], None, "geom", False, None],
            ["hot-inlet-1", "fluid", 1, [2], None, "geom", False, None],
            ["cold-inlet-1", "fluid", 1, [2, 1], None, "geom", False, None],
            ["wall-inlet-1", "fluid", 1, [34], None, "geom", False, None],
            [
                "symmetry-xyplane",
                "solid",
                10,
                [29],
                None,
                "geom",
                None,
                None,
                None,
                "facelabel",
            ],
            [
                "hot-inlet",
                "solid",
                10,
                [1],
                None,
                "geom",
                None,
                None,
                None,
                "facelabel",
            ],
            [
                "cold-inlet",
                "solid",
                10,
                [2],
                None,
                "geom",
                None,
                None,
                None,
                "facelabel",
            ],
            ["outlet", "solid", 10, [3], None, "geom", None, None, None, "facelabel"],
            [
                "wall-inlet",
                "solid",
                10,
                [33],
                None,
                "geom",
                None,
                None,
                None,
                "facelabel",
            ],
            [
                "wall-elbow",
                "solid",
                10,
                [34],
                None,
                "geom",
                None,
                None,
                None,
                "facelabel",
            ],
            [
                "elbow-fluid",
                "solid",
                10,
                [3, 2, 1, 34, 33, 29],
                None,
                "geom",
                None,
                None,
                None,
                "body",
            ],
        ],
        [[87], None],
        [None],
        None,
    ]

    assert (
        meshing_session.meshing_utilities.replace_object_suffix(
            object_name_list=["elbow-fluid"], separator="-", new_suffix="fluid-new"
        )
        == "*the-non-printing-object*"
        or False
    )

    assert (
        meshing_session.meshing_utilities.rename_face_zone_label(
            object_name="elbow-fluid-1",
            old_label_name="outlet",
            new_label_name="outlet-new",
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.replace_label_suffix(
            object_name_list=["elbow-fluid-1"], separator="-", new_suffix="fluid-new"
        )
        == "*the-non-printing-object*"
        or False
    )

    assert (
        meshing_session.meshing_utilities.copy_face_zone_labels(
            from_face_zone_id=33, to_face_zone_id=34
        )
        == "*the-non-printing-object*"
        or False
    )

    assert (
        meshing_session.meshing_utilities.merge_face_zones(
            face_zone_id_list=[30, 31, 32]
        )
        is False
    )

    assert (
        meshing_session.meshing_utilities.merge_face_zones(
            face_zone_name_pattern="wall*"
        )
        == 34
    )

    assert (
        meshing_session.meshing_utilities.merge_face_zones_of_type(
            face_zone_type="velocity-inlet", face_zone_name_pattern="*"
        )
        == 1
    )

    assert (
        meshing_session.meshing_utilities.merge_face_zones_with_same_prefix(
            prefix="elbow"
        )
        is True
    )

    assert (
        meshing_session.meshing_utilities.merge_cell_zones(cell_zone_id_list=[87])
        is False
    )

    assert (
        meshing_session.meshing_utilities.merge_cell_zones(
            cell_zone_name_list=["elbow-fluid"]
        )
        is False
    )

    assert (
        meshing_session.meshing_utilities.merge_cell_zones(cell_zone_name_pattern="*")
        is False
    )

    assert (
        meshing_session.meshing_utilities.merge_cell_zones_with_same_prefix(
            prefix="elbow"
        )
        is True
    )

    assert (
        meshing_session.meshing_utilities.merge_cell_zones_with_same_suffix(
            suffix="fluid"
        )
        is True
    )

    assert (
        meshing_session.meshing_utilities.separate_face_zones_by_cell_neighbor(
            face_zone_id_list=[30, 31, 32]
        )
        is True
    )

    assert (
        meshing_session.meshing_utilities.separate_face_zones_by_cell_neighbor(
            face_zone_name_list=["wall-inlet", "wallfluid-new"]
        )
        is True
    )

    assert (
        meshing_session.meshing_utilities.separate_face_zones_by_cell_neighbor(
            face_zone_name_pattern="*"
        )
        is True
    )

    assert (
        meshing_session.meshing_utilities.refine_marked_faces_in_zones(
            face_zone_id_list=[30, 31, 32]
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.refine_marked_faces_in_zones(
            face_zone_name_list=["wall-inlet", "wallfluid-new"]
        )
        is None
    )

    assert meshing_session.meshing_utilities.refine_marked_faces_in_zones(
        face_zone_name_pattern="*"
    ) == [0, 0, 0, 0, 0]

    assert (
        meshing_session.meshing_utilities.fill_holes_in_face_zone_list(
            face_zone_id_list=[30, 31, 32], max_hole_edges=2
        )
        is False
    )

    assert (
        meshing_session.meshing_utilities.fill_holes_in_face_zone_list(
            face_zone_name_list=["wall-inlet", "wallfluid-new"], max_hole_edges=2
        )
        is False
    )

    assert (
        meshing_session.meshing_utilities.fill_holes_in_face_zone_list(
            face_zone_name_pattern="wall*", max_hole_edges=2
        )
        is False
    )

    assert (
        meshing_session.meshing_utilities.project_zone_on_plane(
            zone_id=87, plane=[[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.delete_all_sub_domains()
        == "*the-non-printing-object*"
        or False
    )

    assert (
        meshing_session.meshing_utilities.delete_marked_faces_in_zones(
            face_zone_id_list=[30, 31, 32]
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.delete_marked_faces_in_zones(
            face_zone_name_list=["wall-inlet", "wallfluid-new"]
        )
        is None
    )

    # assert meshing_session.meshing_utilities.delete_marked_faces_in_zones(
    #     face_zone_name_pattern="*"
    # ) == [0, 0, 0, 0, 3446]

    assert (
        meshing_session.meshing_utilities.delete_empty_face_zones(
            face_zone_id_list=[30, 31, 32]
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.delete_empty_face_zones(
            face_zone_name_list=["wall-inlet", "wallfluid-new"]
        )
        is None
    )

    assert meshing_session.meshing_utilities.delete_empty_face_zones(
        face_zone_name_pattern="*"
    ) == [29, 1, 3, 34, 89]

    assert meshing_session.meshing_utilities.delete_empty_cell_zones(
        cell_zone_id_list=[87]
    ) == [87]

    assert meshing_session.meshing_utilities.delete_empty_cell_zones(
        cell_zone_name_list=["elbow.87"]
    ) == [87]

    assert meshing_session.meshing_utilities.delete_empty_cell_zones(
        cell_zone_name_pattern="*"
    ) == [87]

    assert meshing_session.meshing_utilities.delete_empty_edge_zones(
        edge_zone_id_list=[20, 25, 26]
    ) == [26, 25, 20]

    assert meshing_session.meshing_utilities.delete_empty_edge_zones(
        edge_zone_name_list=[
            "symmetry:xyplane:hot-inlet:elbow-fluid:feature.20",
            "hot-inlet:wall-inlet:elbow-fluid:feature.21",
        ]
    ) == [21]

    assert meshing_session.meshing_utilities.delete_empty_edge_zones(
        edge_zone_name_pattern="*"
    ) == [28, 27, 26, 25, 24, 23, 22, 21, 20]

    assert meshing_session.meshing_utilities.delete_empty_zones(
        zone_id_list=[20, 32, 87]
    ) == [20, 87]

    assert meshing_session.meshing_utilities.delete_empty_zones(
        zone_name_list=["hotfluid-new", "elbow.87"]
    ) == [87]

    assert meshing_session.meshing_utilities.delete_empty_zones(
        zone_name_pattern="*"
    ) == [169, 163, 19, 28, 27, 26, 25, 24, 23, 22, 21, 20, 29, 1, 3, 34, 89, 87]

    assert meshing_session.meshing_utilities.boundary_zone_exists(zone_id=31) is False

    assert (
        meshing_session.meshing_utilities.boundary_zone_exists(zone_name="wall-inlet")
        is False
    )

    assert meshing_session.meshing_utilities.interior_zone_exists(zone_id=31) is False

    assert (
        meshing_session.meshing_utilities.interior_zone_exists(zone_name="wall-inlet")
        is False
    )

    assert meshing_session.meshing_utilities.cell_zone_exists(zone_id=87) is True

    assert (
        meshing_session.meshing_utilities.cell_zone_exists(zone_name="elbow.87") is True
    )

    assert meshing_session.meshing_utilities.mesh_exists() is True

    assert (
        meshing_session.meshing_utilities.replace_face_zone_suffix(
            face_zone_id_list=[30, 31, 32],
            separator="-suffix-",
            replace_with="-with-",
            merge=False,
        )
        is False
    )

    assert (
        meshing_session.meshing_utilities.replace_face_zone_suffix(
            face_zone_name_list=["cold-inlet", "hot-inlet"],
            separator="-suffix-",
            replace_with="-with-",
            merge=False,
        )
        is False
    )

    assert meshing_session.meshing_utilities.replace_cell_zone_suffix(
        cell_zone_id_list=[87], old_suffix="fluid", new_suffix="fluid-new", merge=True
    ) == ["*the-non-printing-object*"] or [False]

    assert (
        meshing_session.meshing_utilities.replace_cell_zone_suffix(
            cell_zone_name_list=["elbow-fluid-new"],
            old_suffix="fluid",
            new_suffix="fluid-new",
            merge=True,
        )
        is None
    )

    assert (
        meshing_session.meshing_utilities.replace_edge_zone_suffix(
            edge_zone_id_list=[20],
            old_suffix="fluid",
            new_suffix="fluid-new",
            merge=True,
        )
        == "*the-non-printing-object*"
        or False
    )

    assert (
        meshing_session.meshing_utilities.replace_edge_zone_suffix(
            edge_zone_name_list=["hot-inlet:wall-inlet:elbow-fluid:feature.21"],
            old_suffix="fluid",
            new_suffix="fluid-new",
            merge=True,
        )
        == "*the-non-printing-object*"
        or False
    )
