from util import create_datamodel_root_in_server

rules_str = (
    "RULES:\n"
    "  STRING: X\n"
    "    allowedValues = yes, no\n"
    "    logicalMapping = True, False\n"
    "  END\n"
    "  STRING: Y\n"
    '    allowedValues = \\"1\\", \\"2\\", \\"3\\"\n'
    '    default = \\"2\\"\n'
    "    isNumerical = True\n"
    "  END\n"
    "  INTEGER: Z\n"
    "  END\n"
    "  SINGLETON: ROOT\n"
    "    members = A\n"
    "    commands = C, D\n"
    "    SINGLETON: A\n"
    "      members = X, Y, Z\n"
    "    END\n"
    "    COMMAND: C\n"
    "      arguments = X\n"
    "      functionName = CFunc\n"
    "    END\n"
    "    COMMAND: D\n"
    "      arguments = X\n"
    "      functionName = CFunc\n"
    "      APIName = dd\n"
    "    END\n"
    "  END\n"
    "END\n"
)

rules_str_caps = (
    "RULES:\n"
    "  STRING: X\n"
    "    allowedValues = Yes, No\n"
    "    default = No\n"
    "    logicalMapping = True, False\n"
    "  END\n"
    "  SINGLETON: ROOT\n"
    "    members = A\n"
    "    SINGLETON: A\n"
    "      members = X\n"
    "    END\n"
    "  END\n"
    "END\n"
)


def get_static_info_value(static_info, type_path):
    for p in type_path.removeprefix("/").split("/"):
        static_info = static_info[p]
    return static_info


def test_datamodel_api_bool_for_str_has_correct_type(
    datamodel_api_version_new, new_solver_session
):
    solver = new_solver_session
    create_datamodel_root_in_server(solver, rules_str)
    service = solver._se_service
    static_info = service.get_static_info("test")
    assert (
        get_static_info_value(static_info, "/singletons/A/parameters/X/type")
        == "Logical"
    )
    cmd_args = get_static_info_value(static_info, "/commands/C/commandinfo/args")
    arg0 = cmd_args[0]
    assert arg0["type"] == "Logical"
