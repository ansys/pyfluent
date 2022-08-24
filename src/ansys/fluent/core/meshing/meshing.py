class Meshing:
    def __init__(self, session_execute_tui, meshing, tui, fluent_connection):
        self.execute_tui = session_execute_tui
        self._meshing = meshing
        self._tui = tui
        self._fluent_connection = fluent_connection

    def switch_to_solver(self):
        """Switch to solver session."""
        from ansys.fluent.core.session_solver import Solver

        self._tui.switch_to_solution_mode("yes")
        solver_session = Solver(fluent_connection=self._fluent_connection)
        return solver_session

    def __getattr__(self, attr):
        return getattr(self._meshing, attr)

    def __dir__(self):
        return sorted(
            set(list(self.__dict__.keys()) + dir(type(self)) + dir(self._meshing))
        )

    def __call__(self):
        return self._meshing()
