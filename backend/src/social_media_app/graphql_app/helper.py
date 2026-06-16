import base64
from typing import Optional

# Helper utility to decode Strawberry/Relay's Base64 cursor to a number
def decode_cursor_to_offset(cursor_string: Optional[str]) -> int:
    if not cursor_string:
        return 0
    try:
        # Relay cursors look like 'arrayconnection:4'
        decoded = base64.b64decode(cursor_string.encode()).decode()
        if ":" in decoded:
            return int(decoded.split(":")[-1]) + 1
    except Exception:
        pass
    return 0