# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
# from routers import items, users # Import the router modules
# from auth import routes as auth_routes
from social_media_app.graphql_app.graphql_app import sm_app_router
from auth_app.graphql_app.graphql_app import auth_router
from pathlib import Path
import sys
from database import get_db
from social_media_app.schemas import UserRole, User
from auth_app.utils import get_password_hash
from contextlib import contextmanager
from fastapi.middleware.cors import CORSMiddleware
# from fastapi import FastAPI
# from starlette.middleware.sessions import SessionMiddleware
# from auth_app.router import router as auth_router
import os

ROOT_DIR=Path(__file__).parent.resolve()
sys.path.append(ROOT_DIR)

app = FastAPI()

# Allowed origins
origins = ["http://127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def create_initial_admin():
    with contextmanager(get_db)() as db:
        # Replace with your actual database logic
        admin_exists = db.query(User).filter(User.role==UserRole.ADMIN.value).first()
        if not admin_exists:
            print("No admin found. Creating default admin...")
            admin_user=User(firstname="", username="admin", hashed_password=get_password_hash("admin@123"), role=UserRole.ADMIN.value)
            db.add(admin_user)
            db.commit()

# Crucial for OAuth state tracking verification
# app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

# app.include_router(auth_router, prefix="/auth")

# Add the GraphQL route to FastAPI
app.include_router(sm_app_router, prefix="/app/graphql")
app.include_router(auth_router, prefix="/auth/graphql")
# Rest API's Route
# app.include_router(sm_app_routes.router, prefix="/sm_app", tags=["sm_app"])
# app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
