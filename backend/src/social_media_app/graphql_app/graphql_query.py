import strawberry
from typing import List, Optional, Iterable
from .graphql_nodes import UserNode, UserProfileNode, UserPostNode, UserSettingNode, FriendRequestNode
from .graphql_types import UserType
from .context_permissions import IsAuthenticated, IsAdmin
from datetime import datetime
from strawberry import relay
from social_media_app.schemas import UserRole, Friend, AccountStatus, AccountType, Gender, Visibility, Theme, MediaType
from social_media_app.schemas import User as UserModel, UserProfile, Post
from .query_inputs import Option

class LazyQuery:
    def __init__(self, info, query, mapper):
        self.info=info
        self.query = query
        self.mapper=mapper

    def __getitem__(self, key: slice):
        print("__getitem__ is called!")
        print("Key: ", key)
        # Translates [0:10] into .slice(0, 10) for the DB
        if isinstance(key, slice):
            results = self.query.slice(key.start, key.stop).all()
            # Map ORM models to GraphQL Types here
            res= [self.mapper(self.info, u) for u in results]
            return res
        raise TypeError("Slicing only")

    def __iter__(self):
        print("__iter__ is called!")
        raise Exception("Error in pagination!")
        # for row in self.query:
        #     print("Row - ", self.mapper(self.info, row))
        #     yield self.mapper(self.info, row)

# 3. Define the Query Class (Read Operations)
@strawberry.type
class Query:
    # This provides the standard 'node(id: ID!)' field for refetching
    node: Optional[relay.Node] = relay.node()

    @strawberry.field(permission_classes=[IsAuthenticated])
    def me(self, info: strawberry.Info) -> UserType:
        user = info.context.user
        return UserType(username=user.username, role=user.role.value)
    
    @relay.connection(graphql_type=relay.ListConnection[UserNode], max_results=10, permission_classes=[IsAuthenticated])
    # @strawberry.field(permission_classes=[IsAuthenticated])
    def all_users(self, info: strawberry.Info) -> Iterable[UserNode]:
        db=info.context.db
        query_obj=db.query(UserModel).filter(UserModel.role!=UserRole.ADMIN)
        return LazyQuery(info, query_obj, UserNode.from_db)
 
    # @strawberry.field(permission_classes=[IsAuthenticated])
    def search_user(self, user_search_str: str) -> List[UserNode]:
        pass
    
    @relay.connection(graphql_type=relay.ListConnection[UserProfileNode], max_results=10, permission_classes=[IsAuthenticated])
    def all_users_profile(self, info: strawberry.Info) -> Iterable[UserProfileNode]:
        db=info.context.db
        query_obj=db.query(UserProfile)
        return LazyQuery(info, query_obj, UserProfileNode.from_db)
    
    @relay.connection(graphql_type=relay.ListConnection[UserProfileNode], max_results=10, permission_classes=[IsAuthenticated])
    def user_profile(self, info: strawberry.Info) -> Iterable[UserProfileNode]:
        user_id=info.context.user.id
        db=info.context.db
        query_obj=db.query(UserProfile).filter(UserProfile.user_id==user_id)
        return LazyQuery(query_obj, UserProfileNode.from_db)
    
    @relay.connection(graphql_type=relay.ListConnection[UserPostNode], max_results=10, permission_classes=[IsAuthenticated])
    def all_User_posts(self, info: strawberry.Info)->Iterable[UserPostNode]:
        user_id=info.context.user.id
        db=info.context.db
        query_obj=db.query(Post).filter(Post.created_by==user_id)
        return LazyQuery(info, query_obj, UserPostNode.from_db)

    @relay.connection(graphql_type=relay.ListConnection[FriendRequestNode], max_results=10, permission_classes=[IsAuthenticated])
    def all_User_friends(self, info: strawberry.Info)->Iterable[FriendRequestNode]:
        user_id=info.context.user.id
        db=info.context.db
        query_obj=db.query(Friend).filter(Friend.user_id==user_id)
        return LazyQuery(info, query_obj, FriendRequestNode.from_db)
    
    @strawberry.field(permission_classes=[IsAuthenticated])
    def user_settings(self, info: strawberry.Info)->Optional[UserSettingNode]:
        user_id=info.context.user.id
        db_user_setting=UserSettingNode.get_user_setting(info, user_id)
        if db_user_setting:
            return UserSettingNode(id=db_user_setting.id,
                               user=UserNode.from_db(UserSettingNode.get_user_setting(info, db_user_setting.user_id)) if db_user_setting.user_id else None,
                               theme=db_user_setting.theme.value)

    @strawberry.field(permission_classes=[IsAuthenticated])
    def get_feeds_for_user(self, info:strawberry.Info)->None:
        """
            feeds -> posts, ad, suggested friends
            posts -> location, most viewed posts, friends liked posts
        """
        pass

    @strawberry.field
    def get_options(self, option: Option)->List[str]:
        if option == Option.ACCOUNT_STATUS:
            return AccountStatus._member_names_
        elif option == Option.ACCOUNT_TYPE:
            return AccountType._member_names_
        elif option == Option.VISIBILITY:
            return Visibility._member_names_
        elif option == Option.GENDER:
            return Gender._member_names_
        elif option == Option.THEME:
            return Theme._member_names_
        elif option == Option.MEDIA_TYPE:
            return MediaType._member_names_
