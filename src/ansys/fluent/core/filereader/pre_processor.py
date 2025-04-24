"""
Pre-processor for XML content from Fluent project files.
"""

import re


def remove_unsupported_xml_chars(content: str):
    """Remove unsupported XML characters from the content."""
    # Replace double colons in tag names with double underscores
    content = re.sub(r"</?([^> ]+)::", r"<\1__", content)

    return content
