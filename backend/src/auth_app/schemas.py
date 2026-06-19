from pydantic import BaseModel
from src.logger import get_logger
logger = get_logger(__name__)

class UserBase(BaseModel):
    username: str
    firstname: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
