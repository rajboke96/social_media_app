import strawberry
from .user import UserNode
from datetime import datetime
from social_media_app.schemas import Visibility, Post, Friend, FriendRequestStatus
from strawberry import relay
from typing import Iterable, List

@strawberry.type
class FriendRequestNode(relay.Node):
    user: UserNode
    friend: UserNode
    friends_at: datetime
    status: FriendRequestStatus

    def resolve_id(self, info: strawberry.Info) -> str:
        # Combine your composite keys into a single string
        # Strawberry will then encode this into a global Relay ID
        return f"{self.user.id}:{self.friend.id}"

    @classmethod
    def resolve_nodes(
        cls, *, info: strawberry.Info, node_ids: Iterable[str], required: bool = False
    ) -> List["FriendRequestNode"]:
        # This method is called when refetching via the 'node' query
        # Strawberry automatically decodes the Base64 IDs back to 'int' node_ids
        results = []
        for nid in node_ids:
            uid, fid = nid.split(":")
            data = FriendRequestNode.get(info, nid)
            if data:
                results.append(FriendRequestNode.from_db(info, data))
        return results

    @staticmethod
    def get(info: strawberry.Info, nid):
        uid, fid = nid.split(":")
        db=info.context.db
        db_user=db.query(Friend).filter(Friend.user_id==uid, Friend.friend_id==fid).first()
        if db_user:
            return db_user
    
    @staticmethod
    def from_db(info: strawberry.Info, db_user:Post)->"FriendRequestNode":
        return FriendRequestNode(friends_at=db_user.friends_at,
            user=UserNode.from_db(info, UserNode.get(info, db_user.user_id)),
            friend=UserNode.from_db(info, UserNode.get(info, db_user.friend_id)),
            status=db_user.status.value
        )