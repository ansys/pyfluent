"""A module for controlling the writing of Fluent Python journals."""


class Journal:
    """Control the writing of Fluent Python journals."""

    def __init__(self, app_utilities):
        """__init__ method of Journal class."""
        self._app_utilities = app_utilities

    def start(self, file_name: str):
        """Start writing a Fluent Python journal at the specified file_name."""
        self._app_utilities.start_python_journal(journal_name=file_name)

    def stop(self):
        """Stop writing the Fluent Python journal."""
        self._app_utilities.stop_python_journal()
