import base64
from typing import Optional
from src.logger import get_logger
logger = get_logger(__name__)

# Helper utility to decode Strawberry/Relay's Base64 cursor to a number
def decode_cursor_to_offset(cursor_string: Optional[str]) -> int:
    if not cursor_string:
        logger.info('exit')
        return 0
    try:
        # Relay cursors look like 'arrayconnection:4'
        decoded = base64.b64decode(cursor_string.encode()).decode()
        if ":" in decoded:
            logger.info('exit')
            return int(decoded.split(":")[-1]) + 1
    except Exception:
        pass
    logger.info('exit')
    return 0

def decode_node_id(node_id: str):
    # Decode the Base64 token back into a readable string
    decoded_bytes = base64.b64decode(node_id)
    decoded_str = decoded_bytes.decode("utf-8")
    
    # Split the type name from the database ID using the colon separator
    type_name, original_id = decoded_str.split(":", 1)
    
    logger.info('exit')
    return type_name, original_id
