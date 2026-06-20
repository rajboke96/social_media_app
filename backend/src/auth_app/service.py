from .dependencies import authenticate_user, get_user
from .models import Token
from .models import SignupFormData, LoginFormData
from social_media_app.schemas import User, UserSetting
from .security import get_password_hash, create_access_token
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.logger import get_logger

logger = get_logger(__name__)

async def login_for_access_token(db: AsyncSession, form_data: LoginFormData) -> Optional[Token]:
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        return None
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")

async def signup(db: AsyncSession, user: SignupFormData) -> Optional[User]:
    db_user = await get_user(db, username=user.username)
    if db_user:
        raise Exception("User already exists!")
    hashed_password = get_password_hash(user.password)
    db_user = User(firstname=user.firstname, username=user.username, hashed_password=hashed_password)
    user_setting = UserSetting(user=db_user)
    db.add_all([db_user, user_setting])
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
        logger.error('Error in auth during upsert_social_user: %s', e, exc_info=True)
        raise