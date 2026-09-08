"""Generate API reference pages from the ``ansys.fluent.core`` package tree."""

from pathlib import Path
import shutil

from ansys.fluent.core import FluentVersion

DOC_DIR = Path(__file__).resolve().parent
SOURCE_PACKAGE = DOC_DIR.parent / "src" / "ansys" / "fluent" / "core"
API_DIR = DOC_DIR / "source" / "api"
PACKAGE_NAME = "ansys.fluent.core"
SKIP_DIRECTORIES = {
    "__pycache__",
    "api_tree",
    "docs",
    "codegen",
    "examples",
    "expressions",
    "generated",
    "rest",
    "ui",
}
SKIP_FILES = {
    "settings_builtin_bases",
    "settings_builtin_data",
    "settings_external",
}
ADDITIONAL_DOCUMENTATION = {
    "ansys.fluent.core.meshing": (
        "Meshing workflows use the underlying meshing workflow object. See the "
        ":ref:`meshing workflow API <ref_meshing_datamodel_meshing_workflow>` "
        "for details.\n"
    ),
    "ansys.fluent.core.solver": (
        "Solver expose an underlying hierarchical settings object. See "
        "the :ref:`settings API <ref_root>` for details.\n"
    ),
}


def _write_common_options(rst_file):
    rst_file.write(
        "    :members:\n"
        "    :show-inheritance:\n"
        "    :undoc-members:\n"
        "    :exclude-members: __weakref__, __dict__\n"
        "    :special-members: __init__, __new__\n"
        "    :autosummary:\n"
    )


def _write_api_page(rst_file, title, directive, module_name):
    rst_file.write(f".. _ref_{module_name.replace('.', '_')}:\n\n")
    rst_file.write(f"{title}\n")
    rst_file.write(f"{'=' * len(title)}\n\n")
    rst_file.write(f".. {directive}:: {module_name}\n")
    _write_common_options(rst_file)


def _write_additional_documentation(rst_file, module_name):
    additional_documentation = ADDITIONAL_DOCUMENTATION.get(module_name)
    if additional_documentation:
        rst_file.write(f"\n{additional_documentation}\n")


def _module_name(source_path):
    relative_path = source_path.relative_to(SOURCE_PACKAGE).with_suffix("")
    return ".".join((PACKAGE_NAME, *relative_path.parts))


def _package_name(source_path):
    relative_path = source_path.relative_to(SOURCE_PACKAGE)
    if not relative_path.parts:
        return PACKAGE_NAME
    return ".".join((PACKAGE_NAME, *relative_path.parts))


def _documented_children(source_path):
    children = []
    for child in source_path.iterdir():
        if (
            child.name in SKIP_DIRECTORIES
            or child.name.startswith("_")
            or child.stem in SKIP_FILES
        ):
            continue
        if child.is_dir() or (child.suffix == ".py" and child.name != "__init__.py"):
            children.append(child)
    return sorted(children, key=lambda path: (not path.is_dir(), path.name))


def _write_module_page(source_path):
    module_name = _module_name(source_path)
    output_path = API_DIR / source_path.relative_to(SOURCE_PACKAGE).with_suffix(".rst")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf8") as rst_file:
        _write_api_page(rst_file, source_path.stem, "automodule", module_name)


def _write_package_index(source_path):
    package_name = _package_name(source_path)
    relative_path = source_path.relative_to(SOURCE_PACKAGE)
    output_directory = API_DIR / relative_path
    output_directory.mkdir(parents=True, exist_ok=True)
    index_name = (
        f"{source_path.name}_contents.rst"
        if relative_path.parts
        else "api_contents.rst"
    )
    output_path = output_directory / index_name
    title = source_path.name if relative_path.parts else PACKAGE_NAME

    with output_path.open("w", encoding="utf8") as rst_file:
        _write_api_page(rst_file, title, "automodule", package_name)
        _write_additional_documentation(rst_file, package_name)
        rst_file.write("\n.. toctree::\n")
        rst_file.write("    :maxdepth: 2\n")
        rst_file.write("    :hidden:\n\n")

        for child in _documented_children(source_path):
            if child.is_dir():
                rst_file.write(f"    {child.name}/{child.name}_contents\n")
            else:
                rst_file.write(f"    {child.stem}\n")

        rst_file.write("\n")


def _generate_package_tree(source_path):
    if source_path != SOURCE_PACKAGE:
        _write_package_index(source_path)
    for child in _documented_children(source_path):
        if child.is_dir():
            _generate_package_tree(child)
        else:
            _write_module_page(child)


def _write_api_index():
    version = FluentVersion.current_release()
    output_path = API_DIR / "api_contents.rst"
    with output_path.open("w", encoding="utf8") as rst_file:
        rst_file.write(
            ".. _ref_api:\n\n"
            "API reference\n"
            "=============\n\n"
            f"This API reference corresponds to {version}. PyFluent maintains strong "
            "backward compatibility guarantees, so scripts targeting older Ansys "
            "versions are expected to work without modification.\n\n"
            "This is PyFluent's class and function reference. Please refer to the "
            ":ref:`ref_user_guide` for full guidelines on their use.\n\n"
            "All public APIs for PyFluent are listed below.\n\n"
            ".. toctree::\n"
            "    :maxdepth: 2\n"
            "    :hidden:\n\n"
        )
        for child in _documented_children(SOURCE_PACKAGE):
            if child.is_dir():
                rst_file.write(f"    {child.name}/{child.name}_contents\n")
            else:
                rst_file.write(f"    {child.stem}\n")


def generate():
    """Generate the API RST tree from the Python source tree.

    Raises:
        FileNotFoundError: If the source Python package directory does not exist.
    """
    if not SOURCE_PACKAGE.is_dir():
        raise FileNotFoundError(f"Python package not found: {SOURCE_PACKAGE}")

    if API_DIR.exists():
        shutil.rmtree(API_DIR)
    API_DIR.mkdir(parents=True)
    _write_api_index()
    _generate_package_tree(SOURCE_PACKAGE)


if __name__ == "__main__":
    generate()
