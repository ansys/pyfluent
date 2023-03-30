from ansys.fluent.core import examples

import_filename = examples.download_file(
    "elbow.cas.h5", "pyfluent/examples/DOE-ML-Mixing-Elbow"
)


def test_meshing_queries(new_mesh_session):
    meshing_session = new_mesh_session
    meshing_session.tui.file.read_case(import_filename)

    assert meshing_session.meshing_queries.GetFaceZoneAtLocation(
        [1.4, 1.4, 1.4]
    ) == meshing_session.scheme_eval.scheme_eval(
        "(get-face-zone-at-location '(1.4 1.4 1.4))"
    )

    assert meshing_session.meshing_queries.GetZonesOfType(
        "velocity-inlet"
    ) == meshing_session.scheme_eval.scheme_eval("(get-zones-of-type 'velocity-inlet)")

    assert meshing_session.meshing_queries.GetZonesOfGroup(
        "inlet"
    ) == meshing_session.scheme_eval.scheme_eval("(get-zones-of-group 'inlet)")

    assert meshing_session.meshing_queries.GetFaceZonesOfFilter(
        "*"
    ) == meshing_session.scheme_eval.scheme_eval("(get-face-zones-of-filter '*)")

    assert meshing_session.meshing_queries.GetCellZonesOfFilter("*") == [3460]
    assert meshing_session.scheme_eval.scheme_eval("(get-cell-zones-of-filter '*)") == (
        3460,
    )

    assert meshing_session.meshing_queries.GetEdgeZonesOfFilter("*") == []
    assert (
        meshing_session.scheme_eval.scheme_eval("(get-edge-zones-of-filter '*)") == None
    )

    assert meshing_session.meshing_queries.GetNodeZonesOfFilter(
        "*"
    ) == meshing_session.scheme_eval.scheme_eval("(get-node-zones-of-filter '*)")

    assert meshing_session.meshing_queries.GetObjectsOfType("mesh") == ["elbow-fluid"]
    # assert meshing_session.scheme_eval.scheme_eval("(get-objects-of-type 'mesh)") == (elbow-fluid,)

    assert meshing_session.meshing_queries.GetFaceZoneIdListOfObject(
        "elbow-fluid"
    ) == meshing_session.scheme_eval.scheme_eval(
        "(tgapi-util-get-face-zone-id-list-of-object 'elbow-fluid)"
    )

    assert (
        meshing_session.meshing_queries.GetEdgeZoneIdListOfObject("elbow-fluid") == []
    )
    assert (
        meshing_session.scheme_eval.scheme_eval(
            "(tgapi-util-get-edge-zone-id-list-of-object 'elbow-fluid)"
        )
        == None
    )

    assert meshing_session.meshing_queries.GetCellZoneIdListOfObject("elbow-fluid") == [
        3460
    ]
    meshing_session.scheme_eval.scheme_eval(
        "(tgapi-util-get-cell-zone-id-list-of-object 'elbow-fluid)"
    ) == (3460,)

    assert (
        meshing_session.meshing_queries.GetFaceZonesSharedByRegionsOfType(
            "elbow-fluid", "fluid-fluid"
        )
        == []
    )
    assert (
        meshing_session.scheme_eval.scheme_eval(
            "(get-face-zones-shared-by-regions-of-type 'elbow-fluid 'fluid-fluid)"
        )
        == None
    )

    assert meshing_session.meshing_queries.GetFaceZonesOfRegions(
        "elbow-fluid", ["fluid"]
    ) == meshing_session.scheme_eval.scheme_eval(
        "(get-face-zones-of-regions 'elbow-fluid '(fluid))"
    )

    assert meshing_session.meshing_queries.GetFaceZonesOfLabels(
        "elbow-fluid", ["inlet", "outlet", "wall", "internal"]
    ) == [
        32
    ]  # noqa: E501
    assert meshing_session.scheme_eval.scheme_eval(
        "(get-face-zones-of-labels 'elbow-fluid '(inlet outlet wall internal))"
    ) == (32,)

    assert meshing_session.meshing_queries.TgapiUtilGetFaceZoneIdListOfLabels(
        "elbow-fluid", ["outlet"]
    ) == [32]
    assert meshing_session.scheme_eval.scheme_eval(
        "(tgapi-util-get-face-zone-id-list-of-labels 'elbow-fluid '(outlet))"
    ) == (32,)

    assert meshing_session.meshing_queries.GetFaceZonesOfObjects(
        ["elbow-fluid"]
    ) == meshing_session.scheme_eval.scheme_eval(
        "(get-face-zones-of-objects '(elbow-fluid))"
    )

    assert meshing_session.meshing_queries.GetEdgeZonesOfObjects(["elbow-fluid"]) == []
    assert (
        meshing_session.scheme_eval.scheme_eval(
            "(get-edge-zones-of-objects '(elbow-fluid))"
        )
        == None
    )

    assert meshing_session.meshing_queries.TgapiUtilGetFaceZoneIdListOfRegions(
        "elbow-fluid", ["fluid"]
    ) == meshing_session.scheme_eval.scheme_eval(
        "(tgapi-util-get-face-zone-id-list-of-regions 'elbow-fluid '(fluid))"
    )  # noqa: E501
