import strawberry
from .graphql_inputs import UpdateUserInput, UserPostInput, UpdateFriendRequest
from typing import Optional
from .graphql_nodes import UserNode, UserPostNode, FriendRequestNode
from database import get_db, get_db_factory
from contextlib import contextmanager
from .context_permissions import IsAuthenticated
from social_media_app.schemas import Post, FriendRequestStatus, Friend
from datetime import datetime
from strawberry import relay
from datetime import date

@strawberry.type
class Mutation:
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
    async def create_post(self, info: strawberry.Info, data: UserPostInput)->Optional[UserPostNode]:
        user_id=info.context.user.id
        user_post=Post(title=data.title,
            description=data.description,
            created_by=user_id,
            created_at=datetime.now(),
            visibility=data.visibility
            )
        async with info.context.db_factory() as db:
            db.add(user_post)
            await db.commit()
            return UserPostNode.from_db(info, user_post)

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
            # user=db.query(UserModel).filter(UserModel.id==user.id).first()
            friend_id=data.friend_id
            print("GlobalID - ", friend_id.node_id)
            friend_req_node=await friend_id.resolve_node(info)
            # print("Resolved Node: ", friend_req_node.user, friend_req_node.friend)
            friend_req=await FriendRequestNode.get(info, friend_req_node.resolve_id(info))
            friend_req.status=data.status
            print("db friend request object: ", friend_req)
            db.add(friend_req)
            await db.commit()
        