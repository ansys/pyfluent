"""Provides a module to fix text documentation for a data object."""

from io import StringIO


def escape_wildcards(doc: str):
    """Escape wildcards."""
    new_doc = StringIO()
    prev_c = None
    for i, c in enumerate(doc):
        if c == "*":
            if prev_c == "\\":
                new_doc.write(r"\*")
            else:
                new_doc.write(r"\\*")
        else:
            new_doc.write(c)
        prev_c = c
    return new_doc.getvalue()


def fix_definition_list_in_class_doc(doc: str):
    """Fix definition list in class docstring."""
    old_lines = doc.splitlines(keepends=True)
    new_lines = []
    for i, line in enumerate(old_lines):
        if line.strip().startswith("-") and not line.strip().startswith("--"):
            if i == 0:
                new_lines.append("\n")
                new_lines.append(line)
            elif i == len(old_lines) - 1:
                new_lines.append(line)
                new_lines.append("\n")
            else:
                prev_line = old_lines[i - 1].strip()
                if prev_line and not prev_line.startswith("-"):
                    new_lines.append("\n")
                new_lines.append(line)
                next_line = old_lines[i + 1].strip()
                if next_line and not next_line.startswith("-"):
                    new_lines.append("\n")
        else:
            new_lines.append(line)
    return "".join(new_lines)


def fix_settings_doc(doc: str):
    """Fix settings docstring."""
    doc = escape_wildcards(doc)
    return fix_definition_list_in_class_doc(doc)
