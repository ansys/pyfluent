"""Module for maintaining journal."""


class Journal:
    """Manages journal streaming."""

    def __init__(self, scheme_eval):
        self.scheme_eval = scheme_eval

    def start(self, file_path: str):
        """Starts writing a journal to the file_path."""
        self.scheme_eval.exec([f'(api-start-python-journal "{file_path}")'])

    def stop(self):
        """Stops writing the journal."""
        self.scheme_eval.exec([f"(api-stop-python-journal)"])
