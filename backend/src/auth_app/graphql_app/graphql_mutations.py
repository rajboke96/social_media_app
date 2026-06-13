import strawberry
from typing import Optional
from auth_app.auth import login_for_access_token, signup
from auth_app.models import LoginFormData, SignupFormData
from fastapi import Response
from .graphql_inputs import CreateTokenInput, CreateUserInput
from .context_permissions import IsAuthenticated

@strawberry.type
class Mutation:
    @strawberry.field
    def login(self, info: strawberry.Info, data: CreateTokenInput)->Optional[str]:
        login_form=LoginFormData(username=data.username, password=data.password)
        token=login_for_access_token(form_data=login_form)
        if token:
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
    def signup(self, info: strawberry.Info, data: CreateUserInput) -> Optional[str]:
        signup_form=SignupFormData(username=data.username, password=data.password, firstname=data.firstname)
        db_user=signup(user=signup_form)
        if db_user:
            return "User registered successfull!"
        
    @strawberry.field(permission_classes=[IsAuthenticated])
    def logout(self, info: strawberry.Info) -> str:
        # Access the FastAPI Response object from context
        response: Response = info.context.response
        response.delete_cookie(key="auth_token")
        return "Logged out successfully!"