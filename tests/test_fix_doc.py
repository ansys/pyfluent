from ansys.fluent.core.utils.fix_doc import fix_settings_doc


def test_fix_definition_list_in_settings_doc():
    old_doc = """Menu to define the rotor pitch and flapping angles.
 - blade-pitch-collective    : ,
 - blade-pitch-cyclic-sin    : ,
 - blade-pitch-cyclic-cos    : ,
For more details please consult the help option of the corresponding menu or TUI command."""
    new_doc = fix_settings_doc(old_doc)
    assert (
        new_doc
        == """Menu to define the rotor pitch and flapping angles.

 - blade-pitch-collective    : ,
 - blade-pitch-cyclic-sin    : ,
 - blade-pitch-cyclic-cos    : ,

For more details please consult the help option of the corresponding menu or TUI command."""
    )


def test_fix_wildcards_in_settings_doc():
    old_doc = """Read boundary profile data (*.prof, *.csv). Default is *.prof."""
    new_doc = fix_settings_doc(old_doc)
    assert (
        new_doc
        == r"""Read boundary profile data (\*.prof, \*.csv). Default is \*.prof."""
    )
