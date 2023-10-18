"""A module for controlling the writing of Fluent Python journals."""


class Journal:
    """Control the writing of Fluent Python journals."""

    def __init__(self, scheme_eval):
        """__init__ method of Journal class."""
        self.scheme_eval = scheme_eval

    def start(self, file_name: str):
        """Start writing a Fluent Python journal at the specified file_name."""
        self.scheme_eval.exec([f'(api-start-python-journal "{file_name}")'])

    def stop(self):
        """Stop writing the Fluent Python journal."""
        self.scheme_eval.exec([f"(api-stop-python-journal)"])
