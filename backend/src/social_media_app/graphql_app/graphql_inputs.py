import strawberry
from strawberry import relay
from typing import List, Optional
from social_media_app.schemas import AccountType, Gender, Visibility, FriendRequestStatus
from datetime import date
from strawberry.file_uploads import Upload
from src.logger import get_logger
logger = get_logger(__name__)

@strawberry.input
class UpdateFriendRequest:
    friend_id: relay.GlobalID
    status: FriendRequestStatus

@strawberry.input
class UpdateUserSettingInput:
    theme: Optional[str] = strawberry.UNSET

@strawberry.input
class ChangePasswordInput:
    current_password: str  # Required for security
    new_password: str
    confirm_new_password: str

@strawberry.input
class UpdateUserInput:
    id: int
    # Setting the default to UNSET makes it optional in GraphQL
    firstname: Optional[str] = strawberry.UNSET
    middlename:Optional[str]= strawberry.UNSET
    Lastname:Optional[str]= strawberry.UNSET
    dob:Optional[date]= strawberry.UNSET
    gender:Optional[Gender]= strawberry.UNSET
    email_address:Optional[str]= strawberry.UNSET
    account_type: Optional[AccountType]= strawberry.UNSET

@strawberry.input
class UserPostInput:
    title:str
    description: Optional[str]=None
    visibility: Visibility
    alt: str
    image: List[Upload] # Use the Upload scalar for the image file

@strawberry.input
class PostFilterInput:
    search: str
    # active_only: bool = True
