from pydantic import BaseModel
from src.logger import get_logger
logger = get_logger(__name__)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserBase(BaseModel):
    username: str

class SignupFormData(UserBase):
    firstname: str
    password: str

class LoginFormData(UserBase):
    password: str

class UserType:
    def __init__(self, id: int, username: str, role: str):
        self.id = id
        self.username = username
        self.role = role
