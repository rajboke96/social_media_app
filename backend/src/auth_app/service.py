from .dependencies import get_db, authenticate_user, create_access_token, get_user
from .models import Token
from .models import SignupFormData, LoginFormData
from social_media_app.schemas import User, UserSetting
from .security import get_password_hash  # Import get_password_hash here
from contextlib import contextmanager
from typing import Optional
from sqlalchemy.orm import Session

def login_for_access_token(form_data: LoginFormData)->Optional[Token]:
    with contextmanager(get_db)() as db:
        user = authenticate_user(db, form_data.username, form_data.password)
        if not user:
            return None
        access_token = create_access_token(data={"sub": user.username})
        token=Token(access_token=access_token, token_type="bearer")
        return token

def signup(user: SignupFormData)->Optional[User]:
    with contextmanager(get_db)() as db:
        db_user = get_user(db, username=user.username)
        if db_user:
            raise Exception("User already exists!")
        hashed_password = get_password_hash(user.password)
        db_user = User(firstname=user.firstname, username=user.username, hashed_password=hashed_password)
        user_setting=UserSetting(user=db_user)
        db.add(db_user)
        db.add(user_setting)
        db.commit()
        db.refresh(db_user)
        return db_user
    
def upsert_social_user(db: Session, firstname: str, email: str, provider: str, provider_id: str) -> User:
    # 1. Check if the user already exists by email
    user = db.query(User).filter(User.email_address == email).first()
    
    if user:
        # User exists! Update their OAuth tracking details if not already set
        if not user.oauth_provider:
            user.oauth_provider = provider
            user.oauth_id = provider_id
            db.commit()
            db.refresh(user)
        return user
        
    # 2. User does not exist, so register them for the first time automatically
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
    db.commit()
    db.refresh(new_user)
    return new_user
