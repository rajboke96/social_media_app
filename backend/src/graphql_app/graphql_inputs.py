import strawberry
from typing import List, Optional
from social_media_app.schemas import AccountType, Gender, Visibility
from datetime import date
from strawberry.file_uploads import Upload

@strawberry.input
class CreateTokenInput:
    username:str
    password:str

@strawberry.input
class CreateUserInput:
    firstname:str
    middlename:Optional[str]=None
    Lastname:Optional[str]=None
    dob:Optional[str]=None
    gender:Optional[Gender]=None
    username:str
    password:str
    email_address:Optional[str]=None
    # account_type: AccountType

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
    image: Upload # Use the Upload scalar for the image file

@strawberry.input
class PostFilterInput:
    search: str
    # active_only: bool = True