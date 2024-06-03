import logging

import ansys.fluent.core as pyfluent


def test_set_console_logging_level(caplog):
    settings_logger = logging.getLogger("pyfluent.settings_api")
    settings_logger.warning("ABC")
    assert len(caplog.records) == 1
    caplog.clear()
    pyfluent.set_console_logging_level("ERROR")
    settings_logger.warning("ABC")
    assert len(caplog.records) == 0
