# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Module for analyzing API docstrings."""

# N.b. misspellings:
# - selected missing last e.
# - many known API misspellings also have corresponding
#   misspellingling for docstring.
# - CGSN

import re

_choose_words = ("Choose", "Indicate", "Select", "Specify")

_remove_first_words = _choose_words + ("Enter", "Set", "To")

# Define problematic patterns with exclusions
_dubious_patterns = [
    (r"Create an instance of this.", ()),
    (r"Enter the adaption .* menu.", ()),
    (r"Allows you to .*", ()),
    (r"Select to .*", ("method",)),
    (r"Choose .*", ("method",)),
    (r"Enter .*", ("method",)),
    (r"Indicate .*", ("method",)),
    (r"Perform .*", ("method",)),
    (r"Select .*", ("method",)),
    (r"Set .*", ("method",)),
    (r"Specify .*", ("method",)),
    (r".* menu.", ()),
    (r"To .*", ()),
    (r"Name for an object.*", ()),
]

# Rewriting problematic patterns for suggestions

_bad_0 = {
    r"Create an instance of this.": r"Create a new instance of the current object type.",
    r"Allows you to (.*)": r"\1",
}

_bad_1 = {
    rf"{w} (whether or not|whether|if) (.*)": r"Specifies whether \2"
    for w in _choose_words
}

_bad_2 = {
    r"Select to (.*)": r"Specifies whether to \1",
    r"Perform (.*)": r"Specifies whether to perform \1",
    r"Enter a (.*)": r"The \1",
    r"Enter an (.*)": r"The \1",
    r"(.*) menu.": r"\1 object.",
}

_bad_3 = {rf"{w} (.*)": r"\1" for w in _remove_first_words}

_bad_4 = {r"Name for an object(.*)": r"Object name\1"}

_bad_to_suggested = dict(**_bad_0, **_bad_1, **_bad_2, **_bad_3, **_bad_4)

# Pre-compile fixed-format empty patterns (case-sensitive)
_empty_patterns = [
    re.compile(f"'.*' {item}.") for item in ("child", "command", "query")
]


def _suggest_fix(docstring: str):
    """Suggest an improved version of a problematic docstring."""
    for bad, suggestion in _bad_to_suggested.items():
        match = re.match(bad, docstring)
        if match:
            replacement = match.expand(suggestion)

            # Capitalize if original docstring started with a capital letter
            if docstring[0].isupper():
                replacement = replacement[0].upper() + replacement[1:]

            # Ensure we don't add duplicate periods
            if replacement.endswith("."):
                return replacement
            return replacement + "."

    return None  # No fix available


def _fixed_doc_string(api_item_type, docstring):
    for pattern_str, exclude_types in _dubious_patterns:
        if api_item_type in exclude_types:
            continue

        if re.match(pattern_str, docstring):
            fix = _suggest_fix(docstring)
            new_fix = None
            if fix:
                new_fix = _fixed_doc_string(api_item_type, fix)
            return new_fix or fix

    return None


class _DocStringAnalysis:
    """Analyzes docstrings for potential issues and categorizes them."""

    def __init__(self):
        """Initialize storage for categorized docstring issues."""
        self.dubious = {}
        self.empty = {}
        self.clean = {}

    def analyse(self, api_path: str, api_item_type: str, api_cls: object):
        """Extract and analyze the docstring for a given API item."""
        docstring = self.get_basic_docstring(api_cls)
        self.analyse_docstring(api_path, api_item_type, docstring)

    def analyse_docstring(self, api_path: str, api_item_type: str, docstring: str):
        """Analyze a docstring and categorize it as clean, dubious, or empty."""

        # Check for empty docstrings first (case-sensitive)
        for pattern in _empty_patterns:
            if pattern.match(docstring):
                self.empty[api_path] = (api_item_type, docstring)
                return

        # Check for dubious patterns
        # TODO just use None?
        fix = _fixed_doc_string(api_item_type, docstring)
        if fix:
            self.dubious[api_path] = (api_item_type, docstring, fix)
            return

        # If no issues, classify as clean
        self.clean[api_path] = (api_item_type, docstring)

    def get_basic_docstring(self, api_cls: object):
        """Extract and clean a class docstring, handling None values."""
        raw_docstring = api_cls.__doc__ or ""
        docstring = "".join(raw_docstring.splitlines()).strip()

        # Remove parameters section if present
        params_section = "        Parameters    ----------        "
        idx = docstring.find(params_section)
        return docstring[:idx] if idx != -1 else docstring

    def show_results(self):
        """Print a categorized summary of analyzed docstrings."""
        print("\nSummary:\n")
        for label, result in [
            ("Empty", self.empty),
            ("Dubious", self.dubious),
            ("Clean", self.clean),
        ]:
            count = len(result)
            print(f"{label}: {count}")
            if label == "Dubious":
                fix_count = len([i for i in result.values() if i[2]])
                print(
                    f"\tNumber with/without suggested fixes: {fix_count}/{count - fix_count}"
                )

        print("\nDetailed results:")
        for label, result in [
            ("Empty", self.empty),
            ("Dubious", self.dubious),
            ("Clean", self.clean),
        ]:
            print(f"\n{label} ({len(result)}):")
            for k, (t, s, *extra) in result.items():
                print(f"{k} ({t}):")
                print(f"\t{s}")

                # Suggest fixes for dubious patterns
                if label == "Dubious" and extra:
                    suggested = extra[0]
                    if suggested:
                        print(f"\tSuggested Fix: {suggested}")
                    else:
                        print("\tNo suggested fix")


def show_all_doc_strings(api_path: str, api_item_type: str, api_cls: object):
    """Prints all docstrings for debugging."""
    indent = "  " * (api_path.count("."))
    bullet = f"{indent}-"

    print(f"{bullet} item: {api_path.split('.')[-1]}")
    print(f"{bullet} type: {api_item_type}")
    print(f"{bullet} docstring: {api_cls.__doc__}")


if __name__ == "__main__":
    import argparse
    import importlib

    from ansys.fluent.core.codegen import walk_api

    # Sample Usage
    #
    # Whole Fluent settings API check with default settings
    # >>> python src\ansys\fluent\core\solver\_docstrings.py --api-version=252

    parser = argparse.ArgumentParser()
    parser.add_argument("--cls", dest="api_cls", type=str, default="root")
    parser.add_argument("--path", dest="api_path", type=str, default="")
    parser.add_argument("--output-type", dest="output_type", type=str, default="stats")
    parser.add_argument("--api-version", dest="api_version", type=str, default="")

    args = parser.parse_args()

    api_cls = args.api_cls
    api_path = args.api_path
    output_type = args.output_type
    api_version = args.api_version

    mod = importlib.import_module(
        name=f"ansys.fluent.core.generated.solver.settings_{api_version}"
    )
    cls = getattr(mod, api_cls)

    if output_type == "show":
        walk_api.walk_api(cls, show_all_doc_strings, api_path)
    elif output_type == "stats":
        analysis = _DocStringAnalysis()
        walk_api.walk_api(cls, analysis.analyse, api_path)
        analysis.show_results()
