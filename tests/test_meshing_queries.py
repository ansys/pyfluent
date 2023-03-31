from ansys.fluent.core import examples

import_filename = examples.download_file(
    "elbow.cas.h5", "pyfluent/examples/DOE-ML-Mixing-Elbow"
)


def test_meshing_queries(new_mesh_session):
    meshing_session = new_mesh_session
    meshing_session.tui.file.read_case(import_filename)

    assert meshing_session.meshing_queries.GetFaceZoneAtLocation([1.4, 1.4, 1.4]) == 34

    assert meshing_session.meshing_queries.GetZonesOfType("velocity-inlet") == [30, 31]

    assert meshing_session.meshing_queries.GetZonesOfGroup("inlet") == [31, 30]

    assert meshing_session.meshing_queries.GetFaceZonesOfFilter("*") == [
        3462,
        34,
        33,
        32,
        31,
        30,
        29,
    ]

    assert meshing_session.meshing_queries.GetCellZonesOfFilter("*") == [3460]

    assert meshing_session.meshing_queries.GetEdgeZonesOfFilter("*") == []

    assert meshing_session.meshing_queries.GetNodeZonesOfFilter("*") == [3625, 3624]

    assert meshing_session.meshing_queries.GetObjectsOfType("mesh") == ["elbow-fluid"]

    assert meshing_session.meshing_queries.GetFaceZoneIdListOfObject("elbow-fluid") == [
        29,
        30,
        31,
        32,
        33,
        34,
    ]

    assert (
        meshing_session.meshing_queries.GetEdgeZoneIdListOfObject("elbow-fluid") == []
    )

    assert meshing_session.meshing_queries.GetCellZoneIdListOfObject("elbow-fluid") == [
        3460
    ]

    assert (
        meshing_session.meshing_queries.GetFaceZonesSharedByRegionsOfType(
            "elbow-fluid", "fluid-fluid"
        )
        == []
    )

    assert meshing_session.meshing_queries.GetFaceZonesOfRegions(
        "elbow-fluid", ["fluid"]
    ) == [34, 33, 32, 31, 30, 29]

    assert meshing_session.meshing_queries.GetFaceZonesOfLabels(
        "elbow-fluid", ["inlet", "outlet", "wall", "internal"]
    ) == [
        32
    ]  # noqa: E501

    assert meshing_session.meshing_queries.GetFaceZoneIdListOfLabels(
        "elbow-fluid", ["outlet"]
    ) == [32]

    assert meshing_session.meshing_queries.GetFaceZonesOfObjects(["elbow-fluid"]) == [
        29,
        30,
        31,
        32,
        33,
        34,
    ]

    assert meshing_session.meshing_queries.GetEdgeZonesOfObjects(["elbow-fluid"]) == []

    assert meshing_session.meshing_queries.GetFaceZoneIdListOfRegions(
        "elbow-fluid", ["fluid"]
    ) == [
        34,
        33,
        32,
        31,
        30,
        29,
    ]  # noqa: E501
