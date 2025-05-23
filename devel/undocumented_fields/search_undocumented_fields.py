"""
Search code for undocumented fields in classes. Requires the ast_comments package.

Usage: python search_undocumented_fields.py ../../src
"""

import os
import sys
from typing import Dict, Set

import ast_comments as ast


def is_ith_undocumented_field(nodes, i: int) -> bool:
    """Check if the ith node is an undocumented field assignment."""
    if i > 0 and isinstance(nodes[i - 1], ast.Comment):
        comment = nodes[i - 1].value.strip()
        print(f"Comment found: {comment}")
        if comment.startswith("#:"):
            return False
    return True


class ClassFieldVisitor(ast.NodeVisitor):
    """AST visitor that extracts public fields from classes."""

    def __init__(self):
        self.classes = {}
        self.current_class = None

    def visit_ClassDef(self, node):
        """Visit a class definition and extract field assignments."""
        old_class = self.current_class
        self.current_class = node.name
        self.classes[node.name] = set()
        if node.name.startswith("_"):
            self.current_class = old_class
            return
        is_enum = False
        for x in node.bases:
            if isinstance(x, ast.Name) and x.id in (
                "Enum",
                "IntEnum",
                "StrEnum",
                "FluentEnum",
            ):
                is_enum = True
            elif isinstance(x, ast.Attribute) and x.attr in (
                "Enum",
                "IntEnum",
                "StrEnum",
                "FluentEnum",
            ):
                is_enum = True
        if is_enum:
            self.current_class = old_class
            return  # Skip Enum classes

        # Visit all child nodes
        for i, child in enumerate(node.body):
            if isinstance(child, ast.Assign):
                # Look for assignments in the class body
                for target in child.targets:
                    if isinstance(target, ast.Name):
                        # Only add public fields (not starting with underscore)
                        if target.id.startswith("_"):
                            continue
                        if is_ith_undocumented_field(node.body, i):
                            self.classes[node.name].add(target.id)
            elif isinstance(child, ast.AnnAssign) and isinstance(
                child.target, ast.Name
            ):
                # Handle annotated assignments (e.g., x: int = 10)
                if child.target.id.startswith("_"):
                    continue
                if is_ith_undocumented_field(node.body, i):
                    self.classes[node.name].add(child.target.id)

        # Visit methods to find instance attribute assignments (self.attr = value)
        for child in node.body:
            if isinstance(child, ast.FunctionDef):
                self.visit(child)

        self.current_class = old_class

    def visit_FunctionDef(self, node):
        """Visit method definitions to find instance attributes."""
        if self.current_class is None:
            return

        # Check if this is an instance method with 'self' parameter
        if node.args.args and node.args.args[0].arg == "self":
            results = list(ast.walk(node))
            for i, child in enumerate(results):
                # Look for self.attr = value assignments
                if isinstance(child, ast.Assign) and any(
                    isinstance(target, ast.Attribute)
                    and isinstance(target.value, ast.Name)
                    and target.value.id == "self"
                    and not target.attr.startswith("_")
                    for target in child.targets
                ):
                    for target in child.targets:
                        if (
                            isinstance(target, ast.Attribute)
                            and isinstance(target.value, ast.Name)
                            and target.value.id == "self"
                        ):
                            if is_ith_undocumented_field(results, i):
                                self.classes[self.current_class].add(target.attr)

                # Handle annotated assignments: self.attr: Type = value
                elif (
                    isinstance(child, ast.AnnAssign)
                    and isinstance(child.target, ast.Attribute)
                    and isinstance(child.target.value, ast.Name)
                    and child.target.value.id == "self"
                    and not child.target.attr.startswith("_")
                ):
                    if is_ith_undocumented_field(results, i):
                        self.classes[self.current_class].add(child.target.attr)


def analyze_file(file_path: str) -> Dict[str, Set[str]]:
    """Analyze a Python file and return classes with their public fields."""
    with open(file_path, "r", encoding="utf-8") as file:
        try:
            tree = ast.parse(file.read(), filename=file_path)
            visitor = ClassFieldVisitor()
            visitor.visit(tree)
            return visitor.classes
        except SyntaxError as e:
            print(f"Syntax error in {file_path}: {e}", file=sys.stderr)
            return {}


def analyze_package(package_path: str) -> Dict[str, Dict[str, Set[str]]]:
    """Analyze all Python files in a package directory."""
    result = {}

    for root, dirs, files in os.walk(package_path):
        # Skip directories named "generated"
        if "generated" in dirs:
            dirs.remove("generated")

        for file in files:
            if file.startswith("_"):
                continue
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                module_name = os.path.relpath(file_path, package_path).replace(
                    os.path.sep, "."
                )
                module_name = module_name[:-3]  # Remove .py extension

                classes = analyze_file(file_path)
                if classes:
                    result[module_name] = classes

    return result


def write_results(results: Dict[str, Dict[str, Set[str]]], f) -> str:
    """Format the analysis results."""
    for module_name, classes in sorted(results.items()):

        if not classes:
            continue

        module_written = False
        for class_name, fields in sorted(classes.items()):
            if not fields:
                continue

            if not module_written:
                f.write(f"  Module: {module_name}\n")
                module_written = True

            f.write(f"  Class: {class_name}\n")

            for field in sorted(fields):
                f.write(f"    - {field}\n")

        if module_written:
            f.write("\n")


def main():
    """Main function."""
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <package_directory>", file=sys.stderr)
        sys.exit(1)

    package_path = sys.argv[1]
    if not os.path.isdir(package_path):
        print(f"Error: {package_path} is not a directory", file=sys.stderr)
        sys.exit(1)

    results = analyze_package(package_path)
    with open("undocumented_fields.txt", "w", encoding="utf-8") as f:
        write_results(results, f)


if __name__ == "__main__":
    main()
