from .dependencies import get_db, authenticate_user, create_access_token, get_user
from .models import Token
from .models import SignupFormData, LoginFormData
from social_media_app.schemas import User, UserSetting
from .security import get_password_hash  # Import get_password_hash here
from contextlib import contextmanager
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def login_for_access_token(db, form_data: LoginFormData)->Optional[Token]:
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        return None
    access_token = create_access_token(data={"sub": user.username})
    token=Token(access_token=access_token, token_type="bearer")
    return token

async def signup(db, user: SignupFormData)->Optional[User]:
    db_user = await get_user(db, username=user.username)
    if db_user:
        raise Exception("User already exists!")
    hashed_password = get_password_hash(user.password)
    db_user = User(firstname=user.firstname, username=user.username, hashed_password=hashed_password)
    user_setting=UserSetting(user=db_user)
    db.add(db_user)
    db.add(user_setting)
    await db.commit()
    await db.refresh(db_user)
    return db_user
    
async def upsert_social_user(db: AsyncSession, firstname: str, email: str, provider: str, provider_id: str) -> User:
    try:
        statement = select(User).where(User.email_address == email)
        result = await db.execute(statement)
        user = result.scalar_one_or_none()  # Safe alternative to .first()
        if user:
            if not user.oauth_provider:
                user.oauth_provider = provider
                user.oauth_id = provider_id
                await db.commit()
                await db.refresh(user)
            return user
            
        new_user = User(
            firstname=firstname, 
            username=email,
            email_address=email,
            # hashed_password=None,  # No local password needed
            oauth_provider=provider,
            oauth_id=provider_id,
            # is_active=True
        )
        user_setting=UserSetting(user=new_user)
        db.add(user_setting)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except Exception as e:
        print("Error in auth: ", e)
        raise Exception("Error in auth: ", e)