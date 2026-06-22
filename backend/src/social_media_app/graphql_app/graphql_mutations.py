import strawberry
from .graphql_inputs import UpdateUserInput, UserPostInput, UpdatePostInput, UpdateFriendRequest
from typing import Optional
from .graphql_nodes import UserNode, UserPostNode, FriendRequestNode
from database import get_db_factory
from src.logger import get_logger
logger = get_logger(__name__)

from .context_permissions import IsAuthenticated
from social_media_app.schemas import Post, FriendRequestStatus, Friend, Media, MediaType
from datetime import datetime
from strawberry import relay
from datetime import date
import os
from database import UPLOAD_DIR
import uuid

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

@strawberry.type
class Mutation:
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def create_post(self, info: strawberry.Info, data: UserPostInput)->Optional[UserPostNode]:
        logger.info('enter create_post')
        allowed_types = ["image/jpeg", "image/png", "image/webp"]
        saved_img_list=[]

        if data.image is not strawberry.UNSET and data.image:
            for img in data.image:
                if img.content_type not in allowed_types:
                    logger.error(f"Rejected file {img.filename} with content type {img.content_type}")
                    raise Exception("Invalid file format. Upload JPEG, PNG, or WebP only.")
                    
                # 2. Ensure Asset Directory Exists
                os.makedirs(UPLOAD_DIR, exist_ok=True)
                # 3. Generate a safe unique file name using UUID
                file_extension = os.path.splitext(img.filename)[1]
                unique_filename = f"{uuid.uuid4().hex}{file_extension}"
                file_save_path = os.path.join(UPLOAD_DIR, unique_filename)
                
                # 4. Stream and write the file asynchronously
                contents = await img.read()
                with open(file_save_path, "wb") as f:
                    f.write(contents)
                # 5. Formulate web-accessible URL path
                public_image_url = f"{os.environ['UPLOAD_DIR']}/{unique_filename}"
                saved_img_list.append({
                    "filename": unique_filename,
                    "file_save_path": file_save_path,
                    # "public_image_url": public_image_url,
                })

        async with info.context.db_factory() as db:
            new_post=Post(title=data.title,
            description=data.description,
            # created_by=user_id,
            created_at=datetime.now(),
            visibility=data.visibility,
            )
            new_post.user=info.context.user
            new_post.user = await db.merge(new_post.user)
            for saved_img_data in saved_img_list:
                media=Media(
                    name = saved_img_data["filename"],
                    alt = data.alt,
                    type=MediaType.IMAGE,
                    uploaded_at = datetime.now(),
                    uploaded_to = saved_img_data["file_save_path"],
                    # public_image_url=saved_img_data["public_image_url"]
                )
                media.user=new_post.user
                new_post.media.append(media)
            try:   
                db.add(new_post)
                logger.debug('Committing database transaction')
                logger.debug('Committing database transaction')
                logger.debug('Performing SQLAlchemy session operation')
                await db.commit()
                user_post_node=await UserPostNode.from_db(info, new_post)
                return user_post_node
            except Exception as e:
                # Rollback and clean up local file if the SQL execution fails
                logger.debug('Rolling back database transaction')
                logger.debug('Rolling back database transaction')
                await db.rollback()
                for saved_img_data in saved_img_list:
                    if os.path.exists(saved_img_data["file_save_path"]):
                        os.remove(saved_img_data["file_save_path"])
                raise Exception(f"Database error: {str(e)}")

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def update_post(self, info: strawberry.Info, data: UpdatePostInput) -> Optional[UserPostNode]:
        logger.info('enter update_post')
        db_factory = info.context.db_factory
        async with db_factory() as db:
            statement = select(Post).where(Post.id == data.id).where(Post.created_by == info.context.user.id)
            result = await db.execute(statement)
            post = result.scalar_one_or_none()
            if not post:
                raise HTTPException(404, f"Post {data.id} not found or not owned by user")

            if data.title is not strawberry.UNSET:
                post.title = data.title
            if data.description is not strawberry.UNSET:
                post.description = data.description
            if data.visibility is not strawberry.UNSET:
                post.visibility = data.visibility
            if data.alt is not strawberry.UNSET:
                for media in post.media:
                    media.alt = data.alt

            if data.image is not strawberry.UNSET and data.image:
                allowed_types = ["image/jpeg", "image/png", "image/webp"]
                for img in data.image:
                    if img.content_type not in allowed_types:
                        raise Exception("Invalid file format. Upload JPEG, PNG, or WebP only.")
                    os.makedirs(UPLOAD_DIR, exist_ok=True)
                    file_extension = os.path.splitext(img.filename)[1]
                    unique_filename = f"{uuid.uuid4().hex}{file_extension}"
                    file_save_path = os.path.join(UPLOAD_DIR, unique_filename)
                    contents = await img.read()
                    with open(file_save_path, "wb") as f:
                        f.write(contents)
                    media = Media(
                        name=unique_filename,
                        alt=data.alt if data.alt is not strawberry.UNSET else None,
                        type=MediaType.IMAGE,
                        uploaded_at=datetime.now(),
                        uploaded_to=file_save_path,
                    )
                    media.user = post.user
                    post.media.append(media)

            db.add(post)
            await db.commit()
            await db.refresh(post)
            logger.info('exit')
            return await UserPostNode.from_db(info, post)

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def delete_post(self, info: strawberry.Info, post_id: int)->str:
        logger.info('enter delete_post')
        db_factory = info.context.db_factory 
        async with db_factory() as db:
            stmt = select(Post).options(selectinload(Post.media)).where(Post.id == post_id).where(info.context.user.id==Post.created_by)
            result = await db.execute(stmt)
            user_post=result.scalar_one_or_none()
            if user_post:
                logger.debug('Performing SQLAlchemy session operation')
                [await db.delete(m) for m in user_post.media]
                user_post.media=[]
                logger.debug('Performing SQLAlchemy session operation')
                await db.delete(user_post)
                logger.debug('Committing database transaction')
                logger.debug('Committing database transaction')
                await db.commit()
                logger.info('exit')
                return f"Post {post_id} deleted successfully!"
            else:
                raise HTTPException(404, f"Post {post_id} not found")

    @strawberry.field
    async def update_user(self, info: strawberry.Info, data: UpdateUserInput) -> Optional[UserNode]:
        logger.info('enter update_user')
        # 1. Fetch existing user from your database
        user_id=info.context.user.id
        user = await UserNode.get(user_id)
        
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
        async with get_db_factory() as db:
            db.add(user)
            logger.debug('Committing database transaction')
            logger.debug('Committing database transaction')
            await db.commit()
            logger.info('exit')
            return UserNode.from_db(user)

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def create_friend_request(self, info: strawberry.Info, user_id: relay.GlobalID) -> Optional[str]:
        logger.info('enter create_friend_request')
        user=info.context.user
        db=info.context.db

        # user=db.query(UserModel).filter(UserModel.id==user.id).first()
        friend=await user_id.resolve_node(info)
        # friend=UserNode.get(info, friend.id)
        # 1. Fetch existing user from your database
        new_friendship = Friend(
            user_id=user.id,
            friend_id=friend.id,
            status=FriendRequestStatus.PENDING, # Setting the enum value
            friends_at=date.today()              # Setting the date value
        )
        db.add(new_friendship)
        logger.debug('Committing database transaction')
        logger.debug('Committing database transaction')
        await db.commit()

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def update_friend_request(self, info: strawberry.Info, data: UpdateFriendRequest) -> Optional[str]:
        logger.info('enter update_friend_request')
        # 1. Fetch existing user from your database
        user=info.context.user
        db_factory=info.context.db_factory
        async with db_factory() as db:
            friend_req=await FriendRequestNode.get(info, data.friend_id.node_id)
            friend_req.status=data.status
            db.add(friend_req)
            logger.debug('Committing database transaction')
            logger.debug('Committing database transaction')
            await db.commit()

    @strawberry.field(permission_classes=[IsAuthenticated])
    def logout(self, info: strawberry.Info) -> str:
        logger.info('enter logout')
        # Access the FastAPI Response object from context
        response = info.context.response
        response.delete_cookie(key="auth_token")
        logger.info('exit')
        return "Logged out successfully!"