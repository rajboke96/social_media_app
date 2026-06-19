import logging
import sys
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
try:
    from strawberry.exceptions import StrawberryGraphQLError
except Exception:
    StrawberryGraphQLError = None


class StrawberryAuthFilter(logging.Filter):
    """Filter that removes exception traceback details for known Strawberry auth errors."""
    def filter(self, record: logging.LogRecord) -> bool:
        try:
            msg = record.getMessage()
            if msg and 'User is not authenticated' in msg:
                # Remove exception info so handlers don't print tracebacks for auth errors
                record.exc_info = None
                record.exc_text = None
        except Exception:
            pass
        return True

# Attach the filter to strawberry loggers if available
_filter = StrawberryAuthFilter()
logging.getLogger('strawberry').addFilter(_filter)
logging.getLogger('strawberry.execution').addFilter(_filter)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
