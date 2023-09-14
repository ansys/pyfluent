from typing import Optional, Tuple


def parse_temperature_units(
    units: str, ignore_exponent: bool, units_to_search: Optional[Tuple[str]] = None
) -> list:
    if units_to_search is None:
        units_to_search = ("K", "C", "F", "R")
    units_out = []
    for term in units.split(" "):
        term_parts = term.split("^")
        label = term_parts[0]
        exponent = term_parts[0] if len(term_parts) > 1 else "0"
        is_temp_diff = (
            label
            and (exponent != "0" or ignore_exponent)
            and label[-1] in units_to_search
        )
        units_out.append((term, is_temp_diff))
    return units_out
