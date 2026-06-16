# app/auth/router.py
from fastapi import APIRouter, Request, Response, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth_app.oauth_config import oauth
from auth_app.service import upsert_social_user
from auth_app.security import create_access_token
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

router = APIRouter()

# --- GOOGLE ROUTES ---

@router.get('/login/google')
async def login_google(request: Request):
    redirect_uri = "http://localhost:8000/auth/callback/google"
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get('/callback/google')
async def callback_google(response: Response, request: Request, db: AsyncSession = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get('userinfo')
        print("usrinfo-------->", user_info)
        if not user_info:
            raise HTTPException(status_code=400, detail="Failed to fetch Google profile info.")
        
        # JIT Provisioning / Upsert local DB matching
        user = await upsert_social_user(
            db=db, 
            firstname=user_info['given_name'],
            email=user_info['email'], 
            provider='google', 
            provider_id=user_info['sub']
        )
        # Generate your independent system JWT 
        token = create_access_token(data={"sub": str(user.username)})
        
        # Set the HttpOnly cookie
        response.set_cookie(
            key="auth_token",
            value=token,
            httponly=True,
            secure=False,   # Required for HTTPS (Production)
            samesite="lax" # Change to "none" if frontend/backend are on different domains
        )
        print("Response: ", response)
        return f"User {user.username} logged in!"
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Authentication error: {str(e)}")
