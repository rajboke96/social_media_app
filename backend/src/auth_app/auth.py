from .dependencies import get_db, authenticate_user, create_access_token, get_user
from .models import Token
from .models import SignupFormData, LoginFormData
from social_media_app.schemas import User, UserSetting
from .utils import get_password_hash  # Import get_password_hash here
from contextlib import contextmanager
from typing import Optional

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