from jose import JWTError, jwt
from sqlalchemy.orm import Session
from .security import verify_password, get_password_hash, create_access_token, SECRET_KEY, ALGORITHM
from .models import TokenData
from social_media_app.schemas import User
from database import AsyncSessionLocal
from fastapi import Depends, Request, Header
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select
from database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_user(db: AsyncSession, username: str):
    statement=select(User).where(User.username == username)
    result = await db.execute(statement)
    return result.scalar_one_or_none()
    # return db.query(User).filter(User.username == username).first()

async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

async def get_current_user(request: Request, db: AsyncSession = Depends(get_db), authorization: Optional[str] = Header(None)):
    token = request.cookies.get("auth_token")
    if not token:
        return
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload["exp"])
        if "exp" in payload and payload["exp"] < datetime.utcnow().timestamp():
            return None
        username: str = payload.get("sub")
        if username is None:
            # raise credentials_exception
            return None
        token_data = TokenData(username=username)
    except JWTError:
        # raise credentials_exception
        return None
    user = await get_user(db, username=token_data.username)
    if user is None:
        # raise credentials_exception
        return None
    db.expunge(user)
    return user