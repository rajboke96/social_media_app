from jose import JWTError, jwt
from sqlalchemy.orm import Session
from .security import verify_password, get_password_hash, create_access_token, SECRET_KEY, ALGORITHM
from .models import TokenData
from social_media_app.schemas import User
from database import SessionLocal
from fastapi import Depends, Request, Header
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def get_current_user(request: Request, db: Session = Depends(get_db), authorization: Optional[str] = Header(None)):
    # if not authorization:
    #     return None
    
    # parts = authorization.split()
    
    # if len(parts) > 1 and parts[0].lower() == "bearer":
    #     token = parts[1]
    # else:
    #     token = parts[0]
    # if not token:
    #     return

    # Get the cookie by name
    token = request.cookies.get("auth_token")
    
    if not token:
        return
    
    # print(token)
    # credentials_exception = HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="Could not validate credentials",
    #     headers={"WWW-Authenticate": "Bearer"},
    # )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload["exp"])
        print("current time: ",datetime.utcnow().timestamp())
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
    user = get_user(db, username=token_data.username)
    print("User: ", User)
    if user is None:
        # raise credentials_exception
        return None
    db.expunge(user)
    return user