"""A module for controlling the writing of Fluent Python journals."""


class PythonJournalNotSupported(RuntimeError):
    """Raised when Python journal is unsupported."""

    def __init__(self):
        """Initialize PythonJournalNotSupported."""
        super().__init__(
            "Python journaling is available in Fluent version 2023 R1 or later."
        )


class Journal:
    """Control the writing of Fluent Python journals."""

    def __init__(self, app_utilities):
        """__init__ method of Journal class."""
        self._app_utilities = app_utilities

    def _check_python_journaling_support(self):
        if self._app_utilities.get_product_version() == "22.2.0":
            raise PythonJournalNotSupported()

    def start(self, file_name: str):
        """Start writing a Fluent Python journal at the specified file_name."""
        self._check_python_journaling_support()
        self._app_utilities.start_python_journal(journal_name=file_name)

    def stop(self):
        """Stop writing the Fluent Python journal."""
        self._check_python_journaling_support()
        self._app_utilities.stop_python_journal()
