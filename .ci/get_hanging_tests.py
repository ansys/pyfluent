"""A script to print the name of the hanging test by parsing the GitHub logs file."""

import argparse


def strip_before_tests(input_string):
    """
    Strips everything before the 'tests/' in the given string.
    Parameters
    ----------
    input_string: str
        The original string to process.
    Returns
    -------
        The modified string.
    """
    index = input_string.find("tests/")
    if index != -1:
        return input_string[index:]


def parse_github_log(log_file_path: str) -> str:
    """
    Parse GitHub log lines to identify hanging tests.

    Parameters
    ----------
    log_file_path: str
        The path of the log file from GitHub.

    Returns
    -------
        Name of the haging tests.
    """
    tests = {}
    hanging_tests = []

    with open(log_file_path, "r", encoding="utf-8") as f:
        log_lines = f.readlines()

    for line in log_lines:
        test_name = strip_before_tests(line)
        if test_name:
            if tests.get(test_name):
                tests[test_name] += 1
            else:
                tests[test_name] = 1

    for key, value in tests.items():
        if value != 2:
            hanging_tests.append(key)

    return hanging_tests


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A script to print the name of the hanging test by parsing the GitHub logs file."
    )
    parser.add_argument(
        "-logfile",
        type=str,
        help="Path of the log file.",
    )
    args = parser.parse_args()
    hanging_tests = parse_github_log(args.logfile)
    if hanging_tests:
        print("\n Hanging tests detected.\n")
        for test in hanging_tests:
            print(test)
    else:
        print("No hanging tests detected.")
