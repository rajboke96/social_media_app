import strawberry
from .graphql_inputs import CreateUserInput, CreateTokenInput, UpdateUserInput, UserPostInput, UpdateUserSettingInput
from typing import Optional
from .graphql_nodes import UserNode, UserPostNode, UserSettingNode
from .graphql_types import Token
from auth_app.auth import login_for_access_token, signup
from auth_app.models import LoginFormData, SignupFormData
from database import get_db
from contextlib import contextmanager
from .context_permissions import IsAuthenticated
from social_media_app.schemas import Post
from datetime import datetime
from fastapi import Response

@strawberry.type
class Mutation:
    @strawberry.field
    # def login(self, data: CreateTokenInput)->Optional[Token]:
    def login(self, info: strawberry.Info, data: CreateTokenInput)->Optional[str]:
        login_form=LoginFormData(username=data.username, password=data.password)
        token=login_for_access_token(form_data=login_form)
        if token:
            # return Token(access_token=token.access_token, token_type=token.token_type)
        
            # Access the FastAPI Response object from context
            response: Response = info.context.response
            
            # Set the HttpOnly cookie
            response.set_cookie(
                key="auth_token",
                value=token.access_token,
                httponly=True,
                secure=False,   # Required for HTTPS (Production)
                samesite="lax" # Change to "none" if frontend/backend are on different domains
            )
            print("Response: ", response)
            
            return f"User {data.username} logged in!"

    @strawberry.field
    def signup(self, data: CreateUserInput) -> Optional[UserNode]:
        signup_form=SignupFormData(username=data.username, password=data.password, firstname=data.firstname)
        db_user=signup(user=signup_form)
        if db_user:
            user=UserNode.from_db(db_user)
            return user

    # @strawberry.field
    # def update_user_setting(self, info: strawberry.Info, data: UpdateUserSettingInput) -> Optional[UserSetting]:
    #     user_id=info.context.user.id
    #     db_user_setting=get_user_setting(user_id)
    #     if data.theme is not strawberry.UNSET:
    #         db_user_setting.theme=data.theme
    #     with contextmanager(get_db)() as db:
    #         db.add(db_user_setting)
    #         db.commit()
    #         return UserSettingNode(id=db_user_setting.id,
    #                            user=User.from_db(get_user_by_id(db_user_setting.user_id)),
    #                            theme=db_user_setting.theme.value)

    @strawberry.field(permission_classes=[IsAuthenticated])
    def create_post(self, info: strawberry.Info, data: UserPostInput)->Optional[UserPostNode]:
        user_id=info.context.user.id
        user_post=Post(title=data.title,
            description=data.description,
            created_by=user_id,
            created_at=datetime.now(),
            visibility=data.visibility
            )
        with contextmanager(get_db)() as db:
            db.add(user_post)
            db.commit()
            return UserPostNode.from_db(info, user_post)

    @strawberry.field
    def update_user(self, info: strawberry.Info, data: UpdateUserInput) -> Optional[UserNode]:
        # 1. Fetch existing user from your database
        user_id=info.context.user.id
        user = UserNode.get(user_id)
        
        # 2. Only update if the field is NOT UNSET
        if data.firstname is not strawberry.UNSET:
            user.firstname = data.firstname # Could be a string or None
        if data.middlename is not strawberry.UNSET:
            user.middlename = data.middlename # Could be a string or None
        if data.Lastname is not strawberry.UNSET:
            user.Lastname = data.Lastname # Could be a string or None
        if data.account_type is not strawberry.UNSET:
            user.account_type = data.account_type # Could be a string or None
        if data.dob is not strawberry.UNSET:
            user.dob = data.dob # Could be a string or None
        with contextmanager(get_db)() as db:
            db.add(user)
            db.commit()
            return UserNode.from_db(user)
        
        # 3. Save and return
        # return user.save()