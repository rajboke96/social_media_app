import enum 
from src.logger import get_logger
logger = get_logger(__name__)

class Option(enum.Enum):
    ACCOUNT_TYPE="account_type"
    ACCOUNT_STATUS="account_status"
    VISIBILITY="visibility"
    GENDER="gender"
    MEDIA_TYPE="media_type"
    THEME="theme"
