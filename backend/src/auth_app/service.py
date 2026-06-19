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
        logger.info('exit')
        return None
    access_token = create_access_token(data={"sub": user.username})
    logger.info('exit')
    return Token(access_token=access_token, token_type="bearer")

async def signup(db: AsyncSession, user: SignupFormData) -> Optional[User]:
    db_user = await get_user(db, username=user.username)
    if db_user:
        raise Exception("User already exists!")
    hashed_password = get_password_hash(user.password)
    db_user = User(firstname=user.firstname, username=user.username, hashed_password=hashed_password)
    user_setting = UserSetting(user=db_user)
    async with db.begin():
        logger.debug('Performing SQLAlchemy session operation')
        logger.debug('Performing SQLAlchemy session operation')
        db.add_all([db_user, user_setting])
    logger.debug('Performing SQLAlchemy session operation')
    await db.refresh(db_user)
    logger.info('exit')
    return db_user

async def upsert_social_user(db: AsyncSession, firstname: str, email: str, provider: str, provider_id: str) -> User:
    statement = select(User).where(User.email_address == email)
    result = await db.execute(statement)
    user = result.scalar_one_or_none()

    if user:
        if not user.oauth_provider:
            user.oauth_provider = provider
            user.oauth_id = provider_id
            async with db.begin():
                db.add(user)
            logger.debug('Performing SQLAlchemy session operation')
            await db.refresh(user)
        logger.info('exit')
        return user

    new_user = User(
        firstname=firstname,
        username=email,
        email_address=email,
        oauth_provider=provider,
        oauth_id=provider_id,
    )
    user_setting = UserSetting(user=new_user)
    async with db.begin():
        logger.debug('Performing SQLAlchemy session operation')
        logger.debug('Performing SQLAlchemy session operation')
        db.add_all([new_user, user_setting])
    logger.debug('Performing SQLAlchemy session operation')
    await db.refresh(new_user)
    logger.info('exit')
    return new_user
