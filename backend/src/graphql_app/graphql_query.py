import strawberry
from typing import List, Optional, Iterable
from .graphql_nodes import UserNode, UserProfileNode, UserPostNode, UserSettingNode
from .graphql_types import UserType
from .context_permissions import IsAuthenticated, IsAdmin
from datetime import datetime
from strawberry import relay
from social_media_app.schemas import User as UserModel, UserProfile, Post

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
        return UserType(username=user.username, role=user.role)
    
    @relay.connection(graphql_type=relay.ListConnection[UserNode], max_results=1, permission_classes=[IsAuthenticated])
    # @strawberry.field(permission_classes=[IsAuthenticated])
    def all_users(self, info: strawberry.Info) -> Iterable[UserNode]:
        db=info.context.db
        query_obj=db.query(UserModel)
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

    
    @strawberry.field(permission_classes=[IsAuthenticated])
    def user_settings(self, info: strawberry.Info)->Optional[UserSettingNode]:
        user_id=info.context.user.id
        db_user_setting=UserSettingNode.get_user_setting(info, user_id)
        if db_user_setting:
            return UserSettingNode(id=db_user_setting.id,
                               user=UserNode.from_db(UserSettingNode.get_user_setting(info, db_user_setting.user_id)) if db_user_setting.user_id else None,
                               theme=db_user_setting.theme.value)

    @strawberry.field
    def account_status_options(self)->List[str]:
        return ["active", "suspended", "inactive"]
    
    @strawberry.field
    def visibility_options(self)->List[str]:
        return ["private", "friends", "public"]

    @strawberry.field
    def account_type_options(self)->List[str]:
        return ["private", "public"]
    
    @strawberry.field
    def gender_options(self)->List[str]:
        return ["male", "female", "other"]
    
    @strawberry.field
    def media_options(self)->List[str]:
        return ["image", "video"]
    
    @strawberry.field
    def theme_options(self)->List[str]:
        return ["light", "dark"]
 