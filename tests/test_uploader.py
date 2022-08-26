import pytest

from ansys.fluent.core import launch_fluent


def test_base_session():
    base_session = launch_fluent(cleanup_on_exit=False, mode="meshing")
    with pytest.raises(Exception) as e_info:
        base_session._upload(
            "D:/PythonPractise/RealWithUnits/ConversionTable.py", "testNow.py"
        )
        base_session._download("testNow.py", "D:/PythonPractise/RealWithUnits")
    base_session.exit()


def test_session():
    session = launch_fluent(cleanup_on_exit=False, meshing_mode=True)
    with pytest.raises(Exception) as e_info:
        session._upload(
            "D:/PythonPractise/RealWithUnits/ConversionTable.py", "testNow.py"
        )
        session._download("testNow.py", "D:/PythonPractise/RealWithUnits")
    session.exit()
