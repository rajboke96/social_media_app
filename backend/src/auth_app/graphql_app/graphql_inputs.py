import strawberry
from typing import Optional
from social_media_app.schemas import Gender

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