# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
# from routers import items, users # Import the router modules
# from auth import routes as auth_routes
from graphql_app.graphql_app import graphql_router
from pathlib import Path
import sys
from database import get_db
from social_media_app.schemas import UserRole, User
from auth_app.utils import get_password_hash
from contextlib import contextmanager
from fastapi.middleware.cors import CORSMiddleware

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

# Add the GraphQL route to FastAPI
app.include_router(graphql_router, prefix="/graphql")
# Rest API's Route
# app.include_router(sm_app_routes.router, prefix="/sm_app", tags=["sm_app"])
# app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
