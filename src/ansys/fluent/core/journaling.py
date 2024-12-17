"""A module for controlling the writing of Fluent Python journals."""

import ansys.fluent.core as pyfluent


class Journal:
    """Control the writing of Fluent Python journals."""

    def __init__(self, scheme_eval, app_utilities):
        """__init__ method of Journal class."""
        self.scheme_eval = scheme_eval
        self._app_utilities = app_utilities

    def start(self, file_name: str):
        """Start writing a Fluent Python journal at the specified file_name."""
        if (
            pyfluent.FluentVersion(self.scheme_eval.version)
            < pyfluent.FluentVersion.v252
        ):
            self.scheme_eval.exec([f'(api-start-python-journal "{file_name}")'])
        else:
            self._app_utilities.start_python_journal(journal_name=file_name)

    def stop(self):
        """Stop writing the Fluent Python journal."""
        if (
            pyfluent.FluentVersion(self.scheme_eval.version)
            < pyfluent.FluentVersion.v252
        ):
            self.scheme_eval.exec(["(api-stop-python-journal)"])
        else:
            self._app_utilities.stop_python_journal()
