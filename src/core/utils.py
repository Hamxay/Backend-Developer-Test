from typing import Optional, Tuple
import re


def parse_integrity_error_message(
    error_msg: str,
) -> Tuple[Optional[str], Optional[str]]:
    key_value_pattern = r"DETAIL:  Key \((.*?)\)=\((.*?)\)"
    match = re.search(key_value_pattern, error_msg)
    if match:
        keys, values = match.groups()
        return keys, values
    return None, None
