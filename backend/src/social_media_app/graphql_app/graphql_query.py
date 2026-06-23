import strawberry
from typing import List, Optional
from .graphql_nodes import UserNode, UserProfileNode, UserPostNode, UserSettingNode, FriendRequestNode, CommentNode
from .graphql_types import UserType
from .context_permissions import IsAuthenticated
from src.logger import get_logger
logger = get_logger(__name__)

from strawberry import relay
from social_media_app.schemas import UserRole, Friend, FriendRequestStatus, AccountStatus, AccountType, Gender, Visibility, Theme, MediaType
from social_media_app.schemas import User as UserModel, UserProfile, Post
from .query_inputs import Option
from sqlalchemy import select, or_, and_, func
from typing import List
from .helper import decode_cursor_to_offset
from sqlalchemy.orm import selectinload
from social_media_app.services.feed_service import get_user_feed

# 3. Define the Query Class (Read Operations)
@strawberry.type
class Query:
    # This provides the standard 'node(id: ID!)' field for refetching
    node: Optional[relay.Node] = relay.node()

    @strawberry.field(permission_classes=[IsAuthenticated])
    def me(self, info: strawberry.Info) -> UserType:
        logger.info('enter me')
        user = info.context.user
        logger.info('exit')
        return UserType(username=user.username, role=user.role.value)
    
    # @relay.connection(graphql_type=relay.ListConnection[UserNode], max_results=10, permission_classes=[IsAuthenticated])
    @strawberry.field(permission_classes=[IsAuthenticated])
    # @strawberry.field(permission_classes=[IsAuthenticated])
    async def UserConnection(self, info: strawberry.Info, first: Optional[int] = 10, after: Optional[str] = None) -> relay.ListConnection[UserNode]:
        db=info.context.db
        db_factory=info.context.db_factory
        async with db_factory() as db:
            # 2. Map Relay's cursor metadata into clean SQL bounds
            sql_offset = decode_cursor_to_offset(after)
            sql_limit = min(first, 50) if first else 10  # Protection ceiling
        
            # 3. Compile your database statement cleanly
            statement = (
                select(UserModel)
                .where(UserModel.role != UserRole.ADMIN)
                .order_by(UserModel.id.asc())  # Consistent sorting is mandatory
                .offset(sql_offset)
                .limit(sql_limit)
            )
            # 4. Await the DB result asynchronously over the network loop
            result = await db.execute(statement)
            users = result.scalars().all()
            
            nodes = [UserNode.from_db(info, user) for user in users]
            logger.info('exit')
            return relay.ListConnection.resolve_connection(
                nodes=nodes,
                info=info,
                after=after,
                first=first
            )
    
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def search_user(self, info: strawberry.Info, user_search_str: str, first: Optional[int] = 10, after: Optional[str] = None) -> relay.ListConnection[UserNode]:
        db_factory = info.context.db_factory
        async with db_factory() as db:
            sql_offset = decode_cursor_to_offset(after)
            sql_limit = min(first, 50) if first else 10
            search_pattern = f"%{user_search_str.strip().lower()}%"

            statement = (
                select(UserModel)
                .where(
                    UserModel.role != UserRole.ADMIN,
                    or_(
                        UserModel.username.ilike(search_pattern),
                        UserModel.firstname.ilike(search_pattern),
                        UserModel.Lastname.ilike(search_pattern),
                        UserModel.email_address.ilike(search_pattern)
                    )
                )
                .order_by(UserModel.id.asc())
                .offset(sql_offset)
                .limit(sql_limit)
            )
            result = await db.execute(statement)
            users = result.scalars().all()
            nodes = [UserNode.from_db(info, user) for user in users]
            logger.info('exit')
            return relay.ListConnection.resolve_connection(
                nodes=nodes,
                info=info,
                after=after,
                first=first
            )
    
    # @relay.connection(graphql_type=relay.ListConnection[UserProfileNode], max_results=10, permission_classes=[IsAuthenticated])
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def usersProfileConnection(self, info: strawberry.Info, first: Optional[int] = 10, after: Optional[str] = None) -> List[UserProfileNode]:
        logger.info('enter usersProfileConnection')
        db=info.context.db

        # 2. Map Relay's cursor metadata into clean SQL bounds
        sql_offset = decode_cursor_to_offset(after)
        sql_limit = min(first, 50) if first else 10  # Protection ceiling
    
        # 3. Compile your database statement cleanly
        statement = (
            select(UserProfile)
            .offset(sql_offset)
            .limit(sql_limit)
        )
        # 4. Await the DB result asynchronously over the network loop
        result = await db.execute(statement)
        users_profile = result.scalars().all()

        nodes = [UserProfileNode.from_db(info, profile) for profile in users_profile]
        logger.info('exit')
        return relay.ListConnection.resolve_connection(
            nodes=nodes,
            info=info,
            after=after,
            first=first
        )

    @strawberry.field(permission_classes=[IsAuthenticated])    
    async def user_profile(self, info: strawberry.Info) -> Optional[UserProfileNode]:
        logger.info('enter user_profile')
        user_id=info.context.user.id
        db_factory=info.context.db_factory
        async with db_factory() as db:
            statement=select(UserProfile).where(UserProfile.user_id==user_id).options(
                selectinload(UserProfile.profile_picture),
                selectinload(UserProfile.cover_picture),
                selectinload(UserProfile.user),
                selectinload(UserProfile.city)
            )
            result=await db.execute(statement)
            user_profile=result.scalar_one_or_none()
            logger.info('exit')
            return UserProfileNode.from_db(info, user_profile) if user_profile else None

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def get_user_profile(self, info: strawberry.Info, user_name: str) -> Optional[UserProfileNode]:
        logger.info('enter get_user_profile')
        db_factory = info.context.db_factory
        async with db_factory() as db:
            user_stmt = select(UserModel).where(UserModel.username == user_name)
            user_result = await db.execute(user_stmt)
            db_user = user_result.scalar_one_or_none()
            if not db_user:
                logger.info('exit')
                return None
            
            profile_stmt = select(UserProfile).where(UserProfile.user_id == db_user.id).options(
                selectinload(UserProfile.profile_picture),
                selectinload(UserProfile.cover_picture),
                selectinload(UserProfile.user),
                selectinload(UserProfile.city)
            )
            profile_result = await db.execute(profile_stmt)
            db_profile = profile_result.scalar_one_or_none()
            logger.info('exit')
            return UserProfileNode.from_db(info, db_profile) if db_profile else None
    
    # @relay.connection(graphql_type=relay.ListConnection[UserPostNode], max_results=10, permission_classes=[IsAuthenticated])
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def UsersPostConnection(self, info: strawberry.Info, first: Optional[int] = 10, after: Optional[str] = None, user_id: Optional[int] = None, username: Optional[str] = None)->relay.ListConnection[UserPostNode]:
        logger.info('enter UsersPostConnection')
        target_user_id = user_id
        if not target_user_id and username:
            db_factory = info.context.db_factory
            async with db_factory() as db:
                user_stmt = select(UserModel).where(UserModel.username == username)
                user_result = await db.execute(user_stmt)
                db_user = user_result.scalar_one_or_none()
                target_user_id = db_user.id if db_user else None
        if not target_user_id:
            target_user_id = info.context.user.id
        db=info.context.db

        db_factory = info.context.db_factory
        async with db_factory() as db:
            # 2. Map Relay's cursor metadata into clean SQL bounds
            sql_offset = decode_cursor_to_offset(after)
            sql_limit = min(first, 50) if first else 10  # Protection ceiling
        
            # 3. Compile your database statement cleanly
            statement = (
                select(Post)
                .where(Post.created_by==target_user_id)
                .options(selectinload(Post.user), selectinload(Post.media))
                .offset(sql_offset)
                .limit(sql_limit)
            )

            # 4. Await the DB result asynchronously over the network loop
            result = await db.execute(statement)
            user_posts = result.scalars().all()
            
            nodes = [await UserPostNode.from_db(info, post) for post in user_posts]
            # 7. CRITICAL FIX: Hand-deliver a pre-calculated connection package
            # This prevents Strawberry from triggering background database tasks
            logger.info('exit')
            return relay.ListConnection.resolve_connection(
                nodes=nodes,
                info=info,
                after=after,
                first=first
            )

    # @relay.connection(graphql_type=relay.ListConnection[FriendRequestNode], max_results=10, permission_classes=[IsAuthenticated])
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def UserFriendsConnection(self, info: strawberry.Info, first: Optional[int] = 10, after: Optional[str] = None, user_id: Optional[int] = None, username: Optional[str] = None)->relay.ListConnection[FriendRequestNode]:
        logger.info('enter UserFriendsConnection')
        target_user_id = user_id
        if not target_user_id and username:
            db_factory = info.context.db_factory
            async with db_factory() as db:
                user_stmt = select(UserModel).where(UserModel.username == username)
                user_result = await db.execute(user_stmt)
                db_user = user_result.scalar_one_or_none()
                target_user_id = db_user.id if db_user else None
        if not target_user_id:
            target_user_id = info.context.user.id
        db=info.context.db
        db_factory=info.context.db_factory
        async with db_factory() as db:
            sql_offset = decode_cursor_to_offset(after)
            sql_limit = min(first, 50) if first else 10  # Protection ceiling
            statement = (
                select(Friend)
                .where(Friend.user_id==target_user_id, Friend.status==FriendRequestStatus.ACCEPTED)
                .options(selectinload(Friend.user), selectinload(Friend.friend))
                .offset(sql_offset)
                .limit(sql_limit)
            )
            # 4. Await the DB result asynchronously over the network loop
            result = await db.execute(statement)
            friends = result.scalars().all()
            
            nodes = [FriendRequestNode.from_db(info, f) for f in friends]
            # 7. CRITICAL FIX: Hand-deliver a pre-calculated connection package
            # This prevents Strawberry from triggering background database tasks
            logger.info('exit')
            return relay.ListConnection.resolve_connection(
                nodes=nodes,
                info=info,
                after=after,
                first=first
            )
    
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def user_settings(self, info: strawberry.Info)->Optional[UserSettingNode]:
        logger.info('enter user_settings')
        user_id=info.context.user.id
        db_user_setting=await UserSettingNode.get(info, user_id)
        if db_user_setting:
            logger.info('exit')
            return UserSettingNode(id=db_user_setting.id,
                               user=UserNode.from_db(info, db_user=await UserNode.get(info, db_user_setting.user_id) if db_user_setting.user_id else None,
                               ), theme=db_user_setting.theme.value
            )

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def get_feeds_for_user(self, info: strawberry.Info, first: Optional[int] = 20, after: Optional[str] = None) -> relay.ListConnection[UserPostNode]:
        """
        Generate personalized feed for the user based on:
        - Posts from followed users (accepted friends)
        - User's own posts
        - Relevance score (likes, comments, recency)
        """
        logger.info('enter get_feeds_for_user')
        user_id = info.context.user.id
        db_factory = info.context.db_factory
        
        async with db_factory() as db:
            sql_offset = decode_cursor_to_offset(after)
            sql_limit = min(first, 50) if first else 20
            
            # Get feed posts using feed service
            feed_posts = await get_user_feed(
                db=db,
                user_id=user_id,
                limit=sql_limit,
                offset=sql_offset
            )
            
            nodes = [await UserPostNode.from_db(info, post) for post in feed_posts]
            logger.info('exit')
            return relay.ListConnection.resolve_connection(
                nodes=nodes,
                info=info,
                after=after,
                first=first
            )

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def get_user_post(self, info: strawberry.Info, post_id: relay.GlobalID) -> Optional[UserPostNode]:
        logger.info('enter get_user_post')
        db_factory = info.context.db_factory
        post_id=post_id.node_id
        async with db_factory() as db:
            statement = select(Post).where(Post.id == post_id).options(selectinload(Post.user), selectinload(Post.media))
            result = await db.execute(statement)
            post = result.scalar_one_or_none()
            if not post:
                logger.info('exit')
                return None
            logger.info('exit')
            return await UserPostNode.from_db(info, post)

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def get_user_profile(self, info: strawberry.Info, user_name: str) -> Optional[UserProfileNode]:
        logger.info('enter get_user_profile')
        db_factory = info.context.db_factory
        async with db_factory() as db:
            user_stmt = select(UserModel).where(UserModel.username == user_name)
            user_result = await db.execute(user_stmt)
            db_user = user_result.scalar_one_or_none()
            if not db_user:
                logger.info('exit')
                return None
            
            profile_stmt = select(UserProfile).where(UserProfile.user_id == db_user.id).options(
                selectinload(UserProfile.profile_picture),
                selectinload(UserProfile.cover_picture),
                selectinload(UserProfile.user),
                selectinload(UserProfile.city)
            )
            profile_result = await db.execute(profile_stmt)
            db_profile = profile_result.scalar_one_or_none()
            logger.info('exit')
            return UserProfileNode.from_db(info, db_profile) if db_profile else None

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def get_user_by_username(self, info: strawberry.Info, username: str) -> Optional[UserNode]:
        logger.info('enter get_user_by_username')
        db_factory = info.context.db_factory
        async with db_factory() as db:
            statement = select(UserModel).where(UserModel.username == username)
            result = await db.execute(statement)
            db_user = result.scalar_one_or_none()
            logger.info('exit')
            return UserNode.from_db(info, db_user) if db_user else None

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def get_user_friends_count(self, info: strawberry.Info, user_id: int) -> int:
        logger.info('enter get_user_friends_count')
        db_factory = info.context.db_factory
        async with db_factory() as db:
            statement = select(Friend).where(Friend.user_id == user_id, Friend.status == FriendRequestStatus.ACCEPTED)
            result = await db.execute(statement)
            friends = result.scalars().all()
            logger.info('exit')
            return len(friends)

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def get_user_posts_count(self, info: strawberry.Info, user_id: int) -> int:
        logger.info('enter get_user_posts_count')
        db_factory = info.context.db_factory
        async with db_factory() as db:
            statement = select(Post).where(Post.created_by == user_id)
            result = await db.execute(statement)
            posts = result.scalars().all()
            logger.info('exit')
            return len(posts)

    @strawberry.field
    def get_options(self, option: Option)->List[str]:
        logger.info('enter get_options')
        if option == Option.ACCOUNT_STATUS:
            logger.info('exit')
            return AccountStatus._member_names_
        elif option == Option.ACCOUNT_TYPE:
            logger.info('exit')
            return AccountType._member_names_
        elif option == Option.VISIBILITY:
            logger.info('exit')
            return Visibility._member_names_
        elif option == Option.GENDER:
            logger.info('exit')
            return Gender._member_names_
        elif option == Option.THEME:
            logger.info('exit')
            return Theme._member_names_
        elif option == Option.MEDIA_TYPE:
            logger.info('exit')
            return MediaType._member_names_
