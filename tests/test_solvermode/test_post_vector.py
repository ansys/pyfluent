import pytest


@pytest.mark.settings_only
@pytest.mark.fluent_version("latest")
def test_post_elbow(mixing_elbow_settings_session):
    mixing_elbow_settings_session.results.graphics.vector[
        "velocity_vector_symmetry"
    ] = {}
    vector_graphics = mixing_elbow_settings_session.results.graphics.vector[
        "velocity_vector_symmetry"
    ]
    vector_graphics.field = "temperature"
    vector_graphics.surfaces_list = ["symmetry-xyplane"]
    vector_graphics.scale.scale_f = 4
    vector_graphics.style = "arrow"
    vel_vector = vector_graphics()
    assert vel_vector.get("name") == "velocity_vector_symmetry"
    assert vel_vector.get("field") == "temperature"
    assert vel_vector.get("surfaces_list") == ["symmetry-xyplane"]
    assert vel_vector.get("scale") == {"auto_scale": True, "scale_f": 4.0}
    assert vel_vector.get("style") == "arrow"
