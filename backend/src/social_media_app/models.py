from pydantic import BaseModel
from datetime import date

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    account_status: str

    class Config:
        from_attributes = True

class UserProfile(BaseModel):
    firstname: str
    dob: date|None
    class Config:
        from_attributes = True

class UserProfileUpdate(UserProfile):
    pass

class UserFeed(BaseModel):
    pass