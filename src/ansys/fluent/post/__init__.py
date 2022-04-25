"""Python post processing integrations for the Fluent solver."""
import platform
import struct
import sys

import pkg_resources

required_libraries = {
    "vtk": "9.1.0",
    "pyvista": "0.33.2",
    "pyvistaqt": "0.7.0",
    "pyside6": "6.2.3",
    "matplotlib": "3.5.1",
}


def _get_vtk_install_cmd(reinstall=False):
    is64 = struct.calcsize("P") * 8 == 64
    if sys.version_info.minor == 10 and is64:
        if platform.system().lower() == "linux":
            return f"  Please {'reinstall' if reinstall else 'install'} vtk with `pip install {'-I' if reinstall else ''} https://github.com/pyvista/pyvista-wheels/raw/main/vtk-9.1.0.dev0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl`"  # noqa: E501

        elif platform.system().lower() == "windows":
            return f"  Please {'reinstall' if reinstall else 'install'} vtk with `pip install {'-I' if reinstall else ''} https://github.com/pyvista/pyvista-wheels/raw/main/vtk-9.1.0.dev0-cp310-cp310-win_amd64.whl`"  # noqa: E501
    else:
        return (
            f"  Please {'reinstall' if reinstall else 'install'} "
            f"vtk with `pip install vtk=={required_libraries[lib]}`."
        )


def _update_vtk_version():
    is64 = struct.calcsize("P") * 8 == 64
    if sys.version_info.minor in (9, 10) and is64:
        required_libraries.update({"vtk": "9.1.0.dev0"})


_update_vtk_version()
installed = {pkg.key for pkg in pkg_resources.working_set}
installed_libraries = [
    lib for lib, version in required_libraries.items() if lib in installed
]
missing_libraries = required_libraries.keys() - installed
import_errors = []
if missing_libraries:
    import_errors.append(
        (
            f"Required libraries {missing_libraries} "
            "are missing to use this feature."
        )
    )
    for lib in missing_libraries:
        import_errors.append(
            (
                f"  Please install {lib} with "
                f"`pip install {lib}=={required_libraries[lib]}`."
                if lib != "vtk"
                else _get_vtk_install_cmd()
            )
        )
if installed_libraries:
    versions_mismatched_message = False
    for lib in installed_libraries:
        required_version = required_libraries[lib]
        installed_version = pkg_resources.get_distribution(lib).version
        if pkg_resources.parse_version(
            installed_version
        ) < pkg_resources.parse_version(required_version):
            if not versions_mismatched_message:
                import_errors.append(
                    (
                        f"Required libraries version is incompatible "
                        "to use this feature."
                    )
                )
                versions_mismatched_message = True
            import_errors.append(
                (
                    f"  Please re-install {lib} with "
                    f"`pip install -I {lib}=={required_libraries[lib]}`."
                    if lib != "vtk"
                    else _get_vtk_install_cmd(True)
                )
            )

if import_errors:
    raise ImportError("\n".join(import_errors))
from ansys.fluent.post._config import get_config, set_config  # noqa: F401
