import jedi


def test_settings_file_read_case():
    prefix = """import ansys.fluent.core as pyfluent
    solver = pyfluent.launch_fluent()
    """
    path = "solver.settings."
    filename = "example.py"
    line = 4
    script = jedi.Script(code=f"{prefix}\n{path}", path=filename)
    completions = script.complete(line=line, column=len(path))
    file = next((c for c in completions if c.name == "file"), None)
    assert file is not None
    assert file.name == "file"
    assert file.docstring() == "file(*args, **kwargs)"  # not correct

    path += "file."
    script = jedi.Script(code=f"{prefix}\n{path}", path=filename)
    completions = script.complete(line=line, column=len(path))
    read_case = next((c for c in completions if c.name == "read_case"), None)
    assert read_case is not None
    assert read_case.name == "read_case"
    assert (
        read_case.docstring()
        == "read_case(file_name: str, pdf_file_name: str)\n\n'read_case' command."
    )

    path += "read_case("
    script = jedi.Script(code=f"{prefix}\n{path}", path=filename)
    completions = script.complete(line=line, column=len(path))
    file_name = next((c for c in completions if c.name == "file_name="), None)
    assert file_name is not None
    assert file_name.name == "file_name="
    assert file_name.docstring() == ""  # not correct
