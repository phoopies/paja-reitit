import re


def is_valid_hex(hex: str) -> bool:
    return re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', hex)