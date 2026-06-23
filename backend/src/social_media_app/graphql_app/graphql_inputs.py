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
    alt: Optional[str] = None
    image: Optional[List[Upload]] = strawberry.UNSET # Use the Upload scalar for the image file

@strawberry.input
class UpdatePostInput:
    id: int
    title: Optional[str] = strawberry.UNSET
    description: Optional[str] = strawberry.UNSET
    visibility: Optional[Visibility] = strawberry.UNSET
    alt: Optional[str] = strawberry.UNSET
    image: Optional[List[Upload]] = strawberry.UNSET

@strawberry.input
class PostFilterInput:
    search: str
    # active_only: bool = True

@strawberry.input
class UpdateProfileInput:
    profile_bio: Optional[str] = strawberry.UNSET
    cover_pic_img: Optional[Upload] = strawberry.UNSET
    profile_pic_img: Optional[Upload] = strawberry.UNSET
    city_id: Optional[int] = strawberry.UNSET
