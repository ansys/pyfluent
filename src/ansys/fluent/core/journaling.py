"""A module for controlling the writing of Fluent Python journals."""


class Journal:
    """Control the writig of Fluent Python journals."""

    def __init__(self, scheme_eval):
        self.scheme_eval = scheme_eval

    def start(self, file_path: str):
        """Start writing a Fluent Python journal at the specified file_path."""
        self.scheme_eval.exec([f'(api-start-python-journal "{file_path}")'])

    def stop(self):
        """Stop writing the Fluent Python journal."""
        self.scheme_eval.exec([f"(api-stop-python-journal)"])
