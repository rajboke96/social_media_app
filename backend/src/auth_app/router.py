# app/auth/router.py
from fastapi import APIRouter, Request, Response, Depends, HTTPException
from fastapi.responses import RedirectResponse
from src.logger import get_logger
logger = get_logger(__name__)

from database import get_db_factory
from auth_app.oauth_config import oauth
from auth_app.service import upsert_social_user
from auth_app.security import create_access_token
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
import os

# --- GOOGLE ROUTES ---

@router.get('/login/google')
async def login_google(request: Request):
    logger.info('enter login_google')
    redirect_uri = "http://localhost:8000/auth/callback/google"
    logger.info('exit')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get('/callback/google')
async def callback_google(response: Response, request: Request, db = Depends(get_db_factory)):
    logger.info('enter callback_google')
    db_factory = await get_db_factory()
    async with db_factory() as db:
        try:
            token = await oauth.google.authorize_access_token(request)
            user_info = token.get('userinfo')
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
            
            redirect_url = f"{os.environ.get('FRONTEND_URL', 'http://localhost:5173')}/"
            response = RedirectResponse(url=redirect_url)
            
            # --- Attach the cookie directly to this object ---
            response.set_cookie(
                key="auth_token",
                value=token,
                httponly=True,
                secure=False,   # Keep False for localhost, change to True for Production HTTPS
                samesite="lax"  # If frontend is port 5173 and backend is 8000, "lax" works as they share localhost
            )
            
            logger.info('exit')
            return response # Return the prepared response object
        except Exception as e:
            logger.error('Error in Google OAuth callback: %s', e, exc_info=True)
            raise HTTPException(status_code=400, detail=f"Authentication error: {str(e)}")
