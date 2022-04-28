def check_report_definition_result(
    report_definitions, report_definition_name, expected_result
):
    assert (
        report_definitions.compute(report_defs=[report_definition_name])[
            report_definition_name
        ][0]
        == expected_result
    )
