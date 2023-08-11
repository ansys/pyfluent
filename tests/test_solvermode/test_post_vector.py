import pytest


@pytest.mark.nightly
@pytest.mark.setup
@pytest.mark.fluent_version("latest")
def test_post_elbow(load_mixing_elbow_case_dat):
    pyflu = load_mixing_elbow_case_dat
    pyflu.results.graphics.vector["velocity_vector_symmetry"] = {}
    pyflu.results.graphics.vector["velocity_vector_symmetry"].field = "temperature"
    pyflu.results.graphics.vector["velocity_vector_symmetry"].surfaces_list = [
        "symmetry-xyplane",
    ]
    pyflu.results.graphics.vector["velocity_vector_symmetry"].scale.scale_f = 4
    pyflu.results.graphics.vector["velocity_vector_symmetry"].style = "arrow"
    vel_vector = pyflu.results.graphics.vector["velocity_vector_symmetry"]()
    assert vel_vector.get("name") == "velocity_vector_symmetry"
    assert vel_vector.get("field") == "temperature"
    assert vel_vector.get("surfaces_list") == ["symmetry-xyplane"]
    assert vel_vector.get("scale") == {"auto_scale": True, "scale_f": 4.0}
    assert vel_vector.get("style") == "arrow"
