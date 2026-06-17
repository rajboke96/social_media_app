import strawberry
from .graphql_inputs import UpdateUserInput, UserPostInput, UpdateFriendRequest
from typing import Optional
from .graphql_nodes import UserNode, UserPostNode, FriendRequestNode
from database import get_db, get_db_factory
from contextlib import contextmanager
from .context_permissions import IsAuthenticated
from social_media_app.schemas import Post, FriendRequestStatus, Friend, Media, MediaType
from datetime import datetime
from strawberry import relay
from datetime import date
import os
from database import UPLOAD_DIR
import uuid
from strawberry.relay.utils import from_base64
from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

@strawberry.type
class Mutation:
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def create_post(self, info: strawberry.Info, data: UserPostInput)->Optional[UserPostNode]:
        allowed_types = ["image/jpeg", "image/png", "image/webp"]
        saved_img_list=[]
        for img in data.image:
            if img.content_type not in allowed_types:
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
            public_image_url = f"/static/uploads/{unique_filename}"
            saved_img_list.append({
                "filename": unique_filename,
                "file_save_path": file_save_path,
                "public_image_url": public_image_url,
            })
        new_post=Post(title=data.title,
        description=data.description,
        # created_by=user_id,
        created_at=datetime.now(),
        visibility=data.visibility,
        )
        new_post.user=info.context.user
        for saved_img_data in saved_img_list:
            media=Media(
                name = saved_img_data["filename"],
                alt = data.alt,
                type=MediaType.IMAGE,
                uploaded_at = datetime.now(),
                uploaded_to = saved_img_data["file_save_path"],
                public_image_url=saved_img_data["public_image_url"]
            )
            media.user=info.context.user
            new_post.media.append(media)
        async with info.context.db_factory() as db:
            try:   
                db.add(new_post)
                await db.commit()
                # await db.refresh(new_post)
                return await UserPostNode.from_db(info, new_post)
            except Exception as e:
                # Rollback and clean up local file if the SQL execution fails
                await db.rollback()
                for saved_img_data in saved_img_list:
                    if os.path.exists(saved_img_data["file_save_path"]):
                        os.remove(saved_img_data["file_save_path"])
                raise Exception(f"Database error: {str(e)}")

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def delete_post(self, info: strawberry.Info, gid: relay.GlobalID)->str:
        db = info.context.db
        db_factory = info.context.db_factory 
        async with db_factory() as db:
            stmt = select(Post).options(selectinload(Post.media)).where(Post.id == gid.node_id).where(info.context.user.id==Post.created_by)
            result = await db.execute(stmt)
            user_post=result.scalar_one_or_none()
            if user_post:
                [await db.delete(m) for m in user_post.media]
                user_post.media=[]
                await db.delete(user_post)
                await db.commit()
                return f"{gid} deleted successfully!"
            else:
                raise HTTPException(404, f"{gid} post not found")

    @strawberry.field
    async def update_user(self, info: strawberry.Info, data: UpdateUserInput) -> Optional[UserNode]:
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
            await db.commit()
            return UserNode.from_db(user)

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def create_friend_request(self, info: strawberry.Info, user_id: relay.GlobalID) -> Optional[str]:
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
        await db.commit()

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def update_friend_request(self, info: strawberry.Info, data: UpdateFriendRequest) -> Optional[str]:
        # 1. Fetch existing user from your database
        user=info.context.user
        db_factory=info.context.db_factory
        async with db_factory() as db:
            friend_req=await FriendRequestNode.get(info, data.friend_id.node_id)
            friend_req.status=data.status
            print("db friend request object: ", friend_req)
            db.add(friend_req)
            await db.commit()
        