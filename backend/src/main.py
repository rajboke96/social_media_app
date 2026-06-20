# main.py
from fastapi import FastAPI
from sqlalchemy import select
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = ROOT_DIR.parent if ROOT_DIR.name == 'src' else ROOT_DIR
sys.path.insert(0, str(PROJECT_ROOT))

from social_media_app.graphql_app.graphql_app import sm_app_router
from auth_app.graphql_app.graphql_app import graphql_auth_router
from social_media_app.schemas import UserRole, User, UserSetting
from auth_app.security import get_password_hash
from fastapi.middleware.cors import CORSMiddleware
import os
from starlette.middleware.sessions import SessionMiddleware
from auth_app.router import router as auth_router
from database import engine, AsyncSessionLocal
from contextlib import asynccontextmanager
from social_media_app.schemas import Base
from src.logger import get_logger
from starlette.config import Config

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

# Handle expected Strawberry GraphQL authorization errors concisely
from fastapi.responses import JSONResponse
from strawberry.exceptions import StrawberryGraphQLError


@app.exception_handler(StrawberryGraphQLError)
async def handle_strawberry_graphql_error(request, exc: StrawberryGraphQLError):
    # Log a concise message only (no stacktrace) for authorization/authentication errors
    logger.info('GraphQL authorization error: %s', str(exc))
    # Return a GraphQL-formatted error response so clients receive the error in the usual shape
    return JSONResponse(status_code=200, content={"data": None, "errors": [{"message": str(exc)}]})

config = Config(".env")
origins = config.get("CORS_ORIGINS").split(",") 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=config.get("SECRET_KEY"))

@app.on_event("startup")
async def create_initial_admin():
    logger.info('enter create_initial_admin')
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User).where(User.role == UserRole.ADMIN))
        admin_exists = result.first()
        if not admin_exists:
            admin_user = User(
                firstname="",
                username="admin",
                hashed_password=get_password_hash(Config("admin_password")),
                role=UserRole.ADMIN,
            )
            user_setting = UserSetting(user=admin_user)
            async with db.begin():
                logger.debug('Performing SQLAlchemy session operation')
                logger.debug('Performing SQLAlchemy session operation')
                db.add_all([user_setting, admin_user])

app.include_router(sm_app_router, prefix="/app/graphql")
app.include_router(graphql_auth_router, prefix="/auth/graphql")
app.include_router(auth_router, prefix="/auth")

@app.get("/")
async def root():
    logger.info('exit')
    return {"message": "Hello Bigger Applications!"}
