import os

MODULE_NAME_ALIAS = "pyfluent"
JOURNAL_FILENAME = None

def start_journal(filename: str):
    global JOURNAL_FILENAME
    JOURNAL_FILENAME = filename
    if os.path.exists(filename):
        os.remove(filename)
    with open(JOURNAL_FILENAME, "w", encoding="utf8") as f:
        f.write(f"import {__name__} as {MODULE_NAME_ALIAS}\n")


def stop_journal():
    global JOURNAL_FILENAME
    JOURNAL_FILENAME = None


def read_journal(filename: str):
    exec(open(filename, encoding="utf8").read())


class PyMenuJournaler:
    def __init__(self, path=None):
        self.pypath = ""
        if not path:
            return
        for comp in path:
            if self.pypath:
                self.pypath += "."
            if comp[1]:
                self.pypath += f"{comp[0]}[{repr(comp[1])}]"
            else:
                self.pypath += comp[0]

    def __write_to_file(self, code):
        if not JOURNAL_FILENAME:
            return
        with open(JOURNAL_FILENAME, "a", encoding="utf8") as f:
            f.write(code)

    def journal_set_state(self, state):
        self.__write_to_file(
            f"{MODULE_NAME_ALIAS}.{self.pypath} = {repr(state)}\n"
        )

    def journal_rename(self, new_name):
        self.__write_to_file(
            f"{MODULE_NAME_ALIAS}.{self.pypath}.rename({repr(new_name)})\n"
        )

    def journal_delete(self, child_name):
        self.__write_to_file(
            f"del {MODULE_NAME_ALIAS}.{self.pypath}[{repr(child_name)}]\n"
        )

    def journal_execute(self, args=None, kwargs=None):
        self.__write_to_file(f"{MODULE_NAME_ALIAS}.{self.pypath}(")
        first = True
        if args is not None:
            for arg in args:
                if not first:
                    self.__write_to_file(", ")
                else:
                    first = False
                self.__write_to_file(repr(arg))
        if kwargs is not None:
            for k, v in kwargs.items():
                if not first:
                    self.__write_to_file(", ")
                else:
                    first = False
                self.__write_to_file(f"{k}={repr(v)}")
        self.__write_to_file(")\n")

    def journal_global_fn_call(self, func_name, args=None, kwargs=None):
        self.__write_to_file(f"{MODULE_NAME_ALIAS}.{func_name}(")
        first = True
        if args is not None:
            for arg in args:
                if not first:
                    self.__write_to_file(", ")
                else:
                    first = False
                self.__write_to_file(repr(arg))
        if kwargs is not None:
            for k, v in kwargs.items():
                if not first:
                    self.__write_to_file(", ")
                else:
                    first = False
                self.__write_to_file(f"{k}={repr(v)}")
        self.__write_to_file(")\n")
