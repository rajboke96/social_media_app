import strawberry
from fastapi import Depends
from strawberry.fastapi import BaseContext
from strawberry.permission import BasePermission
from typing import Optional, Any
from auth_app.dependencies import get_current_user
from auth_app.models import UserType
from social_media_app.schemas import User as UserModel
from database import get_db, get_db_factory
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

class CustomContext(BaseContext):
    def __init__(self, user: Optional[UserModel], db: AsyncSession, db_factory):
        super().__init__()
        if user:
            # user=UserType(id=user.id, username=user.username, role=user.role.value)
            pass
        self.user = user
        self.db=db
        self.db_factory=db_factory

async def get_context(user: Optional[UserModel] = Depends(get_current_user), db: AsyncSession=Depends(get_db)) -> CustomContext:
    return CustomContext(user=user, db=db, db_factory=await get_db_factory())

# 4. Authorization: Permission Classes
class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    def has_permission(self, source: Any, info: strawberry.Info, **kwargs) -> bool:
        return info.context.user is not None

class IsAdmin(BasePermission):
    message = "Admin privileges required"

    def has_permission(self, source: Any, info: strawberry.Info, **kwargs) -> bool:
        user = info.context.user
        return user is not None and user.role == "admin"
