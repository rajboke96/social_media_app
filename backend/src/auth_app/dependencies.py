from jose import JWTError, jwt
from .security import verify_password, SECRET_KEY, ALGORITHM
from .models import TokenData
from social_media_app.schemas import User
from fastapi import Depends, Request
from typing import Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from src.logger import get_logger
logger = get_logger(__name__)

async def get_user(db: AsyncSession, username: str):
    statement = select(User).where(User.username == username)
    result = await db.execute(statement)
    logger.info('exit')
    return result.scalar_one_or_none()

async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user(db, username)
    if not user:
        logger.info('exit')
        return False
    if not verify_password(password, user.hashed_password):
        logger.info('exit')
        return False
    logger.info('exit')
    return user

async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)) -> Optional[User]:
    token = request.cookies.get("auth_token")
    if not token:
        logger.info('exit')
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if "exp" in payload and payload["exp"] < datetime.utcnow().timestamp():
            logger.info('exit')
            return None
        username: str = payload.get("sub")
        if username is None:
            logger.info('exit')
            return None
        token_data = TokenData(username=username)
    except JWTError:
        logger.info('exit')
        return None
    logger.info('exit')
    return await get_user(db, username=token_data.username)
