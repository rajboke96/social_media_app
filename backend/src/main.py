# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
# from routers import items, users # Import the router modules
# from auth import routes as auth_routes
from social_media_app.graphql_app.graphql_app import sm_app_router
from auth_app.graphql_app.graphql_app import graphql_auth_router
from pathlib import Path
import sys
from database import get_db
from social_media_app.schemas import UserRole, User, UserSetting
from auth_app.security import get_password_hash
from contextlib import contextmanager
from fastapi.middleware.cors import CORSMiddleware
# from fastapi import FastAPI
# from starlette.middleware.sessions import SessionMiddleware
# from auth_app.router import router as auth_router
import os
from starlette.middleware.sessions import SessionMiddleware
from auth_app.router import router as auth_router
from database import engine
from contextlib import asynccontextmanager
from social_media_app.schemas import Base

ROOT_DIR=Path(__file__).parent.resolve()
sys.path.append(ROOT_DIR)

# 5. Application Lifespan Manager (Global Lifecycle)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup: Create tables if they do not exist (Optional: better to use Alembic)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Teardown: Safely shut down connection pools on exit
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

# app = FastAPI()

# Allowed origins
origins = ["http://127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crucial for OAuth state tracking verification
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

@app.on_event("startup")
async def create_initial_admin():
    with contextmanager(get_db)() as db:
        # Replace with your actual database logic
        admin_exists = db.query(User).filter(User.role==UserRole.ADMIN.value).first()
        if not admin_exists:
            print("No admin found. Creating default admin...")
            admin_user=User(firstname="", username="admin", hashed_password=get_password_hash("admin@123"), role=UserRole.ADMIN.value)
            user_setting=UserSetting(user=admin_user)
            db.add(user_setting)
            db.add(admin_user)
            db.commit()

app.include_router(sm_app_router, prefix="/app/graphql")
app.include_router(graphql_auth_router, prefix="/auth/graphql")

app.include_router(auth_router, prefix="/auth")

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
